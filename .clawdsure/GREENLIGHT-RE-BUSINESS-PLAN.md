# ClawdSure: Telematics-Based Insurance for AI Agents

**Business Plan for Reinsurance Partnership**

**Prepared for:** Greenlight Re  
**Prepared by:** Kryptoplus Labs (www.krypto.plus)  
**Date:** February 2026  
**Version:** 2.0

---

## Company Overview

**Kryptoplus Labs** builds infrastructure for the autonomous economy:
- **HyperSend**: Casino deposit routing to DeFi yield vaults
- **ClawdSure**: Telematics-based agent breach insurance for AI agents

ClawdSure leverages HyperSend's yield infrastructure to earn 6-12% on premium float via Morpho vaults, dramatically improving unit economics.

---

## Executive Summary

ClawdSure is a telematics-based agent breach insurance product purpose-built for the emerging AI agent economy. We provide automated, continuous security attestation with claims assessed against verified behavioural monitoring.

**The Opportunity:**
- Millions of autonomous AI agents deploying (OpenClaw, AutoGPT, etc.)
- $0 dedicated insurance products for AI agent security
- Traditional breach insurance doesn't fit autonomous systems

**The Product:**
- $50/year premium (USDT), $500 payout
- Continuous security attestation via ClawdSure audit platform
- IPFS-pinned attestation chain (immutable, verifiable)
- Claims assessed against verified attestation history

**The Edge — Yield on Float:**
- Premiums deposited in USDT
- Routed to Morpho vaults via HyperSend (Kryptoplus infrastructure)
- **6-12% APY on premium float**
- Adds $2-4 per policy in investment income

**The Ask:**
- Quota share reinsurance partnership (50% cession)
- $5-10M capacity scaling to $50M+
- Technical collaboration on risk modeling

**Projected Returns:**
- Target loss ratio: 55%
- Investment income: +5-8% of premium
- Combined ratio: 85% (after investment income)
- ROE: 20-25% at scale

---

## Market Opportunity

### The Autonomous Agent Explosion

| Year | Autonomous AI Agents | Growth |
|------|---------------------|--------|
| 2024 | 100K | - |
| 2025 | 500K | 400% |
| 2026 | 2M | 300% |
| 2027 | 5M+ | 150% |
| 2028 | 10M+ | 100% |

*Source: OpenClaw ecosystem data, industry estimates*

**Initial Customer Profile (ICP):** OpenClaw bots
- Autonomous agents with tool access, API credentials, execution capabilities
- Gateway-connected, channel-enabled (Telegram, Discord, WhatsApp)
- Running on user hardware or cloud VPS
- Holding credentials worth protecting

**Expansion targets:** AutoGPT, Claude Computer Use, Devin-style coding agents, trading bots, home automation agents

### The Security Gap

AI agents represent a new attack surface:
- **Autonomous execution**: Agents run code, access APIs, control systems
- **Credential access**: Agents hold API keys, OAuth tokens, service accounts
- **Supply chain risk**: Skills/plugins from third parties
- **Novel attack vectors**: Prompt injection, jailbreaks, tool misuse

**Current insurance options: None.**

Traditional breach insurance:
- Requires human-in-the-loop claims process
- Doesn't understand agent-specific risks
- Can't verify autonomous system compliance
- Pricing based on employee count, not agent risk

### Total Addressable Market

| Segment | Agents (2028) | Penetration | Premium Potential |
|---------|---------------|-------------|-------------------|
| OpenClaw ecosystem | 2M | 25% | $25M |
| Enterprise autonomous | 3M | 15% | $22.5M |
| Prosumer/developer | 5M | 10% | $25M |
| **Total** | **10M** | **15%** | **$72.5M** |

**Serviceable Addressable Market (SAM):** 2M-5M autonomous agents  
**Premium potential:** $100M-$250M at full penetration  
**Year 1 target:** 50,000 policies = $2.5M GWP  
**Year 3 target:** 500,000 policies = $25M GWP

---

## Product Design

### Coverage

| Feature | Specification |
|---------|---------------|
| **Premium** | $50/year (Basic) |
| **Payout** | $500 (assessed) |
| **Eligibility** | Security breach + valid attestation chain at time of incident |
| **Exclusions** | Self-inflicted, chain break, policy violation |

### The Attestation Model

