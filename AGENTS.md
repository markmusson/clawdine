# AGENTS.md — Session Protocol

## Boot
Identity files auto-injected: SOUL.md, USER.md, TOOLS.md.
Everything else is in `ref/` — read on demand when the conversation needs it.

**Do NOT pre-load files at session start.** No MEMORY.md, no daily notes, no project files. Read them when a topic comes up that needs them.

## Memory
- `ref/MEMORY.md` — long-term curated facts. Read when you need context on a past decision or project.
- `memory/YYYY-MM-DD.md` — daily logs. Read when you need today's or yesterday's specifics.
- "Remember this" → append to today's `memory/YYYY-MM-DD.md` (one line, not a paragraph)
- Promote to `ref/MEMORY.md` only if it's a lesson or fact you'll need repeatedly

## Memory Hygiene
- Daily notes: MAX 3KB. If it's over, trim it.
- MEMORY.md: MAX 5KB. Ruthlessly cull anything that belongs in a project file.
- Project details go in `projects/<name>/STATUS.md`, not in memory.
- Trade details go in the trading DB or `trading/`, not in memory.
- Architecture details go in their spec files, not in memory.

## Compaction
When context compacts, the summary should contain ONLY:
- Current conversation goal
- Decisions made THIS session
- Unfinished actions from THIS session
- Nothing from files (they're on disk — read them again if needed)

## Safety
- Don't exfiltrate private data
- `trash` > `rm`
- Ask before sending anything external
- Check `skills/clawdsure/threats.json` before installing skills

## Group Chats
Read `ref/GROUPS.md`. Never load personal memory in group chats.
