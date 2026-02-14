#!/bin/bash
# Clawdsure Daily Attestation
set -euo pipefail

CLAWDSURE_DIR="/Users/clawdine/.openclaw/workspace/.clawdsure"
CLAWDSTRIKE_DIR="/Users/clawdine/.openclaw/workspace/skills/clawdstrike"
CHAIN_FILE="$CLAWDSURE_DIR/chain.jsonl"
KEY_FILE="$CLAWDSURE_DIR/clawdine.key"

cd "$CLAWDSURE_DIR"

# Get previous hash
if [ -f "$CHAIN_FILE" ]; then
  PREV_HASH=$(tail -1 "$CHAIN_FILE" | shasum -a 256 | cut -c1-64)
  SEQ=$(($(wc -l < "$CHAIN_FILE") + 1))
else
  PREV_HASH="null"
  SEQ=1
fi

# Run ClawdStrike collection
export OPENCLAW_WORKSPACE_DIR="/Users/clawdine/.openclaw/workspace"
cd "$CLAWDSTRIKE_DIR"
bash scripts/collect_verified.sh >/dev/null 2>&1

# Get audit results
AUDIT_OUTPUT=$(openclaw security audit 2>&1 || true)
CRITICAL=$(echo "$AUDIT_OUTPUT" | grep -oE '[0-9]+ critical' | grep -oE '[0-9]+' || echo "0")
WARN=$(echo "$AUDIT_OUTPUT" | grep -oE '[0-9]+ warn' | grep -oE '[0-9]+' || echo "0")
INFO=$(echo "$AUDIT_OUTPUT" | grep -oE '[0-9]+ info' | grep -oE '[0-9]+' || echo "0")
VERSION=$(openclaw --version 2>&1 | tail -1)

# Determine result
if [ "$CRITICAL" -eq 0 ]; then
  RESULT="PASS"
else
  RESULT="FAIL"
fi

# Generate attestation
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
ATTESTATION=$(cat << EOF
{"seq":$SEQ,"prev":"$PREV_HASH","ts":"$TIMESTAMP","agent":"CLWD-FFF4D493","result":"$RESULT","critical":$CRITICAL,"warn":$WARN,"info":$INFO,"version":"$VERSION"}
EOF
)

# Sign
cd "$CLAWDSURE_DIR"
SIG=$(echo -n "$ATTESTATION" | openssl dgst -sha256 -sign "$KEY_FILE" | base64 | tr -d '\n')

# Append signed attestation to chain
echo "${ATTESTATION%\}},\"sig\":\"$SIG\"}" >> "$CHAIN_FILE"

echo "=== Clawdsure Attestation #$SEQ ==="
echo "Result: $RESULT"
echo "Critical: $CRITICAL | Warn: $WARN | Info: $INFO"
echo "Chain: $CHAIN_FILE"
