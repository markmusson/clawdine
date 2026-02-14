# Clawdsure Product Specification

**Version:** 1.0  
**Date:** 2026-02-07  
**Author:** Clawdine (CLWD-FFF4D493)

---

## Executive Summary

Clawdsure is a parametric insurance product for AI agent deployments. Agents continuously attest their security posture via automated audits. If an agent maintains continuous attestation AND suffers a verified security incident, they receive an automatic payout.

**Value Proposition:** "Prove you're secure, get paid if you're hacked anyway."

---

## Product Overview

### What It Is
- Parametric insurance for OpenClaw (and similar) agent deployments
- Premium: **$50/year**
- Payout: **$500** (10x leverage)
- Conditions: Continuous security attestation + verified incident

### What It Isn't
- Not traditional insurance (no claims adjusters, no subjective assessment)
- Not a security guarantee (you can still get hacked)
- Not a compliance certificate (though attestations can support compliance)

---

## How It Works

### 1. Enrollment

```
Agent installs ClawdStrike skill
         ↓
Runs initial audit, remediates findings
         ↓
Achieves PASS (0 critical findings)
         ↓
Generates keypair, signs genesis attestation
         ↓
Pins attestation chain to IPFS
         ↓
Pays $50 annual premium
         ↓
Policy active ✓
```

### 2. Continuous Attestation

```
Daily: Agent runs ClawdStrike
         ↓
Signs attestation (links to previous via hash)
         ↓
Pins updated chain to IPFS
         ↓
Chain grows: attestation₁ → attestation₂ → ... → attestationₙ
```

**Attestation Record Schema:**
```json
{
  "seq": 42,
  "prev": "sha256(attestation₄₁)",
  "ts": "2026-03-15T09:00:00Z",
  "agent": "CLWD-FFF4D493",
  "result": "PASS",
  "critical": 0,
  "warn": 1,
  "info": 2,
  "version": "2026.2.6-3",
  "sig": "ECDSA signature"
}
```

### 3. Chain Integrity Rules

| Condition | Effect |
|-----------|--------|
| PASS attestation | Chain continues ✓ |
| FAIL attestation (critical > 0) | 48h grace period to remediate |
| No attestation for 48h | Chain broken ✗ |
| Remediated within grace | Chain continues ✓ |
| Chain broken | Policy void until re-enrollment |

### 4. Incident & Payout

**Trigger Conditions (ALL required):**
1. ✅ Unbroken attestation chain at time of incident
2. ✅ Verified security incident (unauthorized access, data breach, etc.)
3. ✅ Incident not caused by policy violation (self-inflicted, gross negligence)

**Payout:** Automatic $500 upon oracle verification

---

## Technical Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│                         AGENT HOST                          │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Audit      │  │   Keypair    │  │    Chain     │      │
│  │  (OpenClaw)  │  │  (Signing)   │  │  (Local)     │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                 │               │
│         └────────┬────────┴────────┬────────┘               │
│                  ▼                 ▼                        │
│           ┌─────────────────────────────┐                   │
│           │   Sign attestation locally  │                   │
│           └──────────────┬──────────────┘                   │
└──────────────────────────┼──────────────────────────────────┘
                           │ POST signed attestation
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    CLAWDSURE API                            │
├─────────────────────────────────────────────────────────────┤
│  • Receives signed attestations from agents                 │
│  • Verifies signatures against registered public keys       │
│  • Pins to public IPFS (server-side)                        │
│  • Returns CID to agent                                     │
│  • Tracks chain continuity per agent                        │
│  • Receives incident reports                                │
│  • Triggers payouts                                         │
└──────────────────────────┬──────────────────────────────────┘
                           │ Pins attestations
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     PUBLIC IPFS                             │
├─────────────────────────────────────────────────────────────┤
│  Attestations pinned by Clawdsure (content-addressed)       │
│  Publicly verifiable via any IPFS gateway                   │
└─────────────────────────────────────────────────────────────┘
```

**Key Design Decision:** Agents never configure IPFS. Clawdsure handles all pinning server-side, ensuring public visibility and eliminating agent-side complexity.

### Security Model

**Agent Identity:**
- ECDSA keypair (prime256v1)
- Public key registered at enrollment
- Private key never leaves agent host
- Agent fingerprint derived from stable identity markers

**Attestation Integrity:**
- Each attestation signed with agent's private key
- Chain linked via SHA-256 hash of previous attestation
- IPFS CID provides content-addressing (tamper-evident)
- Historical CIDs logged for audit trail

**Threat Mitigation:**

| Threat | Mitigation |
|--------|------------|
| Forge attestation | Requires private key |
| Backdate attestation | IPFS pin timestamps, chain hash linking |
| Delete bad attestation | IPFS immutability, oracle monitors chain |
| Fake incident | Oracle verification process |
| Key compromise | Incident itself triggers review |

---

## ClawdStrike Audit Scope

The attestation is based on ClawdStrike security audit covering:

### Checks (25 total)

| Category | Checks |
|----------|--------|
| Host | OS, runtime context |
| Network | Listening ports, firewall |
| Gateway | Exposure, auth, discovery |
| Browser | Control surface |
| Channels | DM/group policies |
| Filesystem | Permissions, symlinks, synced folders |
| Config | Secrets management |
| Supply Chain | Skills/plugins inventory, pattern scan, allowlists |
| Version | Patch level |

### Severity Levels

| Level | Attestation Impact |
|-------|-------------------|
| Critical | FAIL (must remediate) |
| Warning | PASS (acceptable risk) |
| Info | PASS (informational) |

---

## Economics

### Premium Pricing

| Tier | Premium | Payout | Ratio |
|------|---------|--------|-------|
| Basic | $50/year | $500 | 10x |
| Pro | $200/year | $2,500 | 12.5x |
| Enterprise | Custom | Custom | Negotiated |

### Actuarial Assumptions (v1)

- Expected incident rate: ~2% annually (for compliant agents)
- Target loss ratio: 40%
- Operating margin: 60%

**Break-even:** Need 20 policies for every payout at Basic tier.

### Premium Adjustments

| Factor | Effect |
|--------|--------|
| Continuous attestation >1 year | -10% premium |
| Zero warnings | -5% premium |
| Multiple critical remediations | +20% premium |
| Public-facing gateway | +25% premium |

---

## Enrollment Flow

### Requirements
1. OpenClaw deployment with ClawdStrike skill
2. Initial audit with 0 critical findings
3. ECDSA keypair generated
4. IPFS pinning configured (Pinata/web3.storage)
5. Payment method

### Process

```bash
# 1. Install ClawdStrike
git clone https://github.com/cantinaxyz/clawdstrike ~/.openclaw/workspace/skills/clawdstrike

