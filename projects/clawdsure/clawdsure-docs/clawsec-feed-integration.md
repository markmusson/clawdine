# ClawSec CVE Feed Integration Spec

## Context

Prompt Security (prompt.security) has built ClawSec — an open-source security skill suite for OpenClaw agents. Their CVE advisory feed polls NIST NVD for agent-relevant vulnerabilities and serves them as JSON.

**Feed URL:** `https://clawsec.prompt.security/advisories/feed.json`
**GitHub:** `https://github.com/prompt-security/clawsec`

## What We Want From Them

Their advisory feed as a threat intel source for ClawdSure's attestation and underwriting model.

### CVE Feed → Attestation Chain

When a new CVE is published that affects OpenClaw or installed skills:
1. ClawdSure agent polls the feed (cron, every 6h)
2. Cross-references against policyholder's installed skills + config
3. If affected: flag in attestation chain as `advisory-match` event
4. Policyholder gets a window (e.g. 48h) to patch before it affects coverage status
5. Unpatched known vulnerabilities after the window = material risk change in underwriting

### CVE Feed → TrustGraph

Feed entries map directly to our TrustGraph Threat entity:
```
Threat {
  id: CVE-2026-XXXXX
  severity: critical|high|medium|low
  description: "..."
  affected_packages: [skill names / versions]
  source: "clawsec-nvd-feed"
  published: ISO timestamp
}
```

Edges:
- `Threat --AFFECTS--> Skill` (when a specific skill is named)
- `Threat --AFFECTS--> Package` (when a dependency is named)

### Advisory Schema (from ClawSec)

```jsonc
{
  "id": "CVE-2026-XXXXX",
  "severity": "critical|high|medium|low",
  "description": "...",
  "affected": ["openclaw", "skill-name"],
  "published": "ISO timestamp",
  "source": "NVD"
}
```

## Integration Points

### 1. Feed Poller (cron job, isolated, Haiku)
- Every 6 hours, fetch `feed.json`
- Diff against last known state (store last-seen CVE ID)
- New advisories → write to `clawdsure-docs/advisories/` as individual files
- Critical/High → notify via Telegram

### 2. Attestation Event
New event type for the attestation chain:
```jsonc
{
  "event": "advisory-received",
  "eventMeta": {
    "cveId": "CVE-2026-XXXXX",
    "severity": "critical",
    "affected": ["skill-name"],
    "policyholderExposed": true,
    "patchDeadline": "ISO timestamp (48h from now)"
  }
}
```

### 3. Underwriting Impact
- Known unpatched critical CVE after deadline → coverage may be voided (same as broken attestation chain)
- Patched within window → no impact, good behaviour recorded
- This creates incentive alignment: ClawdSure policyholders patch faster than non-policyholders

## Relationship with ClawSec

**Complementary, not competitive:**
- ClawSec = runtime protection (firewall, drift detection, audit)
- ClawdSure = evidence + insurance (attestation chain, proof of diligence, claims)
- ClawSec users are ideal ClawdSure customers — already security-conscious
- Their feed is our threat intel source
- Our insurance is their upsell: "you're protected AND insured"

## Next Steps

1. Set up feed poller cron job
2. Test feed schema against our TrustGraph ontology
3. When TrustGraph is on Northflank, ingest feed as Threat entities
4. Spec the `advisory-received` attestation event into the OpenClaw PR
