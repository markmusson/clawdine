# OWASP Top 10 for Agentic Applications (2026) → ClawdSure Mapping
*Source: genai.owasp.org, Dec 2025. The benchmark for agentic security.*

---

## The 10 Risks — With ClawdSure Coverage

| # | Risk | ClawdSure Coverage |
|---|------|--------------------|
| ASI01 | Agent Goal Hijack | ⚠️ Partial — attestation detects config/skill changes that could enable hijack |
| ASI02 | Tool Misuse & Exploitation | ✅ Direct — skill inventory + pattern scan catches over-privileged/suspicious tools |
| ASI03 | Identity & Privilege Abuse | ✅ Direct — credentials dir perms, config hash, sandbox state tracked daily |
| ASI04 | Agentic Supply Chain Vulnerabilities | ✅ Core use case — skill content hashes + external URL scan + OTA detection |
| ASI05 | Unexpected Code Execution | ✅ Direct — sandbox mode, elevated exec, gateway bind all in chain |
| ASI06 | Memory & Context Poisoning | ⚠️ Partial — file integrity checks catch file-level tampering; semantic poisoning not in scope |
| ASI07 | Insecure Inter-Agent Communication | ⚠️ Partial — gateway loopback, port state tracked; message auth not attested |
| ASI08 | Cascading Failures | ❌ Out of scope — runtime behavior monitoring, not our layer |
| ASI09 | Human-Agent Trust Exploitation | ✅ Indirect — immutable audit chain is the "trust but verify" layer for operators/insurers |
| ASI10 | Rogue Agents | ✅ Direct — behavioral drift detectable via chain breaks; kill switch via attestation failure |

**Score: 6 direct/strong coverage, 3 partial, 1 out of scope**

---

## Deep Dive by Risk

### ASI01 — Agent Goal Hijack
*Attacker alters agent objectives via poisoned content (emails, PDFs, web)*

ClawdSure position: Attestation doesn't prevent goal hijack but creates a forensic record. If SOUL.md or memory files are modified by injected content, the config hash changes → chain break → alert. Skill-level pattern scanning catches skills that exfiltrate or have suspicious outbound hooks.

Gap: Semantic/runtime prompt injection not detectable without runtime monitoring.

---

### ASI02 — Tool Misuse & Exploitation
*Over-privileged tools called with destructive parameters*

ClawdSure position: **Core coverage.** Daily skill inventory and pattern scan flag:
- Dangerous tool references (exec, shell, browser)
- Skills with suspicious external URL hooks
- Skills without permission manifests
- Skills that modify config

