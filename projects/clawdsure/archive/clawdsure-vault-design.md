# ClawdSure Vault Architecture: Premium Trust & Yield Infrastructure

**Design Concept for Smart Contract Development**

**Prepared for:** Kryptoplus Labs Engineering
**Author:** Mark Musson / Clawdine
**Date:** February 2026
**Status:** Initial Design Concept

---

## Executive Summary

ClawdSure premiums must be held in a structure that mirrors traditional insurance accounting (premium trust, claims reserve, reinsurance cession) while generating DeFi yield on the entire float. This document specifies an ERC-4626 vault architecture with segregated accounting via Safe multisig wallets, unified yield accrual via Morpho Blue/MetaMorpho, and active vault curation via the BeeFi strategy manager.

**Key insight:** The whole pot earns yield as a unit (capital efficiency), but accounting segregation is enforced at the smart contract level (regulatory compliance).

---

## Insurance Accounting Requirements

Traditional insurance requires segregated trust accounts:

| Account | Purpose | Regulatory Requirement |
|---|---|---|
| **Premium Trust** | Holds unearned premium | Cannot be commingled with operating funds |
| **Claims Reserve** | Set aside for expected claims | Actuarially determined, ring-fenced |
| **Reinsurance Cession** | Portion ceded to reinsurer | Must be identifiable and transferable |
| **IBNR Reserve** | Incurred But Not Reported | Conservative buffer |
| **Profit / Operating** | Earned premium minus claims/expenses | Available for distribution |

**The challenge:** In TradFi, these sit in separate bank accounts earning ~4% in treasuries. In DeFi, we can hold them in a unified yield-bearing vault while maintaining logical segregation.

---

## Architecture Overview

```
                           ┌──────────────────────────────────┐
                           │       PREMIUM INFLOW             │
                           │       ($50 USDT per policy)      │
                           └───────────────┬──────────────────┘
                                           │
                                           ▼
                           ┌──────────────────────────────────┐
                           │       ROUTER CONTRACT            │
                           │       (Premium Splitter)         │
                           │                                  │
                           │   Split per policy:              │
                           │   • 50% → Retained Premium      │
                           │   • 50% → Reinsurer Cession     │
                           │                                  │
                           │   From retained:                 │
                           │   • 55% → Claims Reserve         │
                           │   • 25% → Expense Pool           │
                           │   • 20% → Profit Pool            │
                           └───────┬──────────┬───────────────┘
                                   │          │
                    ┌──────────────┘          └──────────────┐
                    ▼                                        ▼
    ┌───────────────────────────┐         ┌───────────────────────────┐
    │   RETAINED VAULT (50%)    │         │   CESSION VAULT (50%)     │
    │   ERC-4626                │         │   ERC-4626                │
    │                           │         │                           │
    │   Safe: Kryptoplus 3/5    │         │   Safe: GLRe 2/3          │
    │                           │         │   (Kryptoplus co-signer)  │
    │   Sub-accounts (shares):  │         │                           │
    │   • Claims Reserve  (55%) │         │   Reinsurer controls      │
    │   • Expense Pool    (25%) │         │   withdrawals             │
    │   • Profit Pool     (20%) │         │   Yield shared pro-rata   │
    │   • IBNR Buffer     (var) │         │                           │
    └───────────┬───────────────┘         └───────────┬───────────────┘
                │                                     │
                └──────────────┬──────────────────────┘
                               │
                               ▼
                ┌──────────────────────────────────┐
                │     UNIFIED YIELD LAYER           │
                │                                   │
                │  ┌─────────────────────────────┐  │
                │  │   BeeFi Strategy Manager     │  │
                │  │                              │  │
                │  │   Active yield curation:     │  │
                │  │   • Morpho Blue markets      │  │
                │  │   • MetaMorpho vaults        │  │
                │  │   • Sky/MakerDAO DSR          │  │
                │  │                              │  │
                │  │   Constraints:               │  │
                │  │   • Stablecoin only           │  │
                │  │   • Overcollateralised only   │  │
                │  │   • High liquidity only       │  │
                │  └─────────────────────────────┘  │
                │                                   │
                └──────────────────────────────────┘
```

