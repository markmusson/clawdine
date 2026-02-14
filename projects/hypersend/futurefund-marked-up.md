# CONCEPT PAPER

## FutureFund

### Long-Term Children's Savings & Investment Platform
### Powered by Institutional-Grade Vault Infrastructure

Prepared by: Aeryn Quarmby & Mark Musson
February 2026
CONFIDENTIAL

---

## 1. Executive Summary

FutureFund is a long-term children's savings and investment platform that enables parents and families to build education funds from birth through to college entry. The platform converts local currency deposits into stablecoins and deploys them into institutional-grade, overcollateralised yield strategies — delivering 6–12% annual returns compared to 4–5% from traditional savings instruments.

Built on HyperSend's multi-chain vault infrastructure and wrapped in CurrenC's CASP2-regulated conversion layer, FutureFund inherits enterprise-grade compliance, sub-accounting, multi-sig governance, and real-time auditability. The entire yield layer is abstracted from the end user: parents see a familiar savings app; underneath, their capital is working harder than any bank account or unit trust could deliver.

Over an 18-year savings horizon, the compounding advantage is transformative. A monthly contribution of R2,000 at a traditional 5% return yields approximately R698,000 at maturity. At 9% through FutureFund, the same contribution grows to approximately R1,148,000 — a 64% improvement that can mean the difference between partial and full coverage of tertiary education costs. That's R450,000 more from the same monthly outlay. Enough for an extra two years of fees.

The platform is designed for the South African market initially, with architecture that supports expansion across the African continent and emerging markets globally.

---

## 2. The Opportunity

### 2.1 The Problem

Parents across South Africa face a compounding crisis in education funding. University costs are rising at 7–10% annually, significantly outpacing inflation. Traditional savings products — fixed deposits, money market funds, education policies — offer returns of 4–6% at best, meaning families are falling further behind each year they save.

Existing education savings products suffer from several structural limitations: high fees that erode returns over long horizons, lock-in periods with punitive early withdrawal penalties, lack of transparency in how funds are invested, limited flexibility in contribution patterns, and no mechanism for extended family participation.

### 2.2 Why Now

Three converging trends make this the right moment to launch:

**Stablecoin legitimacy:** Stablecoins have crossed into mainstream acceptance. USDC and USDT collectively represent over $200B in market capitalisation. Major financial institutions including BlackRock (via BUIDL), Franklin Templeton, and PayPal now issue or utilise stablecoins.

**Institutional-grade infrastructure:** Platforms like HyperSend have built the compliance, governance, and auditability layers that were previously missing. Overcollateralised lending protocols (Aave, Compound, Morpho) have operated through multiple market cycles — including the 2022 collapse that wiped out centralised lenders — without systemic loss. That distinction matters: CeFi failed because it was undercollateralised and opaque. The protocols FutureFund uses are neither.

**Tokenised real-world assets:** Tokenised US Treasuries have grown from $3.9B to $9.2B in one year. RWA tokenisation overall has tripled to $16.7B, with BCG/Ripple projecting $18.9T by 2033. The infrastructure is maturing rapidly.

**Regulatory clarity in South Africa:** The CASP2 licensing framework provides a clear, existing path for regulated crypto asset service provision. CurrenC holds this licence today, eliminating the regulatory uncertainty that has stalled similar products elsewhere.

### 2.3 Market Size

South Africa has approximately 1.2 million births annually. The addressable market includes the roughly 3–4 million households in LSM 7–10 who have disposable income and awareness of education cost pressures. Beyond South Africa, the platform architecture supports deployment across the continent — Nigeria, Kenya, Ghana, and other markets where mobile-first financial products are already dominant.

The global children's savings market is estimated at over $500B in assets under management across education savings accounts, 529 plans, Junior ISAs, and equivalent instruments worldwide.

---

## 3. The Solution

### 3.1 Product Overview

FutureFund presents as a mobile-first savings application. Parents create an account, add a child beneficiary, and begin contributing in ZAR via bank transfer, debit order, or mobile wallet. The platform handles the conversion to stablecoins (USDC/USDT), deployment into yield-generating vaults, and continuous compounding — all invisible to the user.

The user experience is deliberately simple: open the app, see your child's fund balance, current yield rate, projected value at age 18, and contribution history. No wallets, no gas fees, no chain selection. Just a savings account that works harder.

### 3.2 Core Features

