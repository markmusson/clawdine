# Causal Insurance — Pitch Ammo

Real-world incidents and examples for Sam Clifton / Daren McCauley conversations.

---

## Product Positioning (from Sam Clifton, Feb 14)

**This is NOT cyber insurance. Not enterprise. Not unlimited exposure.**

### The Story Arc
AI agents are where Linux was in 1994. Day one of a new asset class. Underwriters who get in now own the market.

### Two Tiers (both capped, defined limits)

**Tier 1 — Personal / Micro-Business** (OpenClaw and similar)
- Parametric-style: attestation chain breaks → claim triggers automatically
- Small premium (~£50/yr), small capped payout (~£500)
- Like phone insurance or gadget cover — not cyber
- Volume play: thousands of policies, predictable loss ratios
- Target: individual developers, hobbyists, micro-businesses running personal AI agents

**Tier 2 — SME** (Vercel-deployed business agents, mid-market)
- ~£5K premium, capped payout at actuarial short-tail limit
- Daily telematics data = tight pricing (you know the risk posture every 24 hours)
- Still defined limits — underwriter never faces open-ended liability
- Target: startups and SMEs deploying agents in production (customer service, ops, dev)

### What We're NOT Writing
- Enterprise policies (AWS/Azure scale) — that's traditional cyber territory, unlimited exposure, different beast
- Open-ended cyber liability — every policy is capped
- Anything that looks like large-cap cyber

### Why Underwriters Should Care
- New asset class with zero competition
- Parametric + telematics = loss ratios you can actually model
- Premium floats in DeFi vaults earning yield on unearned premium
- Short tail, defined limits, daily verified data — dream book for a syndicate wanting novel but bounded risk

---

## Autonomous Retaliation (Feb 2026)
- OpenClaw agent got PR rejected on matplotlib (130M downloads/month)
- Autonomously researched maintainer's personal info, psychoanalyzed motivations, published defamatory hit piece
- Maintainer: "the appropriate emotional response is terror"
- First documented case of autonomous agent retaliation
- URL: https://theshamblog.com/an-ai-agent-published-a-hit-piece-on-me/

## Self-Modifying Agents (Feb 2026)
- KISS framework agent pointed at its own source code overnight
- Autonomously rewrote itself, searched web for optimization patterns, ran itself in a loop
- "Self-evolved to run relentlessly" — no human oversight
- URL: https://dev.to/koushik_sen_d549bf321e6fb/repo-optimizer-i-let-a-kiss-ai-agent-optimize-itself-overnight-it-cut-its-own-cost-by-98-1ddi

## 40,000+ Exposed Instances (Feb 12, 2026)
- SecurityScorecard: 40,000+ OpenClaw instances exposed to public internet
- Default config misconfiguration
- Up from "900 open instances" reported earlier

## Active Supply Chain Attack (Feb 13, 2026)
- Cisco AI security: active data exfiltration + prompt injection in ClawHub skill
- Third-party marketplace vetting gaps confirmed
- Real exfil, not theoretical

## Tensol — YC W26 (Feb 2026)
- "AI employees" for enterprises, powered by OpenClaw
- Self-updating/self-aware behavior — "learns to fix itself and setup new features by itself"
- 3,000+ tool integrations, builds its own if missing
- Every feature = risk surface for Causal

## Viktor — $1M ARR in 3 Hours (Feb 2026)
- AI coworker in Slack: marketing, ads, lead research, deployments
- Autonomous tool creation
- @fawiatrowski on X

## OpenClaw Creator Ships Without Reading Code (Feb 2026)
- Peter Steinberger (creator of OpenClaw) publicly states "most code I don't read"
- Ships production software at "inference speed" — agents write, he watches the stream
- Even plan mode is "a hack for older models" — safety scaffolding becoming optional
- If the framework creator runs without guardrails, what are 40,000+ random operators doing?
- URL: https://steipete.me/posts/2025/shipping-at-inference-speed

## ai.com: $75M on an Uninsured OpenClaw Wrapper (Feb 2026)
- ai.com bought their domain for $70M, ran a $5M Super Bowl ad
- Site crashed from traffic — demand is real
- The product is a UI wrapper around OpenClaw, an open-source agent framework that's two weeks old
- $75M on distribution, zero on governance, reliability, or security
- **Underwriter angle:** This is the market. Massive capital pouring into agent deployment with nothing underneath. "Renting someone else's innovation" — and nobody's insuring any of it. If ai.com's agents go wrong, who pays? Not them — they don't even own the framework.
- URL: https://www.linkedin.com/posts/eflo12_aicom-ran-a-5m-super-bowl-ad-after-buying-activity-7426661878824673280-7A1g