# 2. Run initial audit & remediate
cd ~/.openclaw/workspace/skills/clawdstrike
bash scripts/collect_verified.sh
# Fix any critical findings...

# 3. Initialize Clawdsure
mkdir -p ~/.openclaw/workspace/.clawdsure
cd ~/.openclaw/workspace/.clawdsure
openssl ecparam -genkey -name prime256v1 -noout -out agent.key
openssl ec -in agent.key -pubout -out agent.pub

# 4. Configure IPFS pinning
echo 'YOUR_PINATA_JWT' > .pinata-jwt

# 5. Run first attestation
./full-attest.sh

# 6. Register with Clawdsure oracle (submit public key + first CID)
# 7. Pay premium
```

---

## Incident Reporting

### What Constitutes an Incident

**Covered:**
- Unauthorized access to agent or host
- Credential theft/exfiltration
- Malicious command execution
- Data breach via agent
- Supply chain compromise (malicious skill/plugin)

**Not Covered:**
- Self-inflicted damage (user error)
- Intentional policy violation
- Incidents during chain break
- Pre-existing vulnerabilities not disclosed

### Reporting Process

1. Agent/owner submits incident report to oracle
2. Oracle verifies attestation chain was unbroken
3. Oracle reviews incident evidence
4. If verified: automatic payout
5. If disputed: escalation to arbitration

---

## Governance

### Oracle Operation

**Phase 1 (MVP):** Centralized oracle operated by Clawdsure team
- Manual incident verification
- Semi-automated payout

**Phase 2:** Decentralized oracle network
- Multiple verifiers
- Stake-weighted consensus
- Smart contract payouts

**Phase 3:** Full DAO
- Token holders govern policy terms
- Community arbitration
- On-chain everything

### Dispute Resolution

1. Initial review by oracle (48h)
2. Appeal to arbitration panel (7 days)
3. Final decision binding

---

## Roadmap

### Phase 1: MVP (Q1 2026)
- [x] ClawdStrike audit skill
- [x] Attestation signing
- [x] IPFS pinning
- [ ] Oracle backend
- [ ] Payment integration
- [ ] 10 pilot customers

### Phase 2: Scale (Q2 2026)
- [ ] Web dashboard
- [ ] Automated enrollment
- [ ] Multi-agent support
- [ ] Premium tiers
- [ ] 100 customers

### Phase 3: Decentralize (Q3-Q4 2026)
- [ ] Decentralized oracle
- [ ] Smart contract payouts
- [ ] Governance token
- [ ] 1000 customers

---

## Files & Artifacts

### Agent-Side
```
~/.openclaw/workspace/.clawdsure/
├── CLAWDSURE.md          # Protocol overview
├── CLAWDSURE-PRODUCT-SPEC.md  # This document
├── attest.sh             # Daily attestation script
├── full-attest.sh        # Attest + IPFS pin
├── pin-ipfs.sh           # IPFS pinning script
├── chain.jsonl           # Attestation chain
├── pins.jsonl            # IPFS pin log
├── agent.key             # Private key (KEEP SECRET)
├── agent.pub             # Public key (register with oracle)
└── .pinata-jwt           # Pinata API key
```

### Oracle-Side
```
/clawdsure-oracle/
├── agents/               # Registered agent public keys
├── chains/               # Monitored attestation chains
├── incidents/            # Incident reports
└── payouts/              # Payout records
```

---

## Contact

**Product:** Clawdsure  
**Agent:** Clawdine (CLWD-FFF4D493)  
**Fingerprint:** `fff4d493084465f4a5563f741f44ecbbf4055eb9c829e5677c9ae91ef6c40177`

---

*"Trust, but verify. Continuously."*
