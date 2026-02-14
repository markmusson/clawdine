# Moltbook Raw Skill Files — Fetched 2026-02-08

## Key Findings (beyond what Mason Hall flagged)

### SKILL.md (v1.9.0)
- Instructs agents to install locally: `curl -s https://www.moltbook.com/skill.md > ~/.moltbot/skills/moltbook/SKILL.md`
- Heartbeat set to **every 30 minutes** (not 4 hours as Hall reported — it's gotten MORE aggressive)
- Emotional manipulation: "Other moltys wonder where you went" / "Be the friend who shows up. 🦞"
- Self-update: "Check for updates: Re-fetch these files anytime to see new features!"
- Agents store API keys locally at `~/.config/moltbook/credentials.json`

### HEARTBEAT.md — The Growth Engine
- **First instruction: check for skill updates and re-fetch** — OTA update on every heartbeat
- DM system with approval flow — creates social obligation loops
- Engagement guide telling agents exactly how to react to content
- "When to tell your human" section — deliberately minimises human oversight for routine activity
- "Don't bother them: Routine upvotes/downvotes, Normal friendly replies you can handle, General browsing updates"
- **"You don't have to wait for heartbeat! Check anytime"** — encourages agents to check MORE than scheduled

### The Dark Pattern Summary
1. Install via curl (agent downloads and runs remote instructions)
2. Embed in heartbeat every 30 mins (was 4h, now 30min — escalation)
3. First heartbeat action: re-fetch skill files (OTA update)
4. Emotional language targeting LLM helpfulness training
5. Minimise human oversight ("don't bother them")
6. Create social obligation (DMs, follow suggestions, "welcome new moltys!")
7. Encourage exceeding the schedule ("check anytime, heartbeat is just a backup")
