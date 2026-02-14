# ClawdSure

Continuous security attestation for [OpenClaw](https://github.com/openclaw/openclaw) agents.

## What

Every day, your agent proves it's running on the same machine with a secure configuration. Two independent audits (native + machine) are hashed and signed. These attestations form an append-only chain, signed with ECDSA, backed up to the ClawdSure relay.

No IPFS accounts. No Python dependencies. Just bash + jq + openssl. Works on macOS, Linux, WSL.

## Why

After the [ClawHub supply chain attack](https://x.com/DanielLockyer) (Feb 2026), it's clear that AI agents need continuous proof of security posture — not just one-time audits.

ClawdSure provides:
- **Machine identity**: hardware-bound fingerprint that proves which machine is attesting
- **Config integrity**: hash of security-relevant config that detects drift
- **Dual audits**: native OpenClaw checks + custom machine audit (filesystem, firewall, skills, etc.)
- **Verifiable chain**: anyone can verify an agent's attestation history via relay API
- **Token-efficient**: scripts do the work, models only for judgment

## Install

```bash
# Via ClawHub
clawhub install clawdsure

# Or manually
git clone https://github.com/clawdsure/clawdsure.git ~/.openclaw/workspace/skills/clawdsure
```

## Quick Start

```bash
cd ~/.openclaw/workspace/skills/clawdsure

# 1. Enroll (one-time)
bash scripts/enroll.sh

# 2. Daily attestation
bash scripts/attest.sh

# 3. Verify chain
bash scripts/verify.sh
```

## Automate (macOS)

```bash
cat > ~/Library/LaunchAgents/com.clawdsure.daily.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.clawdsure.daily</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>scripts/attest.sh</string>
    </array>
    <key>WorkingDirectory</key>
    <string>~/.openclaw/workspace/skills/clawdsure</string>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key><integer>9</integer>
        <key>Minute</key><integer>0</integer>
    </dict>
</dict>
</plist>
EOF
launchctl load ~/Library/LaunchAgents/com.clawdsure.daily.plist
```

## Automate (Linux)

```bash
# crontab -e
0 9 * * * cd ~/.openclaw/workspace/skills/clawdsure && bash scripts/attest.sh
```

## Architecture

```
┌────────────────────────────────────────┐
│  OpenClaw Machine                       │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │ fingerprint.sh                    │  │──→ machine + config hash
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │ audit-machine.sh (dual audit)    │  │──→ filesystem, firewall,
│  │ openclaw security audit          │  │   skills, network, ops
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │ attest.sh                         │  │──→ sign + chain + publish
│  │ agent.key (never leaves machine)  │  │
│  └──────────────────────────────────┘  │
└────────────┬────────────────────────────┘
             │ POST /v1/attestation
             ▼
┌─────────────────────────────────────────┐
│  ClawdSure Relay (future)                │
│  api.clawdsure.io                        │──→ backup + verification
│                                          │──→ discovery: /v1/agent/{id}
└──────────────────────────────────────────┘
```

**Current**: Local chain only (relay not yet deployed)  
**Future**: Relay API for backup, discovery, and underwriting integration

## Attestation Format

```json
{
  "v": 1,
  "seq": 42,
  "prev": "sha256 of previous attestation",
  "ts": "2026-02-08T09:30:00Z",
  "agent": "CLWD-A1B2C3D4",
  "fingerprint": {
    "machine": "sha256 of hardware UUID",
    "config": "sha256 of security config"
  },
  "audit_native": "sha256 of openclaw security audit output",
  "audit_machine": "sha256 of audit-machine.sh output",
  "result": "PASS",
  "sig": "ECDSA signature (base64)"
}
```

**Dual audit design:**
- `audit_native`: Hash of `openclaw security audit --json` output
- `audit_machine`: Hash of `audit-machine.sh` JSON output (stored in `.clawdsure/last-audit.json`)
- Both must pass for `result: "PASS"`
- Defense in depth: two independent perspectives on security posture

## What Gets Checked

### Native Audit (`openclaw security audit`)
OpenClaw's built-in security checks (config, permissions, network, etc.)

### Machine Audit (`audit-machine.sh`)
- **Filesystem**: permissions, world-writable, SUID/SGID, synced folders
- **Network**: listening ports
- **Firewall**: macOS/Linux/Windows firewall status
- **Skills**: inventory + pattern scan for suspicious commands (curl|bash, wget, etc.)
- **Operational coherence**: model allowlist consistency, referenced models vs allowlist

See `docs/machine-audit.md` for full details.

## Dependencies

- `openssl` (ECDSA signing)
- `jq` (JSON processing)
- `curl` (relay communication - future)
- OpenClaw (native security audit)

All commonly available. No Node.js, Python, or IPFS tools required on the machine.

## Documentation

- `docs/attestation-schema.md` — attestation record format
- `docs/chain-rules.md` — chain integrity rules and grace periods
- `docs/relay-api.md` — relay API specification (future)
- `docs/underwriting.md` — UW criteria, pricing tiers (real domain knowledge)
- `docs/threat-model.md` — threat model for OpenClaw deployments
- `docs/machine-audit.md` — what audit-machine.sh checks and why

## License

MIT