---

## ERC-4626 Vault Design

### Why ERC-4626

- Standard tokenized vault interface — composable with all DeFi
- Shares represent pro-rata claim on underlying assets + yield
- Atomic deposit/redeem up to limits
- Auditable, transparent, on-chain accounting
- Wide tooling support (OpenZeppelin, Morpho, Yearn)

### Vault Hierarchy

We use **two primary ERC-4626 vaults** sharing a common yield strategy:

#### 1. Retained Premium Vault (`ClawdSureRetainedVault`)

```solidity
// Controlled by Kryptoplus Safe (3/5 multisig)
// Holds: unearned premium, claims reserve, IBNR, profit

contract ClawdSureRetainedVault is ERC4626 {
    // Sub-account tracking (logical segregation via share classes)
    mapping(SubAccount => uint256) public subAccountShares;
    
    enum SubAccount {
        CLAIMS_RESERVE,   // 55% of retained — ring-fenced for payouts
        EXPENSE_POOL,     // 25% of retained — operational costs
        PROFIT_POOL,      // 20% of retained — distributable profit
        IBNR_BUFFER       // Variable — actuarially adjusted
    }
    
    // Claims can ONLY be paid from CLAIMS_RESERVE
    function payClaim(address agent, uint256 amount) external onlyOracle {
        require(subAccountShares[CLAIMS_RESERVE] >= amount);
        // ... redeem shares, transfer USDT to agent
    }
    
    // Expenses can ONLY be withdrawn from EXPENSE_POOL
    function withdrawExpenses(uint256 amount) external onlyAdmin {
        require(subAccountShares[EXPENSE_POOL] >= amount);
        // ...
    }
    
    // Profit can ONLY be distributed from PROFIT_POOL after earning period
    function distributeProfits() external onlyAdmin {
        require(block.timestamp >= currentPeriodEnd);
        // ...
    }
}
```

**Safe multisig:** Kryptoplus 3-of-5
- Mark Musson (founder)
- CTO (TBD)
- CFO/Actuary (TBD)
- Legal (TBD)
- Independent director (TBD)

#### 2. Cession Vault (`ClawdSureCessionVault`)

```solidity
// Controlled by Greenlight Re Safe (2/3 multisig)
// Kryptoplus holds 1 key as co-signer for operational coordination
// Holds: ceded premium, ceded claims reserve

contract ClawdSureCessionVault is ERC4626 {
    // Reinsurer can withdraw earned premium
    // Claims against ceded portion require co-signature
    
    function withdrawEarnedPremium(uint256 amount) external onlyReinsurer {
        // Pro-rata earned premium based on elapsed time
        // ...
    }
    
    function payCededClaim(address agent, uint256 amount) external {
        require(msg.sender == oracleContract);
        // Automatically splits claim payment: 50% from retained, 50% from cession
        // ...
    }
}
```

**Safe multisig:** Greenlight Re 2-of-3
- GLRe treasury (1 key)
- GLRe risk officer (1 key)
- Kryptoplus co-signer (1 key — operational coordination only, cannot unilaterally withdraw)

### Yield Sharing

Both vaults deposit underlying USDT into the **same yield strategy**. Yield accrues to both vaults pro-rata based on their share of the total deposit. This maximises capital efficiency — the whole pot earns as a unit.

```
Total float: $1M (example)
├── Retained vault: $500K (50%)
└── Cession vault: $500K (50%)

Morpho yield: 9% APY
Total yield: $90K/year
├── To retained: $45K (50%)
└── To cession: $45K (50%)
```

---

## Yield Strategy Layer

### BeeFi Strategy Manager

The BeeFi strategy manager actively curates yield across approved protocols. It operates within strict constraints:

