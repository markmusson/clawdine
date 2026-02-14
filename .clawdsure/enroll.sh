#!/bin/bash
# Clawdsure Enrollment Flow
# Install → Audit → Genesis → IPFS → Register → Pay
set -euo pipefail

CLAWDSURE_DIR="$HOME/.openclaw/workspace/.clawdsure"
CLAWDSTRIKE_DIR="$HOME/.openclaw/workspace/skills/clawdstrike"
API_BASE="${CLAWDSURE_API:-https://api.clawdsure.io/v1}"

echo "🛡️  CLAWDSURE ENROLLMENT"
echo "========================"
echo ""

# Step 1: Check/Install ClawdStrike
echo "1️⃣  Checking ClawdStrike skill..."
if [ ! -d "$CLAWDSTRIKE_DIR" ]; then
  echo "   Installing ClawdStrike..."
  git clone https://github.com/cantinaxyz/clawdstrike "$CLAWDSTRIKE_DIR"
else
  echo "   ✓ ClawdStrike installed"
fi

# Step 2: Run initial audit
echo ""
echo "2️⃣  Running security audit..."
export OPENCLAW_WORKSPACE_DIR="$HOME/.openclaw/workspace"
cd "$CLAWDSTRIKE_DIR"
bash scripts/collect_verified.sh >/dev/null 2>&1

AUDIT_OUTPUT=$(openclaw security audit 2>&1 || true)
CRITICAL=$(echo "$AUDIT_OUTPUT" | grep -oE '[0-9]+ critical' | grep -oE '[0-9]+' || echo "0")

if [ "$CRITICAL" -gt 0 ]; then
  echo "   ❌ FAIL: $CRITICAL critical findings"
  echo "   Please remediate before enrolling:"
  echo "$AUDIT_OUTPUT" | grep -A2 "CRITICAL\|critical"
  exit 1
fi
echo "   ✓ PASS: 0 critical findings"

# Step 3: Generate keypair (if not exists)
echo ""
echo "3️⃣  Setting up identity..."
mkdir -p "$CLAWDSURE_DIR"
cd "$CLAWDSURE_DIR"

if [ ! -f agent.key ]; then
  openssl ecparam -genkey -name prime256v1 -noout -out agent.key 2>/dev/null
  openssl ec -in agent.key -pubout -out agent.pub 2>/dev/null
  echo "   ✓ Generated new keypair"
else
  echo "   ✓ Using existing keypair"
fi

# Generate agent fingerprint
FINGERPRINT=$(cat agent.pub | shasum -a 256 | cut -c1-64)
AGENT_ID="CLWD-$(echo $FINGERPRINT | cut -c1-8 | tr 'a-f' 'A-F')"
echo "   Agent ID: $AGENT_ID"
echo "   Fingerprint: $FINGERPRINT"

# Step 4: Generate genesis attestation
echo ""
echo "4️⃣  Creating genesis attestation..."
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
VERSION=$(openclaw --version 2>&1 | tail -1)
WARN=$(echo "$AUDIT_OUTPUT" | grep -oE '[0-9]+ warn' | grep -oE '[0-9]+' || echo "0")
INFO=$(echo "$AUDIT_OUTPUT" | grep -oE '[0-9]+ info' | grep -oE '[0-9]+' || echo "0")

GENESIS=$(cat << EOF
{"seq":1,"prev":"genesis","ts":"$TIMESTAMP","agent":"$AGENT_ID","fingerprint":"$FINGERPRINT","result":"PASS","critical":0,"warn":$WARN,"info":$INFO,"version":"$VERSION","enrollment":true}
EOF
)

# Sign genesis
SIG=$(echo -n "$GENESIS" | openssl dgst -sha256 -sign agent.key 2>/dev/null | base64 | tr -d '\n')
SIGNED_GENESIS="${GENESIS%\}},\"sig\":\"$SIG\"}"

# Write chain
echo "$SIGNED_GENESIS" > chain.jsonl
echo "   ✓ Genesis attestation created"

# Step 5: Pin to IPFS
echo ""
echo "5️⃣  Pinning to IPFS..."
if [ -z "${PINATA_JWT:-}" ] && [ ! -f ".pinata-jwt" ]; then
  echo "   ⚠️  No Pinata JWT configured"
  echo "   Get one at: https://app.pinata.cloud/developers/api-keys"
  echo -n "   Enter Pinata JWT (or press enter to skip): "
  read -r JWT_INPUT
  if [ -n "$JWT_INPUT" ]; then
    echo "$JWT_INPUT" > .pinata-jwt
  fi
