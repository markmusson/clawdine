# OWASP AI Exchange → OpenClaw Advisory Mapping
*Source: owaspai.org — updated Feb 2026, aligned with ISO/IEC 27090 + AI Act prEN 18282*

---

## OWASP AI Exchange Threat Structure

Four main threat categories (updated taxonomy):

| OWASP Category | Description |
|---|---|
| **2. Input threats** (was "Threats through use") | Prompt injection, model extraction, evasion |
| **3. Development-time threats** | Data poisoning, supply chain, model theft |
| **4. Runtime conventional security threats** | Standard infosec: RCE, auth failures, SSRF, path traversal |
| **Agentic AI threats** (highlight section) | Autonomous agent-specific: tool misuse, memory poisoning, lateral movement |

---

## Mapping: Our Advisory Buckets → OWASP Taxonomy

### Bucket 1: WebSocket / Gateway Auth
**OWASP Category 4: Runtime conventional security threats**
- Sub-type: Authentication and access control failures
- OWASP terms: Insecure defaults, privilege escalation, missing origin validation
- CVEs: CVE-2026-25253 (CVSS 8.8), guest mode escalation, localhost trust bypass
- ISO/IEC 27090 alignment: Runtime security controls, access control verification

### Bucket 2: Path Traversal / Archive Extraction
**OWASP Category 4: Runtime conventional security threats**
- Sub-type: Output contains conventional injection → file system escape
- OWASP terms: Path containment failure, archive extraction without boundary checks
- CVEs: VULN-210/PR #16203 (our disclosure — merged), browser tool traversal (fixed 2026.2.13)
- ISO/IEC 27090 alignment: File integrity, supply chain asset protection

### Bucket 3: SSRF
**OWASP Category 4: Runtime conventional security threats**
- Sub-type: Server-side request forgery via agent-as-proxy
- OWASP terms: Internal host access, RFC1918 bypass, URL validation failure
- Fixed in: v2026.2.12 (40+ vuln batch), v2026.2.13
- ISO/IEC 27090 alignment: Network boundary controls, agent communication security

### Bucket 4: Prompt Injection
**OWASP Category 2: Input threats**
- Sub-type: Indirect prompt injection (OWASP renamed from "Threats through use")
- OWASP terms: Input threats via web content, memory poisoning, time-shifted injection
- CVEs: CVE-2026-22708 (web browsing injection), Zenity persistent backdoor
- Adversa "lethal trifecta" + Palo Alto "4th element: persistent memory" — both OWASP-aligned
- ISO/IEC 27090 alignment: Input validation, context separation, memory integrity

### Bucket 5: Supply Chain / Skill Integrity
**OWASP Category 3: Development-time threats** (+ runtime component)
- Sub-type: AI supply chain management — explicitly called out in updated OWASP Exchange
- OWASP terms: Model/skill exfiltration (was "model theft"), supply chain integrity, OTA manipulation
- Moltbook OTA pattern: heartbeat curl-overwrites skill files → OWASP "internal supply chain" threat
- OWASP update: "AI supply chain management includes the **internal supply chain, including full data provenance**" ← this is ClawdSure's exact territory
- ISO/IEC 27090 alignment: Supply chain security, provenance verification, integrity attestation

### Bucket 6: Command Injection
**OWASP Category 4: Runtime conventional security threats**
- Sub-type: Output contains conventional injection → shell execution
- CVEs: CVE-2026-24763, CVE-2026-25157
- ISO/IEC 27090 alignment: Input sanitization, exec boundary enforcement

### Bucket 7: Credential / Secret Exposure
**OWASP Category 4: Runtime conventional security threats** + Category 3
- Sub-type: Data leak (OWASP renamed from "theft"), plaintext credential storage
- ~/.clawdbot predicted as infostealer target — aligns with OWASP "model/data leak" threat class
- ISO/IEC 27090 alignment: Secret management, credential lifecycle

---

## ClawdSure Positioning Against OWASP Framework

The updated OWASP Exchange explicitly identifies the threat ClawdSure addresses:

> *"AI supply chain management includes the internal supply chain, including full data provenance."*

ClawdSure provides **cryptographic provenance** for the internal AI agent supply chain:
- Daily hash chain = tamper-evident log of agent state over time
- ECDSA signatures = cryptographic proof of integrity at each point
- IPFS anchoring = immutable external record the agent can't modify
- Chain breaks = automated detection of supply chain compromise

**OWASP control mapping for ClawdSure:**
| ClawdSure Component | OWASP Control Category |
|---|---|
| Config + skill hashing | #SUPPLYCHAINMANAGE (Category 3) |
| Cryptographic chain | #MODELVERSIONING / integrity controls |
| IPFS external anchoring | Data provenance, audit trail |
| Break detection + alerting | Runtime monitoring, incident response |
| Insurance underwriting | Risk transfer mechanism (Category 1 governance) |

---

## Key OWASP Language to Use in ClawdSure Comms

These are the canonical OWASP terms — use them when pitching to security audiences:

- "Internal supply chain integrity" (not just "skill security")
- "Full data provenance" (not just "audit trail")
- "Input threats via persistent memory" (not just "memory poisoning")
- "Model exfiltration" (not "model theft")
- "Zero-knowledge adversary" (not "black-box attacker")
- "Runtime conventional security" (for CVE-class bugs)
- "Agentic AI threats" (for the autonomous agent attack surface)

---

## Rob van der Veer — Worth Engaging?

Rob is co-editor of ISO/IEC 27090, lead author of ISO 5338, feeding directly into EU AI Act. He's defining the standards our insurance product will need to reference. ClawdSure as "cryptographic attestation of OWASP AI Exchange controls compliance" is a pitch he'd understand immediately.

CC0 licence — we can use any of this content freely without attribution.

---

*Source: owaspai.org (Feb 2026 update), ISO/IEC 27090, prEN 18282, adversa.ai, depthfirst.com*
