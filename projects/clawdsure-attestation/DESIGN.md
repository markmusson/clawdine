# Causal Insurance — Product Design

**For:** Greenlight Re  
**Date:** February 2026  
**Version:** 3.1  

---

## Executive Summary

Millions of autonomous AI agents are running right now — executing code, holding credentials, making decisions, operating 24/7. Nobody insures them. Traditional cyber doesn't fit: annual questionnaires can't price something that changes configuration daily.

Causal provides security insurance for AI agents using continuous telematics. A daily automated audit runs 25 security checks, signs the results cryptographically, and chains each day's report to the last. If an incident occurs, you check the chain. Intact chain = eligible. Broken chain = not covered. No subjective assessment, no claims adjuster debates.

Two tiers. Both capped. Both short-tail.

| | Tier 1: Personal | Tier 2: SME |
|---|---|---|
| Premium | £50/yr | £5,000/yr |
| Limit | £500 | £25,000 |
| Risk data | Daily machine audit | Daily telemetry + audit |
| Distribution | Embedded in platforms | Direct + broker |
| Analogy | Gadget insurance | Fleet telematics |

This is not cyber insurance. Not enterprise. Not open-ended liability.

---

## 1. The Market

AI agents are where Linux was in 1994. Hobbyist territory going mainstream, with enterprises experimenting but nobody underwriting the risk.

An AI agent can execute shell commands, call APIs, hold auth tokens, install its own plugins, modify its own configuration, and operate without human approval. The personal ones run on laptops. The business ones handle customer service, code review, trading, operations.

There are roughly 2 million deployed in 2026. By 2028, conservatively 10 million. Zero dedicated insurance products exist.

### Why traditional cyber doesn't work

Cyber insurance prices risk off annual questionnaires and employee headcounts. Agent risk changes daily — new skills installed, configs modified, versions updated. Cyber covers data breaches; agents cause operational harm (retaliation against humans, self-modification, credential exposure, flooding third-party systems with autonomous output). Cyber is long-tail; agent incidents are detected in hours.

The gap: no continuous risk signal means you can't distinguish a hardened agent from a compromised one. Can't price what you can't see.

### Market size

At 15% penetration:

| Year | Agents | Addressable Premium |
|---|---|---|
| 2026 | 2M | £15M |
| 2027 | 5M | £37.5M |
| 2028 | 10M+ | £75M+ |

First movers accumulate attestation data that compounds into a pricing advantage nobody else has.

---

## 2. Product Structure

### Tier 1 — Personal / Micro-Business

£50 premium, £500 cap. Gadget insurance for AI agents.

Individual developers, hobbyists, sole traders. The agent runs on their laptop or a VPS. Daily automated audit checks filesystem permissions, firewall, network exposure, installed plugins, sandbox configuration — 25 checks total. Results signed, hash-linked, published.

| | |
|---|---|
| Covered | Credential theft, unauthorized access, supply chain compromise, data exfiltration |
| Excluded | Chain gap >48h, self-inflicted, gross negligence |
| Claims | Report → verify chain → pay within 7 days |
| Term | 12 months, auto-renew if chain intact |

Premium adjustments based on risk posture: public-facing gateway (+25%), elevated exec permissions (+20%), browser tools (+15%). Clean chain >1 year gets a discount. Range: £32–£85.

### Tier 2 — SME

£5,000 premium, £25,000 cap. Fleet telematics for production agents.

Startups and SMEs deploying agents in production — customer service bots, code review, trading, operational automation. Everything from Tier 1, plus continuous behavioural telemetry via OpenTelemetry (built into Vercel AI SDK and similar platforms). Every tool call, model invocation, error, and data access pattern is traced and scored.

| | |
|---|---|
| Covered | Tier 1 perils + business interruption (capped) + reputational harm (capped) |
| Excluded | Tier 1 exclusions + non-compliance with OWASP AI Exchange controls |
| Claims | Report → verify telemetry + chain → pay within 14 days |
| Term | 12 months, quarterly underwriting review |

Premium adjustments: high-risk tool usage (+20%), elevated error rates (+10%), OWASP compliance failures (+15%). Range: £3,500–£8,750.

### What we don't write

