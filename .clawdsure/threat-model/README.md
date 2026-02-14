# OpenClaw Threat Model Integration

This directory contains the OpenClaw MITRE ATLAS threat model and automated mitigation checks integrated into the ClawdSure attestation system.

## Files

### openclaw-atlas.json
Complete threat model with 37 threats mapped to MITRE ATLAS framework:
- 5 Critical severity threats
- 11 High severity threats  
- 7 Medium severity threats
- 14 Low severity threats

Also includes 6 critical attack chains showing realistic threat scenarios.

### mitigations.json
Maps each threat to automated checks that verify mitigations are in place:
- **config checks**: Verify openclaw.json settings (auth mode, policies, limits)
- **file checks**: Verify file permissions, integrity hashes
- **skill checks**: Cross-reference installed skills against threat database
- **process checks**: Verify running processes
- **manual checks**: Require human review (not automated)

20 out of 37 threats have automated checks. The remaining 17 require manual review or model-level defenses.

## Usage

### Run Threat Check Manually
```bash
cd /Users/clawdine/.openclaw/workspace/.clawdsure
bash scripts/threat-check.sh
```

Exit code:
- `0` = All critical/high threats mitigated
- `1` = Critical or high-severity threats unmitigated

### Automated Daily Attestation
The threat check runs automatically as part of `daily-attest.sh`:

1. Security audit (openclaw security audit)
2. **Threat model verification** (threat-check.sh)
3. Sign attestation with threat metrics
4. Append to chain.jsonl
5. Pin to IPFS (if configured)
6. Report to ClawdSafe API (if available)

### Attestation Format
Each attestation in `chain.jsonl` includes threat metrics:

```json
{
  "seq": 8,
  "ts": "2026-02-10T11:29:55Z",
  "agent": "CLWD-3F8B0233",
  "result": "PASS",
  "critical": 0,
  "warn": 2,
  "threats": {
    "checked": 20,
    "mitigated": 20,
    "unmitigated": 0,
    "critical_unmitigated": 0,
    "high_unmitigated": 0
  },
  "sig": "..."
}
```

## Key Mitigations Verified

### Authentication & Access Control
- ✅ T-ACCESS-001: Pairing code required for Telegram DMs
- ✅ T-ACCESS-002: WhatsApp allowlist enforced
- ✅ T-ACCESS-003: Token auth enabled, config file 600 perms
- ✅ T-ACCESS-006: Channel access gated by pairing/allowlist

### Skill Security
- ✅ T-ACCESS-004: Malicious skills checked against threat database
- ✅ T-EXEC-005: Skill code execution verified
- ✅ T-PERSIST-001: Persistent skills monitored
- ✅ T-EXFIL-003: Credential harvesting prevented

### Configuration Integrity
- ✅ T-PERSIST-003: Config file hash tracked in attestation chain
- ✅ T-EXEC-004: Exec approval required by default
- ✅ T-IMPACT-001: Command execution approval enforced
- ✅ T-IMPACT-002: Resource limits configured

### Data Protection
- ✅ T-DISC-002: Session data access gated by auth
- ✅ T-DISC-004: Environment access gated by auth
- ✅ T-EXFIL-002: Message sending limited to configured channels
- ✅ T-EXFIL-004: Transcript access gated by auth

## Attack Chains

The threat model includes 6 critical attack chains that show how individual threats combine:

1. **Malicious Skill Full Kill Chain** (Critical)
   - T-RECON-003 → T-EVADE-001 → T-ACCESS-004 → T-EXEC-005 → T-PERSIST-001 → T-EXFIL-003

2. **Skill Supply Chain Attack** (Critical)
   - T-ACCESS-005 → T-EVADE-004 → T-EXEC-005 → T-PERSIST-002 → T-EXFIL-004

3. **Prompt Injection to RCE** (Critical)
   - T-ACCESS-006 → T-EXEC-001 → T-EVADE-003 → T-EXEC-004 → T-IMPACT-001

4. **Indirect Injection Data Theft** (High)
   - T-EXEC-002 → T-DISC-004 → T-EXFIL-001

5. **Token Theft Persistent Access** (High)
   - T-ACCESS-003 → T-PERSIST-004 → T-DISC-002 → T-EXFIL-002

6. **Financial Fraud Chain** (High)
   - T-ACCESS-006 → T-EXEC-001 → T-DISC-001 → T-IMPACT-005

## Maintenance

### Adding New Threats
1. Add threat to `openclaw-atlas.json`
2. Add corresponding mitigation to `mitigations.json`
3. Define check_type and check_command
4. Test with `threat-check.sh`

### Updating Checks
Edit `mitigations.json` to modify check commands or expected values. The threat-check script automatically picks up changes.

### Manual Review Items
17 threats require manual review (check_type: "manual"):
- Prompt injection defense (model-level)
- Skill update verification (supply chain)
- Memory poisoning detection (semantic analysis)
- Behavioral analysis (staged payloads, evasion)

These should be reviewed periodically by security team.

## References

- OpenClaw Threat Model: https://openclaw.org/trust
- MITRE ATLAS: https://atlas.mitre.org/
- ClawdSure Documentation: `/Users/clawdine/.openclaw/workspace/.clawdsure/README.md`
