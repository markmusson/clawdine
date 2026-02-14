#!/usr/bin/env python3
"""
Weather Market Backtest
Compares forecasts vs market prices vs actual resolutions.
Simulates the gap-trading strategy: bet against market when forecast diverges.

Strategy: When forecast temp differs from market-implied temp by ≥3°F,
bet on the bucket closest to the forecast.
"""

import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

BACKTEST_DIR = Path(__file__).parent
PRICE_LOG = BACKTEST_DIR / "price_log.jsonl"
BET_SIZE = 50  # dollars per trade


def get_actual_temps(start_date, end_date):
    """Fetch actual KLGA high temperatures from NOAA weather.gov API
    This is the same station Polymarket resolves against (via Wunderground/KLGA)."""
    from datetime import timedelta as td

    results = {}
    current = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    while current <= end:
        ds = current.strftime("%Y-%m-%d")
        url = (f"https://api.weather.gov/stations/KLGA/observations"
               f"?start={ds}T00:00:00Z&end={ds}T23:59:59Z&limit=100")
        r = subprocess.run(
            ["curl", "-s", "-H", "User-Agent: weather-backtest", url],
            capture_output=True, text=True
        )
        try:
            data = json.loads(r.stdout)
            temps = []
            for obs in data.get("features", []):
                t = obs.get("properties", {}).get("temperature", {}).get("value")
                if t is not None:
                    temps.append(t * 9 / 5 + 32)  # C to F
            if temps:
                results[ds] = round(max(temps))  # whole degrees like Wunderground
        except Exception:
            pass
        current += td(days=1)

    return results


def get_resolution(date_str):
    """Get market resolution for a date (e.g. 'february-8-2026')"""
    slug = f"highest-temperature-in-nyc-on-{date_str}"
    url = f"https://gamma-api.polymarket.com/events?slug={slug}"
    r = subprocess.run(["curl", "-s", url], capture_output=True, text=True)
    clean = re.sub(r'[\x00-\x1f]', '', r.stdout)
    try:
        data = json.loads(clean)
    except Exception:
        return None
    if not data:
        return None

    for m in data[0].get("markets", []):
        prices = json.loads(m.get("outcomePrices", '["0","0"]'))
        if prices[0] == "1":
            return m["question"]
    return None


def parse_bucket_midpoint(bucket_str):
    """Convert bucket like '18-19' or '>=36' or '<=15' to midpoint"""
    if ">=" in bucket_str:
        val = float(bucket_str.replace(">=", ""))
        return val + 1  # assume 1°F above threshold
    elif "<=" in bucket_str:
        val = float(bucket_str.replace("<=", ""))
        return val - 1
    elif "-" in bucket_str:
        lo, hi = bucket_str.split("-")
        return (float(lo) + float(hi)) / 2
    return None


def implied_temp(buckets):
    """Calculate probability-weighted implied temperature"""
    total_prob = sum(buckets.values())
    if total_prob == 0:
        return None
    weighted = sum(parse_bucket_midpoint(b) * p for b, p in buckets.items()
                   if parse_bucket_midpoint(b) is not None)
    return weighted / total_prob


def find_best_bucket(buckets, target_temp):
    """Find the bucket closest to target temperature"""
    best = None
    best_dist = float("inf")
    for b in buckets:
        mid = parse_bucket_midpoint(b)
        if mid is not None:
            dist = abs(mid - target_temp)
            if dist < best_dist:
                best_dist = dist
                best = b
    return best


def resolution_matches_bucket(resolution_question, bucket_str):
    """Check if resolution matches a bucket"""
    if not resolution_question:
        return False

    # Parse resolution
    if "between" in resolution_question:
        match = re.search(r"between (\d+)-(\d+)", resolution_question)
        if match:
            res_key = f"{match.group(1)}-{match.group(2)}"
            return res_key == bucket_str
    elif "or higher" in resolution_question:
        match = re.search(r"(\d+)°F or higher", resolution_question)
        if match:
            return bucket_str == f">={match.group(1)}"
    elif "or below" in resolution_question:
        match = re.search(r"(\d+)°F or below", resolution_question)
        if match:
            return bucket_str == f"<={match.group(1)}"
    return False


