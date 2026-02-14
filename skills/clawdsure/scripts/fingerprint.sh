#!/usr/bin/env bash
# ClawdSure machine fingerprint — two hashes that tell the whole story
#
# MACHINE HASH: "is this the same machine?" (stable, hardware-bound)
# CONFIG HASH:  "is it still configured securely?" (changes on config drift)
#
# Usage: source this, then call clawdsure_fingerprint or clawdsure_config_hash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/portable.sh"

# Machine fingerprint: hardware UUID + OS + arch
# Changes only if you move to a different machine
clawdsure_fingerprint() {
  local machine_id
  machine_id=$(portable_machine_id)
  echo "$machine_id"
}

# Config hash: security-relevant OpenClaw configuration
# Changes if auth, channels, exposure, or permissions change
clawdsure_config_hash() {
  local config_path="${1:-$HOME/.openclaw/openclaw.json}"
  
  if [ ! -f "$config_path" ]; then
    echo "no-config"
    return
  fi

  # Extract security-relevant fields only (deterministic order via jq)
  # This is what the oracle checks: did your security posture change?
  jq -Sc '{
    auth: (.auth // {}),
    gateway: {
      mode: (.gateway.mode // null),
      bind: (.gateway.bind // null),
      auth_mode: (.gateway.auth.mode // null),
      tailscale: (.gateway.tailscale.mode // null)
    },
    channels: ((.channels // {}) | to_entries | map({
      key: .key,
      value: {
        dmPolicy: .value.dmPolicy,
        groupPolicy: .value.groupPolicy,
        selfChatMode: .value.selfChatMode
      }
    }) | from_entries),
    browser: { headless: (.browser.headless // null) },
    elevated: (.tools.exec.elevated // null),
    sandbox: (.tools.exec.sandbox // null)
  }' "$config_path" 2>/dev/null | portable_sha256 -
}

# Full fingerprint record (JSON, for embedding in attestation)
clawdsure_fingerprint_record() {
  local config_path="${1:-$HOME/.openclaw/openclaw.json}"
  local machine_hash config_hash oc_version os_info arch
  
  machine_hash=$(clawdsure_fingerprint)
  config_hash=$(clawdsure_config_hash "$config_path")
  oc_version=$(openclaw --version 2>&1 | tail -1 || echo "unknown")
  os_info=$(uname -s)
  arch=$(uname -m)
  
  jq -nc \
    --arg mh "$machine_hash" \
    --arg ch "$config_hash" \
    --arg ov "$oc_version" \
    --arg os "$os_info" \
    --arg ar "$arch" \
    '{machine: $mh, config: $ch, openclaw: $ov, os: $os, arch: $ar}'
}

# If run directly, print the fingerprint record
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  check_deps
  clawdsure_fingerprint_record "$@"
fi
