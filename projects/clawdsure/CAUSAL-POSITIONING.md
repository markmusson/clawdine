# Causal.insure — Underwriter Positioning Brief

**Date:** Feb 17, 2026
**For:** Greenlight Re / S3456 conversation
**Context:** Positioning Causal as the SME/personal agent segment complement to existing AI insurance products

---

## The Market Gap

### What Exists (Enterprise AI Insurance)

| Product | Insured | Coverage Trigger | Severity Basis | Limit |
|---------|---------|------------------|----------------|-------|
| **Armilla Guaranteed** | AI model vendor | KPI breach | License fee refund | Vendor revenue |
| **Armilla AI Liability** | AI deployer (enterprise) | Output harm | Third-party loss | $25m |
| **AIUC** | AI agent vendor | Agent harm | Customer loss | TBD |
| **Munich Re aiSure** | AI model vendor | Prediction error | Vendor loss | Model value |
| **Vanguard AI** | Enterprise | Mixed cyber/AI | Allocated | $25m AI + $10m cyber |

**Common thread:** These products insure AI **builders** and **enterprise deployers**. The underwriting signal is point-in-time model evaluation (Armilla: "500+ AI evaluations"). The loss trigger is model performance or output error.

### What Doesn't Exist (SME Agent Operator Insurance)

The explosion of personal and SME AI agents (OpenClaw: 135,000+ instances) creates a new risk population:

- **Not building models** — using off-the-shelf LLMs
- **Not enterprise** — 1-50 employees, <$5m revenue
- **Operational risk, not model risk** — agent misconfiguration, data leak, unauthorized action, escalation failure
- **Continuous exposure** — agents run 24/7, not invoked per-transaction

**No product addresses this segment.** Armilla's $25m limits and enterprise pricing don't fit a 5-person agency running an OpenClaw instance.

---

## Causal's Position

### The Segment

**SME Agent Operators:**
- Solopreneurs and small businesses deploying AI agents for operations
- Revenue: $100k–$5m
- Agents: 1–10 active instances
- Use cases: customer service, scheduling, research, workflow automation
- Not building AI — **operating** AI

**Previously mapped ICP (from your SME work):**
- Agencies, consultancies, professional services
- E-commerce operators with AI customer support
- Startups with AI-assisted ops (fundraising, sales, support)
- Freelancers with "AI employees"

### The Product

**Agent Operational Liability** — coverage for losses arising from AI agent operation, not model performance.

| Element | Specification |
|---------|---------------|
| **Insured** | Agent operator (the SME running the agent) |
| **Coverage Trigger** | Operational failure: unauthorized action, data exposure, misconfiguration, escalation failure |
| **Severity Basis** | Remediation cost + limited third-party liability |
| **Limit Range** | $10k–$250k (SME-appropriate) |
| **Premium Range** | $50–$500/month (comparable to SME cyber) |
| **Rate Basis** | Agents × scope × attestation grade |

### The Underwriting Signal: Attestation

**Armilla's signal:** Point-in-time model evaluation → risk score → price.

**Causal's signal:** Continuous operational attestation → live risk profile → dynamic pricing.

The **ClawdSure attestation chain** provides:

| Signal | Underwriting Use | Analogous To |
|--------|------------------|--------------|
| **Machine fingerprint** | Identity/integrity of insured system | Fleet telematics device ID |
| **Config hash** | Change detection, drift monitoring | MLOps audit trail |
| **Daily attestation** | Continuous compliance proof | Telematics heartbeat |
| **IPFS publication** | Tamper-evident record | Blockchain audit |
| **Human-in-the-loop gates** | Escalation controls | Cure period / intervention |

**Key insight for underwriters:** This is **telematics for AI agents**. Same principle as motor: continuous telemetry → better risk selection → lower loss ratio → competitive pricing.

---

## Underwriter Language (How to Frame It)

### Frame 1: Cyber Extension

"This is a **cyber policy extension** for AI agent operational risk. The same SME that buys $1m cyber coverage now has 3 AI agents running 24/7. Their cyber policy covers data breach from hacking. What covers data breach from agent misconfiguration? Causal."

**Familiar concepts:**
- Sublimit for AI-specific perils
- Attestation requirement = security questionnaire equivalent
- Continuous monitoring = MFA/EDR requirement equivalent

### Frame 2: Tech E&O for Agent Operators

"Tech E&O covers professional mistakes. But traditional E&O assumes human-in-the-loop. When an AI agent autonomously executes a flawed recommendation, whose E&O responds? Causal provides affirmative agent E&O for the operator, not the model vendor."

**Familiar concepts:**
- Prior acts date → attestation start date
- Claims-made trigger
- Retroactive coverage with continuous attestation

### Frame 3: Embedded Warranty (MKIII Model)

"MKIII embeds Munich Re warranty into their lending product. Causal embeds coverage into the OpenClaw ecosystem. Agent operators get attestation + coverage as a package. Distribution is built into the platform."

