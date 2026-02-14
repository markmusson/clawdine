# ClawdSure — Project Status

*Last updated: Feb 11, 2026*

## ⚠️ STEALTH MODE

Do not discuss details publicly. Hint and tease only. See `MEMORY.md` for full stealth rules.

## What It Is

Security audit + parametric insurance for OpenClaw agents, under one product name.
Location: `skills/clawdsure/`

## The River Gauge Model

**Core problem:** Self-attestation from a compromised system is worthless.

**Accepted design:**
1. Baseline at policy inception (hash everything)
2. Periodic chain-linked measurements (hash of current + previous)
3. POST to ClawdSure API (external anchor)
4. Four triggers: chain gap, chain break, chain freeze, unexpected delta

**Implementation:** One bash script, `shasum` + `curl`, zero deps.

**Insurance model correction:** It's NOT parametric. Must PROVE hardened state via unbroken attestation chain. Chain broken = policy void. Like motor telematics black box.

## TrustGraph

- Hosted on Northflank
- Threat intel knowledge graph
- 197 skills seeded
- Scope: threat intel ONLY

## Validation

The ClawHub supply chain attack (Feb 5, 2026) validates the entire thesis — top downloaded skill was a malware delivery vehicle.
