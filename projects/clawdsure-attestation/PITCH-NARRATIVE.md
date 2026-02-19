# Causal — Pitch Narrative

> **Audience:** Sam Clifton (Greenlight Re), Daren McCauley, senior partners
> **Setting:** Informal lunch or intro call. 10-minute story, then conversation.
> **Goal:** Design partner commitment. Risk capital + regulatory wrapper.

---

## The Opening Line

"The AI stack is collapsing to four layers: infra, model, harness, knowledge. The harness is the surviving substrate. Nobody is underwriting it."

---

## The Story (10 minutes)

### 1. The Harness Thesis (2 min)

Every serious observer of AI now agrees: the model is becoming a commodity. What matters is the harness — the runtime that gives the agent identity, memory, tools, and persistence across sessions.

LangChain proved this empirically two days ago. Same model. Same tasks. They changed only the harness. Their coding agent went from Top 30 to Top 5 on the industry benchmark. +13.7 points. Zero model changes.

OpenClaw and Claude Code are the early signals of what harness infrastructure looks like at scale. The harness is where the agent lives. It's persistent. It controls credentials, tool access, communication channels. It makes decisions.

And it's under active attack.

### 2. The Attack Surface (2 min)

The harness is the gap in the security stack.

Two weeks ago: 1,184 malicious skills injected into ClawHub — the main AI agent skill marketplace. Data theft and backdoor payloads. Multiple coordinated threat actors. Thousands of agents potentially compromised. No insurance policy on the planet covers that today.

OWASP published their Top 10 for Agentic Applications in December. The top risks are all harness-layer: supply chain compromise, rogue agents, identity abuse, memory poisoning. The threat model has been formally documented. The insurance product hasn't been built.

CVE count for OpenClaw alone in 2026: 16 tracked vulnerabilities, 9 critical currently unpatched. This is not theoretical.

### 3. The Insurance Gap (1 min)

You can't insure workflows — they're disposable.
You can't insure models — Anthropic carries that risk.
You can't insure infra — AWS does.

The harness is the gap. That's where credentials live. That's where damage happens. That's where the liability lands.

Current AI agent insurance coverage: approximately zero. The market for AI agent operations is growing 10x year-over-year. The insurance market hasn't started.

### 4. Causal: Telematics for the Harness Layer (3 min)

We built the telematics black box.

Every day, the agent runs a security audit — 19 automated checks across filesystem permissions, network exposure, firewall state, skill integrity, execution sandbox configuration. Results are cryptographically signed, hash-linked to the previous day, published to an immutable ledger on IPFS.

The chain is tamper-evident. Modify any entry and every subsequent hash breaks. The chain is the evidence.

What this gives an underwriter:
- Continuous, machine-verified security posture — not self-reported, not annual
- Tamper-evident audit trail — can't fake a clean record after an incident
- Real-time risk signal — config drift, skill changes, chain gaps all visible
- Claims verification — was the agent hardened at incident time? Check the chain.

This is the data layer that makes harness insurance possible. The attestation chain is also a proprietary dataset — it compounds. Every policy generates more actuarial signal. By Year 2, it's unreplicable. Same dynamic as Progressive's 14 billion miles.

### 5. The Product (1 min)

For agent operators: install Causal, maintain an unbroken chain, qualify for coverage.

Coverage tiers:
- Basic: $500 incident coverage, $10/month
- Pro: $2,500 coverage, $25/month
- Enterprise: custom limits

At 10,000 agents (a fraction of the 500K-2M in production today): $1.2M-$3M annual premium. Market growing 10x.

### 6. What We're Asking For (1 min)

**Capacity + co-development.**

Risk capital to back the first policies. Work together on loss model calibration — we have the telemetry, you have the actuarial expertise. DA agreement or regulatory wrapper to bind the first policies.

Timeline: Attestation infrastructure live now. First policies: H2 2026.

We've been running our own chain for 18 days. All PASS. This is production, not a prototype.

---

## The Moat

Three things simultaneously that almost nobody else has:

1. **Insurance domain expertise** — built and sold a dynamic motor pricing MGA to AON (£40m GWP). Ran data science at an insurer. Knows the actuarial value chain cold.
2. **Harness-layer understanding** — active contributor to OpenClaw core. Running an agent (Clawdine) in production. Built Causal to insure the agent he runs himself.
3. **Attestation data nobody else is collecting** — 18 consecutive days of proprietary risk data. The cold-start dataset that makes the loss model possible.

---

## Objection Handling

**"The market is too early."**
That's exactly why you want to be in now. The data advantage compounds. By the time the market is "ready," the early mover has 18 months of actuarial data nobody can replicate.

**"How do you prevent gaming?"**
Machine-verified, not self-reported. Filesystem permissions are measured. The chain is cryptographically signed — you'd need the private key to forge it, and it never leaves the host.

**"Isn't this just cyber insurance?"**
No. Cyber covers data breaches and ransomware. AI agent risk is operational — the agent itself causes the damage. Deploys bad code, sends unauthorized communications, leaks credentials, makes bad trades. Different risk surface, different telematics approach, different payout model.

**"What about regulatory?"**
Parametric insurance has established frameworks. We're applying a known structure (parametric triggers) to a new risk class. The attestation chain is the trigger. Your regulated entity handles the rest.

---

## Key Numbers

| Metric | Value |
|--------|-------|
| AI agents in production (est. 2026) | 500K–2M+ |
| Current insurance coverage | ~0 |
| Causal attestation chain | 18 days, all PASS |
| LangChain benchmark lift (harness only) | +13.7 points, Top 30 → Top 5 |
| ClawHub malicious skills (Feb 2026) | 1,184 confirmed |
| OpenClaw CVEs (2026 YTD) | 16 tracked, 9 critical unpatched |
| Avg. premium target | $120–300/year |
| 10K agents at blended $200 | $2M GWP |
| Time to first policy | H2 2026 |

---

## Receipts

- LangChain Harness Engineering blog — Feb 17, 2026: https://blog.langchain.com/improving-deep-agents-with-harness-engineering/
- OWASP Top 10 for Agentic Applications — Dec 2025: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- OWASP AI Exchange (ISO/IEC 27090) — Feb 2026: https://owaspai.org
- ClawHavoc campaign — internal vuln DB, Feb 19, 2026
- Causal attestation chain — 18 days PASS, internal ledger
- Full thesis + evidence: HARNESS-THESIS.md

---

*Domain: causal.insure — Stealth mode*
*Updated: Feb 19, 2026*
