# Berman OpenClaw Implementation Prompts

*Source: Matt Berman (mberman84) — gist.github.com/mberman84/065631c62d6d8f30ecb14748c00fc6d9*
*From Ben Pouladian video transcript. These are the original prompts, not repackaged.*
*Saved: 2026-02-12*

---

## Relevance Map

| # | Prompt | Our Use Case | Priority |
|---|--------|-------------|----------|
| 1 | Personal CRM | Contact mgmt for ClawdSure/Roundy/Nightjar | Medium — after ClawdSure ships |
| 2 | Knowledge Base (RAG) | We have memory-core; good upgrade spec | Low — working solution exists |
| 3 | Content Idea Pipeline | **Repurpose for market research / BTC report** | Medium — pattern fits trading intel |
| 4 | Social Media Research | **BTC social sentiment + X monitoring** | Medium — feeds into BTC scanner |
| 5 | YouTube Analytics | Not relevant | Skip |
| 6 | AI Council | **Already spec'd** at `trading/BTC-COUNCIL-PATTERN.md` | Have it |
| 7 | CRM NL Access | Depends on #1 | Low |
| 8 | Content Humanization | We have SOUL.md + kill list | Have it (better) |
| 9 | Image Generation | Have openai-image-gen skill | Have it |
| 10 | Task Management | **Roundy does this** — meeting → tasks | Cross-ref with Roundy |
| 11 | AI Cost Tracking | `openclaw gateway usage-cost` exists; `ref/COST-TRACKING.md` | Have it |

---

## Prompts We'll Adapt

### 1. Personal CRM Intelligence

Build me a personal CRM system that automatically tracks everyone I interact with, with smart filtering so it only adds real people — not newsletters, bots, or cold outreach.

Data sources:
- Connect to my email (Gmail API or IMAP) and scan the last 60 days of messages.
- Connect to my calendar (Google Calendar API) and scan the last 60 days of events.
- Run this ingestion on a daily cron schedule.

Contact extraction from email:
- Extract sender/recipient email addresses and names from messages.
- Estimate the number of exchanges (back-and-forth threads, not just raw message count): Math.min(Math.floor(totalMessages / 2), threadCount).
- Collect sample subject lines and message snippets for classification.

Contact extraction from calendar:
- Only include meetings with 1-10 attendees (skip large all-hands).
- Only include meetings at least 15 minutes long (skip quick check-ins that are really just reminders).
- Extract attendee names, emails, and the meeting title.

Filtering — two-stage:

Stage 1 — Hard filters (always reject):
- My own email addresses and domains.
- Emails from family or personal contacts I've explicitly excluded (configurable list).
- Contacts already in the CRM or previously rejected.
- Generic role-based inboxes: info@, team@, partnerships@, collabs@, noreply@.
- Marketing/transactional domains matching patterns like: noreply@, tx., cx., mail., email. prefixes.

Stage 2 — AI classification (Haiku or Gemini Flash):
- REJECT clearly automated or notification-only senders.
- REJECT if all sample subjects look like newsletters, digests, or automated reports.
- REJECT cold outreach with low engagement.
- REJECT if snippets show repetitive promotional content.
- APPROVE only if it looks like a real person with genuine two-way interaction.

Contact scoring:
- Base score: 50
- +5 per email exchange (max +20), +3 per meeting (max +15)
- +15 if title matches preferred titles (CEO, Founder, VP, etc.)
- +10 if appeared in small meetings (≤3 attendees)
- +10 if last interaction within 7 days, +5 if within 30 days
- +25 bonus if person appears in both email AND calendar
- +10 if recognizable role, +5 if has company

Storage: SQLite with WAL mode. Embeddings for semantic retrieval. Learning system with skip_domains, prefer_titles, skip_keywords. Dedup by email then name+company.

### 3. Content Idea Pipeline → Market Research Adaptation

Original: content idea dedup + research pipeline. Adapt for:
- **Trading signal research**: "What's the market saying about [city] weather?" → search X, KB, web → dedupe against previous signals → brief
- **BTC intelligence**: topic scanning with semantic dedup against previous reports
- **ClawdSure market research**: competitive landscape scanning

Core pattern worth keeping:
- Trigger on topic → multi-source research → semantic dedup (70% vector / 30% keyword, 40% similarity gate) → brief assembly → store with embedding
- Status tracking: pitched/accepted/rejected/produced/duplicate

### 4. Social Media Research (Tiered X Search)

Tiered retrieval — cheapest first:
- Tier 1 (free): FxTwitter API (api.fxtwitter.com) — individual tweet lookups
- Tier 2 (~$0.15/1K tweets): TwitterAPI.io or SocialData — search, profiles, threads
- Tier 3 (~$0.005/tweet): Official X API v2 — last resort, rate limit 350ms between requests

Cascade by operation:
- Single tweet: T1 → T2 → T3
- Search: T2 → T3
- Profile/thread: T2 → T3

Output: 3-5 key narratives, 5-10 notable posts with links, sentiment summary, contrarian takes.
Cache with 1-hour TTL. Log all API calls with cost estimates.

### 6. AI Council (Reference — we have our own spec)

See `trading/BTC-COUNCIL-PATTERN.md`. Their version adds:
- Explicit signal normalization schema: { source, signal_name, value, confidence, direction, category }
- 4 named personas: GrowthStrategist, RevenueGuardian, SkepticalOperator, TeamDynamicsArchitect
- Priority formula: (impact × 0.4) + (confidence × 0.35) + ((100 - effort) × 0.25)
- Fallback: if consensus fails, use draft; if reviewer fails, stub with error

### 10. Task Management from Meetings

Cross-reference with Roundy — Roundy already does commitment extraction from transcripts.
Useful pattern: approval flow before creating tasks (show numbered list → user picks → create).

### 11. AI Cost Tracking

We already have `openclaw gateway usage-cost`. Their additions worth noting:
- JSONL append-only log per API call with taskType classification
- Routing suggestions: flag frontier model use on simple tasks
- Flag workflows >25% of total spend as optimization candidates

---

*Don't build any of these yet. Reference specs for when the time comes.*
