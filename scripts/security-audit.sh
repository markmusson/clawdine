#!/usr/bin/env bash
# security-audit.sh
# Daily read-only security check for macOS/OpenClaw host.
# Checks: firewall, SSH config, open ports, docker status, OpenClaw audit.
# Outputs a summary line — non-zero exit if any WARN/FAIL found.

set -uo pipefail

LOG_DIR="$HOME/.openclaw/workspace/logs"
LOG_FILE="$LOG_DIR/security-audit.log"
mkdir -p "$LOG_DIR"

TS=$(date '+%Y-%m-%d %H:%M:%S')
ISSUES=()
SUMMARY=()

log() { echo "[$TS] $*" >> "$LOG_FILE"; }
pass() { SUMMARY+=("✅ $1"); log "PASS: $1"; }
warn() { SUMMARY+=("⚠️  $1"); ISSUES+=("$1"); log "WARN: $1"; }
fail() { SUMMARY+=("❌ $1"); ISSUES+=("$1"); log "FAIL: $1"; }

log "security-audit starting"

# --- Firewall ---
FW=$(/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate 2>/dev/null || echo "unknown")
if echo "$FW" | grep -q "enabled"; then
  pass "Firewall enabled"
else
  fail "Firewall DISABLED — run: sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on"
fi

# Stealth mode
STEALTH=$(/usr/libexec/ApplicationFirewall/socketfilterfw --getstealthmode 2>/dev/null || echo "unknown")
if echo "$STEALTH" | grep -q "enabled"; then
  pass "Stealth mode enabled"
else
  warn "Stealth mode off (optional but recommended)"
fi

# --- SSH ---
SSH_RUNNING=$(launchctl list 2>/dev/null | grep -c "com.openssh.sshd" || true)
if [[ "$SSH_RUNNING" -gt 0 ]]; then
  warn "SSH daemon running — ensure key-only auth if intentional"
  # Check PasswordAuthentication
  PW_AUTH=$(grep -E "^PasswordAuthentication" /etc/ssh/sshd_config 2>/dev/null || echo "not set")
  if echo "$PW_AUTH" | grep -qi "no"; then
    pass "SSH: PasswordAuthentication=no"
  else
    warn "SSH: PasswordAuthentication not explicitly disabled"
  fi
else
  pass "SSH daemon not running"
fi

# --- Open ports ---
LISTEN_EXTERNAL=$(lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null | grep -v "127.0.0.1\|::1\|\[::1\]" | grep -v "^COMMAND" || true)
if [[ -z "$LISTEN_EXTERNAL" ]]; then
  pass "No externally-listening TCP ports detected"
else
  PORT_COUNT=$(echo "$LISTEN_EXTERNAL" | wc -l | tr -d ' ')
  warn "External TCP listeners: ${PORT_COUNT} ports (check logs for details)"
  log "External listeners:\n$LISTEN_EXTERNAL"
fi

# --- Docker ---
if command -v docker &>/dev/null; then
  DOCKER_RUNNING=$(docker ps -q 2>/dev/null | wc -l | tr -d ' ')
  if [[ "$DOCKER_RUNNING" -gt 0 ]]; then
    warn "Docker: $DOCKER_RUNNING container(s) running — verify exposure"
  else
    pass "Docker installed, no containers running"
  fi
else
  pass "Docker not installed"
fi

# --- OpenClaw security audit ---
OC_AUDIT=$(openclaw security audit 2>&1 || true)
if echo "$OC_AUDIT" | grep -qi "FAIL\|error\|critical"; then
  fail "openclaw security audit: issues found (check logs)"
  log "OC audit output: $OC_AUDIT"
else
  pass "openclaw security audit: clean"
fi

# --- FileVault ---
FV=$(fdesetup status 2>/dev/null || echo "unknown")
if echo "$FV" | grep -q "On"; then
  pass "FileVault: enabled"
else
  warn "FileVault: off — disk encryption recommended"
fi

# --- Summary ---
log "audit complete — ${#ISSUES[@]} issue(s): ${ISSUES[*]:-none}"

echo ""
echo "=== Security Audit: $TS ==="
for LINE in "${SUMMARY[@]}"; do echo "  $LINE"; done
echo ""

if [[ ${#ISSUES[@]} -gt 0 ]]; then
  echo "Issues found: ${#ISSUES[@]}. Run: cat $LOG_FILE"
  exit 1
else
  echo "All checks passed."
  exit 0
fi
