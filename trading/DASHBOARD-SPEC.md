# Weather Trading Dashboard Spec

Two interfaces, one data layer. Telegram for mobile monitoring, TUI for full control at the terminal.

## Shared Data Layer

Both interfaces read the same files — no separate backend needed.

| Data | Source |
|------|--------|
| Open orders | `data/trading/weather/state.json` → `open_orders[]` |
| Positions | `data/trading/weather/state.json` → `positions[]` |
| Trade history | `data/trading/weather/history.jsonl` |
| Live signals | `output/weather-signals/signals.json` |
| Tuner config | `output/weather-tuner/tuned_config.json` |
| Tuner summary | `output/weather-tuner/summary.md` |
| Balance | CLOB API `get_balance` or parse from last trader log |
| P&L | Computed from history.jsonl (sum of `pnl_net` on settled trades) |

Helper module: `src/dashboard/data.py` — single source of truth. Both TUI and Telegram import it.

```python
class DashboardData:
    def get_balance() -> dict          # {available, locked, total}
    def get_positions() -> list[dict]  # open positions with current value
    def get_open_orders() -> list[dict]
    def get_signals() -> list[dict]    # ranked by ev_score
    def get_pnl() -> dict              # {total, today, week, by_city, by_type}
    def get_tuner_status() -> dict     # {last_run, low_confidence, config_summary}
    def get_exposure() -> dict         # {total_usd, pct_of_balance, by_city}
```

---

## TUI — Textual App

Library: `textual` (Python, pip install textual)

### Layout

```
┌─ Weather Trader ──────────────────────────────────────────────┐
│ Balance: $8.01  │  Exposure: $7.95 (99%)  │  P&L: -$4.99     │
├───────────────────────────────────────────────────────────────┤
│ [Positions]  [Orders]  [Signals]  [History]  [Config]         │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  OPEN ORDERS                                                  │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ Seoul 7°C Feb 13  │ BUY NO │ 78¢ │ 0/10 │ $7.95 │ GTC  │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                               │
│  SIGNALS (ranked by EV)                                       │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ City     │ Market          │ Edge  │ EV    │ Conf │ Type │ │
│  │ London   │ 12°C Feb 14     │ +0.22 │ 0.31  │ high │ p_ex │ │
│  │ NYC      │ >5°C Feb 13     │ +0.18 │ 0.24  │ med  │ r_ab │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                               │
├───────────────────────────────────────────────────────────────┤
│ Tuner: 24 trades │ Sharpe: 39.3 │ Last run: 2h ago │ Active  │
│ Log: [last 3 lines of trader log]                             │
└───────────────────────────────────────────────────────────────┘
```

### Features
- **Auto-refresh**: Poll files every 30s (configurable)
- **Tab navigation**: Positions / Orders / Signals / History / Config
- **History tab**: Scrollable table of all trades from history.jsonl, sortable by date/city/pnl
- **Config tab**: Shows tuned_config.json formatted, city multipliers, exclusions, edge thresholds
- **Keybindings**: `q` quit, `r` force refresh, `1-5` switch tabs, `/` filter
- **Color coding**: Green for profitable, red for losing, yellow for pending
- **Status bar**: Tuner status, last trader cycle time, VPN status (can curl polymarket?)

### Entry point
```bash
uv run main.py dashboard
# or
uv run python -m src.dashboard.tui
```

---

## Telegram Commands

Extend the existing trader Telegram notifications. These are **read-only queries** the user sends to the bot, not OpenClaw commands.

Implementation: Either as Telegram bot command handlers in the trading codebase, or as scripts Clawdine can invoke.

### Commands

| Command | Response |
|---------|----------|
| `/balance` | Balance, exposure, available. One line. |
| `/positions` | Table of open positions with current value and unrealized P&L |
| `/orders` | Open orders: market, side, price, filled/total, age |
| `/signals` | Top 5 signals by EV score. City, market, edge, confidence. |
| `/pnl` | P&L summary: total, today, this week, by city, by market type |
| `/config` | Current tuned config: edge thresholds, city multipliers, exclusions |
| `/status` | One-shot overview: balance + positions + orders + tuner status |

### Format
Keep it tight. Telegram messages, not essays.

```
📊 Status
Balance: $8.01 | Exposure: $7.95 (99%)
P&L: -$4.99 all-time

📋 Orders (1)
• Seoul 7°C Feb 13 — BUY NO @ 78¢ — 0/10 filled — $7.95

📡 Signals (3)
1. London 12°C Feb 14 — edge +0.22 — EV 0.31 — high
2. NYC >5°C Feb 13 — edge +0.18 — EV 0.24 — med
3. Tokyo 8°C Feb 14 — edge +0.15 — EV 0.19 — med

⚙️ Tuner: active | 24 trades | Sharpe 39.3
```

### Implementation options
1. **Standalone bot handlers** — register commands with the trading bot's Telegram integration
2. **Script-based** — shell scripts that read the data files and format output, callable by Clawdine via OpenClaw or by cron

Option 2 is simpler and doesn't need a long-running bot process. Scripts in `scripts/dashboard/` that output formatted text. Clawdine or cron can run them and send via Telegram.

---

## Not In Scope (yet)
- Write operations from Telegram (cancel order, place trade) — too risky without confirmation flow
- Web UI
- Historical charts (TUI is text-first)
- Multi-strategy (BTC arb gets its own dashboard later)

## Dependencies
- `textual` (TUI)
- Existing: `src/traders/polymarket/weather.py`, `src/analysis/polymarket/weather_signals.py`

## File Structure
```
src/
  dashboard/
    __init__.py
    data.py          # Shared data layer
    tui.py           # Textual app
    telegram.py      # Telegram formatters
scripts/
  dashboard/
    status.sh        # Quick status one-liner
    positions.sh     # Position details
```
