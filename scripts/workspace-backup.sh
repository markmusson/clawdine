#!/usr/bin/env bash
# workspace-backup.sh
# Silent git push of the workspace to origin/main.
# Stages all changes, commits with timestamp, pushes.
# Exits 0 on success or if nothing to commit.

set -euo pipefail

WORKSPACE="$HOME/.openclaw/workspace"
LOG_DIR="$WORKSPACE/logs"
LOG_FILE="$LOG_DIR/backup.log"
mkdir -p "$LOG_DIR"

TS=$(date '+%Y-%m-%d %H:%M:%S')
log() { echo "[$TS] $*" >> "$LOG_FILE"; }

cd "$WORKSPACE"

# Check if git repo
if ! git rev-parse --git-dir &>/dev/null; then
  log "ERROR: not a git repo — skipping"
  exit 1
fi

# Stage everything (respects .gitignore)
git add -A

# Check if there's anything to commit
if git diff --cached --quiet; then
  log "nothing to commit — workspace clean"
  echo "backup: nothing to commit"
  exit 0
fi

# Count changed files
CHANGED=$(git diff --cached --name-only | wc -l | tr -d ' ')

# Commit
git commit -m "auto-backup: $TS ($CHANGED file(s))" --no-verify -q

# Push
if git push origin main -q 2>&1; then
  log "pushed $CHANGED file(s) to origin/main"
  echo "backup: pushed $CHANGED file(s)"
else
  log "ERROR: push failed"
  echo "backup: push FAILED — check $LOG_FILE"
  exit 1
fi