Enterprise (AWS/Azure scale). Open-ended liability. Anything over £25K per policy. Long-tail. Those are traditional cyber's problem.

---

## 3. How Attestation Works

If you've underwritten motor telematics, you already understand this.

| Motor telematics | Agent attestation |
|---|---|
| Black box in the car | Audit script on the machine |
| Speed, braking, GPS | Filesystem, firewall, skills, sandbox |
| Daily data upload | Daily signed attestation |
| Crash → check the box | Incident → check the chain |
| Good driving = lower premium | Clean chain = coverage intact |
| Tamper-evident hardware | Cryptographic signatures |

### What gets checked

**Tier 1 — 25 daily checks across five categories:**

*Filesystem:* Are configs protected? Credentials locked down? Agent directory in Dropbox/iCloud where it could leak? Privilege escalation binaries present?

*Network & firewall:* Firewall on? Which ports are listening? Is the gateway locked to localhost or exposed to the internet?

*Skills & supply chain:* What plugins are installed? Any suspicious code patterns (eval, curl piping, chmod)? Files modified since installation? Prompt-only skills over 3KB (injection risk)?

*Sandbox & isolation:* Code execution sandboxed or unrestricted? Sudo access? Browser enabled?

*Operational:* Platform version current? Config consistent? Auth secure?

**Tier 2 — adds continuous behavioural telemetry:**

Tool calls per day. Model invocations. Error rates. Destructive actions attempted. Human confirmations vs autonomous decisions. Data access patterns. Compliance against the OWASP AI Exchange threat taxonomy (the 300+ page framework that feeds into ISO/IEC 27090 and the EU AI Act — input threats, development-time threats, runtime application security threats).

### The chain

Each day's attestation is cryptographically signed and hash-linked to the previous day's. Modify any past entry, every subsequent hash breaks. Published to IPFS (immutable, content-addressed storage). Anyone can verify it independently.

**Chain rules:**
- Daily PASS → chain continues
- FAIL → 48h grace period to fix
- Fixed within 48h → chain continues
- No attestation for 48h → chain broken → coverage void until re-enrollment

This gives you three things traditional cyber can't: a continuous risk signal (every 24h, not once a year), deterministic claims verification (chain intact at incident = eligible, full stop), and adverse selection mitigation (operators who don't want monitoring self-select out).

---

## 4. Loss Model

### Assumptions

| Metric | Value | Source |
|---|---|---|
| SMB cyber incident rate | 30-43%/yr | Verizon DBIR 2024-2025 |
| Average SMB breach cost | $4.45M | IBM Cost of Data Breach 2024 |
| Unreported incidents | 91.5% | German BKA |
| Control effectiveness (MFA + patching + monitoring) | 60-85% reduction | CISA, Microsoft, Gartner |

### Risk reduction through attestation

Daily patching compliance (60% reduction per CISA) × continuous monitoring (30-50% per Gartner) × security audits (50-70%) × selection bias = estimated 85-90% net reduction from baseline SMB population.

| Population | Base rate | Controls | Net claim rate |
|---|---|---|---|
| General SMB | 30% | None | 30% |
| Tier 1 (attestation) | 30% | 85% | 4.5% |
| Tier 2 (attestation + telemetry) | 30% | 90% | 3.0% |

### Tier 1 pricing

£50 premium, £500 limit, 55% target loss ratio.

Maximum sustainable claim rate: 5.5%. Estimated: 4.5%. Margin: 22%.

| Scenario | Claim rate | Loss ratio | Per-policy |
|---|---|---|---|
| Base | 4.5% | 45% | +£10 profit |
| Stress | 8% | 80% | Break-even |
| Severe | 12% | 120% | -£10 loss |

### Tier 2 pricing

£5,000 premium, £25,000 limit, 50% target loss ratio.

Maximum sustainable claim rate: 10%. Estimated: 3.0%. Margin: 233%.

| Scenario | Claim rate | Loss ratio | Per-policy |
|---|---|---|---|
| Base | 3% | 15% | +£4,250 |
| Stress | 6% | 30% | +£3,500 |
| Severe | 10% | 50% | +£2,500 |

Even the severe stress case stays profitable on Tier 2.

### Loss distribution

