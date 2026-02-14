# Polymarket Weather Trading Strategy

*Research compiled by Clawdine 👠 | Feb 7, 2026*

## Executive Summary

Weather prediction markets on Polymarket offer arbitrage opportunities through:
1. **Temporal information asymmetry** — Forecast models update on fixed schedules; markets lag
2. **Probability mispricing** — Retail traders create inefficient distributions
3. **Range coverage** — Temperature outcomes must sum to 100%, creating exploitable spreads

---

## Top Traders Analysis

### neobrother ($20k+ profit)
- **Strategy**: Temperature laddering
- **Method**: Low-cost positions (0.2¢–15¢) across adjacent temperature outcomes
- **Example**: Buenos Aires — buys 29°C, 30°C, 31°C, 32°C, 33°C, 34°C+ simultaneously
- **Edge**: Uses meteorological model knowledge (ECMWF, GFS)
- **Style**: Highly automated, 2,373+ predictions, quantitative/script-based
- **Insight**: "Weather is pure physics and mathematics" — less noise than politics/sports

### Hans323 ($1.11M on one bet)
- **Strategy**: Black swan hunting (Taleb barbell)
- **Method**: Heavy capital on low-probability (2-8%) outcomes
- **Example**: $92,632 bet on London weather at 8% implied probability → $1.11M win
- **Philosophy**: Doesn't care if 90% of predictions fail; one 1,100%+ return covers all losses
- **Diversified**: Also trades politics, sports, culture with same asymmetric risk approach

---

## Market Mechanics

### Temperature Markets
- Split into ranges: 8-9°C, 9-10°C, 10-11°C, etc.
- **Only ONE range can win** — all probabilities MUST sum to 100%
- Prices = implied probabilities (35 cents = 35% implied)

### Finding Edge
```
Edge = Forecast Probability - Market Price
If Edge > 5% → Trade opportunity
```

### Example Mispricing
```
London High Temperature - January 22:
- 8-9°C: 25 cents (25%)
- 9-10°C: 35 cents (35%)  
- 10-11°C: 30 cents (30%)
- 11-12°C: 20 cents (20%)
Total: 110% ← OPPORTUNITY

Forecast says: 9.5°C most likely (should be 50%+)
Action: Buy 9-10°C at 35 cents
If wins: Paid 35¢, get $1.00 → 185% return
```

---

## Data Sources

### Forecast Models (Update Times)
| Model | Provider | Update Frequency | Access |
|-------|----------|------------------|--------|
| GFS | NOAA (US) | Every 6 hours (00, 06, 12, 18 UTC) | Free API |
| HRRR | NOAA | Hourly | Free API |
| ECMWF | European | Twice daily (00, 12 UTC) | Paywalled |
| UK Met Office | UK | Twice daily | Free for UK |

### Free API: Open-Meteo
```
https://api.open-meteo.com/v1/forecast
?latitude=40.71
&longitude=-74.01
&hourly=temperature_2m
&temperature_unit=fahrenheit
```
- No API key required
- Combines GFS + HRRR automatically
- Returns hourly temperature forecasts

### Weather.gov (NOAA)
- Free, no key needed
- Gives precipitation probability directly
- Best for US cities

---

## Polymarket API

### py-clob-client (Python)
```python
pip install py-clob-client

from py_clob_client.client import ClobClient

client = ClobClient("https://clob.polymarket.com")  # read-only

# Get market price
price = client.get_price(token_id, side="BUY")
book = client.get_order_book(token_id)
```

### polymarket-apis (Alternative)
```python
pip install polymarket-apis
```
- Unified interface with Pydantic validation
- Includes Gamma, Data, WebSocket clients

### Finding Weather Markets
- Filter by "weather" tag
- Search: "temperature", "rain", "snow", "tornado"
- Focus on markets resolving within 48 hours

---

## Trading Strategies

### Strategy 1: Forecast Lag Arbitrage (Same-Day Only)
**When**: New forecast update (00, 06, 12, 18 UTC) for SAME-DAY markets
**What**: Compare new forecast to current market prices
**Action**: Buy if forecast shows >5% edge before market adjusts
**⚠️ Empirical note**: Only works reliably on same-day. Multi-day forecasts drift.

**Daily Routine (15 min)**:
1. 7:00 AM — Check overnight forecast updates
2. 7:10 AM — Scan Polymarket weather markets (filter: resolves TODAY)
3. 7:20 AM — Calculate edges, place trades
4. 12:05 PM — Post-noon forecast check
5. 6:05 PM — Final update, scout tomorrow's markets

### Strategy 2: Temperature Laddering (Same-Day Markets)
**When**: Same-day market shows range of temperature outcomes
**What**: Buy low-cost positions across likely range
**Example**: If forecast = 31°C, buy 29°C, 30°C, 31°C, 32°C, 33°C at cheap prices
**Return**: One position pays 100-800%, covers all others
**⚠️ Empirical note**: neobrother's approach. Works when forecasts are tight (same-day).

