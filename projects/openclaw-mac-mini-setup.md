# OpenClaw on Mac Mini: Complete Setup Guide

*Source: Robert Heubanks ([Substack](https://robertheubanks.substack.com/p/openclaw-on-mac-mini-the-complete))*
*Reformatted with checklists for offline use.*

**End result:** Personal AI assistant running 24/7 on a dedicated Mac Mini — Telegram, Discord, WhatsApp, browser dashboard. Web browsing, shell access, file management, extensible with skills.

**Time:** 2–3 hours including security hardening.

---

## Phase 0: Pre-Setup (Do This on Your Phone)

Everything here happens BEFORE touching the Mac Mini.

### Password Manager

- [ ] Install Bitwarden (free) or 1Password (~$3/mo)
- [ ] Create account with strong master password
- [ ] Every credential from this guide goes here. No exceptions.

### Apple ID (prepare, don't create yet)

- [ ] Dedicated Gmail address for this machine (e.g. `your-infra-email@gmail.com`)
- [ ] Strong unique password (different from Gmail password) → save in password manager
- [ ] 2FA phone number — your most stable, long-term number
- [ ] Your real name

> You'll create the Apple ID during Mac Mini Setup Assistant (Phase 1). Creating via web often fails if your number is tied to another Apple ID.

### Infrastructure Gmail

- [ ] Verify login at https://accounts.google.com
- [ ] Update password if needed → save in password manager
- [ ] Enable 2FA: https://myaccount.google.com/security
- [ ] Remove stale recovery emails/phone numbers

> This Gmail is for plumbing only (OAuth, recovery, system ops). Nobody sees it. Outbound email comes later (Phase 10).

### API Keys & Tokens

- [ ] **Anthropic API key** — https://console.anthropic.com (recommended)
- [ ] **OpenAI API key** (optional) — https://platform.openai.com
- [ ] **Brave Search API key** — https://brave.com/search/api/
- [ ] **Set spending limits** on Anthropic and OpenAI billing pages
- [ ] Save every key in password manager immediately

### Telegram Bot

1. [ ] Open Telegram → search `@BotFather` (blue checkmark)
2. [ ] `/start` → `/newbot`
3. [ ] Set display name
4. [ ] Set username (must end in `bot`, must be unique)
5. [ ] **Copy bot token immediately** → save in password manager
6. [ ] Optional: `/setdescription` and `/setuserpic`

### Discord Bot

1. [ ] Go to https://discord.com/developers/applications
2. [ ] "New Application" → name it → "Create"
3. [ ] Left sidebar → "Bot"
4. [ ] "Reset Token" or "Copy" → **save token in password manager**
5. [ ] Scroll to "Privileged Gateway Intents" → enable:
   - [ ] **Message Content Intent** (required)
   - [ ] **Server Members Intent** (recommended)
6. [ ] Save Changes

### Pre-Flight Checklist

- [ ] Password manager ready
- [ ] Apple ID details prepared
- [ ] Infrastructure Gmail accessible with 2FA
- [ ] Anthropic API key
- [ ] OpenAI API key (optional)
- [ ] Brave Search API key
- [ ] Telegram bot token
- [ ] Discord bot token
- [ ] Spending limits set

---

## Phase 1: Mac Mini Setup

### Wipe & Setup Assistant

1. [ ] System Settings → General → Transfer or Reset → **Erase All Content and Settings**
2. [ ] Walk through Setup Assistant:
   - [ ] Connect to Wi-Fi
   - [ ] "Create a new Apple ID" → use infrastructure Gmail
   - [ ] Enter prepared password + 2FA phone
   - [ ] Create local user account (administrator for now)
   - [ ] **Enable FileVault disk encryption**
3. [ ] Decline/skip the following:
   - [ ] Location Services → **Decline**
   - [ ] Share analytics with Apple → **Decline**
   - [ ] Screen Time → **Skip**
   - [ ] Siri → **Skip**
   - [ ] Improve Siri & Dictation → **Decline**
   - [ ] Apple Intelligence → **Skip**
   - [ ] iCloud Keychain → **Skip**
   - [ ] Touch ID → **Enable** (local Secure Enclave, convenient)
   - [ ] Apple Pay → **Skip** (no payment methods on agent machines)

### Update macOS

- [ ] System Settings → General → Software Update → install all
- [ ] Restart if required

### Energy & Sleep

- [ ] System Settings → Energy:
  - [ ] "Prevent automatic sleeping when display is off" → **On**
  - [ ] "Wake for network access" → **On**
  - [ ] "Start up automatically after power failure" → **On**
- [ ] Optional: Install **Amphetamine** from App Store
  - [ ] Launch → Preferences → "Launch at login" → "Start session indefinitely"

---

## Phase 2: Developer Tools

### Xcode Command Line Tools

```bash
xcode-select --install
```
- [ ] Click "Install" on dialog, wait for completion

### Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
- [ ] Follow PATH instructions (Apple Silicon):
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```
- [ ] Verify: `brew --version`

### Node.js 22

```bash
brew install node@22
echo 'export PATH="/opt/homebrew/opt/node@22/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```
- [ ] Verify: `node --version` (v22.x.x+)
- [ ] Verify: `npm --version` (10.x.x+)

### pnpm (optional, for building from source)

```bash
npm install -g pnpm
```

---

## Phase 3: Install OpenClaw

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```
- [ ] Verify: `openclaw --version`

### Onboard

```bash
openclaw onboard --install-daemon
```

The wizard walks through:
- [ ] **Local vs Remote** → Local
- [ ] **Auth/LLM provider** → Anthropic API key
- [ ] **Chat channels** → Telegram token + Discord token
- [ ] **Pairing defaults** → secure DM handling
- [ ] **Skills setup** → Yes, npm as node manager
- [ ] **Daemon** → installs launchd service (24/7)
- [ ] **Gateway token** → auto-generated

> Model tip: Select **Opus 4.5** (or latest) when prompted.

### Web Search

```bash
openclaw configure --section web
```
- [ ] Select Local gateway
- [ ] Enable **web_search** (Brave) → enter API key
- [ ] Enable **web_fetch** (keyless HTTP)

### Heartbeat Optimization

Edit `~/.openclaw/openclaw.json` — add:
```json
"heartbeat": {
  "model": "claude-haiku-4-5-20251001",
  "interval": "1h"
}
```
- [ ] Saves ~$54/month (Opus heartbeat every 10min → Haiku hourly)

---

## Phase 4: Verify

```bash
openclaw gateway status
openclaw status
openclaw health
```
- [ ] All green

### Control UI

```bash
openclaw dashboard --no-open
```
- [ ] Copy tokenized URL → open in Safari → bookmark it

### Telegram Pairing

- [ ] Send `/start` to your bot
- [ ] Approve pairing:
```bash
openclaw pairing list telegram
openclaw pairing approve telegram <code>
```

### Telegram Topics (Recommended)

- [ ] Create private group (e.g. "AI HQ")
- [ ] Add bot as only other member
- [ ] Group Settings → enable Topics
- [ ] Make bot an administrator
- [ ] Create topics: `#general`, `#code-tasks`, `#research`, `#content`, `#automations`
- [ ] Tell bot: "Respond to every message in this group, not just @mentions"

### Discord Setup

1. [ ] Create server ("AI HQ")
2. [ ] Create channels: `#general`, `#code-tasks`, `#research`, `#automations`
3. [ ] Enable Developer Mode: User Settings → Advanced → Developer Mode
4. [ ] Copy and save: Server ID, User ID, Channel IDs
5. [ ] OAuth2 → URL Generator:
   - Scopes: `bot`, `applications.commands`
   - Permissions: Send Messages, Read History, Attach Files, Slash Commands, Reactions, Embeds
6. [ ] Copy invite URL → authorize for your server
7. [ ] Add Discord config to `~/.openclaw/openclaw.json` with guild/channel/user IDs
8. [ ] `openclaw gateway restart`
9. [ ] `openclaw channels status --probe`
10. [ ] Test: `@YourBot hello` in server channel

---

## Phase 5: Security Hardening

> This is the most important phase.

### Update OpenClaw

```bash
npm install -g openclaw@latest
openclaw --version  # Must be 2026.1.29+
openclaw gateway restart
openclaw channels status --probe
```
- [ ] Latest version confirmed

### Create Admin Account & Demote Daily Account

1. [ ] System Settings → Users & Groups → Add User
   - Type: **Administrator**
   - Name: Mac Admin / Account: `macadmin`
   - Strong password → save in password manager
2. [ ] Authorize for FileVault:
```bash
sudo fdesetup add -usertoadd macadmin
```
3. [ ] **Restart** (not log out — FileVault needs full restart)
4. [ ] Log in as **macadmin**
5. [ ] System Settings → Users & Groups → click (i) on original account
6. [ ] Uncheck "Allow this user to administer this computer"
7. [ ] Log out of macadmin → log back into standard account

- [ ] Daily account is now **standard** (not admin)

### Firewall

- [ ] System Settings → Network → Firewall → **On**
- [ ] Options:
  - [ ] "Block all incoming connections" → **On**
  - [ ] "Enable stealth mode" → **On**

### Tailscale (Remote Access)

- [ ] Install Tailscale on Mac Mini (App Store)
- [ ] Install Tailscale on MacBook/phone
- [ ] Enable SSH: System Settings → General → Sharing → Remote Login
- [ ] Test: `ssh yourusername@100.x.x.x`
- [ ] Port forward for Control UI:
```bash
ssh -L 18789:127.0.0.1:18789 yourusername@100.x.x.x
```

### Lock File Permissions

```bash
chmod 700 ~/.openclaw
chmod 600 ~/.openclaw/openclaw.json
chmod -R 600 ~/.openclaw/credentials/
chmod -R 600 ~/.openclaw/agents/*/agent/auth-profiles.json
```
- [ ] Permissions locked

### Verify Gateway Binding

```bash
openclaw gateway status
```
- [ ] Confirms `bind=loopback` (not `0.0.0.0`)

### SOUL.md Constraints

Add to `~/.openclaw/workspace/SOUL.md`:

```markdown
## What You Never Do
CRITICAL: Never execute commands with sudo or attempt privilege escalation.
CRITICAL: Never share API keys, tokens, or credentials in any message or output.
CRITICAL: Never install skills or extensions without explicit approval.
CRITICAL: Never send messages to anyone not explicitly approved.
CRITICAL: Never modify files outside ~/.openclaw/workspace/.
CRITICAL: Never make purchases or financial transactions.
CRITICAL: Never access untrusted sources without asking first.

## How You Work
For any multi-step task, complex operation, or anything that modifies files,
sends messages, or calls external services: ALWAYS present your plan first
and wait for approval before executing.
```
- [ ] Constraints added

### Run Audits

```bash
openclaw doctor
openclaw security audit --deep
```
- [ ] All issues resolved

### Skill Security

> ClawHub has NO curation. A researcher proved this by uploading a benign skill, inflating downloads, and watching blind installs globally.

Before installing ANY third-party skill:
```bash
cat /path/to/skill/SKILL.md
grep -r "api\|token\|credential\|curl\|fetch" /path/to/skill/
```
- [ ] Rule: **If you didn't write it and didn't read the code, don't install it.**

---

## Phase 6: Ongoing Operations

### Daily Self-Review (Cron)

Tell your bot:
> "Set up a daily cron job each morning. Review MEMORY.md, SOUL.md, identity.md, agents.md, and skills folder. Look for outdated info, conflicting rules, undocumented workflows, unused skills, and lessons from failures. Summarize findings. Do not make changes without approval."

- [ ] Cron job created

### Monthly Manual Review

- [ ] Calendar reminder: read `~/.openclaw/workspace/MEMORY.md` monthly
- [ ] Delete anything you wouldn't want an attacker to see
- [ ] Remove anything no longer accurate

### Credential Rotation (Quarterly)

- [ ] Anthropic API key
- [ ] OpenAI API key
- [ ] Discord bot token
- [ ] Telegram bot token
- [ ] Brave Search API key
- [ ] Any other connected tokens

### Config Backup

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak
```
- [ ] Before any update or config change

### Model Routing (Cost Optimization)

| Task | Recommended Model | Notes |
|------|------------------|-------|
| Brain (conversation) | Opus 4.6 | Main intelligence |
| Heartbeat | Haiku | Already done — saves ~$54/mo |
| Image understanding | Gemini 2.5 Flash | Free tier available |
| Web search/browse | DeepSeek v3 | Very cheap |
| Coding | Codex GPT 5.2 | Specialized |

Start with heartbeat + image + web search. Keep Opus as brain until comfortable.

---

## Emergency Procedures

### Kill Agent

```bash
openclaw gateway stop
# If that fails:
pkill -f openclaw
```

### Suspected Compromise (Do ALL, In Order)

1. [ ] Stop gateway
2. [ ] **Revoke ALL API keys** — Anthropic, OpenAI, Brave, everything. Revoke first, investigate later.
3. [ ] Rotate Discord token (Developer Portal → Bot → Reset Token)
4. [ ] Rotate Telegram token (@BotFather → `/revoke`)
5. [ ] Review logs:
```bash
cat /tmp/openclaw/openclaw-*.log
cat ~/.openclaw/agents/*/sessions/*.jsonl
```
6. [ ] Check for persistence:
```bash
crontab -l
cat ~/.ssh/authorized_keys
cat ~/.zprofile
cat ~/.zshrc
```
7. [ ] **DO NOT restart until you understand what happened**
8. [ ] When in doubt: wipe and rebuild (that's the beauty of a dedicated machine)

---

## Quick Reference

### Key Paths

| Path | Purpose |
|------|---------|
| `~/.openclaw/` | Main config directory |
| `~/.openclaw/openclaw.json` | Primary config |
| `~/.openclaw/workspace/` | Skills, prompts, memories |
| `~/.openclaw/credentials/` | OAuth and channel creds |
| `~/.openclaw/agents/` | Per-agent auth and data |

### Key Commands

| Command | Purpose |
|---------|---------|
| `openclaw status` | Quick status |
| `openclaw health` | Health check |
| `openclaw status --all` | Full debug report |
| `openclaw doctor` | Diagnose issues |
| `openclaw doctor --fix` | Auto-fix issues |
| `openclaw security audit --deep` | Security audit |
| `openclaw dashboard` | Open Control UI |
| `openclaw dashboard --no-open` | Print tokenized URL |
| `openclaw gateway status` | Gateway status |
| `openclaw gateway restart` | Restart gateway |
| `openclaw channels status --probe` | Channel connectivity |
| `openclaw channels login` | Connect channels |
| `openclaw pairing list <channel>` | Pending pairings |
| `openclaw pairing approve <ch> <code>` | Approve pairing |
| `openclaw configure --section web` | Configure web search |
| `openclaw update --channel stable` | Update OpenClaw |

---

## Phase 10: Outbound Email (When Ready)

- [ ] Set up a Gmail with your real name (e.g. `firstname.lastname@gmail.com`)
- [ ] Enable 2FA
- [ ] Install Gmail skill: ask bot "Set up Gmail integration"
- [ ] Authenticate with outbound email (NOT infrastructure Gmail)
- [ ] Test: "Send a test email to [personal email]"

> Future: Custom domain via Google Workspace (~$7/mo)

---

## Resources

- **Docs:** https://docs.openclaw.ai
- **Getting Started:** https://docs.openclaw.ai/start/getting-started
- **macOS Guide:** https://docs.openclaw.ai/platforms/macos
- **GitHub:** https://github.com/openclaw/openclaw
- **Discord:** Linked from GitHub
- **Cost Optimization:** Alex Finn's "How to Run OpenClaw for Dirt Cheap" (YouTube)

---

*Reformatted from Robert Heubanks' original guide. All credit to him.*
