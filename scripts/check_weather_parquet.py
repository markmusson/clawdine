#!/usr/bin/env python3
"""Check weather markets in parquet files."""

import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

MARKETS_DIR = Path("/Users/clawdine/.openclaw/workspace/projects/prediction-market-analysis/data/polymarket/markets")

def main():
    # Read all parquet files
    print("Reading market data from parquet files...")
    
    all_files = list(MARKETS_DIR.glob("*.parquet"))
    if not all_files:
        print(f"No parquet files found in {MARKETS_DIR}")
        return
    
    print(f"Found {len(all_files)} parquet files")
    
    # Read all files into a single dataframe
    dfs = []
    for f in all_files:
        dfs.append(pd.read_parquet(f))
    
    df = pd.concat(dfs, ignore_index=True)
    print(f"Total markets: {len(df)}")
    
    # Filter for weather markets
    weather_mask = (
        df['question'].str.lower().str.contains('temperature|degrees|fahrenheit|celsius|°f|°c', na=False, regex=True)
    ) & ~df['question'].str.lower().str.contains('mayweather', na=False)
    
    weather_df = df[weather_mask].copy()
    print(f"Weather markets: {len(weather_df)}")
    
    # Check which are open
    now = datetime.now(timezone.utc)
    
    # Parse end dates
    weather_df['end_datetime'] = pd.to_datetime(weather_df['end_date'], utc=True, errors='coerce')
    weather_df['is_future'] = weather_df['end_datetime'] > now
    weather_df['is_open'] = weather_df['active'] & ~weather_df['closed'] & weather_df['is_future']
    
    open_markets = weather_df[weather_df['is_open']].copy()
    print(f"Open weather markets: {len(open_markets)}\n")
    
    if len(open_markets) > 0:
        # Show details
        open_markets = open_markets.sort_values('end_datetime')
        
        print("OPEN WEATHER MARKETS:")
        for idx, row in open_markets.head(20).iterrows():
            print(f"\nQuestion: {row['question'][:100]}")
            print(f"  Condition: {row['condition_id']}")
            print(f"  End: {row['end_date']}")
            print(f"  Slug: {row['slug']}")
            print(f"  Prices: {row['outcome_prices']}")
            print(f"  Outcomes: {row['outcomes']}")
        
        # Summary stats
        print(f"\n=== SUMMARY ===")
        print(f"Total open: {len(open_markets)}")
        print(f"Earliest end: {open_markets['end_datetime'].min()}")
        print(f"Latest end: {open_markets['end_datetime'].max()}")
    else:
        # Show most recent closed ones
        print("\nMost recent closed weather markets:")
        closed_markets = weather_df[~weather_df['is_open']].sort_values('end_datetime', ascending=False)
        
        for idx, row in closed_markets.head(10).iterrows():
            print(f"\n  Question: {row['question'][:100]}")
            print(f"    End: {row['end_date']}, Closed: {row['closed']}, Active: {row['active']}")
    
    # Check last fetched time
    if '_fetched_at' in df.columns:
        last_fetched = df['_fetched_at'].max()
        print(f"\nData last fetched: {last_fetched}")

if __name__ == "__main__":
    main()
