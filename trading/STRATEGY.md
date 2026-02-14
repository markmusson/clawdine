# Weather Trading Strategy

## The Edge

Market overconfidence on precision. NOAA multi-day forecasts have ±7–9°F errors that markets don't price.

## Rules

- **Same-day:** Ladder YES (forecasts tight)
- **Multi-day:** Bet NO on precision (forecasts drift)
- **Position sizing:** One win must cover 2–3 losses

## Clawdine 1.0 Validation

- NO on precision: +$100 (clean win)
- YES on specific temps: −$48 (NOAA was 7–9°F off)
- Net: +$52 with 33% win rate

## Critical: Data Sources

**Polymarket resolves against KLGA (LaGuardia Airport) via Weather Underground, NOT Central Park.**

- All scripts use KLGA coords: 40.7772, −73.8726
- Forecast source: NOAA weather.gov API
- **DO NOT USE:** Open-Meteo or Central Park coords

## Trading System

| Component | Location |
|-----------|----------|
| Price logging | `price_log.jsonl` — daily snapshots (forecast + market + gap) |
| Gap alert | Triggers when NOAA KLGA diverges ≥3°F from market implied temp |
| Backtest | `trading/backtest/backtest.py` |
| BTC monitor | `scripts/kalshi-btc-monitor.py` — KXBTC price range markets |
| Polymarket data | `poly_data`, `gamma-api`, `py-clob-client` |

## Trading Autonomy (Feb 9, 2026)

Mark granted full decision-making autonomy on paper trades. If I see an opportunity, I take it — don't ask, just record it.

---

*See `PRINCIPLES.md` for experiment framework.*
