#!/usr/bin/env python3
"""
Weather Market Gap Detector
Alerts when NOAA KLGA forecast diverges >3°F from market-implied temperature.
Uses weather.gov API (same source chain as Polymarket resolution).
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timedelta

ALERT_THRESHOLD_F = 3.0


def fetch_noaa_forecast():
    """Get NOAA forecast for KLGA from weather.gov API.
    Returns dict of {date_str: high_temp_F}"""
    # Step 1: Get forecast URL for KLGA coordinates
    points_url = "https://api.weather.gov/points/40.7772,-73.8726"
    r = subprocess.run(
        ["curl", "-s", "-H", "User-Agent: clawdine-weather-trader", points_url],
        capture_output=True, text=True
    )
    try:
        points = json.loads(r.stdout)
        forecast_url = points["properties"]["forecast"]
    except (json.JSONDecodeError, KeyError):
        print("ERROR: Failed to get forecast URL from weather.gov")
        return {}

    # Step 2: Get forecast periods
    r = subprocess.run(
        ["curl", "-s", "-H", "User-Agent: clawdine-weather-trader", forecast_url],
        capture_output=True, text=True
    )
    try:
        fc = json.loads(r.stdout)
    except json.JSONDecodeError:
        print("ERROR: Failed to parse forecast data")
        return {}

    # Extract daytime highs (isDaytime=True periods)
    result = {}
    for period in fc.get("properties", {}).get("periods", []):
        if period.get("isDaytime"):
            # Parse the date from startTime (e.g. "2026-02-10T07:00:00-05:00")
            start = period["startTime"]
            date_str = start[:10]  # YYYY-MM-DD
            temp = period["temperature"]
            unit = period.get("temperatureUnit", "F")
            if unit == "C":
                temp = temp * 9 / 5 + 32
            result[date_str] = temp
    return result


def fetch_market(date_str):
    """Fetch market prices for date (format: february-8-2026)"""
    slug = f"highest-temperature-in-nyc-on-{date_str}"
    url = f"https://gamma-api.polymarket.com/events?slug={slug}"
    result = subprocess.run(["curl", "-s", url], capture_output=True, text=True)
    clean = re.sub(r'[\x00-\x1f]', '', result.stdout)
    try:
        data = json.loads(clean)
        if not data or not data[0].get('markets'):
            return None
        return data[0]
    except Exception:
        return None


def calc_implied_temp(event):
    """Calculate probability-weighted implied temperature from market"""
    if not event or 'markets' not in event:
        return None

    weighted_sum = 0
    total_prob = 0

    for market in event['markets']:
        question = market.get('question', '')
        prices = json.loads(market.get('outcomePrices', '["0","0"]'))
        yes_prob = float(prices[0])

        if 'between' in question:
            match = re.search(r'between (\d+)-(\d+)°F', question)
            if match:
                midpoint = (int(match.group(1)) + int(match.group(2))) / 2
                weighted_sum += midpoint * yes_prob
                total_prob += yes_prob
        elif 'or higher' in question:
            match = re.search(r'(\d+)°F or higher', question)
            if match:
                midpoint = int(match.group(1)) + 5
                weighted_sum += midpoint * yes_prob
                total_prob += yes_prob
        elif 'or below' in question:
            match = re.search(r'(\d+)°F or below', question)
            if match:
                midpoint = int(match.group(1)) - 5
                weighted_sum += midpoint * yes_prob
                total_prob += yes_prob

    if total_prob > 0:
        return weighted_sum / total_prob
    return None


def check_gaps():
    """Check all upcoming markets for gaps"""
    now = datetime.now()
    forecasts = fetch_noaa_forecast()

    if not forecasts:
        print("WARNING: No NOAA forecast data available")
        return []

    print(f"NOAA KLGA forecast periods: {', '.join(f'{d}: {t}°F' for d, t in sorted(forecasts.items()))}\n")

    alerts = []

    for i in range(1, 4):  # Check next 3 days
        target = now + timedelta(days=i)
        date_slug = target.strftime('%B-%-d-%Y').lower()
        iso_date = target.strftime('%Y-%m-%d')

        forecast_temp = forecasts.get(iso_date)
        if not forecast_temp:
            print(f"{iso_date}: No NOAA forecast available")
            continue

        event = fetch_market(date_slug)
        if not event:
            print(f"{iso_date}: No Polymarket event found")
            continue

        implied_temp = calc_implied_temp(event)
        if not implied_temp:
            print(f"{iso_date}: Could not calculate implied temp")
            continue

        gap = abs(forecast_temp - implied_temp)
        direction = "warmer" if implied_temp > forecast_temp else "colder"

        print(f"{iso_date}: NOAA {forecast_temp:.0f}°F | Market implies {implied_temp:.1f}°F | Gap: {gap:.1f}°F ({direction})")

        if gap >= ALERT_THRESHOLD_F:
            alerts.append({
                'date': iso_date,
                'forecast': forecast_temp,
                'market_implied': round(implied_temp, 1),
                'gap': round(gap, 1),
                'direction': direction
            })

    return alerts


def main():
    print(f"=== Gap Alert Check: {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")
    print(f"Source: NOAA weather.gov KLGA | Threshold: {ALERT_THRESHOLD_F}°F\n")

    alerts = check_gaps()

    if alerts:
        print(f"\n🚨 ALERTS ({len(alerts)}):")
        for a in alerts:
            print(f"  {a['date']}: {a['gap']}°F gap — NOAA says {a['forecast']:.0f}°F, market thinks {a['direction']} ({a['market_implied']}°F)")

        print("\n---ALERT_DATA---")
        print(json.dumps(alerts))
        return 1
    else:
        print("\n✅ No significant gaps detected")
        return 0


if __name__ == '__main__':
    sys.exit(main())
