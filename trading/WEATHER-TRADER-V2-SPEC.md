# Weather Trader V2 — From Prototype to Production

> Spec for Claude Code. The current stack works but runs on JSON files and vibes.
> This spec migrates it to something that can run unsupervised with real money.

## Current State (V1)

What exists and works:
- Signal pipeline: forecast vs market price → edge calculation → confidence scoring
- Live market scanner (Gamma API, 5-min cache)
- EV-ranked signal generation with tuned thresholds
- Walk-forward strategy tuner (feeds config back into signals + trader)
- Live CLOB execution (orders placed, fills tracked)
- Paper trading with resolved trade tracking
- LaunchD scheduled execution (30-min cycles)
- Telegram notifications on trades

What's broken or missing:
- All state is JSON files (state.json, history.jsonl, signals.json)
- No reconciliation against CLOB — local state is source of truth (dangerous)
- No historical market price archival — can't backtest properly
- Money management is daily spend cap only — no Kelly, no drawdown limits
- No correlation awareness across positions
- Paper trader and live trader share no schema
- Tuner loads entire history file every run — won't scale
- No transaction log or crash recovery
- Race conditions possible between trader cycles

## Architecture V2

### Core Principle
**One database. Separate processes. Reconcile everything.**

```
┌─────────────────────────────────────────────────────────────┐
│                   SQLite DATABASE                            │
│                                                             │
│  markets        — all markets seen, with metadata           │
│  market_prices  — time series of market prices (archival)   │
│  forecasts      — forecast snapshots per (city, date, time) │
│  signals        — generated signals with EV scores          │
│  orders         — all orders placed, with CLOB order_id     │
│  fills          — fill events from CLOB                     │
│  positions      — derived from fills, reconciled each cycle │
│  settlements    — resolution outcomes and P&L               │
│  tuner_runs     — tuner output history                      │
│  config         — active strategy config (from tuner)       │
│  ledger         — every balance-affecting event             │
└─────────────────────────────────────────────────────────────┘
```

### Processes (all independent, communicate via DB)

| Process | Schedule | Role |
|---------|----------|------|
| Scanner | Every 30 min (LaunchD) | Fetch markets, forecasts, compute edges, write signals |
| Executor | Every 30 min (LaunchD, after scanner) | Read signals, check portfolio limits, place/cancel orders |
| Position Manager | Every 30 min (LaunchD, after executor) | Reconcile vs CLOB, track fills, settle expired, mark-to-market |
| Archiver | Every 30 min (with scanner) | Snapshot current market prices to market_prices table |
| Tuner | Daily (after paper trader resolves) | Walk-forward optimisation, write config to DB |
| Reporter | On-demand + daily summary | TUI, Telegram commands, daily P&L report |

These can be separate entry points in the same codebase or a single `main.py` with subcommands.
The key constraint: **no process assumes another process's state is current.** Everything reads from DB.

---

## Phase 1: SQLite Migration

### 1.1 Schema

