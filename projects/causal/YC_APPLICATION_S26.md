# YC S26 Application — Causal (causal.insure)
*Drafted: 2026-02-22 | Status: Draft v2 — revised per founder corrections*

---

## STRATEGIC NOTE

Causal is positioned at the intersection of two YC S26 RFS themes:
- **AI infrastructure** — the missing trust layer for enterprise agent deployment
- **Financial primitives** — parametric insurance as a new product category enabled by continuous AI state verification

**Positioning:** Causal is a **tech-enabled full-stack MGA** — not an attestation SaaS vendor selling to insurers. The attestation protocol is proprietary technology that enables superior AI underwriting; the insurance product is what we sell. This is the same model as Humn (telematics-native MGA) applied to AI agents. The founder built exactly this model before and sold it to AON.

---

## COMPLETE YC APPLICATION

---

### COMPANY

**Company name:**
```
Causal
```

**Describe what your company does in 50 characters or less:**
```
The tech-enabled MGA that insures AI agents
```

**Describe what you're building in 1 sentence (150 chars):**

> Causal is a parametric MGA for AI agents — we underwrite agentic deployments using our own cryptographic attestation protocol instead of one-time red-team assessments.

*(168 chars — trim to:)*

> We underwrite AI agent deployments using cryptographic state attestation — parametric coverage that triggers on verifiable configuration drift, not incident reports.

*(165 chars — tighten to:)*

> Causal insures AI agents with parametric policies backed by our own continuous cryptographic attestation protocol — not static assessments.

*(139 chars ✓)*

---

**What is your company going to make?**

AI agents are making material decisions in enterprise workflows — loan approvals, insurance claims, legal drafting, customer service — and nobody can insure them properly. Not because insurers don't want to, but because they have no underwriting signal. Armilla and Lloyd's syndicates are issuing AI liability coverage based on one-time red-team assessments. The problem: agents drift. Model versions change, system prompts evolve, guardrails get silently removed. A static assessment is out of date before the ink dries.

Causal is a tech-enabled full-stack MGA. We have built our own proprietary attestation protocol — a cryptographic black box that runs alongside any AI agent deployment and produces a continuous, tamper-evident, chain-linked record of harness configuration state. Every attestation captures: model identifier, prompt version hashes, tool definitions, guardrail configurations, and memory backend state — hashed, signed, chain-linked to the prior record, and published to IPFS. Retroactive modification is cryptographically detectable.

This attestation chain is our proprietary underwriting data. We use it to issue parametric AI agent policies with automatic triggers: if a claim occurs and the harness configuration matches the declared, attested state, coverage applies. If configuration has drifted from the declared state, the trigger conditions are clear. We price risk dynamically based on live attestation data rather than static snapshots.

The product is the insurance. The attestation is the technology that makes our underwriting better than anyone else's.

---

**Why did you pick this idea?**

I built and sold a by-the-second dynamic motor pricing MGA to AON at £40m GWP. That business was built on the same principle: telematics as proprietary underwriting signal, enabling parametric products that incumbents couldn't offer because they lacked continuous behavioural data. We didn't sell telematics software to insurers — we were the insurer, using our own data to price risk better than anyone else.

When I saw Lloyd's syndicates trying to build parametric AI products in 2025, I recognised the pattern immediately. They want to offer AI agent coverage but have no continuous signal — only static assessments that go stale. Armilla is doing exactly what the old-school motor insurers were doing before telematics: underwriting on declarations and occasional inspections. I built the solution to that problem in motor. Causal applies the same model to AI.

I confirmed the market need with Lloyd's underwriters directly. The consistent answer: "We want parametric AI triggers but we have no continuous signal — one-time assessments aren't sufficient for dynamic systems." That's the same conversation I had with motor insurers in 2012. I know what comes next.

---

### TRACTION

**How far along are you?**

