#!/usr/bin/env bash
# ClawdSure daily attestation
# Generates machine fingerprint + config hash, signs, chains, publishes
# Silent on success (exit 0). Outputs only on FAIL or errors.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/portable.sh"
source "$SCRIPT_DIR/fingerprint.sh"

DATA_DIR="${CLAWDSURE_DIR:-$HOME/.openclaw/workspace/.clawdsure}"
VERBOSE="${CLAWDSURE_VERBOSE:-false}"

check_deps

# Must be enrolled
if [ ! -f "$DATA_DIR/agent.key" ] || [ ! -f "$DATA_DIR/chain.jsonl" ]; then
  echo "❌ Not enrolled. Run: bash $(dirname "$0")/enroll.sh"
  exit 1
fi

cd "$DATA_DIR"

# Agent identity
PUBKEY_HASH=$(portable_sha256 agent.pub)
AGENT_ID="CLWD-$(echo "$PUBKEY_HASH" | cut -c1-8 | tr 'a-f' 'A-F')"

# Verify chain continuity (agent ID must match)
CHAIN_AGENT=$(tail -1 chain.jsonl | jq -r '.agent' 2>/dev/null || echo "")
if [ -n "$CHAIN_AGENT" ] && [ "$CHAIN_AGENT" != "$AGENT_ID" ]; then
  echo "❌ Agent ID mismatch. Chain: $CHAIN_AGENT, Key: $AGENT_ID"
  echo "   Re-enroll: bash $(dirname "$0")/enroll.sh"
  exit 1
fi

# 1. Machine fingerprint + config hash
FP_RECORD=$(clawdsure_fingerprint_record)
MACHINE_HASH=$(echo "$FP_RECORD" | jq -r '.machine')
CONFIG_HASH=$(echo "$FP_RECORD" | jq -r '.config')

# 2. Run OpenClaw security audit (if available)
RESULT="PASS"
AUDIT_NATIVE_HASH="none"
AUDIT_MACHINE_HASH="none"
CRITICAL=0

if command -v openclaw >/dev/null 2>&1; then
  AUDIT_OUT=$(openclaw security audit --json 2>&1 || echo '{}')
  AUDIT_NATIVE_HASH=$(echo -n "$AUDIT_OUT" | portable_sha256 -)
  
  # Check for critical findings
  CRITICAL=$(echo "$AUDIT_OUT" | jq -r '.summary.critical // 0' 2>/dev/null || echo "0")
  if [ "${CRITICAL:-0}" -gt 0 ]; then
    RESULT="FAIL"
  fi
fi

# 3. Run audit-machine.sh and hash output
AUDIT_MACHINE_OUT=$(bash "$SCRIPT_DIR/audit-machine.sh" 2>/dev/null || echo '{"error":"audit-machine.sh failed"}')
AUDIT_MACHINE_HASH=$(echo -n "$AUDIT_MACHINE_OUT" | portable_sha256 -)
echo "$AUDIT_MACHINE_OUT" > "$DATA_DIR/last-audit.json"

# Check for machine audit failures
MACHINE_FAILS=$(echo "$AUDIT_MACHINE_OUT" | jq -r '.summary.fail // 0' 2>/dev/null || echo "0")
if [ "${MACHINE_FAILS:-0}" -gt 0 ]; then
  RESULT="FAIL"
  CRITICAL=$((CRITICAL + MACHINE_FAILS))
fi

# 4. Build attestation
PREV_LINE=$(tail -1 chain.jsonl)
PREV_HASH=$(echo -n "$PREV_LINE" | portable_sha256 -)
SEQ=$(($(wc -l < chain.jsonl | tr -d ' ') + 1))
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

ATTESTATION=$(jq -nc \
  --argjson fp "$FP_RECORD" \
  --arg ts "$TIMESTAMP" \
  --arg agent "$AGENT_ID" \
  --arg prev "$PREV_HASH" \
  --arg an "$AUDIT_NATIVE_HASH" \
  --arg am "$AUDIT_MACHINE_HASH" \
  --arg result "$RESULT" \
  --argjson seq "$SEQ" \
  '{v:1, seq:$seq, prev:$prev, ts:$ts, agent:$agent, fingerprint:$fp, audit_native:$an, audit_machine:$am, result:$result, sig:""}')

# 5. Sign
UNSIGNED=$(echo "$ATTESTATION" | jq -c 'del(.sig)')
SIG=$(echo -n "$UNSIGNED" | openssl dgst -sha256 -sign agent.key 2>/dev/null | base64 | tr -d '\n')
ATTESTATION=$(echo "$ATTESTATION" | jq -c --arg s "$SIG" '.sig = $s')

# 6. Append to chain
echo "$ATTESTATION" >> chain.jsonl

# 7. Publish to relay
PUB_RESULT=$(bash "$SCRIPT_DIR/publish.sh" 2>/dev/null || echo "offline")

# 8. Output
if [ "$RESULT" = "FAIL" ]; then
  echo "🚨 CLAWDSURE FAIL: $AGENT_ID | #$SEQ | $CRITICAL critical findings"
  echo "   Remediate within 48h or chain breaks."
  exit 1
fi

# Check for chain gap warning
if [ "$SEQ" -gt 1 ]; then
  PREV_TS=$(echo "$PREV_LINE" | jq -r '.ts' 2>/dev/null || echo "")
  if [ -n "$PREV_TS" ]; then
    PREV_EPOCH=$(portable_epoch "$PREV_TS")
    NOW_EPOCH=$(date +%s)
    GAP_H=$(( (NOW_EPOCH - PREV_EPOCH) / 3600 ))
    if [ "$GAP_H" -gt 36 ]; then
      echo "⚠️ CLAWDSURE: ${GAP_H}h gap (48h = chain break) | #$SEQ"
    fi
  fi
fi

# Silent success — log only
echo "$TIMESTAMP | #$SEQ | $RESULT | $PUB_RESULT" >> "$DATA_DIR/attest.log"

if [ "$VERBOSE" = "true" ]; then
  echo "✅ #$SEQ | $RESULT | machine:${MACHINE_HASH:0:8} config:${CONFIG_HASH:0:8} | $PUB_RESULT"
fi

exit 0
