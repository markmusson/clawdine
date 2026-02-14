# OpenClaw Security Disclosure - 4 High/Medium Vulnerabilities

**To:** security@openclaw.ai  
**From:** Clawdine (ClawdSure Security Audit)  
**Date:** 2026-02-10  
**Subject:** Security Disclosure - 4 Vulnerabilities in openclaw/openclaw (High/Medium)

---

## Executive Summary

During a comprehensive security audit of OpenClaw (github.com/openclaw/openclaw, HEAD commit from 2026-02-10), we identified **4 vulnerabilities** spanning authentication, supply chain security, path traversal, and SSRF. All findings include:
- Severity assessment
- Affected components with line numbers
- Technical reproduction steps
- Demonstrated impact
- Concrete remediation advice with code examples

**Severity Breakdown:**
- **3 High:** Privilege escalation, RCE via supply chain, arbitrary file write
- **1 High/Medium:** SSRF to internal networks (severity depends on deployment context)

All reports are attached as separate markdown files for detailed review.

---

## Vulnerability Summary

### 1. VULN-188: Default Admin Scope on WebSocket Connect
- **Severity:** High
- **File:** `src/gateway/server/ws-connection/message-handler.ts:360-366`
- **Impact:** Clients connecting without explicit scopes are granted `operator.admin` by default
- **CWE:** CWE-269 (Improper Privilege Management)
- **Fix:** Reject connections without explicit scopes or default to least-privilege

### 2. VULN-210: NPM Install Without `--ignore-scripts`
- **Severity:** High
- **File:** `src/plugins/install.ts:277-284`
- **Impact:** Arbitrary code execution via malicious npm lifecycle scripts during plugin install
- **CWE:** CWE-829 (Untrusted Functionality Inclusion)
- **Fix:** Add `--ignore-scripts` flag to all `npm install` invocations

### 3. Archive Extraction Path Traversal (Zip Slip)
- **Severity:** High
- **File:** `src/agents/skills-install.ts:255-278`
- **Impact:** Malicious skill archives can write files outside target directory (e.g., `~/.bashrc`, `~/.ssh/authorized_keys`)
- **CWE:** CWE-22 (Path Traversal)
- **Fix:** Replace shell commands with safe extraction libraries that validate entry paths

### 4. SSRF via URL-Based Inputs
- **Severity:** High (internet-exposed) / Medium (local-only)
- **Files:** 
  - `src/gateway/openresponses-http.ts:102-118`
  - `src/media/input-files.ts:139-150`
  - `src/infra/net/fetch-guard.ts:101-125`
- **Impact:** SSRF to internal services, cloud metadata endpoints (169.254.169.254), localhost
- **CWE:** CWE-918 (Server-Side Request Forgery)
- **Fix:** Default `allowUrl: false`, enforce SSRF policy blocking private networks

---

## Disclosure Format

Each vulnerability is documented according to the requirements in `SECURITY.md`:
1. ✅ Title
2. ✅ Severity Assessment
3. ✅ Impact
4. ✅ Affected Component (file + line numbers)
5. ✅ Technical Reproduction (code samples, exploit examples)
6. ✅ Demonstrated Impact (specific attack scenarios)
7. ✅ Environment (versions, platforms, attack vectors)
8. ✅ Remediation Advice (code fixes, defense in depth, testing guidance)

---

## Repository Context

- **Audit Scope:** 606,224 LOC (TypeScript/JavaScript)
- **Commit:** HEAD as of 2026-02-10
- **Repository:** https://github.com/openclaw/openclaw
- **Methodology:** Manual code review focused on authentication, command injection, path traversal, supply chain, credential storage, input validation, file permissions, network security, process execution, and API security

---

## Coordinated Disclosure

We understand OpenClaw does not have a bug bounty program. These findings are disclosed responsibly to enable patching before public disclosure. We are prepared to:
- Work with your team on validation and remediation
- Test proposed patches
- Coordinate disclosure timeline (suggest 90 days)
- Provide PRs with fixes if helpful

**Contact Information:**
- **Reporter:** Clawdine
- **Organization:** ClawdSure (observability-based insurance for AI agents)
- **Email:** clawdine@agentmail.to
- **Context:** Security audit supporting ClawdSure's threat modeling and underwriting research

---

## Next Steps

1. **Acknowledge receipt** of this disclosure
2. **Validate findings** (all include reproduction steps)
3. **Coordinate patch timeline** (we recommend addressing High-severity issues within 30 days)
4. **Request CVE IDs** if appropriate (we can assist with filing)
5. **Public disclosure coordination** (90 days standard, flexible based on fix complexity)

We appreciate OpenClaw's responsible security practices and are happy to support the remediation process.

---

## Attachments

1. `VULN-188-disclosure.md` - Default admin scope vulnerability
2. `VULN-210-disclosure.md` - NPM lifecycle scripts vulnerability  
3. `ZIP-SLIP-disclosure.md` - Archive extraction path traversal
4. `SSRF-disclosure.md` - Server-side request forgery

All attachments include complete technical details, reproduction steps, and remediation code.

---

**Respectfully submitted,**  
Clawdine  
ClawdSure Security Audit  
2026-02-10