Attestation protocol in production. We have run 21 consecutive daily attestations on a live AI agent deployment — publicly verifiable at causal.insure/chain. The cryptographic mechanism works: machine fingerprint, config hashes, chain signatures, IPFS publication. Tampering with any historical record invalidates the entire subsequent chain.

The protocol is the hard part. The MGA infrastructure — policy wording, capacity, coverholder authority — is the next phase. Two Lloyd's-market underwriters are in active pilot conversations. Neither currently has a continuous AI signal; both are building parametric products that require one.

**How many users / customers?**

Two Lloyd's pilot LOIs. Zero revenue for Causal. Pre-revenue at application; the MGA licence and first policies are the immediate next milestone.

---

### MARKET

**Who are your competitors and what do you do better?**

**Armilla AI** (Lloyd's Lab, Swiss Re, Chaucer backing): The leading AI insurer. They underwrite on one-time red-team assessments — a static snapshot of the system at a point in time. Their testimonials describe "third-party certification." No continuous signal. When a model version changes or a guardrail is removed post-assessment, their coverage is based on a configuration that no longer exists. They are doing AI insurance the way motor insurers did pricing before telematics existed.

Causal's underwriting data is continuous and proprietary. We know the current state of every insured deployment at all times. Our parametric triggers are automatic and verifiable. Armilla's are manual and retrospective. Different architecture, not incremental improvement.

**Monitoring/observability platforms** (LangSmith, Langfuse, Datadog AI): Record what agents *do*, not what was *running* when they did it. Behaviour logs are not harness state records. An operator can swap a model version, change a system prompt, remove a guardrail — the monitoring platform records outputs, not configuration. We record state. The distinction matters enormously for underwriting.

**No competitor has continuous cryptographic attestation of AI agent harness state.** Confirmed directly by both Lloyd's underwriters we spoke to.

**How big is this market?**

The analogy is usage-based motor insurance. When telematics became the underwriting signal for motor, it didn't just improve existing products — it created an entirely new category (pay-as-you-drive, young driver policies, parametric pricing) that incumbents couldn't offer. Total UK telematics motor premium is now ~£1B annually.

AI agent deployments in enterprise are approximately where motor was in 2010 — entering production, inadequately insured, with regulators beginning to mandate auditability. The EU AI Act's Article 9 obligations for high-risk AI systems come into force August 2026. Every AI agent deployment in financial services, healthcare, legal, and government is a potential insured.

Addressable market: Global cyber and tech E&O premium is ~$15B annually; AI-specific parametric coverage is nascent. Even 1% of global enterprise AI deployments becoming insureds through our MGA represents hundreds of millions in GWP. The Lloyd's market for AI coverage will be measured in billions within five years. We intend to be the MGA that writes a significant portion of it on the back of superior underwriting data.

**Why is now the right time?**

1. AI agents entered enterprise production in 2024-2025. The stakes of configuration errors are now material — the first AI agent insurance claims have begun appearing.
2. EU AI Act Article 9 enforcement begins August 2026. Enterprises need auditability infrastructure now.
3. Lloyd's syndicates are actively building parametric AI products but lack the underwriting signal to launch them. We have spoken to two; both said they are waiting for exactly this capability.
4. The attestation gap is open. Monitoring platforms grew fast (LangSmith, Langfuse) but focused on observability. AI insurers grew fast (Armilla) but focused on static assessments. The continuous attestation layer is still open. In six months it won't be.

---

### FOUNDERS

**Tell us about the founders.**

**Mark Musson — Founder & CEO**

Built a dynamic by-the-second motor pricing MGA from zero to £40m GWP and sold it to AON. The business was a full-stack, tech-enabled MGA — proprietary telematics data, proprietary pricing algorithms, our own underwriting authority. Not a software vendor selling to insurers; we were the insurer, using technology to underwrite better than anyone else. That is exactly the Causal model applied to AI agents.

After the exit: joined the insurer as head of data science. Designed and built statistical loss models for commercial lines underwriting. Understands the underwriter's perspective from the inside — what signal they need, what triggers they will write into policy wording, what verification they require for parametric claims.

Deep cross-domain expertise that is rare in the market: insurance underwriting architecture, parametric product design, AI/ML systems, regulatory navigation (FCA regulated business), and successful company building with exit to a global broker. The specific combination — telematics-based MGA founder + insurance data science + AI systems — does not exist elsewhere in the AI insurance space.

Mark is a solo founder building a team, not seeking a forced co-founder pairing. The prior company was built with a team assembled after founding. Founder breakup is one of the primary startup failure modes; experience and deliberate team construction mitigates this better than convenience co-founding.

**Why is this team uniquely positioned?**

The incumbents in AI insurance (Armilla) come from AI safety and cyber insurance backgrounds. They understand AI risk in the abstract but have not built a telematics-based MGA. They do not know what it takes to design a parametric trigger that is actually executable and not just theoretically sound.

Mark has designed executable parametric pricing in motor. He knows the exact questions a Lloyd's underwriter will ask about the attestation protocol — because he has been on both sides of that conversation. He knows what the policy wording needs to say for the trigger to hold up to a claims challenge. He knows the regulatory path for MGA authority.

This is not a technology founder who discovered insurance. This is an insurance founder who built the technology.

---

### VISION

**What's the unfair advantage?**

Three moats in order of defensibility:

1. **Founder domain moat**: The specific combination — telematics MGA exit, insurance data science, AI systems — is not replicable quickly. Nobody else in the AI insurance space has built a parametric MGA and run its data science function. This is the moat that matters at the start.

2. **Proprietary attestation data**: Every insured deployment generates attestation data that informs our underwriting model. As the corpus grows, our loss models become more accurate than any competitor's. Network effects compound — more insureds means better models means better pricing means more insureds. This is the same data flywheel telematics insurers built in motor.

3. **Mandate creation**: If we secure the Lloyd's pilots and our attestation becomes the standard signal referenced in parametric AI policy wording, we become mandated infrastructure. The enterprise AI team doesn't buy our attestation because they want to — they buy it because their insurance requires it. This is the same dynamic as telematics boxes in UK young driver motor insurance.

**How does Causal become a large company?**

Year 1: Close Lloyd's pilots. Obtain coverholder authority. Write first parametric AI agent policies. Build the attestation SaaS layer for enterprise AI teams who need the protocol independently of insurance. First MRR target: £50k/month (combined SaaS + premium participation).

Year 2: Expand to US market (NIST AI RMF alignment, SEC/FINRA regulated AI deployments). Establish attestation protocol as referenced standard in Lloyd's parametric AI policy wording. Land in three regulated verticals: financial services, healthcare, legal.

Year 3: Protocol standardisation. Work with standards bodies (NIST, OWASP) to formalise the cryptographic attestation spec. If we own the spec, every compliant tool references us. Revenue evolves: MGA premium → protocol licensing → compliance infrastructure.

At scale: the same way telematics redrew motor insurance — new entrants with better data winning share from incumbents writing blind — Causal redraws AI insurance. We write parametric policies that incumbents cannot write because they lack the underwriting signal. The compounding data advantage makes this durable.

**If this works, what does the world look like?**

Every enterprise AI deployment has an attestation chain — a verifiable, cryptographically signed record of what was running at every moment. When an AI agent causes a material error, "was the system operating as declared?" is a binary, verifiable question. Parametric claims settle automatically. Regulators audit AI systems without forensic investigations. Enterprises deploy AI agents with underwritten coverage, not hope.

The current situation — AI agents making material decisions with no verifiable configuration provenance — is remembered the same way we remember pre-seatbelt car design. Obviously dangerous in hindsight. The mechanism to fix it existed. Someone built it.

---

**How will you make money?**

1. **MGA premium participation**: We write parametric AI agent policies as the MGA/coverholder, participating in premium. Target: 10-15% MGA commission on GWP. At £10m GWP (achievable within 3 years given the motor precedent), this is £1-1.5m annually. Scales with GWP.

2. **Attestation SaaS**: Monthly recurring fee for enterprise AI teams who purchase the attestation service independently of insurance (compliance, EU AI Act, NIST alignment). Target: £2,000-£8,000/month per deployment. Smaller at launch but high-margin.

3. **Compliance reporting**: Annual attestation reports for EU AI Act Article 9, NIST AI RMF, SOC-2-equivalent AI audits. £5,000-£20,000 per annual report package.

The MGA premium channel is the large revenue line. The SaaS and compliance products provide early cash flow and prove the attestation value before policy wording is finalised.

---

## ⚠️ WEAKNESS FLAGS — 2 THINGS TO STRENGTHEN BEFORE SUBMISSION

### WEAKNESS 1 (HIGH): No Revenue, No Paying Customers

**The problem:** Zero revenue for Causal. Two pilot LOIs are promising but YC partners will want at least one paying customer or a specific, imminent path to first revenue.

**How to strengthen:**
- Convert one Lloyd's LOI to a paid POC before submission — even £500/month for access to the attestation API while they build the product. First cash changes the narrative entirely.
- Alternatively: find one enterprise AI team who will pay for attestation coverage for their compliance obligations (EU AI Act). £1,000/month for the attestation service with a compliance report. This is independently sellable before the MGA authority is in place.
- If neither is possible: be maximally specific about the Lloyd's conversations. Name the syndicates if permitted. Quote what they said. Give the timeline for when they need the signal and what "active pilot" means in concrete terms.

---

### WEAKNESS 2 (MEDIUM): Technical Explanation Risks Losing Non-Technical Partners

**The problem:** "Chain-linked signatures, IPFS publication, tamper-evident config hashes" — accurate but may read as jargon to a non-specialist YC partner.

**How to strengthen:**
- Add the lay explanation: "Each day, we take a cryptographic fingerprint of the AI agent's full configuration — every setting, every prompt, every tool. We sign it with a private key, then include yesterday's signature in today's fingerprint. This means changing any historical record breaks every subsequent record — the same principle as a blockchain, applied to AI configuration. It's publicly verifiable; anyone can audit any historical state in seconds."
- Include the live attestation chain link as the demo URL: `causal.insure/chain`. Let the reviewer verify it themselves. This is stronger than any description.
- Optional: 60-second demo video showing (1) what an attestation looks like, (2) what happens when you attempt to tamper with a record, (3) what an insurer sees when a claim comes in.

---

## FOUNDER VIDEO SCRIPT (1 minute)

**0:00–0:20:**
"I'm Mark Musson. I built a by-the-second dynamic motor pricing MGA — full-stack, proprietary telematics data, our own underwriting algorithms — grew it to £40m GWP and sold it to AON. The model: use better data than incumbents to underwrite risk they couldn't touch. I then ran data science at a motor insurer. I know this business from both sides."

**0:20–0:45:**
"When I saw Lloyd's trying to insure AI agents in 2025, I saw the same problem I solved in motor: they're underwriting on declarations and static assessments, not continuous verified data. The telematics box doesn't exist for AI. I built one. Causal runs alongside any AI agent deployment — continuous cryptographic attestation of configuration state, chain-linked, tamper-evident, publicly verifiable. 21 consecutive attestations live now at causal.insure/chain. Two Lloyd's underwriters are piloting it as the signal for parametric AI products they cannot currently launch without it."

**0:45–1:00:**
"This is the same company I built in motor — tech-enabled full-stack MGA, proprietary underwriting data, parametric products incumbents can't match. EU AI Act enforcement is August 2026. The window to become the standard is now. That's Causal."

---

*Draft v2 — 2026-02-22. Corrections applied: full-stack MGA framing, solo founder weakness flag removed, Nightjar removed, prior company described without unverified name.*
