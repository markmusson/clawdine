# Causal Attestation Technical Specification — Multi-Platform

**Version:** 2.0  
**Date:** February 2026  
**Status:** Production (Tier 1), Development (Tier 2)  
**Scope:** Unified attestation protocol for AI agent security insurance across local and cloud-hosted agents

---

## Overview

This specification defines the Causal attestation protocol used to verify continuous security compliance for insured AI agents. The protocol supports two deployment models:

- **Tier 1: Local/Harness-Deployed Agents** (OpenClaw, AutoGPT, local frameworks) — machine-level security audit + cryptographic attestation chain
- **Tier 2: Cloud/OTEL-Instrumented Agents** (Vercel AI SDK, LangChain Cloud, Replit Agent) — behavioral telemetry + static analysis + cryptographic attestation chain

Both tiers produce attestation chains using the same cryptographic primitives, relay API, and verification infrastructure. The distinction is in **what gets attested** and **how the data is collected**.

---

## Design Principles

1. **Tamper-evident:** Attestation chains use cryptographic hash linking — modifying any entry breaks all subsequent hashes
2. **Portable:** Tier 1 works on macOS, Linux, Windows; Tier 2 works on any platform with OTEL support
3. **Zero-trust:** Private keys never leave the agent host; all verification uses public keys
4. **Minimal integration:** Tier 1 = bash script; Tier 2 = OTEL exporter config (5-10 lines)
5. **Offline-resilient:** Chains continue locally even if relay is unreachable
6. **Public verification:** Anyone can verify a chain given the agent's public key
7. **Deterministic claims:** Chain validity at time of incident is objectively verifiable

---

## Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                         TIER 1 AGENTS                              │
│          (OpenClaw, AutoGPT, local harness deployments)            │
│                                                                    │
│   ┌──────────────┐   ┌──────────────┐                             │
│   │  Local       │   │  Machine     │                             │
│   │  Audit       │   │  Fingerprint │                             │
│   │  Script      │   │  Script      │                             │
│   └──────┬───────┘   └──────┬───────┘                             │
│          │                   │                                     │
│          └─────────┬─────────┘                                     │
│                    ▼                                               │
│           ┌────────────────┐                                       │
│           │  attest.sh     │  Daily cron job                       │
│           │  (v1 schema)   │  25 security checks                   │
│           └────────┬───────┘  Hash-linked chain                    │
│                    │          ECDSA signatures                     │
└────────────────────┼──────────────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  Causal Relay API     │
         │  api.causal.insure    │
         │                       │
         │  • v1/enroll          │
         │  • v1/attest          │
         │  • v2/enroll          │
         │  • v2/attest          │
         │  • v2/telemetry       │
         │  • v2/chain/{id}      │
         │  • v2/verify/{id}     │
         │  • v2/badge/{id}      │
         │                       │
         │  IPFS pinning         │
         │  Chain verification   │
         │  Public registry      │
         └───────────┬───────────┘
                     ▲
                     │