- **Child-linked accounts** — one fund per child, trackable from birth to maturity
- **Family contributions** — grandparents, aunts, uncles can contribute directly via shareable link or QR code. Birthday money goes into the fund, not into plastic that breaks in a week
- **Flexible contributions** — no minimum lock-in, adjust monthly amounts anytime, lump-sum top-ups welcome
- **Real-time dashboard** — current balance, yield earned this month/year/lifetime, projected value at age 18
- **Milestone notifications** — "Your child's fund just passed R100,000" / "On track to cover 4 years of tuition"
- **Controlled withdrawals** — designed for long-duration savings with clear withdrawal mechanics (see Section 8: Risk)

### 3.3 How It Works (Technical Architecture)

FutureFund is built on a regulated, multi-layered stack where each entity holds only its own risk:

```
Parent (ZAR deposit)
    → EFT Corp (fiat conversion, settlement, reconciliation, KYC/AML)
        → CurrenC (CASP2-regulated crypto asset conversion)
            → HyperSend (multi-chain vault infrastructure, ERC-4626)
                → Yield protocols (Aave, Compound, Morpho — overcollateralised only)
```

**EFT Corp** provides the regulated fiat rails — ZAR conversion, settlement, reporting, and reconciliation through its existing banking infrastructure across Africa. EFT does not custody consumer funds, does not promise yield, and carries no balance sheet exposure to the savings product. It provides the same plumbing it already operates, applied to a new product category.

**CurrenC** provides the CASP2-regulated bridge between fiat and crypto assets. This licence is held today — not pending, not applied for.

**HyperSend** provides the vault infrastructure:
- ERC-4626 compliant — the same tokenised vault standard BlackRock uses for BUIDL
- Deterministic deployment across 4+ chains
- Share-based sub-accounting — mirrors how treasurers segregate funds. Each child's account tracks its own yield, fully auditable
- Multi-sig governance via Gnosis Safe. Time-delayed upgrades. Emergency procedures. Multiple access control layers
- Cross-chain routing — deposit any supported asset on any chain, lands in the right vault
- Real-time GraphQL APIs — balances, yields, transaction history across every chain

**FutureFund SPV** is the licensed product issuer. It holds the consumer relationship, carries the product liability, and is registered with the FSCA as a financial product provider. This is the entity that makes promises to parents. No other entity in the stack does.

---

## 4. Yield Comparison & Projections

The following projections illustrate the compounding advantage over an 18-year savings horizon. All figures assume monthly contributions with no withdrawals until maturity.

### 4.1 Scenario: R2,000/month for 18 years

| Scenario | Annual Return | Maturity Value | Difference vs Bank |
|---|---|---|---|
| Bank savings account | 4% | R626,000 | — |
| Education policy | 5% | R698,000 | +R72,000 |
| **FutureFund Conservative** | **7%** | **R867,000** | **+R241,000** |
| **FutureFund Moderate** | **9%** | **R1,148,000** | **+R522,000** |
| **FutureFund Aggressive** | **12%** | **R1,618,000** | **+R992,000** |

At the moderate scenario (9%), FutureFund delivers R450,000 more than a traditional education policy — from identical monthly contributions. That's an extra two years of university fees.

### 4.2 Stress Test: What If Yields Compress?

| Scenario | Annual Return | Maturity Value | vs Education Policy |
|---|---|---|---|
| Yield compression | 5% | R698,000 | Break-even |
| Severe compression | 4% | R626,000 | -R72,000 |
| Moderate (expected) | 9% | R1,148,000 | +R450,000 |

If yields compress to traditional savings levels, FutureFund breaks even — parents don't lose money, they just don't gain the advantage. The architecture still provides superior transparency and flexibility. The downside is parity, not loss.

### 4.3 Currency Considerations

FutureFund operates in USD-denominated stablecoins. For South African users, this introduces currency exposure that has historically been favourable: the rand has depreciated against the dollar at an average rate of approximately 5–6% per annum over the past two decades. This means ZAR-denominated returns are typically higher than the USD yield alone.

**However, currency movements are not guaranteed.** In a scenario where the rand strengthens 10% against the dollar over the savings period, USD-denominated returns would be reduced in ZAR terms. Even in this scenario, the yield advantage (6–12% vs 4–5%) more than compensates for currency headwinds.

The platform will provide clear, prominent disclosure on currency exposure. A future ZAR-pegged stablecoin option (such as ZARP) could be offered when market depth permits.

---

## 5. Regulatory & Compliance Framework

FutureFund operates within a clearly bounded regulatory structure. Each entity in the stack is regulated for its specific function:

