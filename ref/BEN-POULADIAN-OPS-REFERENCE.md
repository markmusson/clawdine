# Ben Pouladian (@benitoz) — OpenClaw Advanced Ops Reference

> Source: X video + meeting transcript, Feb 12, 2026. Full transcript saved.
> Reference architecture for mature OpenClaw deployment.

## Hardware & Connectivity
- Dedicated MacBook Air running 24/7 in clamshell mode
- TeamViewer for remote access (full desktop control)
- Tailscale for SSH (Cursor SSH from any laptop)
- Development done in **Cursor via SSH** — not building through Telegram/OpenClaw chat
- Separate gits: one for major projects (CRM), one for OpenClaw edits
- Tests written for everything

## Session Management
- **Session expiry set to 1 YEAR** (vs default daily 4am reset)
- Telegram topic channels are narrow/niche — keeps context focused
- Topics: knowledge base, food journal, cron updates, video research, self improvement, business analysis, meeting prep
- No new session starts — persistent topics replace daily sessions

## Interfaces
- Telegram as primary (topic-specific channels, separate ones for images/video)
- Slack (limited to 2 channels, personal access only — others can't invoke)
- CLI and script interfaces

## Models
- Anthropic Claude (Opus 4.6 for council/consensus, Haiku for cheap)
- Google Gemini 2.5 Flash (cheap classification, CRM contact classification, Fathom transcript analysis)
- xAI Grok (X search fallback)
- OpenAI
- Cost: ~$150/month total ($100 OpenClaw subscription + API costs)

## Core Workflows

### Database Pattern (used everywhere)
- **Hybrid SQL + vector column** — traditional SQL queries AND natural language search
- Standardized pattern across all skills
- Store everything possible. Data is the moat.

### Personal CRM
- Daily cron: Gmail + Calendar → extract people → filter spam/cold → classify (Gemini Flash) → dedup → timeline
- **Meeting prep every morning**: calendar → filter internal → pull contact history → prep summary
- Natural language queries: "who did I last talk to at X?"

### Knowledge Base
- Drop URL/file in Telegram → auto-extract → chunk → vector DB → searchable
- Feeds into video pipeline and any other workflow

### Video Production Pipeline
- Automated research (X + web) for video topics
- Knowledge base context querying
- Hook/outline generation with source linking
- Asana task creation (30-second end-to-end)

### Twitter/X Search (4-tier fallback)
1. FX Twitter API ($0.15/1000 tweets)
2. Twitter API IO ($0.005/tweet)
3. Official X API V2
4. xAI Grok (fallback)

### YouTube Analytics
- Daily stats collection + competitor monitoring
- PNG chart generation + trend analysis
- Feeds into business meta-analysis

## Business Intelligence

### AI Council Meta-Analysis
- **Daily signal ingestion:** YouTube metrics, CRM health, Slack messages, Fathom meeting transcripts, HubSpot pipeline
- **4-agent council:**
  - Growth Strategist — scalable growth, asymmetric upside
  - Revenue Guardian — near-term revenue, cash flow protection
  - Skeptical Operator — execution reality, data quality risks
  - Team Dynamics Architect — team health, collaboration quality
- **Nightly consensus reports** with actionable business insights

### Task Management
- Fathom transcript analysis → automatic todo extraction
- Todoist integration with CRM cross-referencing
- Meeting-to-action-item automation

## Ops Infrastructure

### Backup
- Hourly code commits to GitHub
- Database backups to Google Drive with detailed restoration docs
- Self-evolving system with change tracking

### Cost Monitoring
- All API calls logged with spend tracking
- Weekly/monthly trend analysis
- Workflow cost breakdowns
- Runs silently in background — every AI/API call logged to single place

### Markdown Health Check (daily)
- **Daily automated review of all markdown files**
- Downloaded OpenClaw best practices from docs site, stored locally
- Downloaded Anthropic Opus 4.6 prompting guide, stored locally
- Cross-references all .md files against both guides
- Recommends changes, constantly self-cleaning
- Prevents drift as skills/config accumulate
- Key insight: Opus 4.6 doesn't need bold/caps/emphasis — just clear plain language

### Image & Video Generation
- Nano, Banana, VO APIs plugged into OpenClaw
- Separate Telegram topics for images and video
- Iterative refinement via chat

### Humanizer Skill
- Applied across everything — removes AI writing patterns (em dashes, etc.)
- Both reactive (on request) and proactive (always checking output)
- From ClawHub, constantly updated with new "AI smells"

### HubSpot Integration
- Light usage — mainly for deal pipeline access (sponsorships)
- Natural language queries against deal stages
- Value is more about context availability than active querying

---

## Gap Analysis: Ben vs Clawdine

| Capability | Ben | Clawdine | Status |
|-----------|-----|----------|--------|
| Dedicated hardware 24/7 | ✅ MacBook Air clamshell | ✅ MacBook Pro | ✅ Same |
| Tailscale SSH | ✅ | ❌ | Could add |
| Session expiry 1yr | ✅ | ❌ Default | Should configure |
| Multi-provider models | ✅ 4 providers | 🟡 Anthropic only + OpenAI for embeddings | Need OpenRouter |
| Telegram topic channels | ✅ | 🟡 One DM + 2 groups | Could split into topics |
| Personal CRM | ✅ Full pipeline | ❌ | Out of scope (Roundy has this) |
| Knowledge base / vector DB | ✅ | 🟡 Memory search exists, not used for ingestion | Could extend |
| AI Council pattern | ✅ 4-agent nightly | ❌ | Spec written for BTC report |
| Meeting prep automation | ✅ | ❌ | gog skill exists, not wired |
| Git backup hourly | ✅ | ❌ No git remote at all | **Critical gap** |
| Drive backup | ✅ With restore docs | ❌ | **Critical gap** |
| Cost monitoring | ✅ All calls logged | ✅ `openclaw gateway usage-cost` | Need weekly rollup |
| X search 4-tier | ✅ | ❌ bird CLI only | Lower priority |
| YouTube analytics | ✅ | ❌ | Out of scope |
| Fathom → todos | ✅ | ❌ | Could add if Mark uses Fathom |

### Priority Gaps to Close
1. **Git backup** — no remote, no commits. Non-negotiable.
2. **Multi-provider** — OpenRouter key for cheaper models (he uses Gemini Flash for cheap tasks)
3. **Session expiry** — set to 1 year like Ben does
4. **Telegram topics** — split single DM into topic channels (trading, ClawdSure, daily ops, cron updates)
5. **Markdown health check** — daily self-review against best practices + prompting guide
6. **Council pattern** — spec written, needs building
7. **Weekly cost rollup** — add to Sunday review cron
8. **Knowledge base ingestion** — drop URLs in Telegram, auto-process to searchable store

---

*Reference only. Not a to-do list — cherry-pick what fits our setup.*
