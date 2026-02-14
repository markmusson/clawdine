#!/usr/bin/env python3
"""
Unified Paper Trading Portfolio Dashboard
Reads from weather and BTC paper trading stats, produces terminal report + JSON summary.
"""

import json
import math
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw/workspace"
WEATHER_STATS = WORKSPACE / "trading/weather_paper_stats.json"
KALSHI_STATS = WORKSPACE / "trading/kalshi/paper_stats.json"
SUMMARY_FILE = WORKSPACE / "trading/portfolio_summary.json"

# Bet sizes for P&L normalization
WEATHER_BET = 50  # dollars
KALSHI_BET = 1    # dollar (100 cents)


def load_json(path):
    if path.exists():
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def analyze_weather(stats):
    """Analyze weather paper trading stats."""
    total = stats.get("total_trades", 0)
    wins = stats.get("wins", 0)
    losses = stats.get("losses", 0)
    settled = wins + losses
    pnl = stats.get("total_pnl", 0.0)
    pending = stats.get("pending", {})
    history = stats.get("history", [])

    returns = []
    for t in history:
        if t.get("pnl") is not None:
            returns.append(t["pnl"])

    open_positions = []
    for date, trade in pending.items():
        open_positions.append({
            "strategy": "weather",
            "id": date,
            "description": f"{trade.get('bucket', 'Unknown')}",
            "entry_price": trade.get("entry_price", 0),
            "bet_size": f"${WEATHER_BET}",
            "opened": trade.get("opened_at", "?")[:10]
        })

    return {
        "name": "Weather Gap",
        "total_trades": total,
        "settled": settled,
        "wins": wins,
        "losses": losses,
        "win_rate": (wins / settled * 100) if settled > 0 else 0,
        "pnl": round(pnl, 2),
        "avg_return": round(pnl / settled, 2) if settled > 0 else 0,
        "returns": returns,
        "open_count": len(pending),
        "open_positions": open_positions,
        "recent": history[-10:] if history else []
    }


def analyze_kalshi(stats):
    """Analyze Kalshi BTC paper trading stats."""
    total = stats.get("total_trades", 0)
    wins = stats.get("wins", 0)
    losses = stats.get("losses", 0)
    settled = wins + losses
    pnl_cents = stats.get("total_pnl", 0)
    pnl_dollars = pnl_cents / 100.0  # convert cents to dollars
    pending = stats.get("pending", {})

    # Build returns from by_hour data (we don't have per-trade history in kalshi stats)
    returns = []
    for hour, data in stats.get("by_hour", {}).items():
        # Approximate: distribute pnl evenly across trades in each hour
        n = data.get("trades", 0)
        if n > 0:
            per_trade = data.get("pnl", 0) / n / 100.0  # cents to dollars
            returns.extend([per_trade] * n)

    open_positions = []
    for ticker, trade in pending.items():
        open_positions.append({
            "strategy": "btc",
            "id": ticker,
            "description": f"{trade.get('subtitle', ticker)} ({trade.get('event_key', '')})",
            "entry_price": f"{trade.get('entry_price', 0)}¢",
            "bet_size": f"${KALSHI_BET}",
            "opened": trade.get("timestamp", "?")[:10]
        })

    recent = []
    # Kalshi stats don't keep a history array, so we can't show recent trades easily

    return {
        "name": "BTC Range (Kalshi)",
        "total_trades": total,
        "settled": settled,
        "wins": wins,
        "losses": losses,
        "win_rate": (wins / settled * 100) if settled > 0 else 0,
        "pnl": round(pnl_dollars, 2),
        "avg_return": round(pnl_dollars / settled, 2) if settled > 0 else 0,
        "returns": returns,
        "open_count": len(pending),
        "open_positions": open_positions,
        "recent": recent
    }


def compute_sharpe(returns):
    """Sharpe-like ratio: mean / stddev of per-trade returns."""
    if len(returns) < 2:
        return 0
    mean = sum(returns) / len(returns)
    var = sum((r - mean) ** 2 for r in returns) / (len(returns) - 1)
    std = math.sqrt(var) if var > 0 else 0
    return round(mean / std, 2) if std > 0 else 0