| Entity | Regulatory Function | Regulator | Status |
|---|---|---|---|
| **EFT Corp** | Fiat conversion, settlement, KYC/AML | SARB, FIC | Existing licence |
| **CurrenC** | Crypto asset service provision | FSCA (CASP2) | **Licence held today** |
| **FutureFund SPV** | Financial product issuance | FSCA (FSP) | To be registered |
| **HyperSend** | Vault infrastructure provider | N/A (technology layer) | Not consumer-facing |

**Critical principle:** No entity carries another entity's regulatory burden. EFT provides rails, not custody. CurrenC provides conversion, not investment advice. HyperSend provides infrastructure, not a consumer product. FutureFund SPV is the single entity that faces the consumer and carries product liability.

**The question "whose balance sheet touches the money when something goes wrong?" has a clear answer:** The FutureFund SPV, backed by ring-fenced client assets in segregated vaults with multi-sig governance.

Custody of funds is structured through the regulated custodial arrangement, ensuring client assets are ring-fenced and protected in the event of platform insolvency. The multi-sig governance inherited from HyperSend provides an additional layer of protection at the smart contract level.

---

## 6. Risk Assessment

### 6.1 Smart Contract Risk

Yield protocols (Aave, Compound, Morpho) are battle-tested across multiple market cycles. Aave has processed over $100B in loans without systemic loss. HyperSend's vaults undergo independent security audits. However, smart contract risk can never be fully eliminated. **Mitigation:** multi-protocol diversification, formal verification, insurance coverage via Nexus Mutual or equivalent, and conservative allocation limits per protocol.

### 6.2 Stablecoin Depeg Risk

USDC briefly depegged during the SVB crisis (March 2023) to ~$0.87 before recovering within 48 hours. **Mitigation:** multi-stablecoin diversification (USDC, USDT, DAI), automatic rebalancing triggers, and clear disclosure to users that stablecoins are not bank deposits.

### 6.3 Yield Compression Risk

DeFi yields are variable, not fixed. If institutional capital floods into the same protocols, yields will compress. **Mitigation:** FutureFund does not promise a specific return rate. Marketing uses ranges ("historically 6–12%") with clear disclaimers. The product still wins on transparency and flexibility even at lower yields.

### 6.4 Currency Risk

ZAR/USD movements can work for or against the investor. **Mitigation:** clear disclosure, optional ZAR-pegged stablecoin when available, and scenario modelling in the app showing returns under different currency assumptions.

### 6.5 Regulatory Risk

The South African regulatory landscape for crypto assets is evolving. CASP2 provides the current framework, but regulations may change. **Mitigation:** proactive engagement with FSCA, conservative product structuring, and architecture that can adapt to new requirements without rebuilding.

### 6.6 Custodial / Platform Risk

If FutureFund ceases operations, what happens to the funds? **Mitigation:** client assets are held in segregated, multi-sig vaults — not on FutureFund's balance sheet. Recovery procedures are built into the smart contract governance. An independent trustee structure ensures fund continuity.

### 6.7 Early Withdrawal

Parents may need emergency access to funds. Punitive lock-ins erode trust. **Mitigation:** tiered withdrawal — contributions can be withdrawn anytime (no penalty), yield earned has a graduated release schedule incentivising long-term holding. No punitive fees. The goal is retention through returns, not through traps.

---

## 7. Business Model

### 7.1 Revenue Streams

| Stream | Mechanism | Estimated |
|---|---|---|
| Yield spread | Difference between gross protocol yield and net yield passed to users | 1.0–1.5% of AUM |
| Conversion fees | ZAR→stablecoin and back | 0.3–0.5% per transaction |
| Premium tier | Advanced features (tax reporting, multi-child dashboards, advisor access) | R99/month |
| B2B white-label | Platform licensed to other financial institutions | Per-deal |

### 7.2 Unit Economics

At scale, the primary revenue driver is the yield spread on assets under management. Assuming an average AUM of R50,000 per account and a 1.5% yield spread, each active account generates approximately R750 per year in revenue. Customer acquisition cost is estimated at R200–R400 through digital channels, implying a payback period of under 6 months. Lifetime value over an 18-year relationship is approximately R13,500 per account before considering premium upsell or family network expansion.

**Churn consideration:** Over 18 years, some parents will need emergency access. The tiered withdrawal mechanism (Section 6.7) is designed to allow access without destroying the account. Historical churn in long-duration savings products (Junior ISAs, 529 plans) runs at 3–5% annually — FutureFund's superior returns and transparency should keep churn at the low end.

---

## 8. Go-to-Market Strategy

### 8.1 Phase 1: Foundation (Months 1–6)

