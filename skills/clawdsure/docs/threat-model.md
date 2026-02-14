# ClawdSure Design Doc: Threat Model for OpenClaw Deployments

**This is a design document, not runtime instructions.**

## Assets

What we're protecting:
- **Credentials**: API keys, tokens, passwords in config and credential stores
- **Conversations**: Chat history, session data (may contain sensitive info)
- **Files**: Workspace files, scripts, agent memory
- **Channels**: Message accounts (Telegram, Discord, etc.) - can send as agent owner
- **Gateway Control**: Admin UI, can reconfigure agent
- **Node Execution**: Remote command execution on paired devices

## Actors

Realistic threats for OpenClaw deployments:
- **External attackers**: Network-based exploitation, credential stuffing
- **Malicious skill authors**: Supply chain attacks via clawhub
- **Compromised accounts**: If channel credentials leak (Telegram token, etc.)
- **Insiders**: Users with filesystem access to state dir
- **Lateral movement**: From one compromised service to OpenClaw

## Entry Points

Where attacks can originate:
- **Gateway/Control UI**: Web interface (if exposed)
- **Skills/plugins**: Installed code with filesystem + API access
- **Channels**: Inbound messages from Telegram/Discord/etc.
- **Browser control**: If enabled, can interact with websites
- **Node execution**: If nodes are paired, can run commands remotely
- **Filesystem**: Direct access to state dir/config

## Trust Boundaries

- **Host OS**: Config file permissions, process isolation
- **Gateway**: Reverse proxy, authentication, rate limiting
- **Skills**: Sandboxed? (currently no - full filesystem access)
- **Channels**: Message accounts are trusted (agent acts as owner)
- **Nodes**: Paired devices are trusted (mutual consent via pairing)

## Attack Scenarios

### 1. Malicious Skill Installation
**Actor**: Malicious skill author  
**Entry**: `clawhub install malicious-skill`  
**Impact**: Full filesystem access, can read credentials, exfiltrate data  
**Mitigations**: 
- ClawdSure threat feed (threats.json)
- Pattern scanning for suspicious commands (curl|bash, etc.)
- Manual review before install
- Skill signature verification (future)

### 2. Config File Exposure
**Actor**: External attacker, insider  
**Entry**: World-readable openclaw.json or credentials dir  
**Impact**: Credential theft, API key leaks  
**Mitigations**:
- Filesystem permission checks (audit-machine.sh)
- Fail attestation if world-writable/readable
- User education (don't put state dir in Dropbox)

### 3. Synced Folder Risk
**Actor**: Cloud sync service compromise (Dropbox, iCloud)  
**Entry**: Agent puts state dir in synced folder  
**Impact**: Credentials exposed to cloud provider, other synced devices  
**Mitigations**:
- Detect synced folders (audit-machine.sh)
- Warn in attestation
- Recommend moving state dir

### 4. Firewall Disabled
**Actor**: Lateral movement from compromised service  
**Entry**: OpenClaw gateway exposed without firewall  
**Impact**: Unauthorized access to control UI  
**Mitigations**:
- Check firewall status (audit-machine.sh)
- Warn if no firewall detected
- Recommend localhost-only or VPN access

### 5. Model Allowlist Bypass
**Actor**: Misconfigured agent  
**Entry**: Heartbeat/cron using model not in allowlist  
**Impact**: Unexpected model access, cost overrun, data exposure  
**Mitigations**:
- Operational coherence checks (audit-machine.sh)
- Detect referenced models not in allowlist
- Warn in attestation

### 6. Supply Chain Attack via Skill Update
**Actor**: Compromised skill repository  
**Entry**: Agent auto-updates skill with malicious code  
**Impact**: Similar to malicious skill installation  
**Mitigations**:
- Pattern scanning on skill files
- No auto-update by default (manual review)
- Threat feed integration
- Git commit signature verification (future)

## Residual Risks

Even with ClawdSure, these risks remain:
- **Zero-day exploits**: In OpenClaw, Node.js, or dependencies
- **Social engineering**: Tricking the human to disable security
- **Physical access**: If attacker has console access
- **Model jailbreaking**: LLM prompt injection attacks
- **Rate limiting bypass**: If gateway exposed without proper limits

## Mitigations (Prioritized)

From most to least impactful:

1. **Filesystem permissions** (audit-machine.sh checks)
   - Fix: `chmod 600 ~/.openclaw/openclaw.json`
   - Fix: `chmod 700 ~/.openclaw/credentials/`

2. **Firewall enablement** (audit-machine.sh checks)
   - macOS: System Preferences → Security & Privacy → Firewall
   - Linux: `sudo ufw enable`

3. **Synced folder avoidance** (audit-machine.sh checks)
   - Move state dir outside Dropbox/iCloud/OneDrive

4. **Model allowlist enforcement** (audit-machine.sh checks)
   - Review config, remove unused models
   - Ensure heartbeat/cron use allowed models

5. **Skill vetting before install** (agent-assisted via threats.json)
   - Check threats.json before `clawhub install`
   - Review SKILL.md and scripts

6. **Gateway access control** (future enhancement)
   - Localhost-only by default
   - VPN or Tailscale for remote access
   - Strong auth (not just session cookies)

## Design Philosophy

ClawdSure doesn't prevent attacks. It **detects configuration drift** and **proves good practice**. Think of it like car insurance telematics:
- We don't stop you from speeding
- We measure your driving behavior
- We price risk accordingly
- We void coverage if you disable the device

Same here:
- We don't stop you from installing malicious skills
- We detect suspicious patterns and misconfigurations
- We price risk via attestation history
- We void coverage if chain breaks (no audit for >48h)
