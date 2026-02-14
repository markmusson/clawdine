#!/usr/bin/env python3
"""
Daily Trading Report
Reads portfolio_summary.json and outputs a Telegram-friendly report to stdout.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SUMMARY_FILE = Path.home() / ".openclaw/workspace/trading/portfolio_summary.json"


def main():
    if not SUMMARY_FILE.exists():
        print("No portfolio summary found. Run portfolio.py first.")
        sys.exit(1)

    with open(SUMMARY_FILE) as f:
        s = json.load(f)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    c = s["combined"]

    lines = [
        f"📊 Paper Trading Report — {today}",
        "",
        f"💰 Total P&L: ${c['total_pnl']:+.2f}",
        f"📈 Record: {c['wins']}W-{c['losses']}L ({c['win_rate']:.0f}%)",
        f"📉 Sharpe: {c['sharpe']}",
    ]

    # Per strategy
    for strat in s["strategies"]:
        lines.append("")
        lines.append(f"• {strat['name']}: ${strat['pnl']:+.2f} P&L, "
                      f"{strat['wins']}W-{strat['losses']}L, "
                      f"{strat['open_count']} open")

    # Open positions
    ops = s.get("open_positions", [])
    if ops:
        lines.append("")
        lines.append(f"📌 Open positions ({len(ops)}):")
        for p in ops:
            tag = "🌤" if p["strategy"] == "weather" else "₿"
            lines.append(f"  {tag} {p['description'][:50]} @ {p['entry_price']}")

    # Recent settled today
    recent_today = [t for t in s.get("recent_trades", [])
                    if t.get("settled_at", "")[:10] == today]
    if recent_today:
        lines.append("")
        lines.append(f"🔔 Closed today ({len(recent_today)}):")
        for t in recent_today:
            emoji = "✅" if t.get("result") == "win" else "❌"
            lines.append(f"  {emoji} {t.get('date', '?')} — ${t.get('pnl', 0):+.2f}")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