Launch a closed beta with 100–200 families. **Specific recruitment channel:** EFT Corp's existing banking relationships provide direct access to private school parent networks and corporate employee benefit programmes. This isn't cold outreach — it's warm introduction through trusted financial infrastructure.

Focus on product-market fit: Is the onboarding smooth enough? Do parents understand the value proposition? Are family contribution mechanics used? Iterate rapidly on the mobile experience based on real user behaviour.

### 8.2 Phase 2: Growth (Months 6–18)

Open access with a referral-driven growth model. Parents who have seen their fund growing become the most credible advocates. Introduce a "gift a contribution" feature timed around key cultural moments: birthdays, Christmas, Eid, back-to-school. Partner with parenting influencers and financial literacy platforms. Target early adopters in the LSM 8–10 bracket who are comfortable with digital financial products.

### 8.3 Phase 3: Partnerships (Months 12–24)

Approach corporates for employee benefit integration: "Start your child's education fund as a company benefit." Partner with private schools and crèches for direct parent reach. Engage with banks and insurers to explore white-label opportunities. Expand geographically to Nigeria and Kenya where mobile-first savings adoption is high.

### 8.4 Phase 4: Scale (Months 24+)

Introduce additional product lines: wedding funds, gap year savings, first car funds. B2B white-label platform for financial institutions. API access for fintechs wanting to embed education savings into their own products. Explore government partnership opportunities for co-funded savings matching schemes (similar to UK Child Trust Fund or US 529 matching).

---

## 9. Option Value Beyond FutureFund

FutureFund is the first product on a general-purpose stack. The combination of EFT's fiat rails, CurrenC's regulated conversion, and HyperSend's vault infrastructure creates a platform for **any** long-duration, auditable, pooled savings product:

- **Housing deposit funds** — first-time buyer savings with yield
- **Retirement savings wrappers** — supplementary pension with transparent allocation
- **Employee benefit schemes** — company-matched savings via payroll integration
- **Cross-border remittance-to-savings** — diaspora sending money home that earns instead of sits
- **NGO program fund management** — donor funds earning yield with per-program segregation and on-chain audit trail

Each additional product runs on the same rails. No new infrastructure. No new regulatory applications (beyond product-specific FSCA registration). The marginal cost of each new product category is near zero.

This is the option value: not one product, but a regulated platform for tokenised savings across Southern Africa.

---

## 10. Team & Partnerships

### 10.1 Core Team

**Aeryn Quarmby** — Payments infrastructure across Africa via EFT Corp. Deep understanding of banking operations, reconciliation, and compliance requirements across the continent. Front-row seat to how institutional finance actually operates — and where the gaps are.

**Mark Musson** — Pricing and risk specialist. Built and sold a dynamic motor pricing MGA to AON (£40M GWP). Financial engineering expertise applied to yield strategy design and risk management. If it involves pricing risk under uncertainty, he's done it before and sold the company.

### 10.2 Key Partnerships

| Partner | Role | Status |
|---|---|---|
| **EFT Corp** | Fiat rails, settlement, banking infrastructure | In discussion |
| **CurrenC** | CASP2-regulated crypto conversion | Available |
| **HyperSend** | Vault infrastructure (ERC-4626, multi-chain) | Built |

---

## 11. Funding Requirements

FutureFund is seeking seed funding of R5–10 million to bring the platform from concept to market launch:

| Allocation | % | Amount (R) | Purpose |
|---|---|---|---|
| Platform development | 35% | R1.75–3.5M | Mobile app, API integrations, testing |
| Regulatory & legal | 20% | R1.0–2.0M | FSCA registration, legal structuring, compliance |
| Operations & team | 25% | R1.25–2.5M | Core team, support, infrastructure |
| Marketing & launch | 15% | R0.75–1.5M | Beta programme, growth, partnerships |
| Reserve | 5% | R0.25–0.5M | Contingency |

---

## 12. Next Steps

FutureFund sits at the intersection of three powerful forces: the institutional maturation of yield infrastructure, the mainstream acceptance of stablecoins, and the universal need for better long-term savings products for children.

The underlying infrastructure is built. The regulatory wrapper exists. What remains is to assemble the product that parents trust, regulators approve, and families use.

We are actively seeking:

- **Seed investors** who understand the opportunity at the intersection of institutional yield infrastructure and consumer financial products
- **Strategic partners** in banking, insurance, and fintech who could accelerate distribution
- **Regulatory advisors** with FSCA and fintech licensing experience
- **Early adopter families** willing to participate in the beta programme

The question is who builds the plumbing.

---

**Contact:**
Aeryn Quarmby — aeryn@hypersend.com
Mark Musson — markmusson@gmail.com
