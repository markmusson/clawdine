# ClawdSure Design Doc: Attestation Schema

**This is a design document, not runtime instructions.**

## Standard Attestation

```json
{
  "v": 1,
  "seq": 42,
  "prev": "sha256-hash-of-previous-attestation",
  "ts": "2026-03-15T09:00:00Z",
  "agent": "CLWD-FFF4D493",
  "fingerprint": {
    "machine": "abc123...",
    "config": "def456..."
  },
  "audit_native": "sha256-of-openclaw-audit-output",
  "audit_machine": "sha256-of-audit-machine-output",
  "result": "PASS",
  "sig": "base64-ecdsa-signature"
}
```

## Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `v` | integer | ✓ | Schema version (currently 1) |
| `seq` | integer | ✓ | Sequence number (1-indexed, monotonic) |
| `prev` | string | ✓ | SHA-256 hash of previous attestation (or "genesis" for first) |
| `ts` | string | ✓ | ISO 8601 timestamp in UTC |
| `agent` | string | ✓ | Agent ID (CLWD-XXXXXXXX format) |
| `fingerprint` | object | ✓ | Machine and config hashes |
| `fingerprint.machine` | string | ✓ | SHA-256 of machine identity |
| `fingerprint.config` | string | ✓ | SHA-256 of openclaw.json |
| `audit_native` | string | ✓ | SHA-256 hash of `openclaw security audit --json` output |
| `audit_machine` | string | ✓ | SHA-256 hash of `audit-machine.sh` JSON output |
| `result` | string | ✓ | "PASS" or "FAIL" |
| `sig` | string | ✓ | Base64-encoded ECDSA signature |

## Genesis Attestation

First attestation uses `prev: "genesis"` and establishes the agent identity.

## Agent ID Format

```
CLWD-XXXXXXXX
     ^^^^^^^^
     First 8 chars of pubkey fingerprint (uppercase)
```

Example:
- Public key hash: `fff4d493084465f4a5563f741f44ecbbf4055eb9c829e5677c9ae91ef6c40177`
- Agent ID: `CLWD-FFF4D493`

## Dual Audit Design

ClawdSure uses **two independent audits** to maximize coverage:

### 1. Native Audit (`audit_native`)
- Uses OpenClaw's built-in `openclaw security audit` command
- Checks config, permissions, network exposure, etc.
- Hash of full JSON output stored in attestation
- Full output retained by agent for local review

### 2. Machine Audit (`audit_machine`)
- Custom script: `audit-machine.sh`
- Cross-platform bash (macOS, Linux, WSL)
- Checks: filesystem permissions, firewall, network, skills patterns, operational coherence
- Outputs structured JSON with findings
- Hash stored in attestation
- Full output saved to `.clawdsure/last-audit.json`

**Why both?**
- Defense in depth
- Native audit may evolve/change; machine audit is pinned to skill version
- Different perspectives: OpenClaw internal view + external system view
- Enables underwriters to assess risk from multiple angles

## Signature

The signature covers the JSON attestation **without** the `sig` field:

```bash
# Create unsigned attestation
UNSIGNED='{"v":1,"seq":42,"prev":"abc...","ts":"...","agent":"...","result":"PASS",...}'

# Sign with ECDSA
echo -n "$UNSIGNED" | openssl dgst -sha256 -sign agent.key | base64 -w0
```

## Chain File Format

The chain is stored in `chain.jsonl` (JSON Lines format):

```jsonl
{"v":1,"seq":1,"prev":"genesis","ts":"2026-02-07T10:00:00Z","agent":"CLWD-FFF4D493","fingerprint":{...},"result":"PASS",...,"sig":"..."}
{"v":1,"seq":2,"prev":"a1b2c3...","ts":"2026-02-08T09:00:00Z","agent":"CLWD-FFF4D493","fingerprint":{...},"result":"PASS",...,"sig":"..."}
{"v":1,"seq":3,"prev":"d4e5f6...","ts":"2026-02-09T09:00:00Z","agent":"CLWD-FFF4D493","fingerprint":{...},"result":"PASS",...,"sig":"..."}
```

### Properties
- One attestation per line
- Append-only (never modify existing lines)
- `prev` of line N = SHA-256 of line N-1
- Sequence numbers are consecutive (no gaps)

## Hash Linking

Each attestation's `prev` field contains the SHA-256 hash of the **entire previous line** (including signature):

```bash
# Hash of previous attestation (full JSON line)
PREV_HASH=$(tail -1 chain.jsonl | shasum -a 256 | cut -c1-64)
```

This creates a tamper-evident chain:
- Modifying any attestation breaks all subsequent `prev` hashes
- Cryptographic proof of chain integrity
- Relay server provides additional backup/verification

## Result Values

| Value | Meaning | Chain Effect |
|-------|---------|--------------|
| `PASS` | No critical/fail findings | Chain continues |
| `FAIL` | Critical findings or machine audit failures | 48h grace period |

## Validation Rules

### Per-Attestation
1. `v` must be 1
2. `seq` must equal line number in file
3. `prev` must match SHA-256 of previous line (or "genesis" for seq=1)
4. `sig` must verify against registered public key
5. `ts` must be valid ISO 8601 UTC timestamp
6. `result` must be "PASS" or "FAIL"
7. Both `audit_native` and `audit_machine` must be valid SHA-256 hashes

### Chain-Wide
1. No gaps in sequence numbers
2. Timestamps must be monotonically increasing
3. No timestamp gap >48h (chain break)
4. All agent IDs must match
