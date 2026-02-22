#!/usr/bin/env bash
# post-update-check.sh
# Run after every `openclaw update` to catch pairing/health regressions.
# Usage: bash ~/.openclaw/workspace/scripts/post-update-check.sh

set -uo pipefail

ISSUES=()

echo "=== Post-Update Health Check ==="
echo ""

# 1. Gateway health
echo -n "Gateway health... "
HEALTH=$(openclaw health 2>&1)
if echo "$HEALTH" | grep -q "pairing required"; then
  echo "FAIL — pairing required"
  ISSUES+=("Gateway pairing lost — run: openclaw devices list && openclaw devices approve <id>")
elif echo "$HEALTH" | grep -q "connect failed"; then
  echo "FAIL — cannot connect"
  ISSUES+=("Gateway not responding")
else
  echo "OK"
fi

# 1b. Pending device repairs (missed by health check)
echo -n "Pending device repairs... "
PENDING=$(openclaw devices list 2>/dev/null | grep -c "repair" || true)
if [[ "$PENDING" -gt 0 ]]; then
  echo "WARN — $PENDING device(s) need re-approval"
  ISSUES+=("$PENDING device repair pending — run: openclaw devices list && openclaw devices approve <id> (sub-agent spawning will fail until resolved)")
  # Auto-approve if only one pending
  REPAIR_ID=$(openclaw devices list 2>/dev/null | grep "repair" | awk '{print $2}' | head -1)
  if [[ -n "$REPAIR_ID" ]]; then
    openclaw devices approve "$REPAIR_ID" 2>/dev/null && echo "  → auto-approved $REPAIR_ID" || true
  fi
else
  echo "OK"
fi

# 2. Duplicate gateway processes
echo -n "Duplicate gateway processes... "
GW_COUNT=$(ps aux | grep openclaw-gateway | grep -v grep | wc -l | tr -d ' ')
if [[ "$GW_COUNT" -gt 1 ]]; then
  echo "WARN — $GW_COUNT processes (expected 1)"
  ISSUES+=("$GW_COUNT gateway processes running — kill old: pkill -f openclaw-gateway && openclaw gateway start")
else
  echo "OK ($GW_COUNT process)"
fi

# 3. Telegram channel
echo -n "Telegram channel... "
if echo "$HEALTH" | grep -q "Telegram: ok"; then
  echo "OK"
else
  echo "WARN — not confirmed"
  ISSUES+=("Telegram channel not confirmed healthy")
fi

# 4. Cron jobs still loaded
echo -n "Cron jobs... "
CRON_COUNT=$(python3 -c "
import json, os
d = json.load(open(os.path.expanduser('~/.openclaw/cron/jobs.json')))
jobs = d.get('jobs', d) if isinstance(d, dict) else d
enabled = [j for j in jobs if j.get('enabled', True)]
print(len(enabled))
" 2>/dev/null || echo "?")
echo "$CRON_COUNT enabled"

# 5. Summary
echo ""
if [[ ${#ISSUES[@]} -eq 0 ]]; then
  echo "✅ All checks passed. Update looks clean."
else
  echo "⚠️  Issues found:"
  for i in "${ISSUES[@]}"; do echo "  - $i"; done
  echo ""
  echo "Fix issues before relying on scheduled crons."
fi
