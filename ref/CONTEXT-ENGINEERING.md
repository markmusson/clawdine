# Context Engineering Reference

*Source: Manus blog (manus.im/blog/Context-Engineering-for-AI-Agents) + our own observations*
*Created: 2026-02-12*

---

## KV-Cache Rules

1. **Prefix must be byte-identical.** One token difference invalidates cache from that point forward.
2. **Timestamps in system prompt kill cache.** Don't put second-precision timestamps at the top. Check if OpenClaw does this — could explain 66% cache-write costs.
3. **Context must be append-only.** Don't modify previous messages/tool results. Deterministic JSON serialization matters.
4. **Anthropic cache TTL: 5 minutes.** Our heartbeat at 55min keeps the *prompt* cache warm, but mid-conversation gaps >5min between messages mean full cache-write on next turn.
5. **Cache breakpoints** should at minimum cover the end of the system prompt.

## Tool Management

- **Don't add/remove tools mid-conversation.** Tool definitions sit near the front of context — changing them invalidates cache for everything after.
- **Mask, don't remove.** Use constrained decoding / logit masking to restrict available actions without changing the tool list.
- Relevant: our groups-lite agent has different tools than main. That's fine (different sessions). But don't dynamically swap within a session.

## Context as File System

- File system = unlimited, persistent, agent-operable memory.
- **Compression should be restorable.** Drop content but keep the path/URL so the agent can re-fetch if needed.
- Check: does our cache-TTL pruning leave breadcrumbs (file paths, URLs) or strip everything?

## Attention Manipulation via Recitation

- Manus writes/updates `todo.md` every few steps to keep goals in recent attention window.
- Fights "lost in the middle" — model pays most attention to start and end of context.
- **Action for us:** On multi-step tasks, periodically re-state the goal near the end of context. COMMITMENTS.md is read on boot but not recited during long work sessions.

## Keep Errors In Context

- Don't erase failed tool calls or errors from the conversation.
- The model learns from seeing its own mistakes in-context — removing them removes evidence.
- We already do this (accidental best practice).

## Cost Implications

- Manus input:output ratio is 100:1. Ours is similar (agent work = lots of reading, short actions).
- Anthropic cached tokens: $0.30/MTok vs uncached $3/MTok (10x difference).
- Cache hit rate is THE cost metric for production agents.

---

## Audit Results (2026-02-12)

- [x] **Timestamp check: CLEAR.** OpenClaw only injects timezone string (`Europe/London`), not a per-second timestamp. System prompt prefix is stable. No cache invalidation.
- [x] **Pruning audit: PARTIAL.** Soft-trim keeps head 1500 + tail 1500 chars (URLs/paths likely survive). Hard-clear replaces with placeholder (no breadcrumbs). Hard-clear only fires on tool results older than 3 assistant messages AND after 55min idle. Acceptable given heartbeat keeps cache warm.
- [x] **Recitation pattern: ADOPTED.** Added to AGENTS.md — re-read goals every 5-8 actions on multi-step tasks.
- [ ] Optional: increase `softTrim.headChars` to better preserve URLs/paths in trimmed results