#### Hard Constraints (Enforced On-Chain)

| Constraint | Rationale |
|---|---|
| **Stablecoin only** | No directional market risk on insurance float |
| **Overcollateralised lending only** | Counterparty risk minimised — borrowers post >100% collateral |
| **High liquidity only** | Claims must be payable within 24h — no lock-ups |
| **Whitelisted protocols only** | Governance-approved list, no arbitrary deployments |
| **Max allocation per protocol** | 40% — diversification across yield sources |
| **Max allocation per market** | 25% — granular diversification within protocols |

#### Approved Yield Sources

##### 1. Morpho Blue (Primary)

Morpho Blue is a permissionless lending protocol. We lend USDT into overcollateralised markets:

| Market | Collateral | LTV | Typical APY | Risk Profile |
|---|---|---|---|---|
| USDT/WETH | ETH | 77% | 4-8% | Low — ETH liquid, deep markets |
| USDT/wstETH | Lido stETH | 77% | 5-10% | Low — stETH liquid, correlated |
| USDT/WBTC | Bitcoin | 71% | 3-6% | Low — BTC deep liquidity |
| USDT/sDAI | MakerDAO savings | 94.5% | 3-5% | Very low — stablecoin collateral |

**Why Morpho Blue:** Isolated markets (no cross-contamination), known liquidation parameters, battle-tested contracts, overcollateralised only.

##### 2. MetaMorpho Vaults (Curated)

MetaMorpho vaults are curated ERC-4626 wrappers around Morpho Blue markets. Trusted curators (Re7, Steakhouse, Gauntlet) manage allocation across markets:

| Vault | Curator | Strategy | Typical APY |
|---|---|---|---|
| Re7 USDT | Re7 Labs | Lending against interest-bearing stablecoins | 6-12% |
| Steakhouse USDT | Steakhouse Financial | Conservative multi-market | 5-8% |
| Gauntlet USDT | Gauntlet | Risk-optimised allocation | 6-10% |

**Why MetaMorpho:** Professional curation, auto-rebalancing, ERC-4626 composable, audited.

##### 3. Sky/MakerDAO DSR (Stability)

The Dai Savings Rate (DSR) on Sky (formerly MakerDAO) provides a stable baseline yield:

| Feature | Value |
|---|---|
| Current DSR | ~5-8% |
| Risk | Very low (MakerDAO governance risk only) |
| Liquidity | Instant (no lock-up) |
| Collateral | N/A — deposit DAI/USDS, earn yield |

**Reference:** Joe Lubin recently deposited 15,000 ETH into Sky and borrowed $4.1M DAI — demonstrating institutional confidence in Sky's overcollateralised model. The same mechanics that secure Lubin's position secure our float deposits.

**Why Sky/MakerDAO:** Battle-tested since 2019, institutional adoption, stable yield floor, instant liquidity.

#### Strategy Allocation (Initial)

```
Total Float Allocation:
├── Morpho Blue (direct markets): 40%
│   ├── USDT/WETH:    20%
│   ├── USDT/wstETH:  10%
│   └── USDT/WBTC:    10%
├── MetaMorpho (curated vaults): 40%
│   ├── Re7 USDT:     20%
│   └── Steakhouse:   20%
└── Sky DSR (stability floor): 20%
    └── USDS/DAI:      20%
```

**Blended target APY:** 6-10% (conservative estimate: 8%)

#### Rebalancing

The BeeFi strategy manager monitors yields and rebalances:
- **Frequency:** Weekly review, rebalance if >2% APY divergence
- **Trigger:** Any protocol APY drops below 3% → reallocate to higher-yielding approved source
- **Emergency:** Any protocol incident → immediate withdrawal to Sky DSR (safe haven)
- **Governance:** Rebalancing within approved protocols is automated. Adding new protocols requires Safe multisig approval.

---

## Premium Flow: End to End

### Policy Purchase

