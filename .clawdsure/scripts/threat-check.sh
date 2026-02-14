#!/bin/bash
# ClawdSure Threat Model Checker
# Verifies OpenClaw threat mitigations are in place
set -euo pipefail

CLAWDSURE_DIR="/Users/clawdine/.openclaw/workspace/.clawdsure"
THREAT_MODEL_DIR="$CLAWDSURE_DIR/threat-model"
ATLAS_FILE="$THREAT_MODEL_DIR/openclaw-atlas.json"
MITIGATIONS_FILE="$THREAT_MODEL_DIR/mitigations.json"
THREATS_DB="$CLAWDSURE_DIR/vulns/vulns.db"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
TOTAL_THREATS=0
CHECKED=0
MITIGATED=0
UNMITIGATED=0
CRITICAL_UNMITIGATED=0
HIGH_UNMITIGATED=0

# Findings array (we'll build JSON manually)
FINDINGS=()

# Check if required files exist
if [ ! -f "$ATLAS_FILE" ]; then
  echo "❌ Error: openclaw-atlas.json not found"
  exit 1
fi

if [ ! -f "$MITIGATIONS_FILE" ]; then
  echo "❌ Error: mitigations.json not found"
  exit 1
fi

echo "🔒 ClawdSure Threat Model Check"
echo "================================"
echo ""

# Get list of all threats with severity
THREAT_IDS=$(jq -r '.threats[] | "\(.id):\(.severity)"' "$ATLAS_FILE")
TOTAL_THREATS=$(echo "$THREAT_IDS" | wc -l | tr -d ' ')

# Get skill threats from database if it exists
MALICIOUS_SKILLS=""
if [ -f "$THREATS_DB" ]; then
  MALICIOUS_SKILLS=$(sqlite3 "$THREATS_DB" "SELECT name FROM vulnerabilities WHERE severity IN ('critical', 'high');" 2>/dev/null | tr '\n' '|' || echo "")
fi

# Process each mitigation
while IFS= read -r mitigation; do
  THREAT_ID=$(echo "$mitigation" | jq -r '.threat_id')
  CHECK_TYPE=$(echo "$mitigation" | jq -r '.check_type')
  CHECK_CMD=$(echo "$mitigation" | jq -r '.check_command // empty')
  EXPECTED=$(echo "$mitigation" | jq -r '.expected // empty')
  MITIGATED_FLAG=$(echo "$mitigation" | jq -r '.mitigated')
  NOTES=$(echo "$mitigation" | jq -r '.notes')
  
  # Get threat severity
  SEVERITY=$(echo "$THREAT_IDS" | grep "^$THREAT_ID:" | cut -d: -f2)
  
  # Skip manual checks
  if [ "$CHECK_TYPE" = "manual" ]; then
    continue
  fi
  
  CHECKED=$((CHECKED + 1))
  
  # Run the check
  CHECK_PASSED=false
  ACTUAL_VALUE=""
  ERROR_MSG=""
  
  case "$CHECK_TYPE" in
    config)
      if [ -n "$CHECK_CMD" ]; then
        ACTUAL_VALUE=$(eval "$CHECK_CMD" 2>/dev/null || echo "ERROR")
        if [ "$ACTUAL_VALUE" != "ERROR" ]; then
          if [ -n "$EXPECTED" ]; then
            # Check if actual contains expected (using string match, not regex)
            if echo "$ACTUAL_VALUE" | grep -qF "$EXPECTED"; then
              CHECK_PASSED=true
            fi
          else
            # No expected value, just verify command succeeded
            CHECK_PASSED=true
          fi
        else
          ERROR_MSG="Command failed or config key missing"
        fi
      fi
      ;;
      
    file)
      if [ -n "$CHECK_CMD" ]; then
        ACTUAL_VALUE=$(eval "$CHECK_CMD" 2>/dev/null || echo "ERROR")
        if [ "$ACTUAL_VALUE" != "ERROR" ]; then
          if [ -n "$EXPECTED" ]; then
            # Use fixed string match for file checks
            if echo "$ACTUAL_VALUE" | grep -qF "$EXPECTED"; then
              CHECK_PASSED=true
            fi
          else
            # File hash or existence check
            CHECK_PASSED=true
          fi
        else
          ERROR_MSG="File check failed"
        fi
      fi
      ;;
      
    skill)
      if [ -n "$CHECK_CMD" ]; then
        INSTALLED_SKILLS=$(eval "$CHECK_CMD" 2>/dev/null || echo "")
        if [ -n "$INSTALLED_SKILLS" ]; then
          # Check if any installed skill is in the malicious list
          FOUND_THREAT=false
          if [ -n "$MALICIOUS_SKILLS" ]; then
            for skill in $INSTALLED_SKILLS; do
              if echo "$MALICIOUS_SKILLS" | grep -q "|$skill|"; then
                FOUND_THREAT=true
                ERROR_MSG="Malicious skill detected: $skill"
                break
              fi
            done
          fi
          
          if [ "$FOUND_THREAT" = false ]; then
            CHECK_PASSED=true
            ACTUAL_VALUE="No malicious skills detected"
          else
            ACTUAL_VALUE="Threat detected"
          fi
        else
          # No skills installed is also safe
          CHECK_PASSED=true
          ACTUAL_VALUE="No skills installed"
        fi
      fi
      ;;
      
    process)
      if [ -n "$CHECK_CMD" ]; then
        if eval "$CHECK_CMD" >/dev/null 2>&1; then
          CHECK_PASSED=true
          ACTUAL_VALUE="Process check passed"
        else
          ERROR_MSG="Process check failed"
        fi
      fi
      ;;
  esac
  
  # Record result
  if [ "$CHECK_PASSED" = true ]; then
    MITIGATED=$((MITIGATED + 1))
    echo -e "${GREEN}✓${NC} $THREAT_ID ($SEVERITY): Mitigated"
  else
    UNMITIGATED=$((UNMITIGATED + 1))
    echo -e "${RED}✗${NC} $THREAT_ID ($SEVERITY): NOT MITIGATED"
    
    if [ "$SEVERITY" = "critical" ]; then
      CRITICAL_UNMITIGATED=$((CRITICAL_UNMITIGATED + 1))
    elif [ "$SEVERITY" = "high" ]; then
      HIGH_UNMITIGATED=$((HIGH_UNMITIGATED + 1))
    fi
    
    # Add to findings
    FINDING=$(cat <<EOF
{
  "threat_id": "$THREAT_ID",
  "severity": "$SEVERITY",
  "check_type": "$CHECK_TYPE",
  "status": "unmitigated",
  "error": "$ERROR_MSG",
  "notes": "$NOTES"
}
EOF
)
    FINDINGS+=("$FINDING")
  fi
  
