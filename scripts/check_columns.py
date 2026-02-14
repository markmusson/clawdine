#!/usr/bin/env python3
import pandas as pd
from pathlib import Path

MARKETS_DIR = Path("/Users/clawdine/.openclaw/workspace/projects/prediction-market-analysis/data/polymarket/markets")

# Read just one file to see columns
first_file = list(MARKETS_DIR.glob("*.parquet"))[0]
df = pd.read_parquet(first_file)
print("Columns:")
for col in sorted(df.columns):
    print(f"  - {col}")
