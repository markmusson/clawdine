# ClawdSure — Pitch Narrative for Greenlight Re

> **Audience:** Sam Clifton, Greenlight Re. Reinsurance capacity + investment capital.
> **Setting:** Lunch at Olympic Studios, Barnes. Informal. 10-minute story, then conversation.
> **Goal:** Design partner commitment. Greenlight provides capacity, ClawdSure provides the risk model.

---

## The Story (10 minutes)

### 1. The Problem (2 min)

There are now more AI agents running unsupervised than there are people managing them.

Every company deploying AI agents — from startups with a single bot to enterprises with hundreds — is running uninsured. Not because they don't want insurance, but because nobody knows how to underwrite it. The agents have root access, API keys, can send emails, move money, deploy code. When something goes wrong — and it does, daily — there's no safety net.

This isn't theoretical. Two weeks ago, a supply chain attack hit the largest AI agent skill marketplace. Top downloaded skill was a malware delivery vehicle. Fake dependency, staging page, obfuscated payload, binary download with quarantine stripping. Thousands of agents potentially compromised. No insurance policy on the planet covers that today.

The market for AI agent operations is growing exponentially. The market for AI agent insurance is zero. That gap is the opportunity.

### 2. Why Insurance Can't Underwrite This Today (1 min)

Traditional cyber insurance relies on questionnaires. "Do you have a firewall? Do you patch regularly?" Self-reported, verified annually, gamed constantly. The loss ratios in cyber are already terrible because the data is garbage.

AI agents are worse. They change configuration daily. They install new capabilities. They operate autonomously. A questionnaire from January is worthless by February. There's no telematics. No continuous signal. No way to distinguish a hardened agent from a compromised one.

Without continuous, verifiable risk data, you can't price the risk. And if you can't price it, you can't insure it.

### 3. ClawdSure: Telematics for AI Agents (3 min)

We built the telematics box.

Think of it like the black box in a car — the one that proved you weren't speeding when someone hit you. Except it's for AI agents, and it runs continuously.

**How it works:**

Every day, the agent runs a security audit — 19 automated checks across filesystem permissions, network exposure, firewall status, skill integrity, sandbox configuration. The results get cryptographically signed with the agent's private key, hash-linked to the previous day's attestation, and published to an immutable ledger.

The chain is tamper-evident. Modify any entry and every subsequent hash breaks. Miss a day and there's a 48-hour grace period. Miss two days and the chain breaks. The chain is the evidence.

**What this gives an underwriter:**

- Continuous, machine-verified security posture — not self-reported, not annual
- Tamper-evident audit trail — can't fake a clean record after an incident
- Real-time risk signal — config drift, new vulnerabilities, chain gaps all visible
- Claims verification — was the agent hardened at the time of the incident? Check the chain.

This is the data layer that makes AI agent insurance possible.

### 4. The Product (2 min)

**For agent operators:**
- Install ClawdSure (one command)
- Daily attestation runs automatically
- Maintain an unbroken chain → qualify for coverage
- Incident happens → file claim → chain verified → payout

**For underwriters (Greenlight Re):**
- Continuous risk data per agent, per day
- Actuarial signal that improves with every attestation
- Portfolio-level view across all insured agents
- Parametric-style payout: chain intact at incident time = valid claim. No claims adjusters, no ambiguity.

**Coverage tiers (initial):**
- Basic: $500 incident coverage, $10/month
- Pro: $2,500 coverage, $25/month
- Enterprise: custom limits, custom pricing

At even 10,000 agents (a fraction of the market), that's $1.2M-$3M annual premium at basic/pro mix. The market is growing 10x year-over-year.

### 5. Why Greenlight Re (1 min)

We don't want to build an insurance company. We want to build the risk intelligence layer and partner with someone who knows how to deploy capacity.

Greenlight Re is the right partner because:

1. **You understand new risk pools.** This isn't another cyber product — it's a new asset class. AI agent operational risk doesn't fit neatly into existing cyber policies. It needs fresh thinking.

2. **Capacity + capital.** We need reinsurance capacity to backstop the product and investment to build the platform. Greenlight does both.

3. **Speed.** The window is open now. Every month without an insurance product is a month where the market is training itself that AI agents are uninsurable. First mover sets the standard.

### 6. What We're Asking For (1 min)

**Design partnership.** Work together on:
- Loss model calibration (we have the data, you have the actuarial expertise)
- Coverage structure and exclusions
- Capacity commitment for launch
- Optional: seed investment to accelerate platform build

**Timeline:**
- Relay API (attestation infrastructure): live this month
- Verification dashboard: March
- First policies bound: Q2 2026
- We've been running our own attestation chain for 10 days. All PASS. The system works.

---

## Objection Handling

**"The market is too early."**
That's exactly why you want to be in now. The data advantage compounds. Every attestation we collect makes the loss model better. By the time the market is "ready," the early mover has 12 months of actuarial data nobody else has.

**"How do you prevent agents from gaming the attestation?"**
The audit checks are machine-verified, not self-reported. Filesystem permissions are measured, not declared. The chain is cryptographically signed — you'd need the private key to forge an entry, and the private key never leaves the host. Config drift is detected automatically via hash fingerprinting.

**"What's the loss model based on?"**
Initially: the ClawHub supply chain audit (60%+ of marketplace skills had suspicious patterns), public AI incident data, and our own attestation history. The model improves with every policy — we're collecting the training data as we insure. This is the cold-start advantage.

**"Isn't this just cyber insurance?"**
No. Cyber insurance covers data breaches, ransomware, business interruption from network events. AI agent risk is operational — the agent itself causes the damage. It deploys bad code, sends unauthorized communications, leaks credentials, makes bad trades. The risk surface is fundamentally different. The telematics approach is different. The payout model is different.

**"Why not just improve agent security instead of insuring the failures?"**
Both. The attestation chain incentivises better security (you need a PASS to maintain coverage). The insurance covers residual risk that security alone can't eliminate. This is the same model as auto insurance — seatbelts and airbags reduce accidents, insurance covers the ones that still happen.

**"What about regulatory?"**
Parametric insurance has established regulatory frameworks. We're not inventing a new insurance structure — we're applying an existing one (parametric triggers) to a new risk class (AI agent operations). The attestation chain is the trigger mechanism. Greenlight Re's regulatory infrastructure handles the rest.

---

## Key Numbers

| Metric | Value |
|--------|-------|
| AI agents in production (est. 2026) | 500K-2M+ |
| Current insurance coverage for AI agents | ~0 |
| ClawdSure attestation chain | 10 days, all PASS |
| Avg. premium (basic) | $120/year |
| Avg. premium (pro) | $300/year |
| 10K agents at blended $200/year | $2M GWP |
| 100K agents | $20M GWP |
| ClawHub marketplace attack | Feb 5, 2026 — validated thesis |
| Time to first policy (est.) | Q2 2026 |

## Mark's Unfair Advantage

- Built and sold a dynamic motor pricing MGA to AON (£40m GWP) — knows the insurance value chain cold
- Ran a data science team at an insurer — built the actuarial models
- Running an AI agent himself (Clawdine) — built ClawdSure to insure his own agent first
- "Dogfooding" — the attestation chain was built because he needed it, not because he thought it would sell
- Deep understanding of both sides: insurance underwriting AND AI agent operations
- Almost nobody else on the planet has both

---

*Draft v1. Mark to review, tear apart, and tighten. The story should feel like a conversation, not a deck.*
