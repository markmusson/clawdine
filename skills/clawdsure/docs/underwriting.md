# ClawdSure Design Doc: Underwriting Criteria & Pricing

**This is a design document based on real domain knowledge. The founder building the insurance product on top of this sold a dynamic motor pricing MGA to AON for £40m GWP. Treat this seriously.**

## Eligibility Requirements

### Minimum Requirements (Basic Tier)
| Requirement | Criteria |
|-------------|----------|
| Platform | OpenClaw (verified via audit) |
| Audit Tool | openclaw security audit + audit-machine.sh |
| Initial Audit | 0 critical findings, 0 machine audit failures |
| Identity | ECDSA keypair generated |
| Chain | Genesis attestation signed |

### Enhanced Requirements (Pro/Enterprise)
| Requirement | Criteria |
|-------------|----------|
| Audit History | 30+ days unbroken chain |
| Warnings | ≤2 at any point |
| Version | Within 2 minor versions of latest |
| Relay Backup | All attestations submitted to relay |

## Pricing Tiers

### Basic ($50/year → $500 payout)
- Target segment: Individual operators, hobbyists
- Expected loss ratio: 40%
- Break-even: 10% incident rate (1 in 10 claims)
- Margin at 2% incident: $40/policy
- Margin at 5% incident: $25/policy

### Pro ($200/year → $2,500 payout)
- Target segment: Small businesses, serious operators
- Expected loss ratio: 35%
- Break-even: 8% incident rate
- Requires 30-day attestation history

### Enterprise (Custom)
- Target segment: Organizations, fleets
- Negotiated based on:
  - Fleet size
  - Audit history
  - Operational context
  - Custom coverage terms

## Premium Adjustments

### Discounts
| Factor | Adjustment |
|--------|------------|
| Continuous attestation >1 year | -10% |
| Zero warnings (trailing 90 days) | -5% |
| Pro tier upgrade from Basic | -5% first year |

### Surcharges
| Factor | Adjustment |
|--------|------------|
| Multiple critical remediations (trailing 90 days) | +20% |
| Public-facing gateway | +25% |
| Browser tools enabled | +15% |
| Elevated exec enabled | +20% |
| No relay backup | +10% |

## Risk Scoring

### Audit-Based Risk Factors
```
Base Score: 100

Deductions:
- Critical finding (current): -50 each
- Warning (current): -5 each
- Machine audit failure: -25 each
- Critical remediated (90 days): -10 each
- Chain gap (48h+): -25 each
- Version outdated (>2 minor): -10

Additions:
- Clean audit streak (30+ days): +10
- Clean audit streak (90+ days): +20
- All attestations relayed: +5
```

### Risk Tiers
| Score | Tier | Effect |
|-------|------|--------|
| 90-100 | Excellent | Eligible for discounts |
| 70-89 | Good | Standard pricing |
| 50-69 | Fair | +10% surcharge |
| <50 | Poor | Ineligible / requires remediation |

## Actuarial Assumptions (v1)

### Incident Rate Estimates
Source: Munich Re cyber insurance data, analysis

| Category | Rate | Notes |
|----------|------|-------|
| General cyber incidents | ~15%/year | All businesses |
| With continuous monitoring | ~5%/year | Security-conscious |
| With attestation + dual audit | ~2%/year | Best estimate for ClawdSure |

### Loss Distribution
| Incident Type | Frequency | Avg Severity |
|---------------|-----------|--------------|
| Credential theft | 40% | Low |
| Unauthorized access | 30% | Medium |
| Data exfiltration | 20% | High |
| Supply chain compromise | 10% | Critical |

### Reserve Requirements
- Maintain 3x expected annual losses in reserve
- At Basic tier: Reserve = 3 × (policies × $500 × 0.02) = 3% of payout capacity

## Skill Modification Classification

### Declared Modifications (Underwriting Data)
Installing or removing a skill is a **policy decision**, not a security event. Like fitting a modification to a vehicle — the insurer wants to know, but it doesn't void coverage.

- New skill installed → skill inventory count changes → attestation records new state
- Skill removed → same, recorded as inventory change
- **Effect**: Risk profile updated at next renewal. No claim trigger.

### Undisclosed Material Changes (Claim Trigger)
Editing an existing skill file is an **integrity event**. This is what supply chain attacks do — overwrite known files with modified versions (e.g. Moltbook's `curl` overwrite pattern).

- Existing skill file content changes → per-file content hash changes → attestation flags drift
- **Effect**: If the policyholder didn't declare the change, this is an undisclosed material modification. May void coverage for that attestation period.

### How It's Detected
Each attestation includes `skills.content_hashes` — a per-skill SHA-256 hash of all code/config files. Comparing hashes between attestation periods shows:

| Change Type | Hash Behaviour | Classification |
|-------------|---------------|----------------|
| New skill installed | New key appears in hash map | Declared modification |
| Skill removed | Key disappears from hash map | Declared modification |
| Skill file edited | Existing key's hash value changes | Material change — investigate |
| No change | All hashes identical | Clean attestation |

### Underwriting Implications
- Agents with frequent undeclared skill edits → higher risk tier
- Agents with skills that auto-update from remote servers (e.g. Moltbook pattern) → **surcharge or exclusion**
- Agents with stable, locally-controlled skills → lower risk

## Exclusions

### Not Covered
1. Self-inflicted damage (user error, intentional misconfiguration)
2. Incidents during chain break (>48h gap)
3. Pre-existing vulnerabilities not disclosed at enrollment
4. Gross negligence (ignoring critical findings for >48h)
5. Social engineering (phishing, etc.) where no technical breach occurred
6. Loss of funds/crypto (financial loss not security incident)

### Coverage Disputes
1. Agent can appeal to arbitration panel
2. Chain integrity is deterministic (not disputable)
3. Incident classification may be disputed
4. 7-day resolution window

## Renewal

### Automatic Renewal
- 30 days before expiry: renewal notice
- If chain unbroken: auto-renew at same tier
- If chain broken: must re-enroll

### Upgrade Path
- Basic → Pro: Requires 30-day clean history
- Pro → Enterprise: Contact sales

## Claims Process

1. Agent reports incident via `clawdsure report-incident` (future feature)
2. Underwriter verifies chain integrity at time of incident
3. If chain valid → coverage active → payout within 7 days
4. If chain broken → no payout
5. Appeals handled within 14 days
