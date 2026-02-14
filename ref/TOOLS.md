# TOOLS.md — Local Notes

Skills define _how_ tools work. This file is for _your_ specifics.

---

## Browser Rules (MANDATORY)

1. **Always headless** — config enforces this, never spawn visible windows
2. **One tab at a time** — close when done, never leave tabs open
3. **Prefer web_fetch over browser** — browser is for interaction, not reading
4. **Prefer bird CLI for X/Twitter** — don't browser-automate X
5. **Close browser sessions** when done
6. **Spawn Haiku for browser work** — browser clicking = cheap subagents, not Opus

---

## X/Twitter (bird CLI)

- **Status:** ✅ FULLY WORKING (verified Feb 11, 2026)
- **Auth:** Chrome default profile cookies (automatic)
- **Account:** @Clawdine_shoe (ID: 2017895400984764417)
- **Commands:**
  - `bird whoami` — verify auth
  - `bird read <url>` — read tweet/thread
  - `bird tweet "text"` — post
  - `bird user-tweets <handle> -n 10 --json` — get user's tweets
  - `bird search <query> --json` — search
- Safari cookie warning is harmless — falls back to Chrome, works fine.
- **DO NOT claim bird is broken.** It works. Reading, posting, search all functional.

## Email (AgentMail)

- **Status:** ✅ WORKING
- **Address:** clawdine@agentmail.to
- **API key:** `~/.openclaw/workspace/.credentials/agentmail-api-key`
- **Helper:** `uvx --from agentmail python ~/.openclaw/workspace/scripts/clawmail.py inbox`
- **SDK:** `from agentmail import AgentMail`
- **CRITICAL:** Always use base64 attachment method. Inline body sends blank emails.
- **Format:** `{filename, content: <base64>, content_type}` in attachments array
- **To field:** string array `["email@example.com"]`, NOT object array

## Gmail (gog CLI)

- **Status:** ❌ NOT CONFIGURED — no OAuth tokens stored
- Needs `gog auth` to set up

---

## Memory / Vector Search

- **Provider:** OpenAI (text-embedding-3-small, 1536 dims)
- **Backend:** SQLite + sqlite-vec (`~/.openclaw/memory/main.sqlite`)
- **Plugin:** memory-core (enabled)
- **Config:** `openclaw.json` → `provider: "openai"`, `sessionMemory: true`
- **Mode:** Hybrid BM25 + vector (0.7 vector / 0.3 text)
- **Sources:** memory files (MEMORY.md + memory/*.md) + session transcripts
- **Indexed:** 13 files, 595 chunks
- **DO NOT remove or disable** — this is the vector memory layer that survives compaction

---

## Infrastructure

### Model Tiering
- **Main:** anthropic/claude-opus-4-6
- **Subagents:** anthropic/claude-sonnet-4-5
- **Cron jobs:** anthropic/claude-haiku-4-5

### Mission Control
- Location: `/workspace/mission-control`
- Run: `npm run dev` → http://localhost:3000

### OpenClaw Studio
- github.com/grp06/openclaw-studio on localhost:3000
- Zero-token dashboard for file edits, cron, model switching
- Settings: `~/.openclaw/openclaw-studio/settings.json`

### API Keys (as of Feb 10, 2026)
- Three keys: Clawdine ($390), Claudine-typo ($440), fundr ($43)
- Total: $873. Daily burn $80–120 since Feb 5.
- "Claudine" key possibly orphaned.

---

## Session Architecture

- Three Telegram groups: Main DM, ClawdSure, Prediction Day Job
- OpenClaw auto-isolates group sessions
- Groups need telegram allowlist in openclaw.json

---

## What Else Goes Here

Camera names, SSH hosts, preferred TTS voices, speaker/room names, device nicknames — anything environment-specific. Skills are shared; this file is yours.