```
1. Agent pays $50 USDT
         │
         ▼
2. Router Contract receives USDT
         │
         ├──→ $25 USDT → Retained Vault (50%)
         │     ├──→ Claims Reserve:  $13.75 (55% of retained)
         │     ├──→ Expense Pool:     $6.25 (25% of retained)
         │     └──→ Profit Pool:      $5.00 (20% of retained)
         │
         └──→ $25 USDT → Cession Vault (50% to GLRe)
               └──→ Ceded reserve:   $25.00
         
3. Both vaults deposit USDT into yield strategy
4. Yield accrues pro-rata (whole pot earns as unit)
```

### Claim Payout

```
1. Oracle verifies: chain valid + incident verified
         │
         ▼
2. Oracle calls ClaimRouter.payClaim(agent, $500)
         │
         ├──→ $250 from Retained Vault (Claims Reserve)
         │     └──→ Redeem shares → withdraw USDT from yield strategy
         │
         └──→ $250 from Cession Vault (Ceded Reserve)
               └──→ Redeem shares → withdraw USDT from yield strategy
         
3. $500 USDT transferred to agent's wallet
4. Settlement: <24 hours (instant on-chain)
```

### Premium Earning

```
Premium earns linearly over 12 months:

Month 1:   $4.17 earned ($50/12)
Month 6:   $25.00 earned (50%)
Month 12:  $50.00 earned (100%)

Unearned premium remains in vault generating yield.
At expiry: earned premium moves from reserve to profit pool.
```

---

## Smart Contract Architecture

### Contract Map

```
┌─────────────────────────────────────────────────────────────────┐
│                        CORE CONTRACTS                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ClawdSurePremiumRouter.sol                                     │
│  ├── Receives premium payments (USDT)                           │
│  ├── Splits to retained/cession per quota share                 │
│  ├── Allocates retained sub-accounts                            │
│  └── Emits PolicyBound event                                    │
│                                                                 │
│  ClawdSureRetainedVault.sol (ERC-4626)                          │
│  ├── Holds retained premium float                               │
│  ├── Sub-account tracking (claims/expense/profit/IBNR)          │
│  ├── Claims payout (oracle-triggered)                           │
│  └── Controlled by Kryptoplus Safe (3/5)                        │
│                                                                 │
│  ClawdSureCessionVault.sol (ERC-4626)                           │
│  ├── Holds ceded premium float                                  │
│  ├── Reinsurer withdrawal (earned premium)                      │
│  ├── Ceded claims payout (oracle-triggered)                     │
│  └── Controlled by GLRe Safe (2/3 + Kryptoplus co-sign)         │
│                                                                 │
│  ClawdSureClaimRouter.sol                                       │
│  ├── Oracle-only: processes verified claims                     │
│  ├── Splits payout across retained + cession vaults             │
│  └── Emits ClaimPaid event with attestation CID                 │
│                                                                 │
│  ClawdSureYieldStrategy.sol                                     │
│  ├── Deposits vault USDT into approved yield sources            │
│  ├── Enforces constraints (stablecoin, overcollateralised, etc) │
│  ├── Rebalances across Morpho/MetaMorpho/Sky                    │
│  └── Controlled by BeeFi strategy manager                       │
│                                                                 │
│  ClawdSureOracle.sol                                            │
│  ├── Verifies attestation chain validity                        │
│  ├── Receives incident reports                                  │
│  ├── Triggers claim payouts                                     │
│  └── Phase 1: multisig | Phase 2: decentralised                │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                     SAFE MULTISIG WALLETS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  KryptoplusSafe.eth (3/5)                                       │
│  ├── Controls RetainedVault                                     │
│  ├── Controls PremiumRouter configuration                       │
│  └── Co-signs CessionVault operations                           │
│                                                                 │
│  GreenlightReSafe.eth (2/3)                                     │
│  ├── Controls CessionVault withdrawals                          │
│  └── Kryptoplus holds 1 key for coordination                    │
│                                                                 │
│  OracleMultisig.eth (3/5) — Phase 1                             │
│  ├── Approves claim payouts                                     │
│  └── Transitions to decentralised oracle in Phase 2             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key Interfaces

```solidity
// Premium Router
interface IClawdSurePremiumRouter {
    function payPremium(
        bytes32 agentId,        // ClawdSure agent ID
        uint256 amount,         // USDT amount (must be $50 or tier equivalent)
        uint256 policyDuration  // Seconds (default: 365 days)
    ) external;
    