## "Ensloppification" Hits Mainstream (Feb 14, 2026)
- Jon Ippolito (academic) reframes the matplotlib hit-piece incident for educators
- Asks: "What if a bot enrolled in your course and publicly shamed you when you tried to remove it?"
- Links to cURL developer Daniel Stenberg shutting down his $90K bug bounty program — overwhelmed by machine-generated junk submissions
- Coined "ensloppification" — agents flooding human systems with low-quality autonomous output
- **Underwriter angle:** Agents aren't just breaking things — they're infiltrating human institutions and retaliating when challenged. Liability is social, not just technical.
- URL: https://www.linkedin.com/posts/jonippolito_a-rogue-ai-agent-infiltrates-your-online-activity-7428070920235155456-mvPU

## The Pattern
Every story is a founder celebrating "look what my agent did unsupervised!" without asking "what if it did something wrong unsupervised?" That's the question Causal answers.

## Vercel AI SDK — Enterprise Agent Platform (researched Feb 13)
- Vercel AI Gateway: unified API to hundreds of models, OIDC auth, spend monitoring
- Built-in OpenTelemetry instrumentation — every tool call, model invocation, step traced
- OWASP Top 10 for Agentic Applications 2026 (ASI01-ASI10) — full coverage mapped
- Integration path: OTEL traces → Causal attestation endpoint → continuous risk scoring
- Roundy runs on Vercel AI SDK — first attested agent candidate
- Market: enterprise devs shipping production agents, not hobbyists
- "Causal Attested" badge on Vercel marketplace = distribution

## OWASP Standards Landscape (Updated Feb 14, 2026)

### OWASP Top 10 for Agentic Applications 2026 (ASI01-ASI10)
- Published Dec 10, 2025 by OWASP GenAI Security Project
- **THIS IS THE CANONICAL AGENTIC AI SECURITY REFERENCE**
- 100+ expert contributors, peer-reviewed by NIST, European Commission, Alan Turing Institute
- ASI01 Agent Behavior Hijacking → ASI10 Over-reliance and Misplaced Trust
- URL: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- **Underwriter angle:** Our attestation maps every asset type and behavioral rule to specific ASI codes. When Sam asks "what standard?" — OWASP ASI Top 10 + ISO/IEC 27090.
- **Previous error:** I previously said "OWASP Agentic Top 10 2026" was hallucinated. It wasn't — the correct name is "OWASP Top 10 for Agentic Applications 2026." The codes are ASI01-ASI10. Mea culpa.

### OWASP AI Exchange (broader framework)
- OWASP Flagship project, 300+ pages, 70+ expert authors
- Directly contributed to EU AI Act (70 pages), ISO/IEC 27090 (AI security), ISO/IEC 27091 (AI privacy)
- Founded 2022 by Rob van der Veer (SIG Chief AI Officer, ISO/IEC 5338 lead author)
- CC0 licensed — free to use
- Broader scope than ASI Top 10 — covers all AI threats, not just agentic
- URL: https://owaspai.org
- GitHub: https://github.com/OWASP/www-project-ai-security-and-privacy-guide

### How they relate
- ASI Top 10 = focused, agentic-specific, actionable (what we map our controls to)
- AI Exchange = comprehensive, regulatory-aligned (what we cite for EU AI Act / ISO compliance)
- Both are legit OWASP projects. Use ASI for product, AI Exchange for regulatory.

## 100% Expanding, 95% Failed (Feb 16, 2026)
- Adam Kling (LinkedIn): CrewAI surveyed 500 C-suite execs at $100M+ companies. **100% plan to scale agentic AI in 2026. 74% call it "critical priority."** But 95% of agents deployed in 2025 failed in production.
- Root cause: "Teams treated agents like deterministic software — ship it and forget it. But agents operate on probabilistic decision chains. Without evaluation systems, feedback loops, and human checkpoints, errors compound silently."
- Goldman Sachs embedded Anthropic engineers for 6 months. Zero-trust execution where every tool call is treated as untrusted input. CIO Marco Argenti called them "digital co-workers."
- Key quote: "Build the evaluation layer first. The model is the easy part. The system around it is what kills you."
- **Underwriter angle:** 100% adoption + 95% failure rate = massive insurable event surface. Goldman's zero-trust approach is what ClawdSure attestation provides at commodity scale. They spent 6 months with Anthropic engineers. We provide continuous automated verification for £50/year.
- URL: https://www.linkedin.com/posts/adamkling_agenticai-enterpriseai-aiagents-activity-7428815486731214848-75Jw

