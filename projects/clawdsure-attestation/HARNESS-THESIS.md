# The Harness Thesis
*Crystallised Feb 19, 2026*

---

## The Thesis

The AI stack is collapsing to four layers: infra, model, harness, knowledge. Everything in between is disposable — workflows, orchestration tools, no-code agents, anything that sits between layers. The harness is the surviving substrate.

**The harness is where the agent lives.** It controls tools, credentials, memory, identity. It's persistent across sessions. It determines outcomes — not the model.

The model is a commodity input. The harness is the moat.

Nobody is underwriting it.

---

## Why Harness Wins

- **Infra layer** — AWS, GCP, NVIDIA own this
- **Model layer** — Anthropic, OpenAI, Google own this
- **Harness layer** — OpenClaw, Claude Code are early signals. This is the surviving substrate.
- **Knowledge layer** — proprietary data and domain expertise

Workflows, orchestration tools, no-code agents: disposable. They don't own identity, memory, or persistence. The harness does.

---

## Where Causal Plays

You can't insure workflows — disposable.
You can't insure models — Anthropic carries that risk.
You can't insure infra — AWS does.

**Harness is the gap.** That's where the agent can be compromised. That's where credentials live. That's where real damage happens when something goes wrong.

Causal makes harness infrastructure insurable — cryptographic attestation of agent state, chained daily, anchored to IPFS. If the harness is tampered with, the chain breaks. Telematics black box for AI agents.

The attestation chain is also a proprietary dataset nobody else is collecting. It's the actuarial foundation for underwriting agent behaviour. It compounds over time.

**The pitch:** "We're not insuring AI. We're making harness infrastructure insurable. If harness wins, harness trust wins with it."

---

## The Moat

This requires three things simultaneously:

1. **Insurance domain expertise** — built and sold an MGA to AON (£40m GWP)
2. **Harness-layer understanding** — active contributor to OpenClaw core (VULN-210/PR #16203, PR #20266, PR #20424)
3. **Attestation data nobody else has** — 18 consecutive daily attestation chains as of Feb 19, 2026

Most people have one. We have all three.

---

## Receipts

### The model is a commodity. The harness determines outcomes.

**LangChain Terminal Bench 2.0** (Feb 17, 2026):
- Coding agent: Top 30 → Top 5. Same model (GPT-5.2-Codex). Same tasks. Only the harness changed.
- +13.7 points (52.8% → 66.5%) from harness engineering alone.
- Source: https://blog.langchain.com/improving-deep-agents-with-harness-engineering/

### The harness is under active attack.

**ClawHavoc supply chain campaign** (Feb 19, 2026):
- 1,184 malicious skills injected into ClawHub marketplace. First skill: Jan 27. Major surge: Jan 31.
- Data theft and backdoor payloads. Multiple coordinated threat actors.
- Previous count was 341. Actual count 3.5x higher.
- Source: vuln-scan-daily, ClawdSure vuln DB

**OWASP Top 10 for Agentic Applications** (Dec 2025):
- ASI04 (Agentic Supply Chain) — harness-layer attack. Malicious MCP servers, poisoned skills, compromised plugins.
- ASI10 (Rogue Agents) — compromised harnesses acting while appearing legitimate.
- Source: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/

**OpenClaw CVE history** (2026 YTD):
- CVE-2026-25253 (CVSS 8.8): 1-click RCE via WebSocket + sandbox disable
- CVE-2026-26327: DNS-SD TLS bypass (unpatched)
- CVE-2026-26317: CSRF on loopback mutation endpoints (unpatched)
- 16 tracked vulns, 9 critical unpatched as of Feb 19, 2026
- Source: vuln-scan-daily

### The insurance gap is real.

**OWASP AI Exchange** (ISO/IEC 27090, Feb 2026 update):
- "AI supply chain management includes the internal supply chain, including full data provenance."
- Explicitly identifies harness-layer supply chain as a primary threat category.
- Source: https://owaspai.org

**ClawdSure attestation coverage** against OWASP Agentic Top 10:
- 6 of 10 risks: direct coverage
- 3 of 10 risks: partial coverage
- 1 of 10 risks: out of scope (runtime cascading failures)
- Source: OWASP-AGENTIC-TOP10-MAPPING.md

### The market exists now.

- 21,000+ OpenClaw instances found on Shodan within one week of launch
- 1.5M API tokens exposed in Moltbook-adjacent incident
- EU AI Act (prEN 18282) — liability framework arriving for AI systems
- RSAC 2026 GenAI Security Summit: March 25, San Francisco

---

## Key Contacts

- **Sam Clifton** — Greenlightre (reinsurer, Lloyd's syndicate). Risk capital + capacity. "Very keen."
- **Daren McCauley** — Actuary, ex-CEO of insurer behind Humn. Has regulated entity. Potential delegated authority / regulatory wrapper.
- **Rob van der Veer** — Co-editor ISO/IEC 27090, feeding EU AI Act. Defines the standards Causal will reference. Worth engaging.

---

*Domain: causal.insure*
*Stealth mode — no public details*