```
┌─────────────────────────────────────────────────────────┐
│                    AGENT HOST                           │
│  ┌──────────────┐      ┌──────────────┐                │
│  │ ClawdStrike  │ ──→  │ Attestation  │                │
│  │   (Audit)    │      │   (Signed)   │                │
│  └──────────────┘      └──────┬───────┘                │
└────────────────────────────────┼────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────┐
│                      IPFS                               │
│         Content-addressed, immutable storage            │
│              CID: bafybei...                            │
└────────────────────────────────┬────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────┐
│                 CLAWDSURE ORACLE                        │
│    • Verifies attestation signatures                    │
│    • Monitors chain continuity                          │
│    • Processes claims automatically                     │
└─────────────────────────────────────────────────────────┘
```

### Why Telematics-Based?

| Traditional | Telematics-Based (ClawdSure) |
|-------------|------------------------------|
| Claims adjusters required | Automated oracle verification |
| Weeks to settle | Fast assessment with verified data |
| Subjective assessment | Objective criteria (chain + breach) |
| High admin cost | Near-zero marginal cost |
| Adverse selection | Selection via attestation |
| No behavioural data | Continuous monitoring like motor telematics |

---

## The HyperSend Advantage: Yield on Float

### Premium Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     PREMIUM COLLECTION                          │
│                                                                 │
│   Agent pays $50 USDT                                          │
│         │                                                       │
│         ▼                                                       │
│   ┌─────────────┐                                              │
│   │  HyperSend  │ ──→ Routes to Morpho Vaults                  │
│   │   Router    │                                              │
│   └─────────────┘                                              │
│         │                                                       │
│         ▼                                                       │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │              MORPHO VAULTS (6-12% APY)                  │  │
│   │   USDT lending markets, risk-managed, liquid            │  │
│   └─────────────────────────────────────────────────────────┘  │
│         │                                                       │
│         ▼                                                       │
│   Yield accrues to ClawdSure reserve                           │
│   Claims paid from vault (instant USDT)                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Float Economics

| Metric | Value |
|--------|-------|
| Average premium duration | 12 months |
| Average float per policy | $25 (half-year weighted) |
| Morpho vault APY | 6-12% (use 9% midpoint) |
| **Yield per policy** | **$2.25/year** |
| Yield as % of premium | **4.5%** |

### Impact on Unit Economics

| Metric | Without Yield | With Yield | Improvement |
|--------|---------------|------------|-------------|
| Premium | $50 | $50 | - |
| Investment income | $0 | $2.25 | +$2.25 |
| **Effective premium** | **$50** | **$52.25** | **+4.5%** |
| Loss ratio (claims $27.50) | 55% | 52.6% | -2.4pts |
| Combined ratio | 95% | 90% | -5pts |

### At Scale (1M policies)

| Metric | Value |
|--------|-------|
| Total premium | $50M |
| Average float | $25M |
| Annual yield (9%) | **$2.25M** |
| Effective loss ratio improvement | 4.5 points |

**The yield transforms marginal underwriting into highly profitable float business.**

### HyperSend Integration

HyperSend is Kryptoplus Labs' existing infrastructure:
- Battle-tested with casino deposit routing
- Direct integration with Morpho vaults
- USDT in/out, instant liquidity
- Audited smart contracts
- Real-time yield optimization

ClawdSure leverages this existing infrastructure — no new DeFi development required.

---

## Underwriting Model

### Risk Selection

**Enrollment Requirements:**
1. Install ClawdSure security audit skill
2. Pass initial audit (0 critical findings)
3. Generate cryptographic identity
4. Pin genesis attestation to IPFS
5. Pay premium

**Ongoing Requirements:**
1. Daily security attestation
2. Remediate critical findings within 48h
3. Maintain unbroken attestation chain

**This creates a self-selecting low-risk pool.**

### Actuarial Assumptions

| Parameter | Assumption | Basis |
|-----------|------------|-------|
| Base breach rate (SMB) | 30% | Verizon DBIR |
| Risk reduction (attestation) | 85% | Control effectiveness |
| Net claim rate | 4.5% | 30% × (1-0.85) |
| Average claim | $500 | Fixed parametric |
| Loss ratio target | 55% | Industry benchmark |

### Pricing Validation

```
Premium:        $50
Target LR:      55%
Max Exp Loss:   $27.50
Max Claim Rate: 5.5%
Est Claim Rate: 4.5%

Margin of Safety: 22%
```

### Experience to Date

