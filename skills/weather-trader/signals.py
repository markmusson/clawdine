#!/usr/bin/env python3
"""
Signal generation: compare forecast to market odds, find edge.

The core logic:
1. Get NOAA/Open-Meteo forecast for city/date
2. Find which bucket the forecast falls into
3. Check market price for that bucket
4. If market price < expected (based on forecast confidence), that's edge

Example:
  Forecast: 58°F (confidence 0.85)
  Market bucket "56-59°F": 60% YES
  Expected: ~85% if forecast is right
  Edge: 85% - 60% = 25% underpriced → BUY signal
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from noaa import Forecast
from discover import Market


@dataclass
class Signal:
    city: str
    date: str
    action: str           # BUY_YES, BUY_NO, or NONE
    bucket: str           # Target bucket
    market_price: float   # Current market price
    expected_price: float # Our expected fair price
    edge: float          # Expected - Market (positive = underpriced)
    confidence: float    # Forecast confidence
    forecast_temp: float # Actual forecast temperature
    market_title: str
    market_slug: str
    
    @property
    def is_trade(self) -> bool:
        return self.action != "NONE" and self.edge > 0.10  # 10% minimum edge
    
    def to_dict(self) -> Dict:
        return {
            "city": self.city,
            "date": self.date,
            "action": self.action,
            "bucket": self.bucket,
            "market_price": self.market_price,
            "expected_price": self.expected_price,
            "edge": self.edge,
            "confidence": self.confidence,
            "forecast_temp": self.forecast_temp,
            "market_title": self.market_title,
            "market_slug": self.market_slug
        }


def find_bucket(temp: float, buckets: Dict[str, float], unit: str = "fahrenheit") -> Tuple[str, float]:
    """
    Find which market bucket a temperature falls into.
    
    Returns: (bucket_name, current_price)
    """
    temp_int = int(round(temp))
    unit_char = "F" if unit == "fahrenheit" else "C"
    
    for bucket_name, price in buckets.items():
        # Parse bucket ranges
        name_lower = bucket_name.lower().replace("°", "").replace("f", "").replace("c", "")
        
        # Handle "X or below" format
        if "or below" in bucket_name.lower() or "below" in bucket_name.lower():
            try:
                threshold = int(''.join(filter(str.isdigit, bucket_name.split()[0])))
                if temp_int <= threshold:
                    return bucket_name, price
            except:
                pass
        
        # Handle "X or higher" / "X or above" format  
        elif "or higher" in bucket_name.lower() or "or above" in bucket_name.lower():
            try:
                threshold = int(''.join(filter(str.isdigit, bucket_name.split()[0])))
                if temp_int >= threshold:
                    return bucket_name, price
            except:
                pass
        
        # Handle "X-Y" range format (e.g., "56-57°F")
        elif "-" in name_lower:
            try:
                parts = name_lower.replace(" ", "").split("-")
                low = int(''.join(filter(str.isdigit, parts[0])))
                high = int(''.join(filter(str.isdigit, parts[1])))
                if low <= temp_int <= high:
                    return bucket_name, price
            except:
                pass
        
        # Handle exact match (e.g., "57°F")
        else:
            try:
                bucket_temp = int(''.join(filter(str.isdigit, bucket_name)))
                if temp_int == bucket_temp:
                    return bucket_name, price
            except:
                pass
    
    # If no match found, return closest bucket
    return _find_closest_bucket(temp_int, buckets)


def _find_closest_bucket(temp: int, buckets: Dict[str, float]) -> Tuple[str, float]:
    """Find the closest bucket when exact match fails."""
    best_bucket = None
    best_price = 0
    best_diff = float('inf')
    
    for bucket_name, price in buckets.items():
        try:
            # Extract any number from bucket name
            nums = [int(s) for s in bucket_name.replace("-", " ").split() if s.isdigit()]
            if nums:
                bucket_mid = sum(nums) / len(nums)
                diff = abs(temp - bucket_mid)
                if diff < best_diff:
                    best_diff = diff
                    best_bucket = bucket_name
                    best_price = price
        except:
            pass
    
    return best_bucket or list(buckets.keys())[0], best_price


def generate_signal(forecast: Forecast, market: Market, edge_threshold: float = 0.15) -> Signal:
    """
    Generate a trading signal by comparing forecast to market.
    
    Args:
        forecast: Weather forecast for city/date
        market: Polymarket temperature market
        edge_threshold: Minimum edge to signal (default 15%)
    
    Returns:
        Signal object with trade recommendation
    """
    # Find the bucket our forecast falls into
    bucket_name, market_price = find_bucket(
        forecast.high_temp, 
        market.buckets,
        forecast.unit
    )
    
    # Expected price based on forecast confidence
    # If forecast says it'll be in this bucket, fair price ≈ confidence
    expected_price = forecast.confidence
    
    # Calculate edge
    edge = expected_price - market_price
    
    # Determine action
    if edge >= edge_threshold:
        action = "BUY_YES"  # Market underpricing, buy YES
    elif edge <= -edge_threshold:
        action = "BUY_NO"   # Market overpricing, buy NO
    else:
        action = "NONE"     # No significant edge
    
    return Signal(
        city=forecast.city,
        date=forecast.date,
        action=action,
        bucket=bucket_name,
        market_price=market_price,
        expected_price=expected_price,
        edge=edge,
        confidence=forecast.confidence,
        forecast_temp=forecast.high_temp,
        market_title=market.title,
        market_slug=market.slug
    )


def scan_for_signals(days_ahead: int = 2, edge_threshold: float = 0.15) -> List[Signal]:
    """
    Scan all available markets for trading signals.
    """
    from noaa import get_all_forecasts
    from discover import discover_markets, get_market_for_forecast
    
    signals = []
    
    for days in range(0, days_ahead + 1):
        forecasts = get_all_forecasts(days_ahead=days)
        
        for city, forecast in forecasts.items():
            market = get_market_for_forecast(city, forecast.date)
            
            if market and market.active:
                signal = generate_signal(forecast, market, edge_threshold)
                signals.append(signal)
    
    return signals


if __name__ == "__main__":
    # Test
    print("Scanning for trading signals...\n")
    
    signals = scan_for_signals(days_ahead=1, edge_threshold=0.10)
    
    for sig in signals:
        emoji = "🟢" if sig.is_trade else "⚪"
        print(f"{emoji} {sig.city.upper()} ({sig.date})")
        print(f"   Forecast: {sig.forecast_temp}° → Bucket: {sig.bucket}")
        print(f"   Market: {sig.market_price*100:.1f}% | Expected: {sig.expected_price*100:.1f}%")
        print(f"   Edge: {sig.edge*100:+.1f}% | Action: {sig.action}")
        print()
