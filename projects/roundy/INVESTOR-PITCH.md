# Roundy — Investor Pitch

## The Problem

Fundraising is broken at the process level.

A founder raising a seed round manages 40-80 investor conversations simultaneously. Each conversation is a multi-week, multi-touch sales cycle with no CRM built for it. So founders use spreadsheets, scattered notes, and gut instinct to decide who to follow up with, when, and what to say.

The result: founders lose deals they should win. Not because the business is wrong, but because the follow-up was late, the objection went unaddressed, or the warm lead went cold while they chased a dead one.

This is a $4.7B problem. In 2024, 37,000 companies raised venture funding globally. The average founder spends 6 months fundraising and takes 60+ meetings to close a round. That is 2.2 million investor meetings per year, almost entirely unstructured.

No tool exists that tells a founder: "Stop chasing Sequoia. They went quiet 11 days ago after you couldn't answer the unit economics question. Focus on Emma at Founders Fund — she asked for your data room yesterday and you haven't sent it."

## The Product

Roundy is a fundraising operating system that builds a context graph from every investor interaction and computes the single highest-leverage action a founder should take each day.

It is not a CRM with AI bolted on. It is an intelligence system with a CRM underneath.

**How it works:**

1. **Interactions go in.** A founder uploads a meeting transcript, pastes an email thread, or logs a quick note. Roundy's AI extracts entities, sentiment, commitment signals, objections, and action items automatically. Every piece of data becomes a node in the context graph.

2. **The graph learns.** Roundy tracks behavioral signals per investor: response latency, meeting frequency, commitment language vs hedge language, who owns the next step. It classifies investors into archetypes (fast mover, slow deliberate, relationship builder) and detects momentum changes before the founder notices them.

3. **Actions come out.** Each morning, Roundy surfaces "The Move" — one prioritized recommendation backed by specific evidence. Not "follow up with investors" but "Send the data room to Emma Wilson at Founders Fund. She asked for it 2 days ago, has responded within 24 hours to every previous message, and her conviction score has increased from 4/10 to 7/10 across your last three interactions."

**Key capabilities:**

- **Pitch Intelligence**: Upload transcripts, get scored (0-100) on clarity, structure, and delivery. See what consistently lands and what consistently misses across all your pitches. Get objection clustering, FAQ generation, and investor-specific prep.

- **Heat Tracker**: Momentum detection based on velocity, not vibes. A deal trending up from EV=2 to EV=3 is hotter than one sitting at EV=4. Combines response latency, conviction signals, and stall risk into a single score.

- **Conviction Index**: "Am I getting better at pitching?" Track your improvement over time. See recurring patterns — what you keep nailing, what you keep missing, which objections you've learned to handle.

- **Context Graph**: Structured knowledge extraction from unstructured text. "Blake Rhodes is a partner at Sequoia. He is concerned about unit economics. He invested in Acme Corp's Series A." Every fact links to a verbatim quote from a specific interaction.

- **Layered Memory**: Every interaction is stored in a vector database for semantic search and in an episodic memory system (Hindsight) for pattern analysis. When a founder asks "What did Andrea say about our pricing?", the system retrieves the exact conversation, not a summary.

- **Adversarial Validation**: After analyzing a pitch transcript, Roundy impersonates the investor and predicts their actual next action: follow up, stall, soft pass, or hard pass. This catches founder optimism bias — when you think a meeting went well but the signals say otherwise.

## The Market

**TAM**: $4.7B — all founders actively fundraising globally, at an average willingness-to-pay of $600/year for tooling that materially improves outcomes.

**SAM**: $1.2B — English-speaking markets (US, UK, EU, ANZ), tech-enabled founders who already use some form of digital fundraising management.

**SOM (Year 3)**: $12M ARR — ~7,100 paying accounts at ~$140/month blended ARPU, with accelerator tier expansion.

**Why now:**

1. **LLM capability inflection.** Claude Sonnet 4 can extract structured data from unstructured transcripts with 90%+ accuracy. This was not possible two years ago at any price point.

2. **Meeting transcript ubiquity.** Tools like Granola, Otter, and Fireflies mean founders now have transcripts of every investor call. The raw data exists — nobody is doing anything useful with it.

