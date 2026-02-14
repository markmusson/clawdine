# Clawdsure Parametric Insurance Protocol

## Overview
Agent-operated parametric insurance for OpenClaw deployments. Pay premium, maintain continuous security attestation, get payout if hacked.

## Economics
- **Premium**: $50/year
- **Payout**: $500 (if conditions met)
- **Leverage**: 10x
- **Conditions**: Continuous attestation + verified incident

## Attestation Model

### Certificate Chain
Each attestation includes hash of previous attestation, creating an immutable chain:

```
attestation_n.prev_hash = sha256(attestation_n-1)
```

### Continuous Attestation Schedule
- **Frequency**: Daily (via launchd/cron)
- **Tool**: ClawdStrike
- **Requirement**: 0 critical findings for valid attestation
- **Grace period**: 48 hours for remediation before chain breaks

### Certificate Fields
```json
{
  "certificate_type": "clawdsure_security_attestation",
  "version": "1.0",
  "sequence": 1,
  "prev_hash": null,
  "agent": {
    "id": "string",
    "fingerprint": "sha256",
    "host": "string"
  },
  "audit": {
    "tool": "clawdstrike",
    "timestamp": "ISO8601",
    "result": "PASS|FAIL",
    "findings": { "critical": 0, "warn": 0, "info": 0 },
    "acceptable_risks": ["string"],
    "openclaw_version": "string"
  },
  "signature": "base64(ec_sign(attestation))"
}
```

## Claim Process

### Trigger Conditions
1. **Continuous attestation**: Unbroken chain of PASS attestations
2. **Incident verified**: 
   - Unauthorized access detected (logs, anomalies)
   - Root cause identified
   - Not self-inflicted or policy violation

### Payout
- Automatic if oracle verifies both conditions
- Smart contract or manual adjudication

## Implementation

### Daily Attestation Job
```bash
# /Users/clawdine/.openclaw/workspace/.clawdsure/attest.sh
#!/bin/bash
cd /Users/clawdine/.openclaw/workspace/skills/clawdstrike
bash scripts/collect_verified.sh
# Parse results, generate attestation, sign, append to chain
```

### Chain Storage
- Local: `~/.clawdsure/chain.jsonl`
- Remote: IPFS pin / blockchain anchor (optional)

## Public Key
```
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE...
-----END PUBLIC KEY-----
```

Agent: CLWD-FFF4D493
Fingerprint: fff4d493084465f4a5563f741f44ecbbf4055eb9c829e5677c9ae91ef6c40177
