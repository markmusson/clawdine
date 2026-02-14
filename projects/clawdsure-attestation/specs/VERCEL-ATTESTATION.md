# Causal Attestation for Vercel AI SDK Agents

**Status:** Draft spec
**Date:** 2026-02-13
**Author:** Clawdine
**MVP Target:** Roundy (roundy.ai)

---

## Problem

ClawdSure currently only attests OpenClaw agents running on local machines (macOS/Linux). The attestation model — daily script, local chain file, machine audit — doesn't translate to cloud-hosted agents built on the Vercel AI SDK.

Vercel AI SDK agents are the enterprise market. They run in serverless functions, use hundreds of models via AI Gateway, and have zero attestation or insurance coverage. The OWASP Agentic Top 10 2026 exists but nobody's enforcing it continuously.

## Opportunity

The Vercel AI SDK has **built-in OpenTelemetry instrumentation**. Every `generateText`, `streamText`, and `tool()` call emits traces. This is the data pipe Causal needs — no custom scripts, no local audits, just standard OTEL collection.

## Architecture

```
Vercel AI SDK Agent (e.g. Roundy)
    │
    ├── OpenTelemetry traces (built-in)
    │       ├── model invocations (provider, model, tokens, latency)
    │       ├── tool executions (name, params, result, duration)
    │       ├── agent steps (count, branching, errors)
    │       └── custom spans (business logic)
    │
    ▼
Causal OTEL Collector
    │
    ├── Behavioral analysis (real-time)
    │       ├── Tool safety scoring
    │       ├── Step count anomaly detection
    │       ├── Error rate monitoring
    │       ├── Data access pattern analysis
    │       └── OWASP Agentic compliance checks
    │
    ├── Attestation generation (periodic)
    │       ├── Risk score computation
    │       ├── Chain append (same schema, extended)
    │       └── Certificate issuance
    │
    ▼
Causal Relay API (existing, extended)
    │
    ├── Public verification endpoint
    ├── Daily merkle manifests
    └── Insurance underwriting feed
```

## Attestation Schema v2 (extended for Vercel)

The existing v1 schema works for OpenClaw. V2 adds fields for cloud/serverless agents:

```json
{
  "v": 2,
  "seq": 42,
  "prev": "sha256-hash-of-previous",
  "ts": "2026-03-15T09:00:00Z",
  "agent": "CASL-A1B2C3D4",
  "platform": "vercel-ai-sdk",
  "fingerprint": {
    "app": "sha256-of-package-lock+config",
    "deployment": "vercel-deployment-id",
    "sdk_version": "6.2.1",
    "gateway_config": "sha256-of-provider-config"
  },
  "audit": {
    "static": {
      "hash": "sha256-of-eslint-output",
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
      "destructive_actions": 0,
      "human_confirmations": 12,
      "max_steps_hit": 0,
      "anomalies_detected": 0,
      "data_access_violations": 0
    }
  },
  "risk_score": 12,
  "result": "PASS",
  "sig": "base64-ecdsa-signature"
}
```

### Key differences from v1:
- `platform` field — identifies agent framework
- `fingerprint.app` replaces `fingerprint.machine` — hash of deployment, not hardware
- `fingerprint.deployment` — Vercel deployment ID (immutable, traceable)
- `audit.static` — code-level checks (ESLint OWASP rules)
- `audit.runtime` — behavioral data from OTEL telemetry
- `risk_score` — computed 0-100 (lower = safer), used for underwriting

### Agent ID Format (Vercel)
```
CASL-XXXXXXXX
     ^^^^^^^^
     First 8 chars of app signing key fingerprint
```

CASL prefix distinguishes from CLWD (OpenClaw) agents.

## Integration Points

### 1. OTEL Collector Endpoint

Vercel AI SDK agents add Causal as an OTEL exporter:

```typescript
// instrumentation.ts (Next.js)
import { registerOTel } from '@vercel/otel';

registerOTel({
  serviceName: 'roundy',
  exporters: [
    // Default Vercel observability
    vercelExporter(),
    // Causal attestation collector
    causalExporter({
      endpoint: 'https://otel.causal.insure/v1/traces',
      agentId: 'CASL-A1B2C3D4',
      apiKey: process.env.CAUSAL_API_KEY,
    }),
  ],
});
```

