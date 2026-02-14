# ClawdSure Design Doc: Machine Audit

**This is a design document documenting what `audit-machine.sh` checks and why.**

## Overview

`audit-machine.sh` is a cross-platform bash script (macOS, Linux, WSL) that performs security hygiene checks on an OpenClaw deployment. It outputs structured JSON with findings.

**Design goals:**
- Cross-platform (bash + jq + openssl only)
- Fast (<10 seconds)
- Deterministic (same input = same output)
- No network calls
- Redacts secrets from output

## Check Categories

### 1. Filesystem Permissions (`fs.*`)

#### `fs.state_dir_perms`
**What**: Checks if `~/.openclaw` is writable and not world-writable  
**Why**: World-writable state dir allows any local user to tamper with config  
**Fail**: State dir world-writable or missing  
**Warn**: State dir is a symlink (unusual, may indicate misconfiguration)

#### `fs.config_perms`
**What**: Checks `openclaw.json` file permissions  
**Why**: World-readable config exposes credentials  
**Fail**: Config file world-writable (067 permission bits)  
**Warn**: Config missing (unusual for active deployment)

#### `fs.credentials_perms`
**What**: Checks `~/.openclaw/credentials/` directory permissions  
**Why**: Credential files (API keys, tokens) should be owner-only  
**Fail**: Credentials dir world-writable

#### `fs.synced_folder`
**What**: Detects if state dir is in Dropbox, iCloud, OneDrive, Google Drive  
**Why**: Synced folders expose credentials to cloud providers  
**Warn**: State dir in synced folder (high-risk configuration)

#### `fs.suid_sgid`
**What**: Looks for SUID/SGID files in state dir  
**Why**: SUID binaries in state dir are suspicious (privilege escalation risk)  
**Warn**: Any SUID/SGID files found

### 2. Network (`net.*`)

#### `net.listening_ports`
**What**: Checks for listening TCP/UDP ports (via `ss`, `lsof`, or `netstat`)  
**Why**: Awareness of network exposure (gateway, etc.)  
**OK**: Always (informational check)  
**Detail**: Count of listening ports

*Note: Currently informational. Future enhancement: detect unexpected high-port listeners.*

### 3. Firewall (`fw.*`)

Platform-specific checks for firewall status. At least one firewall should be active.

#### `fw.macos`
**What**: macOS Application Firewall status  
**Warn**: Firewall not enabled  
**OK**: Firewall enabled

#### `fw.ufw`
**What**: UFW (Uncomplicated Firewall) on Linux  
**Warn**: UFW not active  
**OK**: UFW active

#### `fw.firewalld`
**What**: Firewalld on RHEL/CentOS/Fedora  
**Warn**: Firewalld not running  
**OK**: Firewalld running

#### `fw.iptables` / `fw.nftables`
**What**: Checks for iptables/nftables rules  
**OK**: Rules present (≥5 rules indicates active firewall)

#### `fw.windows`
**What**: Windows Firewall (via `netsh`)  
**Warn**: Firewall not enabled  
**OK**: Firewall enabled

#### `fw.none`
**What**: No firewall detected  
**Warn**: If none of the above found

### 4. Skills Inventory (`skills.*`)

#### `skills.inventory`
**What**: Count of installed skills (workspace + state dirs)  
**OK**: Always (informational)  
**Detail**: Number of skills found

#### `skills.pattern_scan`
**What**: Scans skill files for suspicious patterns:
- `curl.*|` (piping curl to shell)
- `wget.*|` (piping wget to shell)
- `bash.*-c` / `sh.*-c` (shell execution)
- `chmod +x` (making files executable)
- `eval` (code evaluation)
- `base64.*-d` (base64 decode, often used for obfuscation)
- `Invoke-WebRequest`, `iwr`, `irm` (PowerShell download)

**Why**: These patterns indicate potential supply chain attacks or malicious behavior  
**Warn**: Suspicious patterns found (manual review needed)  
**OK**: No patterns detected

*Note: This is pattern-based heuristic, not a guarantee of safety. Review findings manually.*

### 5. Operational Coherence (`ops.*`)

#### `ops.model_allowlist`
**What**: Checks if models referenced in config are in the allowlist  
**Why**: Catches silent failures like heartbeat using a model not in `agents.defaults.models`  
**Checks**:
- `agents.defaults.model.primary` in allowlist?
- `agents.defaults.heartbeat.model` in allowlist?
- `agents.defaults.subagents.model` in allowlist?

**Warn**: Referenced model not in allowlist  
**OK**: All models consistent

## Output Format

```json
{
  "ts": "2026-02-08T10:00:00Z",
  "checks": {
    "fs.state_dir_perms": {
      "status": "ok",
      "detail": "State dir permissions OK"
    },
    "fw.macos": {
      "status": "warn",
      "detail": "macOS firewall not enabled"
    },
    ...
  },
  "summary": {
    "ok": 8,
    "warn": 2,
    "fail": 0
  }
}
```

### Status Values
- **`ok`**: Check passed
- **`warn`**: Issue detected, but not critical (review recommended)
- **`fail`**: Critical issue (causes FAIL attestation)

### Summary Counts
- `ok`: Count of passed checks
- `warn`: Count of warnings
- `fail`: Count of failures

## Integration with attest.sh

1. `attest.sh` runs `audit-machine.sh`
2. Captures JSON output
3. Hashes output: `SHA-256(audit-machine.sh output)`
4. Includes hash in attestation as `audit_machine`
5. Saves full output to `.clawdsure/last-audit.json` for reference
6. If `summary.fail > 0`, attestation result is `FAIL`

## Redaction

All output is redacted before inclusion:
- Bearer tokens: `Bearer xyz123` → `Bearer ****REDACTED****`
- Key-value patterns: `token=xyz123` → `token=****REDACTED****`
- Protects against accidental credential leaks in attestation

## Future Enhancements

Ideas for v2:
- Check for unexpected cron jobs
- Verify skill signatures (git commit sigs)
- Check for outdated dependencies (npm audit)
- Detect browser automation enabled (higher risk)
- Check for elevated exec enabled (higher risk)
- Cross-reference installed skills with threat feed (threats.json)
- Memory/CPU usage anomaly detection (cryptomining)

## Why Not Use openclaw security audit?

We use **both** (`audit_native` + `audit_machine`):
- `openclaw security audit`: Internal OpenClaw view, may evolve with versions
- `audit-machine.sh`: External system view, pinned to skill version
- Defense in depth: Two independent perspectives
- Allows underwriters to assess risk from multiple angles
- If OpenClaw audit changes, machine audit remains consistent
