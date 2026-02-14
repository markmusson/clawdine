#!/bin/bash
# Clawdsure IPFS Pinning via Pinata
# Get free API key: https://app.pinata.cloud/developers/api-keys

set -euo pipefail

CLAWDSURE_DIR="/Users/clawdine/.openclaw/workspace/.clawdsure"
CHAIN_FILE="$CLAWDSURE_DIR/chain.jsonl"
PINS_LOG="$CLAWDSURE_DIR/pins.jsonl"

# Check for API key
if [ -z "${PINATA_JWT:-}" ]; then
  if [ -f "$CLAWDSURE_DIR/.pinata-jwt" ]; then
    PINATA_JWT=$(cat "$CLAWDSURE_DIR/.pinata-jwt")
  else
    echo "❌ Set PINATA_JWT env var or create $CLAWDSURE_DIR/.pinata-jwt"
    echo "   Get free key: https://app.pinata.cloud/developers/api-keys"
    exit 1
  fi
fi

# Pin the file
echo "📌 Pinning chain.jsonl to IPFS..."
RESPONSE=$(curl -s -X POST "https://api.pinata.cloud/pinning/pinFileToIPFS" \
  -H "Authorization: Bearer $PINATA_JWT" \
  -F "file=@$CHAIN_FILE" \
  -F "pinataMetadata={\"name\":\"clawdsure-chain-$(date +%Y%m%d)\"}")

# Extract CID
CID=$(echo "$RESPONSE" | jq -r '.IpfsHash // empty')

if [ -z "$CID" ]; then
  echo "❌ Pin failed:"
  echo "$RESPONSE" | jq .
  exit 1
fi

# Log the pin
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SEQ=$(wc -l < "$CHAIN_FILE" | tr -d ' ')
echo "{\"ts\":\"$TIMESTAMP\",\"seq\":$SEQ,\"cid\":\"$CID\",\"gateway\":\"https://gateway.pinata.cloud/ipfs/$CID\"}" >> "$PINS_LOG"

echo "✅ Pinned!"
echo "   CID: $CID"
echo "   URL: https://gateway.pinata.cloud/ipfs/$CID"
echo "   Log: $PINS_LOG"
