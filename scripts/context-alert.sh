#!/bin/bash
# Context Budget Alert — runs via launchd, zero tokens
# Checks main session context usage, sends Telegram alert if ≥50%

set -uo pipefail

STATE_FILE="$HOME/.openclaw/workspace/memory/heartbeat-state.json"
TELEGRAM_BOT_TOKEN=$(python3 -c "
import json
with open('$HOME/.openclaw/openclaw.json') as f:
    c = json.load(f)
print(c['channels']['telegram']['botToken'])
")
MARK_CHAT_ID="7018377788"

# Get main session context %
CTX_LINE=$(openclaw sessions 2>/dev/null | grep "agent:main:main" || true)
if [ -z "$CTX_LINE" ]; then
    exit 0  # No main session, nothing to alert
fi

# Parse percentage from "31k/1000k (3%)"
CTX_PCT=$(echo "$CTX_LINE" | grep -oE '\(([0-9]+)%\)' | grep -oE '[0-9]+')
if [ -z "$CTX_PCT" ]; then
    exit 0
fi

# Read last alert threshold from state file
LAST_ALERT_PCT=0
if [ -f "$STATE_FILE" ]; then
    LAST_ALERT_PCT=$(python3 -c "
import json
with open('$STATE_FILE') as f:
    d = json.load(f)
print(d.get('contextAlert', {}).get('lastAlertPct', 0))
" 2>/dev/null || echo 0)
fi

# Determine threshold
THRESHOLD=0
if [ "$CTX_PCT" -ge 80 ]; then
    THRESHOLD=80
elif [ "$CTX_PCT" -ge 50 ]; then
    THRESHOLD=50
fi

# Only alert if we crossed a new threshold
if [ "$THRESHOLD" -gt 0 ] && [ "$THRESHOLD" -gt "$LAST_ALERT_PCT" ]; then
    # Get model info
    MODEL=$(echo "$CTX_LINE" | awk '{print $4}')
    TOKENS=$(echo "$CTX_LINE" | grep -oE '[0-9]+k/[0-9]+k')
    NOW=$(date "+%Y-%m-%d %H:%M %Z")
    
    MSG="⚠️ Context Alert: ${CTX_PCT}%

• Context: ${TOKENS} (${CTX_PCT}%)
• Model: ${MODEL}
• Time: ${NOW}

Context is above ${THRESHOLD}% threshold."
    
    if [ "$THRESHOLD" -ge 80 ]; then
        MSG="$MSG Consider starting fresh."
    else
        MSG="$MSG Consider switching models or starting fresh."
    fi

    # Send via Telegram Bot API
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d chat_id="$MARK_CHAT_ID" \
        -d text="$MSG" \
        >/dev/null 2>&1

    # Update state
    python3 -c "
import json
state = {}
try:
    with open('$STATE_FILE') as f:
        state = json.load(f)
except: pass
state.setdefault('contextAlert', {})
state['contextAlert']['lastAlertPct'] = $THRESHOLD
state['contextAlert']['lastAlertTs'] = '$(date -u +%Y-%m-%dT%H:%M:%SZ)'
with open('$STATE_FILE', 'w') as f:
    json.dump(state, f, indent=2)
"
elif [ "$THRESHOLD" -eq 0 ] && [ "$LAST_ALERT_PCT" -gt 0 ]; then
    # Reset state when context drops back below 50%
    python3 -c "
import json
state = {}
try:
    with open('$STATE_FILE') as f:
        state = json.load(f)
except: pass
state.setdefault('contextAlert', {})
state['contextAlert']['lastAlertPct'] = 0
state['contextAlert']['lastAlertTs'] = None
with open('$STATE_FILE', 'w') as f:
    json.dump(state, f, indent=2)
"
fi