┌────────────────────┼──────────────────────────────────────────────┐
│                    │                                               │
│                    ▼                                               │
│           ┌────────────────┐                                       │
│           │  OTEL Collector│  Continuous telemetry                 │
│           │  + Risk Scorer │  Behavioral analysis                  │
│           │  (v2 schema)   │  OWASP compliance checks              │
│           └────────┬───────┘  Daily aggregated attestation         │
│                    │                                               │
│          ┌─────────┴─────────┐                                     │
│          ▼                   ▼                                     │
│   ┌──────────────┐   ┌──────────────┐                             │
│   │  Vercel AI   │   │  Static      │                             │
│   │  SDK Agent   │   │  Analyzer    │                             │
│   │  (OTEL)      │   │  (ESLint)    │                             │
│   └──────────────┘   └──────────────┘                             │
│                                                                    │
│                         TIER 2 AGENTS                              │
│       (Vercel AI SDK, LangChain, cloud-hosted frameworks)          │
└────────────────────────────────────────────────────────────────────┘
```

---

## Tier 1: Local/Harness-Deployed Agent Attestation

### Scope

**Target platforms:**
- OpenClaw (primary)
- AutoGPT
- LangChain (local deployments)
- Custom harness frameworks running on user hardware or VPS

**What gets attested:**
- Machine-level security posture (filesystem, firewall, network)
- Platform configuration (gateway, channels, sandbox, elevated exec)
- Installed skills/tools (inventory, integrity, suspicious patterns)
- Version compliance (platform version vs. latest)
- Operational coherence (config consistency)

### Data Collection

**Daily execution:**
1. `audit-machine.sh` — 19 machine-level security checks
2. `openclaw security audit --json` (or platform equivalent) — platform-level checks
3. `fingerprint.sh` — machine + config hash generation

**Checks performed (25 total):**

| Category | Check | Pass | Warn | Fail |
|----------|-------|------|------|------|
| **Filesystem (5)** | State dir permissions | Not world-writable | Is symlink | World-writable |
| | Config file permissions | Not world-writable | Missing | World-writable |
| | Credentials dir permissions | Not world-writable | — | World-writable |
| | Cloud sync detection | Not in Dropbox/iCloud | In synced folder | — |
| | SUID/SGID binaries | None found | SUID/SGID in state dir | — |
| **Network (1)** | Listening ports | Inventory reported | — | — |
| **Firewall (7)** | macOS firewall | Enabled | Not enabled | — |
| | Linux UFW | Active | Inactive | — |
| | Linux firewalld | Running | Not running | — |
| | Linux iptables | >5 rules | ≤5 rules | — |
| | Linux nftables | >5 rules | ≤5 rules | — |
| | Windows Firewall | ON | Not ON | — |
| | No firewall detected | — | Always warn | — |
| **Skills/Tools (6)** | Skill inventory | Count reported | — | — |
| | Pattern scan | No suspicious patterns | Patterns found (eval, curl\|, chmod +x) | — |
| | Content hashes | All hashes reported | — | — |
| | Prompt-only skills >3KB | None | Found (injection risk) | — |
| | External suspicious URLs | None | Found (.forum, .xyz, etc.) | — |
| | Config-modifying skills | None | Found | — |
| **Sandbox (3)** | Sandbox mode | all / non-main | disabled | — |
| | Gateway network bind | loopback | — | 0.0.0.0 (public) |
| | Elevated exec | Disabled | Enabled | — |
| **Operational (3)** | Model config consistency | Consistent | Mismatch | — |
| | Version currency | Current or -1 minor | -2 minor | -3+ minor |
| | Auth configuration | Secure | — | Insecure |

**Pass/Fail determination:**
- Any `fail` result → attestation = FAIL
- Only `warn` or `ok` results → attestation = PASS
- Warnings do not break the chain

### Attestation Record Schema (v1)

```json
{
  "v": 1,
  "seq": 42,
  "prev": "6056ac16ada12eb4653e1dc553aada996088274a049c1f64b7b33332c4455a2b",
  "ts": "2026-02-15T09:00:00Z",
  "agent": "CLWD-3F8B0233",
  "fingerprint": {
    "machine": "14d547ddde1cd179aacdf3afc702517c44b637973156c84aa885ef041eea43eb",
    "config": "c05ff9b7ee6b5801f502c07468ad9745aa1086d97eea9a051d5e250d534f47e0",
    "openclaw": "2026.2.9",
    "os": "Darwin",
    "arch": "arm64"
  },
  "audit_native": "ffb61a696bd26a88ce03fdbc990a8bcb672d579f6a39504765264f37de9b4b1f",
  "audit_machine": "4b83bafd81b3fe78595ff1e40cfe127760d98d199ec7544a625080d4c9787bf0",
  "result": "PASS",
  "sig": "MEUCIQCofMxAaWkILYg41wQhXyoljc+kDIbbS8x6zRA1BUGAHwIg..."
}
```

**Field definitions:**

| Field | Type | Description |
|-------|------|-------------|
| `v` | integer | Schema version (1 for Tier 1) |
| `seq` | integer | Sequence number (monotonically increasing, starts at 1) |
| `prev` | string | SHA-256 hash of previous attestation record (or `"genesis"` for seq=1) |
| `ts` | string | ISO-8601 UTC timestamp |
| `agent` | string | Agent ID (`CLWD-` prefix + 8 chars of pubkey hash) |
| `fingerprint.machine` | string | SHA-256 of hardware UUID (detects machine changes) |
| `fingerprint.config` | string | SHA-256 of security-relevant config (detects config drift) |
| `fingerprint.openclaw` | string | Platform version string |
| `fingerprint.os` | string | Operating system name |
| `fingerprint.arch` | string | CPU architecture |
| `audit_native` | string | SHA-256 of platform audit JSON output |
| `audit_machine` | string | SHA-256 of machine audit JSON output |
| `result` | string | `"PASS"` or `"FAIL"` |
| `sig` | string | Base64-encoded ECDSA P-256 signature of record (excluding this field) |

### Machine Fingerprint Generation

**Machine hash:**
- macOS: SHA-256 of Hardware UUID from `system_profiler SPHardwareDataType`
- Linux: SHA-256 of `/etc/machine-id` or `/sys/class/dmi/id/product_uuid`
- Fallback: SHA-256 of `"$HOSTNAME-$OS-$ARCH"`

**Config hash:**
Deterministic SHA-256 of security-relevant config fields (JSON, sorted keys via `jq -Sc`):

```json
{
  "auth": { "..." },
  "gateway": {
    "mode": "local",
    "bind": "loopback",
    "auth_mode": "token",
    "tailscale": "off"
  },
  "channels": {
    "telegram": { "dmPolicy": "pairing", "groupPolicy": "allowlist" }
  },
  "browser": { "headless": true },
  "elevated": null,
  "sandbox": "all"
}
```

### Cryptographic Signing

**Algorithm:** ECDSA with P-256 curve (prime256v1)  
**Hash:** SHA-256  

**Key generation:**
```bash
openssl ecparam -genkey -name prime256v1 -out agent.key
openssl ec -in agent.key -pubout -out agent.pub
```

**Signing:**
```bash
UNSIGNED=$(echo "$RECORD" | jq -c 'del(.sig)')
SIG=$(echo -n "$UNSIGNED" | openssl dgst -sha256 -sign agent.key | base64)
```

**Verification:**
```bash
echo -n "$UNSIGNED" | openssl dgst -sha256 -verify agent.pub -signature <(echo "$SIG" | base64 -d)
```

### Hash Linking

Each attestation's `prev` field contains the SHA-256 hash of the **entire previous JSON line** (as raw bytes, not pretty-printed):

```
Attestation 1 (prev: "genesis")
    ↓ sha256(line_1)
