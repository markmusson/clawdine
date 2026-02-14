# Kalshi BTC 15-Minute Paper Trading Monitor

## Overview
Automated paper trading system for Kalshi's "BTC Up or Down - 15 minutes" markets. Runs every 5 minutes via launchd, requires zero tokens, no AI.

## Files
- **Script:** `~/.openclaw/workspace/scripts/kalshi-btc-monitor.py`
- **LaunchD:** `~/Library/LaunchAgents/com.clawdine.kalshi-btc-monitor.plist`
- **Logs:** `~/.openclaw/workspace/trading/kalshi/`
  - `monitor.log` - Execution logs
  - `btc_15min_log.jsonl` - Market snapshots and trades
  - `paper_stats.json` - Running statistics

## How It Works

### Market Discovery
- Queries Kalshi API for BTC 15-minute markets
- Searches series tickers: KXBTC, KXBTCUD, BTCUD, BTC15
- Filters for "BTC" + "15 min" in title/subtitle

### Paper Trading Logic
**High Conviction Zones:**
- **Buy YES:** when yes_ask < 35¢ (bullish)
- **Buy NO:** when yes_ask > 65¢ (bearish)

One trade per market (tracked in `pending`).

### Settlement
- Monitors market status and result field
- Calculates P&L: `(100 - entry_price)` if win, `-entry_price` if loss
- Tracks by hour of day for pattern analysis

### Data Collected
Each market snapshot logs:
- Timestamp, hour, ticker
- Bid/ask spreads (YES and NO)
- Volume, open interest
- Orderbook depth

Each trade logs:
- Entry direction and price
- Settlement result and P&L

### Stats Tracked
- Total trades, wins, losses
- P&L by hour of day (0-23)
- Win rate per hour
- Best/worst performing hours
- Total P&L (in cents)

## Commands

### Manual Run
```bash
cd ~/.openclaw/workspace
python3 scripts/kalshi-btc-monitor.py
```

### LaunchD Control
```bash
# Check status
launchctl list | grep kalshi

# View details
launchctl list com.clawdine.kalshi-btc-monitor

# Stop
launchctl unload ~/Library/LaunchAgents/com.clawdine.kalshi-btc-monitor.plist

# Start
launchctl load ~/Library/LaunchAgents/com.clawdine.kalshi-btc-monitor.plist

# Restart
launchctl unload ~/Library/LaunchAgents/com.clawdine.kalshi-btc-monitor.plist
launchctl load ~/Library/LaunchAgents/com.clawdine.kalshi-btc-monitor.plist
```

### View Logs
```bash
# Live tail
tail -f ~/.openclaw/workspace/trading/kalshi/monitor.log

# View stats
cat ~/.openclaw/workspace/trading/kalshi/paper_stats.json | jq

# Count trades
wc -l ~/.openclaw/workspace/trading/kalshi/btc_15min_log.jsonl
```

## Schedule
Runs every 5 minutes (300 seconds) via launchd StartInterval.

## Requirements
- Python 3 (stdlib only)
- No API key needed (public endpoints)
- Handles rate limits with exponential backoff
- Gracefully handles missing markets

## Strategy Context
Part of reverse-engineering effort on computational arbitrage for Kalshi BTC 15-minute markets. Uses time-window analysis and structural math to identify edge in high-conviction zones (< 35¢ or > 65¢).

Pattern tracking enables:
- Hour-of-day volatility analysis
- Spread pattern recognition
- Volume/liquidity timing optimization

## Status
✅ **Installed and running** - launchd job active
📊 Next run: every 5 minutes
🔍 Waiting for active BTC 15-minute markets on Kalshi