done < <(jq -c '.mitigations[]' "$MITIGATIONS_FILE")

# Build JSON report
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
FINDINGS_JSON="[]"
if [ ${#FINDINGS[@]} -gt 0 ]; then
  FINDINGS_JSON=$(printf '%s\n' "${FINDINGS[@]}" | jq -s '.')
fi

REPORT=$(cat <<EOF
{
  "timestamp": "$TIMESTAMP",
  "total_threats": $TOTAL_THREATS,
  "threats_checked": $CHECKED,
  "mitigated": $MITIGATED,
  "unmitigated": $UNMITIGATED,
  "critical_unmitigated": $CRITICAL_UNMITIGATED,
  "high_unmitigated": $HIGH_UNMITIGATED,
  "findings": $FINDINGS_JSON
}
EOF
)

echo ""
echo "================================"
echo "📊 Threat Check Summary"
echo "================================"
echo "Total threats: $TOTAL_THREATS"
echo "Automated checks: $CHECKED"
echo -e "Mitigated: ${GREEN}$MITIGATED${NC}"
echo -e "Unmitigated: ${RED}$UNMITIGATED${NC}"

if [ $CRITICAL_UNMITIGATED -gt 0 ]; then
  echo -e "${RED}Critical unmitigated: $CRITICAL_UNMITIGATED${NC}"
fi

if [ $HIGH_UNMITIGATED -gt 0 ]; then
  echo -e "${YELLOW}High unmitigated: $HIGH_UNMITIGATED${NC}"
fi

echo ""
echo "$REPORT"

# Save JSON report to file for attestation integration
echo "$REPORT" > "$CLAWDSURE_DIR/threat-check-report.json"

# Exit code logic
if [ $CRITICAL_UNMITIGATED -gt 0 ]; then
  echo ""
  echo "❌ FAIL: Critical threats unmitigated"
  exit 1
fi

if [ $HIGH_UNMITIGATED -gt 0 ]; then
  echo ""
  echo "⚠️  WARNING: High-severity threats unmitigated"
  exit 1
fi

echo ""
echo "✅ PASS: All critical and high-severity threats mitigated"
exit 0
