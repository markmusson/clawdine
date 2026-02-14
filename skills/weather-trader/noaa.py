#!/usr/bin/env python3
"""
Fetch weather forecasts from Open-Meteo API.
Free, no API key required.
"""

import requests
from datetime import datetime, timedelta
from typing import Dict, Optional
from dataclasses import dataclass

# City configurations
CITIES = {
    "nyc": {
        "name": "New York City",
        "lat": 40.7128,
        "lon": -74.006,
        "unit": "fahrenheit",
        "timezone": "America/New_York"
    },
    "atlanta": {
        "name": "Atlanta",
        "lat": 33.749,
        "lon": -84.388,
        "unit": "fahrenheit",
        "timezone": "America/New_York"
    },
    "london": {
        "name": "London",
        "lat": 51.5074,
        "lon": -0.1278,
        "unit": "celsius",
        "timezone": "Europe/London"
    },
    "seattle": {
        "name": "Seattle",
        "lat": 47.6062,
        "lon": -122.3321,
        "unit": "fahrenheit",
        "timezone": "America/Los_Angeles"
    },
    "dallas": {
        "name": "Dallas",
        "lat": 32.7767,
        "lon": -96.7970,
        "unit": "fahrenheit",
        "timezone": "America/Chicago"
    }
}


@dataclass
class Forecast:
    city: str
    city_name: str
    date: str
    high_temp: float
    low_temp: float
    unit: str
    confidence: float = 0.85  # Default confidence for 1-2 day forecasts
    
    @property
    def bucket(self) -> str:
        """Return the temperature bucket this forecast falls into."""
        temp = int(round(self.high_temp))
        return f"{temp}°{self.unit[0].upper()}"
    
    def to_dict(self) -> Dict:
        return {
            "city": self.city,
            "city_name": self.city_name,
            "date": self.date,
            "high_temp": self.high_temp,
            "low_temp": self.low_temp,
            "unit": self.unit,
            "confidence": self.confidence,
            "bucket": self.bucket
        }


def get_forecast(city: str, date: Optional[str] = None, days_ahead: int = 1) -> Optional[Forecast]:
    """
    Get forecast for a city on a specific date.
    
    Args:
        city: City key (nyc, atlanta, london, seattle, dallas)
        date: Date string (YYYY-MM-DD) or None for days_ahead
        days_ahead: Days from today (used if date is None)
    
    Returns:
        Forecast object or None if failed
    """
    if city not in CITIES:
        print(f"Unknown city: {city}. Available: {list(CITIES.keys())}")
        return None
    
    config = CITIES[city]
    
    # Determine target date
    if date:
        target_date = datetime.strptime(date, "%Y-%m-%d")
    else:
        target_date = datetime.now() + timedelta(days=days_ahead)
    
    date_str = target_date.strftime("%Y-%m-%d")
    
    # Calculate days from now for confidence adjustment
    days_out = (target_date - datetime.now()).days
    
    # Confidence decreases with forecast horizon
    # Day 0-1: 0.90, Day 2: 0.85, Day 3: 0.75, Day 4+: 0.65
    confidence_map = {0: 0.92, 1: 0.90, 2: 0.85, 3: 0.75}
    confidence = confidence_map.get(days_out, 0.65)
    
    # Build API URL
    temp_unit = "fahrenheit" if config["unit"] == "fahrenheit" else "celsius"
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={config['lat']}"
        f"&longitude={config['lon']}"
        f"&daily=temperature_2m_max,temperature_2m_min"
        f"&temperature_unit={temp_unit}"
        f"&timezone={config['timezone']}"
        f"&start_date={date_str}"
        f"&end_date={date_str}"
    )
    
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        daily = data.get("daily", {})
        highs = daily.get("temperature_2m_max", [])
        lows = daily.get("temperature_2m_min", [])
        
        if not highs or not lows:
            print(f"No forecast data for {city} on {date_str}")
            return None
        
        return Forecast(
            city=city,
            city_name=config["name"],
            date=date_str,
            high_temp=highs[0],
            low_temp=lows[0],
            unit=config["unit"],
            confidence=confidence
        )
        
    except Exception as e:
        print(f"Error fetching forecast for {city}: {e}")
        return None


def get_all_forecasts(days_ahead: int = 1) -> Dict[str, Forecast]:
    """Get forecasts for all supported cities."""
    forecasts = {}
    for city in CITIES:
        forecast = get_forecast(city, days_ahead=days_ahead)
        if forecast:
            forecasts[city] = forecast
    return forecasts


if __name__ == "__main__":
    # Test
    print("Fetching forecasts for tomorrow...\n")
    forecasts = get_all_forecasts(days_ahead=1)
    for city, fc in forecasts.items():
        print(f"{fc.city_name}: {fc.high_temp}°{fc.unit[0].upper()} (confidence: {fc.confidence})")
