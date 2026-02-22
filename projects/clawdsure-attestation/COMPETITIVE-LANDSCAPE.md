# Competitive Landscape: Agent Harness Attestation & Verification
*Research date: Feb 20, 2026*
*Scope: ALL agent harnesses, not just OpenClaw*

## Summary
Nobody is doing continuous cryptographic attestation of harness configuration state with a chain-linked audit trail designed to feed parametric insurance. The gap is real and current.

---

## TIER 1 — Direct competitors (attestation / config verification)

### Acuvity (acuvity.ai)
- **What:** "Agent Integrity Framework" — 5 pillars: Intent Alignment, Identity & Attribution, Behavioral Consistency, Audit Trails, Operational Transparency
- **Published:** Feb 2026 (2 weeks ago)
- **Technical approach:** Behavioural monitoring — are agent actions aligned with intent
- **Gap vs ClawdSure:** No machine fingerprint, no cryptographic config hash chain, no parametric insurance hook. Framework document, not a deployed verification layer.
- **Status:** WATCH CLOSELY — most likely to move into the space

### Sumsub "Know Your Agent" (KYA)
- **What:** Binds AI agent identity to verified human identity. Agent-to-human accountability chain.
- **Launched:** Jan 29, 2026
- **Gap:** KYC for agents, not harness integrity. Different attack surface entirely.

### HID Global — PKI for AI Agents
- **What:** Capability attestation via PKI — what is this agent allowed to do
- **Gap:** Identity + capability scoping, not runtime config state. No insurance connection.

### ERC-8004 (Ethereum proposed standard)
- **What:** On-chain registries: Identity, Reputation, Validation for autonomous AI agents
- **Gap:** Crypto-native only. Not relevant to enterprise harnesses.

### Autonolas / Olas
- **What:** Decentralised agent coordination with on-chain identity and service agreements
- **Gap:** Registration layer, not harness config attestation

---

## TIER 2 — Adjacent: security / monitoring / observability

| Company | What they do | Why it's NOT attestation |
|---|---|---|
| **Lakera Guard** (→ Check Point, $300M, Sep 2025) | Runtime prompt injection + content filtering | Input/output guardrails. No config verification. |
| **Invariant Labs** | Agent firewall: deterministic invariants over tool call traces | Behavioural, not config integrity. Open source. |
| **Protect AI / Guardian / ModelScan** | Model supply chain security, pickle exploit scanning | Model-layer, not harness-layer. No runtime attestation. |
| **Palo Alto Prisma AIRS** | AI Runtime Security — traffic inspection, model scanning | Monitoring, not attestation. |
| **Obsidian Security** | AI agent identity: short-lived certs, HSMs | Auth infrastructure, not harness verification. |
| **Credo AI** | AI governance platform, policy enforcement, model cards | Process-based, not cryptographic. |
| **LangSmith / W&B / Arize / TruLens** | Observability, evals, trace logging, output quality | None produce signed chain-linked harness config records. |

### MITRE ATLAS 2026
- Explicitly lists "Modify AI Agent Configuration" as an attack vector
- Threat taxonomy only — no mitigation tooling
- **Useful:** Legitimises the threat, can be cited in pitch

---

## TIER 3 — Insurance / risk transfer for AI agents

### Armilla (armilla.ai) ⚠️ COMPETITOR
- First MGA dedicated to AI liability
- Backed by Lloyd's (Chaucer syndicate)
- Covers: hallucinations, model errors, regulatory violations, data leakage, agent misquoting
- **Underwriting method:** Third-party testing, red-teaming, point-of-time assessment
- **Their gap:** Assess once at underwriting, no continuous runtime attestation
- **Our position:** We out-compete them on continuous verification and parametric triggers
- **Action:** Do NOT share IP with them. Monitor their product evolution.

### Testudo
- Lloyd's Lab graduate, coverholder from late 2025
- AI liability for companies integrating vendor GenAI
- Early stage, underwriting methodology not yet public
- Could be partner or compete

### Vouch
- AI insurance for startups (2024)
- Covers: AI errors, discrimination claims, IP infringement
- Not harness-specific

### CoverYourAI
- Business interruption for AI failures

### Lloyd's market (parametric experiments)
- Multiple syndicates experimenting with parametric triggers for specific AI failure events (Carrier Management, Oct 2025)
- "Paying preset amounts for specific AI failure events"
- **No continuous attestation feed to trigger cleanly — this is our product**

### The market signal
From Substack (Dec 2025): insurers rolling frontier models into claims/underwriting are asking *"How do we prove to our board and reinsurers that this won't blow up?"* — that is the ClawdSure customer.

---

## TIER 4 — Standards & frameworks

| Standard | Status | Gap |
|---|---|---|
| NIST AI RMF | Published 2023, automation tooling 2025-26 | No cryptographic mechanism specified |
| ISO/IEC 42001 | Emerging global AI management benchmark | Process-based, audit-friendly, not technical |
| EU AI Act | High-risk AI obligations in force 2026 | Requires logging/oversight/docs — no attestation spec |
| OWASP Agentic AI Top 10 | 2025 | Threat taxonomy only |
| MITRE ATLAS | Updated 2026 | Config tampering listed as attack vector, no tooling |

**The standards vacuum is the moat.** None specify the cryptographic mechanism. First mover gets to become the de facto standard.

---

## Key findings

1. **Nobody is doing continuous cryptographic harness config attestation.** The field is empty.
2. **The insurance market needs exactly this.** Armilla underwrites on one-time assessments. Parametric triggers exist conceptually but have no continuous signal.
3. **Acuvity is the company to watch** — published Agent Integrity Framework Feb 2026. If they add crypto backing to their Behavioral Consistency pillar, they enter the space.
4. **Armilla = partnership, not competition.** They have Lloyd's, MGA infrastructure, customers. They need continuous attestation feed.
5. **Standards vacuum is durable moat** — MITRE/OWASP/EU Act all say "you should" verify. Nobody says how.
6. **Decentralised approaches (ERC-8004, Olas) serve a different market** — crypto-native agents, not enterprise harnesses.

---

## Action matrix

| Company | Why | Next step |
|---|---|---|
| Armilla | Competitor — MGA with point-in-time assessment, no continuous attestation | Monitor, do not engage |
| Acuvity | Closest framework competitor, 2 weeks old | Monitor, track product launches |
| Testudo | Lloyd's Lab, AI liability MGA, early | Watch for methodology publication |
| Invariant Labs | Tool-call invariants = complementary technical layer | Assess technical partnership |
| Sumsub | KYA framework, human binding | Integration potential |

---

*Sources: acuvity.ai, sumsub.com, armilla.ai, protectai.com, checkpointresearch (Lakera), reinsurancene.ws, pymnts.com, helpnetsecurity.com, arxiv.org/2511.02841, arxiv.org/2505.19301, arxiv.org/2511.15712, chaincatcher.com, ainvest.com, practical-devsecops.com, spiceworks.com, carriermanagement.com, techlifefuture.com, autonomousintelligence.substack.com, blog.hidglobal.com, dev.to/htekdev*
