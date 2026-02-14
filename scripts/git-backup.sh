#!/bin/bash
# Auto git backup — runs hourly via launchd
set -euo pipefail

cd /Users/clawdine/.openclaw/workspace

# Skip if no changes
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
  exit 0
fi

git add -A
git commit -m "auto-backup: $(date -u +%Y-%m-%dT%H:%M:%SZ)" --no-verify
git push origin main --quiet
