#!/usr/bin/env python3
"""
Weather Market Price Tracker
Logs NOAA KLGA forecast + Polymarket prices daily for forward backtesting.
Aligned to 1.0 strategy: NOAA weather.gov is the forecast source.
"""

import json
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

TRACKER_FILE = Path(__file__).parent / "price_log.jsonl"


def fetch_noaa_forecast():
    """Get NOAA KLGA forecast from weather.gov API.
    Returns dict of {iso_date: high_temp_F}"""
    points_url = "https://api.weather.gov/points/40.7772,-73.8726"
    r = subprocess.run(
        ["curl", "-s", "-H", "User-Agent: clawdine-weather-trader", points_url],
        capture_output=True, text=True
    )
    try:
        points = json.loads(r.stdout)
        forecast_url = points["properties"]["forecast"]
    except (json.JSONDecodeError, KeyError):
        print("ERROR: Failed to get NOAA forecast URL")
        return {}

    r = subprocess.run(
        ["curl", "-s", "-H", "User-Agent: clawdine-weather-trader", forecast_url],
        capture_output=True, text=True
    )
    try:
        fc = json.loads(r.stdout)
    except json.JSONDecodeError:
        print("ERROR: Failed to parse NOAA forecast")
        return {}

    result = {}
    for period in fc.get("properties", {}).get("periods", []):
        if period.get("isDaytime"):
            date_str = period["startTime"][:10]
            temp = period["temperature"]
            if period.get("temperatureUnit", "F") == "C":
                temp = temp * 9 / 5 + 32
            result[date_str] = temp
    return result


def fetch_market_prices(date_str):
    """Fetch Polymarket prices for a specific date (format: february-8-2026)"""
    slug = f"highest-temperature-in-nyc-on-{date_str}"
    url = f"https://gamma-api.polymarket.com/events?slug={slug}"
    result = subprocess.run(["curl", "-s", url], capture_output=True, text=True)
    clean = re.sub(r'[\x00-\x1f]', '', result.stdout)
    try:
        data = json.loads(clean)
        if not data:
            return None
        return data[0]
    except Exception:
        return None


def extract_buckets(event_data):
    """Extract price buckets from event data"""
    if not event_data or 'markets' not in event_data:
        return {}

    buckets = {}
    for market in event_data['markets']:
        question = market.get('question', '')
        prices = json.loads(market.get('outcomePrices', '["0","0"]'))
        yes_price = float(prices[0])

        if 'between' in question:
            match = re.search(r'between (\d+)-(\d+)°F', question)
            if match:
                buckets[f"{match.group(1)}-{match.group(2)}"] = yes_price
        elif 'or higher' in question:
            match = re.search(r'(\d+)°F or higher', question)
            if match:
                buckets[f">={match.group(1)}"] = yes_price
        elif 'or below' in question:
            match = re.search(r'(\d+)°F or below', question)
            if match:
                buckets[f"<={match.group(1)}"] = yes_price

    return buckets


def log_snapshot():
    """Take a snapshot of current NOAA forecast + market prices"""
    now = datetime.now()

    forecasts = fetch_noaa_forecast()
    if not forecasts:
        print("No NOAA forecast data — aborting")
        return []

    print(f"NOAA KLGA forecasts: {', '.join(f'{d}: {t}°F' for d, t in sorted(forecasts.items()))}\n")

    entries = []

    for i in range(1, 6):
        target_date = now + timedelta(days=i)
        date_str = target_date.strftime('%B-%-d-%Y').lower()
        iso_date = target_date.strftime('%Y-%m-%d')

        forecast_temp = forecasts.get(iso_date)
        if not forecast_temp:
            continue

        event = fetch_market_prices(date_str)
        if not event:
            continue

        buckets = extract_buckets(event)

        entry = {
            'timestamp': now.isoformat(),
            'target_date': iso_date,
            'forecast_source': 'NOAA_KLGA',
            'forecast_high_f': forecast_temp,
            'market_buckets': buckets,
            'days_until': i
        }
        entries.append(entry)

        if buckets:
            max_bucket = max(buckets, key=buckets.get)
            max_prob = buckets[max_bucket]
            entry['market_implied'] = max_bucket
            entry['market_confidence'] = max_prob

            print(f"{iso_date} (+{i}d): NOAA {forecast_temp:.0f}°F | Market favors {max_bucket} @ {max_prob:.1%}")

    with open(TRACKER_FILE, 'a') as f:
        for entry in entries:
            f.write(json.dumps(entry) + '\n')

    print(f"\nLogged {len(entries)} entries to {TRACKER_FILE}")
    return entries


if __name__ == '__main__':
    print(f"=== Weather Market Snapshot: {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")
    print(f"Source: NOAA weather.gov KLGA\n")
    log_snapshot()