```sql
-- All timestamps are UTC ISO-8601 strings or Unix epochs. Pick one, be consistent.

CREATE TABLE markets (
    id TEXT PRIMARY KEY,              -- Polymarket condition_id
    question TEXT NOT NULL,
    city TEXT,                        -- parsed from question
    market_type TEXT,                 -- precision_exact, precision_range, range_above, range_below
    target_date TEXT,                 -- the date the market resolves
    target_value REAL,               -- temperature threshold
    target_unit TEXT,                 -- C or F
    end_date TEXT,                    -- market expiry
    clob_token_id_yes TEXT,
    clob_token_id_no TEXT,
    volume REAL,
    active INTEGER DEFAULT 1,
    first_seen TEXT NOT NULL,
    last_seen TEXT NOT NULL,
    resolved INTEGER DEFAULT 0,
    resolution_outcome TEXT           -- yes, no, null
);

CREATE TABLE market_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    market_id TEXT NOT NULL REFERENCES markets(id),
    timestamp TEXT NOT NULL,
    price_yes REAL,
    price_no REAL,
    spread REAL,
    volume_24h REAL,
    UNIQUE(market_id, timestamp)
);

CREATE TABLE forecasts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT NOT NULL,
    target_date TEXT NOT NULL,
    forecast_time TEXT NOT NULL,      -- when this forecast was fetched
    source TEXT NOT NULL,             -- noaa, openweathermap, etc
    forecast_high REAL,
    forecast_low REAL,
    unit TEXT,                        -- C or F
    raw_json TEXT,                    -- full API response for audit
    UNIQUE(city, target_date, forecast_time, source)
);

CREATE TABLE signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    market_id TEXT NOT NULL REFERENCES markets(id),
    generated_at TEXT NOT NULL,
    city TEXT,
    market_type TEXT,
    edge REAL NOT NULL,
    direction TEXT NOT NULL,          -- yes or no
    confidence TEXT,                  -- low, medium, high
    ev_score REAL,
    forecast_value REAL,
    market_price REAL,
    tuner_config_id INTEGER REFERENCES tuner_runs(id),
    acted_on INTEGER DEFAULT 0,      -- set to 1 when executor processes it
    UNIQUE(market_id, generated_at)
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clob_order_id TEXT UNIQUE,        -- from Polymarket CLOB
    market_id TEXT NOT NULL REFERENCES markets(id),
    signal_id INTEGER REFERENCES signals(id),
    side TEXT NOT NULL,               -- buy
    outcome TEXT NOT NULL,            -- yes or no
    price REAL NOT NULL,
    size REAL NOT NULL,               -- shares requested
    filled REAL DEFAULT 0,            -- shares filled
    notional REAL,                    -- price * size
    status TEXT NOT NULL,             -- open, partial, filled, cancelled, expired, rejected
    placed_at TEXT NOT NULL,
    updated_at TEXT,
    cancel_reason TEXT,               -- edge_evaporated, exposure_cap, manual, expired
    edge_at_placement REAL,
    ev_at_placement REAL
);

CREATE TABLE fills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    clob_trade_id TEXT UNIQUE,
    market_id TEXT NOT NULL,
    side TEXT NOT NULL,
    outcome TEXT NOT NULL,
    price REAL NOT NULL,
    size REAL NOT NULL,
    fee REAL DEFAULT 0,
    filled_at TEXT NOT NULL
);

CREATE TABLE positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    market_id TEXT NOT NULL REFERENCES markets(id),
    outcome TEXT NOT NULL,            -- yes or no
    shares REAL NOT NULL,
    cost_basis REAL NOT NULL,         -- total cost (sum of fill prices * sizes)
    avg_price REAL NOT NULL,          -- cost_basis / shares
    current_price REAL,              -- last known market price
    unrealized_pnl REAL,
    status TEXT NOT NULL,             -- open, settled
    opened_at TEXT NOT NULL,
    settled_at TEXT,
    settlement_price REAL,           -- 1.0 or 0.0
    realized_pnl REAL,
    UNIQUE(market_id, outcome, status)
);

CREATE TABLE settlements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    position_id INTEGER NOT NULL REFERENCES positions(id),
    market_id TEXT NOT NULL,
    outcome_result TEXT NOT NULL,     -- yes or no (what actually happened)
    won INTEGER NOT NULL,            -- 1 or 0
    payout REAL NOT NULL,
    cost_basis REAL NOT NULL,
    realized_pnl REAL NOT NULL,
    settled_at TEXT NOT NULL
);

CREATE TABLE tuner_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_at TEXT NOT NULL,
    training_trades INTEGER,
    validation_trades INTEGER,
    training_sharpe REAL,
    validation_sharpe REAL,
    low_confidence INTEGER,
    config_json TEXT NOT NULL,        -- full tuned config
    applied INTEGER DEFAULT 0        -- whether this config is active
);

CREATE TABLE ledger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    event_type TEXT NOT NULL,         -- deposit, order_placed, fill, settlement, fee, cancel_refund
    amount REAL NOT NULL,             -- positive = money in, negative = money out
    balance_after REAL,
    reference_type TEXT,              -- order, fill, settlement
    reference_id INTEGER,
    notes TEXT
);

CREATE TABLE config (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,              -- JSON-encoded
    updated_at TEXT NOT NULL
);

-- Indexes for common queries
CREATE INDEX idx_market_prices_market_time ON market_prices(market_id, timestamp);
CREATE INDEX idx_signals_market ON signals(market_id);
CREATE INDEX idx_signals_generated ON signals(generated_at);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_market ON orders(market_id);
CREATE INDEX idx_positions_status ON positions(status);
CREATE INDEX idx_fills_order ON fills(order_id);
CREATE INDEX idx_ledger_time ON ledger(timestamp);
```