**Effort:** ~10 lines of config. No code changes to the agent itself.

### 2. Static Analysis (CI/CD)

ESLint plugin runs in the build pipeline:

```yaml
# vercel.json or GitHub Actions
{
  "buildCommand": "npx eslint-plugin-vercel-ai-security src/ --format json > .causal/static-audit.json && next build"
}
```

Causal receives the static audit hash at deploy time.

### 3. Relay API Extensions

New endpoints for Vercel agents:

#### POST /v2/enroll
Same as v1 but accepts `platform: "vercel-ai-sdk"` and app fingerprint instead of machine fingerprint.

#### POST /v2/telemetry
Bulk OTEL span ingestion (alternative to OTEL exporter for simpler setups):

```json
{
  "agent_id": "CASL-A1B2C3D4",
  "spans": [...],
  "period": { "from": "...", "to": "..." }
}
```

#### GET /v2/agent/{agent_id}/badge
Returns SVG/PNG badge for display:
- "Causal Attested — PASS" (green)
- "Causal Attested — WARN" (yellow)  
- "Causal Attested — LAPSED" (grey)

Embeddable in README, landing page, Vercel marketplace listing.

### 4. Vercel Marketplace Integration (future)

Causal as a Vercel integration:
1. One-click install from Vercel marketplace
2. Auto-configures OTEL exporter
3. Adds static analysis to build pipeline
4. Dashboard in Vercel project settings
5. Badge on deployment

## Risk Scoring Model

The `risk_score` (0-100) is computed from:

| Factor | Weight | Scoring |
|--------|--------|---------|
| OWASP static compliance | 25% | Each failing check adds 3 points |
| Tool safety (destructive ops without confirmation) | 20% | Per-tool, based on parameter validation + human-in-loop |
| Error rate | 15% | Errors/total invocations, normalized |
| Step count anomalies | 10% | Agents hitting maxSteps or running unusually long |
| Data access patterns | 15% | Unusual access to PII, credentials, external APIs |
| Model diversity risk | 5% | Using unvetted/unknown models via gateway |
| Attestation chain health | 10% | Gap days, consecutive fails, chain length |

**Underwriting thresholds:**
- 0-20: Low risk → standard premium
- 21-50: Medium risk → elevated premium
- 51-75: High risk → restricted coverage
- 76-100: Critical → no coverage until remediated

## MVP: Roundy as First Attested Vercel Agent

### Why Roundy
- Already on Vercel AI SDK + AI Gateway
- Has Vercel instrumentation (OTEL)
- Handles sensitive data (investor conversations, financial models, personal info)
- Mark controls both Roundy and Causal — can iterate fast
- Real product with real users — not a demo

### MVP Scope
1. **Add OTEL exporter to Roundy** → sends traces to Causal endpoint
2. **Run eslint-plugin-vercel-ai-security** on Roundy codebase → static audit
3. **Build minimal Causal collector** → receives OTEL, computes risk score, generates v2 attestation
4. **Extend relay API** → accept v2 attestations, serve badge endpoint
5. **Display badge on roundy.ai** → "Causal Attested"

### Not in MVP
- Vercel marketplace integration
- Automated insurance policy binding
- Multi-agent telemetry correlation
- Anomaly detection ML (rule-based first)

### Build Order
1. Define v2 schema (this spec) ✅
2. Build OTEL collector endpoint (Causal side)
3. Add OTEL exporter to Roundy (Roundy side)
4. Build risk score computation (Causal side)
5. Extend relay API for v2 (Causal side)
6. Run static analysis on Roundy (CI/CD)
7. Generate first v2 attestation
8. Badge endpoint + display on roundy.ai

## What This Unlocks

1. **Platform-agnostic attestation** — not "OpenClaw insurance" but "agent insurance"
2. **Enterprise distribution** — Vercel marketplace, not ClawHub
3. **Standard protocol** — OTEL is universal, works with any framework that emits traces
4. **Roundy as case study** — "We insure our own product" is the strongest possible pitch
5. **Sam Clifton meeting** — "Here's a live attested agent handling investor conversations. Here's the risk score. Here's what insurance on this looks like."

---

*This spec extends, not replaces, the existing v1 OpenClaw attestation. Both run in parallel. The relay API serves both CLWD and CASL agents.*
