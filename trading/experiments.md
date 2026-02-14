# Experiment Tracker

## Summary

| ID | Hypothesis | Status | Result |
|----|-----------|--------|--------|
| EXP-001 | NO on multi-day precision beats market | 🔬 Active | Pending |
| EXP-002 | Forecast error increases with horizon | 🔬 Active | Pending |

---

## EXP-001: NO on Multi-Day Precision

**Hypothesis:** Betting NO on specific temperature ranges for multi-day forecasts is profitable because NOAA error (±5-9°F) exceeds market-implied confidence.

**Data Sources:**
- Open-Meteo API (GFS/HRRR forecasts)
- Polymarket Gamma API (market prices)
- Weather Underground (resolution data)

**Test:**
- Paper trade NO positions on multi-day (24h+) precision bets
- Track: Entry price, forecast, actual, P&L

**Success Criteria:**
- Win rate > 60% on NO positions
- Positive P&L over 1 week (7+ trades)

**Timeline:** Feb 7-14, 2026

**Status:** 🔬 Active

**Trades:**
| Date | Market | Position | Entry | Forecast | Actual | Result | P&L |
|------|--------|----------|-------|----------|--------|--------|-----|
| Feb 7 | NYC Feb 8 18-19°F | NO | $0.565 | 14.8°F | TBD | TBD | TBD |

**Learnings:** *(To be updated)*

---

## EXP-002: Forecast Accuracy by Horizon

**Hypothesis:** Forecast error increases predictably with time horizon:
- Same-day: ±2°F
- 1-day: ±4°F
- 2-3 day: ±6-8°F

**Data Sources:**
- Open-Meteo historical forecasts
- Weather Underground actuals
- Build error distribution database

**Test:**
- Track forecast vs actual for 5 cities over 2 weeks
- Compute error distribution by horizon

**Success Criteria:**
- Quantify error distributions
- Identify which horizons have tradeable edge

**Timeline:** Feb 7-21, 2026

**Status:** 🔬 Active

**Data:**
| Date | City | Horizon | Forecast | Actual | Error |
|------|------|---------|----------|--------|-------|
| Feb 7 | NYC | +1 day | 14.8°F | TBD | TBD |
| Feb 7 | Atlanta | +1 day | 56.3°F | TBD | TBD |

**Learnings:** *(To be updated)*

---

## Experiment Backlog

- EXP-003: Same-day laddering profitability
- EXP-004: Probability sum arbitrage frequency
- EXP-005: Retail fade win rate on precipitation markets
- EXP-006: Optimal position sizing for NO vs YES strategies

---

## Invalidated Experiments

*(Move experiments here when invalidated — they're still valuable data)*

| ID | Hypothesis | Why Invalidated | Key Learning |
|----|-----------|-----------------|--------------|
| | | | |

---

*Updated: Feb 7, 2026*
