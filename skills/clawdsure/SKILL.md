---
name: ClawdSure
description: "Continuous security attestation for OpenClaw agents. Machine fingerprint + config hash, signed daily, chain-linked, published to IPFS via relay."
---

# ClawdSure

Continuous security attestation for AI agents. Proves a machine maintains good security posture over time.

## How It Works

```
Machine → fingerprint + dual audit → sign → chain → relay
```

1. **Machine fingerprint**: hardware-bound hash (stable, identifies the machine)
2. **Config hash**: SHA-256 of security-relevant OpenClaw config (changes on drift)
3. **Dual audit**: 
   - `openclaw security audit` (native checks)
   - `audit-machine.sh` (filesystem, firewall, skills, operational coherence)
4. **Attestation**: signed record with both audit hashes, linking to previous (append-only chain)
5. **Relay**: POST to api.clawdsure.io — backup and verification (no user accounts needed)
6. **Oracle**: can discover and verify any agent's chain via relay

## Commands

### First time: Enroll
```bash
bash scripts/enroll.sh
```
Generates ECDSA keypair, creates genesis attestation, publishes to relay.

### Daily: Attest
```bash
bash scripts/attest.sh
```
Silent on success. Alerts on FAIL (critical findings) or chain gap >36h.

Set up via launchd/cron for automation.

### Verify chain
```bash
bash scripts/verify.sh
```
Validates signatures, hash linking, time gaps, and continuity.

## When the agent asks you to run ClawdSure

1. Run `bash scripts/attest.sh` (or `CLAWDSURE_VERBOSE=true bash scripts/attest.sh` for output)
2. If FAIL: run `openclaw security audit` and report findings
3. If chain gap warning: attestation was already appended, just note the gap

## Data

```
~/.openclaw/workspace/.clawdsure/
├── agent.key       # ECDSA private key (NEVER SHARE)
├── agent.pub       # Public key (registered with relay)
├── chain.jsonl     # Attestation chain (append-only)
├── last-audit.json # Most recent audit-machine.sh output
└── attest.log      # Run log
```

## Chain Rules

| Condition | Effect |
|-----------|--------|
| Daily PASS | Chain continues ✓ |
| FAIL (critical findings) | 48h to remediate |
| No attestation for 48h | Chain broken ✗ |
| Chain broken | Must re-enroll |

## What Gets Checked

### Native Audit (`openclaw security audit`)
OpenClaw's built-in security checks

### Machine Audit (`audit-machine.sh`)
- **Filesystem**: permissions, world-writable files, synced folders (Dropbox/iCloud)
- **Network**: listening ports
- **Firewall**: macOS/Linux/Windows firewall status
- **Skills**: inventory + pattern scan for suspicious commands
- **Operational**: model allowlist consistency

See `docs/machine-audit.md` for full details.

## Safety

- `agent.key` never leaves the machine
- Attestations reflect actual audit results (never faked)
- Config hash uses only security-relevant fields (secrets are never included)
- Audit outputs are redacted (no token/password leaks)
- Relay receives only: agent ID, public key, signed attestation