3. **Founder tool fatigue.** The CRM incumbents (Affinity, Attio, HubSpot) optimize for relationship tracking, not fundraising process optimization. Founders don't need another place to store contacts. They need someone to tell them what to do next.

## Business Model

| Plan | Price | Target |
|------|-------|--------|
| Pro | $119/month | Solo founders actively raising |
| Team | $249/month + $59/seat | Multi-founder teams, advisors |
| Accelerator | Custom (from $2,000/month) | Accelerators, studios, VCs managing portfolio fundraising |

Annual discount: 17% (Pro at $99/month, Team at $209/month).

No free tier. Founders raising a round don't optimise for free — they optimise for speed. A 14-day free trial proves the value; the intelligence layer pays for itself after one saved deal interaction.

**Unit economics:**
- **CAC**: $65 (content-led growth + founder community referrals + Boardy co-distribution)
- **LTV**: $1,344 (9.6-month average fundraising engagement, 85% monthly retention, ~$140 blended ARPU)
- **LTV/CAC**: 20.7x
- **Gross margin**: 82% (AI inference at ~$0.12/interaction, higher ARPU dilutes fixed cost)

**Pricing rationale:**
Affinity charges $200+/month for relationship intelligence. Fundingstack charges $250/user/month. Roundy's intelligence layer — pitch scoring, adversarial validation, behavioral prediction — is more valuable than a contact database. $119/month is priced below the competition for a more capable product. Room to grow.

**Growth flywheel:**
1. Founder uses Roundy to raise a round
2. Round closes successfully (attribution event)
3. Founder recommends to portfolio founders
4. Investors who saw good follow-up processes ask founders what tool they use
5. Accelerators adopt Roundy for their cohorts — batch distribution

The recommender is not the user — it is the investor who received unusually good follow-up from a founder using Roundy.

**Boardy co-distribution:** Boardy (AI networking agent, $8M raised) connects founders to investors. Roundy manages what happens after the introduction. Together they own the entire fundraising funnel. Co-launch targets $1M combined ARR.

## Traction

- Product launched Q4 2025
- Active in production with real fundraising workflows
- Full AI pipeline operational: transcript ingestion, pitch scoring, daily recommendations, meeting prep
- 58 UI components, 30+ AI tools, 50+ API endpoints
- Context Graph and Hindsight memory system deployed
- Granola integration live (MCP protocol)
- Stripe billing integrated with trial flow

## Competitive Landscape

| Competitor | What they do | What they don't do |
|------------|-------------|-------------------|
| **Affinity** | Relationship intelligence, auto-captures emails | No pitch analysis, no behavioral signals, investor-side tool |
| **Attio** | Flexible CRM with workflows | Generic — not built for fundraising process |
| **Visible.co** | Investor updates and reporting | Post-raise tool, not active fundraising |
| **DocSend** | Document sharing analytics | Tracks opens, not conversations |
| **Otter/Granola** | Meeting transcription | Raw transcripts, no analysis or recommendations |

Roundy's moat is the **context graph**. Every interaction a founder logs makes the system smarter — better at predicting which deals are real, which are stalling, and what the founder should do about it. This compounds. After 20+ interactions, Roundy knows more about your fundraising pipeline than you do.

## The Team

Building at the intersection of AI, fintech, and founder tooling.

## The Ask

Raising a seed round to:

1. **Expand the intelligence layer** — deeper behavioral analysis, automated email drafting, calendar integration for zero-friction interaction logging
2. **Launch self-serve growth** — founder community, content marketing, referral program
3. **Build the investor-side product** — the natural expansion: give investors a view into their deal flow, powered by the same context graph (with founder consent)

Target: 18 months runway to $1M ARR and Series A readiness.

## Why This Matters

Every year, good companies die because their founders are bad at fundraising process. Not bad at building. Not bad at selling. Bad at managing 60 simultaneous conversations with high-status strangers who will never tell you the truth.

Roundy fixes this. One recommendation per day, backed by evidence, computed from every interaction you've ever had. No more gut feel. No more missed follow-ups. No more losing deals you should have won.
