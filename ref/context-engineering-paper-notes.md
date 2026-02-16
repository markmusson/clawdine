# Context Engineering Paper Notes

**Paper:** "Everything is Context: Agentic File System Abstraction for Context Engineering"
**Authors:** Xiwei Xu, Robert Mao, Quan Bai, Xuewu Gu, Yechao Li, Liming Zhu (CSIRO Data61)
**arXiv:** 2512.05470 (December 2025)

## Core Thesis

Current agent architectures treat context as static injection at session start. This creates:
- Token waste (loading everything upfront)
- Context loss on compaction (summarization destroys retrievability)
- No discoverability (agent can't browse what it flushed)

Solution: treat all context as files in a unified namespace with explicit operations.

## Key Architecture Components

### 1. Unified Namespace (`/context/*`)
- `/context/history/` — immutable interaction logs (source of truth)
- `/context/memory/episodic/` — session-bounded summaries
- `/context/memory/fact/` — atomic durable entries (preferences, decisions)
- `/context/memory/user/` — personal attributes
- `/context/pad/` — task-scoped scratchpads (promotable or discardable)
- `/context/tools/` — tool metadata
- `/context/sessions/` — session artifacts

### 2. Operational Layer (between filesystem and token window)
- **Constructor:** Pre-turn context selection, token-budget-aware, produces manifest
- **Updater:** Incremental streaming during reasoning, replaces outdated pieces
- **Evaluator:** Post-response verification, writes back to filesystem, flags low confidence

### 3. Three-Tier Memory
- Scratchpad → Episodic → Fact
- Each tier has own retention policy and promotion path
- Replaces current binary (today's log vs forever file)

## Mapping to Mark's PR #17345

PR: "Runner memory rebuild: token budgeting, recall caps, incremental summary state"

| Paper Concept | PR Coverage | Gap |
|---------------|-------------|-----|
| Token budgeting | ✅ Phase 1 | — |
| Recall caps | ✅ Phase 2 | — |
| Incremental summary | ✅ Phase 3 | — |
| Unified namespace | ❌ | Not in PR scope |
| Constructor/manifest | ❌ | Not in PR scope |
| Demand-driven loading | ❌ | Not in PR scope |
| Three-tier promotion | ❌ | Not in PR scope |
| Evaluator/writeback | ❌ | Not in PR scope |

**Assessment:** PR #17345 addresses the *symptoms* (token management, summary state) but not the *architecture* (static injection → dynamic discovery). The paper argues you can't fully solve the problem without changing the delivery model.

## OpenClaw-Specific Pain Points (from daily ops)

1. **MEMORY.md conflation** — mixes atomic facts with episodic context. Paper's three-tier split directly addresses this.

2. **Compaction destroys retrievability** — after window resets, agent uses search and hopes. Paper's manifest + immutable history solves this.

3. **No debuggability** — "what did the agent load?" is unanswerable. Paper's constructor manifest provides audit trail.

4. **21k base cost per turn** — static injection of SOUL.md, AGENTS.md, workspace files. Paper's demand-driven model would reduce this.

5. **Daily logs vs MEMORY.md binary** — no middle ground. Paper's scratchpad → episodic → fact promotion path fills this gap.

## Potential RFC Structure

1. **Problem:** Static context injection + destructive compaction
2. **Prior Art:** CSIRO paper (cite), Cursor's dynamic context discovery
3. **Proposal:** Implement `/context/*` namespace with list/read/write/search ops
4. **Phases:**
   - Phase A: Expose context sources under predictable paths
   - Phase B: Enable list/read at runtime
   - Phase C: Shift boot injection to minimal preload + on-demand fetch
   - Phase D: Decompose MEMORY.md into fact/episodic stores
   - Phase E: Add promotion, archival, retention policies, audit logs
5. **Relation to PR #17345:** Builds on token budgeting foundation, extends to delivery model

## Key Quotes for GitHub Issue

> "Memory stops being a preload and becomes something the agent discovers, fetches, and evolves per turn."

> "Compaction stops being destructive. After the window resets, the agent can still list and read context files directly."

> "Context assembly becomes debuggable. The manifest records what the constructor selected for each turn."

---

*Saved pre-compaction: Feb 16, 2026*
