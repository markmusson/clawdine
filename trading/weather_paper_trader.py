#!/usr/bin/env python3
"""
Weather Paper Trader
- `python3 weather_paper_trader.py trade` — run gap alert, open positions if signals found
- `python3 weather_paper_trader.py settle` — settle any resolved positions  
- `python3 weather_paper_trader.py both` — do both (default)
- `python3 weather_paper_trader.py status` — print current state

Stats file: trading/weather_paper_stats.json
Schema: {total_trades, wins, losses, total_pnl, pending: {date: trade}, history: [trade]}
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw/workspace"
STATS_FILE = WORKSPACE / "trading/weather_paper_stats.json"
GAP_ALERT = WORKSPACE / "trading/backtest/gap_alert.py"
PAPER_BET_SIZE = 50
GAMMA_API = "https://gamma-api.polymarket.com"


def load_stats():
    if STATS_FILE.exists():
        try:
            return json.loads(STATS_FILE.read_text())
        except Exception:
            pass
    return {"total_trades": 0, "wins": 0, "losses": 0, "total_pnl": 0.0, "pending": {}, "history": []}


def save_stats(stats):
    STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATS_FILE.write_text(json.dumps(stats, indent=2))


def curl_json(url):
    try:
        r = subprocess.run(
            ["curl", "-s", "-H", "User-Agent: clawdine-weather-trader", url],
            capture_output=True, text=True, timeout=15
        )
        return json.loads(re.sub(r'[\x00-\x1f]', '', r.stdout))
    except Exception:
        return None


def fetch_event(date_str):
    """date_str: YYYY-MM-DD"""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    slug = dt.strftime("highest-temperature-in-nyc-on-%B-%-d-%Y").lower()
    data = curl_json(f"{GAMMA_API}/events?slug={slug}")
    if data and isinstance(data, list) and data:
        return data[0]
    return None


def find_best_bucket(event, forecast_temp):
    """Find market bucket closest to forecast. Returns (question, condition_id, yes_price)."""
    if not event or "markets" not in event:
        return None, None, None

    best = None
    best_dist = float("inf")

    for m in event["markets"]:
        q = m.get("question", "")
        prices = json.loads(m.get("outcomePrices", '["0","0"]'))
        yes = float(prices[0])
        cid = m.get("conditionId", m.get("id", ""))

        mid = None
        if "between" in q:
            match = re.search(r"between (\d+)-(\d+)", q)
            if match:
                mid = (int(match.group(1)) + int(match.group(2))) / 2
        elif "or higher" in q:
            match = re.search(r"(\d+)°F or higher", q)
            if match:
                mid = int(match.group(1)) + 5
        elif "or below" in q:
            match = re.search(r"(\d+)°F or below", q)
            if match:
                mid = int(match.group(1)) - 5

        if mid is not None:
            dist = abs(mid - forecast_temp)
            if dist < best_dist:
                best_dist = dist
                best = (q, cid, yes)

    return best if best else (None, None, None)


def run_gap_alert():
    """Run gap_alert.py, return list of alerts."""
    if not GAP_ALERT.exists():
        print("ERROR: gap_alert.py not found")
        return []

    r = subprocess.run(
        [sys.executable, str(GAP_ALERT)],
        capture_output=True, text=True, timeout=30
    )
    print(r.stdout)

    if "---ALERT_DATA---" in r.stdout:
        json_str = r.stdout.split("---ALERT_DATA---")[1].strip()
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            print("ERROR: Failed to parse alert JSON")
    return []


def do_trade(stats):
    """Run gap alert and open positions for any signals."""
    alerts = run_gap_alert()

    if not alerts:
        print("No gap alerts — no new trades.")
        return

    for alert in alerts:
        date = alert["date"]

        # Idempotent: skip if already have position or traded this date
        if date in stats["pending"]:
            print(f"  Already have open position for {date}, skipping")
            continue
        if any(t.get("date") == date for t in stats["history"]):
            print(f"  Already traded {date}, skipping")
            continue

        event = fetch_event(date)
        if not event:
            print(f"  No Polymarket event for {date}")
            continue

        question, cid, ask = find_best_bucket(event, alert["forecast"])
        if not question or ask is None or ask <= 0:
            print(f"  No valid bucket for {date}")
            continue

        trade = {
            "date": date,
            "bucket": question,
            "condition_id": cid,
            "entry_price": round(ask, 4),
            "bet_size": PAPER_BET_SIZE,
            "forecast_temp": alert["forecast"],
            "market_implied": alert["market_implied"],
            "gap_size": alert["gap"],
            "direction": alert["direction"],
            "opened_at": datetime.now(timezone.utc).isoformat(),
            "status": "open"
        }

        stats["pending"][date] = trade
        stats["total_trades"] += 1
        print(f"  📊 TRADE: {date} — YES on '{question}' @ {ask:.1%} (NOAA: {alert['forecast']}°F)")


def do_settle(stats):
    """Settle any resolved positions."""
    pending = stats.get("pending", {})
    if not pending:
        print("No pending positions to settle.")
        return

    print(f"Checking {len(pending)} pending positions...")
    settled_dates = []

    for date, trade in pending.items():
        event = fetch_event(date)
        if not event:
            continue

        # Check if market resolved
        for m in event.get("markets", []):
            cid = m.get("conditionId", m.get("id", ""))
            if cid != trade["condition_id"]:
                continue

            prices = json.loads(m.get("outcomePrices", '["0","0"]'))
            final = float(prices[0])

            # Resolved if price is very close to 0 or 1
            if final > 0.95:
                # We won
                pnl = round(PAPER_BET_SIZE / trade["entry_price"] - PAPER_BET_SIZE, 2)
                trade.update({"status": "settled", "result": "win", "pnl": pnl,
                              "settled_at": datetime.now(timezone.utc).isoformat()})
                stats["wins"] += 1
                stats["total_pnl"] = round(stats["total_pnl"] + pnl, 2)
                stats["history"].append(trade)
                settled_dates.append(date)
                print(f"  ✅ WIN: {date} — +${pnl:.2f}")
                break
            elif final < 0.05:
                # We lost
                pnl = -PAPER_BET_SIZE
                trade.update({"status": "settled", "result": "loss", "pnl": pnl,
                              "settled_at": datetime.now(timezone.utc).isoformat()})
                stats["losses"] += 1
                stats["total_pnl"] = round(stats["total_pnl"] + pnl, 2)
                stats["history"].append(trade)
                settled_dates.append(date)
                print(f"  ❌ LOSS: {date} — -${PAPER_BET_SIZE}")
                break

        # Fallback: if date is >30 hours old and not resolved, check all markets for winner
        if date not in settled_dates:
            market_date = datetime.strptime(date, "%Y-%m-%d")
            if datetime.now() > market_date + timedelta(hours=30):
                # Find which bucket won
                our_cid = trade["condition_id"]
                won = False
                for m in event.get("markets", []):
                    prices = json.loads(m.get("outcomePrices", '["0","0"]'))
                    if float(prices[0]) > 0.95:
                        # This bucket won
                        if m.get("conditionId", m.get("id", "")) == our_cid:
                            won = True
                        break

                pnl = round(PAPER_BET_SIZE / trade["entry_price"] - PAPER_BET_SIZE, 2) if won else -PAPER_BET_SIZE
                result = "win" if won else "loss"
                trade.update({"status": "settled", "result": result, "pnl": pnl,
                              "settled_at": datetime.now(timezone.utc).isoformat()})
                stats["wins" if won else "losses"] += 1
                stats["total_pnl"] = round(stats["total_pnl"] + pnl, 2)
                stats["history"].append(trade)
                settled_dates.append(date)
                emoji = "✅" if won else "❌"
                print(f"  {emoji} {'WIN' if won else 'LOSS'} (fallback): {date} — ${pnl:+.2f}")

    for d in settled_dates:
        del stats["pending"][d]


def do_status(stats):
    """Print current state."""
    total = stats["total_trades"]
    wins = stats["wins"]
    losses = stats["losses"]
    pending = len(stats["pending"])
    pnl = stats["total_pnl"]
    wr = (wins / (wins + losses) * 100) if (wins + losses) > 0 else 0

    print(f"Weather Paper Trading Status:")
    print(f"  Trades: {total} ({pending} open, {wins + losses} settled)")
    print(f"  Record: {wins}W-{losses}L ({wr:.0f}%)")
    print(f"  P&L: ${pnl:+.2f}")

    if stats["pending"]:
        print(f"\n  Open positions:")
        for date, t in stats["pending"].items():
            print(f"    {date}: {t['bucket'][:60]} @ {t['entry_price']:.1%} (${t['bet_size']})")

    if stats["history"]:
        print(f"\n  Recent trades:")
        for t in stats["history"][-5:]:
            emoji = "✅" if t["result"] == "win" else "❌"
            print(f"    {emoji} {t['date']}: ${t['pnl']:+.2f}")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "both"
    stats = load_stats()

    if mode == "trade":
        do_trade(stats)
    elif mode == "settle":
        do_settle(stats)
    elif mode == "status":
        do_status(stats)
    elif mode == "both":
        do_trade(stats)
        do_settle(stats)
    else:
        print(f"Unknown mode: {mode}")
        print("Usage: weather_paper_trader.py [trade|settle|both|status]")
        sys.exit(1)

    save_stats(stats)


if __name__ == "__main__":
    main()