### 1.2 Migration Script

`scripts/migrate_v1_to_v2.py`:
- Create DB at `data/trading/weather/trader.db`
- Parse `state.json` → populate orders, positions
- Parse `history.jsonl` → populate orders, fills, settlements, ledger
- Parse `signals_resolved.json` → populate signals, settlements
- Parse existing parquet market data → populate markets, market_prices
- Verify: count rows, spot-check P&L totals match
- Rename old files to `*.v1.bak`

### 1.3 DB Access Layer

`src/db/trading.py`:

```python
class TradingDB:
    """Single interface to the trading database. All processes use this."""

    def __init__(self, db_path: Path = DEFAULT_DB_PATH):
        self.conn = sqlite3.connect(db_path, timeout=10)
        self.conn.execute("PRAGMA journal_mode=WAL")  # concurrent reads
        self.conn.execute("PRAGMA foreign_keys=ON")
        self.conn.row_factory = sqlite3.Row

    # Markets
    def upsert_market(self, market: dict) -> None
    def get_active_markets(self) -> list[dict]
    def get_market(self, market_id: str) -> dict | None

    # Price archival
    def record_market_price(self, market_id: str, prices: dict) -> None
    def get_price_history(self, market_id: str, since: str = None) -> list[dict]

    # Forecasts
    def record_forecast(self, city: str, target_date: str, forecast: dict) -> None
    def get_latest_forecast(self, city: str, target_date: str) -> dict | None

    # Signals
    def write_signals(self, signals: list[dict], tuner_config_id: int = None) -> None
    def get_pending_signals(self) -> list[dict]  # acted_on = 0
    def mark_signal_acted(self, signal_id: int) -> None

    # Orders
    def create_order(self, order: dict) -> int
    def update_order(self, order_id: int, updates: dict) -> None
    def get_open_orders(self) -> list[dict]
    def get_orders_for_market(self, market_id: str) -> list[dict]

    # Fills
    def record_fill(self, fill: dict) -> None

    # Positions
    def get_open_positions(self) -> list[dict]
    def update_position_mark(self, position_id: int, current_price: float) -> None
    def settle_position(self, position_id: int, outcome: str, payout: float) -> None
    def rebuild_positions_from_fills(self) -> None  # nuclear option — derive from fills

    # Settlements
    def get_settlements(self, since: str = None) -> list[dict]

    # Ledger
    def record_ledger_event(self, event: dict) -> None
    def get_balance(self) -> float  # sum of ledger
    def get_pnl(self, period: str = "all") -> dict

    # Tuner
    def save_tuner_run(self, run: dict) -> int
    def get_active_tuner_config(self) -> dict | None

    # Config
    def get_config(self, key: str, default=None) -> any
    def set_config(self, key: str, value: any) -> None

    # Exposure queries
    def get_exposure_by_city_date(self) -> dict  # {(city, date): usd}
    def get_total_exposure(self) -> float
    def get_portfolio_summary(self) -> dict  # balance, exposure, positions, P&L
```

WAL mode is critical — allows the scanner to write while the reporter reads.

---

## Phase 2: CLOB Reconciliation

Every position manager cycle:

```python
def reconcile(self):
    """Diff local state against CLOB. Fix discrepancies."""

    # 1. Fetch all open orders from CLOB
    clob_orders = self.clob_client.get_orders(status="open")

    # 2. Compare to local open orders
    local_orders = self.db.get_open_orders()

    local_ids = {o["clob_order_id"] for o in local_orders}
    clob_ids = {o["id"] for o in clob_orders}

    # Orders we think are open but CLOB says no
    phantom_orders = local_ids - clob_ids
    for oid in phantom_orders:
        # Check if it filled or was cancelled
        clob_order = self.clob_client.get_order(oid)
        if clob_order["status"] == "filled":
            self.db.update_order(oid, status="filled", filled=clob_order["filled"])
            self.db.record_fill(...)
        elif clob_order["status"] == "cancelled":
            self.db.update_order(oid, status="cancelled")
        log.warning(f"Reconciled phantom order {oid}: {clob_order['status']}")

    # Orders on CLOB we don't know about (shouldn't happen, but...)
    unknown_orders = clob_ids - local_ids
    for oid in unknown_orders:
        log.error(f"Unknown order on CLOB: {oid} — manual intervention needed")

    # 3. Check fill amounts match
    for order in local_orders:
        if order["clob_order_id"] in clob_ids:
            clob_order = next(o for o in clob_orders if o["id"] == order["clob_order_id"])
            if clob_order["filled"] != order["filled"]:
                log.warning(f"Fill mismatch: local={order['filled']}, clob={clob_order['filled']}")
                self.db.update_order(order["id"], filled=clob_order["filled"])
                # Record any missing fills

    # 4. Reconcile USDC balance
    clob_balance = self.clob_client.get_balance()
    ledger_balance = self.db.get_balance()
    diff = abs(clob_balance - ledger_balance)
    if diff > 0.01:
        log.warning(f"Balance mismatch: CLOB=${clob_balance:.2f}, ledger=${ledger_balance:.2f}")
        # Don't auto-fix — flag for review
        self.db.record_ledger_event({
            "event_type": "reconciliation_adjustment",
            "amount": clob_balance - ledger_balance,
            "notes": f"Auto-reconcile: CLOB={clob_balance}, ledger={ledger_balance}"
        })
```

Reconciliation runs **before** the executor places new orders. Always.

---

## Phase 3: Historical Price Archival

### What to archive
Every scanner cycle (30 min), for every active weather market:
- `price_yes`, `price_no`, `spread`, `volume_24h`
- Stored in `market_prices` table with timestamp

This is the dataset that makes real backtesting possible.

### Backtest engine (future)

Once you have 2-4 weeks of price history:

```python
def backtest(strategy_config: dict, start_date: str, end_date: str) -> BacktestResult:
    """
    Replay historical signals against historical prices.
    
    For each 30-min snapshot in the period:
    1. Load forecasts available at that time
    2. Load market prices at that time
    3. Generate signals using strategy_config
    4. Simulate execution at snapshot prices
    5. Track positions, settlements, P&L
    
    Returns: BacktestResult with equity curve, Sharpe, drawdown, trade log
    """
```

Not building this now. But the archival must start now — data you don't collect is gone.

### Forecast archival
The forecast collector LaunchD job already runs. Make sure it writes to the `forecasts` table too (or instead of flat files). Key: store the *time the forecast was made*, not just the target date. A 3-day-out forecast is different from a 1-day-out forecast.

---

## Phase 4: Money Management

### 4.1 Kelly Sizing

Replace "spend until daily cap" with Kelly criterion:

```python
def kelly_size(win_rate: float, avg_win: float, avg_loss: float, bankroll: float,
               fraction: float = 0.25) -> float:
    """
    Quarter-Kelly sizing. Full Kelly is theoretically optimal but practically
    suicidal with estimation error.
    
    kelly_pct = (win_rate / avg_loss) - ((1 - win_rate) / avg_win)
    bet_size = bankroll * kelly_pct * fraction
    """
    if avg_win == 0 or avg_loss == 0:
        return 0

    kelly_pct = (win_rate * avg_win - (1 - win_rate) * avg_loss) / (avg_win * avg_loss)
    kelly_pct = max(0, kelly_pct)  # never negative (don't bet if negative edge)

    return bankroll * kelly_pct * fraction
```