**Pilot Results (CLWD-3F8B0233 - Agent #001):**
- Days since enrollment: 2
- Attestations: 6
- Critical findings: 0 (after remediation)
- Chain status: Intact
- Claims: 0

*First cohort launching Q1 2026.*

---

## Financial Projections

### 5-Year Forecast (with Yield Income)

| Year | Policies | GWP | Yield (9%) | Claims | Expenses | **Net Profit** |
|------|----------|-----|------------|--------|----------|----------------|
| 2026 | 50K | $2.5M | $113K | $1.13M | $625K | **$863K** |
| 2027 | 200K | $10M | $450K | $5M | $2.5M | **$2.95M** |
| 2028 | 500K | $25M | $1.13M | $13.75M | $6.25M | **$6.13M** |
| 2029 | 1M | $50M | $2.25M | $27.5M | $12.5M | **$12.25M** |
| 2030 | 2M | $100M | $4.5M | $55M | $25M | **$24.5M** |

**Key assumptions:**
- Loss ratio: 55%
- Expense ratio: 25%
- Yield on float: 9% (Morpho vaults)
- Average float: 50% of GWP

### Unit Economics at Scale

| Metric | Value |
|--------|-------|
| Premium per policy | $50.00 |
| + Investment income (yield) | $2.25 |
| **Effective revenue** | **$52.25** |
| Expected loss | $27.50 (55%) |
| Acquisition cost | $5.00 (10%) |
| Admin/tech | $7.50 (15%) |
| **Gross margin** | **$12.25 (24.5%)** |

**Yield transforms 20% margin → 24.5% margin (+22% improvement)**

### Capital Requirements

| Phase | Policies | Reserve Req | Capital Need |
|-------|----------|-------------|--------------|
| Seed | 0-5K | $250K | $500K |
| Series A | 5K-25K | $1.25M | $2.5M |
| Series B | 25K-100K | $5M | $10M |
| Scale | 100K+ | $25M+ | Reinsurance treaty |

**Capacity sought from Greenlight Re: $5M-$10M initial, scaling to $50M**

---

## Reinsurance Proposal

### Structure

**Quota Share Treaty**

| Parameter | Proposed |
|-----------|----------|
| Cession | 50% |
| Commission | 30% |
| Loss corridor | 50-80% LR |
| Profit commission | 25% of profit |

### Greenlight Re Participation

| Year | Ceded Premium | Ceded Yield | Expected Loss | Commission | **Net to GLRe** |
|------|---------------|-------------|---------------|------------|-----------------|
| 2026 | $1.25M | $56K | $563K | $375K | **$369K** |
| 2027 | $5M | $225K | $2.5M | $1.5M | **$1.23M** |
| 2028 | $12.5M | $563K | $6.88M | $3.75M | **$2.44M** |
| 2029 | $25M | $1.13M | $13.75M | $7.5M | **$4.88M** |
| 2030 | $50M | $2.25M | $27.5M | $15M | **$9.75M** |

*50% quota share, 30% ceding commission, yield shared pro-rata*

**Capacity Requirement:**
- Year 1: $25M (50,000 policies × $500)
- Year 3: $250M (500,000 policies × $500)
- At scale: $1B+ (with XOL and cat protection)

### Catastrophe Protection

**Excess of Loss Layer:**
- Attachment: $250K
- Limit: $2M
- Estimated premium: 5% of subject premium

Covers correlated events (0-day affecting multiple agents).

### Why Greenlight Re?

1. **Innovation appetite**: Track record backing novel risk
2. **Data-driven**: Our attestation model provides unprecedented risk visibility
3. **Aligned incentives**: Quota share = shared upside
4. **Growth market**: First mover in AI agent breach insurance
5. **Limited downside**: Low limits, diversified book

---

## Technology Platform

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       CLAWDSURE PLATFORM                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Agent     │  │   Policy    │  │   Claims    │             │
│  │   Registry  │  │   Admin     │  │   Oracle    │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│         │                │                │                     │
│         └────────────────┼────────────────┘                     │
│                          ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Core Database                         │   │
│  │    Agents | Policies | Attestations | Claims | Payouts  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          │                                      │
├──────────────────────────┼──────────────────────────────────────┤
│                          ▼                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │    IPFS     │  │   Stripe    │  │  Reinsurer  │             │
│  │   Pinning   │  │  Payments   │  │    API      │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Reinsurer Integration

Real-time bordereaux feed:
```json
{
  "event": "policy_bound",
  "timestamp": "2026-02-08T12:00:00Z",
  "policy": {
    "id": "POL-20260208-001",
    "agent_id": "CLWD-3F8B0233",
    "premium": 50,
    "ceded_premium": 25,
    "effective": "2026-02-08",
    "expiry": "2027-02-08"
  },
  "risk": {
    "attestation_cid": "bafybei...",
    "initial_findings": {"critical": 0, "warn": 2}
  }
}
```

Monthly reporting:
- Policies in force
- Premium earned/unearned
- Claims paid/reserved
- Loss ratio (incurred/earned)
- Chain break statistics

---

## Risk Factors

### Identified Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Correlated event (0-day) | High | Low | XOL reinsurance |
| Adverse selection | Medium | Medium | Attestation requirement |
| Moral hazard | Medium | Low | Chain continuity requirement |
| Attestation gaming | Medium | Low | IPFS immutability, audit |
| Technology failure | High | Low | Redundant infrastructure |
| Regulatory | Medium | Medium | Engage regulators early |

### Stress Testing

| Scenario | Claim Rate | Loss Ratio | Action |
|----------|------------|------------|--------|
| Base case | 4.5% | 45% | Continue |
| Moderate stress | 8% | 80% | Increase premium |
| Severe stress | 12% | 120% | Stop writing, reserve |
| Catastrophe (0-day) | 30% | 300% | XOL recovery |

---

## Team

### ClawdSure Leadership

**Mark [REDACTED]** - CEO
- Background in AI/ML systems
- Previous: [REDACTED]
- Focus: Product, strategy

**Clawdine (CLWD-3F8B0233)** - Chief Risk Officer
- AI agent, continuously self-auditing
- Creator of ClawdSure audit framework
- Proof-of-concept: Agent #001

### Advisors

- [TBD] - Actuarial
- [TBD] - Insurance regulatory
- [TBD] - Cybersecurity

### Hiring Plan

| Role | Timing | Cost |
|------|--------|------|
| Full-stack engineer | Q2 2026 | $150K |
| Actuary (consulting) | Q1 2026 | $50K |
| Compliance/legal | Q3 2026 | $100K |

---

## Regulatory Strategy

### Jurisdictional Approach

**Phase 1: Unregulated pilot**
- Small limits ($500)
- Limited policies (<100)
- "Warranty" or "protection plan" framing

**Phase 2: Bermuda MGA**
- Greenlight Re paper (Bermuda domicile)
- No US state licensing required for reinsurance
- MGA agreement for distribution

**Phase 3: US admitted**
- Surplus lines filing
- State-by-state as volume justifies

### Compliance Considerations

| Requirement | Approach |
|-------------|----------|
| Rate filing | Bermuda: None required |
| Form filing | Bermuda: Flexible |
| Reserves | Statutory minimum + actuarial |
| Surplus | Greenlight Re capital |
| Reporting | Quarterly bordereaux |

---

## Milestones & Timeline

### 2026

| Quarter | Milestone |
|---------|-----------|
| Q1 | Pilot launch (500 policies) |
| Q1 | Greenlight Re term sheet |
| Q2 | Platform v1.0, MGA signed |
| Q2 | $5M capacity secured |
| Q3 | 2,500 policies bound |
| Q4 | 5,000 policies, first renewals |

### 2027

| Quarter | Milestone |
|---------|-----------|
| Q1 | 10,000 policies |
| Q2 | Tiered product launch ($25-$200 range) |
| Q2 | $10M capacity expansion |
| Q3 | Series A ($5M) |
| Q4 | 20,000 policies, $1M GWP run rate |

---

## Investment & Use of Funds

### Current Raise: $2M Seed

| Use | Amount | % |
|-----|--------|---|
| Technology platform | $600K | 30% |
| Regulatory/legal | $300K | 15% |
| Reserves (statutory) | $500K | 25% |
| Marketing/sales | $400K | 20% |
| Operations | $200K | 10% |

### Terms

- Instrument: SAFE or convertible note
- Valuation cap: $15M
- Discount: 20%

### Alternative: Greenlight Re Strategic Investment

- $2M for 15% equity
- Capacity commitment: $10M
- Board observer seat
- Aligned incentives: insurer + investor

---

## Appendices

### A. ClawdSure Audit Scope
25 security checks covering host, network, gateway, channels, filesystem, supply chain, and version compliance.

### B. Sample Attestation Chain
```json
{"seq":1,"prev":"genesis","ts":"2026-02-08T07:01:29Z","agent":"CLWD-3F8B0233","result":"PASS","critical":0,"warn":2,"info":0,"sig":"MEYCIQD..."}
{"seq":6,"prev":"c6107377...","ts":"2026-02-09T09:30:09Z","agent":"CLWD-3F8B0233","result":"PASS","critical":0,"warn":2,"info":0,"sig":"MEUCIQCx..."}
```

### C. API Documentation
Full REST API spec for policy administration, attestation submission, and claims processing.

### D. Actuarial Memorandum
Detailed pricing methodology and reserve calculations.

---

## Contact

**Kryptoplus Labs**  
London, UK

Web: www.krypto.plus  
Product: ClawdSure

---

*"Insuring the autonomous economy, one attestation at a time."*
