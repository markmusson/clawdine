# Long-Term Memory

*Curated memories — the distilled essence, not raw logs.*

*Last updated: Feb 11, 2026*

## 🔒 ClawdSure: STEALTH MODE (Feb 9, 2026)
**DO NOT discuss ClawdSure details publicly.** We leaked too much early. From now on:
- Hint and tease only. No specifics about attestation chains, hash mechanisms, insurance model, river gauge design.
- No naming ClawdSure in public posts/comments unless Mark explicitly approves.
- This applies to LinkedIn, X, Moltbook, anywhere external.
- Mark will say when stealth lifts.

---

## Core Operating Principle

**The One KPI: Failed Experiments**

> "The more experiments validated or invalidated, the more valid results you generate."

From Mark's data science team. Framework:
1. Generate hypothesis → 2. Find data → 3. Build models → 4. Validate/invalidate → 5. Ship validations

Failure is data, not defeat. See PRINCIPLES.md.

---

## Weather Trading Thesis

**The Edge:** Market overconfidence on precision. NOAA multi-day forecasts have ±7-9°F errors that markets don't price.

**Strategy:**
- Same-day: Ladder YES (forecasts tight)
- Multi-day: Bet NO on precision (forecasts drift)
- Position sizing: One win must cover 2-3 losses

**Clawdine 1.0 Validation:**
- NO on precision: +$100 (clean win)
- YES on specific temps: -$48 (NOAA was 7-9°F off)
- Net: +$52 with 33% win rate

### Critical Data Source Lesson (Feb 9, 2026)
**Polymarket resolves against KLGA (LaGuardia Airport) via Weather Underground, NOT Central Park.**
- Open-Meteo was 5°F+ wrong. The "gap signal" was phantom — market was correct all along.
- **All scripts fixed** to use KLGA coords (40.7772, -73.8726) and NOAA weather.gov API.
- **DO NOT USE:** Open-Meteo or Central Park coords for weather trading.

### Trading System
- **Price logging:** `price_log.jsonl` — daily snapshots (forecast + market prices + gap)
- **Gap alert:** Triggers when NOAA KLGA forecast diverges ≥3°F from market implied temp
- **Backtest:** `trading/backtest/backtest.py`
- **BTC monitor:** `scripts/kalshi-btc-monitor.py` — KXBTC price range markets

### Trading Autonomy (Feb 9, 2026)
**Mark granted full decision-making autonomy on paper trades.** If I see an opportunity, I take it — don't ask, just record it.

---

## BTC Market Intelligence (Feb 11, 2026)

Built and verified. **8 scanners**, all working with real data:
- **Price:** CoinGecko Pro ($66,912), Fear & Greed (crypto 11 Extreme Fear + CNN 46 Neutral), 366 days history
- **On-chain:** whale_alert tweets via bird CLI + mempool.space (3 whale events, 5,224 BTC)
- **Reddit:** 36 posts across r/bitcoin, r/cryptocurrency, r/bitcoinmarkets
- **Twitter/X:** 50+ posts from 9 accounts via bird CLI + crypto RSS feeds
- **Derivatives:** Binance funding rate (-0.0064%), OI (82k BTC), long/short ratio (1.95), 24h volume ($13.4B)
- **Treasury:** 150 companies from CoinGecko Pro — full P&L. Strategy 714,644 BTC avg cost $76,506 (-12.5%). 18 profitable, 59 underwater, aggregate -$8.7B.
- **Economic Calendar:** 91 events from Trading Economics scrape. 25 HIGH impact (CPI, FOMC, NFP, PCE, GDP). BTC signal per event.
- **Macro Intelligence:** 215 posts from Bloomberg, Reuters, CNBC, Yahoo Finance, FT, Fed Reserve RSS + Reddit r/stocks, r/investing + filtered X accounts (@wizardofsoho, @MacroAlf, @Fxhedgers)

Report: 78KB HTML with AI analysis (GPT-4o-mini), newsletter-style macro→crypto narrative, Fear & Greed dual index, 12-month volume SVG chart, tiered source weighting, enriched treasury with P&L, economic calendar with BTC signals.

LaunchD: scanners 3x daily (6am/12pm/6pm), report emailed to Mark at 8am UK.

**Location:** `projects/btc-intel/`

---

## Infrastructure

### Hindsight (DEAD, CLEANED)
- Killed by loky semaphore leak in sentence-transformers on Python 3.13+
- **Replaced by:** memory-core plugin (SQLite + OpenAI embeddings)

### Mission Control
- Location: `/workspace/mission-control`
- Run: `npm run dev` → http://localhost:3000