def build_summary(strategies):
    """Build combined portfolio summary."""
    total_trades = sum(s["total_trades"] for s in strategies)
    total_settled = sum(s["settled"] for s in strategies)
    total_wins = sum(s["wins"] for s in strategies)
    total_losses = sum(s["losses"] for s in strategies)
    total_pnl = round(sum(s["pnl"] for s in strategies), 2)
    total_open = sum(s["open_count"] for s in strategies)

    all_returns = []
    for s in strategies:
        all_returns.extend(s["returns"])

    all_open = []
    for s in strategies:
        all_open.extend(s["open_positions"])

    # Recent trades (merge and sort by date, last 20)
    all_recent = []
    for s in strategies:
        for t in s.get("recent", []):
            t["_strategy"] = s["name"]
            all_recent.append(t)
    all_recent.sort(key=lambda x: x.get("settled_at", x.get("opened_at", "")), reverse=True)
    all_recent = all_recent[:20]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "strategies": [{
            "name": s["name"],
            "total_trades": s["total_trades"],
            "settled": s["settled"],
            "wins": s["wins"],
            "losses": s["losses"],
            "win_rate": round(s["win_rate"], 1),
            "pnl": s["pnl"],
            "avg_return": s["avg_return"],
            "open_count": s["open_count"]
        } for s in strategies],
        "combined": {
            "total_trades": total_trades,
            "settled": total_settled,
            "wins": total_wins,
            "losses": total_losses,
            "win_rate": round(total_wins / total_settled * 100, 1) if total_settled > 0 else 0,
            "total_pnl": total_pnl,
            "avg_return": round(total_pnl / total_settled, 2) if total_settled > 0 else 0,
            "sharpe": compute_sharpe(all_returns),
            "open_positions": total_open
        },
        "open_positions": all_open,
        "recent_trades": all_recent
    }


def print_report(summary):
    """Print a clean terminal report."""
    print("=" * 60)
    print("  📊 PAPER TRADING PORTFOLIO DASHBOARD")
    print(f"  Generated: {summary['generated_at'][:19]}Z")
    print("=" * 60)

    # Per-strategy
    for s in summary["strategies"]:
        print(f"\n  ── {s['name']} ──")
        print(f"  Trades: {s['total_trades']} ({s['open_count']} open, {s['settled']} settled)")
        print(f"  Record: {s['wins']}W - {s['losses']}L ({s['win_rate']:.0f}% win rate)")
        print(f"  P&L: ${s['pnl']:+.2f} | Avg: ${s['avg_return']:+.2f}/trade")

    # Combined
    c = summary["combined"]
    print(f"\n  ══ COMBINED ══")
    print(f"  Total trades: {c['total_trades']} ({c['open_positions']} open)")
    print(f"  Record: {c['wins']}W - {c['losses']}L ({c['win_rate']:.0f}%)")
    print(f"  Total P&L: ${c['total_pnl']:+.2f}")
    print(f"  Avg return: ${c['avg_return']:+.2f}/trade")
    print(f"  Sharpe-like: {c['sharpe']}")

    # Open positions
    ops = summary.get("open_positions", [])
    if ops:
        print(f"\n  ── Open Positions ({len(ops)}) ──")
        for p in ops:
            tag = "🌤" if p["strategy"] == "weather" else "₿"
            print(f"  {tag} {p['description']} @ {p['entry_price']} ({p['bet_size']}) [{p['opened']}]")

    # Recent trades
    recent = summary.get("recent_trades", [])
    if recent:
        print(f"\n  ── Recent Settled Trades ──")
        for t in recent[:10]:
            strat = t.get("_strategy", "?")
            result = t.get("result", "?")
            pnl = t.get("pnl", 0)
            date = t.get("date", t.get("settled_at", "?")[:10])
            emoji = "✅" if result == "win" else "❌"
            print(f"  {emoji} [{strat}] {date} — ${pnl:+.2f}")

    print("\n" + "=" * 60)


def main():
    weather_stats = load_json(WEATHER_STATS)
    kalshi_stats = load_json(KALSHI_STATS)

    strategies = []
    strategies.append(analyze_weather(weather_stats))
    strategies.append(analyze_kalshi(kalshi_stats))

    summary = build_summary(strategies)

    # Save JSON summary
    SUMMARY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SUMMARY_FILE, "w") as f:
        json.dump(summary, f, indent=2)

    # Print terminal report
    print_report(summary)

    print(f"\n  Summary saved to {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
