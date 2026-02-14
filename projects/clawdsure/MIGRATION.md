# ClawdSure Migration — Feb 11 2026

## What Changed

The ClawdSure agent has been **decommissioned**. All ClawdSure work now runs under the main agent.

## Why

- ClawdSure agent ran Sonnet 4.5 for a low-volume group chat (2-3 msgs/day)
- All actual work (attestation, vuln scans) already ran via Haiku cron jobs under main
- Separate workspace meant fragmented memory — ClawdSure learnings stayed isolated
- Cost: ~$0.10-0.15/day for what's now $0.01/day on Haiku

## What Moved

From `/Users/clawdine/.openclaw/workspace-clawdsure/` to `/Users/clawdine/.openclaw/workspace/projects/clawdsure/`:

- `.clawdsure/` — attestation chains, audit scripts, vuln database
- `clawdsure-docs/` — design docs (machine-audit, attestation-chain, etc)
- `disclosures/` — security findings, disclosure reports
- `openclaw-security-audit-*.md` — audit reports (preliminary, final, vuln hunting)
- `memory-archive/` — old ClawdSure daily logs (archived, not active memory)

## What's Still Running

All cron jobs continue unchanged:
- `clawdsure-daily-attest` — 9:30am, Haiku, runs attest.sh
- `vuln-scan-daily` — 10:00am, Haiku, searches + updates vuln-db

## Group Binding

ClawdSure Telegram group (`-5233512601`) now routes to `groups-lite` (Haiku).

## Config Change

```json
// Removed from agents.list:
{
  "id": "clawdsure",
  "name": "ClawdSure",
  "workspace": "/Users/clawdine/.openclaw/workspace-clawdsure",
  "model": {
    "primary": "anthropic/claude-sonnet-4-5"
  }
}

// Binding updated:
{
  "agentId": "groups-lite",  // was: clawdsure
  "match": {
    "channel": "telegram",
    "peer": {
      "kind": "group",
      "id": "-5233512601"
    }
  }
}
```

## Cost Impact

- **Before:** Sonnet (~$3-5/M in, ~$15/M out) × ~20K tokens/day = ~$0.10-0.15/day
- **After:** Haiku (~$0.25/M in, ~$1.25/M out) × ~15K tokens/day = ~$0.01-0.02/day
- **Savings:** ~90% on ClawdSure group chat costs

Cron jobs were already Haiku, so no change there.

---

*Migration completed: 2026-02-11 18:40 GMT*
