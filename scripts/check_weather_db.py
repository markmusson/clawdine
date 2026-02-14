#!/usr/bin/env python3
"""Check weather markets in the local DuckDB database."""

import duckdb
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path("/Users/clawdine/.openclaw/workspace/projects/prediction-market-analysis/data/markets.duckdb")

def main():
    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}")
        return
    
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    
    # Check for weather markets
    query = """
    SELECT 
        condition_id,
        question,
        end_date_iso,
        active,
        closed,
        enable_order_book,
        market_slug
    FROM polymarket_markets
    WHERE 
        (LOWER(question) LIKE '%temperature%' 
         OR LOWER(question) LIKE '%degrees%'
         OR LOWER(question) LIKE '%fahrenheit%'
         OR LOWER(question) LIKE '%celsius%'
         OR LOWER(question) LIKE '%°f%'
         OR LOWER(question) LIKE '%°c%'
         OR LOWER(description) LIKE '%temperature%')
        AND LOWER(question) NOT LIKE '%mayweather%'
    ORDER BY end_date_iso DESC
    LIMIT 50
    """
    
    results = conn.execute(query).fetchall()
    
    print(f"Found {len(results)} weather markets in database\n")
    
    now = datetime.now(timezone.utc)
    
    open_count = 0
    for row in results:
        condition_id, question, end_date_iso, active, closed, enable_order_book, market_slug = row
        
        # Parse end date
        try:
            end_date = datetime.fromisoformat(end_date_iso.replace("Z", "+00:00"))
            is_future = end_date > now
        except:
            is_future = False
        
        is_open = active and not closed and is_future
        
        if is_open:
            open_count += 1
            print(f"OPEN: {question[:80]}")
            print(f"  Condition: {condition_id}")
            print(f"  End: {end_date_iso}")
            print(f"  Slug: {market_slug}")
            print(f"  Order book: {enable_order_book}")
            print()
    
    print(f"\nTotal open: {open_count}")
    
    # Show when database was last updated
    last_fetched = conn.execute("""
        SELECT MAX(_fetched_at) as last_update
        FROM polymarket_markets
    """).fetchone()[0]
    
    print(f"Database last updated: {last_fetched}")
    
    conn.close()

if __name__ == "__main__":
    main()