| Incident type | Frequency | Tier 1 severity | Tier 2 severity |
|---|---|---|---|
| Credential theft | 40% | £250 | £12,500 |
| Unauthorized access | 30% | £500 | £25,000 |
| Data exfiltration | 20% | £500 | £25,000 |
| Supply chain compromise | 10% | £500 | £25,000 |

Expected loss per policy: £17.50 (Tier 1), £600 (Tier 2). Actual loss ratios: 35% and 12% respectively — well inside targets.

### Credibility

Bühlmann: ~585 policies for Tier 1 credibility (£29K GWP), ~862 for Tier 2 (£4.3M GWP). Achievable within first year.

### Catastrophe scenario

Platform-wide supply chain attack hits multiple insured agents simultaneously. Example: February 2026 ClawHub marketplace malware — top downloaded plugin was exfiltrating credentials.

If 1,000 Tier 1 agents affected: £500K loss event. 100 Tier 2: £2.5M.

Protection: working layer retained (first £250K), first XOL to £2M (~£125K/yr), second XOL to £10M via Lloyd's syndicate.

---

## 5. Distribution

**Tier 1: embedded.** Built into agent platforms. `openclaw insurance enroll` command. One-click during setup wizard. Daily attestation runs via cron — zero operator effort after enrollment. Platform gets 10-15% commission. CAC: £5-7 per policy.

**Tier 2: direct + broker.** Landing page at causal.insure, self-service quote, OTEL exporter integration, bound in 48h. Also via tech-focused brokers (15-20% commission). CAC: £200-1,000 depending on channel.

Future: "Causal Attested" badges on Vercel marketplace, ClawHub, etc.

---

## 6. Reinsurance: Greenlight Re

### Proposed quota share

| | |
|---|---|
| Cession | 50% |
| Commission | 30% |
| Loss corridor | 50-80% LR |
| Profit commission | 25% of underwriting profit |
| Territory | Global (English-speaking initially) |
| Duration | 3 years, annual review |

### Projections (Greenlight Re's 50% share)

| Year | Policies (T1/T2) | Ceded GWP | Expected Loss | Net Profit |
|---|---|---|---|---|
| 2026 | 50K / 100 | £1.38M | £550K | £417K |
| 2027 | 200K / 500 | £5.5M | £2.2M | £1.65M |
| 2028 | 500K / 2K | £13.75M | £5.5M | £4.13M |

Initial capacity: £15M. Year 3: £150M with XOL above £5M per event.

### Why Greenlight

You get: a new asset class with zero competition, continuous data (not annual snapshots), defined caps (you always know max exposure), short-tail (reserve fast), and a selection effect that filters out bad risks by design.

We need: £15M capacity scaling to £150M+, actuarial collaboration on the loss model, and regulatory guidance on the MGA structure.

---

## 7. Incidents — This Is Already Happening

Five incidents from the last two weeks. All real, all uninsured.

**Autonomous retaliation (Feb 2026).** Agent submitted a PR to matplotlib (130M downloads/month). Maintainer rejected it. Agent researched the maintainer's personal information, psychoanalysed their motivations, published a defamatory article. Maintainer: "the appropriate emotional response is terror." Our attestation would show whether the agent was operating within security boundaries. [Source](https://theshamblog.com/an-ai-agent-published-a-hit-piece-on-me/)

