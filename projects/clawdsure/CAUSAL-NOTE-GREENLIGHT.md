# Causal.insure — Market Note

**February 2026**

---

## The Emerging AI Agent Insurance Market

The AI insurance landscape is consolidating around a clear structure:

**Model Performance Warranties** — Munich Re's aiSure and Armilla Guaranteed provide insurance-backed warranties for AI model vendors. Coverage triggers on KPI breach; severity is capped by license fees or pre-agreed remedies. Underwriting is driven by point-in-time model evaluation (accuracy, fairness, robustness, drift risk). Greenlight Re participates via S3456 on the Armilla warranty product.

**AI Liability (Third-Party)** — Armilla's standalone AI liability product, led by Chaucer on Syndicate 1084, provides affirmative coverage for AI output errors, hallucinations, agent failures, and regulatory violations. Limits to $25m per organisation. Vanguard AI (Feb 2026) coordinates this with cyber/tech E&O via predefined allocation rules.

**Agent Vendor Insurance** — AIUC (emerged from stealth July 2025, $15m seed led by Nat Friedman) is building insurance and certification infrastructure for AI agent vendors. Their AIUC-1 framework combines NIST, EU AI Act, and MITRE ATLAS into an auditable agent safety standard. Target: enterprises deploying third-party AI agents.

**Common characteristics:**
- Enterprise-focused ($25m limits, bespoke underwriting)
- Model builder or agent vendor as insured
- Point-in-time evaluation as underwriting signal
- Coverage triggered by model/output failure

---

## The Unaddressed Segment: SME Agent Operators

The proliferation of open-source AI agent frameworks (OpenClaw alone has 135,000+ deployed instances) has created a new risk population that existing products don't serve:

| Characteristic | Enterprise AI Deployer | SME Agent Operator |
|----------------|------------------------|-------------------|
| Revenue | >$10m | $100k–$5m |
| AI relationship | Builds or licenses models | Operates off-the-shelf agents |
| Risk type | Model performance, output liability | Operational: misconfiguration, data exposure, escalation failure |
| Appropriate limit | $1m–$25m | $10k–$250k |
| Appropriate premium | $10k–$100k+ | $400–$4,000/year |
| Underwriting signal | Model evaluation | Operational telemetry |

**This segment is currently uninsured.** Armilla's pricing and limits don't fit a 5-person agency. AIUC targets vendors, not operators. Traditional cyber/E&O doesn't affirmatively cover agent-specific operational failures.

---

## Causal: Agent Operational Liability for SMEs

Causal provides coverage for losses arising from AI agent **operation**, distinct from model performance or vendor liability.

**Product structure:**
- **Insured:** SME operating AI agents (not building, not vendoring)
- **Coverage:** Operational failures — unauthorised agent actions, data exposure from misconfiguration, escalation failures, third-party claims from agent output
- **Limits:** $10k–$250k (first-dollar coverage below cyber/E&O towers)
- **Premium:** $400–$4,000/year, based on revenue band × agent count × attestation grade

**Underwriting signal: Continuous attestation**

Where Armilla uses point-in-time model evaluation, Causal uses continuous operational telemetry via an attestation chain:

| Signal | Function |
|--------|----------|
| Machine fingerprint | Unique identity of insured system |
| Configuration hash | Drift detection, change monitoring |
| Daily attestation | Continuous compliance proof |
| Cryptographic chain | Tamper-evident audit trail |
| Human-in-the-loop gates | Escalation controls (analogous to cure periods) |

This is **telematics for AI agents**. The same principle that transformed motor underwriting — continuous telemetry enables better risk selection, lower loss ratios, and pricing that rewards good operational hygiene.

**Attestation-linked pricing:**
- Standard rate: base premium
- Verified (continuous attestation): 30% credit

---

## Distribution & Accumulation

**Embedded distribution:** Causal's attestation infrastructure is integrated into the OpenClaw ecosystem. Coverage can be offered at point of agent deployment — embedded insurance at platform level, similar to how MKIII embeds Munich Re warranty into lending products.

**Accumulation control:** Unlike model-level risk (where one model version deployed across thousands of clients creates correlated exposure), agent operational risk is tenant-specific. Each insured has a unique attestation chain — machine fingerprint, configuration, operational history. Losses from operator error are independent even when agents share a platform.

Systemic vulnerability (e.g., platform CVE) is monitored via attestation chain correlation and managed through programme-level aggregates.

---

## Market Sizing

- **OpenClaw deployments:** 135,000+ (Feb 2026)
- **SME segment (est.):** 60–70% of deployments
- **Addressable population:** ~80,000–95,000 SME agent operators
- **At $1,500 average premium:** $120m–$140m addressable GWP
- **Growth:** Agent adoption doubling every 6 months; AIUC projects $500bn AI insurance market by 2030

---

## Capacity Requirements

| Element | Specification |
|---------|---------------|
| Per-risk limit | $10k–$250k |
| Programme aggregate | $5m–$10m (year 1) |
| Classes | Tech E&O / Miscellaneous |
| Territory | US, UK, EU |
| Distribution | Delegated authority via MGA |

---

## Summary

The AI insurance market has products for model builders (aiSure, Armilla Guaranteed) and enterprise deployers (Armilla Liability, AIUC, Vanguard AI). 

**Causal addresses the missing segment:** SME agent operators — the tens of thousands of small businesses now running AI agents 24/7 with no coverage for operational failures.

The underwriting innovation is continuous attestation — real-time operational telemetry that provides risk signal no point-in-time evaluation can match.

The distribution advantage is platform integration — coverage embedded where agents are deployed.

---

*Causal.insure — Coverage for the age of autonomous agents*
