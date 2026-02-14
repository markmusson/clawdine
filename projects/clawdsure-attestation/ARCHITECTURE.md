# ClawdSure Attestation Suite — Architecture v2.0

**Author:** Clawdine  
**Date:** 2026-02-14  
**Status:** Design — awaiting approval

---

## Executive Summary

ClawdSure v2 is a comprehensive attestation suite for AI agents, built on soul-guardian's tamper-evident primitives and extended to cover all dimensions of agent security posture.

**Core principle:** Every attestable aspect of an agent gets an approved baseline, continuous drift detection, and immutable audit trail in a single hash-chained log.

**What changes from v1:**
- v1: hodgepodge of scripts bolted together
- v2: unified attestation framework with consistent primitives across all asset types

**Insurance value:** Underwriters get cryptographic proof not just of "hardened today" but of continuous integrity verification across the entire agent lifecycle.

---

## 1. Attestation Primitives (The soul-guardian Pattern)

### 1.1 Core Concepts

**Baseline:**
- Approved state of an asset (file, config, inventory)
- SHA256 hash + snapshot
- Approval requires explicit actor + note
- Stored immutably (separate from live state)

**Drift:**
- Detected difference between current state and approved baseline
- Triggers event in audit log
- Policy determines response (restore, alert, ignore)

**Event:**
- Immutable record of state change
- Hash-chained to previous event (tamper-evident)
- Includes: timestamp, actor, asset, action, hashes, note

**Chain:**
- Append-only JSONL file
- Each line: `{event, ts, actor, asset, prev_chain_hash, chain_hash, signature}`
- Genesis: `prev_chain_hash = "0" × 64`
- Verification: recompute chain from genesis, check every link

**Policy:**
- Per-asset mode: `restore` (auto-fix), `alert` (notify only), `ignore` (skip)
- Defined in `policy.json`
- Example: SOUL.md → restore, CVE data → alert, memory/ → ignore

### 1.2 Why This Pattern Works

**Tamper-evident:** Can't retroactively forge events without breaking chain.  
**Auditable:** Every change has actor, timestamp, reason.  
**Verifiable:** Underwriters recompute chain hash, verify signatures.  
**Flexible:** Same primitives work for files, config, inventory, anything with state.

---

## 2. Asset Types

### 2.1 File Assets
**Examples:** SOUL.md, AGENTS.md, openclaw.json, TOOLS.md, IDENTITY.md

**Baseline:**
- SHA256 of approved file content
- Full snapshot stored in `baselines/files/<path>/`

**Drift detection:**
- Read current file, compute SHA256
- Compare to approved baseline
- If different: log event, execute policy (restore/alert)