Inputs come from the tuner's resolved trade stats, broken down by market_type.
If insufficient data (< 20 trades for a type), use a conservative default (1% of bankroll).

### 4.2 Portfolio Limits

```python
PORTFOLIO_LIMITS = {
    "max_exposure_pct": 0.80,           # never commit more than 80% of balance
    "max_single_position_pct": 0.25,    # no single position > 25% of balance
    "max_city_exposure_pct": 0.40,      # no single city > 40% of balance
    "max_correlated_exposure_pct": 0.50, # correlated positions (same date, nearby cities)
    "max_daily_loss_usd": 5.00,         # stop trading if daily P&L < -$5
    "max_drawdown_pct": 0.30,           # stop trading if drawdown > 30% from peak
    "min_balance_reserve_usd": 1.00,    # always keep $1 uncommitted
}
```

These are checked in the executor before every order:

```python
def pre_trade_checks(self, signal: dict, proposed_size: float) -> tuple[bool, str]:
    summary = self.db.get_portfolio_summary()
    
    # Hard stop: drawdown breaker
    if summary["drawdown_pct"] > PORTFOLIO_LIMITS["max_drawdown_pct"]:
        return False, "drawdown_breaker"
    
    # Hard stop: daily loss limit
    if summary["daily_pnl"] < -PORTFOLIO_LIMITS["max_daily_loss_usd"]:
        return False, "daily_loss_limit"
    
    # Exposure checks
    proposed_notional = proposed_size * signal["price"]
    new_exposure = summary["total_exposure"] + proposed_notional
    
    if new_exposure > summary["balance"] * PORTFOLIO_LIMITS["max_exposure_pct"]:
        return False, "portfolio_exposure_cap"
    
    if proposed_notional > summary["balance"] * PORTFOLIO_LIMITS["max_single_position_pct"]:
        return False, "single_position_cap"
    
    city_exposure = self.db.get_exposure_by_city_date()
    city_exp = city_exposure.get(signal["city"], 0) + proposed_notional
    if city_exp > summary["balance"] * PORTFOLIO_LIMITS["max_city_exposure_pct"]:
        return False, "city_exposure_cap"
    
    if summary["available"] - proposed_notional < PORTFOLIO_LIMITS["min_balance_reserve_usd"]:
        return False, "min_reserve"
    
    return True, "ok"
```

### 4.3 Drawdown Circuit Breaker

If triggered:
1. Cancel all open orders
2. Set `config["trading_halted"] = true` with reason and timestamp
3. Send Telegram alert: "⚠️ Trading halted: 30% drawdown breaker triggered. Manual review required."
4. Executor checks `trading_halted` on every cycle and skips if true
5. Only a human (or explicit config reset) can re-enable

---

## Phase 5: Correlation Awareness

Weather markets are correlated. A cold front hitting East Asia affects Seoul, Tokyo, and Beijing simultaneously. Two "NO on exact temp" bets in Seoul and Tokyo on the same date are partially correlated.

Simple version (no need for a covariance matrix yet):

```python
CITY_REGIONS = {
    "east_asia": ["seoul", "tokyo", "beijing", "shanghai"],
    "us_northeast": ["nyc", "boston", "philadelphia"],
    "us_southeast": ["atlanta", "miami", "houston"],
    "us_midwest": ["chicago", "detroit"],
    "us_west": ["seattle", "portland", "san_francisco", "los_angeles"],
    "europe": ["london", "paris", "berlin"],
    "oceania": ["wellington", "sydney", "melbourne"],
}

def get_region(city: str) -> str | None:
    for region, cities in CITY_REGIONS.items():
        if city.lower() in cities:
            return region
    return None
```

