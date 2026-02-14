#!/usr/bin/env python3
"""
Weather Trader CLI

Commands:
  forecast [--city CITY]  - Check forecasts
  scan                    - Find trading opportunities
  trade                   - Execute paper trades on signals
  status                  - Check portfolio
  resolve --index N --won/--lost - Settle a trade
  demo                    - Test with simulated markets
  reset [--balance N]     - Reset portfolio
"""

import argparse
import sys
from datetime import datetime, timedelta


def cmd_forecast(args):
    """Show forecasts for all or specific city."""
    from noaa import get_forecast, get_all_forecasts, CITIES
    
    days = args.days if hasattr(args, 'days') else 1
    
    if args.city:
        if args.city not in CITIES:
            print(f"Unknown city: {args.city}")
            print(f"Available: {', '.join(CITIES.keys())}")
            return
        
        forecast = get_forecast(args.city, days_ahead=days)
        if forecast:
            print(f"\n🌡️  {forecast.city_name} ({forecast.date})")
            print(f"   High: {forecast.high_temp}°{forecast.unit[0].upper()}")
            print(f"   Low: {forecast.low_temp}°{forecast.unit[0].upper()}")
            print(f"   Confidence: {forecast.confidence*100:.0f}%")
    else:
        print(f"\n📊 Forecasts for +{days} day(s):\n")
        forecasts = get_all_forecasts(days_ahead=days)
        for city, fc in forecasts.items():
            print(f"🌡️  {fc.city_name}: {fc.high_temp}°{fc.unit[0].upper()} (conf: {fc.confidence*100:.0f}%)")


def cmd_scan(args):
    """Scan for trading opportunities."""
    from signals import scan_for_signals
    
    edge = args.edge if hasattr(args, 'edge') else 0.15
    days = args.days if hasattr(args, 'days') else 2
    
    print(f"\n🔍 Scanning for signals (edge threshold: {edge*100:.0f}%)...\n")
    
    signals = scan_for_signals(days_ahead=days, edge_threshold=edge)
    
    trades = [s for s in signals if s.is_trade]
    
    if not signals:
        print("No markets found. Weather markets may not be active.")
        return
    
    for sig in signals:
        emoji = "🟢" if sig.is_trade else "⚪"
        print(f"{emoji} {sig.city.upper()} ({sig.date})")
        print(f"   Forecast: {sig.forecast_temp}° → Bucket: {sig.bucket}")
        print(f"   Market: {sig.market_price*100:.1f}% | Expected: {sig.expected_price*100:.1f}%")
        print(f"   Edge: {sig.edge*100:+.1f}% | Action: {sig.action}")
        print()
    
    print(f"Found {len(trades)} trade(s) with edge > {edge*100:.0f}%")


def cmd_trade(args):
    """Execute paper trades on found signals."""
    from signals import scan_for_signals
    from trade import execute_paper_trade, get_status
    
    edge = args.edge if hasattr(args, 'edge') else 0.15
    size = args.size if hasattr(args, 'size') else 5.0
    
    print(f"\n📝 Finding signals and executing paper trades...\n")
    
    signals = scan_for_signals(days_ahead=2, edge_threshold=edge)
    trades = [s for s in signals if s.is_trade]
    
    if not trades:
        print("No trading signals found.")
        return
    
    for sig in trades:
        trade = execute_paper_trade(sig, size=size)
        if trade:
            print(f"✅ {sig.city.upper()}: ${size:.2f} {sig.action} on '{sig.bucket}' @ {sig.market_price*100:.1f}%")
            print(f"   Edge: {sig.edge*100:+.1f}% | Forecast: {sig.forecast_temp}°")
    
    # Show status
    print()
    status = get_status()
    print(f"💰 Balance: ${status['balance']:.2f} | Pending: {status['pending_count']} trades")


def cmd_status(args):
    """Show portfolio status."""
    from trade import get_status
    
    status = get_status()
    
    print("\n=== PAPER TRADING STATUS ===")
    print(f"💰 Balance: ${status['balance']:.2f}")
    print(f"📈 Total P&L: ${status['total_pnl']:+.2f}")
    print(f"📊 ROI: {status['roi']:+.1f}%")
    print(f"🎯 Win Rate: {status['win_rate']:.0f}% ({status['wins']}W-{status['losses']}L)")
    print(f"⏳ Pending: {status['pending_count']} trades (${status['pending_exposure']:.2f})")
    
    if status['pending']:
        print("\n📋 Pending Trades:")
        for i, t in enumerate(status['pending']):
            print(f"   [{i}] {t['city'].upper()} {t['date']}: {t['action']} '{t['bucket']}' ${t['size']:.2f}")