def run_backtest():
    """Run the backtest"""
    # Load price log
    snapshots = []
    with open(PRICE_LOG) as f:
        for line in f:
            snapshots.append(json.loads(line.strip()))

    # Group by target date, take latest snapshot per date
    by_date = {}
    for s in snapshots:
        date = s["target_date"]
        if date not in by_date or s["timestamp"] > by_date[date]["timestamp"]:
            by_date[date] = s

    # Get actual temps (only for past dates)
    dates = sorted(by_date.keys())
    today = datetime.now().strftime("%Y-%m-%d")
    past_dates = [d for d in dates if d < today]
    actuals = get_actual_temps(past_dates[0], past_dates[-1]) if past_dates else {}

    print("=" * 70)
    print("WEATHER MARKET BACKTEST")
    print("Strategy: Bet on forecast bucket when gap ≥ 3°F")
    print(f"Bet size: ${BET_SIZE}")
    print("=" * 70)

    total_pnl = 0
    trades = 0
    wins = 0

    for date in dates:
        snap = by_date[date]
        buckets = snap["market_buckets"]
        forecast = snap["forecast_high_f"]
        mkt_implied = implied_temp(buckets)
        actual = actuals.get(date)

        # Get resolution
        dt = datetime.strptime(date, "%Y-%m-%d")
        date_slug = dt.strftime("%B-%-d-%Y").lower()
        resolution = get_resolution(date_slug)

        gap = abs(forecast - mkt_implied) if mkt_implied else 0

        print(f"\n{'─'*70}")
        print(f"📅 {date}")
        print(f"  Forecast:       {forecast:.1f}°F")
        print(f"  Market implied: {mkt_implied:.1f}°F" if mkt_implied else "  Market implied: N/A")
        print(f"  Gap:            {gap:.1f}°F {'⚠️  SIGNAL' if gap >= 3 else ''}")
        print(f"  Actual (OMeteo):{actual:.1f}°F" if actual else "  Actual: pending")
        print(f"  Resolution:     {resolution or 'pending'}")

        # Show all buckets
        print(f"  Buckets: ", end="")
        for b, p in sorted(buckets.items(), key=lambda x: parse_bucket_midpoint(x[0]) or 0):
            print(f"{b}={p:.1%} ", end="")
        print()

        # Simulate trade if gap >= 3°F
        if gap >= 3 and resolution:
            target_bucket = find_best_bucket(buckets, forecast)
            entry_price = buckets.get(target_bucket, 0)

            won = resolution_matches_bucket(resolution, target_bucket)
            if won:
                pnl = BET_SIZE * (1 / entry_price - 1) if entry_price > 0 else 0
                wins += 1
            else:
                pnl = -BET_SIZE

            total_pnl += pnl
            trades += 1

            print(f"  🎯 TRADE: YES on {target_bucket} @ {entry_price:.1%}")
            print(f"  {'✅ WIN' if won else '❌ LOSS'}: ${pnl:+,.0f}")
        elif gap >= 3:
            print(f"  📋 Would trade {find_best_bucket(buckets, forecast)} — awaiting resolution")
        else:
            print(f"  ⏸️  No trade (gap < 3°F)")

    # Summary
    wr = (wins / trades * 100) if trades > 0 else 0
    print(f"\n{'='*70}")
    print(f"SUMMARY")
    print(f"  Trades:    {trades}")
    print(f"  Wins:      {wins} ({wr:.0f}%)")
    print(f"  Total P&L: ${total_pnl:+,.0f}")
    print(f"  Per trade: ${total_pnl/trades:+,.0f}" if trades else "")
    print(f"{'='*70}")

    # Key observations
    print(f"\nOBSERVATIONS:")
    for date in dates:
        snap = by_date[date]
        forecast = snap["forecast_high_f"]
        mkt_implied = implied_temp(snap["market_buckets"])
        actual = actuals.get(date)
        if actual and mkt_implied:
            forecast_err = abs(forecast - actual)
            market_err = abs(mkt_implied - actual)
            better = "Forecast" if forecast_err < market_err else "Market"
            print(f"  {date}: Forecast err {forecast_err:.1f}°F, Market err {market_err:.1f}°F → {better} was closer")


if __name__ == "__main__":
    run_backtest()
