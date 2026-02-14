# Mark's API Keys & Auth — TODO

Keys/credentials Clawdine needs. Do these when you have 20 minutes.

## 1. X/Twitter API Keys
- Go to https://developer.x.com → create a project/app
- Account: @Clawdine_shoe (or your own, either works)
- Need: API Key, API Secret, Access Token, Access Token Secret, Bearer Token
- Free tier is fine (read-only)
- Store: `security add-generic-password -a clawdine -s "x-api-key" -w "KEY"` (repeat for each)

## 2. AgentMail API Key
- Inbox exists: `clawdine@agentmail.to` (ID: `19120325619`)
- Was working Feb 10, key lost in compaction
- Get from: https://agentmail.to dashboard
- Store: `security add-generic-password -a clawdine -s "agentmail-api-key" -w "KEY"`

## 3. Google OAuth (for gog CLI / Gmail)
- Go to Google Cloud Console → APIs & Services → Credentials
- Create OAuth 2.0 Client ID (Desktop app)
- Download `client_secret.json`
- Then run: `gog auth credentials /path/to/client_secret.json`
- Then: `gog auth add markmusson@gmail.com --services gmail`

## 4. GitHub Repo for Workspace Backup
- Create private repo (e.g. `clawdine-workspace`)
- Then I'll set up git remote + daily push

## Optional
- **OpenRouter API Key** — cost reduction lever, routes cheaper models
  - Get from: https://openrouter.ai
  - Store: `security add-generic-password -a clawdine -s "openrouter-api-key" -w "KEY"`