def cmd_resolve(args):
    """Resolve a pending trade."""
    from trade import resolve_trade, get_status
    
    if args.index is None:
        print("Error: --index required")
        return
    
    if not args.won and not args.lost:
        print("Error: must specify --won or --lost")
        return
    
    trade = resolve_trade(args.index, won=args.won)
    
    if trade:
        result = "✅ WON" if trade.status == "WON" else "❌ LOST"
        print(f"\n{result}: {trade.city.upper()} {trade.date}")
        print(f"   P&L: ${trade.pnl:+.2f}")
        
        status = get_status()
        print(f"\n💰 Balance: ${status['balance']:.2f} | Total P&L: ${status['total_pnl']:+.2f}")


def cmd_demo(args):
    """Run demo with simulated markets."""
    print("\n🎮 DEMO MODE - Simulating weather markets\n")
    
    # Simulated signals
    demo_signals = [
        ("atlanta", "2026-02-08", "56-58°F", 0.60, 57.0, 0.25),
        ("seattle", "2026-02-08", "48-50°F", 0.55, 49.0, 0.30),
        ("dallas", "2026-02-08", "62-64°F", 0.50, 63.0, 0.35),
        ("nyc", "2026-02-08", "28-30°F", 0.45, 29.0, 0.40),
    ]
    
    for city, date, bucket, price, temp, edge in demo_signals:
        print(f"🟢 DEMO SIGNAL: BUY_YES | Edge: {edge*100:.0f}% | {city.upper()}")
        print(f"   NOAA: {temp}°F | Market Q: Will {city.upper()} high be {bucket} on {date}?")
    
    print("\n📝 Executing demo paper trades...")
    
    balance = 100.0
    for i, (city, date, bucket, price, temp, edge) in enumerate(demo_signals):
        size = round(5 * (1 - i*0.05), 2)  # Decreasing Kelly
        balance -= size
        print(f"✅ {city.upper()}: ${size:.2f} @ {price:.2f}")
    
    print(f"\n=== PAPER TRADING STATUS ===")
    print(f"Balance: ${balance:.2f}")
    print(f"Total PnL: $+0.00")
    print(f"Win Rate: 0% (0W-0L)")
    print(f"Pending: {len(demo_signals)} trades")


def cmd_reset(args):
    """Reset portfolio."""
    from trade import reset_portfolio
    balance = args.balance if hasattr(args, 'balance') and args.balance else 100.0
    reset_portfolio(initial_balance=balance)


def main():
    parser = argparse.ArgumentParser(description="Weather Trader - Polymarket weather arbitrage")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # forecast
    p_forecast = subparsers.add_parser("forecast", help="Check weather forecasts")
    p_forecast.add_argument("--city", "-c", help="Specific city (nyc, atlanta, london, seattle, dallas)")
    p_forecast.add_argument("--days", "-d", type=int, default=1, help="Days ahead (default: 1)")
    
    # scan
    p_scan = subparsers.add_parser("scan", help="Scan for trading opportunities")
    p_scan.add_argument("--edge", "-e", type=float, default=0.15, help="Edge threshold (default: 0.15)")
    p_scan.add_argument("--days", "-d", type=int, default=2, help="Days to scan (default: 2)")
    
    # trade
    p_trade = subparsers.add_parser("trade", help="Execute paper trades")
    p_trade.add_argument("--edge", "-e", type=float, default=0.15, help="Edge threshold (default: 0.15)")
    p_trade.add_argument("--size", "-s", type=float, default=5.0, help="Trade size in $ (default: 5.0)")
    
    # status
    p_status = subparsers.add_parser("status", help="Check portfolio status")
    
    # resolve
    p_resolve = subparsers.add_parser("resolve", help="Resolve a pending trade")
    p_resolve.add_argument("--index", "-i", type=int, required=True, help="Trade index (from status)")
    p_resolve.add_argument("--won", action="store_true", help="Trade won")
    p_resolve.add_argument("--lost", action="store_true", help="Trade lost")
    
    # demo
    p_demo = subparsers.add_parser("demo", help="Run demo mode")
    
    # reset
    p_reset = subparsers.add_parser("reset", help="Reset portfolio")
    p_reset.add_argument("--balance", "-b", type=float, default=100.0, help="Initial balance (default: 100)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    commands = {
        "forecast": cmd_forecast,
        "scan": cmd_scan,
        "trade": cmd_trade,
        "status": cmd_status,
        "resolve": cmd_resolve,
        "demo": cmd_demo,
        "reset": cmd_reset,
    }
    
    commands[args.command](args)


if __name__ == "__main__":
    main()
