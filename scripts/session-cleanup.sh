#!/usr/bin/env bash
# session-cleanup.sh
# Prunes old .jsonl session files from ~/.openclaw/agents/*/sessions/
# Keeps: files modified within KEEP_DAYS, always keeps 5 most recent per agent.
# Active sessions (modified last 2h) are never touched.
# Moves to Trash instead of hard delete.

KEEP_DAYS="${SESSION_KEEP_DAYS:-3}"
SESSIONS_BASE="$HOME/.openclaw/agents"
LOG_DIR="$HOME/.openclaw/workspace/logs"
LOG_FILE="$LOG_DIR/session-cleanup.log"
TRASH_DIR="$HOME/.Trash"

mkdir -p "$LOG_DIR"

TS=$(date '+%Y-%m-%d %H:%M:%S')
echo "[$TS] session-cleanup starting (keep=${KEEP_DAYS}d)" >> "$LOG_FILE"

TOTAL_BEFORE=$(find "$SESSIONS_BASE" -name "*.jsonl" 2>/dev/null | wc -l | tr -d ' ')
SIZE_BEFORE=$(du -sh "$SESSIONS_BASE" 2>/dev/null | cut -f1)

DELETED=0
KEPT=0

for AGENT_DIR in "$SESSIONS_BASE"/*/sessions; do
  [[ -d "$AGENT_DIR" ]] || continue

  # Get files sorted newest first
  FILES=()
  while IFS= read -r -d '' f; do
    FILES+=("$f")
  done < <(find "$AGENT_DIR" -name "*.jsonl" -print0 | xargs -0 ls -t 2>/dev/null | tr '\n' '\0' 2>/dev/null || true)

  TOTAL_IN_DIR=${#FILES[@]}
  IDX=0

  for FILE in "${FILES[@]}"; do
    # Always keep the 5 most recent (index 0-4 in newest-first order)
    if [[ $IDX -lt 5 ]]; then
      KEPT=$((KEPT + 1))
      IDX=$((IDX + 1))
      continue
    fi

    # Skip if modified in last 2 hours (active session guard)
    MTIME=$(stat -f "%m" "$FILE" 2>/dev/null || echo 0)
    NOW=$(date +%s)
    AGE_SECS=$((NOW - MTIME))
    if [[ $AGE_SECS -lt 7200 ]]; then
      KEPT=$((KEPT + 1))
      IDX=$((IDX + 1))
      continue
    fi

    # Keep if modified within KEEP_DAYS
    AGE_DAYS=$((AGE_SECS / 86400))
    if [[ $AGE_DAYS -lt $KEEP_DAYS ]]; then
      KEPT=$((KEPT + 1))
      IDX=$((IDX + 1))
      continue
    fi

    # Move to Trash
    BASENAME=$(basename "$FILE")
    mv "$FILE" "$TRASH_DIR/$BASENAME" 2>/dev/null && DELETED=$((DELETED + 1)) || true
    IDX=$((IDX + 1))
  done
done

TOTAL_AFTER=$(find "$SESSIONS_BASE" -name "*.jsonl" 2>/dev/null | wc -l | tr -d ' ')
SIZE_AFTER=$(du -sh "$SESSIONS_BASE" 2>/dev/null | cut -f1)

echo "[$TS] done — deleted=$DELETED kept=$KEPT before=${TOTAL_BEFORE}files/${SIZE_BEFORE} after=${TOTAL_AFTER}files/${SIZE_AFTER}" >> "$LOG_FILE"
echo "session-cleanup: -${DELETED} files (${SIZE_BEFORE} → ${SIZE_AFTER})"
