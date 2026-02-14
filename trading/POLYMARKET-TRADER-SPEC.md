# Polymarket Trader — Reference Architecture

## Reference Implementation
`ivorn42/polymarket-copy-trade-bot` — DeepWiki: https://deepwiki.com/ivorn42/polymarket-copy-trade-bot

## CLOB Integration

Two channels:
- **HTTP REST** `https://clob.polymarket.com/` — orders, balances, positions
- **WebSocket** `wss://ws-subscriptions-clob.polymarket.com/ws` — real-time trade events, order book

SDK: `@polymarket/clob-client` v4.14.0 (official Polymarket SDK)

## Auth

Wallet-based, two-step:
1. Create `ethers.Wallet` from `PRIVATE_KEY`
2. Init `ClobClient` without creds → `createApiKey()` or `deriveApiKey()` fallback
3. Re-init `ClobClient` with creds → ready for authenticated ops

Config:
- `PRIVATE_KEY` — wallet signing key
- `PROXY_WALLET` — Gnosis Safe proxy wallet address (funder)
- `CLOB_HTTP_URL` — REST endpoint
- `CLOB_WS_URL` — WebSocket endpoint
- Chain ID: 137 (Polygon mainnet)
- Signature type: `POLY_GNOSIS_SAFE`

## Our Architecture

```
┌─────────────────────────────────┐     ┌──────────────────────────┐
│     Mac (London, UK)            │     │   US Server (NYC VPS)    │
│                                 │     │                          │
│  NOAA/Weather data collection   │     │  CLOB client (auth)      │
│  Signal generation              │ ──▶ │  Order execution         │
│  Gap detection                  │     │  Balance/position mgmt   │
│  Paper trading validation       │     │  WebSocket monitoring    │
│                                 │     │                          │
│  Clawdine monitors & reports    │     │  Runs autonomously       │
└─────────────────────────────────┘     └──────────────────────────┘
         signals via API                    executes via CLOB
```

**Why split:** Polymarket CLOB is geo-restricted. Can't trade from UK IP. Signal generation doesn't need US access. Execution does.

## Services (adapted from copy-trade-bot)

### Signal Service (Mac side)
- Replaces "Trade Monitor" from copy-trade-bot
- Watches NOAA forecasts, calculates gaps vs market implied prices
- When gap exceeds threshold → emits signal to US server
- Existing scripts: `weather_tracker.py`, `signal_gen.py`, `gap_alert.py`

### Execution Service (US server side)
- Replaces "Trade Executor" from copy-trade-bot
- Receives signals, validates (balance check, position check)
- Posts orders to CLOB via HTTP REST
- Monitors fills via WebSocket
- Risk controls: max position size, max daily loss, market liquidity check

## CLOB Operations

| Operation | Method | Purpose |
|-----------|--------|---------|
| Balance | GET /balances | USDC available |
| Positions | GET /positions | Current holdings |
| Place order | POST /order | Buy/sell |
| Order status | GET /orders | Verify fills |
| Market data | WebSocket | Real-time prices, book |

## Risk Controls (from reference)

- Balance check before every order
- Position size limits
- No duplicate orders on same market
- Liquidity check (thin markets = skip)

## Dependencies

- `@polymarket/clob-client` ^4.14.0
- `@polymarket/order-utils` (transitive)
- `ethers` ^5.7.2
- Node.js runtime on US server

## Geo-Restriction Solution

Options (Mark decides):
1. **VPN** — route scripts through US VPN. Risky (drops = stuck positions)
2. **US VPS** — DigitalOcean/AWS in NYC region, ~$5-10/mo. Clean separation. ← recommended
3. **Pivot** — Kalshi only (different restrictions)

## Current State

- Signal generation: built, running on Mac via launchd
- Paper trading: running, validating signals
- CLOB integration: not built yet
- US server: not provisioned
- Live trading: blocked on geo-restriction solution

## What Claude Code Needs to Build

1. Execution service for US server (Node.js, CLOB client, signal receiver)
2. Signal relay API (Mac → US server, authenticated)
3. Position management (track open positions, settlements)
4. Risk controls layer
5. Deployment scripts for VPS

**Clawdine does NOT write this code.** Claude Code builds it. I spec and monitor.
