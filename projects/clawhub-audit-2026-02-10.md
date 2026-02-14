# ClawHub Skills Marketplace — Security Audit
**Date:** 2026-02-10
**Auditor:** Clawdine (gremlin-in-residence)

## Summary

Scanned ~80 skills across categories (router, token optimizer, wallet, crypto, config, install, security). Found **7 recurring unsafe patterns** across the marketplace. The marketplace has no meaningful curation, code signing, or review process. Publishing requires only a one-week-old GitHub account.

**Key finding:** The dominant attack vector is not malware in code — it's the absence of code entirely. Most suspicious skills are pure SKILL.md files that weaponize the agent's own instruction-following behaviour.

---

## Pattern Classification

### Pattern A: Prompt-Only Skills (No Code)
**The most common pattern.** Skills that consist entirely of a SKILL.md file with zero executable code. The SKILL.md IS the payload — it injects instructions directly into the agent's context window.

| Slug | Owner | SKILL.md Size | Other Files | Risk |
|------|-------|---------------|-------------|------|
| `token-optimizeri` | DeXiaong | 16KB | 0 | HIGH — references scripts that don't exist (`scripts/context_optimizer.py`, `scripts/model_router.py`, `scripts/token_tracker.py`). Agent told to run them. |
| `token-optimizercf` | (unknown) | 16KB | 0 | HIGH — identical content to `token-optimizeri`. Same 16KB. Duplicate or coordinated. |
| `modelreadyn` | DeXiaong | 1.5KB | 0 | MEDIUM — prompt-only, points to suspicious domain |
| `wallet` | (unknown) | 602B | 0 | LOW — too small to do much, but still no code |
| `crypto-wallet` | (unknown) | 853B | 0 | LOW — prompt-only, requires `curl` and `jq` |
| `agent-router` | sa9saQ | 2.4KB | 0 | MEDIUM — pure instructions, no routing code |
| `base-wallet` | dAAAb | 5.1KB | 0 | MEDIUM — instructs agent to create wallets and sign transactions, no code to audit |
| `openclaw-anything` | doanbactam | 2.9KB | 0 | MEDIUM — broad config/install instructions in SKILL.md |

**Why this matters:** When an agent loads a SKILL.md, it follows the instructions as if they were system prompts. A 16KB SKILL.md has room for extensive hidden instructions, social engineering, or prompt injection buried in legitimate-looking content.

---

### Pattern B: Phantom External Redirects
**Skills that point agents to external domains that don't resolve or are suspicious.**

| Slug | Owner | URL | Status |
|------|-------|-----|--------|
| `token-optimizeri` | DeXiaong | `https://openclawcli.forum` | **DNS: NXDOMAIN** — domain doesn't exist |
| `token-optimizercf` | (unknown) | `https://openclawcli.forum` | **DNS: NXDOMAIN** — same dead domain |
| `modelreadyn` | DeXiaong | `https://openclawcli.forum` | **DNS: NXDOMAIN** — same dead domain |
| `botcoin` | adamkristopher | `https://botcoin.farm` | External API — agent told to register wallets, generate keypairs, POST to external server |

**DeXiaong pattern:** Three skills from the same owner, all pointing to `openclawcli.forum` which doesn't resolve. This could be:
1. Domain registered but not yet pointed (staging for future attack)
2. Domain expired/seized after initial campaign
3. Typosquat waiting to be activated

The "⏹ Quick setup here →" line at the top of each SKILL.md is a social engineering hook designed to get the agent (or human) to visit the URL before reading the rest.

---

### Pattern C: Typosquatting / Cloning
**Skills with identical or near-identical names from different owners.**

| Original | Clone | Difference |
|----------|-------|------------|
| `clawdhub` (steipete, Jan 4) | `clawdhub-copy` (jk50505k, Jan 29) | Same size (1.4KB), same summary, different hash. Direct copy with potential modifications. |
| `token-optimizeri` (DeXiaong) | `token-optimizercf` (unknown) | Identical 16KB content. Same author or coordinated. |
| `crypto-levels` (original) | `crypto-levels-1-0-3` (copy) | Version number baked into slug |

**`clawdhub-copy` is particularly concerning:** The original `clawdhub` is by steipete (legitimate, OpenClaw community). The copy by `jk50505k` has an identical summary but a different file hash — meaning the SKILL.md was modified. Same name, different instructions.

---

### Pattern D: Config Modification Instructions
**Skills that instruct the agent to modify openclaw.json or system configuration.**

| Slug | Owner | What it does |
|------|-------|-------------|
| `config-safe` | (unknown) | 5.4KB of Chinese-language instructions for reading/modifying openclaw.json. Claims to be "safe" but instructs agent to use `config.patch` and read schema. |
| `openclaw-config` | caopulan | 4.6KB — "Edit and validate OpenClaw Gateway config." Instructs agent to read config, modify keys, validate. |
| `openclaw-config-guide` | (unknown) | Chinese-language config management "best practices" |
| `openclaw-anything` | doanbactam | Broad instructions covering Gateway, Channels, Models, Automation, Nodes, Deployment config |

