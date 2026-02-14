#!/usr/bin/env python3
"""
Intraday KLGA Observation Monitor
Checks current KLGA temperature against today's market pricing.
Identifies same-day opportunities when observations diverge from market expectations.
Runs via cron every 1-2 hours during NYC daytime (12:00-22:00 UTC / 7am-5pm EST).
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw/workspace"
LOG_FILE = WORKSPACE / "trading/intraday_log.jsonl"
STATS_FILE = WORKSPACE / "trading/weather_paper_stats.json"


def get_klga_observations_today():
    """Get all KLGA observations for today"""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    url = (f"https://api.weather.gov/stations/KLGA/observations"
           f"?start={today}T00:00:00Z&end={today}T23:59:59Z&limit=200")
    r = subprocess.run(
        ["curl", "-s", "-H", "User-Agent: clawdine-weather-trader", url],
        capture_output=True, text=True
    )
    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError:
        return []

    temps = []
    for obs in data.get("features", []):
        t = obs["properties"]["temperature"]["value"]
        ts = obs["properties"]["timestamp"]
        if t is not None:
            temps.append({"time": ts, "temp_f": round(t * 9 / 5 + 32, 1)})

    temps.sort(key=lambda x: x["time"])
    return temps


def get_noaa_forecast_today():
    """Get NOAA forecast high for today"""
    url = "https://api.weather.gov/points/40.7772,-73.8726"
    r = subprocess.run(
        ["curl", "-s", "-H", "User-Agent: clawdine-weather-trader", url],
        capture_output=True, text=True
    )
    try:
        points = json.loads(r.stdout)
        fc_url = points["properties"]["forecast"]
    except (json.JSONDecodeError, KeyError):
        return None

    r2 = subprocess.run(
        ["curl", "-s", "-H", "User-Agent: clawdine-weather-trader", fc_url],
        capture_output=True, text=True
    )
    try:
        fc = json.loads(r2.stdout)
        for period in fc["properties"]["periods"]:
            if period.get("isDaytime"):
                return {
                    "high": period["temperature"],
                    "name": period["name"],
                    "detail": period["detailedForecast"]
                }
    except (json.JSONDecodeError, KeyError):
        return None
    return None


def get_today_market():
    """Get today's Polymarket weather market"""
    now = datetime.now()
    date_slug = now.strftime("%B-%-d-%Y").lower()
    url = f"https://gamma-api.polymarket.com/events?slug=highest-temperature-in-nyc-on-{date_slug}"
    r = subprocess.run(["curl", "-s", url], capture_output=True, text=True)
    clean = re.sub(r"[\x00-\x1f]", "", r.stdout)
    try:
        data = json.loads(clean)
        if data:
            return data[0]
    except json.JSONDecodeError:
        pass
    return None


def extract_buckets(event):
    """Extract bucket prices"""
    if not event or "markets" not in event:
        return {}

    buckets = {}
    for m in event["markets"]:
        q = m.get("question", "")
        prices = json.loads(m.get("outcomePrices", '["0","0"]'))
        yes = float(prices[0])
        if "between" in q:
            match = re.search(r"between (\d+)-(\d+)", q)
            if match:
                buckets[f"{match.group(1)}-{match.group(2)}"] = yes
        elif "or higher" in q:
            match = re.search(r"(\d+)°F or higher", q)
            if match:
                buckets[f">={match.group(1)}"] = yes
        elif "or below" in q:
            match = re.search(r"(\d+)°F or below", q)
            if match:
                buckets[f"<={match.group(1)}"] = yes
    return buckets


