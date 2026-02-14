#!/bin/bash
# Clawdsure Full Attestation: Audit → Sign → Pin to IPFS
set -euo pipefail

CLAWDSURE_DIR="/Users/clawdine/.openclaw/workspace/.clawdsure"

echo "🔒 Clawdsure Full Attestation"
echo "=============================="

# Step 1: Run ClawdStrike and sign attestation
echo ""
echo "1️⃣ Running security audit..."
bash "$CLAWDSURE_DIR/attest.sh"

# Step 2: Pin to IPFS (if configured)
if [ -n "${PINATA_JWT:-}" ] || [ -f "$CLAWDSURE_DIR/.pinata-jwt" ]; then
  echo ""
  echo "2️⃣ Pinning to IPFS..."
  bash "$CLAWDSURE_DIR/pin-ipfs.sh"
else
  echo ""
  echo "⏭️ Skipping IPFS pin (no Pinata JWT configured)"
  echo "   To enable: https://app.pinata.cloud/developers/api-keys"
  echo "   Then: echo 'YOUR_JWT' > $CLAWDSURE_DIR/.pinata-jwt"
fi

# Show chain status
echo ""
echo "📊 Chain Status:"
echo "   Attestations: $(wc -l < "$CLAWDSURE_DIR/chain.jsonl" | tr -d ' ')"
if [ -f "$CLAWDSURE_DIR/pins.jsonl" ]; then
  echo "   IPFS Pins: $(wc -l < "$CLAWDSURE_DIR/pins.jsonl" | tr -d ' ')"
  echo "   Latest CID: $(tail -1 "$CLAWDSURE_DIR/pins.jsonl" | jq -r '.cid')"
fi

echo ""
echo "✅ Attestation complete"
