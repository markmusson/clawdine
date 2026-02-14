#!/usr/bin/env python3
"""Check for city-specific precision weather markets."""

import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

MARKETS_DIR = Path("/Users/clawdine/.openclaw/workspace/projects/prediction-market-analysis/data/polymarket/markets")

def main():
    print("Reading market data...")
    
    all_files = list(MARKETS_DIR.glob("*.parquet"))
    dfs = [pd.read_parquet(f) for f in all_files]
    df = pd.concat(dfs, ignore_index=True)
    
    # Cities commonly used in precision weather markets
    cities = ['nyc', 'new york', 'los angeles', 'la ', 'chicago', 'houston', 'phoenix', 
              'philadelphia', 'san antonio', 'san diego', 'dallas', 'miami', 'boston',
              'seattle', 'denver', 'atlanta', 'washington', 'las vegas', 'portland',
              'san francisco']
    
    # Look for city + temp pattern
    city_pattern = '|'.join(cities)
    
    city_weather = df[
        df['question'].str.lower().str.contains(city_pattern, na=False, regex=True) &
        df['question'].str.lower().str.contains('temperature|temp|high|low|degrees', na=False, regex=True)
    ].copy()
    
    print(f"Found {len(city_weather)} city-specific temperature markets")
    
    # Check for open ones
    now = datetime.now(timezone.utc)
    city_weather['end_datetime'] = pd.to_datetime(city_weather['end_date'], utc=True, errors='coerce')
    city_weather['is_future'] = city_weather['end_datetime'] > now
    city_weather['is_open'] = city_weather['active'] & ~city_weather['closed'] & city_weather['is_future']
    
    open_city = city_weather[city_weather['is_open']]
    
    print(f"Open city weather markets: {len(open_city)}\n")
    
    if len(open_city) > 0:
        for idx, row in open_city.iterrows():
            print(f"Question: {row['question']}")
            print(f"  End: {row['end_date']}")
            print(f"  Slug: {row['slug']}")
            print()
    else:
        print("No open city-specific precision weather markets found.")
        print("\nMost recent closed city weather markets:")
        closed_city = city_weather[~city_weather['is_open']].sort_values('end_datetime', ascending=False)
        for idx, row in closed_city.head(5).iterrows():
            print(f"  - {row['question'][:100]}")
            print(f"    Ended: {row['end_date']}")

if __name__ == "__main__":
    main()