**Policy modes:**
- `restore`: SOUL.md, AGENTS.md (core identity must be immutable)
- `alert`: TOOLS.md, USER.md, openclaw.json (notify but don't auto-restore)
- `ignore`: memory/*.md, .clawdsure/*.jsonl (expected to change)

**Integration:** Direct adoption of soul-guardian file monitor.

---

### 2.2 Config Assets
**Examples:** Model settings, auth profiles, tool allowlists, plugin config

**Baseline:**
- Canonical JSON of config section
- SHA256 of serialized config

**Drift detection:**
- On `config.patch` or `config.apply`, compute new config hash
- Compare to approved baseline
- If different: log event with old→new diff

**Policy modes:**
- `alert`: notify on any config change
- Manual approval required after change: `attest approve config --note "switched to Sonnet for cost"`

**Event schema:**
```json
{
  "event": "config_drift",
  "ts": "2026-02-14T09:35:00Z",
  "actor": "clawdine",
  "asset": "config.agents.defaults.model",
  "baseline_hash": "abc123...",
  "current_hash": "def456...",
  "diff": {
    "old": "anthropic/claude-opus-4-6",
    "new": "anthropic/claude-sonnet-4-5"
  },
  "note": "cost reduction",
  "prev_chain_hash": "xyz789...",
  "chain_hash": "qrs012...",
  "signature": "..."
}
```

---

### 2.3 CVE/Advisory Assets
**Source:** ClawSec advisory feed (`~/.openclaw/clawsec-suite-feed-state.json`)

**Baseline:**
- Approved set of known CVEs: `{advisory_id: {severity, status, discovered}}`
- SHA256 of canonical JSON

**Drift detection:**
- On feed update (clawsec-suite hook), diff new advisories vs baseline
- New CVEs = drift
- Log event with new CVE details

**Policy modes:**
- `alert`: always notify on new CVEs
- Manual approval after review: `attest approve cve --note "CVE-2026-1234 reviewed, patched in 2026.2.13"`

**Event schema:**
```json
{
  "event": "cve_drift",
  "ts": "2026-02-14T09:00:00Z",
  "actor": "clawsec-hook",
  "asset": "cve_database",
  "baseline_count": 42,
  "current_count": 45,
  "new_cves": [
    {"id": "CVE-2026-1234", "severity": "high", "title": "..."}
  ],
  "note": "clawsec-suite feed update",
  "prev_chain_hash": "...",
  "chain_hash": "...",
  "signature": "..."
}
```

**Integration:** ClawSec advisory feed becomes a monitored asset, not a separate system.

---

### 2.4 Audit Result Assets
**Source:** `openclaw security audit --json --deep`

**Baseline:**
- Approved audit outcome: `{check_id: {status, detail}}`
- SHA256 of canonical JSON

**Drift detection:**
- Daily audit run (openclaw-audit-watchdog)
- Compare new results vs approved baseline
- New failures = drift

**Policy modes:**
- `alert`: notify on new FAIL or WARN
- Manual approval after remediation: `attest approve audit --note "fixed sandbox.mode warning by design"`

**Event schema:**
```json
{
  "event": "audit_drift",
  "ts": "2026-02-14T09:30:00Z",
  "actor": "daily-audit",
  "asset": "security_audit",
  "baseline_summary": {"ok": 15, "warn": 2, "fail": 0},
  "current_summary": {"ok": 14, "warn": 3, "fail": 0},
  "new_findings": [
    {"check": "skills.pattern_scan", "status": "warn", "detail": "12 patterns (was 10)"}
  ],
  "note": "daily audit #13",
  "prev_chain_hash": "...",
  "chain_hash": "...",
  "signature": "..."
}
```

**Integration:** openclaw-audit-watchdog output feeds into attestation chain.

---

### 2.5 Skills Inventory Assets
**Source:** Installed skills in `~/.openclaw/workspace/skills/`

**Baseline:**
- Approved skills list: `{skill_name: {version, sha256, clawhub_verified}}`
- SHA256 of canonical JSON

**Drift detection:**
- On skill install/update (clawhub hook)
- Compare current inventory vs approved baseline
- New skills or changed hashes = drift

**Policy modes:**
- `alert`: notify on any skill changes
- Manual approval after review: `attest approve skills --note "installed clawsec-suite v0.0.10"`

**Event schema:**
```json
{
  "event": "skills_drift",
  "ts": "2026-02-14T09:19:00Z",
  "actor": "clawhub",
  "asset": "skills_inventory",
  "baseline_count": 5,
  "current_count": 6,
  "added": [
    {"skill": "clawsec-suite", "version": "0.0.10", "sha256": "..."}
  ],
  "removed": [],
  "modified": [],
  "note": "clawhub install clawsec-suite",
  "prev_chain_hash": "...",
  "chain_hash": "...",
  "signature": "..."
}
```

**Integration:** ClawHub install/update triggers drift event, awaits approval.

---

### 2.6 Network/Firewall Assets
**Source:** `netstat -an`, macOS firewall status, listening ports

**Baseline:**
- Approved network posture: `{listening_ports: [...], firewall_enabled: true}`
- SHA256 of canonical JSON

**Drift detection:**
- Daily check (part of security audit)
- Compare current network state vs approved baseline
- New listening ports or firewall disabled = drift

**Policy modes:**
- `alert`: notify on changes
- Manual approval: `attest approve network --note "added port 8080 for local dev"`

**Event schema:**
```json
{
  "event": "network_drift",
  "ts": "2026-02-14T09:30:00Z",
  "actor": "daily-audit",
  "asset": "network_posture",
  "baseline": {"listening_ports": [18789, 22], "firewall": "enabled"},
  "current": {"listening_ports": [18789, 22, 8080], "firewall": "enabled"},
  "diff": {"added_ports": [8080]},
  "note": "daily audit detected new listener",
  "prev_chain_hash": "...",
  "chain_hash": "...",
  "signature": "..."
}
```

---

## 3. Chain Structure

### 3.1 Single Canonical Chain
**Location:** `~/.clawdsure/attestation.jsonl`

**Why one chain:**
- Unified audit trail (no separate logs to correlate)
- Single verification entry point for underwriters
- Chronological event ordering (files, config, CVEs, audits all interleaved)

**Event ordering:**
- Append-only (events added in chronological order)
- Hash chain prevents reordering
- Timestamp + chain position = verifiable timeline

---

### 3.2 Event Schema (Unified)

```json
{
  "schema_version": "2.0",
  "event": "drift|approve|restore|init",
  "ts": "2026-02-14T09:30:00Z",
  "actor": "clawdine|heartbeat|clawhub|clawsec-hook|user",
  "asset_type": "file|config|cve|audit|skills|network",
  "asset": "SOUL.md|config.agents.defaults.model|cve_database|...",
  "baseline_hash": "abc123...",
  "current_hash": "def456...",
  "action": "restored|alerted|approved",
  "diff": {...},
  "note": "human-readable reason",
  "prev_chain_hash": "xyz789...",
  "chain_hash": "sha256(canonical_json(this_event))",
  "signature": "ed25519_detached_signature"
}
```

**Required fields:** `schema_version`, `event`, `ts`, `actor`, `asset_type`, `asset`, `prev_chain_hash`, `chain_hash`

**Optional fields:** `baseline_hash`, `current_hash`, `action`, `diff`, `note`, `signature`

**Chain hash computation:**
```python
canonical = json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
chain_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
```

**Signature (optional for insurance tier):**
- Ed25519 detached signature over `chain_hash`
- Private key stored in macOS Keychain
- Public key pinned in policy (verifiable out-of-band)

---

### 3.3 Genesis Event

```json
{
  "schema_version": "2.0",
  "event": "init",
  "ts": "2026-02-14T10:00:00Z",
  "actor": "setup",
  "asset_type": "chain",
  "asset": "attestation_chain",
  "note": "ClawdSure v2 attestation suite initialized",
  "prev_chain_hash": "0000000000000000000000000000000000000000000000000000000000000000",
  "chain_hash": "...",
  "signature": "..."
}
```

---

## 4. Approval Workflow

### 4.1 Initialization

**Command:** `clawdsure init`

**Actions:**
1. Create `~/.clawdsure/` state directory
2. Write `policy.json` (default policies for all asset types)
3. Scan current state (files, config, CVEs, audits, skills, network)
4. Write approved baselines for all assets
5. Write genesis event to `attestation.jsonl`

**Output:**
```
ClawdSure v2 initialized.

Baselines created:
- 7 files (SOUL.md, AGENTS.md, ...)
- 5 config sections
- 42 CVEs in database
- 18 audit checks
- 6 installed skills
- 2 network listeners

Genesis event: chain_hash a1b2c3d4...

Next: run 'clawdsure check' to monitor for drift.
```

---

### 4.2 Drift Detection

**Command:** `clawdsure check [--asset-type <type>] [--output-format alert|json]`

**Actions:**
1. Load policy + approved baselines
2. Scan current state for specified asset types (default: all)
3. Compare current vs baseline for each asset
4. For drift:
   - Execute policy (restore/alert)
   - Append event to chain
   - Output alert or JSON summary

**Automated triggers:**
- Heartbeat (every 55min): `clawdsure check --asset-type file --output-format alert`
- Daily audit (9:30am): `clawdsure check --output-format json` (all assets)
- ClawSec hook (on CVE update): `clawdsure check --asset-type cve`
- Config change (on restart): `clawdsure check --asset-type config`

**Output (alert format):**
```
🚨 CLAWDSURE DRIFT DETECTED

Asset: SOUL.md (file)
Mode: restore
Status: ✅ RESTORED to approved baseline
Expected: abc123def456...
Found:    789xyz000111...
Diff: ~/.clawdsure/patches/20260214T093000-SOUL-drift.patch

Asset: cve_database
Mode: alert
Status: ⚠️ NEW CVE DETECTED
CVE-2026-1234 (high): Prompt injection in skill-loader

Review changes:
  clawdsure diff SOUL.md
  clawdsure diff cve_database

Approve after review:
  clawdsure approve SOUL.md --note "reverted malicious edit"
  clawdsure approve cve_database --note "CVE reviewed, will patch"
```

---

### 4.3 Manual Approval

**Command:** `clawdsure approve <asset> [--note <reason>]`

**Actions:**
1. Read current state of asset
2. Update approved baseline to current state
3. Append `approve` event to chain
4. Clear drift status for asset

**Use cases:**
- After fixing a security issue: `clawdsure approve audit --note "fixed skills.pattern_scan warning"`
- After intentional config change: `clawdsure approve config --note "switched to Sonnet for cost"`
- After reviewing CVE: `clawdsure approve cve_database --note "CVE-2026-1234 not applicable"`
- After installing skill: `clawdsure approve skills --note "installed clawsec-suite, reviewed source"`

**Approval requires:**
- Actor (defaults to `$USER`, override with `--actor`)
- Note (mandatory, explains WHY approval is granted)

---

### 4.4 Restore

**Command:** `clawdsure restore <asset>`

**Actions:**
1. Load approved baseline for asset
2. Restore current state to baseline
3. Quarantine current state (for forensics)
4. Append `restore` event to chain

**Use cases:**
- Manual restore after failed auto-restore
- Rollback after reviewing drift and deciding current state is bad

**Automatic restore:**
- Policy mode `restore` assets (SOUL.md, AGENTS.md) are restored on every `check`
- No manual restore needed unless auto-restore fails

---

## 5. Verification Interface (For Underwriters)

### 5.1 Chain Verification

**Command:** `clawdsure verify [--from <date>] [--to <date>] [--public-key <path>]`

**Actions:**
1. Load attestation chain
2. Verify chain integrity:
   - Genesis event has `prev_chain_hash = "0" × 64`
   - Each event's `prev_chain_hash` matches previous event's `chain_hash`
   - Recompute `chain_hash` for each event, verify matches recorded value
3. Verify signatures (if present):
   - Load public key
   - Verify Ed25519 signature for each event
4. Output verification report

**Output:**
```
ClawdSure Chain Verification

Chain: ~/.clawdsure/attestation.jsonl
Events: 487 (from 2026-02-01 to 2026-02-14)

Genesis: ✅ VALID
  Event 0: chain_hash a1b2c3d4... (2026-02-01T10:00:00Z)

Hash Chain: ✅ VALID
  All 487 events correctly linked

Signatures: ✅ VALID (486/487)
  Public key: 35866e1b1479a043...
  Failed: Event 42 (signature missing)

Asset Coverage:
  Files:   142 events (7 assets)
  Config:  23 events (5 assets)
  CVE:     18 events (42 CVEs tracked)
  Audit:   14 events (18 checks)
  Skills:  11 events (6 skills)
  Network: 8 events (2 listeners)

Drift Events: 87 total
  Restored: 64 (SOUL.md × 32, AGENTS.md × 32)
  Alerted:  23 (config × 12, CVE × 8, audit × 3)

Last Attestation: 2026-02-14T09:30:00Z (Event 487)
  All checks: PASS
  Machine: 4edbae61
  Config:  c05ff9b7

Chain Status: ✅ TAMPER-EVIDENT INTEGRITY VERIFIED
```

### 5.2 Export for Underwriters

**Command:** `clawdsure export --from <date> --to <date> --output <path>`

**Actions:**
1. Extract events in date range
2. Bundle with:
   - Chain verification report
   - Public key (for signature verification)
   - Policy file (shows approved baselines)
   - Diff patches (for file drift events)
3. Write to tarball or ZIP

**Output structure:**
```
clawdsure-export-2026-02-14.tar.gz
├── attestation.jsonl (filtered events)
├── verification-report.txt
├── public-key.pem
├── policy.json
└── patches/
    ├── 20260214T093000-SOUL-drift.patch
    └── ...
```

**Underwriter workflow:**
1. Receive export bundle
2. Run `clawdsure verify` on extracted chain (independent verification tool)
3. Review drift events, patches, approval notes
4. Assess risk based on:
   - Frequency of drift (more drift = higher risk)
   - Restoration success rate (failed restores = compromise)
   - Approval rationale quality (vague notes = red flag)
   - Chain integrity (broken chain = reject claim)

---

## 6. ClawSec Integration

### 6.1 clawsec-suite
**Role:** CVE feed provider

**Integration:**
- ClawSec advisory feed state (`~/.openclaw/clawsec-suite-feed-state.json`) becomes a monitored asset
- On feed update (clawsec-advisory-guardian hook), trigger `clawdsure check --asset-type cve`
- New CVEs generate drift event, await approval

**Hook modification:**
```javascript
// In clawsec-advisory-guardian/handler.ts, after unseenMatches detection:
if (unseenMatches.length > 0) {
  // Existing: push alert to event.messages
  event.messages.push(buildAlertMessage(unseenMatches, installRoot));
  
  // New: trigger ClawdSure drift check
  execSync('clawdsure check --asset-type cve', {stdio: 'inherit'});
}
```

---

### 6.2 openclaw-audit-watchdog
**Role:** Daily audit runner + formatter

**Integration:**
- Audit results (`openclaw security audit --json --deep`) become a monitored asset
- On audit run (23:00 daily), parse JSON output and trigger `clawdsure check --asset-type audit`
- New failures generate drift event, await approval

**Cron payload modification:**
```bash
# Run audits
audit_json=$(openclaw security audit --json --deep)

# Feed into ClawdSure
echo "$audit_json" > /tmp/audit-results.json
clawdsure check --asset-type audit --input /tmp/audit-results.json

# Format report (existing logic)
clawdsure report --output telegram --channel telegram --to 7018377788
```

---

### 6.3 soul-guardian
**Role:** Foundation pattern (files only)

**Integration:**
- soul-guardian becomes the file asset monitor within ClawdSure
- Instead of running `soul_guardian.py` standalone, ClawdSure calls its primitives:
  - `check_drift(path, baseline)` → detect file changes
  - `restore_file(path, baseline)` → auto-restore on drift
  - `write_audit_event(event)` → append to ClawdSure chain (not soul-guardian's own log)

**Code reuse:**
- soul-guardian's `soul_guardian.py` functions become ClawdSure library functions
- ClawdSure's file asset monitor imports from soul-guardian
- soul-guardian's standalone CLI becomes thin wrapper around ClawdSure: `soul_guardian.py check` → `clawdsure check --asset-type file`

**Migration:**
- Existing soul-guardian state (`memory/soul-guardian/`) migrated to ClawdSure state (`~/.clawdsure/`)
- Existing soul-guardian audit log imported into ClawdSure chain (with chain hash recalculation)

---

## 7. Implementation Plan

### Phase 1: Core Framework (Week 1)
**Goal:** Build attestation primitives + chain structure

**Tasks:**
1. ✅ Design architecture (this doc)
2. Create `clawdsure` CLI tool (Python 3)
   - Commands: `init`, `check`, `approve`, `restore`, `verify`, `export`, `report`
   - Library: `clawdsure/` module with asset monitors
3. Implement chain primitives:
   - `Chain.append(event)` — write event with hash linking
   - `Chain.verify()` — recompute hashes, check integrity
   - `Chain.sign(event, private_key)` — Ed25519 signature
4. Implement file asset monitor (port soul-guardian code)
5. Write tests for chain integrity + signature verification

**Deliverable:** `clawdsure init` and `clawdsure check --asset-type file` working.

---

### Phase 2: Asset Monitors (Week 2)
**Goal:** Extend to all asset types

**Tasks:**
1. Config asset monitor:
   - Hook into `gateway` tool `config.patch` and `config.apply`
   - Compare before/after config hash
   - Append drift event to chain
2. CVE asset monitor:
   - Read ClawSec feed state
   - Compare known CVEs vs approved baseline
   - Append drift event on new CVEs
3. Audit asset monitor:
   - Parse `openclaw security audit --json` output
   - Compare check results vs approved baseline
   - Append drift event on new failures
4. Skills asset monitor:
   - Scan `~/.openclaw/workspace/skills/`
   - Hash each skill's `SKILL.md` + scripts
   - Compare vs approved inventory
   - Append drift event on new/changed skills
5. Network asset monitor:
   - Run `netstat -an | grep LISTEN`
   - Check macOS firewall status
   - Compare vs approved baseline
   - Append drift event on changes

**Deliverable:** `clawdsure check` monitors all asset types.

---

### Phase 3: ClawSec Integration (Week 3)
**Goal:** Wire ClawSec tools into ClawdSure

**Tasks:**
1. Modify clawsec-advisory-guardian hook:
   - Call `clawdsure check --asset-type cve` after feed update
2. Modify openclaw-audit-watchdog cron:
   - Call `clawdsure check --asset-type audit` after audit run
   - Replace custom report formatting with `clawdsure report`
3. Migrate soul-guardian state:
   - Import existing audit log into ClawdSure chain
   - Move baselines to `~/.clawdsure/baselines/files/`
4. Install openclaw-audit-watchdog + soul-guardian (now integrated)

**Deliverable:** Daily attestation (9:30am) uses unified ClawdSure chain.

---

### Phase 4: Verification + Export (Week 4)
**Goal:** Underwriter-facing tools

**Tasks:**
1. Implement `clawdsure verify`:
   - Chain integrity check
   - Signature verification
   - Coverage report (all assets checked)
2. Implement `clawdsure export`:
   - Bundle chain + policy + patches + verification report
   - Tarball output
3. Write underwriter documentation:
   - How to run verification
   - How to interpret drift events
   - Risk assessment framework
4. Generate sample export for Sam Clifton + Daren McCauley lunches

**Deliverable:** Underwriter-ready verification package.

---

## 8. File Structure

```
~/.clawdsure/
├── attestation.jsonl          # Single canonical chain
├── policy.json                 # Asset policies (restore/alert/ignore)
├── private-key.pem             # Ed25519 signing key (Keychain-backed)
├── public-key.pem              # Ed25519 verification key
├── baselines/
│   ├── files/
│   │   ├── SOUL.md             # Approved file snapshot
│   │   ├── AGENTS.md
│   │   └── ...
│   ├── config.json             # Approved config state
│   ├── cve_database.json       # Approved CVE list
│   ├── audit_results.json      # Approved audit outcomes
│   ├── skills_inventory.json   # Approved skills list
│   └── network_posture.json    # Approved network state
├── patches/
│   ├── 20260214T093000-SOUL-drift.patch
│   └── ...
└── quarantine/                 # Replaced files (forensics)
    ├── SOUL.md-20260214T093000
    └── ...
```

---

## 9. Policy Configuration

**`~/.clawdsure/policy.json`**

```json
{
  "version": 2,
  "signing": {
    "enabled": true,
    "algorithm": "ed25519",
    "private_key": "keychain:clawdsure-signing-key",
    "public_key_fingerprint": "35866e1b1479a043ae816899562ac877e879320c3c5660be1e79f06241ca0854"
  },
  "assets": {
    "files": [
      {"path": "SOUL.md", "mode": "restore"},
      {"path": "AGENTS.md", "mode": "restore"},
      {"path": "USER.md", "mode": "alert"},
      {"path": "TOOLS.md", "mode": "alert"},
      {"path": "IDENTITY.md", "mode": "alert"},
      {"path": "HEARTBEAT.md", "mode": "alert"},
      {"path": "openclaw.json", "mode": "alert"},
      {"pattern": "memory/*.md", "mode": "ignore"}
    ],
    "config": {
      "mode": "alert",
      "sections": [
        "agents.defaults.model",
        "auth.profiles",
        "tools",
        "commands",
        "session.reset"
      ]
    },
    "cve": {
      "mode": "alert",
      "source": "~/.openclaw/clawsec-suite-feed-state.json"
    },
    "audit": {
      "mode": "alert",
      "command": "openclaw security audit --json --deep"
    },
    "skills": {
      "mode": "alert",
      "directory": "~/.openclaw/workspace/skills"
    },
    "network": {
      "mode": "alert",
      "checks": ["listening_ports", "firewall_status"]
    }
  }
}
```

---

## 10. Underwriter Risk Assessment Framework

### 10.1 Green Flags (Low Risk)
- ✅ Chain integrity verified (all hashes valid)
- ✅ All signatures valid (if signing enabled)
- ✅ High restoration success rate (>95% of file drifts restored)
- ✅ Low drift frequency (<10 events/day)
- ✅ Detailed approval notes ("reviewed CVE-2026-1234, not applicable because we don't use skill-loader")
- ✅ Quick approval turnaround (<24h from drift to approval)
- ✅ No unexplained chain gaps (continuous timeline)

### 10.2 Yellow Flags (Medium Risk)
- ⚠️ Moderate drift frequency (10-50 events/day)
- ⚠️ Occasional failed restores (90-95% success rate)
- ⚠️ Generic approval notes ("reviewed and approved")
- ⚠️ Slow approval turnaround (24-72h)
- ⚠️ Unsigned chain (no Ed25519 signatures)

### 10.3 Red Flags (High Risk / Reject Claim)
- 🚨 Broken chain (hash mismatch, missing link)
- 🚨 Invalid signature (chain tampered with)
- 🚨 High drift frequency (>50 events/day — indicates unstable system)
- 🚨 Consistent failed restores (<90% success — compromise suspected)
- 🚨 No approval notes (automated approvals, no human review)
- 🚨 Chain gaps (missing days — attestation disabled during incident?)
- 🚨 SOUL.md drift without restoration (core identity compromised)

### 10.4 Claim Decision Matrix

| Chain Valid | Signatures Valid | Restore Rate | Drift Freq | Decision |
|-------------|------------------|--------------|------------|----------|
| ✅ | ✅ | >95% | <10/day | **Approve** |
| ✅ | ✅ | 90-95% | 10-50/day | **Approve with premium increase** |
| ✅ | ⚠️ N/A | >95% | <10/day | **Approve with conditions** |
| ✅ | ⚠️ N/A | 90-95% | 10-50/day | **Decline** |
| ✅ | Any | <90% | Any | **Decline (compromise suspected)** |
| ✅ | Any | Any | >50/day | **Decline (unstable system)** |
| 🚨 | Any | Any | Any | **Decline + investigate fraud** |

---

## 11. Open Questions / Decisions Needed

1. **Signing key management:** Store in macOS Keychain (current) or hardware token (YubiKey)?
2. **IPFS publishing:** Publish daily attestation snapshots to IPFS for public verifiability?
3. **Multi-agent support:** How to handle attestation across multiple agents (Clawdine + future agents)?
4. **Backward compatibility:** Import v1 chain into v2 chain, or start fresh?
5. **Performance:** Chain grows ~100 events/day. At 36K events/year, how to handle verification speed?

---

## 12. Success Criteria

**v2 is done when:**
1. ✅ One canonical chain covers all asset types
2. ✅ Daily attestation (9:30am) writes to unified chain
3. ✅ File drift auto-restores (SOUL.md, AGENTS.md)
4. ✅ Config changes auto-alert, await approval
5. ✅ CVE updates auto-alert, await approval
6. ✅ Audit failures auto-alert, await approval
7. ✅ Skills changes auto-alert, await approval
8. ✅ `clawdsure verify` confirms chain integrity
9. ✅ `clawdsure export` generates underwriter bundle
10. ✅ Underwriter documentation written

**Insurance pitch value:**
- "Continuous cryptographic proof of agent integrity, not just point-in-time audits"
- "Tamper-evident audit trail — can't retroactively forge clean history"
- "Automated drift detection + restoration — proves we catch compromises fast"

---

## Appendix A: soul-guardian vs ClawdSure v2

| Aspect | soul-guardian (standalone) | ClawdSure v2 |
|--------|----------------------------|--------------|
| Scope | Files only | All asset types |
| Chain | Per-skill audit log | Unified attestation chain |
| Policy | File-level (restore/alert) | Asset-level (all types) |
| Integration | Standalone tool | Framework with hooks |
| Verification | `verify-audit` command | Full underwriter export |
| Insurance value | Proof of file integrity | Proof of continuous agent integrity |

**Relationship:** ClawdSure v2 adopts soul-guardian's pattern and extends it. soul-guardian becomes the file monitor within ClawdSure.

---

## Appendix B: Migration Path (v1 → v2)

**v1 state:**
- `.clawdsure/chain.jsonl` — security checks only
- `memory/soul-guardian/audit.jsonl` — file integrity events (if installed)
- No config/CVE/skills monitoring

**Migration steps:**
1. Export v1 chain: `cat ~/.clawdsure/chain.jsonl > ~/.clawdsure/chain-v1.jsonl.bak`
2. Export soul-guardian audit: `cat memory/soul-guardian/audit.jsonl > ~/.clawdsure/soul-guardian-v1.jsonl.bak`
3. Run `clawdsure init --migrate-from-v1`
   - Reads both v1 chains
   - Merges events by timestamp
   - Recomputes chain hashes in unified v2 format
   - Writes merged chain to `~/.clawdsure/attestation.jsonl`
4. Verify migration: `clawdsure verify`
5. Delete old chains after confirmation

**Backwards compatibility:** v1 scripts continue to work via compatibility shims until v2 is proven.

---

**End of Architecture Spec**

Next: Mark reviews and approves design, then Phase 1 implementation begins.
