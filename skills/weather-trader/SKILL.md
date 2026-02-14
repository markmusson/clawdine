# Weather Trader Skill

Polymarket weather arbitrage using forecast data vs market odds.

## The Edge

Weather markets are predictable via meteorological data, but most traders ignore these "boring" markets. Free alpha.

**gopfan2 stats:** $2M+ profit, 70%+ win rate, 1,342 predictions.

## Strategy

1. Get forecast for target city/date (Open-Meteo API)
2. Find corresponding Polymarket temperature market (Gamma API, slug-based)
3. Compare: if forecast says 58°F and market has "56-57°F" at 60%, that's mispriced
4. Bet when forecast disagrees with market consensus

## Commands

```bash
# Check forecasts for all cities
python run.py forecast

# Scan for trading opportunities
python run.py scan

# Execute paper trades on found signals
python run.py trade

# Check portfolio status
python run.py status

# Resolve a trade (when market settles)
python run.py resolve --index N --won   # or --lost

# Demo mode (simulated markets)
python run.py demo
```

## Files

- `noaa.py` — Fetch forecasts from Open-Meteo (free, no key needed)
- `discover.py` — Find weather markets via Gamma API (slug-based queries)
- `signal.py` — Compare forecast vs market odds, generate signals
- `trade.py` — Paper/live trading, portfolio management
- `run.py` — CLI runner
- `paper_ledger.json` — Portfolio state

## Key Insight

Gamma API doesn't expose weather markets via standard queries. Use **slug-based** discovery:

```
highest-temperature-in-{city}-on-{month}-{day}-{year}
```

Example: `highest-temperature-in-nyc-on-february-8-2026`

## Supported Cities

- NYC (New York City) — LaGuardia Airport
- Atlanta — Hartsfield-Jackson
- London — City Airport (Celsius)
- Seattle — Sea-Tac
- Dallas — DFW

## Thresholds

- **Edge threshold:** 15%+ difference between forecast bucket and market odds
- **Position size:** 5% of portfolio per trade (paper default: $5)
- **Kelly fraction:** 0.25 (quarter Kelly for safety)
