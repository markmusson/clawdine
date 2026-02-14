#!/usr/bin/env bash
# ClawdSure chain verification
# Validates signatures, hash linking, timestamps, and continuity
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/portable.sh"

DATA_DIR="${CLAWDSURE_DIR:-$HOME/.openclaw/workspace/.clawdsure}"

if [ ! -f "$DATA_DIR/chain.jsonl" ]; then
  echo "❌ No chain found. Run enroll.sh first."
  exit 1
fi
if [ ! -f "$DATA_DIR/agent.pub" ]; then
  echo "❌ No public key found."
  exit 1
fi

check_deps
cd "$DATA_DIR"

echo "🔍 ClawdSure Chain Verification"
echo ""

ERRORS=0
WARNINGS=0
PREV_HASH="genesis"
PREV_TS=""
TOTAL=$(wc -l < chain.jsonl | tr -d ' ')
LINE=0

while IFS= read -r entry; do
  LINE=$((LINE + 1))
  SEQ=$(echo "$entry" | jq -r '.seq')
  PREV=$(echo "$entry" | jq -r '.prev')
  TS=$(echo "$entry" | jq -r '.ts')
  RESULT=$(echo "$entry" | jq -r '.result')
  SIG=$(echo "$entry" | jq -r '.sig')
  UNSIGNED=$(echo "$entry" | jq -c 'del(.sig)')

  printf "#%-3s %s " "$SEQ" "$TS"

  # Sequence
  if [ "$SEQ" != "$LINE" ]; then
    printf "❌ seq mismatch (expected %d) " "$LINE"
    ERRORS=$((ERRORS + 1))
  fi

  # Hash link
  if [ "$PREV" != "$PREV_HASH" ]; then
    printf "❌ broken link "
    ERRORS=$((ERRORS + 1))
  fi

  # Signature
  if echo -n "$UNSIGNED" | openssl dgst -sha256 -verify agent.pub \
      -signature <(echo "$SIG" | portable_base64_decode) >/dev/null 2>&1; then
    printf "✓sig "
  else
    printf "❌ bad sig "
    ERRORS=$((ERRORS + 1))
  fi

  # Time gap
  if [ -n "$PREV_TS" ]; then
    CURR_E=$(portable_epoch "$TS")
    PREV_E=$(portable_epoch "$PREV_TS")
    if [ "$CURR_E" -gt 0 ] && [ "$PREV_E" -gt 0 ]; then
      GAP_H=$(( (CURR_E - PREV_E) / 3600 ))
      if [ "$GAP_H" -gt 48 ]; then
        printf "❌ %dh gap " "$GAP_H"
        ERRORS=$((ERRORS + 1))
      elif [ "$GAP_H" -gt 36 ]; then
        printf "⚠️ %dh gap " "$GAP_H"
        WARNINGS=$((WARNINGS + 1))
      fi
    fi
  fi

  # Result
  if [ "$RESULT" = "FAIL" ]; then
    printf "⚠️FAIL "
    WARNINGS=$((WARNINGS + 1))
  fi

  printf "\n"

  PREV_HASH=$(echo -n "$entry" | portable_sha256 -)
  PREV_TS="$TS"
done < chain.jsonl

echo ""
echo "Chain: $TOTAL attestations | $ERRORS errors | $WARNINGS warnings"

if [ "$ERRORS" -gt 0 ]; then
  echo "❌ INVALID — chain integrity broken"
  exit 1
elif [ "$WARNINGS" -gt 0 ]; then
  echo "⚠️  VALID (warnings)"
  exit 0
else
  echo "✅ VALID"
  exit 0
fi
