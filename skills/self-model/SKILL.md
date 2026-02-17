---
name: self-model
version: 1.0.0
description: "Agent capability memory. Tracks what I can do, stops rediscovery loops."
author: clawdine
metadata:
  openclaw:
    emoji: "🧠"
    kind: "memory"
---

# Self-Model — Capability Memory

Read `{baseDir}/references/capabilities.md` at session start or when uncertain about available tools.

## Problem Solved

Agent forgets capabilities between sessions:
- "Can I send email?" → rediscovers clawmail.py every time
- "Is gog authenticated?" → tries, fails, wastes tokens
- Tools exist but aren't in prompt → agent doesn't know to use them

## How It Works

| File | Purpose | Size Target |
|------|---------|-------------|
| `capabilities.md` | Active capabilities (LOADED) | <800 bytes |
| `capability.log` | Discovery/failure history | Unlimited |

Only `capabilities.md` hits context. Log is audit trail.

## Capability Format

```markdown
# Capabilities

## Communication
- email: clawmail.py → clawdine@agentmail.to ✓
- telegram: message tool ✓
- gmail/gog: NOT CONFIGURED ✗

## Data
- qmd: semantic search ✓
- clawvault: memory primitives ✓

## External
- gh: GitHub CLI ✓
- web_search: Brave API ✓
```

## Update Protocol

When discovering a capability works or fails:

1. Update `capabilities.md` status (✓/✗)
2. Append to `capability.log`:
```
[YYYY-MM-DD] DISCOVERED: tool | STATUS: works/broken | NOTES: details
```

## Scan Command

To refresh capabilities, run:
```bash
# Check scripts
ls -1 scripts/*.py scripts/*.sh 2>/dev/null

# Check API keys
ls -1 .credentials/ 2>/dev/null

# Check installed skills
ls -1 skills/*/SKILL.md 2>/dev/null
```

Then update `capabilities.md` with findings.

## Pruning

Remove capabilities not used in 30 days. If `capabilities.md` exceeds 800 bytes, consolidate or remove stale entries.
