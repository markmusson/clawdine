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

### 6. Sandbox & Isolation (`sandbox.*`)

Informed by Harrison Chase's (LangChain) two-pattern framework for agent-sandbox architecture:
- **Pattern 1 (Agent IN Host):** Agent runs on the host with full access. Maximum blast radius if compromised. This is OpenClaw's default.
- **Pattern 2 (Sandbox as Tool):** Agent runs locally but executes tools in isolated containers. Reduced blast radius.

#### `sandbox.mode`
**What**: Checks `agents.defaults.sandbox.mode` in config
**Why**: Sandbox mode is the single most impactful security setting. Without it, the agent runs with full host privileges.
**OK**: `all` (full isolation) or `non-main` (partial isolation)
**Warn**: `none` or missing — Pattern 1, maximum blast radius

#### `sandbox.docker`
**What**: Checks Docker availability when sandbox is enabled
**Why**: Sandbox mode requires Docker. If Docker isn't running, sandbox config is a lie.
**OK**: Docker available and running
**Warn**: Docker missing or not running

#### `sandbox.network`
**What**: Checks `agents.defaults.sandbox.docker.network`
**Why**: Network-enabled sandboxes can still exfiltrate data. `none` = fully isolated.
**OK**: `none` (fully isolated)
**Warn**: Any other value (agent code can reach the internet from sandbox)

#### `sandbox.gateway_bind`
**What**: Checks `gateway.bind` setting
**Why**: If the gateway binds to `0.0.0.0`, it's accessible from the network. One of the 30,000+ exposed instances.
**OK**: `loopback` / `localhost` / `127.0.0.1`
**Fail**: Any other value — gateway exposed to network

#### `sandbox.elevated_exec`
**What**: Checks if elevated (sudo) exec is enabled
**Why**: Gives the agent root access. Combined with no sandbox = full machine compromise.
**OK**: Disabled
**Warn**: Enabled

### 7. Skill Threat Patterns (`skills.prompt_only`, `skills.external_urls`, `skills.config_mod`)

Based on ClawHub marketplace audit (Feb 10, 2026) which found 60%+ of suspicious skills are SKILL.md-only — pure prompt injection with no code to audit.

#### `skills.prompt_only`
**What**: Detects installed skills that have no code files — only a large SKILL.md (>3KB)
**Why**: These are prompt injection vehicles. The SKILL.md IS the payload. No code means no static analysis possible. Documented attack pattern: DeXiaong published 3 skills all pointing to non-resolving domain `openclawcli.forum`.
**OK**: No prompt-only skills
**Warn**: Prompt-only skills found (manual review needed)

#### `skills.external_urls`
**What**: Scans SKILL.md files for suspicious external URLs (.forum, .xyz, .tk, .ml, .ga, .cf, openclawcli)
**Why**: Skills that redirect agents to external domains can stage remote code execution, credential harvesting, or future activation attacks.
**OK**: No suspicious URLs
**Warn**: Suspicious URLs found

#### `skills.config_mod`
**What**: Scans SKILL.md files for config modification instructions (openclaw.json, config.patch, config.apply)
**Why**: A skill that instructs an agent to modify config can disable auth, change bindings, alter permissions, or add itself to plugins.
**OK**: No config modification instructions
**Warn**: Config modification references found

## Future Enhancements

Ideas for v2:
- Check for unexpected cron jobs
- Verify skill signatures (git commit sigs)
- Check for outdated dependencies (npm audit)
- Detect browser automation enabled (higher risk)
- Cross-reference installed skills with threat feed (threats.json)
- Memory/CPU usage anomaly detection (cryptomining)
- SOUL.md/MEMORY.md integrity hash (detect persistent poisoning)

## Why Not Use openclaw security audit?

We use **both** (`audit_native` + `audit_machine`):
- `openclaw security audit`: Internal OpenClaw view, may evolve with versions
- `audit-machine.sh`: External system view, pinned to skill version
- Defense in depth: Two independent perspectives
- Allows underwriters to assess risk from multiple angles
- If OpenClaw audit changes, machine audit remains consistent