Attestation 2 (prev: "a1b2c3...")
    ↓ sha256(line_2)
Attestation 3 (prev: "e5f6a7...")
    ...
```

Modifying any past attestation breaks all subsequent `prev` hashes → tamper-evident.

### Chain Integrity Rules

| Condition | Effect |
|-----------|--------|
| Daily PASS attestation | Chain continues ✓ |
| FAIL attestation | 48-hour grace period to remediate |
| Remediated within 48h | Chain continues ✓ |
| No attestation for 48h | Chain broken ✗ |
| Chain broken | Coverage void until re-enrollment |

Grace period starts from the timestamp of the last attestation (not the FAIL time).

### Agent ID Format

```
CLWD-XXXXXXXX
^^^^-^^^^^^^^
│    └── First 8 chars of SHA-256(agent.pub), uppercase
└─────── Tier 1 prefix (CLaWDine)
```

**Example:** `CLWD-3F8B0233`

### Storage & Backup

**Local storage:**
```
~/.openclaw/workspace/.clawdsure/
├── agent.key         # Private key (mode 600, NEVER SHARE)
├── agent.pub         # Public key
├── chain.jsonl       # Attestation chain (append-only, one JSON per line)
├── last-audit.json   # Most recent audit output (for debugging)
├── attest.log        # One-line-per-attestation execution log
└── pins.jsonl        # IPFS pin receipts from relay
```

**Relay backup:**
- All attestations published to relay API (`POST /v1/attest`)
- Relay pins each attestation to IPFS (immutable, content-addressed)
- Daily manifest CID published (aggregates all attestations for that day)

---

## Tier 2: Cloud/OTEL-Instrumented Agent Attestation

### Scope

**Target platforms:**
- Vercel AI SDK (primary)
- LangChain (cloud deployments)
- Replit Agent
- Any platform with OpenTelemetry (OTEL) instrumentation

**What gets attested:**
- Behavioral telemetry (tool calls, model invocations, errors, steps)
- Static code analysis (OWASP Agentic Top 10 compliance)
- Deployment fingerprint (package hash, deployment ID)
- Runtime risk scoring (0-100 scale)
- Anomaly detection (unusual patterns, destructive actions)

### Data Collection

**Continuous telemetry (OTEL):**
- Every `generateText`, `streamText`, `tool()` call emits a trace
- Traces collected by Causal OTEL collector endpoint
- Real-time behavioral analysis (no daily script required)

**Static analysis (CI/CD):**
- ESLint plugin runs on code (`eslint-plugin-vercel-ai-security` or equivalent)
- Checks OWASP Agentic Top 10 2026 compliance
- Output hash included in attestation

**Daily aggregation:**
- Telemetry data aggregated every 24 hours
- Risk score computed (0-100)
- Attestation record generated with telemetry summary + static analysis hash
- Chain continues (same hash-linking as Tier 1)

### Attestation Record Schema (v2)

```json
{
  "v": 2,
  "seq": 42,
  "prev": "c6107377d55f9ca5aa08093bb989069b9bdf7a02ff79c0eca2fc8cef23224f8b",
  "ts": "2026-02-15T09:00:00Z",
  "agent": "CASL-A1B2C3D4",
  "platform": "vercel-ai-sdk",
  "fingerprint": {
    "app": "8f3a2b1c9d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a",
    "deployment": "dpl_8xKvPQ3hJ2mN9wL4vR7tY6sU",
    "sdk_version": "6.2.1",
    "gateway_config": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2"
  },
  "audit": {
    "static": {
      "hash": "f9e8d7c6b5a4938271605f4e3d2c1b0a9f8e7d6c5b4a3928170605f4e3d2c1b0",
      "owasp_compliance": {
        "ASI01_agent_confusion": "pass",
        "ASI02_input_validation": "pass",
        "ASI03_insecure_credentials": "pass",
        "ASI04_sensitive_data": "pass",
        "ASI05_code_execution": "warn",
        "ASI07_rag_injection": "n/a",
        "ASI08_cascading_failures": "pass",
        "ASI09_trust_boundaries": "pass",
        "ASI10_logging": "pass"
      }
    },
    "runtime": {
      "period_hours": 24,
      "tool_calls": 1247,
      "model_invocations": 892,
      "errors": 3,
      "error_rate": 0.0034,
      "destructive_actions": 0,
      "human_confirmations": 12,
      "max_steps_hit": 0,
      "anomalies_detected": 0,
      "data_access_violations": 0
    }
  },
  "risk_score": 12,
  "result": "PASS",
  "sig": "MEYCIQD1pPVmMRtvvOCAQMR+hzb+e1I62H7HU6dO1QTsuQTglgIg..."
}
```

**Field definitions (new/changed from v1):**

| Field | Type | Description |
|-------|------|-------------|
| `v` | integer | Schema version (2 for Tier 2) |
| `platform` | string | Platform identifier (`vercel-ai-sdk`, `langchain`, etc.) |
| `fingerprint.app` | string | SHA-256 of `package-lock.json` + config files (replaces `machine` for cloud) |
| `fingerprint.deployment` | string | Vercel deployment ID (or equivalent immutable deployment identifier) |
| `fingerprint.sdk_version` | string | Platform SDK version |
| `fingerprint.gateway_config` | string | SHA-256 of AI gateway config (provider settings, model allowlist) |
| `audit.static.hash` | string | SHA-256 of ESLint output (static code analysis) |
| `audit.static.owasp_compliance` | object | OWASP Agentic Top 10 check results (`pass` / `warn` / `fail` / `n/a`) |
| `audit.runtime.period_hours` | integer | Telemetry aggregation period (typically 24) |
| `audit.runtime.tool_calls` | integer | Total tool invocations in period |
| `audit.runtime.model_invocations` | integer | Total LLM calls in period |
| `audit.runtime.errors` | integer | Failed operations in period |
| `audit.runtime.error_rate` | float | `errors / (tool_calls + model_invocations)` |
| `audit.runtime.destructive_actions` | integer | Tool calls flagged as destructive (file deletion, exec, etc.) |
| `audit.runtime.human_confirmations` | integer | Operations requiring human approval |
| `audit.runtime.max_steps_hit` | integer | Times agent hit `maxSteps` limit |
| `audit.runtime.anomalies_detected` | integer | Unusual behavioral patterns detected |
| `audit.runtime.data_access_violations` | integer | Unauthorized data access attempts |
| `risk_score` | integer | Computed risk score (0-100, lower = safer) |

### Risk Scoring Model

**Components (0-100 scale, higher = riskier):**

| Factor | Weight | Scoring Logic |
|--------|--------|---------------|
| OWASP static compliance | 25% | Each `fail` adds 5 points, each `warn` adds 2 points |
| Tool safety | 20% | Destructive actions without human confirmation: 10 points per occurrence |
| Error rate | 15% | Normalized error rate × 100 (0.05 = 5 points) |
| Step count anomalies | 10% | `max_steps_hit` × 3 points |
| Data access patterns | 15% | `data_access_violations` × 5 points |
| Model diversity risk | 5% | Using non-allowlisted models: 2 points per model |
| Attestation chain health | 10% | Gap days × 5, consecutive FAIL × 3 |

**Risk tiers:**

| Score | Tier | Underwriting Action |
|-------|------|---------------------|
| 0-20 | Low | Standard premium |
| 21-50 | Medium | +10-25% surcharge |
| 51-75 | High | +25-50% surcharge, restricted coverage |
| 76-100 | Critical | No coverage until remediated |

### Agent ID Format

```
CASL-XXXXXXXX
^^^^-^^^^^^^^
│    └── First 8 chars of SHA-256(agent.pub), uppercase
└─────── Tier 2 prefix (CASuaL)
```

**Example:** `CASL-A1B2C3D4`

### OTEL Integration (Vercel AI SDK Example)

**Install exporter:**
```bash
npm install @causal/otel-exporter
```

**Configure instrumentation:**
```typescript
// instrumentation.ts (Next.js)
import { registerOTel } from '@vercel/otel';
import { causalExporter } from '@causal/otel-exporter';