**Familiar concepts:**
- Embedded insurance via platform
- Per-seat or per-agent pricing
- Automated underwriting via attestation grade

---

## Pricing Framework

### Rate Basis Options

| Basis | Advantages | Challenges |
|-------|------------|------------|
| **Per agent per month** | Simple, usage-aligned | Varies by agent scope |
| **Revenue band** | Familiar to E&O underwriters | Doesn't capture agent intensity |
| **Agent-hours × scope** | Precise exposure measure | Requires telemetry |
| **Attestation score** | Risk-differentiated | Needs scoring model |

**Recommended:** Hybrid of revenue band + agent count + attestation modifier.

### Illustrative Premium Schedule

| Revenue | Agents | Attestation | Annual Premium |
|---------|--------|-------------|----------------|
| <$500k | 1–2 | Standard | $600 |
| <$500k | 1–2 | Verified | $400 |
| $500k–$2m | 3–5 | Standard | $1,800 |
| $500k–$2m | 3–5 | Verified | $1,200 |
| $2m–$5m | 5–10 | Standard | $4,000 |
| $2m–$5m | 5–10 | Verified | $2,800 |

**"Verified" = continuous attestation with ClawdSure chain** — 30% premium credit for telemetry.

### Benchmark Comparison

| Product | SME Premium | Limit |
|---------|-------------|-------|
| SME Cyber (market) | $1,000–$5,000/year | $1m |
| Tech E&O (market) | $500–$1,000/employee/year | $1m |
| **Causal (proposed)** | $400–$4,000/year | $10k–$250k |

Causal sits below cyber/E&O in limit and premium — it's the **first-dollar coverage for agent-specific operational risk**.

---

## Exclusions Framework

**Affirmative coverage for:**
- Agent operational errors (misconfiguration, wrong action, escalation failure)
- Data exposure from agent malfunction (not breach)
- Third-party claims from agent output (defamation, misinformation)
- Regulatory investigation costs (AI Act, state AI laws)

**Exclusions (standard market language):**
- Intentional/criminal acts
- Known defects at inception
- Model performance (Armilla's territory)
- Cyber events (separate tower)
- Bodily injury / property damage (GL territory)
- Employment practices (EPLI territory)

---

## Accumulation Control

**The problem:** One agent framework (OpenClaw) deployed across thousands of SMEs. Systemic vulnerability = correlated loss.

**Armilla/Vanguard's approach:** Allocation rules, dedicated aggregates, carve-outs.

**Causal's approach:**

1. **Attestation diversity** — each insured has unique machine fingerprint, config hash. No two attestation chains are identical.

2. **No shared model risk** — Causal insures agent *operation*, not the underlying LLM. The LLM vendor's liability is upstream.

3. **Correlation monitoring** — attestation chain detects if multiple insureds are affected by same vulnerability (e.g., OpenClaw CVE). Triggers portfolio-level response.

4. **Aggregate limits** — programme-level aggregate protects against black swan.

**Key message:** Single-tenant attestation means losses are *operationally independent* even if agents share a platform.

---

## Competitive Landscape

| Competitor | Segment | Causal Differentiation |
|------------|---------|------------------------|
| **Armilla** | Enterprise AI deployers | Causal: SME segment, operational (not model) risk |
| **AIUC** | AI agent vendors | Causal: agent operators, not vendors |
| **Vanguard AI** | Enterprise cyber/AI | Causal: standalone SME product, not bundle |
| **Munich Re aiSure** | AI model vendors | Causal: operators, not model builders |

**Causal's moat:** Attestation infrastructure embedded in the largest open-source agent ecosystem (OpenClaw). Distribution + underwriting signal in one.

---

## Path to Market

### Option A: Greenlight S3456 Binder

- Causal as **coverholder / MGA**
- Greenlight provides capacity via S3456
- Product: "Agent Operational Liability" delegated authority
- Distribution: embedded in OpenClaw, direct SME sales

**Fit with S3456:**
- Innovation syndicate mandate ✓
- Insurtech partnership model ✓
- Novel risk class ✓
- £51m capacity sufficient for SME book ✓

### Option B: Facility with Daren's Entity

- Daren's regulated entity provides fronting / delegated authority
- Greenlight as reinsurer on excess layer
- Faster to market (existing regulatory wrapper)

### Option C: Hybrid

- Daren for UK/EU regulatory execution
- Greenlight S3456 for US surplus lines
- Reinsurance treaty ties them together

---

## What We Need from Greenlight

1. **Indication of interest** in SME agent segment
2. **Appetite guidance** — limits, classes, excluded use cases
3. **Technical underwriting input** — attestation as rating factor, minimum controls
4. **Capacity indication** — line size, aggregate

---

## The Pitch (One-Liner)

> "Armilla insures AI model builders. AIUC insures AI agent vendors. Causal insures the 135,000 SMEs **operating** AI agents today — with continuous attestation that gives you underwriting signal you can't get anywhere else."

---

*Prepared by Clawdine for Mark Musson, Causal.insure / ClawdSure*
