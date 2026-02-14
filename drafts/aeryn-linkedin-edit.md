# I Went Quiet for a Year. I Was Building DeFi Plumbing for People Who Wear Suits.

I disappeared from LinkedIn. No posts, no panels, no "thrilled to announce." I was building.

Here's the short version: traditional finance is sitting on trillions earning 4-5%. DeFi lending protocols are generating 6-12% on stablecoins, overcollateralised, transparent, liquid. But nobody built the bridge properly — because institutions don't care about your smart contract if it can't talk to their compliance team.

That's what I've been building.

## The Gap

I work at EFT Corp on banking projects across Africa. They're genuinely impressive — reconciliation infrastructure, payment orchestration, BaaS and card issuing expanding across the continent at pace. Front-row seat to how the best in TradFi actually operate.

And that's exactly what made the gap so obvious.

DeFi built incredible financial primitives and then wrapped them in interfaces only crypto-native people could navigate. The yields are real. The risk profiles are sound (overcollateralised lending is fundamentally different from the unsecured stuff that blew up in 2022). But the operational layer — compliance, accounting, governance, auditability — doesn't exist.

So we built it.

## HyperSend

I've been building this with Mark Musson. His background is pricing and risk — he built and sold a dynamic motor pricing MGA to AON. Mine is payments infrastructure across Africa. Between us, we cover the financial engineering and the operational reality.

HyperSend is multi-chain vault infrastructure for institutional treasurers. In plain English: a smart allocation layer that routes capital across the highest-performing, lowest-risk DeFi yield strategies — with the controls, reporting, and governance that a CFO actually needs.

**The boring bits that matter:**

- **ERC-4626 compliant** — same tokenised vault standard BlackRock uses for BUIDL. Not an accident.
- **Deterministic deployment** across 4+ chains. Same addresses, same interfaces, same guarantees everywhere.
- **Share-based sub-accounting** — mirrors how treasurers actually segregate funds (operating capital, reserves, program allocations). Each sub-account tracks its own yield. Fully auditable.
- **Multi-sig governance** via Gnosis Safe. Time-delayed upgrades. Emergency procedures. Multiple access control layers.
- **Cross-chain routing** — deposit any supported asset on any chain, lands in the right vault.
- **Real-time GraphQL APIs** — balances, yields, transaction history across every chain, instantly.

We didn't build a DeFi product. We built treasury infrastructure that happens to run on-chain.

## Who This Is For

**Corporate treasuries.** $100M+ sitting in T-bills at 4-5%. Same risk profile, 6-12%, instant liquidity, real-time accounting. No lock-ups. No redemption queues.

**NGOs.** Donor funds earning yield while maintaining full segregation between programs — auditable on a public ledger. Imagine a donor verifying on-chain that their contribution is held separately and earning returns for the designated program. That transparency doesn't exist today.

**Insurance float.** Premiums held in reserve until claims are paid — often billions. Sub-vault architecture mirrors traditional insurance accounting: claims reserves, expense pools, profit allocations, each with independent yield tracking.

**Gaming operators.** House funds need yield and per-user accounting simultaneously. Same infrastructure, zero code changes. Configuration only.

Same core vault serves all of them. The architecture adapts through configuration, not custom development.

## The Market Isn't Coming. It's Here.

- Tokenised US Treasuries: $3.9B → $9.2B in one year
- BlackRock's BUIDL: $2.3B+
- RWA tokenisation overall: tripled to $16.7B
- BCG/Ripple projection: $18.9T by 2033 (53% CAGR)
- Yield-bearing stablecoins doubling in supply

This is institutional capital flowing onto public chains. The question is who builds the plumbing.

## What's Next

The infrastructure is built. We're forming partnerships with organisations that see the same opportunity. If your organisation is sitting on idle capital that could work harder — or you're building at this intersection — let's talk.

---

*What's the biggest barrier you see to institutions going on-chain? Genuinely want to know.*
