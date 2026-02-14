# Sample Output Examples

## Monitor Log (monitor.log)
```
[2026-02-08 09:04:45 UTC] ============================================================
[2026-02-08 09:04:45 UTC] Starting Kalshi BTC 15-min market scan...
[2026-02-08 09:04:45 UTC] Discovering BTC 15-minute markets...
[2026-02-08 09:04:46 UTC] Found 2 active BTC 15-minute markets
[2026-02-08 09:04:46 UTC] Market: KXBTC-26FEB08-UP15 | YES: 45/48¢ | NO: 52/55¢ | Vol: 1250 | Status: open
[2026-02-08 09:04:47 UTC] Market: KXBTC-26FEB08-DN15 | YES: 28/32¢ | NO: 68/72¢ | Vol: 890 | Status: open
[2026-02-08 09:04:47 UTC] 📊 PAPER TRADE: YES on KXBTC-26FEB08-DN15 @ 32¢
[2026-02-08 09:04:47 UTC] 📈 Paper Trading Stats: 1 trades | 0W-0L | Win Rate: 0.0% | P&L: +0¢
```

## Market Snapshot (btc_15min_log.jsonl)
```json
{"type": "market_snapshot", "timestamp": "2026-02-08T14:30:00Z", "hour": 14, "ticker": "KXBTC-26FEB08-UP15", "yes_bid": 45, "yes_ask": 48, "no_bid": 52, "no_ask": 55, "spread": 3, "volume": 1250, "open_interest": 3400, "close_time": "2026-02-08T14:45:00Z", "status": "open", "orderbook_depth": 12}
```

## Paper Trade Entry (btc_15min_log.jsonl)
```json
{"type": "paper_trade", "trade": {"ticker": "KXBTC-26FEB08-DN15", "direction": "YES", "entry_price": 32, "timestamp": "2026-02-08T14:30:15Z", "close_time": "2026-02-08T14:45:00Z", "hour": 14}}
```

## Settlement (btc_15min_log.jsonl)
```json
{"type": "settlement", "ticker": "KXBTC-26FEB08-DN15", "trade": {"ticker": "KXBTC-26FEB08-DN15", "direction": "YES", "entry_price": 32, "timestamp": "2026-02-08T14:30:15Z", "close_time": "2026-02-08T14:45:00Z", "hour": 14}, "result": "yes", "won": true, "pnl": 68}
```

## Paper Stats (paper_stats.json) - After Some Trades
```json
{
  "total_trades": 15,
  "wins": 9,
  "losses": 6,
  "pending": {
    "KXBTC-26FEB08-UP17": {
      "ticker": "KXBTC-26FEB08-UP17",
      "direction": "NO",
      "entry_price": 34,
      "timestamp": "2026-02-08T17:15:00Z",
      "close_time": "2026-02-08T17:30:00Z",
      "hour": 17
    }
  },
  "by_hour": {
    "9": {"trades": 2, "wins": 1, "losses": 1, "pnl": 15},
    "10": {"trades": 3, "wins": 2, "losses": 1, "pnl": 82},
    "11": {"trades": 1, "wins": 1, "losses": 0, "pnl": 66},
    "13": {"trades": 4, "wins": 2, "losses": 2, "pnl": -8},
    "14": {"trades": 3, "wins": 2, "losses": 1, "pnl": 94},
    "15": {"trades": 1, "wins": 0, "losses": 1, "pnl": -28},
    "17": {"trades": 1, "wins": 1, "losses": 0, "pnl": 68}
  },
  "total_pnl": 289,
  "best_hour": 14,
  "worst_hour": 15
}
```

## Analysis After 1 Week
```
📊 WEEKLY SUMMARY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Trades:     127
Win Rate:         58.3% (74W-53L)
Total P&L:        +$14.23
Avg Per Trade:    +$0.11

🏆 BEST HOURS (by P&L):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10:00 UTC → +$4.82 (12 trades, 75% win)
14:00 UTC → +$3.94 (15 trades, 67% win)
11:00 UTC → +$2.46 (8 trades, 62% win)

📉 WORST HOURS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
15:00 UTC → -$1.28 (9 trades, 33% win)
22:00 UTC → -$0.82 (6 trades, 33% win)

🔍 INSIGHTS:
• Morning hours (10-12 UTC) show strongest edge
• Afternoon (14-15 UTC) high volume but mixed results
• Late night (22-23 UTC) avoid - low liquidity
• Spread <35¢ zones show 68% win rate
• Spread >65¢ zones show 52% win rate
```

## Key Metrics Tracked
1. **Volume patterns** - Which hours have most trading activity
2. **Spread patterns** - When markets show highest conviction (extreme prices)
3. **Win rate by hour** - Time-of-day edge detection
4. **P&L by hour** - Profitability timing
5. **Orderbook depth** - Liquidity availability

This enables computational arbitrage through structural patterns rather than prediction.