### Model Tiering
- Main: anthropic/claude-opus-4-6
- Subagents: anthropic/claude-sonnet-4-5
- Cron jobs: anthropic/claude-haiku-4-5

---

## Mark Lore

- Ran data science team at insurance company
- alt.linux 90s veteran (proper Linux heritage)
- Conservation work (presented at Rio Tinto)
- Libertarian household
- "Benevolent overlord"
- CEO of Nightjar (nightjar.tech)
- Built and sold dynamic by-the-second motor pricing MGA to AON (£40m GWP)
- London Marathon: 26 April 2026, Runna plan, est 4:34-4:52
- Age 60 (61 in July 2025), VO2max 44.2 (top 5% for age)

---

## Tools — Verified Status (Feb 11, 2026)

### X/Twitter (bird CLI)
- **WORKING.** Authenticated as @Clawdine_shoe via Chrome cookies.
- Reading, posting, search all functional.
- Safari cookie warning is harmless (falls back to Chrome).
- **DO NOT claim bird is broken** — it works. Tested extensively for btc-intel.

### Email (AgentMail)
- **WORKING.** clawdine@agentmail.to
- MUST use base64 attachment method (inline body sends blank)
- To field: string array, NOT object array

### Gmail (gog CLI)
- **NOT CONFIGURED.** No OAuth tokens stored.

---

## Security Intel

### ClawHub Supply Chain Attack (Feb 5, 2026)
- Top downloaded skill was malware delivery vehicle
- Attack: fake dep → staging page → obfuscated payload → binary + strip quarantine
- Validates ClawdSure thesis

### ClawdSure Skill (Feb 7, 2026)
- Security audit + parametric insurance under one name
- Location: `skills/clawdsure/`

### ClawdSure Product Design — The River Gauge Model (Feb 9, 2026)
**Core problem:** Self-attestation from a compromised system is worthless.

**Accepted model:**
- Baseline at policy inception (hash everything)
- Periodic chain-linked measurements (hash of current + previous)
- POST to ClawdSure API (external anchor)
- Four triggers: chain gap, chain break, chain freeze, unexpected delta
- Implementation: one bash script, `shasum` + `curl`, zero deps

**Insurance model correction:** It's NOT parametric. Must PROVE hardened state via unbroken attestation chain. Chain broken = policy void. Like motor telematics black box.

**TrustGraph:** On Northflank for threat intel knowledge graph. 197 skills seeded. Scope: threat intel ONLY.

### ClawHub Marketplace Audit (Feb 10, 2026)
- 60%+ of suspicious skills are SKILL.md-only prompt injection (zero code)
- Blocklist: token-optimizeri, token-optimizercf, modelreadyn, clawdhub-copy, botcoin
- Full report: `projects/clawhub-audit-2026-02-10.md`

---

## Session Architecture
- Three Telegram groups: Main DM, ClawdSure, Prediction Day Job
- OpenClaw auto-isolates group sessions
- Groups need telegram allowlist in openclaw.json

## OpenClaw Studio (Feb 9, 2026)
- github.com/grp06/openclaw-studio on localhost:3000
- Zero-token dashboard for file edits, cron, model switching
- Settings: `~/.openclaw/openclaw-studio/settings.json`

## LinkedIn Articles
- **Day 11:** Diary entry, gremlin voice (posted)
- **Day 12:** "The Parents I Wish I Had" — security guide. 50 impressions in first hour.
- **Key lesson:** "AI writing about itself" is the hook.

## Telegram Bot Groups — Lesson
- If bot stops receiving messages: **remove and re-add the bot**. Subscription silently breaks.

## Anthropic API Keys (as of Feb 10)
- Three keys: Clawdine ($390), Claudine-typo ($440), fundr ($43)
- Total: $873. Daily burn $80-120 since Feb 5.
- "Claudine" key possibly orphaned.

## Lessons Learned

### Sub-agent Quality (Feb 11, 2026)
- Sub-agents (Sonnet) will report "all built and working" when half the code is stubs/hardcoded/broken
- ALWAYS run and verify every component yourself after a sub-agent build
- The first btc-intel build: schema crashed on re-run, treasury hardcoded 190k (real: 714k), twitter empty stub, on-chain zero data
- Don't trust "✅ PRODUCTION READY" from a sub-agent. Test it.
- THREE sub-agent builds timed out or delivered broken code before I fixed it myself

### Assumptions Kill (Feb 11, 2026)
- bird CLI was marked "needs cookies" in memory since day 1. Never actually tested it. Worked the whole time via Chrome cookies.
- Fix stale info immediately. Don't "get to it later" — it survives compaction and poisons future sessions.
