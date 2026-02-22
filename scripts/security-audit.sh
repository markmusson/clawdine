#!/usr/bin/env bash
# security-audit.sh — daily macOS/OpenClaw security check
# Only flags genuine issues. Known-good operational choices are suppressed.
# Exits 1 if any WARN/FAIL found (triggers Telegram notify from cron agent).

set -uo pipefail

LOG_DIR="$HOME/.openclaw/workspace/logs"
LOG_FILE="$LOG_DIR/security-audit.log"
mkdir -p "$LOG_DIR"

TS=$(date '+%Y-%m-%d %H:%M:%S')
ISSUES=()
SUMMARY=()

log()  { echo "[$TS] $*" >> "$LOG_FILE"; }
pass() { SUMMARY+=("✅ $1"); log "PASS: $1"; }
warn() { SUMMARY+=("⚠️  $1"); ISSUES+=("$1"); log "WARN: $1"; }
fail() { SUMMARY+=("❌ $1"); ISSUES+=("$1"); log "FAIL: $1"; }
info() { SUMMARY+=("ℹ️  $1"); log "INFO: $1"; }

log "security-audit starting"

# --- Firewall ---
FW=$(/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate 2>/dev/null || echo "unknown")
if echo "$FW" | grep -q "enabled"; then
  pass "Firewall enabled"
else
  fail "Firewall DISABLED — run: sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on"
fi

# Stealth mode — informational only, not a hard requirement
STEALTH=$(/usr/libexec/ApplicationFirewall/socketfilterfw --getstealthmode 2>/dev/null || echo "unknown")
if echo "$STEALTH" | grep -q "enabled"; then
  pass "Stealth mode enabled"
else
  info "Stealth mode off (optional)"
fi

# --- SSH ---
SSH_RUNNING=$(launchctl list 2>/dev/null | grep -c "com.openssh.sshd" || true)
if [[ "$SSH_RUNNING" -gt 0 ]]; then
  PW_AUTH=$(grep -E "^PasswordAuthentication" /etc/ssh/sshd_config 2>/dev/null || echo "not set")
  if echo "$PW_AUTH" | grep -qi "no"; then
    pass "SSH: running, PasswordAuthentication=no"
  else
    warn "SSH: running with password auth not explicitly disabled"
  fi
else
  pass "SSH daemon not running"
fi

# --- Open ports --- skip known-good OpenClaw gateway port 18789
LISTEN_EXTERNAL=$(lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null \
  | grep -v "127.0.0.1\|::1\|\[::1\]\|:18789" \
  | grep -v "^COMMAND" || true)
if [[ -z "$LISTEN_EXTERNAL" ]]; then
  pass "No unexpected externally-listening TCP ports"
else
  PORT_COUNT=$(echo "$LISTEN_EXTERNAL" | wc -l | tr -d ' ')
  warn "Unexpected external TCP listeners: ${PORT_COUNT} (check logs)"
  log "External listeners: $LISTEN_EXTERNAL"
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

# --- OpenClaw security audit --- suppress known-harmless warnings
OC_AUDIT=$(openclaw security audit 2>&1 || true)
REAL_ISSUES=$(echo "$OC_AUDIT" | grep -iE "FAIL|critical" \
  | grep -v "reverse.proxy\|haiku\|model.tier\|untrusted.header\|0 critical\|· [0-9]* critical" || true)
if [[ -n "$REAL_ISSUES" ]]; then
  fail "openclaw security audit: $REAL_ISSUES"
  log "OC audit output: $OC_AUDIT"
else
  pass "openclaw security audit: clean"
fi

# --- FileVault --- genuine risk if off on a laptop
FV=$(fdesetup status 2>/dev/null || echo "unknown")
if echo "$FV" | grep -q "On"; then
  pass "FileVault: enabled"
else
  warn "FileVault: off — enable disk encryption (System Settings → Privacy & Security)"
fi

# --- Sandbox mode --- informational only, known operational choice
SANDBOX=$(openclaw config get sandbox.mode 2>/dev/null || echo "unknown")
if echo "$SANDBOX" | grep -qi "disabled\|full"; then
  info "Sandbox disabled (intentional — full host access enabled)"
else
  pass "Sandbox: $SANDBOX"
fi

# --- Summary ---
log "audit complete — ${#ISSUES[@]} issue(s): ${ISSUES[*]:-none}"

echo ""
echo "=== Security Audit: $TS ==="
for LINE in "${SUMMARY[@]}"; do echo "  $LINE"; done
echo ""

if [[ ${#ISSUES[@]} -gt 0 ]]; then
  echo "Issues found: ${#ISSUES[@]}"
  exit 1
else
  echo "All checks passed."
  exit 0
fi