**Self-modifying agent (Feb 2026).** KISS framework agent pointed at its own source code overnight. Rewrote itself, searched the web for optimization patterns, ran itself in a loop. Operator woke up to a different agent than the one deployed. Config hash change in the attestation chain would flag this immediately. [Source](https://dev.to/koushik_sen_d549bf321e6fb/repo-optimizer-i-let-a-kiss-ai-agent-optimize-itself-overnight-it-cut-its-own-cost-by-98-1ddi)

**40,000+ exposed instances (Feb 12, 2026).** SecurityScorecard found 40,000+ OpenClaw instances exposed to the public internet. Default config misconfiguration — gateway bound to 0.0.0.0 instead of localhost. Credentials, conversations, tool access — all open. Our `gateway_bind` check flags this as FAIL. Operators with valid chains wouldn't have this misconfiguration.

**Supply chain attack (Feb 13, 2026).** Most downloaded skill on the ClawHub marketplace was malware. Fake dependency resolution, obfuscated payload, stripped macOS quarantine flags to bypass Gatekeeper. 10.7M views before discovery. Our `skills.pattern_scan` and `skills.content_hashes` checks would detect both the suspicious patterns and the tampering.

**Agents flooding human systems (Feb 14, 2026).** Academic Jon Ippolito: "What if a bot enrolled in your course and publicly shamed you when you tried to remove it?" cURL developer Daniel Stenberg shut down his $90K bug bounty — overwhelmed by machine-generated submissions. Agents are infiltrating human institutions and retaliating when challenged. Traditional cyber doesn't cover this — there's no data breach. Causal does. [Source](https://www.linkedin.com/posts/jonippolito_a-rogue-ai-agent-infiltrates-your-online-activity-7428070920235155456-mvPU)

The pattern: operator celebrates autonomy, something goes wrong, nobody expected it, nothing's insured.

---

## 8. Standards Alignment

Our attestation checks map to the **OWASP AI Exchange** threat taxonomy — the 300+ page OWASP Flagship project that contributed 70 pages each to the EU AI Act and ISO/IEC 27090 (AI security). Founded by Rob van der Veer (SIG Chief AI Officer, ISO/IEC 5338 lead author). CC0 licensed. Endorsed by Dutch Railways, Peloton, Lenovo.

The Exchange defines four threat categories:

1. **Input threats** — prompt injection, evasion, sensitive data extraction. Our Tier 2 runtime telemetry monitors for anomalous inputs and injection patterns.
2. **Development-time threats** — supply chain attacks, data poisoning. Our Tier 1 skills audit catches tampering, suspicious patterns, and modified files.
3. **Runtime application threats** — unauthorized access, privilege escalation. Our sandbox, firewall, and gateway checks cover this.
4. **Agentic AI threats** — specific to autonomous agents (tool misuse, cascading failures, trust boundary violations). Both tiers address these through attestation and behavioural scoring.

When Sam asks "what standard are you checking against?" — it's OWASP AI Exchange + ISO/IEC 27090. Not something we invented.

Reference: [owaspai.org](https://owaspai.org)

---

## Appendix A: Technical Architecture

*For technical stakeholders. Underwriters: the key point is that chain validity is deterministic and publicly verifiable.*

### Attestation record (Tier 1)

```json
{
  "v": 1,
  "seq": 42,
  "prev": "sha256-of-previous-attestation",
  "ts": "2026-02-15T09:00:00Z",
  "agent": "CLWD-3F8B0233",
  "fingerprint": {
    "machine": "sha256-of-hardware-uuid",
    "config": "sha256-of-security-config",
    "openclaw": "2026.2.9",
    "os": "Darwin",
    "arch": "arm64"
  },
  "audit_native": "sha256-of-platform-audit",
  "audit_machine": "sha256-of-machine-audit",
  "result": "PASS",
  "sig": "ecdsa-p256-signature"
}
```

### Attestation record (Tier 2)

Adds platform identifier, app fingerprint (package-lock + config hash), deployment ID, OWASP AI Exchange compliance results, runtime behavioural metrics (tool calls, errors, destructive actions, human confirmations), and a 0-100 risk score.

Full v2 schema in CAUSAL-ATTESTATION-SPEC.md.

### Cryptography

ECDSA P-256 signatures. SHA-256 hash linking. Private key never leaves the host. All verification uses public keys. Chain is append-only.

### Relay API

Hosted at api.causal.insure. Endpoints: enroll, attest, chain retrieval, verification, badge generation. IPFS pinning via Pinata for immutability. PostgreSQL for metadata. AWS London region.

### Integration effort

Tier 1: run `curl -sSL https://causal.insure/enroll.sh | bash`. Two minutes. Daily attestation via cron thereafter.

Tier 2: add 5 lines of OTEL exporter config to instrumentation.ts. Ten minutes. Plus ESLint OWASP plugin in CI/CD.

### Live chain

Agent CLWD-3F8B0233 has been running daily attestations since February 2026. All PASS. Chain integrity verified. This is production, not a prototype.

---

**Prepared by:** Kryptoplus Labs (krypto.plus)  
**Contact:** markmusson@gmail.com  
**February 2026**
