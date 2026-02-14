#!/usr/bin/env python3
"""Check for currently open weather/temperature markets on Polymarket."""

import requests
from datetime import datetime
import re

def main():
    # Get all markets
    url = "https://gamma-api.polymarket.com/markets"
    params = {
        "limit": 1000
    }
    
    print("Fetching markets from Polymarket...")
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    markets = response.json()
    print(f"Total markets fetched: {len(markets)}")
    
    # Better weather detection - word boundaries
    weather_patterns = [
        r'\btemperature\b',
        r'\bdegrees\b',
        r'\bfahrenheit\b',
        r'\bcelsius\b',
        r'°f',
        r'°c',
        r'\bhigh temp\b',
        r'\blow temp\b',
        r'\bweather\b(?!.*mayweather)',  # Weather but not Mayweather
    ]
    
    weather_markets = []
    
    for market in markets:
        question = market.get("question", "").lower()
        description = market.get("description", "").lower()
        text = question + " " + description
        
        if any(re.search(pattern, text, re.IGNORECASE) for pattern in weather_patterns):
            weather_markets.append(market)
    
    print(f"Found {len(weather_markets)} weather/temperature markets total")
    
    # Now filter for open ones
    now = datetime.utcnow()
    open_markets = []
    
    for m in weather_markets:
        closed = m.get("closed", False)
        active = m.get("active", False)
        end_date_str = m.get("end_date_iso")
        
        # Check if truly open
        is_open = not closed and active
        
        if end_date_str:
            try:
                end_date = datetime.fromisoformat(end_date_str.replace("Z", "+00:00"))
                is_open = is_open and end_date > now
            except:
                pass
        
        if is_open:
            open_markets.append(m)
    
    print(f"Open weather markets: {len(open_markets)}\n")
    
    for m in open_markets[:20]:  # Show up to 20
        print(f"Question: {m.get('question')}")
        print(f"  Condition ID: {m.get('condition_id')}")
        print(f"  End Date: {m.get('end_date_iso')}")
        print(f"  Market Slug: {m.get('market_slug')}")
        print(f"  Active: {m.get('active')}, Closed: {m.get('closed')}")
        print()
    
    # Show a few closed ones for comparison
    closed_markets = [m for m in weather_markets if m not in open_markets]
    if closed_markets:
        print(f"\nExample closed weather markets ({len(closed_markets)} total):")
        for m in closed_markets[:5]:
            print(f"  - {m.get('question')[:80]} (closed={m.get('closed')}, active={m.get('active')})")

if __name__ == "__main__":
    main()
