# GitHub Issue: openclaw/openclaw

**Title:** Anthropic context window hardcoded to 200k — should use per-model values

## Problem

`DEFAULT_CONTEXT_TOKENS` is hardcoded to `2e5` (200,000) in `src/agents/defaults.ts`. This is used as the fallback for all models when `lookupContextTokens()` returns nothing from `MODEL_CACHE`.

For Anthropic models served via direct API key (not Bedrock), the model discovery doesn't populate `MODEL_CACHE` with context window sizes, so everything falls through to 200k.

Claude Opus 4.6 shipped with a **1M token context window** (beta). The 200k default means:
- `/status` and `openclaw sessions` report wrong percentages
- Compaction/safeguard triggers fire too early
- Any tooling built on context % (alerts, dashboards) is off by 5x

## Current workaround

```json
{"agents": {"defaults": {"contextTokens": 1000000}}}
```

This works but is a blunt override — it applies the same window to all models. If you run Haiku (200k window) as a heartbeat model, it'll show wrong % for those sessions too.

## Suggested fix

Either:
1. **Static catalog for Anthropic models** — like `VENICE_MODEL_CATALOG` and `SYNTHETIC_MODEL_CATALOG` already do. Map known model IDs to their actual context windows.
2. **Per-model `contextWindow` in the models allowlist config** — let users specify it alongside `alias` and `params`:
   ```json
   {"anthropic/claude-opus-4-6": {"alias": "opus", "contextWindow": 1000000}}
   ```
3. **Query Anthropic's API** — the `/v1/models` endpoint may expose this (needs checking).

Option 2 is probably the quickest and most flexible.

## Environment

- OpenClaw 2026.2.6-3 (85ed6c7)
- Model: anthropic/claude-opus-4-6 via direct API key
- OS: macOS (arm64)
