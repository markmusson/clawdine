#!/usr/bin/env python3
"""
Polymarket Weather Backtest Analysis
Compares market resolutions to Open-Meteo forecasts to identify edge
"""

import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

BACKTEST_DIR = Path(__file__).parent

def extract_winner(data):
    """Extract winning bucket from resolved market"""
    if not data or not data[0].get('markets'):
        return None, None
    
    for market in data[0]['markets']:
        prices = market.get('outcomePrices', '[]')
        # Winner has YES price = 1
        if prices.startswith('["1"'):
            question = market['question']
            # Extract temp range from question
            if 'between' in question:
                # "between 32-33°F"
                match = re.search(r'between (\d+)-(\d+)°F', question)
                if match:
                    return (int(match.group(1)), int(match.group(2))), question
            elif 'or higher' in question:
                match = re.search(r'(\d+)°F or higher', question)
                if match:
                    return (int(match.group(1)), 999), question
            elif 'or below' in question:
                match = re.search(r'(\d+)°F or below', question)
                if match:
                    return (-999, int(match.group(1))), question
    return None, None

def analyze_markets():
    """Analyze all downloaded market data"""
    results = []
    
    for f in sorted(BACKTEST_DIR.glob('nyc-february-*.json')):
        date_str = f.stem.replace('nyc-', '')
        
        with open(f) as fp:
            try:
                data = json.load(fp)
            except:
                continue
        
        if not data:
            continue
            
        winner_range, question = extract_winner(data)
        if winner_range:
            results.append({
                'date': date_str,
                'winner_range': winner_range,
                'winner_question': question
            })
    
    return results

if __name__ == '__main__':
    print("=== Polymarket NYC Temperature Resolutions ===\n")
    
    results = analyze_markets()
    for r in results:
        lo, hi = r['winner_range']
        if hi == 999:
            range_str = f"≥{lo}°F"
        elif lo == -999:
            range_str = f"≤{hi}°F"
        else:
            range_str = f"{lo}-{hi}°F"
        
        print(f"{r['date']}: {range_str}")
    
    print("\n=== Key Insight ===")
    print("Compare these to Open-Meteo forecasts from 1-3 days prior")
    print("Edge = when forecast confidence > market implied probability")
