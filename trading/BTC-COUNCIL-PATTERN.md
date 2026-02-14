# BTC Daily Report — Council Pattern

> Overlay the multi-agent adversarial review pattern onto the daily BTC report.
> Sourced from Mark's research pipeline architecture diagram.

## Signal Sources (swap-in for BTC context)

### Existing Scanners (6)
1. Price feeds (spot, futures, funding rates)
2. On-chain (whale flows, exchange balances, MVRV)
3. Social (sentiment, trending topics, fear/greed)
4. Derivatives (open interest, liquidations, options flow)
5. Treasury (corporate holdings, ETF flows)
6. Macro (DXY, rates, correlation)

### New: Podcast Intelligence
Transcribe latest episodes via Whisper API, extract key datapoints and analyst positions.

| Priority | Show | Spotify ID | Notes |
|----------|------|------------|-------|
| ⭐ Top | TBD (fair value analyst) | 4FeivSs55CRUd0qch0IiKz | Fair value calculation, key datapoints |
| ⭐ Top | TBD | 41TNnXSv5ExcQSzEGLlGhy | Good datapoints |
| ⭐ Top | Bitcoin Magazine Podcast | 1IxBiqXrUwWUgwiQwKWwxk | Major BTC news/analysis |
| 🟡 Med | When Shift Happens | 7JqCB5tnRky7XS7NRFWQJt | Crypto builders, interesting guests |
| 🟡 Med | TBD | 0QnvAOKX8ZUzdwMl89h3gU | Medium priority |

**Need Mark to confirm names for shows #1, #2, #5.**

## Pipeline Architecture

```
Signal Collection (10+ sources)
  [6 scanners] + [podcast transcripts] + [X/Twitter] + [news feeds]
        │
        ▼
  Compact to Top 200 Signals by Confidence
        │
        ▼
  Phase 1: Draft — LeadAnalyst (Opus)
  Scored horizons + initial recommendations
        │
        ▼
  Phase 2: Parallel Review (Promise.all)
  ┌─────────────┬──────────────┬────────────────┬───────────────┐
  │ BullCase     │ BearCase     │ RiskAnalyst    │ ArbHunter     │
  │ Momentum,    │ Distribution,│ Volatility,    │ Mispricings,  │
  │ accumulation,│ overleveraged│ correlation,   │ cross-exchange,│
  │ narrative    │ macro heads  │ liquidation    │ Polymarket     │
  └─────────────┴──────────────┴────────────────┴───────────────┘
        │
        ▼
  Phase 3: Consensus — CouncilModerator (Opus)
  Reconcile disagreements, final recommendation set
        │
        ▼
  Phase 4: Ranking and Delivery
  Priority Score = impact * w1 + confidence * w2 + (100 - effort) * w3
        │
        ├──→ Persist council trace to DB
        └──→ Deliver digest to Telegram / Email
```

## Podcast Ingestion Pipeline

1. Check for new episodes (Spotify RSS or API)
2. Download audio
3. Transcribe via Whisper API
4. Extract: key claims, price targets, fair value estimates, risk flags
5. Score confidence based on analyst track record (manual initially)
6. Feed extracted signals into council pipeline

## Implementation Notes

- Podcast transcription adds latency — run as background job, not in critical path
- Cache transcripts — don't re-transcribe same episode
- The fair value analyst (#1) is the highest signal — his datapoints should be weighted higher
- Council trace in DB enables backtesting the council's recommendations against outcomes
- Same pattern reusable for Roundy (swap sources to CRM, meetings, pipeline data)

---

*This is the architecture. Claude Code builds it. I verify it.*