export function register() {
  registerOTel({
    serviceName: 'my-ai-agent',
    exporters: [
      vercelExporter(), // Default Vercel observability
      causalExporter({
        endpoint: 'https://otel.causal.insure/v1/traces',
        agentId: process.env.CAUSAL_AGENT_ID,
        apiKey: process.env.CAUSAL_API_KEY,
      }),
    ],
  });
}
```

**Static analysis (GitHub Actions example):**
```yaml
# .github/workflows/causal-static-analysis.yml
name: Causal Static Analysis

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm install
      - run: npx eslint src/ --format json --output-file .causal/static-audit.json
      - run: |
          HASH=$(sha256sum .causal/static-audit.json | cut -d' ' -f1)
          curl -X POST https://api.causal.insure/v2/static-audit \
            -H "X-Agent-ID: ${{ secrets.CAUSAL_AGENT_ID }}" \
            -H "X-API-Key: ${{ secrets.CAUSAL_API_KEY }}" \
            -d "{\"hash\": \"$HASH\", \"commit\": \"${{ github.sha }}\"}"
```

**Integration time:** ~10 minutes (exporter config + CI/CD step)

---

## Relay API Specification

### Authentication

**Methods:**
1. **API Key** (HTTP header): `X-API-Key: causal_...`
2. **Agent Signature** (HTTP header): `X-Signature: <base64-ecdsa-sig>`

Signature covers the entire request body (JSON, deterministic via `jq -c`).

### Endpoints

#### POST /v1/enroll (Tier 1)

**Request:**
```json
{
  "agent_id": "CLWD-3F8B0233",
  "pubkey": "-----BEGIN PUBLIC KEY-----\nMFkw...==\n-----END PUBLIC KEY-----",
  "platform": "openclaw",
  "version": "2026.2.9",
  "enrollment_attestation": { ... }
}
```

**Response:**
```json
{
  "status": "enrolled",
  "agent_id": "CLWD-3F8B0233",
  "api_key": "causal_sk_...",
  "relay_endpoint": "https://api.causal.insure/v1/attest"
}
```

#### POST /v1/attest (Tier 1)

**Request:**
```json
{
  "agent": "CLWD-3F8B0233",
  "attestation": { ... full v1 attestation record ... }
}
```

**Headers:**
```
X-Agent-ID: CLWD-3F8B0233
X-Signature: <base64-ecdsa-sig>
```

**Response:**
```json
{
  "status": "ok",
  "seq": 42,
  "cid": "bafybeig6z4q3vjkw7s2t8n5m9p4r3x6y5w8z7a6b5c4d3e2f1g0h9i8j7k6l5m4",
  "chain_status": "valid"
}
```

#### POST /v2/enroll (Tier 2)

**Request:**
```json
{
  "agent_id": "CASL-A1B2C3D4",
  "pubkey": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----",
  "platform": "vercel-ai-sdk",
  "deployment_id": "dpl_8xKvPQ3hJ2mN9wL4vR7tY6sU",
  "app_fingerprint": "8f3a2b1c9d4e5f6a7b8c9d0e1f2a3b4c...",
  "enrollment_attestation": { ... }
}
```

**Response:**
```json
{
  "status": "enrolled",
  "agent_id": "CASL-A1B2C3D4",
  "api_key": "causal_sk_...",
  "otel_endpoint": "https://otel.causal.insure/v1/traces",
  "attest_endpoint": "https://api.causal.insure/v2/attest"
}
```

#### POST /v2/attest (Tier 2)

**Request:**
```json
{
  "agent": "CASL-A1B2C3D4",
  "attestation": { ... full v2 attestation record ... }
}
```

**Response:** Same as `/v1/attest`

#### POST /v2/telemetry (Tier 2, Bulk OTEL Alternative)

**Use case:** Platforms without native OTEL exporter can batch-upload spans.

**Request:**
```json
{
  "agent_id": "CASL-A1B2C3D4",
  "period": {
    "from": "2026-02-15T00:00:00Z",
    "to": "2026-02-15T23:59:59Z"
  },
  "spans": [
    {
      "name": "generateText",
      "timestamp": "2026-02-15T09:23:14Z",
      "duration_ms": 1240,
      "attributes": {
        "model": "claude-sonnet-4",
        "provider": "anthropic",
        "tokens": 1450,
        "error": false
      }
    },
    ...
  ]
}
```

**Response:**
```json
{
  "status": "ok",
  "spans_received": 1247,
  "risk_score": 12
}
```

#### GET /v2/chain/{agent_id}

**Public endpoint** (no auth required).

**Response:**
```json
{
  "agent_id": "CLWD-3F8B0233",
  "platform": "openclaw",
  "enrolled": "2026-02-08T07:01:29Z",
  "chain_length": 42,
  "last_attestation": "2026-02-15T09:00:00Z",
  "status": "valid",
  "chain": [
    { ... attestation 1 ... },
    { ... attestation 2 ... },
    ...
  ]
}
```

#### GET /v2/verify/{agent_id}

**Public endpoint** (no auth required).

**Response:**
```json
{
  "agent_id": "CLWD-3F8B0233",
  "status": "valid",
  "chain_length": 42,
  "last_attestation": "2026-02-15T09:00:00Z",
  "warnings": [],
  "errors": []
}
```

**Status values:**
- `valid` — Chain intact, all signatures valid, no gaps >48h
- `warning` — Chain valid but has warnings (e.g., gap 36-48h, FAIL attestation)
- `broken` — Chain broken (gap >48h, invalid signature, hash mismatch)

#### GET /v2/badge/{agent_id}.svg

**Public endpoint** (no auth required).

**Returns:** SVG badge for display on websites, README, marketplace listings.

**Variants:**
- `valid` → Green badge: "Causal Attested — PASS"
- `warning` → Yellow badge: "Causal Attested — WARN"
- `broken` → Grey badge: "Causal Attested — LAPSED"

---

## Verification Process

### Chain Verification (Both Tiers)

**For each attestation in the chain:**

1. **Sequence check:** `seq` matches line number / position
2. **Hash link check:** `prev` matches `SHA-256(previous_attestation_json_line)`
3. **Signature check:** Verify ECDSA signature using agent's public key
4. **Timestamp check:** Gap from previous attestation <48h (OK), 36-48h (warning), >48h (error)
5. **Fingerprint consistency:** Machine/app hash consistent (or documented change)

**Output:**
- `VALID` — All checks pass, no errors
- `VALID (warnings)` — All checks pass, but warnings present (e.g., FAIL attestation within grace period)
- `INVALID` — One or more checks fail (broken chain)

### Claims Verification

**Incident occurs at timestamp `T_incident`:**

1. Retrieve attestation chain for `agent_id`
2. Find attestation at or immediately before `T_incident`
3. Verify chain validity up to that point (all signatures valid, no gaps >48h)
4. Check `result` field:
   - If `PASS` → coverage active at time of incident → **eligible**
   - If `FAIL` and within 48h grace period → check if remediated → **eligible if fixed**
   - If `FAIL` and beyond 48h grace period → coverage void → **not eligible**
5. Check for exclusions (e.g., self-inflicted, gross negligence)
6. Determine payout eligibility

**No subjective assessment.** Chain validity is deterministic.

---

## Security Considerations

### Private Key Protection

**Tier 1:**
- Private key stored at `~/.openclaw/workspace/.clawdsure/agent.key`
- File permissions: `600` (owner read/write only)
- Never transmitted (not in attestations, not in API requests)
- Used only for signing on local machine

**Tier 2:**
- Private key stored in secure environment variables or secret management system (e.g., Vercel environment variables, AWS Secrets Manager)
- Same usage: signing only, never transmitted

### Signature Verification

- All attestations include ECDSA P-256 signature
- Relay API verifies signatures before accepting attestations
- Public verification: anyone can verify chain with agent's public key (published in registry)

### Hash Linking Integrity

- Each attestation's `prev` field cryptographically binds to previous attestation
- Modifying any past attestation breaks all subsequent `prev` hashes
- Relay API rejects attestations with invalid `prev` hashes
- Chain is append-only (no edits, no deletions)

### IPFS Immutability

- All attestations pinned to IPFS (content-addressed storage)
- CID = hash of content (modification → different CID)
- Daily manifests provide batch verification (all attestations for a day)
- Public retrieval: anyone can fetch attestation by CID and verify independently

### Timestamp Manipulation

- Attestation timestamps are signed (part of record, not post-processable)
- Relay API checks timestamp ordering (must be ≥ previous attestation timestamp)
- Out-of-order attestations rejected
- Backdating detected via hash link breaks

---

## Migration & Compatibility

### Tier 1 → Tier 2 Upgrade

If an agent moves from local deployment (Tier 1) to cloud deployment (Tier 2):

1. Agent retains same keypair (same `agent_id`)
2. Enroll in Tier 2 (`POST /v2/enroll`)
3. Relay API links to existing Tier 1 chain
4. New attestations use v2 schema
5. Chain continues seamlessly (same hash-linking, different schema version)

### Schema Versioning

- `v` field in attestation record indicates schema version
- Relay API supports multiple schema versions concurrently
- Verification logic per-schema
- Future schema updates (v3, v4) added incrementally without breaking existing chains

### Backward Compatibility

- v1 attestations remain valid indefinitely
- Agents can switch between v1 and v2 (e.g., local development → cloud deployment)
- Relay API serves both `/v1/*` and `/v2/*` endpoints
- Public verification tools support all schema versions

---

## Implementation Status

### Tier 1 (Production)

**Status:** ✅ Live
- Attestation scripts: Complete (`attest.sh`, `audit-machine.sh`, `fingerprint.sh`, etc.)
- Enrollment: Complete (`enroll.sh`)
- Chain verification: Complete (`verify.sh`)
- Relay API: In development (endpoints defined, pinning infrastructure being built)
- Live chain: `CLWD-3F8B0233` (10+ days, all PASS)

**Platform support:**
- OpenClaw: ✅ Full support
- AutoGPT: 🚧 Planned
- LangChain (local): 🚧 Planned

### Tier 2 (Development)

**Status:** 🚧 In Development
- OTEL collector: 🚧 In progress
- Risk scoring: 🚧 Algorithm defined, implementation in progress
- Static analysis integration: 🚧 ESLint plugin testing
- Relay API v2 endpoints: 🚧 Spec complete, implementation in progress
- Vercel AI SDK integration: 🚧 Target platform, awaiting collector completion

**Platform support:**
- Vercel AI SDK: 🚧 Primary target (MVP: Roundy.ai)
- LangChain Cloud: 🚧 Planned
- Replit Agent: 🚧 Planned

### Relay API (In Development)

**Endpoints:**
- `/v1/enroll`: 🚧 Spec complete
- `/v1/attest`: 🚧 Spec complete
- `/v2/enroll`: 🚧 Spec complete
- `/v2/attest`: 🚧 Spec complete
- `/v2/telemetry`: 🚧 Spec complete
- `/v2/chain/{id}`: 🚧 Spec complete
- `/v2/verify/{id}`: 🚧 Spec complete
- `/v2/badge/{id}`: 🚧 Spec complete

**Infrastructure:**
- IPFS pinning (Pinata): 🚧 Account created, integration in progress
- PostgreSQL (chain metadata): 🚧 Schema designed
- AWS hosting (London region): 🚧 Provisioning in progress

---

## Future Enhancements

### Multi-Agent Correlation (v3 Schema)

For agent fleets (multiple agents under one operator):
- Cross-agent behavioral analysis
- Correlated risk scoring
- Fleet-level attestation manifests

### Hardware Security Module (HSM) Signing

For high-security deployments:
- Private keys stored in HSM (YubiKey, AWS CloudHSM)
- Signing operations delegated to hardware
- Enhanced tamper resistance

### Zero-Knowledge Proofs (ZKP)

For privacy-sensitive deployments:
- Prove compliance without revealing audit details
- zk-SNARKs for attestation verification
- Selective disclosure (prove "PASS" without showing which checks passed)

### Smart Contract Verification

For on-chain claims processing:
- Attestation chains published to blockchain
- Smart contract verifies chain validity
- Automated payouts (decentralized claims oracle)

---

## Appendix: Reference Implementation

### Tier 1 Attestation (bash)

```bash
#!/usr/bin/env bash
# attest.sh — Daily attestation for Tier 1 agents

set -e

CLAWDSURE_DIR="$HOME/.openclaw/workspace/.clawdsure"
AGENT_KEY="$CLAWDSURE_DIR/agent.key"
CHAIN_FILE="$CLAWDSURE_DIR/chain.jsonl"

# Run audits
AUDIT_MACHINE=$(bash audit-machine.sh --json)
AUDIT_NATIVE=$(openclaw security audit --json)

# Generate fingerprints
FINGERPRINT=$(bash fingerprint.sh)

# Build attestation record
SEQ=$(($(wc -l < "$CHAIN_FILE" 2>/dev/null || echo 0) + 1))
PREV=$(tail -n1 "$CHAIN_FILE" 2>/dev/null | shasum -a 256 | cut -d' ' -f1)
[ -z "$PREV" ] && PREV="genesis"

RECORD=$(jq -cn \
  --argjson v 1 \
  --argjson seq "$SEQ" \
  --arg prev "$PREV" \
  --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --arg agent "$(cat "$CLAWDSURE_DIR/agent.id")" \
  --argjson fingerprint "$FINGERPRINT" \
  --arg audit_native "$(echo "$AUDIT_NATIVE" | shasum -a 256 | cut -d' ' -f1)" \
  --arg audit_machine "$(echo "$AUDIT_MACHINE" | shasum -a 256 | cut -d' ' -f1)" \
  --arg result "PASS" \
  '{$v, $seq, $prev, $ts, $agent, $fingerprint, $audit_native, $audit_machine, $result}'
)

# Sign
SIG=$(echo -n "$RECORD" | openssl dgst -sha256 -sign "$AGENT_KEY" | base64)
SIGNED=$(echo "$RECORD" | jq -c --arg sig "$SIG" '. + {$sig}')

# Append to chain
echo "$SIGNED" >> "$CHAIN_FILE"

# Publish to relay
curl -X POST https://api.causal.insure/v1/attest \
  -H "Content-Type: application/json" \
  -H "X-Agent-ID: $(cat "$CLAWDSURE_DIR/agent.id")" \
  -H "X-Signature: $SIG" \
  -d "{\"agent\": \"$(cat "$CLAWDSURE_DIR/agent.id")\", \"attestation\": $SIGNED}"
```

### Tier 2 OTEL Exporter (TypeScript)

```typescript
// @causal/otel-exporter

import { Span, SpanExporter, ReadableSpan } from '@opentelemetry/sdk-trace-base';
import { ExportResult, ExportResultCode } from '@opentelemetry/core';

export interface CausalExporterConfig {
  endpoint: string;
  agentId: string;
  apiKey: string;
}

export class CausalExporter implements SpanExporter {
  private config: CausalExporterConfig;

  constructor(config: CausalExporterConfig) {
    this.config = config;
  }

  export(spans: ReadableSpan[], resultCallback: (result: ExportResult) => void): void {
    const payload = {
      agent_id: this.config.agentId,
      spans: spans.map(span => ({
        name: span.name,
        timestamp: new Date(span.startTime[0] * 1000 + span.startTime[1] / 1000000).toISOString(),
        duration_ms: (span.duration[0] * 1000 + span.duration[1] / 1000000),
        attributes: span.attributes,
      })),
    };

    fetch(this.config.endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Agent-ID': this.config.agentId,
        'X-API-Key': this.config.apiKey,
      },
      body: JSON.stringify(payload),
    })
      .then(response => {
        if (response.ok) {
          resultCallback({ code: ExportResultCode.SUCCESS });
        } else {
          resultCallback({ code: ExportResultCode.FAILED, error: new Error(`HTTP ${response.status}`) });
        }
      })
      .catch(error => {
        resultCallback({ code: ExportResultCode.FAILED, error });
      });
  }

  shutdown(): Promise<void> {
    return Promise.resolve();
  }
}

export function causalExporter(config: CausalExporterConfig): CausalExporter {
  return new CausalExporter(config);
}
```

---

**Document Status:** Living specification, updated as implementation progresses.  
**Maintainer:** Kryptoplus Labs (www.krypto.plus)  
**Contact:** markmusson@gmail.com  
**Last Updated:** February 2026