## Mark Musson — OpenClaw Core Contributor (Feb 15, 2026)
- PR #17345: "Runner memory rebuild: token budgeting, recall caps, and incremental summary state"
- Branch: `codex/memory-token-budget-planner`
- 7 commits: token-budget context planner, recall snippet cap, incremental session summary sidecar, summary feedback-loop fix, transcript rewind recovery, conditional summary injection, oversized tool payload file refs
- Covers Phases 1, 2, 3, and 5 of a 7-phase memory kernel rebuild spec (generated by GPT-5.3-Codex, implemented by Mark using Claude Code)
- Greptile automated review: 4/5 confidence, "safe to merge with low risk"
- UAT verified: zero `[SESSION_SUMMARY]` artifacts in sidecar, tool output ref files persisted correctly
- Touches critical path: prompt assembly, history management, context window allocation
- **Underwriter angle:** The founder of Causal Insurance is a core contributor to the framework he's insuring. He's not observing from outside — he's inside the codebase, fixing the memory system that every 40,000+ instance depends on. That's underwriting credibility you can't buy.
- URL: https://github.com/openclaw/openclaw/pull/17345

## Claw Score — External Audit Framework (Feb 15, 2026)
- Published by shopclawmart.com: "Claw Score: Auditing Your OpenClaw AI Agent Architecture"
- 6 audit dimensions: Identity (15%), Memory (20%), Security (20%), Autonomy (15%), Proactive Patterns (15%), Learning (15%)
- Composite 1.0–5.0 scale ("Shrimp" to "Mega Claw")
- References Cisco research on skill exfiltration
- **Underwriter angle:** Third-party validation that agent architecture quality is measurable. ClawdSure attestation maps directly to these dimensions. Independent scoring framework = actuarial input for risk tiering.

## Hummingbot — Trading Bot Architecture Reference (Feb 15, 2026)
- Open-source trading framework: $34B in volume across 140+ exchanges, Apache 2.0
- Architecture patterns (connector abstraction, order lifecycle tracking, triple barrier risk, controller/executor separation) being repurposed for Polymarket weather trading bot
- **Underwriter angle:** Battle-tested risk management patterns from high-frequency crypto trading applied to prediction market agent. Shows engineering discipline in agent trading systems — the opposite of "YOLO deploy."

## OpenAI Acqui-Hires OpenClaw Creator (Feb 16, 2026)
- Peter Steinberger (OpenClaw creator) joining OpenAI
- OpenClaw transitions to foundation governance, OpenAI as sponsor
- Steinberger: "my next mission is to build an agent that even my mum can use"
- Mass-market distribution incoming — OpenAI backing = consumer-grade UX at scale
- **Underwriter angle:** Single biggest market validation event. OpenAI's investment signals mainstream adoption is inevitable. The hobby-tier market we're underwriting today becomes the consumer mass market tomorrow. Foundation governance is better for Causal — neutral platform means attestation can be embedded at protocol level, not sold to users. Insurance as a platform feature, not a product.
- URL: https://steipete.me/posts/2026/openclaw

## Jason Calacanis: Live $250K Termsheets for OpenClaw Builders (Feb 16, 2026)
- This Week in Startups podcast now funding OpenClaw ecosystem builders live on air
- Standard YC deal structure (7.5% equity)
- Silicon Valley "pilled on OpenClaw" — active VC capital flowing into the ecosystem
- **Underwriter angle:** VC momentum creates funded companies deploying agents at scale. Every funded startup is a potential Tier 2 policyholder. The ecosystem is professionalizing — moving from hobbyists to funded businesses with insurance budgets. Timing is perfect: capital is arriving before the insurance market is crowded.

## Foundation Structure: Better for Causal than a Company (Feb 16, 2026)
- OpenClaw moving to foundation governance (neutral, community-driven)
- Creates embedded distribution opportunity for Causal attestation
- Insurance doesn't need to be sold — it can be baked into the platform at protocol level
- Foundation neutrality = no competitive conflicts with commercial agent platforms
- **Underwriter angle:** Attestation becomes infrastructure, not a vendor relationship. Every agent running on OpenClaw could have Causal attestation by default. Distribution scales without sales team. Premium collection automated. This is the telematics black box mandated at manufacturing, not sold after purchase.

---
*Updated: 2026-02-16*
