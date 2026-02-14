#!/usr/bin/env bash
# ClawdSure enrollment — generate identity + genesis attestation
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/portable.sh"
source "$SCRIPT_DIR/fingerprint.sh"

DATA_DIR="${CLAWDSURE_DIR:-$HOME/.openclaw/workspace/.clawdsure}"
RELAY="${CLAWDSURE_RELAY:-https://api.clawdsure.io/v1}"

check_deps

echo "🛡️  ClawdSure Enrollment"
echo ""

# 1. Check OpenClaw
if ! command -v openclaw >/dev/null 2>&1; then
  echo "❌ OpenClaw not found. Install from https://github.com/openclaw/openclaw"
  exit 1
fi

# 2. Create data dir
mkdir -p "$DATA_DIR"
cd "$DATA_DIR"

# 3. Generate keypair (if not exists)
if [ -f agent.key ]; then
  echo "✓ Using existing keypair"
else
  openssl ecparam -genkey -name prime256v1 -noout -out agent.key 2>/dev/null
  openssl ec -in agent.key -pubout -out agent.pub 2>/dev/null
  chmod 600 agent.key
  echo "✓ Generated ECDSA keypair"
fi

# 4. Derive agent ID
PUBKEY_HASH=$(portable_sha256 agent.pub)
AGENT_ID="CLWD-$(echo "$PUBKEY_HASH" | cut -c1-8 | tr 'a-f' 'A-F')"
echo "  Agent: $AGENT_ID"

# 5. Machine fingerprint
FP_RECORD=$(clawdsure_fingerprint_record)
echo "  Machine: $(echo "$FP_RECORD" | jq -r '.machine' | cut -c1-16)..."
echo "  Config:  $(echo "$FP_RECORD" | jq -r '.config' | cut -c1-16)..."

# 6. Genesis attestation
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

GENESIS=$(jq -nc \
  --argjson fp "$FP_RECORD" \
  --arg ts "$TIMESTAMP" \
  --arg agent "$AGENT_ID" \
  '{v:1, seq:1, prev:"genesis", ts:$ts, agent:$agent, fingerprint:$fp, result:"PASS", sig:""}')

# Sign (without sig field)
UNSIGNED=$(echo "$GENESIS" | jq -c 'del(.sig)')
SIG=$(echo -n "$UNSIGNED" | openssl dgst -sha256 -sign agent.key 2>/dev/null | base64 | tr -d '\n')
GENESIS=$(echo "$GENESIS" | jq -c --arg s "$SIG" '.sig = $s')

# Write chain
echo "$GENESIS" > chain.jsonl
echo "✓ Genesis attestation signed"

# 7. Publish to relay
echo ""
bash "$SCRIPT_DIR/publish.sh" && true

# Summary
echo ""
echo "═══════════════════════════════"
echo "Agent ID:  $AGENT_ID"
echo "Chain:     $DATA_DIR/chain.jsonl"
echo "Key:       $DATA_DIR/agent.key (KEEP SECRET)"
echo ""
echo "Next: set up daily attestation"
echo "  bash $SCRIPT_DIR/attest.sh"
echo "═══════════════════════════════"
