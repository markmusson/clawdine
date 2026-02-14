#!/usr/bin/env python3
"""Check for precision weather markets (city + date + specific temp threshold)."""

import pandas as pd
from pathlib import Path
from datetime import datetime, timezone
import re

MARKETS_DIR = Path("/Users/clawdine/.openclaw/workspace/projects/prediction-market-analysis/data/polymarket/markets")

def main():
    print("Reading market data...")
    
    all_files = list(MARKETS_DIR.glob("*.parquet"))
    dfs = [pd.read_parquet(f) for f in all_files]
    df = pd.concat(dfs, ignore_index=True)
    
    # Precision weather patterns:
    # - Must have "high" or "low" temperature
    # - Must have a specific number (like 45, 32, 75, etc.)
    # - Must have a date or day reference
    
    precision_pattern = r'(high|low).*?(temperature|temp).*?(\d+).*?(°f|fahrenheit)|(\d+).*?(°f|fahrenheit).*(high|low)'
    
    precision_weather = df[
        df['question'].str.lower().str.contains(precision_pattern, na=False, regex=True, case=False)
    ].copy()
    
    print(f"Found {len(precision_weather)} precision temperature markets")
    
    # Check for open ones
    now = datetime.now(timezone.utc)
    precision_weather['end_datetime'] = pd.to_datetime(precision_weather['end_date'], utc=True, errors='coerce')
    precision_weather['is_future'] = precision_weather['end_datetime'] > now
    precision_weather['is_open'] = precision_weather['active'] & ~precision_weather['closed'] & precision_weather['is_future']
    
    open_precision = precision_weather[precision_weather['is_open']]
    
    print(f"Open precision weather markets: {len(open_precision)}\n")
    
    if len(open_precision) > 0:
        print("OPEN PRECISION WEATHER MARKETS:")
        for idx, row in open_precision.head(20).iterrows():
            print(f"\nQuestion: {row['question']}")
            print(f"  End: {row['end_date']}")
            print(f"  Slug: {row['slug']}")
            print(f"  Prices: {row['outcome_prices']}")
    else:
        print("No open precision weather markets found.")
        print("\nMost recent closed precision weather markets:")
        closed_precision = precision_weather[~precision_weather['is_open']].sort_values('end_datetime', ascending=False)
        for idx, row in closed_precision.head(10).iterrows():
            print(f"\n  Question: {row['question'][:120]}")
            print(f"    Ended: {row['end_date']}")
            print(f"    Slug: {row['slug'][:60]}")
    
    # Data freshness
    if '_fetched_at' in df.columns:
        last_fetched = df['_fetched_at'].max()
        print(f"\n\nData last fetched: {last_fetched}")

if __name__ == "__main__":
    main()
