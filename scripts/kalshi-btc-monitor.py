#!/usr/bin/env python3
"""
Kalshi BTC Price Range Market Monitor & Paper Trader
Monitors KXBTC series — BTC price range prediction markets with various expiry windows.
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# Configuration
BASE_URL = "https://api.elections.kalshi.com/trade-api/v2"
WORKSPACE = Path.home() / ".openclaw/workspace"
LOG_DIR = WORKSPACE / "trading/kalshi"
MARKET_LOG = LOG_DIR / "btc_range_log.jsonl"
PAPER_STATS = LOG_DIR / "paper_stats.json"
MONITOR_LOG = LOG_DIR / "monitor.log"

# Paper trading config
PAPER_BET_SIZE = 100  # cents per trade
# Buy YES on a bucket when price ≤ this and bucket contains current BTC price
MISPRICING_THRESHOLD = 40  # cents — bucket with current price trading below 40¢


def log(msg):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{timestamp}] {msg}"
    print(line)
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        with open(MONITOR_LOG, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def api_get(endpoint, retry=3, delay=2):
    url = f"{BASE_URL}{endpoint}"
    for attempt in range(retry):
        try:
            req = Request(url, headers={"Accept": "application/json"})
            with urlopen(req, timeout=10) as resp:
                return json.loads(resp.read().decode())
        except HTTPError as e:
            if e.code == 429:
                time.sleep(delay * (attempt + 1))
            elif attempt == retry - 1:
                log(f"HTTP {e.code}: {e.reason}")
                return None
            else:
                time.sleep(delay)
        except Exception as e:
            if attempt == retry - 1:
                log(f"Error: {e}")
                return None
            time.sleep(delay)
    return None


def get_btc_price():
    """Get current BTC price from CoinGecko"""
    try:
        req = Request(
            "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
            headers={"Accept": "application/json"}
        )
        with urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data["bitcoin"]["usd"]
    except Exception as e:
        log(f"Failed to get BTC price: {e}")
        return None


def parse_bucket(subtitle):
    """Parse subtitle like '$78,500 to 78,749.99' or '$79,250 or above' into (low, high)"""
    subtitle = subtitle.replace("$", "").replace(",", "")
    if "or above" in subtitle:
        val = float(subtitle.split(" or above")[0].strip())
        return (val, float("inf"))
    elif "or below" in subtitle:
        val = float(subtitle.split(" or below")[0].strip())
        return (float("-inf"), val)
    elif " to " in subtitle:
        parts = subtitle.split(" to ")
        return (float(parts[0].strip()), float(parts[1].strip()))
    return None


def discover_markets():
    """Fetch all open KXBTC markets and group by event"""
    log("Fetching KXBTC markets...")
    data = api_get("/markets?series_ticker=KXBTC&status=open&limit=200")
    if not data or "markets" not in data:
        return {}

    markets = data["markets"]
    log(f"Found {len(markets)} open KXBTC markets")

    # Group by event (date+time from ticker)
    events = {}
    for m in markets:
        ticker = m.get("ticker", "")
        parts = ticker.split("-")
        event_key = parts[1] if len(parts) > 1 else "unknown"
        events.setdefault(event_key, []).append(m)

    return events


def analyze_event(event_key, markets, btc_price):
    """Analyze a single event's markets against current BTC price"""
    close_time = markets[0].get("close_time", "unknown")
    total_volume = sum(m.get("volume", 0) for m in markets)

    log(f"\n{'='*60}")
    log(f"Event: {event_key} | {len(markets)} buckets | Vol: {total_volume} | Closes: {close_time}")

    # Parse buckets and find where BTC currently sits
    bucket_data = []
    current_bucket = None

    for m in markets:
        subtitle = m.get("subtitle", "")
        bounds = parse_bucket(subtitle)
        if not bounds:
            continue

        low, high = bounds
        yes_bid = m.get("yes_bid", 0) or 0
        yes_ask = m.get("yes_ask", 0) or 0
        volume = m.get("volume", 0)

        entry = {
            "ticker": m["ticker"],
            "subtitle": subtitle,
            "low": low,
            "high": high,
            "yes_bid": yes_bid,
            "yes_ask": yes_ask,
            "spread": yes_ask - yes_bid if yes_ask and yes_bid else None,
            "volume": volume,
            "contains_price": low <= btc_price <= high if btc_price else False
        }
        bucket_data.append(entry)

        if entry["contains_price"]:
            current_bucket = entry

    # Sort by low bound
    bucket_data.sort(key=lambda x: x["low"] if x["low"] != float("-inf") else -1e12)

    if current_bucket:
        log(f"BTC ${btc_price:,.0f} sits in: {current_bucket['subtitle']} "
            f"| YES: {current_bucket['yes_bid']}/{current_bucket['yes_ask']}¢ "
            f"| Vol: {current_bucket['volume']}")

        # Show nearby buckets for context
        log("Nearby buckets:")
        for b in bucket_data:
            if b["low"] != float("-inf") and b["high"] != float("inf"):
                if abs((b["low"] + b["high"]) / 2 - btc_price) < 2000:
                    marker = " ← CURRENT" if b["contains_price"] else ""
                    log(f"  {b['subtitle']}: {b['yes_bid']}/{b['yes_ask']}¢ vol={b['volume']}{marker}")
    else:
        log(f"BTC ${btc_price:,.0f} — no matching bucket found")

    return {
        "event_key": event_key,
        "close_time": close_time,
        "total_volume": total_volume,
        "num_buckets": len(bucket_data),
        "current_bucket": current_bucket,
        "buckets": bucket_data,
        "btc_price": btc_price
    }


