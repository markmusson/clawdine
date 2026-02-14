# ClawdSure Design Doc: Chain Integrity Rules

**This is a design document, not runtime instructions.**

## Core Principle

The attestation chain is the source of truth for coverage eligibility. An unbroken chain proves continuous security compliance.

## Chain States

### ✅ VALID
- All attestations signed correctly
- All hash links verified
- No gaps >48h
- Coverage active

### ⚠️ GRACE PERIOD
- Most recent attestation is FAIL
- <48h since FAIL
- Agent has time to remediate
- Coverage still active

### ❌ BROKEN
- Gap >48h between attestations, OR
- FAIL attestation not remediated within 48h
- Coverage void
- Must re-enroll

## State Transitions

```
                              ┌─────────────────┐
                              │                 │
                    PASS      │     VALID       │◄────┐
              ┌──────────────►│                 │     │
              │               └────────┬────────┘     │
              │                        │              │
              │                   FAIL │              │ PASS + 
              │                        │              │ remediated
              │                        ▼              │
              │               ┌─────────────────┐     │
              │               │                 │     │
              │               │  GRACE PERIOD   │─────┘
              │               │   (48h max)     │
              │               └────────┬────────┘
              │                        │
              │              >48h or   │
              │              no attest │
              │                        ▼
              │               ┌─────────────────┐
              │               │                 │
              └───────────────│     BROKEN      │
                 re-enroll    │                 │
                              └─────────────────┘
```

## Detailed Rules

### Rule 1: Daily Attestation Required
- Maximum allowed gap: **48 hours**
- Recommended: Run daily (24h intervals)
- Buffer: 48h allows for maintenance, travel, outages

### Rule 2: PASS Continues Chain
- Any attestation with `result: "PASS"` continues coverage
- PASS means both audits (native + machine) found no critical issues
- Warnings don't affect chain status

### Rule 3: FAIL Triggers Grace Period
- Attestation with `result: "FAIL"` starts grace period
- Caused by: critical findings in native audit OR fails in machine audit
- Grace period starts at FAIL timestamp
- Agent has 48h to:
  1. Fix critical findings
  2. Run new attestation
  3. Submit PASS attestation

### Rule 4: Grace Period Resolution
- **Remediated**: PASS attestation within 48h → chain continues
- **Not remediated**: >48h since FAIL without PASS → chain broken

### Rule 5: Chain Break Consequences
- Coverage immediately void
- No payouts for incidents after break
- Must re-enroll (new genesis attestation)
- Previous chain archived but not reactivated

### Rule 6: Re-enrollment After Break
- Run fresh audits (must achieve PASS)
- New genesis attestation
- New agent ID (or keep old one with new chain)
- 30-day probation (reduced payout tier per underwriting rules)

## Time Gap Calculations

### Normal Operation
```
Attestation N:   2026-02-07T09:00:00Z
Attestation N+1: 2026-02-08T09:00:00Z
Gap: 24h ✓
```

### Maximum Allowed
```
Attestation N:   2026-02-07T09:00:00Z
Attestation N+1: 2026-02-09T08:59:59Z
Gap: 47h 59m 59s ✓
```

### Chain Break
```
Attestation N:   2026-02-07T09:00:00Z
Attestation N+1: 2026-02-09T09:00:01Z
Gap: 48h 0m 1s ✗ CHAIN BROKEN
```

## Grace Period Examples

### Example 1: Remediated in Time
```
Day 1, 09:00: Attestation #42 - PASS
Day 2, 09:00: Attestation #43 - FAIL (critical found)
              Grace period starts
Day 2, 15:00: Agent remediates issue
Day 2, 15:30: Attestation #44 - PASS
              Grace period ends, chain continues ✓
```

### Example 2: Not Remediated
```
Day 1, 09:00: Attestation #42 - PASS
Day 2, 09:00: Attestation #43 - FAIL (critical found)
              Grace period starts (48h)
Day 4, 09:01: Attestation #44 - PASS (too late)
              CHAIN BROKEN ✗
              Must re-enroll
```

### Example 3: Multiple FAILs
```
Day 1, 09:00: Attestation #42 - PASS
Day 2, 09:00: Attestation #43 - FAIL
Day 2, 15:00: Attestation #44 - FAIL (different issue)
              Grace period RESETS from #44
Day 4, 14:59: Attestation #45 - PASS
              Just in time ✓
```

## Verification Checklist

When verifying a chain:

1. ☐ Genesis attestation present (seq=1, prev="genesis")
2. ☐ All sequence numbers consecutive (no gaps)
3. ☐ All `prev` hashes match SHA-256 of previous line
4. ☐ All signatures verify against public key
5. ☐ All timestamps in chronological order
6. ☐ No timestamp gaps >48h
7. ☐ Any FAIL attestations have PASS within 48h

## Edge Cases

### Timezone Handling
- All timestamps MUST be UTC
- Local time conversion is client responsibility
- Server validates UTC timestamps only

### Clock Skew
- Attestation timestamp must be within 5 minutes of server time
- Future timestamps rejected
- Past timestamps allowed (for catch-up after outage)

### Duplicate Attestations
- Same `seq` number rejected
- Same `prev` hash indicates fork (rejected)
- Append-only: no modifications

### Partial Chain Recovery
Not supported. If chain is broken:
- Previous attestations remain valid for historical record
- Cannot graft new attestations onto old chain
- Fresh start required
