#!/bin/bash
# Daily Status Report — runs via launchd, zero tokens
# Checks cron jobs + launchd agents, sends evening Telegram report
# Highlights failures and dodgy jobs

set -euo pipefail

TELEGRAM_BOT_TOKEN=$(python3 -c "
import json
with open('$HOME/.openclaw/openclaw.json') as f:
    c = json.load(f)
print(c['channels']['telegram']['botToken'])
")
MARK_CHAT_ID="7018377788"
NOW=$(date "+%Y-%m-%d %H:%M %Z")
PROBLEMS=""

# --- Cron Jobs ---
CRON_SECTION=""
while IFS= read -r line; do
    [[ "$line" == ID* ]] && continue
    [ -z "$line" ] && continue
    NAME=$(echo "$line" | awk '{print $2}')
    LAST=$(echo "$line" | grep -oE '[0-9]+[mhd] ago' || echo "never")
    JOB_STATUS=$(echo "$line" | grep -oE '(idle|ok|fail|running)' | tail -1)
    if [ "$JOB_STATUS" = "fail" ]; then
        ICON="❌"
        PROBLEMS="${PROBLEMS}• Cron '${NAME}' failed (last: ${LAST})
"
    elif [ "$JOB_STATUS" = "ok" ] || [ "$JOB_STATUS" = "idle" ]; then
        ICON="✅"
    else
        ICON="⚠️"
        PROBLEMS="${PROBLEMS}• Cron '${NAME}' status: ${JOB_STATUS}
"
    fi
    CRON_SECTION="${CRON_SECTION}  ${ICON} ${NAME} (${JOB_STATUS}, last: ${LAST})
"
done < <(openclaw cron list 2>/dev/null || echo "")

[ -z "$CRON_SECTION" ] && CRON_SECTION="  (none)
"

# --- LaunchD Agents ---
LAUNCHD_SECTION=""
AGENTS=("com.clawdine.weather-tracker" "com.clawdine.context-alert" "com.clawdine.kalshi-btc-monitor" "com.clawdine.daily-status-report" "com.clawdine.weather-signal-gen" "com.clawdine.weather-signal-alert" "com.clawdine.weather-paper-trader")
for agent in "${AGENTS[@]}"; do
    SHORT="${agent##com.clawdine.}"
    INFO=$(launchctl list "$agent" 2>/dev/null || echo "")
    if [ -n "$INFO" ]; then
        EXIT=$(echo "$INFO" | grep LastExitStatus | grep -oE '[0-9]+' || echo "?")
        if [ "$EXIT" = "0" ]; then
            LAUNCHD_SECTION="${LAUNCHD_SECTION}  ✅ ${SHORT} (exit:0)
"
        else
            LAUNCHD_SECTION="${LAUNCHD_SECTION}  ❌ ${SHORT} (exit:${EXIT})
"
            PROBLEMS="${PROBLEMS}• LaunchD '${SHORT}' exited ${EXIT}
"
        fi
    else
        LAUNCHD_SECTION="${LAUNCHD_SECTION}  ❌ ${SHORT} (not loaded)
"
        PROBLEMS="${PROBLEMS}• LaunchD '${SHORT}' not loaded
"
    fi
done

# --- Gateway ---
GW_STATUS=$(openclaw gateway status 2>/dev/null | head -1 || echo "unknown")
if ! echo "$GW_STATUS" | grep -qi "loaded\|running"; then
    PROBLEMS="${PROBLEMS}• Gateway: ${GW_STATUS}
"
fi

# --- Header ---
if [ -n "$PROBLEMS" ]; then
    HEADER="🚨 ISSUES FOUND"
    PROBLEM_BLOCK="
⚠️ Problems:
${PROBLEMS}"
else
    HEADER="✅ ALL CLEAR"
    PROBLEM_BLOCK=""
fi

# --- Build message ---
MSG="📊 Evening Status — ${NOW}
${HEADER}

🔧 Gateway: ${GW_STATUS}

⏰ Cron:
${CRON_SECTION}
🚀 LaunchD:
${LAUNCHD_SECTION}${PROBLEM_BLOCK}"

# Send via Telegram
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -d chat_id="$MARK_CHAT_ID" \
    -d text="$MSG" \
    >/dev/null 2>&1

echo "Report sent at $NOW"
