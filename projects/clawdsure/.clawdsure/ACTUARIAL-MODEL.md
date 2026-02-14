# ClawdSafe Actuarial Pricing Model

**Date:** 2026-02-07  
**Version:** 2.0  
**Company:** Kryptoplus Labs (www.krypto.plus)

---

## Executive Summary

The $50 premium → $500 payout model is **highly viable** with yield enhancement:

**Without yield:**
- Claim rate ≤6% required for 60% loss ratio
- Marginal profitability

**With HyperSend/Morpho yield (6-12% on float):**
- Adds $2.25/policy in investment income
- Effective combined ratio drops to **85%**
- Transforms marginal UW into profitable float business

**Key requirements:**
- ~385 policies minimum for statistical credibility
- Active breach rate reduction via continuous attestation
- USDT premium collection for yield routing

---

## Industry Benchmarks (2024-2025)

| Metric | Value | Source |
|--------|-------|--------|
| Global cyber insurance market | $15B (2024) | Security.org |
| Market growth rate | 30% CAGR | Security.org |
| Average breach cost | $4.45M | IBM |
| SMB breach rate (any incident) | ~43% annually | Verizon DBIR |
| Ransomware in breaches | 44% | Verizon DBIR |
| Cyber claims (breach-related) | 73% | NetDiligence |
| Unreported incidents | 91.5% | German BKA |
| Cyber insurance loss ratio | 45-65% | Industry avg |

---

## Actuarial Framework

### Core Formula

```
Pure Premium = P(claim) × E(payout)
Gross Premium = Pure Premium / (1 - Expense Ratio - Profit Margin)
Loss Ratio = Claims Paid / Premiums Earned
```

### Target Ratios

| Component | Target | Notes |
|-----------|--------|-------|
| Loss Ratio | 60% | Claims / Premium |
| Expense Ratio | 25% | Admin, marketing, tech |
| Profit Margin | 15% | Underwriting profit |
| **Combined Ratio** | **100%** | Break-even point |

---

## Pricing Analysis: $50 → $500

### Back-Solving for Maximum Claim Rate

Given:
- Premium (P) = $50
- Payout (L) = $500
- Target Loss Ratio (LR) = 60%

```
Max Expected Loss = P × LR = $50 × 0.60 = $30
Max Claim Rate = $30 / $500 = 6.0%
```

**The model works if ≤6% of policyholders make claims.**

### Sensitivity Analysis (UW Only)

| Claim Rate | Expected Loss | Loss Ratio | Viable? |
|------------|---------------|------------|---------|
| 2% | $10 | 20% | ✅ Very profitable |
| 4% | $20 | 40% | ✅ Profitable |
| 6% | $30 | 60% | ✅ Target |
| 8% | $40 | 80% | ⚠️ Marginal |
| 10% | $50 | 100% | ❌ Break-even |
| 12% | $60 | 120% | ❌ Loss |

---

## Investment Income: HyperSend/Morpho Yield

### The Float Opportunity

Insurance is a float business. Warren Buffett built Berkshire on insurance float invested at scale. ClawdSafe applies this to crypto-native premiums via HyperSend.

### Premium Flow

```
Agent pays $50 USDT
      ↓
HyperSend Router
      ↓
Morpho Vaults (6-12% APY)
      ↓
Yield accrues to reserve
      ↓
Claims paid instantly in USDT
```

### Float Calculation

| Variable | Value | Notes |
|----------|-------|-------|
| Annual premium | $50 | Paid upfront |
| Earning period | 12 months | Full year coverage |
| Average float | $25 | Half-year weighted average |
| Morpho APY (low) | 6% | Conservative |
| Morpho APY (mid) | 9% | Base case |
| Morpho APY (high) | 12% | Optimistic |

### Yield Per Policy

| APY Scenario | Yield/Policy | As % of Premium |
|--------------|--------------|-----------------|
| 6% (low) | $1.50 | 3.0% |
| 9% (mid) | $2.25 | 4.5% |
| 12% (high) | $3.00 | 6.0% |

### Impact on Combined Ratio

