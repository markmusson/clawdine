#!/usr/bin/env python3
"""
Paper and live trading execution.

Paper trading uses a JSON ledger to track positions.
Live trading would use py-clob-client (not implemented yet).
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from signals import Signal

LEDGER_FILE = os.path.join(os.path.dirname(__file__), "paper_ledger.json")

DEFAULT_PORTFOLIO = {
    "balance": 100.0,
    "initial_balance": 100.0,
    "trades": [],
    "pending": [],
    "wins": 0,
    "losses": 0,
    "total_pnl": 0.0,
    "created": datetime.now().isoformat(),
    "updated": datetime.now().isoformat()
}


@dataclass
class Trade:
    id: int
    city: str
    date: str
    bucket: str
    action: str          # BUY_YES or BUY_NO
    entry_price: float
    size: float          # Dollar amount
    edge: float
    forecast_temp: float
    market_slug: str
    status: str          # PENDING, WON, LOST
    pnl: float
    created: str
    resolved: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, d: Dict) -> "Trade":
        return cls(**d)


def load_portfolio() -> Dict:
    """Load portfolio from ledger file."""
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_PORTFOLIO.copy()


def save_portfolio(portfolio: Dict):
    """Save portfolio to ledger file."""
    portfolio["updated"] = datetime.now().isoformat()
    with open(LEDGER_FILE, "w") as f:
        json.dump(portfolio, f, indent=2)


def execute_paper_trade(signal: Signal, size: float = 5.0) -> Optional[Trade]:
    """
    Execute a paper trade based on a signal.
    
    Args:
        signal: Trading signal
        size: Dollar amount to trade (default $5)
    
    Returns:
        Trade object or None if insufficient balance
    """
    portfolio = load_portfolio()
    
    # Check balance
    if portfolio["balance"] < size:
        print(f"Insufficient balance: ${portfolio['balance']:.2f} < ${size:.2f}")
        return None
    
    # Create trade
    trade_id = len(portfolio["trades"]) + len(portfolio["pending"]) + 1
    
    trade = Trade(
        id=trade_id,
        city=signal.city,
        date=signal.date,
        bucket=signal.bucket,
        action=signal.action,
        entry_price=signal.market_price,
        size=size,
        edge=signal.edge,
        forecast_temp=signal.forecast_temp,
        market_slug=signal.market_slug,
        status="PENDING",
        pnl=0.0,
        created=datetime.now().isoformat()
    )
    
    # Deduct from balance
    portfolio["balance"] -= size
    portfolio["pending"].append(trade.to_dict())
    
    save_portfolio(portfolio)
    
    return trade


def resolve_trade(trade_index: int, won: bool) -> Optional[Trade]:
    """
    Resolve a pending trade.
    
    Args:
        trade_index: Index in pending list (0-based)
        won: True if trade won, False if lost
    
    Returns:
        Resolved Trade object
    """
    portfolio = load_portfolio()
    
    if trade_index >= len(portfolio["pending"]):
        print(f"Invalid trade index: {trade_index}")
        return None
    
    # Get and remove from pending
    trade_dict = portfolio["pending"].pop(trade_index)
    trade = Trade.from_dict(trade_dict)
    
    # Calculate P&L
    if won:
        if trade.action == "BUY_YES":
            # Bought YES, it resolved YES
            # Payout = size / entry_price, profit = payout - size
            payout = trade.size / trade.entry_price
            trade.pnl = payout - trade.size
        else:
            # Bought NO, it resolved NO
            payout = trade.size / (1 - trade.entry_price)
            trade.pnl = payout - trade.size
        trade.status = "WON"
        portfolio["wins"] += 1
    else:
        # Lost the bet
        trade.pnl = -trade.size
        trade.status = "LOST"
        portfolio["losses"] += 1
    
    trade.resolved = datetime.now().isoformat()
    
    # Update portfolio
    portfolio["balance"] += trade.size + trade.pnl
    portfolio["total_pnl"] += trade.pnl
    portfolio["trades"].append(trade.to_dict())
    
    save_portfolio(portfolio)
    
    return trade


def get_status() -> Dict:
    """Get current portfolio status."""
    portfolio = load_portfolio()
    
    total_trades = portfolio["wins"] + portfolio["losses"]
    win_rate = (portfolio["wins"] / total_trades * 100) if total_trades > 0 else 0
    
    return {
        "balance": portfolio["balance"],
        "initial_balance": portfolio["initial_balance"],
        "total_pnl": portfolio["total_pnl"],
        "roi": (portfolio["total_pnl"] / portfolio["initial_balance"] * 100) if portfolio["initial_balance"] > 0 else 0,
        "wins": portfolio["wins"],
        "losses": portfolio["losses"],
        "win_rate": win_rate,
        "pending_count": len(portfolio["pending"]),
        "pending_exposure": sum(t["size"] for t in portfolio["pending"]),
        "pending": portfolio["pending"]
    }


def reset_portfolio(initial_balance: float = 100.0):
    """Reset portfolio to initial state."""
    portfolio = DEFAULT_PORTFOLIO.copy()
    portfolio["balance"] = initial_balance
    portfolio["initial_balance"] = initial_balance
    portfolio["created"] = datetime.now().isoformat()
    save_portfolio(portfolio)
    print(f"Portfolio reset with ${initial_balance:.2f}")


if __name__ == "__main__":
    # Test
    status = get_status()
    print("=== PORTFOLIO STATUS ===")
    print(f"Balance: ${status['balance']:.2f}")
    print(f"Total P&L: ${status['total_pnl']:+.2f}")
    print(f"ROI: {status['roi']:+.1f}%")
    print(f"Win Rate: {status['win_rate']:.0f}% ({status['wins']}W-{status['losses']}L)")
    print(f"Pending: {status['pending_count']} trades (${status['pending_exposure']:.2f})")