def estimate_peak(temps):
    """Estimate likely peak temp based on observations so far"""
    if len(temps) < 3:
        return None

    current = temps[-1]["temp_f"]
    high_so_far = max(t["temp_f"] for t in temps)

    # Calculate recent warming rate (last hour of readings)
    recent = [t for t in temps if t["time"] >= temps[-1]["time"][:14]]
    if len(recent) >= 2:
        rate_per_hour = (recent[-1]["temp_f"] - recent[0]["temp_f"])
    else:
        rate_per_hour = 0

    # Hours until typical NYC peak (2pm EST = 19:00 UTC)
    now_utc = datetime.now(timezone.utc)
    peak_hour = 19  # 2pm EST
    hours_left = max(0, peak_hour - now_utc.hour + (0 if now_utc.minute < 30 else 0.5))

    if hours_left <= 0:
        # Past peak time — high is probably in
        return {"estimate": high_so_far, "confidence": "high", "hours_left": 0,
                "rate": rate_per_hour, "high_so_far": high_so_far}

    # Linear extrapolation (conservative)
    estimated_peak = current + (rate_per_hour * hours_left)
    # Don't go below high already observed
    estimated_peak = max(estimated_peak, high_so_far)

    confidence = "low" if hours_left > 4 else ("medium" if hours_left > 2 else "high")

    return {
        "estimate": round(estimated_peak, 1),
        "confidence": confidence,
        "hours_left": round(hours_left, 1),
        "rate": round(rate_per_hour, 1),
        "high_so_far": high_so_far
    }


def find_bucket_for_temp(buckets, temp):
    """Find which bucket a temperature falls into"""
    rounded = round(temp)
    for key in buckets:
        if "-" in key and not key.startswith(">=") and not key.startswith("<="):
            lo, hi = key.split("-")
            if int(lo) <= rounded <= int(hi):
                return key
        elif key.startswith(">="):
            threshold = int(key[2:])
            if rounded >= threshold:
                return key
        elif key.startswith("<="):
            threshold = int(key[2:])
            if rounded <= threshold:
                return key
    return None


def main():
    now = datetime.now(timezone.utc)
    print(f"=== Intraday KLGA Monitor: {now.strftime('%Y-%m-%d %H:%M')} UTC ===\n")

    # Get data
    temps = get_klga_observations_today()
    forecast = get_noaa_forecast_today()
    event = get_today_market()
    buckets = extract_buckets(event)

    if not temps:
        print("No observations yet today")
        return 0

    high_so_far = max(t["temp_f"] for t in temps)
    current = temps[-1]["temp_f"]
    peak_est = estimate_peak(temps)

    print(f"KLGA current: {current}°F | High so far: {high_so_far}°F")
    if forecast:
        print(f"NOAA forecast: {forecast['high']}°F")
    if peak_est:
        print(f"Estimated peak: {peak_est['estimate']}°F ({peak_est['confidence']} confidence)")
        print(f"  Warming rate: {peak_est['rate']}°F/hr | Hours to peak: {peak_est['hours_left']}")

    if not buckets:
        print("\nNo market data available")
        return 0

    print(f"\nMarket buckets:")
    for b, p in sorted(buckets.items(), key=lambda x: -x[1]):
        if p >= 0.01:
            marker = ""
            if peak_est and find_bucket_for_temp(buckets, peak_est["estimate"]) == b:
                marker = " ← EST. PEAK"
            print(f"  {b}: {p:.1%}{marker}")

    # Identify opportunity
    if peak_est and peak_est["confidence"] in ("medium", "high"):
        est_bucket = find_bucket_for_temp(buckets, peak_est["estimate"])
        if est_bucket:
            est_price = buckets.get(est_bucket, 0)
            # Market favored bucket
            market_fav = max(buckets, key=buckets.get)
            market_fav_price = buckets[market_fav]

            if est_bucket != market_fav and est_price < 0.30:
                print(f"\n🚨 OPPORTUNITY: Market favors {market_fav} ({market_fav_price:.0%}) "
                      f"but observations suggest {est_bucket} ({est_price:.1%})")

    # Log
    snapshot = {
        "timestamp": now.isoformat(),
        "current_f": current,
        "high_so_far": high_so_far,
        "noaa_forecast": forecast["high"] if forecast else None,
        "peak_estimate": peak_est,
        "buckets": buckets
    }
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(snapshot) + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