| Metric | Without Yield | With Yield (9%) |
|--------|---------------|-----------------|
| Premium | $50.00 | $50.00 |
| Investment income | $0.00 | $2.25 |
| **Effective revenue** | **$50.00** | **$52.25** |
| Claims (55% LR) | $27.50 | $27.50 |
| Expenses (25%) | $12.50 | $12.50 |
| **Net margin** | **$10.00 (20%)** | **$12.25 (24.5%)** |
| **Combined ratio** | **95%** | **90%** |

### Sensitivity with Yield

| Claim Rate | Loss (UW) | Yield | Net Result | Viable? |
|------------|-----------|-------|------------|---------|
| 4% | $20 | +$2.25 | $30.25 profit | ✅ Excellent |
| 6% | $30 | +$2.25 | $20.25 profit | ✅ Good |
| 8% | $40 | +$2.25 | $10.25 profit | ✅ Marginal → OK |
| 10% | $50 | +$2.25 | $0.25 profit | ⚠️ Break-even → Marginal |
| 12% | $60 | +$2.25 | -$9.75 loss | ❌ Loss (but less severe) |

**Yield extends viability from 6% claim rate to ~10% claim rate.**

### At Scale

| Policies | GWP | Avg Float | Yield (9%) | Impact |
|----------|-----|-----------|------------|--------|
| 50K | $2.5M | $1.25M | $113K | Material |
| 500K | $25M | $12.5M | $1.13M | Significant |
| 2M | $100M | $50M | $4.5M | Transformative |
| 5M | $250M | $125M | $11.25M | Float business |

At 5M policies, **yield alone covers 40% of expected claims**.

---

## Claim Rate Estimation

### Baseline: Uncontrolled SMB Population

| Incident Type | Annual Rate | Source |
|---------------|-------------|--------|
| Any cyber incident | 43% | Verizon DBIR |
| Data breach | 28% | Ponemon |
| Ransomware | 15-20% | Coalition |
| BEC/fraud | 12% | FBI IC3 |

**Uncontrolled baseline: ~30-40% would file claims**

### Controlled: Clawdsure Population (with continuous attestation)

Security controls reduce breach probability:

| Control | Risk Reduction | Source |
|---------|---------------|--------|
| Regular patching | 60% | CISA |
| MFA enabled | 80-90% | Microsoft |
| Security audits | 50-70% | Various |
| Endpoint protection | 40-60% | Various |
| Continuous monitoring | 30-50% | Gartner |

**Compounded reduction estimate:**
```
Base rate: 30%
× (1 - 0.60) patch compliance
× (1 - 0.50) security audit (ClawdStrike)
× (1 - 0.30) continuous monitoring
= 30% × 0.40 × 0.50 × 0.70
= 4.2%
```

**Estimated claim rate for compliant agents: 3-6%**

This is within the 6% threshold for 60% loss ratio.

---

## Capital Requirements

### Minimum Policies for Statistical Credibility

Using Bühlmann credibility theory:
```
n = k² / (p × (1-p))

Where:
k = desired precision (0.05 for 5%)
p = expected claim rate (0.05)

n = 0.05² / (0.05 × 0.95) = 0.0025 / 0.0475 ≈ 53 minimum
```

For 95% confidence with 5% claim rate: **~385 policies**

### Reserve Requirements

Standard actuarial reserves:
```
Expected Claims Reserve = n × p × L
                       = 385 × 0.05 × $500
                       = $9,625

Catastrophe Reserve (2× expected) = $19,250

IBNR Reserve (10% of expected) = $963

Total Reserves Needed = ~$30,000
```

### Break-Even Analysis

| Policies | Premium Revenue | Expected Claims | Gross Margin |
|----------|-----------------|-----------------|--------------|
| 100 | $5,000 | $2,500 (5%) | $2,500 |
| 385 | $19,250 | $9,625 (5%) | $9,625 |
| 1,000 | $50,000 | $25,000 (5%) | $25,000 |
| 10,000 | $500,000 | $250,000 (5%) | $250,000 |

---

## Premium Adjustment Factors

### Risk-Based Pricing

