#!/usr/bin/env python3
"""
Discover weather markets on Polymarket via Gamma API.

KEY INSIGHT: Standard Gamma API queries don't expose weather markets.
Use SLUG-BASED queries instead:
  gamma-api.polymarket.com/events?slug=highest-temperature-in-{city}-on-{month}-{day}-{year}

This is the fix that makes discovery work.
"""

import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass

# City slug mappings
CITY_SLUGS = {
    "nyc": "nyc",           # or "new-york-city" for some markets
    "atlanta": "atlanta",
    "london": "london", 
    "seattle": "seattle",
    "dallas": "dallas"
}

# Polymarket uses different city names in slugs
CITY_SLUG_VARIANTS = {
    "nyc": ["nyc", "new-york-city"],
    "atlanta": ["atlanta"],
    "london": ["london"],
    "seattle": ["seattle"],
    "dallas": ["dallas"]
}

GAMMA_API = "https://gamma-api.polymarket.com"


@dataclass
class Market:
    slug: str
    title: str
    city: str
    date: str
    buckets: Dict[str, float]  # bucket_name -> price
    volume: float
    liquidity: float
    end_date: str
    active: bool
    
    def get_price(self, bucket: str) -> Optional[float]:
        """Get price for a specific temperature bucket."""
        # Try exact match first
        if bucket in self.buckets:
            return self.buckets[bucket]
        # Try partial match
        for b, price in self.buckets.items():
            if bucket.replace("°", "").lower() in b.replace("°", "").lower():
                return price
        return None
    
    def to_dict(self) -> Dict:
        return {
            "slug": self.slug,
            "title": self.title,
            "city": self.city,
            "date": self.date,
            "buckets": self.buckets,
            "volume": self.volume,
            "liquidity": self.liquidity,
            "end_date": self.end_date,
            "active": self.active
        }


def build_slug(city: str, date: datetime) -> str:
    """
    Build Polymarket event slug for a city and date.
    
    Format: highest-temperature-in-{city}-on-{month}-{day}-{year}
    Example: highest-temperature-in-nyc-on-february-8-2026
    """
    month = date.strftime("%B").lower()
    day = date.day
    year = date.year
    city_slug = CITY_SLUGS.get(city, city)
    return f"highest-temperature-in-{city_slug}-on-{month}-{day}-{year}"


def get_market(city: str, date: datetime) -> Optional[Market]:
    """
    Fetch a specific weather market by city and date.
    """
    # Try different slug variants
    variants = CITY_SLUG_VARIANTS.get(city, [city])
    
    for city_variant in variants:
        slug = build_slug(city_variant, date) if city_variant != city else build_slug(city, date)
        
        # Override slug building for variants
        if city_variant != CITY_SLUGS.get(city, city):
            month = date.strftime("%B").lower()
            day = date.day
            year = date.year
            slug = f"highest-temperature-in-{city_variant}-on-{month}-{day}-{year}"
        
        url = f"{GAMMA_API}/events?slug={slug}"
        
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            if not data:
                continue
            
            event = data[0]
            
            # Parse markets (temperature buckets)
            buckets = {}
            markets = event.get("markets", [])
            
            for m in markets:
                title = m.get("groupItemTitle", "")
                prices = m.get("outcomePrices", "[]")
                
                # Parse prices (JSON string)
                try:
                    import json
                    price_list = json.loads(prices)
                    yes_price = float(price_list[0]) if price_list else 0
                except:
                    yes_price = 0
                
                if title:
                    buckets[title] = yes_price
            
            if buckets:
                return Market(
                    slug=slug,
                    title=event.get("title", ""),
                    city=city,
                    date=date.strftime("%Y-%m-%d"),
                    buckets=buckets,
                    volume=event.get("volume", 0),
                    liquidity=event.get("liquidity", 0),
                    end_date=event.get("endDate", ""),
                    active=not event.get("closed", False)
                )
                
        except Exception as e:
            continue
    
    return None


def discover_markets(days_ahead: int = 2) -> List[Market]:
    """
    Discover all active weather markets for the next N days.
    """
    markets = []
    
    for days in range(0, days_ahead + 1):
        target_date = datetime.now() + timedelta(days=days)
        
        for city in CITY_SLUGS:
            market = get_market(city, target_date)
            if market and market.active:
                markets.append(market)
    
    return markets


def get_market_for_forecast(city: str, date_str: str) -> Optional[Market]:
    """
    Get market matching a forecast's city and date.
    """
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return get_market(city, date)


if __name__ == "__main__":
    # Test
    print("Discovering weather markets...\n")
    
    # Test specific market
    from datetime import datetime
    tomorrow = datetime.now() + timedelta(days=1)
    
    print(f"Looking for NYC market for {tomorrow.strftime('%Y-%m-%d')}...")
    market = get_market("nyc", tomorrow)
    
    if market:
        print(f"\n✅ Found: {market.title}")
        print(f"   Volume: ${market.volume:,.0f}")
        print(f"   Buckets:")
        for bucket, price in sorted(market.buckets.items()):
            print(f"      {bucket}: {price*100:.1f}%")
    else:
        print("   No market found")
    
    # Test discover all
    print("\n\nDiscovering all markets (today + tomorrow)...")
    all_markets = discover_markets(days_ahead=1)
    print(f"Found {len(all_markets)} markets")
    for m in all_markets:
        print(f"  - {m.city}: {m.date} ({len(m.buckets)} buckets)")