The skills-audit PR (#20266) does static analysis. ClawdSure adds: *has this changed since yesterday?* Chain breaks if a skill is silently updated to add dangerous tool references.

---

### ASI03 — Identity & Privilege Abuse
*Inherited credentials reused/escalated across agents*

ClawdSure position: **Direct coverage.**
- `fs.credentials_perms` — credentials directory permissions checked daily
- `sandbox.mode` — sandbox disabled = elevated privilege risk, flagged
- `sandbox.elevated_exec` — elevated exec tracked in chain
- Config hash catches changes to permission model

---

### ASI04 — Agentic Supply Chain Vulnerabilities
*Malicious MCP servers, poisoned prompt templates, compromised third-party agents*

ClawdSure position: **Core use case. This is why ClawdSure exists.**
- `skills.content_hashes` — SHA-256 of every installed skill, verified daily
- `skills.pattern_scan` — detects exfiltration patterns, OTA update hooks
- `skills.external_urls` — flags suspicious outbound endpoints
- `skills.config_mod` — detects skills that try to modify agent config
- Chain: if a ClawHub skill silently updates (Moltbook OTA pattern), hash changes → chain break

OWASP mitigation: "signed manifests, curated registries, dependency pinning, kill switches." ClawdSure provides the cryptographic manifest + tamper-evident chain. The insurance product is the kill switch trigger.

---

### ASI05 — Unexpected Code Execution
*Generated code runs unsafely, shell commands triggered via injection*

ClawdSure position: **Direct coverage.**
- `sandbox.mode` — is execution sandboxed?
- `sandbox.gateway_bind` — is gateway bound to loopback only?
- `sandbox.elevated_exec` — is elevated host exec enabled?
- All three tracked in daily chain, flagged on change

If someone disables sandboxing (CVE-2026-25253 kill chain step 3), the chain breaks the next attestation cycle. Not real-time, but it's the audit trail that proves whether you had safe defaults.

---

### ASI06 — Memory & Context Poisoning
*RAG poisoning, cross-tenant leakage, adversarial drift via persistent memory*

ClawdSure position: **Partial.**
- File integrity checks cover SOUL.md, MEMORY.md, daily log files — if content is overwritten by injected payload, file hash changes → chain break
- Does not detect semantic drift within files (agent being gradually influenced without explicit file modification)
- Does not cover vector DB or RAG index poisoning

Gap is real. Future extension: hash embeddings/vector store contents as separate attestation surface.

---

### ASI07 — Insecure Inter-Agent Communication
*Spoofed agents, replayed delegation messages, unauthenticated MCP/A2A channels*

ClawdSure position: **Partial.**
- `net.listening_ports` — network exposure tracked
- `sandbox.gateway_bind` — loopback binding verified
- Does not attest to message-level authentication between agents

Gap: inter-agent message signing is outside ClawdSure's current scope. OWASP mitigation (mutual TLS, signed payloads) would need to be a separate attestation surface.

---

### ASI08 — Cascading Failures
*Small agent error compounds across planning/execution layers*

ClawdSure position: **Out of scope.**
Runtime behavioral isolation and circuit breaking is architecture, not attestation. ClawdSure is a daily check, not a real-time circuit breaker. Different product category.

---

### ASI09 — Human-Agent Trust Exploitation
*Users over-trust agent recommendations; attackers exploit this*

ClawdSure position: **Indirect — but this is the insurance play.**
The entire value proposition of ClawdSure to an insurer is: *can you trust this agent's behavior history?* A clean attestation chain is cryptographic proof that the agent hasn't been tampered with. That's the foundation for underwriting trust.

OWASP mitigation: "immutable logs, clear risk indicators." ClawdSure *is* the immutable log.

---

### ASI10 — Rogue Agents
*Compromised/misaligned agents acting harmfully while appearing legitimate*

ClawdSure position: **Direct coverage — and the killer use case.**
A rogue agent that persists across sessions, self-modifies, or exfiltrates data will leave traces:
- Config changes → config hash changes → chain break
- Skill modifications → skill hash changes → chain break
- New network exposure → port scan detects → chain break
- Sandbox disabled → flagged in attestation

The key OWASP mitigation: "behavioral monitoring and kill switches." ClawdSure's chain break IS the behavioral monitoring signal. The insurance policy IS the kill switch economic incentive.

---

## ClawdSure Positioning Statement (OWASP-aligned)

> ClawdSure provides cryptographic attestation of an AI agent's security posture against the OWASP Top 10 for Agentic Applications (2026). Daily hash chains — covering skill integrity (ASI02, ASI04), execution environment (ASI05), identity/privilege posture (ASI03), and configuration state (ASI10) — create tamper-evident proof that an agent has been operating within defined security parameters. Chain breaks provide automated detection of supply chain compromise, rogue agent behavior, and environment drift. The attestation record is the foundation for AI agent insurance underwriting.

---

## What This Means for the Pitch

1. **OWASP-native language** — every ClawdSure feature maps to a numbered risk that security teams already know
2. **ASI04 is our headline** — supply chain is the #4 risk and our clearest win
3. **ASI10 is our story** — rogue agents + kill switch + insurance = the product
4. **ASI09 is the insurer's frame** — "immutable logs for underwriting trust"
5. **Gaps are honest** — ASI06 semantic poisoning and ASI08 cascading failures are out of scope; say so. Credibility > completeness.

---

## Files Updated
- `OWASP-AI-EXCHANGE-MAPPING.md` — ISO 27090 + advisory bucket mapping
- `OWASP-AGENTIC-TOP10-MAPPING.md` — this file
- `OPENCLAW-INTEGRATION-ANALYSIS.md` — codebase integration path