    event PolicyBound(
        bytes32 indexed agentId,
        uint256 premium,
        uint256 retained,
        uint256 ceded,
        uint256 expiry
    );
}

// Claim Router  
interface IClawdSureClaimRouter {
    function processClaim(
        bytes32 agentId,
        uint256 payoutAmount,
        bytes32 attestationCID,  // IPFS CID of valid attestation chain
        bytes calldata evidence
    ) external onlyOracle;
    
    event ClaimPaid(
        bytes32 indexed agentId,
        uint256 amount,
        uint256 fromRetained,
        uint256 fromCession,
        bytes32 attestationCID
    );
}

// Yield Strategy
interface IClawdSureYieldStrategy {
    function deposit(uint256 amount) external;
    function withdraw(uint256 amount) external returns (uint256 received);
    function totalAssets() external view returns (uint256);
    function currentAPY() external view returns (uint256); // basis points
    function rebalance() external onlyManager;
    
    // Hard constraints — revert if violated
    function isApprovedProtocol(address protocol) external view returns (bool);
    function maxAllocationPerProtocol() external view returns (uint256); // 40%
    function maxAllocationPerMarket() external view returns (uint256);   // 25%
}
```

---

## Yield Projections

### Per-Policy Economics (With Vault Yield)

| Metric | Low (6%) | Base (9%) | High (12%) |
|---|---|---|---|
| Premium | $50.00 | $50.00 | $50.00 |
| Average float (half-year weighted) | $25.00 | $25.00 | $25.00 |
| **Yield per policy** | **$1.50** | **$2.25** | **$3.00** |
| Effective revenue | $51.50 | $52.25 | $53.00 |
| Claims (55% of premium) | ($27.50) | ($27.50) | ($27.50) |
| Expenses (25%) | ($12.50) | ($12.50) | ($12.50) |
| **Net margin per policy** | **$11.50** | **$12.25** | **$13.00** |
| **Margin %** | **23%** | **24.5%** | **26%** |

### At Scale

| Policies | Total Float | Yield (6%) | Yield (9%) | Yield (12%) |
|---|---|---|---|---|
| 50K | $1.25M | $75K | $113K | $150K |
| 500K | $12.5M | $750K | $1.13M | $1.5M |
| 2M | $50M | $3M | $4.5M | $6M |
| 5M | $125M | $7.5M | $11.25M | $15M |

At 5M policies with 9% APY, yield generates **$11.25M annually** — covering ~40% of expected claims from investment income alone.

### Yield Split (50/50 Quota Share)

| Year | Total Float | Kryptoplus Yield | GLRe Yield |
|---|---|---|---|
| 2026 | $1.25M | $56K | $56K |
| 2027 | $5M | $225K | $225K |
| 2028 | $12.5M | $563K | $563K |
| 2029 | $25M | $1.13M | $1.13M |
| 2030 | $50M | $2.25M | $2.25M |

---

## Risk Management

### Smart Contract Risk

| Risk | Mitigation |
|---|---|
| Vault exploit | Audited contracts (Trail of Bits / OpenZeppelin), bug bounty |
| Yield source hack | Max 40% allocation per protocol, emergency withdrawal to Sky DSR |
| Stablecoin depeg | USDT primary; diversify to USDC/DAI if needed; overcollateralised positions buffer depeg |
| Oracle manipulation | Phase 1: multisig with time-lock; Phase 2: decentralised verification |
| Governance attack | Safe multisig with independent signers; time-locks on parameter changes |

### Liquidity Risk

| Scenario | Response Time | Mechanism |
|---|---|---|
| Normal claim | <1 hour | Direct withdrawal from yield strategy |
| Mass claims (cat event) | <24 hours | Emergency withdrawal from all vaults to USDT |
| Protocol incident | <4 hours | BeeFi emergency withdrawal to Sky DSR |

### Regulatory Risk

| Jurisdiction | Approach |
|---|---|
| Bermuda | Greenlight Re paper — flexible regulatory environment |
| UK | FCA watching brief — "warranty" framing for Phase 1 |
| US | Surplus lines via reinsurer — no direct state licensing needed |
| DeFi-native | Smart contracts are tools, not the insurer — Kryptoplus is the MGA |

---

## Implementation Phases

### Phase 1: MVP (Q1-Q2 2026)

- Single retained vault (Kryptoplus Safe)
- Manual cession tracking (no separate vault — spreadsheet reconciliation)
- Yield via single MetaMorpho USDT vault (Re7 or Steakhouse)
- Oracle: manual multisig claim approval
- **Goal:** Prove the flow works with 500 policies

### Phase 2: Full Segregation (Q3 2026)

- Separate retained + cession ERC-4626 vaults
- GLRe Safe controls cession vault
- Premium router contract automates splits
- BeeFi strategy manager across 2-3 yield sources
- Claim router automates payout splits
- **Goal:** Production-ready for GLRe treaty

### Phase 3: Scale (2027)

- Multi-protocol yield diversification (Morpho + Sky + additional curated vaults)
- Automated rebalancing via BeeFi
- Decentralised oracle (Phase 2 of oracle design)
- XOL layer for catastrophe protection
- Multi-tier premium support ($25-$200 range)
- **Goal:** 200K policies, $10M GWP

---

## Open Questions for Engineering

1. **ERC-4626 sub-accounting:** Do we use share classes within a single vault, or separate vaults per sub-account? Separate is simpler but less capital-efficient.

2. **Cross-vault yield:** Both vaults depositing into the same yield strategy requires careful share accounting. Should we use a shared "strategy vault" that both deposit into?

3. **Premium earning schedule:** Linear over 12 months, but on-chain gas cost of updating earned/unearned balance daily is prohibitive. Batch monthly? Or compute on-read?

4. **Oracle design:** Phase 1 multisig is fine, but the attestation chain is already on IPFS — could the oracle simply verify IPFS CIDs on-chain via a Chainlink function?

5. **USDT vs multi-stablecoin:** Start USDT-only for simplicity? Or accept USDC/DAI from day 1 with a swap layer?

6. **Gas chain selection:** Mainnet for trust, or L2 (Base/Arbitrum) for cost? Morpho is on both mainnet and Base.

---

## References

- [ERC-4626 Standard](https://ethereum.org/developers/docs/standards/tokens/erc-4626/)
- [OpenZeppelin ERC-4626](https://docs.openzeppelin.com/contracts/5.x/erc4626)
- [Morpho Blue Documentation](https://docs.morpho.org/)
- [MetaMorpho Vaults](https://app.morpho.org/vaults)
- [Sky (MakerDAO) DSR](https://sky.money/)
- [Safe Multisig](https://safe.global/)
- [Joe Lubin Sky Deposit](https://www.bitget.com/news/detail/12560605184172) — 15,000 ETH collateral, $4.1M DAI borrowed (Feb 2026)
- [Ethereum Foundation Morpho Deposits](https://themerkle.com/ethereum-foundation-expands-defi-strategy-deposits-6m-and-2400-eth-into-morpho-vaults/) — $6M + 2,400 ETH (Oct 2025)

---

*"Insurance is the business of pricing uncertainty + investing float. ClawdSure does both better — on-chain, transparent, and at 2-3× traditional yield."*