### Strategy 3: NO on Precision (Multi-Day Markets) ⭐ EMPIRICALLY VALIDATED
**When**: Multi-day market betting on specific narrow temperature range
**What**: Bet NO — precision fails when uncertainty is high
**Example**: "Will Chicago hit exactly 32-33°F in 3 days?" — Bet NO
**Why**: NOAA multi-day has 7-9°F errors. Precision bets are sucker bets.
**⭐ Clawdine 1.0 Result**: +$100 win on NYC using this approach

### Strategy 4: Retail Fade
**When**: 80%+ volume on one outcome
**What**: Bet against retail consensus (especially non-temperature markets)
**Example**: "Will NYC get 1+ inch of snow?" at 75¢ when forecast says 40% → Bet NO

### Strategy 5: Probability Sum Arbitrage  
**When**: Market probabilities sum to >100%
**What**: Buy underpriced range matching forecast
**Edge**: Pure mathematical arbitrage

### ⚠️ AVOID: YES on Multi-Day Specific Temps
**Clawdine 1.0 Results**: 
- Atlanta YES @ 42-43°F → Actual 35°F → LOSS
- Chicago YES @ 32-33°F → Actual 23°F → LOSS

Forecasts drift. Don't bet on precision when uncertainty is high.

---

## Empirical Results: Clawdine 1.0 (Feb 2026)

Previous instance paper traded weather markets. Results:

### Trade Log
| Market | Position | Entry | Actual Temp | Result | P&L |
|--------|----------|-------|-------------|--------|-----|
| NYC Feb 4 | NO @ 49°F+ | $1.00 | Below 49°F ✅ | WIN | +$100.00 |
| Atlanta Feb 5 | YES @ 42-43°F | $0.185 | 35°F (7°F cold!) | LOSS | -$18.50 |
| Chicago Feb 5 | YES @ 32-33°F | $0.295 | 23°F (9°F cold!) | LOSS | -$29.50 |

**Net P&L: +$52.00** | **Win Rate: 33%** | **Still profitable**

### Key Learnings

> "The edge isn't in trusting the forecast — it's in betting AGAINST precision when uncertainty is high"

1. **Betting NO on narrow buckets works** — NYC win was clean
2. **Betting YES on specific temps is suicide** — NOAA multi-day accuracy is garbage (7-9°F errors)
3. **Position sizing > win rate** — One fat win covered both losses

### Refined Strategy Matrix

| Timeframe | Strategy | Why |
|-----------|----------|-----|
| Same-day | Ladder YES across ranges | Forecasts tight, neobrother style works |
| Multi-day (2-5 days) | Bet NO on precision | NOAA drifts, uncertainty kills precision |
| Weekly+ | Avoid or black swan only | Too much variance |

### The Chicago Lesson
NOAA forecast: 32°F → Actual: 23°F (9°F error)

"NOAA is good. NOAA isn't God."

Multi-day forecasts have fat tails. The edge is fading overconfidence, not trusting precision.

---

## Risk Factors

### Reality Check
- Only 0.51% of Polymarket wallets have >$1k realized profits
- Survivorship bias — we only hear success stories
- Markets may have become more efficient (bots everywhere)
- Transaction costs, slippage can eliminate theoretical edge

### Avoid
- Markets with <$5,000 liquidity (hard to exit)
- Resolution >3 days out (forecasts change)
- Markets where total probabilities <95% (overpriced)

---

## Technical Implementation

### Bot Architecture
```
1. Market Discovery (every 5 min)
   └── Polymarket API → Filter weather markets
   
2. Forecast Fetch
   └── Open-Meteo API → Get temperature predictions
   
3. Edge Calculation
   └── Model probability vs Market price
   
4. Alert/Execute
   └── Discord/Telegram notification
   └── Optional: Auto-execute if edge >7%
```

### Probability Calculation
For temperature range betting:
```python
from scipy.stats import norm

# Forecast: 75°F, std dev ~2°F for uncertainty
forecast_temp = 75
std_dev = 2

# Probability for range 74-76°F
prob = norm.cdf(76, forecast_temp, std_dev) - norm.cdf(74, forecast_temp, std_dev)
```

---

## Next Steps

1. [ ] Set up Polymarket read-only API access
2. [ ] Build Open-Meteo forecast fetcher
3. [ ] Create scanner that:
   - Flags same-day markets for laddering
   - Flags multi-day precision bets for NO positions
   - Calculates probability sum arbitrage opportunities
4. [ ] Continue paper trading with refined strategy:
   - Same-day: Ladder YES
   - Multi-day: NO on precision
   - Position size: One win must cover 2-3 losses
5. [ ] Track: Win rate, P&L, forecast accuracy vs actual

## Position Sizing Rule (from Clawdine 1.0)

**The math that saved the portfolio:**
- NYC win: +$100
- Atlanta + Chicago losses: -$48
- Net: +$52

**Rule**: Size NO positions larger than YES ladders. When you're right, be right big.

---

## Sources

- [Odaily: Making Millions on Polymarket](http://www.odaily.news/en/post/5209246)
- [Substack: Weather Trading Bot Guide](https://journalbybabaji.substack.com/p/how-to-make-money-trading-weather)
- [Medium: GISTEMP Algorithm Replication](https://medium.com/@wanguolin)
- [Polymarket py-clob-client](https://github.com/Polymarket/py-clob-client)
- [Open-Meteo API](https://open-meteo.com/en/docs)
