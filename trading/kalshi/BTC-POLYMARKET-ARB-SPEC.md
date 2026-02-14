# BTC Polymarket Arbitrage — Reference Architecture

## Reference Implementation
`gabagool222/15min-btc-polymarket-trading-bot` — DeepWiki: https://deepwiki.com/gabagool222/15min-btc-polymarket-trading-bot

## Strategy: Pure Arbitrage (not directional)

Buy BOTH UP and DOWN when `price_up + price_down < $1.00`. One side always pays $1.00. Pocket the difference. Zero prediction needed.

```
UP:   $0.48
DOWN: $0.51
Cost: $0.99
Pay:  $1.00 guaranteed
Profit: $0.01/share (1.01% ROI per 15-min window)
```

Only execute when depth-aware cost ≤ TARGET_PAIR_COST (default $0.991).

## Why This Instead of Directional

Our Kalshi paper trading: 219 trades, 21% win rate, -$5.86 P&L. We're bad at predicting BTC direction in 15-min windows. Nobody is. But mispricing between UP and DOWN is mechanical — no prediction required.

## Architecture

### Market Data (two modes)
- **WebSocket** `wss://ws-subscriptions-clob.polymarket.com` — real-time L2 book, price deltas. Low latency.
- **HTTP polling** `https://clob.polymarket.com` — concurrent GET for UP/DOWN books. Fallback mode.

### Market Discovery (3-tier fallback)
1. Computed slugs (fastest)
2. Gamma API `https://gamma-api.polymarket.com` (reliable)
3. Page scraping `https://polymarket.com/crypto/15M` (last resort)

### Execution
- FOK (Fill-Or-Kill) orders — both sides fill completely or neither does
- Paired verification — poll `get_order()` to confirm both legs
- Emergency unwind — SELL at best_bid FAK if only one leg fills
- Auto-rollover to next 15-min market at close

## Risk Controls

| Control | Detail |
|---------|--------|
| Balance margin | 120% of investment required before execution |
| FOK orders | Prevents partial fills / one-leg exposure |
| Paired verification | Confirms both legs filled |
| Emergency unwind | Best-effort flatten on partial fill |
| Cooldown | 10s between executions (configurable) |
| Auto-rollover | Discovers next market at close |

## Tech Stack

Python (matches our existing scripts):
- `py-clob-client` — official Polymarket Python SDK
- `websockets` 12.0 — real-time book data
- `httpx` 0.27.0 — async HTTP for discovery + book fetching
- `web3.py` — on-chain balance verification (Polygon, chain 137)
- `python-dotenv` — config

## Config

```
PRIVATE_KEY=         # wallet signing key
POLYMARKET_FUNDER=   # proxy wallet (Gnosis Safe)
API_KEY=             # derived from create_api_keys.py
API_SECRET=
API_PASSPHRASE=
CLOB_HTTP_URL=https://clob.polymarket.com/
CLOB_WS_URL=wss://ws-subscriptions-clob.polymarket.com/ws
TARGET_PAIR_COST=0.991
ORDER_SIZE=10        # USDC per side
ORDER_TYPE=FOK
COOLDOWN_SECONDS=10
DRY_RUN=true         # paper trading mode
SIM_BALANCE=500      # simulated starting balance
USE_WSS=true         # WebSocket mode
```

## Operating Modes

| Mode | DRY_RUN | What happens |
|------|---------|-------------|
| Simulation | true | Logs opportunities, tracks virtual P&L, no real orders |
| Live | false | Real orders, real USDC, FOK execution |

## Deployment

Same geo-restriction problem as weather trading. Execution needs US IP.

```
Mac (London)                    US VPS (NYC)
├── Monitor Kalshi              ├── py-clob-client (Polymarket)
├── Opportunity detection       ├── Order execution
├── Reporting                   ├── WebSocket book monitoring
└── Clawdine watches            └── Arb scanner + executor
```

## Relationship to Kalshi BTC

Currently paper trading BTC on Kalshi (KXBTC range markets). Two parallel plays:
- **Kalshi**: directional range bets (current, losing)
- **Polymarket**: pure arb on 15-min UP/DOWN (new, market-neutral)

Different strategies, different platforms, same underlying. Polymarket arb is lower risk, lower reward per trade, but consistent if the mispricing exists.

## What Claude Code Needs to Build

1. Fork/adapt gabagool222's bot for our config
2. Paper trading validation (DRY_RUN=true) to verify opportunities exist
3. Signal relay from Mac if needed (or run scanner entirely on US VPS)
4. Integration with our existing Kalshi monitoring for combined reporting
5. Deployment to US VPS alongside weather trader execution service

**Clawdine does NOT write this code.**
