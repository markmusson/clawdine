# ClawdSure Rebuild Complete

## What Was Built

### 1. ✅ scripts/audit-machine.sh
- Lean cross-platform security checks (macOS, Linux, WSL)
- Outputs JSON to stdout (not file)
- Checks:
  - Filesystem permissions (state dir, config, credentials)
  - World-writable detection
  - SUID/SGID detection
  - Synced folder detection (Dropbox, iCloud, etc.)
  - Network listening ports
  - Firewall status (macOS/Linux/Windows)
  - Skills inventory + pattern scan for suspicious commands
  - Operational coherence (model allowlist consistency)
- Redacts secrets from output
- Exit 0 always (findings are data, not script failures)

### 2. ✅ Updated scripts/attest.sh
- Calls audit-machine.sh and hashes its output
- Includes dual audit hashes in attestation:
  - `audit_native`: openclaw security audit hash
  - `audit_machine`: audit-machine.sh hash
- Stores full audit-machine.sh output in `.clawdsure/last-audit.json`
- Fails attestation if machine audit has `fail` status findings

### 3. ✅ docs/ Directory
Reorganized reference documentation:
- `attestation-schema.md` — updated with dual audit format
- `chain-rules.md` — chain integrity rules (kept from backup)
- `relay-api.md` — relay API spec (renamed from api.md, updated)
- `underwriting.md` — UW criteria, pricing (KEPT - real domain knowledge)
- `threat-model.md` — threat model for OpenClaw (updated)
- `machine-audit.md` — NEW: documents audit-machine.sh checks and rationale

### 4. ✅ Updated SKILL.md
- Added reference to audit-machine.sh
- Updated data structure section
- Added "What Gets Checked" section
- Kept concise (agent instructions, not human docs)

### 5. ✅ Updated README.md
- Updated architecture diagram with dual audit
- Updated attestation format to show audit_native + audit_machine
- Added "What Gets Checked" section
- Documented dependencies
- Added link to docs/

## Verified Working

```bash
$ bash scripts/audit-machine.sh | jq .summary
{
  "ok": 8,
  "warn": 2,
  "fail": 0
}

$ CLAWDSURE_VERBOSE=true bash scripts/attest.sh
✅ #3 | PASS | machine:14d547dd config:c05ff9b7 | local-only

$ tail -1 ~/.openclaw/workspace/.clawdsure/chain.jsonl | jq .
{
  "v": 1,
  "seq": 3,
  "audit_native": "5fede4ea...",
  "audit_machine": "84d2468e...",
  "result": "PASS",
  ...
}

$ cat ~/.openclaw/workspace/.clawdsure/last-audit.json | jq .summary
{
  "ok": 8,
  "warn": 2,
  "fail": 0
}
```

## Design Principles Maintained

✅ Scripts do the work, models only for judgment
✅ Silent on success, loud on failure
✅ No Python dependencies (bash + jq + openssl + curl only)
✅ Cross-platform (macOS, Linux, WSL)
✅ Redacts all secrets in audit output
✅ Everything is deterministic and hashable

## What Was Removed

Per instructions, did NOT bring back:
- report-format.md, evidence-template.md (agent-driven audit report, unnecessary)
- canvas-browser.md, channels.md, tools.md, etc. (check-by-check agent instructions, now in scripts)
- config-keys.md, verified-allowlist.md, redaction.md (implementation details now in scripts)
- incident-flow.md (premature)
- supply-chain.md, version-risk.md, threat-feed.md (hallucinated threat intel)

## File Structure

```
skills/clawdsure/
├── README.md (updated)
├── SKILL.md (updated)
├── docs/
│   ├── attestation-schema.md
│   ├── chain-rules.md
│   ├── relay-api.md
│   ├── underwriting.md
│   ├── threat-model.md
│   └── machine-audit.md (NEW)
└── scripts/
    ├── portable.sh (kept as-is)
    ├── fingerprint.sh (kept as-is)
    ├── enroll.sh (kept as-is)
    ├── attest.sh (UPDATED - dual audit)
    ├── verify.sh (kept as-is)
    ├── publish.sh (kept as-is)
    └── audit-machine.sh (NEW)
```

## Ready for Production

The skill is now:
- Functionally complete (enrollment, attestation, verification, publishing)
- Cross-platform compatible
- Token-efficient (minimal model usage)
- Well-documented (design docs for humans, SKILL.md for agent)
- Tested and working

Next steps (future):
- Deploy ClawdSure relay API
- Add incident reporting feature
- Integrate threat feed checking into audit-machine.sh
- Add skill signature verification
