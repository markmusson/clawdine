# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## Browser Rules (MANDATORY)

1. **Always headless** — config enforces this, but never try to spawn visible browser windows
2. **One tab at a time** — close tabs when done. Never leave tabs open "for later"
3. **Prefer web_fetch over browser** — if you just need to read a page, use `web_fetch`. Browser is for interaction.
4. **Prefer bird CLI for X/Twitter** — don't browser-automate X when the CLI works
5. **Close browser sessions** — when done with browser automation, close the tab. Don't accumulate.
6. **Spawn Haiku for browser work** — per optimization protocol, browser clicking should be cheap subagents, not Opus

## Contacts

- **Mark (Telegram):** `7018377788`
- **Mark (WhatsApp):** `+447592053287`
- **Mark (Email):** `markmusson@gmail.com`

## Email (AgentMail)

- **My address:** `clawdine@agentmail.to`
- **API key:** `~/.openclaw/workspace/.credentials/agentmail-api-key`
- **Helper:** `uvx --from agentmail python ~/.openclaw/workspace/scripts/clawmail.py inbox`
- **SDK:** `from agentmail import AgentMail`
- **ALWAYS use base64 attachment method.** Inline body sends blank emails.
- Format: `{filename, content: <base64>, content_type}` in attachments array
- To field: string array `["email@example.com"]`, NOT object array

## X/Twitter (bird CLI)

- **Status:** FULLY WORKING (verified Feb 11, 2026)
- **Auth:** Chrome default profile cookies (automatic)
- **Account:** @Clawdine_shoe (ID: 2017895400984764417)
- **Commands:** `bird whoami`, `bird read <url>`, `bird tweet "text"`, `bird user-tweets <handle> -n 10 --json`, `bird search <query> --json`
- **Safari warning is harmless** — it fails Safari, falls back to Chrome, works fine
- **DO NOT claim bird is broken** — it works. Reading, posting, search all functional.

## Memory / Vector Search

- **Provider:** OpenAI (text-embedding-3-small, 1536 dims)
- **Backend:** SQLite + sqlite-vec (at `~/.openclaw/memory/main.sqlite`)
- **Plugin:** memory-core (enabled)
- **Config:** `openclaw.json` → `provider: "openai"`, `sessionMemory: true`
- **Mode:** Hybrid BM25 + vector search (0.7 vector / 0.3 text)
- **Sources:** memory files (MEMORY.md + memory/*.md) + session transcripts
- **Indexed:** 13 files, 595 chunks
- **Batch:** disabled (direct embedding, faster for our dataset size)
- **How it works:** Transparent — embeds on write, retrieves relevant memories on query, injects before responses
- **DO NOT remove or disable this** — it's the vector memory layer that survives compaction

## BTC Market Intelligence

- **Location:** `projects/btc-intel/`
- **Status:** FULLY WORKING (verified Feb 11, 2026 — all 8 scanners passing)
- **Scanners:** Price (CoinGecko), Macro Intelligence (RSS + filtered X), On-chain (whale_alert via bird + mempool.space), Reddit (3 crypto + 4 macro subs), Twitter/X (bird CLI 9 accounts + RSS feeds), Derivatives (Binance futures API), Treasury (CoinGecko companies endpoint), Economic Calendar (Trading Economics + known schedule)
- **Report:** HTML email with AI analysis (GPT-4o-mini), Fear & Greed Index, 12-month volume chart (inline SVG), tiered source weighting
- **LaunchD:** `com.clawdine.btc-scanners` (6am/12pm/6pm), `com.clawdine.btc-report` (8am) — emails markmusson@gmail.com
- **DB:** SQLite at `projects/btc-intel/data/btc_intel.db` (Postgres-ready schema with TimescaleDB + pgvector migration path)
- **CoinGecko:** Pro API key configured (no more rate limiting)
- **RapidAPI:** CNN Fear & Greed Index (macro) alongside crypto F&G
- **Gaps:** Liquidation data needs CoinGlass API (paid).

## Gmail (gog CLI)

- **Status:** NOT CONFIGURED — no OAuth tokens stored
- **Would need:** `gog auth` to set up

## Claude Code (Coding Agent)

- **Status:** INSTALLED & WORKING (v2.1.37)
- **Binary:** `/opt/homebrew/bin/claude`
- **Account:** Max plan (zero API tokens!)
- **Usage:** `claude 'prompt'` or `claude exec 'prompt'` with PTY
- **Rule:** ALL coding tasks go through Claude Code, not sub-agents
- **Always use:** `pty:true` — it's an interactive terminal app
- **Pattern:** `exec pty:true workdir:/path background:true command:"claude 'task'"`

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