def paper_trade(analysis, stats):
    """Paper trade: buy YES on current-price bucket if mispriced"""
    bucket = analysis.get("current_bucket")
    if not bucket:
        return

    ticker = bucket["ticker"]
    yes_ask = bucket["yes_ask"]

    if ticker in stats.get("pending", {}):
        return

    # Only trade if the bucket containing current price is underpriced
    if yes_ask and yes_ask <= MISPRICING_THRESHOLD:
        trade = {
            "ticker": ticker,
            "direction": "YES",
            "entry_price": yes_ask,
            "subtitle": bucket["subtitle"],
            "btc_at_entry": analysis["btc_price"],
            "event_key": analysis["event_key"],
            "close_time": analysis["close_time"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "hour": datetime.now(timezone.utc).hour
        }

        stats.setdefault("pending", {})[ticker] = trade
        stats["total_trades"] = stats.get("total_trades", 0) + 1

        log(f"📊 PAPER TRADE: YES on {bucket['subtitle']} @ {yes_ask}¢ "
            f"(BTC=${analysis['btc_price']:,.0f})")

        append_jsonl(MARKET_LOG, {"type": "paper_trade", "trade": trade})


def settle_trades(stats):
    """Check and settle any pending trades"""
    if not stats.get("pending"):
        return

    settled = []
    for ticker, trade in stats["pending"].items():
        data = api_get(f"/markets/{ticker}")
        if not data or "market" not in data:
            continue

        market = data["market"]
        status = market.get("status")
        result = market.get("result")

        if result in ("yes", "no"):
            entry_price = trade["entry_price"]
            won = (result == "yes" and trade["direction"] == "YES")

            pnl = (100 - entry_price) if won else -entry_price
            stats["total_pnl"] = stats.get("total_pnl", 0) + pnl
            if won:
                stats["wins"] = stats.get("wins", 0) + 1
            else:
                stats["losses"] = stats.get("losses", 0) + 1

            hour_key = str(trade.get("hour", 0))
            by_hour = stats.setdefault("by_hour", {})
            h = by_hour.setdefault(hour_key, {"trades": 0, "wins": 0, "losses": 0, "pnl": 0})
            h["trades"] += 1
            h["pnl"] += pnl
            h["wins" if won else "losses"] += 1

            log(f"{'✅' if won else '❌'} SETTLED: {trade['subtitle']} → {result} | "
                f"P&L: {pnl:+.0f}¢ | {'WIN' if won else 'LOSS'}")

            append_jsonl(MARKET_LOG, {
                "type": "settlement", "ticker": ticker,
                "trade": trade, "result": result, "won": won, "pnl": pnl
            })
            settled.append(ticker)

    for t in settled:
        del stats["pending"][t]


def append_jsonl(filepath, data):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "a") as f:
        f.write(json.dumps(data) + "\n")


def load_paper_stats():
    if PAPER_STATS.exists():
        try:
            with open(PAPER_STATS) as f:
                return json.load(f)
        except Exception:
            pass
    return {"total_trades": 0, "wins": 0, "losses": 0, "pending": {},
            "by_hour": {}, "total_pnl": 0}


def save_paper_stats(stats):
    PAPER_STATS.parent.mkdir(parents=True, exist_ok=True)
    with open(PAPER_STATS, "w") as f:
        json.dump(stats, f, indent=2)


def process_markets():
    log("=" * 60)
    log("Kalshi BTC Price Range Monitor")

    btc_price = get_btc_price()
    if not btc_price:
        log("Cannot get BTC price — aborting")
        return

    log(f"Current BTC: ${btc_price:,.2f}")

    events = discover_markets()
    if not events:
        log("No open KXBTC markets found")
        return

    stats = load_paper_stats()

    for event_key, markets in sorted(events.items()):
        analysis = analyze_event(event_key, markets, btc_price)

        # Log snapshot
        append_jsonl(MARKET_LOG, {
            "type": "event_snapshot",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_key": event_key,
            "btc_price": btc_price,
            "close_time": analysis["close_time"],
            "total_volume": analysis["total_volume"],
            "num_buckets": analysis["num_buckets"],
            "current_bucket": {
                "subtitle": analysis["current_bucket"]["subtitle"],
                "yes_bid": analysis["current_bucket"]["yes_bid"],
                "yes_ask": analysis["current_bucket"]["yes_ask"],
                "volume": analysis["current_bucket"]["volume"]
            } if analysis["current_bucket"] else None
        })

        paper_trade(analysis, stats)

    # Settle any completed trades
    settle_trades(stats)
    save_paper_stats(stats)

    # Summary
    total = stats.get("total_trades", 0)
    wins = stats.get("wins", 0)
    losses = stats.get("losses", 0)
    pending = len(stats.get("pending", {}))
    pnl = stats.get("total_pnl", 0)
    wr = (wins / total * 100) if total > 0 else 0

    log(f"\n📈 Paper Stats: {total} trades ({pending} pending) | "
        f"{wins}W-{losses}L ({wr:.0f}%) | P&L: {pnl:+.0f}¢")


if __name__ == "__main__":
    try:
        process_markets()
    except Exception as e:
        log(f"❌ Fatal: {e}")
        import traceback
        log(traceback.format_exc())
        sys.exit(1)