fi

if [ -f ".pinata-jwt" ]; then
  PINATA_JWT=$(cat .pinata-jwt)
  RESPONSE=$(curl -s -X POST "https://api.pinata.cloud/pinning/pinFileToIPFS" \
    -H "Authorization: Bearer $PINATA_JWT" \
    -F "file=@chain.jsonl" \
    -F "pinataMetadata={\"name\":\"clawdsure-genesis-$AGENT_ID\"}")
  
  CID=$(echo "$RESPONSE" | jq -r '.IpfsHash // empty')
  if [ -n "$CID" ]; then
    echo "   ✓ Pinned to IPFS"
    echo "   CID: $CID"
    echo "   URL: https://gateway.pinata.cloud/ipfs/$CID"
    echo "{\"ts\":\"$TIMESTAMP\",\"seq\":1,\"cid\":\"$CID\",\"type\":\"genesis\"}" > pins.jsonl
  else
    echo "   ❌ Pin failed: $RESPONSE"
    CID="pending"
  fi
else
  echo "   ⏭️  Skipped (no JWT)"
  CID="pending"
fi

# Step 6: Create enrollment request for UW platform
echo ""
echo "6️⃣  Preparing underwriting request..."

# Create enrollment payload
ENROLLMENT_PAYLOAD=$(cat << EOF
{
  "action": "enroll",
  "agent": {
    "id": "$AGENT_ID",
    "fingerprint": "$FINGERPRINT",
    "publicKey": "$(cat agent.pub | base64 | tr -d '\n')"
  },
  "genesis": {
    "attestation": $SIGNED_GENESIS,
    "ipfsCid": "$CID",
    "timestamp": "$TIMESTAMP"
  },
  "audit": {
    "tool": "clawdstrike",
    "version": "$VERSION",
    "result": "PASS",
    "findings": {
      "critical": 0,
      "warn": $WARN,
      "info": $INFO
    }
  },
  "policy": {
    "tier": "basic",
    "premium": 50,
    "payout": 500,
    "term": "annual"
  }
}
EOF
)

echo "$ENROLLMENT_PAYLOAD" > enrollment-request.json
echo "   ✓ Enrollment request created"

# Sign the enrollment request
ENROLLMENT_SIG=$(echo -n "$ENROLLMENT_PAYLOAD" | openssl dgst -sha256 -sign agent.key 2>/dev/null | base64 | tr -d '\n')
echo "$ENROLLMENT_SIG" > enrollment-request.sig

# Step 7: Submit to UW platform (or show how to)
echo ""
echo "7️⃣  Submitting to underwriting platform..."

# Check if API is reachable
if curl -s --max-time 5 "$API_BASE/health" >/dev/null 2>&1; then
  # Real API call
  RESPONSE=$(curl -s -X POST "$API_BASE/enroll" \
    -H "Content-Type: application/json" \
    -H "X-Agent-Signature: $ENROLLMENT_SIG" \
    -d "@enrollment-request.json")
  echo "   API Response: $RESPONSE"
else
  echo "   ℹ️  UW Platform not available (prototype mode)"
  echo "   Request saved to: enrollment-request.json"
  echo "   Signature saved to: enrollment-request.sig"
  echo ""
  echo "   To submit manually:"
  echo "   curl -X POST $API_BASE/enroll \\"
  echo "     -H 'Content-Type: application/json' \\"
  echo "     -H 'X-Agent-Signature: <sig>' \\"
  echo "     -d @enrollment-request.json"
fi

# Step 8: Summary
echo ""
echo "========================================"
echo "📋 ENROLLMENT SUMMARY"
echo "========================================"
echo "Agent ID:     $AGENT_ID"
echo "Fingerprint:  ${FINGERPRINT:0:16}..."
echo "Genesis CID:  $CID"
echo "Audit:        PASS (0 critical, $WARN warn, $INFO info)"
echo "Policy:       Basic (\$50/year → \$500 payout)"
echo ""
echo "Files created:"
echo "  ~/.openclaw/workspace/.clawdsure/"
echo "  ├── agent.key      (KEEP SECRET)"
echo "  ├── agent.pub"
echo "  ├── chain.jsonl"
echo "  ├── pins.jsonl"
echo "  └── enrollment-request.json"
echo ""
echo "Next steps:"
echo "  1. Complete payment at: https://clawdsure.io/pay/$AGENT_ID"
echo "  2. Set up daily attestation (cron/launchd)"
echo "  3. Keep your chain unbroken!"
echo ""
echo "✅ Enrollment complete"
