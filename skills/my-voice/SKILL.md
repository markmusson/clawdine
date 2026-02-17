---
name: my-voice
version: 1.0.0
description: "Self-improving writing voice. Learns from corrections, stays compact."
author: clawdine
metadata:
  openclaw:
    emoji: "🎤"
    kind: "memory"
---

# My Voice — Adaptive Writing Style

Read `{baseDir}/references/rules.md` before writing content that should match personal style.

## How It Works

Two files, one compact:

| File | Purpose | Size Target |
|------|---------|-------------|
| `rules.md` | Active rules (LOADED) | <500 bytes |
| `corrections.log` | Raw history (NOT loaded) | Unlimited |

Only `rules.md` hits the context window. Corrections log is append-only archive.

## Correction Protocol

When user flags something as wrong:

1. Acknowledge
2. Apply immediately
3. Append to `corrections.log`:
```
[YYYY-MM-DD] DON'T: "what I wrote" → DO: "what they wanted" | WHY: reason
```

## Compaction (Weekly or at 20+ corrections)

Review `corrections.log`, extract patterns, update `rules.md` with consolidated principles. Keep rules.md under 500 bytes — if it grows, generalize.

Example compaction:
- 5 corrections about "leverage" → one rule: "No corporate verbs"
- 3 corrections about throat-clearing → one rule: "Skip preamble"

## Rules Format

```markdown
# Voice Rules (compact)

## Don't
- Corporate verbs (leverage, optimize, utilize)
- Throat-clearing (It's important to note, Let me explain)
- Hedging when certain

## Do
- Direct statements
- Specific > vague
- Numbers > adjectives
```
