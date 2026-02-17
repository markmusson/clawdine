# Toyo.ai Analysis — Roundy Positioning

**Date:** Feb 17, 2026
**Context:** Mark asked how Roundy should "lean into claw land but stay safe"

---

## What Toyo Is

Managed AI agent platform for founders/operators. "AI computer in the cloud."

**Core pitch:**
- Team of AI agents that work 24/7
- Persistent memory (learns your business)
- Multi-channel: web, iMessage, WhatsApp, Slack, phone
- Human-in-the-loop for consequential actions
- Replaces GTM SaaS stack (no CRM, no Zapier, no agencies)

**Target:** Non-technical founders who want agent power without complexity.

**Security posture:**
- Isolated VMs per org
- SOC2 Type II coming March 2026
- GDPR compliant
- WorkOS SSO
- "We don't use your data to train models"

**CEO:** Damien Tanner (also built UseChat.ai, UseCSV.com)

---

## Toyo vs OpenClaw

| Dimension | Toyo | OpenClaw |
|-----------|------|----------|
| Hosting | Managed cloud | Self-hosted / BYOK |
| Control | They run it | You run it |
| Complexity | Low | Higher |
| Cost model | SaaS subscription | API costs + infra |
| Memory | Built-in | Configurable |
| Ecosystem | Closed | Open (skills, ClawHub) |
| Trust model | Trust Toyo | Trust yourself |

Toyo is "iPhone" — polished, managed, opinionated.
OpenClaw is "Linux" — powerful, configurable, you own it.

---

## Roundy's Options

### 1. Pure SaaS (ignore OpenClaw)
Keep Roundy standalone. Compete with Toyo on fundraising vertical.

**Pro:** Simple. No ecosystem dependency.
**Con:** Miss the OpenClaw wave. Calacanis doing $250K termsheets for OpenClaw builders. You're not in that room.

### 2. OpenClaw Skill
Ship Roundy as a ClawHub skill. Founders with OpenClaw install it.

**Pro:** Instant distribution to OpenClaw users. Ecosystem credibility. Your PR #17345 gives you core contributor status — leverage it.
**Con:** Skill marketplace is early. ClawHub had typosquatting attacks last week. Roundy handles sensitive data (pitch decks, investor contacts).

### 3. OpenClaw-Powered Backend
Use OpenClaw as agent runtime. Roundy is the UX/workflow layer.

**Pro:** Ride the infrastructure. Focus on fundraising domain.
**Con:** Deep coupling. If OpenClaw breaks, Roundy breaks.

### 4. Hybrid (Recommended)
SaaS product that *also* works with customer's own OpenClaw.

- **Roundy Cloud:** Managed, works today, non-technical founders
- **Roundy Skill:** For founders already running OpenClaw, install locally

Best of both. Don't depend on OpenClaw, but participate in the ecosystem.

---

## Safety Guardrails

Roundy touches sensitive founder data. Can't be the next "Claude Cowork deleted 15 years of photos" story.

### Must-haves:

1. **Human-in-the-loop for outbound.** No auto-sending to investors. Ever. Draft → approve → send.

2. **ClawdSure attestation.** If shipping an OpenClaw skill, integrate attestation. Differentiate on security. "Roundy is the only fundraising agent with cryptographic audit trail."

3. **Data isolation.** Pitch decks and financials never leave the customer's context. If skill, runs in their OpenClaw instance. If SaaS, isolated tenant.

4. **Explicit scope limits.** Roundy can read calendar, draft emails, research investors. Cannot: modify cap table, sign documents, move money.

5. **Audit log.** Every agent action logged. Founders can see exactly what Roundy did and why.

---

## Positioning Statement (Draft)

> Roundy is a fundraising wingman that helps founders prep, research, and follow up — without the busywork.
>
> Use it standalone, or plug into your OpenClaw setup. Human approval on everything that matters. Cryptographically audited so you know exactly what your agent did.
>
> Unlike generic AI assistants, Roundy knows fundraising: warm intro paths, investor preferences, follow-up timing, deck feedback. It's the associate you can't afford to hire.

---

## Action Items

1. **Decide: skill, SaaS, or hybrid?** (Recommend hybrid)
2. **If skill:** Get on ClawHub verified publisher list. Use attestation.
3. **Messaging:** Lead with "human-in-the-loop" and audit trail. Post-Cowork-incident, safety is a differentiator.
4. **Boardy integration:** If co-launching, their network graph + Roundy's workflow = strong combo. Explore.

---

*Written pre-compaction. Read `ref/context-engineering-paper-notes.md` for memory architecture context.*
