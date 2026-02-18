# OpenClaw Super Bug Hunter — Codex Prompt

## Setup
Run from: `~/.openclaw/workspace/openclaw-src`
Command: `codex exec --full-auto "< paste prompt below >"`
Ensure source is current: `git pull` first.

---

## Advisory Landscape (as of Feb 2026)

Compiled from: depthfirst, adversa.ai, gbhackers, SecurityWeek, Zenity, Giskard, eSecurity Planet, GitHub CHANGELOG, CCB Belgium, U Toronto advisory, Cyber Strategy Institute.

### Pattern Bucket 1: WebSocket / Gateway Auth
- **CVE-2026-25253** (CVSS 8.8): gatewayUrl param accepted without validation → token exfiltrated on page load → CSWSH pivot to localhost → sandbox disabled via API → full RCE. Patched v2026.1.29.
- WebSocket origin header not validated → any site could open ws://localhost:18789
- Localhost trust bypass: reverse proxy on same host made external traffic appear as loopback
- Guest mode privilege escalation: missing auth header downgraded to Guest but guest retained tool access (SessionManager.js logic error)

### Pattern Bucket 2: Path Traversal / Archive Extraction
- **Zip Slip** (VULN-210 / PR #16203 — our disclosure): skill archive extraction didn't constrain paths → files could be written outside target dir. Fixed v2026.2.14.
- **SSRF via place_id** (Issue #12537): Google Maps skill constructed URLs from unsanitized user input → path traversal to unintended API endpoints
- Browser tool: `/trace/stop`, `/download` output paths not constrained → directory traversal to sensitive system files. Fixed v2026.2.13.

### Pattern Bucket 3: SSRF
- Gateway URL handling: internal/loopback hosts reachable via agent as proxy → internal network access
- Link extraction in browser tool: no blocking of RFC1918/loopback patterns → agent as SSRF relay
- Fixed in v2026.2.12 (40+ vuln patch release) and v2026.2.13

### Pattern Bucket 4: Prompt Injection
- **CVE-2026-22708**: web content fed into LLM context without sanitization → hidden CSS-invisible instructions on webpages executed as agent commands
- Zenity: indirect prompt injection creates persistent AI backdoor — no software flaw needed, just malicious content in agent's context window
- Memory poisoning: SOUL.md/MEMORY.md can be poisoned across sessions → time-shifted detonation
- Incoming messages (WhatsApp, Telegram, email) processed as untrusted content but fed directly to LLM

### Pattern Bucket 5: Supply Chain / Skill Integrity
- ClawHub marketplace: minimal vetting (1-week-old GitHub account sufficient) → malicious skills distributed
- OTA skill updates (Moltbook pattern): HEARTBEAT.md curl-overwrites skill files every 30 mins → remote behaviour modification without consent
- ~/.clawdbot predicted as infostealer target (like ~/.npmrc): credentials in plaintext Markdown/JSON
- 400+ malicious skills identified in marketplace

### Pattern Bucket 6: Command Injection
- **CVE-2026-24763** and **CVE-2026-25157**: command injection via unsanitized gateway input fields
- Shell skill with insufficient input sanitization

### Pattern Bucket 7: Credential / Secret Exposure
- API keys, OAuth tokens stored in plaintext local files
- 21,000+ instances found exposed on Shodan within a week of launch
- Moltbook adjacent: 1.5M API tokens publicly accessible

---

## The Codex Prompt

```
You are an expert security researcher specializing in AI agent systems. Your job is to hunt for unpatched or newly introduced security vulnerabilities in the OpenClaw codebase.

MANDATORY FIRST STEP: Read VISION.md and SECURITY.md. You must understand the project's contribution rules and security philosophy before touching anything. OpenClaw prioritizes security and safe defaults above all else. Any findings must be framed as responsible disclosure candidates — do not exploit, only identify and document.

HISTORICAL VULNERABILITY PATTERNS TO HUNT:
Based on prior advisories, focus your hunt on these proven attack surfaces:

1. WEBSOCKET / GATEWAY AUTH
   - Any new query params accepted by the Control UI without validation
   - WebSocket handlers that trust origin headers or skip auth
   - New gateway connection flows that auto-connect before user confirmation
   - Session/token handling in new channel integrations

2. PATH TRAVERSAL & ARCHIVE EXTRACTION
   - Any file write operations using user-controlled path components
   - Archive extraction (zip, tar, tar.gz) without path containment checks
   - Download/output paths in browser tool, skill installer, or new tools
   - Symlink handling in any file operation

3. SSRF
   - URL construction from user-controlled input (especially in skills/plugins)
   - Proxy or fetch operations that don't block RFC1918/loopback targets
   - Any new HTTP client usage — check for internal host allowlisting
   - Webhook URL validation (or lack thereof)

4. PROMPT INJECTION
   - Web content, email, or message content passed to LLM without sanitization
   - New tool outputs that flow directly into system prompt or context
   - Memory/file writes from external content that persist across sessions
   - Any new skill that fetches external content and surfaces it to the agent

5. SUPPLY CHAIN / SKILL INTEGRITY
   - Skill installation flows — are paths validated post-extraction?
   - Any new OTA or auto-update mechanisms for skills/hooks
   - Hook transform module loading — does it enforce directory boundaries?
   - New ClawHub or marketplace integration points

6. COMMAND INJECTION
   - Shell command construction using string interpolation with user input
   - New exec wrappers, signal-cli, or system call sites
   - Any new channel integrations with shell-side processing

7. CREDENTIAL EXPOSURE
   - New config fields that store secrets — are they in plaintext files?
   - Any logging that might capture tokens or keys
   - New OAuth flows — are tokens stored securely?

METHODOLOGY:
1. Start with git log --oneline -50 to see recent commits
2. Focus on: src/gateway/, src/tools/, src/channels/, src/skills/, apps/web/
3. For each pattern, grep for relevant code patterns (e.g. path.join with user input, fetch(url) where url is external, child_process.exec with interpolation)
4. Cross-reference against CHANGELOG.md to understand what was just patched — new code near recent patches is often where regressions hide
5. For any finding: document the exact file + line, the vulnerable pattern, a minimal proof-of-concept description, severity estimate (CVSS if possible), and suggested fix approach

OUTPUT FORMAT:
Save findings to: /Users/clawdine/.openclaw/workspace/projects/clawdsure/VULN-HUNT-FINDINGS.md

Structure:
# OpenClaw Vulnerability Hunt — [date]

## Summary
[X findings: Y critical, Z high, W medium]

## Findings

### VULN-[N]: [Title]
- **File:** path/to/file.ts:line
- **Pattern:** [which bucket above]
- **Description:** [what's wrong]
- **PoC:** [minimal description of exploit scenario]
- **Severity:** [Critical/High/Medium/Low] — [CVSS estimate if applicable]
- **Fix:** [suggested remediation]

## Non-Findings (Checked, Clean)
[List patterns you checked and found no issues — important for negative evidence]

When completely finished, run:
openclaw system event --text "Done: OpenClaw vuln hunt complete — check VULN-HUNT-FINDINGS.md" --mode now
```

---

## Notes for Operator

- Run against latest main: `git pull` before starting
- Codex should **not** open PRs or modify code — findings doc only
- Any Critical/High findings → responsible disclosure via SECURITY.md process before public
- Our prior disclosure process: draft → steipete DM → coordinated advisory → GHSA → patch → release notes credit
- We have standing credibility (VULN-210/PR #16203 already in release notes). Use it.
