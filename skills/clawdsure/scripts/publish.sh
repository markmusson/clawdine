#!/usr/bin/env bash
# ClawdSure publish — send latest attestation to the relay
# The relay handles IPFS pinning. Users never need IPFS accounts.
#
# Flow: agent → relay (api.clawdsure.io) → IPFS
# The relay aggregates daily attestations into a manifest and pins it.
# Discovery: relay publishes agent→CID mapping, anyone can verify on IPFS.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/portable.sh"

DATA_DIR="${CLAWDSURE_DIR:-$HOME/.openclaw/workspace/.clawdsure}"
RELAY="${CLAWDSURE_RELAY:-https://api.clawdsure.io/v1}"

if [ ! -f "$DATA_DIR/chain.jsonl" ] || [ ! -f "$DATA_DIR/agent.key" ]; then
  echo "not-enrolled"
  exit 0
fi

cd "$DATA_DIR"

# Get latest attestation
LATEST=$(tail -1 chain.jsonl)
SEQ=$(echo "$LATEST" | jq -r '.seq')
AGENT_ID=$(echo "$LATEST" | jq -r '.agent')

# Build publish payload: latest attestation + chain length + public key
PUBKEY_B64=$(base64 < agent.pub | tr -d '\n')
PAYLOAD=$(jq -nc \
  --arg agent "$AGENT_ID" \
  --arg pubkey "$PUBKEY_B64" \
  --argjson seq "$SEQ" \
  --argjson att "$LATEST" \
  '{agent: $agent, pubkey: $pubkey, seq: $seq, attestation: $att}')

# Sign the payload
SIG=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -sign agent.key 2>/dev/null | base64 | tr -d '\n')

# POST to relay
RESPONSE=$(curl -s --max-time 10 \
  -X POST "$RELAY/attest" \
  -H "Content-Type: application/json" \
  -H "X-Agent-ID: $AGENT_ID" \
  -H "X-Signature: $SIG" \
  -d "$PAYLOAD" 2>/dev/null || echo '{"status":"offline"}')

# Parse response
STATUS=$(echo "$RESPONSE" | jq -r '.status // "offline"' 2>/dev/null || echo "offline")
CID=$(echo "$RESPONSE" | jq -r '.cid // empty' 2>/dev/null || echo "")

if [ "$STATUS" = "ok" ] || [ "$STATUS" = "accepted" ]; then
  # Log the pin
  echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"seq\":$SEQ,\"cid\":\"${CID:-pending}\",\"relay\":\"$RELAY\"}" >> "$DATA_DIR/pins.jsonl"
  echo "published:${CID:-pending}"
else
  # Relay offline — attestation is still in chain.jsonl, will sync later
  echo "local-only"
fi

exit 0
