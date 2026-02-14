---
name: model-hierarchy
description: >
  Cost-optimize by routing tasks to appropriate models based on complexity.
  Use when: deciding which model for a task, spawning sub-agents, or when the current model is overkill.
---

# Model Hierarchy

Route to the cheapest model that can do the job. Most work is janitorial.

## Our Tiers

| Tier | Model | Cost (in/out per M) | Use For |
|------|-------|---------------------|---------|
| Cheap | Haiku 4.5 | $1 / $5 | Routine — file ops, status, formatting, cron, heartbeats |
| Mid | Sonnet 4.5 | $3 / $15 | Moderate — code gen, summaries, drafts, analysis, research |
| Premium | Opus 4.6 | $15 / $75 | Complex — debugging, architecture, security, novel problems |

## Classification

### ROUTINE → Haiku
- Single-step, clear instructions, no judgment needed
- File read/write, status checks, lookups, formatting, list ops
- API calls with known params, heartbeats, cron tasks, URL fetching

### MODERATE → Sonnet
- Multi-step but well-defined, some synthesis needed
- Code generation, summarization, draft writing, data analysis
- Multi-file operations, tool orchestration, search and research

### COMPLEX → Opus
- Novel problem solving, multiple valid approaches, nuanced judgment
- Multi-step debugging, architecture decisions, security review
- Tasks where a cheaper model already failed
- Long-context reasoning (>50K tokens), creative work, ambiguous requirements

## Rules

1. **Escalation:** If a task failed on a cheaper model, bump up one tier
2. **Sub-agents:** Default to Haiku unless clearly moderate+
3. **Automated tasks:** Heartbeats and monitoring are always Haiku. Scheduled reports are Haiku or Sonnet. Alerts start at Sonnet, escalate if needed.
4. **Main session:** Interactive chat stays on whatever model is set. Suggest spawning cheap sub-agents for routine subtasks.
5. **Batch similar tasks** to amortize overhead

## Anti-Patterns

- Running heartbeats on Opus
- Premium models for file I/O
- Spawning sub-agents on premium by default
- Staying on expensive model when the task is obviously routine

## Cost Impact (100K tokens/day)

| Strategy | Monthly |
|----------|---------|
| Pure Opus | ~$225 |
| Pure Sonnet | ~$45 |
| Hierarchy (80/15/5) | ~$19 |

Based on [zscole/model-hierarchy-skill](https://github.com/zscole/model-hierarchy-skill). MIT.
