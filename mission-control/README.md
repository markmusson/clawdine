# Mission Control 🐾

OpenClaw Mission Control Dashboard - A local dashboard for monitoring your OpenClaw agent.

## Features

### 1. 📊 Activity Feed
- Real-time view of OpenClaw gateway logs
- Filters by log level (info, warn, error)
- Auto-refreshes every 30 seconds
- Shows timestamp, subsystem, and message

### 2. 📅 Calendar View
- Weekly view of scheduled tasks
- Displays cron jobs from OpenClaw config
- Shows heartbeat schedule
- Next run time for each job

### 3. 🔍 Global Search
- Full-text search through workspace files
- Indexes markdown files, memories, and documents
- Highlighted search results
- Shows file path and matching context

## Quick Start

```bash
# Navigate to project
cd mission-control

# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Tech Stack

- **Next.js 14+** - React framework with App Router
- **Tailwind CSS** - Utility-first styling
- **TypeScript** - Type safety

## API Routes

| Route | Description |
|-------|-------------|
| `/api/logs` | Fetches parsed OpenClaw gateway logs |
| `/api/cron` | Returns cron jobs and heartbeat schedule |
| `/api/search?q=query` | Searches workspace files |

## Configuration

The dashboard reads from these locations:

- **Logs**: `/tmp/openclaw/openclaw-*.log`
- **Config**: `~/.openclaw/openclaw.json`
- **Cron Jobs**: `~/.openclaw/cron/jobs.json`
- **Workspace**: `~/.openclaw/workspace/`

## Adding Convex (Optional)

For real-time sync across devices, you can add Convex:

```bash
# Install Convex
npm install convex

# Initialize Convex
npx convex dev
```

Then create your schema in `convex/schema.ts`. This is optional - the dashboard works fully with local file access.

## Development

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## Features

The dashboard includes:
- 🌙 Dark mode by default
- 📱 Responsive layout
- 🔄 Auto-refreshing data
- 🎨 Clean, minimal UI
- 💚 Live status indicators

## Data Sources

| Feature | Source |
|---------|--------|
| Activity Feed | `/tmp/openclaw/openclaw-*.log` |
| Calendar | `~/.openclaw/cron/jobs.json` + config heartbeat |
| Search | `~/.openclaw/workspace/**/*.md` |

## Notes

- Runs locally on macOS
- Requires OpenClaw gateway to be running for logs
- Read-only - doesn't write back to OpenClaw
- Polling-based updates (30s for logs, 60s for cron)

---

Built for OpenClaw 🐾
