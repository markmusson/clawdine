#!/bin/bash
# Clawdsure Daily Attestation with API Reporting
set -euo pipefail

CLAWDSURE_DIR="$HOME/.openclaw/workspace/.clawdsure"
CLAWDSTRIKE_DIR="$HOME/.openclaw/workspace/skills/clawdstrike"
API_BASE="${CLAWDSURE_API:-https://api.clawdsure.io/v1}"

cd "$CLAWDSURE_DIR"

# Load agent identity
FINGERPRINT=$(cat agent.pub | shasum -a 256 | cut -c1-64)
AGENT_ID="CLWD-$(echo $FINGERPRINT | cut -c1-8 | tr 'a-f' 'A-F')"

echo "🔄 Daily Attestation: $AGENT_ID"
echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo ""

# Step 1: Run ClawdStrike audit
echo "1️⃣  Running security audit..."
export OPENCLAW_WORKSPACE_DIR="$HOME/.openclaw/workspace"
cd "$CLAWDSTRIKE_DIR"
bash scripts/collect_verified.sh >/dev/null 2>&1

AUDIT_OUTPUT=$(openclaw security audit 2>&1 || true)
CRITICAL=$(echo "$AUDIT_OUTPUT" | grep -oE '[0-9]+ critical' | grep -oE '[0-9]+' || echo "0")
WARN=$(echo "$AUDIT_OUTPUT" | grep -oE '[0-9]+ warn' | grep -oE '[0-9]+' || echo "0")
INFO=$(echo "$AUDIT_OUTPUT" | grep -oE '[0-9]+ info' | grep -oE '[0-9]+' || echo "0")
VERSION=$(openclaw --version 2>&1 | tail -1)

if [ "$CRITICAL" -gt 0 ]; then
  RESULT="FAIL"
  echo "   ⚠️  FAIL: $CRITICAL critical findings"
else
  RESULT="PASS"
  echo "   ✓ PASS"
fi

# Step 2: Build attestation
echo ""
echo "2️⃣  Creating attestation..."
cd "$CLAWDSURE_DIR"

PREV_HASH=$(tail -1 chain.jsonl | shasum -a 256 | cut -c1-64)
SEQ=$(($(wc -l < chain.jsonl | tr -d ' ') + 1))
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

ATTESTATION=$(cat << EOF
{"seq":$SEQ,"prev":"$PREV_HASH","ts":"$TIMESTAMP","agent":"$AGENT_ID","result":"$RESULT","critical":$CRITICAL,"warn":$WARN,"info":$INFO,"version":"$VERSION"}
EOF
)

# Sign attestation
SIG=$(echo -n "$ATTESTATION" | openssl dgst -sha256 -sign agent.key 2>/dev/null | base64 | tr -d '\n')
SIGNED="${ATTESTATION%\}},\"sig\":\"$SIG\"}"

# Append to chain
echo "$SIGNED" >> chain.jsonl
echo "   ✓ Attestation #$SEQ signed"

# Step 3: Pin to IPFS
echo ""
echo "3️⃣  Pinning to IPFS..."
CID="pending"
if [ -f ".pinata-jwt" ]; then
  PINATA_JWT=$(cat .pinata-jwt)
  RESPONSE=$(curl -s -X POST "https://api.pinata.cloud/pinning/pinFileToIPFS" \
    -H "Authorization: Bearer $PINATA_JWT" \
    -F "file=@chain.jsonl" \
    -F "pinataMetadata={\"name\":\"clawdsure-$AGENT_ID-seq$SEQ\"}")
  
  CID=$(echo "$RESPONSE" | jq -r '.IpfsHash // empty')
  if [ -n "$CID" ]; then
    echo "   ✓ CID: $CID"
    echo "{\"ts\":\"$TIMESTAMP\",\"seq\":$SEQ,\"cid\":\"$CID\"}" >> pins.jsonl
  else
    echo "   ❌ Pin failed"
  fi
else
  echo "   ⏭️  Skipped (no JWT)"
fi

# Step 4: Report to UW platform
echo ""
echo "4️⃣  Reporting to ClawdSafe..."

REPORT_PAYLOAD=$(cat << EOF
{
  "action": "attestation",
  "agent": {
    "id": "$AGENT_ID",
    "fingerprint": "$FINGERPRINT"
  },
  "attestation": $SIGNED,
  "ipfs": {
    "cid": "$CID",
    "gateway": "https://gateway.pinata.cloud/ipfs/$CID"
  },
  "chain": {
    "length": $SEQ,
    "prevHash": "$PREV_HASH"
  }
}
EOF
)

REPORT_SIG=$(echo -n "$REPORT_PAYLOAD" | openssl dgst -sha256 -sign agent.key 2>/dev/null | base64 | tr -d '\n')

# Submit to API
if curl -s --max-time 5 "$API_BASE/health" >/dev/null 2>&1; then
  RESPONSE=$(curl -s -X POST "$API_BASE/attestation" \
    -H "Content-Type: application/json" \
    -H "X-Agent-ID: $AGENT_ID" \
    -H "X-Agent-Signature: $REPORT_SIG" \
    -d "$REPORT_PAYLOAD")
  echo "   API: $RESPONSE"
else
  echo "   ℹ️  API offline (local-only mode)"
  # Save for later sync
  echo "$REPORT_PAYLOAD" > "pending-report-$SEQ.json"
fi

# Step 5: Summary
echo ""
echo "========================================"
echo "📊 ATTESTATION SUMMARY"
echo "========================================"
echo "Seq:      #$SEQ"
echo "Result:   $RESULT"
echo "Findings: $CRITICAL critical, $WARN warn, $INFO info"
echo "CID:      $CID"
echo "Chain:    $SEQ attestations"
echo ""

if [ "$RESULT" = "FAIL" ]; then
  echo "⚠️  WARNING: Critical findings detected!"
  echo "   You have 48h to remediate before chain break."
  echo "   Run: openclaw security audit"
  exit 1
fi

echo "✅ Attestation complete"