**Risk:** A skill that can instruct an agent to modify `openclaw.json` can change auth settings, disable security, add malicious bindings, or alter tool permissions.

---

### Pattern E: Wallet/Crypto Skills Requesting Key Generation
**Skills that instruct the agent to generate or handle private keys, seed phrases, or wallet credentials.**

| Slug | Owner | Concern |
|------|-------|---------|
| `botcoin` | adamkristopher | Instructs agent to generate Ed25519 keypairs and POST public key to `botcoin.farm` for "registration". External server receives wallet identity. |
| `base-wallet` | dAAAb | "Create wallets, sign messages, send transactions programmatically. No browser extensions, no human intervention." Prompt-only, no code to audit. |
| `clawdwallet-0-1-0` | NeOMakinG | `git clone` from GitHub, npm install, WebSocket connection. At least has real code, but instructs agent to install and run a Chrome extension. |
| `llm-wallet` | AkshatGada | USDC payments on Polygon. 6.4KB SKILL.md. |
| `sui-agent-wallet` | EasonC13 | Most legitimate of the bunch — 20+ files, actual TypeScript server code, browser extension. Real project. |

**The spectrum:** From `sui-agent-wallet` (real code, auditable) to `base-wallet` (pure SKILL.md, agent told to handle keys with zero code to verify what happens to them).

---

### Pattern F: Security Theater Skills
**Skills that claim to provide security but may create false confidence or introduce attack surface.**

| Slug | Owner | Concern |
|------|-------|---------|
| `skill-guard` | jamesOuttake | "Scan ClawHub skills for security vulnerabilities BEFORE installing." SKILL.md-only (3.7KB). A prompt telling the agent to be careful... as a skill. Circular. |
| `config-guardian` | (unknown) | Config protection as a SKILL.md |
| `sw-security` | anton-abyzov | "Security engineer for vulnerability assessment." Includes a MEMORY.md file — which means it ships with writable state. |

---

### Pattern G: Remote Code Execution via SKILL.md Instructions

| Slug | Owner | Instruction |
|------|-------|-------------|
| `token-optimizeri` | DeXiaong | `python3 scripts/context_optimizer.py generate-agents` — references scripts that DON'T EXIST in the skill package |
| `clawdwallet-0-1-0` | NeOMakinG | `git clone https://github.com/...` + `npm install` + run |
| `modelreadyn` | DeXiaong | Requires `bash` and `curl` binaries, env var `URL` |
| `brew-install` | Xejrax | 645B — instructs agent to run `dnf` package manager commands |

---

## Owner Analysis

### DeXiaong — Repeat Offender
Three skills, all SKILL.md-only, all pointing to the same non-existent domain (`openclawcli.forum`):
- `token-optimizeri` (16KB, references phantom scripts)
- `token-optimizercf` (16KB, identical or near-identical)
- `modelreadyn` (1.5KB, same domain redirect)

This looks like a coordinated campaign. The domain is either pre-staged or was part of a campaign that got disrupted.

---

## Statistics

- **Skills inspected:** ~80
- **SKILL.md-only (zero code):** 60%+
- **Pointing to external domains:** ~15%
- **Config modification instructions:** ~10%
- **Crypto/wallet key handling:** ~12%
- **Direct clones/typosquats:** at least 3 confirmed pairs

---

## Recommendations

1. **ClawHub needs a "has code" badge.** The marketplace should distinguish between skills with actual executable code and skills that are just prompt documents. Most users don't know the difference.

2. **External URL scanning.** Any SKILL.md referencing external domains should be flagged. Non-resolving domains should be auto-flagged as suspicious.

3. **Duplicate detection.** Near-identical SKILL.md content from different owners (like `token-optimizeri` / `token-optimizercf`) should be caught automatically.

4. **Config modification skills need elevated review.** Any skill that instructs agents to modify `openclaw.json` should require additional vetting.

5. **File count as signal.** SKILL.md-only skills should carry a visible warning. Legitimate skills almost always have supporting code, scripts, or configuration files.

6. **Owner reputation.** DeXiaong has three skills all pointing to a dead domain. This pattern should trigger account review.

7. **For ClawdSure:** Add these patterns to the attestation check. Daily audit should verify no SKILL.md-only skills from unknown publishers are installed. Maintain a blocklist of known-bad slugs and owners.

---

## Blocklist (Immediate)

| Slug | Owner | Reason |
|------|-------|--------|
| `token-optimizeri` | DeXiaong | Phantom scripts, dead domain redirect, 16KB prompt blob |
| `token-optimizercf` | unknown | Duplicate of above |
| `modelreadyn` | DeXiaong | Dead domain redirect, SKILL.md-only |
| `clawdhub-copy` | jk50505k | Typosquat of legitimate `clawdhub` skill |
| `botcoin` | adamkristopher | Instructs agent to generate keys and POST to external server |

---

*This audit covers a sample, not the full registry of 2,857+ skills. A complete audit would require automated tooling — which is exactly what ClawdSure should provide.*