| Factor | Adjustment | Rationale |
|--------|------------|-----------|
| **Base** | $50 | Standard compliant agent |
| +Critical findings history | +$15 (+30%) | Higher risk |
| +Public gateway | +$10 (+20%) | Larger attack surface |
| +No MFA on channels | +$10 (+20%) | Account compromise risk |
| -1+ year clean chain | -$5 (-10%) | Proven compliance |
| -Zero warnings | -$3 (-6%) | Exceptional hygiene |

**Premium range: $32 - $85**

### Experience Rating (Year 2+)

```
Adjusted Premium = Base × Experience Mod

Experience Mod = (Actual Losses + Expected Losses × Credibility) 
                 / (Expected Losses × (1 + Credibility))
```

---

## Payout Tiers (Alternative Model)

Instead of flat $500, tiered by incident type:

| Incident Type | Payout | Frequency | Expected Cost |
|---------------|--------|-----------|---------------|
| Credential theft | $250 | 3% | $7.50 |
| Data breach | $500 | 1.5% | $7.50 |
| Ransomware | $1,000 | 0.5% | $5.00 |
| Full compromise | $2,000 | 0.25% | $5.00 |
| **Total** | | **5.25%** | **$25.00** |

This gives 50% loss ratio with more granular payouts.

---

## Moral Hazard & Adverse Selection

### Moral Hazard Mitigation
- **Continuous attestation required** - Can't let security lapse
- **Chain breaks void coverage** - Incentive to maintain compliance
- **48h grace period** - Reasonable remediation window
- **Public chain** - Transparency prevents gaming

### Adverse Selection Mitigation
- **Genesis audit required** - Must be clean to enroll
- **Experience rating** - Bad actors priced out over time
- **Payout caps** - Limits catastrophic loss from bad pool

---

## Reinsurance Considerations

For catastrophic/correlated events (0-day affecting all agents):

| Layer | Retention | Reinsurance | Premium Cost |
|-------|-----------|-------------|--------------|
| Working layer | $0 - $50K | Self-retained | $0 |
| First excess | $50K - $250K | Quota share 50% | ~$5K/year |
| Catastrophe | $250K+ | Stop-loss | ~$10K/year |

At scale (1000+ policies), reinsurance becomes economical.

---

## Recommendations

### Phase 1: MVP (0-100 policies)
- **Premium**: $50/year
- **Payout**: $500 flat
- **Reserve**: $15,000 (self-funded)
- **Target loss ratio**: 50%
- **No reinsurance** (accept tail risk)

### Phase 2: Growth (100-1000 policies)
- **Premium**: $40-70 risk-adjusted
- **Payout**: Tiered ($250-$1000)
- **Reserve**: $100,000
- **Target loss ratio**: 55%
- **Quota share reinsurance** 25%

### Phase 3: Scale (1000+ policies)
- **Premium**: Actuarially modeled per-risk
- **Payout**: Up to $5,000 (larger limits)
- **Reserve**: Actuarially determined
- **Target loss ratio**: 60%
- **Full reinsurance program**

---

## Key Metrics to Track

| Metric | Formula | Target |
|--------|---------|--------|
| Loss Ratio | Claims / Premium | ≤60% |
| Claim Frequency | Claims / Policies | ≤6% |
| Average Claim | Total Claims / # Claims | ~$500 |
| Persistency | Renewals / Expiring | ≥80% |
| Chain Break Rate | Breaks / Active | ≤10% |

---

## Conclusion

**The $50/$500 model is highly viable with yield enhancement:**

1. ✅ Claim rate tolerance extends from ≤6% to ≤10% with yield
2. ✅ HyperSend/Morpho adds 4.5% effective premium
3. ✅ Combined ratio drops from 95% to 85%
4. ✅ Float business model proven (Berkshire, Markel, Fairfax)
5. ✅ USDT-native = seamless DeFi integration

**Estimated profitability at 500,000 policies:**
- GWP: $25,000,000
- Investment income: $1,125,000
- Claims (55%): $13,750,000
- Expenses (25%): $6,250,000
- **Net profit: $6,125,000 (24.5% margin)**

**The killer insight:** Traditional insurers earn 3-5% on float (bonds, equities). ClawdSafe earns 6-12% on float (DeFi). This structural advantage compounds at scale.

---

*"Insurance is the business of pricing uncertainty + investing float. ClawdSafe does both better."*
