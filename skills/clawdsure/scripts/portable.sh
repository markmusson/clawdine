#!/usr/bin/env bash
# ClawdSure portable helpers — works on macOS, Linux, WSL

portable_sha256() {
  if [ $# -eq 0 ] || [ "$1" = "-" ]; then
    # stdin mode
    if command -v sha256sum >/dev/null 2>&1; then
      sha256sum | cut -c1-64
    elif command -v shasum >/dev/null 2>&1; then
      shasum -a 256 | cut -c1-64
    else
      openssl dgst -sha256 -r | cut -c1-64
    fi
  else
    # file mode
    if command -v sha256sum >/dev/null 2>&1; then
      sha256sum "$1" | cut -c1-64
    elif command -v shasum >/dev/null 2>&1; then
      shasum -a 256 "$1" | cut -c1-64
    else
      openssl dgst -sha256 "$1" | awk '{print $NF}'
    fi
  fi
}

portable_epoch() {
  local ts="$1"
  if date -d "$ts" +%s 2>/dev/null; then
    return
  elif command -v gdate >/dev/null 2>&1; then
    gdate -d "$ts" +%s 2>/dev/null && return
  fi
  # macOS fallback
  date -j -f "%Y-%m-%dT%H:%M:%SZ" "$ts" +%s 2>/dev/null ||
    python3 -c "from datetime import datetime; print(int(datetime.strptime('$ts','%Y-%m-%dT%H:%M:%SZ').timestamp()))" 2>/dev/null ||
    echo "0"
}

portable_base64_decode() {
  base64 -d 2>/dev/null || base64 -D 2>/dev/null
}

# Machine ID: stable across reboots, unique per machine
portable_machine_id() {
  local raw=""
  # macOS: hardware UUID
  if command -v system_profiler >/dev/null 2>&1; then
    raw=$(system_profiler SPHardwareDataType 2>/dev/null | grep "Hardware UUID" | awk '{print $NF}')
  fi
  # Linux: machine-id
  if [ -z "$raw" ] && [ -f /etc/machine-id ]; then
    raw=$(cat /etc/machine-id)
  fi
  # Linux fallback: product_uuid (needs root)
  if [ -z "$raw" ] && [ -f /sys/class/dmi/id/product_uuid ]; then
    raw=$(cat /sys/class/dmi/id/product_uuid 2>/dev/null || true)
  fi
  # Last resort: hostname + kernel
  if [ -z "$raw" ]; then
    raw="$(hostname)-$(uname -s)-$(uname -m)"
  fi
  echo -n "$raw" | portable_sha256 -
}

check_deps() {
  local missing=""
  for cmd in openssl jq curl; do
    command -v "$cmd" >/dev/null 2>&1 || missing="$missing $cmd"
  done
  if [ -n "$missing" ]; then
    echo "❌ Missing:$missing"
    echo "   brew install$missing / apt install$missing"
    exit 1
  fi
}