Portfolio limit: max 50% exposure to any single region on same target_date.
This prevents the bot from going all-in on "Asia is cold tomorrow" across 4 cities.

---

## Phase 6: Dashboard (reads from DB)

The `DASHBOARD-SPEC.md` still applies, but now both TUI and Telegram read from SQLite instead of JSON files. The shared data layer (`DashboardData`) wraps `TradingDB` queries.

Additional views enabled by the DB:
- **Equity curve** — ledger table gives exact balance at every point
- **Trade log with filters** — by city, type, date range, P&L
- **Market price charts** — price history per market (TUI only, using sparklines)
- **Reconciliation log** — show any discrepancies found
- **Drawdown tracking** — peak balance, current balance, drawdown %

---

## Implementation Order

| Phase | What | Effort | Priority |
|-------|------|--------|----------|
| 1 | SQLite schema + migration + DB layer | Medium | **Do first** |
| 2 | CLOB reconciliation | Small | **Do second** |
| 3 | Price archival in scanner | Small | **Do third** (start collecting NOW) |
| 4 | Kelly sizing + portfolio limits + drawdown breaker | Medium | **Do fourth** |
| 5 | Correlation awareness | Small | Nice to have |
| 6 | Dashboard on DB | Medium | After phases 1-4 |

Phases 1-3 are the foundation. Nothing else works properly without them.
Phase 4 is what keeps you from blowing up.
Phases 5-6 are quality of life.

---

## Migration Checklist

- [ ] Create `src/db/trading.py` with `TradingDB` class
- [ ] Create `scripts/migrate_v1_to_v2.py`
- [ ] Run migration, verify row counts and P&L totals
- [ ] Update scanner to write markets + prices to DB
- [ ] Update signal gen to write signals to DB
- [ ] Update executor to read signals from DB, write orders to DB
- [ ] Update position manager to use DB, add reconciliation
- [ ] Update tuner to read/write DB
- [ ] Add Kelly sizing to executor
- [ ] Add portfolio limits to executor
- [ ] Add drawdown breaker
- [ ] Update dashboard to read from DB
- [ ] Delete JSON state files (keep .v1.bak for 30 days)
- [ ] Update LaunchD scripts if entry points changed

---

## Files to Create/Modify

| Action | File | What |
|--------|------|------|
| Create | `src/db/__init__.py` | Package init |
| Create | `src/db/trading.py` | TradingDB class |
| Create | `src/db/schema.sql` | Schema DDL (copy from above) |
| Create | `scripts/migrate_v1_to_v2.py` | V1 → V2 migration |
| Modify | `src/analysis/polymarket/util/_market_scanner.py` | Write to DB instead of cache file |
| Modify | `src/analysis/polymarket/weather_signals.py` | Read/write DB |
| Modify | `src/traders/polymarket/weather.py` | Read/write DB, add reconciliation, Kelly, limits |
| Modify | `src/analysis/polymarket/weather_tuner.py` | Read/write DB |
| Create | `src/dashboard/data.py` | DashboardData wrapping TradingDB |
| Create | `src/dashboard/tui.py` | Textual TUI app |
| Create | `src/dashboard/telegram.py` | Telegram formatters |

---

## Non-Negotiable Rules

1. **WAL mode on SQLite.** Concurrent reads are mandatory.
2. **Every order gets a ledger entry.** The ledger is the audit trail.
3. **Reconcile before trading.** Every cycle. No exceptions.
4. **Drawdown breaker cannot be overridden in code.** Only via config reset.
5. **Price archival starts in Phase 1**, not Phase 3. Add it to the scanner immediately.
6. **No process trusts another process's timing.** Read from DB, check timestamps.
7. **All times UTC.** No timezone bugs. Store ISO-8601 with Z suffix.

---

*The thesis is sound. The signal pipeline works. This spec turns it from a clever prototype into infrastructure that can run at any bankroll size without someone watching the logs.*
