#!/usr/bin/env bash
# ClawdSure machine audit - lean cross-platform security checks
# Output: JSON to stdout (not file)
# Exit 0 always (findings are data, not script failures)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/portable.sh"

STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
CONFIG_PATH="${OPENCLAW_CONFIG_PATH:-$STATE_DIR/openclaw.json}"
WORKSPACE_DIR="${OPENCLAW_WORKSPACE_DIR:-${WORKSPACE:-$HOME/.openclaw/workspace}}"

# Track check results (JSON array, compatible with old bash)
CHECKS_JSON="{"
CHECKS_FIRST=true
OK_COUNT=0
WARN_COUNT=0
FAIL_COUNT=0

# Redact secrets from text (macOS sed compatible)
redact_text() {
  local text="$1"
  # Redact bearer tokens
  text=$(echo "$text" | sed -E 's/([Bb]earer[[:space:]]+)[A-Za-z0-9._~+/=-]{8,}/\1****REDACTED****/g')
  # Redact key=value patterns
  text=$(echo "$text" | sed -E 's/([Tt]oken|[Pp]assword|[Ss]ecret|[Aa]pi[_-]?[Kk]ey|[Cc]ookie|[Aa]uth)([^=:]*[:=][[:space:]]*)[A-Za-z0-9._~+/=-]{6,}/\1\2****REDACTED****/g')
  # Skip problematic JSON regex on macOS sed
  echo "$text"
}

# Add check result
add_check() {
  local id="$1" status="$2" detail="$3"
  detail=$(redact_text "$detail")
  
  if [ "$CHECKS_FIRST" = true ]; then
    CHECKS_FIRST=false
  else
    CHECKS_JSON="${CHECKS_JSON},"
  fi
  
  local check_obj=$(jq -nc --arg s "$status" --arg d "$detail" '{status:$s, detail:$d}')
  CHECKS_JSON="${CHECKS_JSON}\"${id}\":${check_obj}"
  
  case "$status" in
    ok) OK_COUNT=$((OK_COUNT + 1)) ;;
    warn) WARN_COUNT=$((WARN_COUNT + 1)) ;;
    fail) FAIL_COUNT=$((FAIL_COUNT + 1)) ;;
  esac
}

has_cmd() { command -v "$1" >/dev/null 2>&1; }

# Filesystem checks
check_filesystem() {
  # State dir permissions
  if [ -d "$STATE_DIR" ]; then
    if [ -w "$STATE_DIR" ] && [ ! -L "$STATE_DIR" ]; then
      # Check if world-writable
      if has_cmd stat; then
        perms=$(stat -c '%a' "$STATE_DIR" 2>/dev/null || stat -f '%Lp' "$STATE_DIR" 2>/dev/null || echo "")
        if [[ "$perms" =~ 2$ ]]; then
          add_check "fs.state_dir_perms" "fail" "State dir world-writable: $STATE_DIR"
        else
          add_check "fs.state_dir_perms" "ok" "State dir permissions OK"
        fi
      else
        add_check "fs.state_dir_perms" "ok" "State dir exists, stat unavailable"
      fi
    elif [ -L "$STATE_DIR" ]; then
      add_check "fs.state_dir_perms" "warn" "State dir is symlink: $STATE_DIR"
    else
      add_check "fs.state_dir_perms" "fail" "State dir not writable"
    fi
  else
    add_check "fs.state_dir_perms" "fail" "State dir missing: $STATE_DIR"
  fi

  # Config file permissions
  if [ -f "$CONFIG_PATH" ]; then
    if has_cmd stat; then
      perms=$(stat -c '%a' "$CONFIG_PATH" 2>/dev/null || stat -f '%Lp' "$CONFIG_PATH" 2>/dev/null || echo "")
      if [[ "$perms" =~ [2367]$ ]]; then
        add_check "fs.config_perms" "fail" "Config world-writable: $CONFIG_PATH"
      else
        add_check "fs.config_perms" "ok" "Config permissions OK"
      fi
    else
      add_check "fs.config_perms" "ok" "Config exists, stat unavailable"
    fi
  else
    add_check "fs.config_perms" "warn" "Config missing: $CONFIG_PATH"
  fi

  # Credentials dir permissions
  creds_dir="$STATE_DIR/credentials"
  if [ -d "$creds_dir" ]; then
    if has_cmd stat; then
      perms=$(stat -c '%a' "$creds_dir" 2>/dev/null || stat -f '%Lp' "$creds_dir" 2>/dev/null || echo "")
      if [[ "$perms" =~ 2$ ]]; then
        add_check "fs.credentials_perms" "fail" "Credentials dir world-writable"
      else
        add_check "fs.credentials_perms" "ok" "Credentials dir permissions OK"
      fi
    else
      add_check "fs.credentials_perms" "ok" "Credentials dir exists, stat unavailable"
    fi
  else
    add_check "fs.credentials_perms" "ok" "Credentials dir not present"
  fi

  # Synced folder detection (Dropbox, iCloud, etc.)
  case "$STATE_DIR" in
    *"/Dropbox/"*|*"/OneDrive/"*|*"/Google Drive/"*|*"/iCloud/"*|*"/Library/Mobile Documents/"*)
      add_check "fs.synced_folder" "warn" "State dir in synced folder (security risk)"
      ;;
    *)
      add_check "fs.synced_folder" "ok" "Not in synced folder"
      ;;
  esac

  # SUID/SGID files in state dir (suspicious)
  if [ -d "$STATE_DIR" ] && has_cmd find; then
    suid_files=$(find "$STATE_DIR" -xdev -type f \( -perm -4000 -o -perm -2000 \) -print 2>/dev/null | head -5)
    if [ -n "$suid_files" ]; then
      add_check "fs.suid_sgid" "warn" "SUID/SGID files found: $(echo "$suid_files" | tr '\n' ' ')"
    else
      add_check "fs.suid_sgid" "ok" "No SUID/SGID files"
    fi
  else
    add_check "fs.suid_sgid" "ok" "SUID check skipped"
  fi
}

# Network checks
check_network() {
  # Listening ports
  local listen_out=""
  if has_cmd ss; then
    listen_out=$(ss -tulpen 2>/dev/null | grep LISTEN | head -10 || true)
  elif has_cmd lsof; then
    listen_out=$(lsof -i -P -n 2>/dev/null | grep LISTEN | head -10 || true)
  elif has_cmd netstat; then
    listen_out=$(netstat -ano 2>/dev/null | grep LISTEN | head -10 || true)
  fi

  if [ -n "$listen_out" ]; then
    port_count=$(echo "$listen_out" | wc -l | tr -d ' ')
    add_check "net.listening_ports" "ok" "$port_count listening ports detected"
  else
    add_check "net.listening_ports" "ok" "No listening ports or tool unavailable"
  fi
}

# Firewall checks
check_firewall() {
  local fw_detected=false

  # macOS
  if [ -x /usr/libexec/ApplicationFirewall/socketfilterfw ]; then
    fw_state=$(/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate 2>/dev/null || echo "unknown")
    if [[ "$fw_state" =~ enabled|on ]]; then
      add_check "fw.macos" "ok" "macOS firewall enabled"
    else
      add_check "fw.macos" "warn" "macOS firewall not enabled"
    fi
    fw_detected=true
  fi

  # Linux: ufw
  if has_cmd ufw; then
    fw_state=$(ufw status 2>/dev/null | head -1 || echo "unknown")
    if [[ "$fw_state" =~ active ]]; then
      add_check "fw.ufw" "ok" "UFW firewall active"
    else
      add_check "fw.ufw" "warn" "UFW not active"
    fi
    fw_detected=true
  fi

  # Linux: firewalld
  if has_cmd firewall-cmd; then
    fw_state=$(firewall-cmd --state 2>/dev/null || echo "not running")
    if [[ "$fw_state" == "running" ]]; then
      add_check "fw.firewalld" "ok" "Firewalld running"
    else
      add_check "fw.firewalld" "warn" "Firewalld not running"
    fi
    fw_detected=true
  fi

  # Linux: iptables/nftables
  if has_cmd iptables; then
    rule_count=$(iptables -S 2>/dev/null | wc -l | tr -d ' ' || echo "0")
    if [ "${rule_count:-0}" -gt 5 ]; then
      add_check "fw.iptables" "ok" "Iptables rules present"
      fw_detected=true
    fi
  fi

  if has_cmd nft; then
    rule_count=$(nft list ruleset 2>/dev/null | wc -l | tr -d ' ' || echo "0")
    if [ "${rule_count:-0}" -gt 5 ]; then
      add_check "fw.nftables" "ok" "Nftables rules present"
      fw_detected=true
    fi
  fi

  # Windows
  if has_cmd netsh; then
    fw_state=$(netsh advfirewall show allprofiles 2>/dev/null | grep State || echo "")
    if [[ "$fw_state" =~ ON ]]; then
      add_check "fw.windows" "ok" "Windows firewall enabled"
    else
      add_check "fw.windows" "warn" "Windows firewall not enabled"
    fi
    fw_detected=true
  fi

  if [ "$fw_detected" = false ]; then
    add_check "fw.none" "warn" "No firewall detected"
  fi
}

# Skills inventory and pattern scan
check_skills() {
  local suspicious_pattern='(curl.*\||wget.*\||bash.*-c|sh.*-c|chmod \+x|eval |base64.*-d|Invoke-WebRequest|iwr|irm)'
  local total_skills=0
  local suspicious_matches=""

  # Scan workspace skills
  if [ -d "$WORKSPACE_DIR/skills" ]; then
    total_skills=$(find "$WORKSPACE_DIR/skills" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
    
    if has_cmd rg; then
      suspicious_matches=$(rg -n --no-messages -S "$suspicious_pattern" "$WORKSPACE_DIR/skills" 2>/dev/null | head -10 || true)
    elif has_cmd grep; then
      suspicious_matches=$(grep -rn -E "$suspicious_pattern" "$WORKSPACE_DIR/skills" 2>/dev/null | head -10 || true)
    fi
  fi

  # Scan state skills
  if [ -d "$STATE_DIR/skills" ]; then
    state_skills=$(find "$STATE_DIR/skills" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
    total_skills=$((total_skills + state_skills))
    
    if has_cmd rg; then
      state_matches=$(rg -n --no-messages -S "$suspicious_pattern" "$STATE_DIR/skills" 2>/dev/null | head -10 || true)
      suspicious_matches="${suspicious_matches}${state_matches}"
    elif has_cmd grep; then
      state_matches=$(grep -rn -E "$suspicious_pattern" "$STATE_DIR/skills" 2>/dev/null | head -10 || true)
      suspicious_matches="${suspicious_matches}${state_matches}"
    fi
  fi

  add_check "skills.inventory" "ok" "${total_skills} skills installed"

  if [ -n "$suspicious_matches" ]; then
    match_count=$(echo "$suspicious_matches" | wc -l | tr -d ' ')
    add_check "skills.pattern_scan" "warn" "${match_count} suspicious patterns found (review needed)"
  else
    add_check "skills.pattern_scan" "ok" "No suspicious patterns detected"
  fi

  # Per-file content hashing — detects edits to existing skill files
  # This is the integrity layer: install is a declaration, edit is a material change
  local skill_hashes=""
  local skill_dirs="$WORKSPACE_DIR/skills $STATE_DIR/skills"
  for sdir in $skill_dirs; do
    if [ -d "$sdir" ]; then
      while IFS= read -r skill_dir; do
        local skill_name
        skill_name=$(basename "$skill_dir")
        # Hash all .md, .sh, .json, .py, .js, .ts files in the skill (sorted for determinism)
        local content_hash
        content_hash=$(find "$skill_dir" -type f \( -name '*.md' -o -name '*.sh' -o -name '*.json' -o -name '*.py' -o -name '*.js' -o -name '*.ts' \) 2>/dev/null | sort | xargs cat 2>/dev/null | portable_sha256 - || echo "empty")
        if [ -n "$skill_hashes" ]; then
          skill_hashes="${skill_hashes},\"${skill_name}\":\"${content_hash}\""
        else
          skill_hashes="\"${skill_name}\":\"${content_hash}\""
        fi
      done < <(find "$sdir" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sort)
    fi
  done
  add_check "skills.content_hashes" "ok" "{${skill_hashes}}"
}

# Operational coherence checks
check_operational() {
  if [ ! -f "$CONFIG_PATH" ]; then
    add_check "ops.model_allowlist" "warn" "Config missing, can't verify model allowlist"
    return
  fi

  if ! has_cmd jq; then
    add_check "ops.model_allowlist" "warn" "jq missing, can't verify model allowlist"
    return
  fi

  # Check model allowlist consistency
  local allowlist=$(jq -r '.agents.defaults.models // {} | keys[]' "$CONFIG_PATH" 2>/dev/null || echo "")
  local primary_model=$(jq -r '.agents.defaults.model.primary // .agents.defaults.model // empty' "$CONFIG_PATH" 2>/dev/null || echo "")
  local heartbeat_model=$(jq -r '.agents.defaults.heartbeat.model // empty' "$CONFIG_PATH" 2>/dev/null || echo "")
  local subagent_model=$(jq -r '.agents.defaults.subagents.model // empty' "$CONFIG_PATH" 2>/dev/null || echo "")

  local missing=""
  if [ -n "$primary_model" ] && [ -n "$allowlist" ]; then
    if ! echo "$allowlist" | grep -q "^${primary_model}$"; then
      missing="${missing}primary:${primary_model} "
    fi
  fi
  if [ -n "$heartbeat_model" ] && [ -n "$allowlist" ]; then
    if ! echo "$allowlist" | grep -q "^${heartbeat_model}$"; then
      missing="${missing}heartbeat:${heartbeat_model} "
    fi
  fi
  if [ -n "$subagent_model" ] && [ -n "$allowlist" ]; then
    if ! echo "$allowlist" | grep -q "^${subagent_model}$"; then
      missing="${missing}subagent:${subagent_model} "
    fi
  fi

  if [ -n "$missing" ]; then
    add_check "ops.model_allowlist" "warn" "Models not in allowlist: $missing"
  else
    add_check "ops.model_allowlist" "ok" "Model allowlist consistent"
  fi
}

# Sandbox and isolation checks (Harrison Chase Pattern 1 vs Pattern 2)
check_sandbox() {
  if [ ! -f "$CONFIG_PATH" ] || ! has_cmd jq; then
    add_check "sandbox.mode" "warn" "Config/jq missing, can't verify sandbox mode"
    return
  fi

  # Check sandbox mode
  local sandbox_mode=$(jq -r '.agents.defaults.sandbox.mode // "none"' "$CONFIG_PATH" 2>/dev/null || echo "none")
  
  case "$sandbox_mode" in
    all)
      add_check "sandbox.mode" "ok" "Sandbox: all tool execution isolated (Pattern 2)"
      ;;
    non-main)
      add_check "sandbox.mode" "ok" "Sandbox: non-main agents isolated (Pattern 2 partial)"
      ;;
    none|"")
      add_check "sandbox.mode" "warn" "Sandbox: disabled — agent runs with full host access (Pattern 1, max blast radius)"
      ;;
    *)
      add_check "sandbox.mode" "warn" "Sandbox mode unrecognized: $sandbox_mode"
      ;;
  esac

  # Check if Docker is available when sandbox is enabled
  if [ "$sandbox_mode" != "none" ] && [ "$sandbox_mode" != "" ]; then
    if has_cmd docker; then
      if docker info >/dev/null 2>&1; then
        add_check "sandbox.docker" "ok" "Docker available and running"
      else
        add_check "sandbox.docker" "warn" "Docker installed but not running — sandbox won't work"
      fi
    else
      add_check "sandbox.docker" "warn" "Docker not installed — sandbox configured but unavailable"
    fi
  fi

  # Check sandbox network isolation
  local sandbox_network=$(jq -r '.agents.defaults.sandbox.docker.network // "default"' "$CONFIG_PATH" 2>/dev/null || echo "default")
  if [ "$sandbox_mode" != "none" ] && [ "$sandbox_mode" != "" ]; then
    if [ "$sandbox_network" = "none" ]; then
      add_check "sandbox.network" "ok" "Sandbox network: none (fully isolated)"
    else
      add_check "sandbox.network" "warn" "Sandbox network: $sandbox_network (agent code can reach the internet)"
    fi
  fi

  # Check gateway bind address (network exposure)
  local bind_mode=$(jq -r '.gateway.bind // "loopback"' "$CONFIG_PATH" 2>/dev/null || echo "loopback")
  case "$bind_mode" in
    loopback|localhost|127.0.0.1)
      add_check "sandbox.gateway_bind" "ok" "Gateway bound to loopback only"
      ;;
    *)
      add_check "sandbox.gateway_bind" "fail" "Gateway bound to $bind_mode — exposed to network"
      ;;
  esac

  # Check elevated exec
  local elevated=$(jq -r '.tools.exec.elevated // false' "$CONFIG_PATH" 2>/dev/null || echo "false")
  if [ "$elevated" = "true" ]; then
    add_check "sandbox.elevated_exec" "warn" "Elevated (sudo) exec enabled — high privilege"
  else
    add_check "sandbox.elevated_exec" "ok" "Elevated exec disabled"
  fi
}

# ClawHub skill threat patterns (SKILL.md-only detection)
check_skill_threats() {
  local skill_dirs="$WORKSPACE_DIR/skills $STATE_DIR/skills"
  local skillmd_only_count=0
  local skillmd_only_list=""
  local external_url_count=0
  local config_mod_count=0

  for sdir in $skill_dirs; do
    if [ -d "$sdir" ]; then
      while IFS= read -r skill_dir; do
        local skill_name
        skill_name=$(basename "$skill_dir")
        
        # Count non-metadata files (exclude SKILL.md, _meta.json, .clawhub/)
        local code_files
        code_files=$(find "$skill_dir" -type f \
          -not -name "SKILL.md" -not -name "_meta.json" \
          -not -path "*/.clawhub/*" -not -name "*.md" \
          2>/dev/null | wc -l | tr -d ' ')
        
        if [ "$code_files" -eq 0 ] && [ -f "$skill_dir/SKILL.md" ]; then
          local skillmd_size
          skillmd_size=$(wc -c < "$skill_dir/SKILL.md" 2>/dev/null | tr -d ' ')
          # Flag SKILL.md-only skills, especially large ones (>3KB)
          if [ "${skillmd_size:-0}" -gt 3000 ]; then
            skillmd_only_count=$((skillmd_only_count + 1))
            skillmd_only_list="${skillmd_only_list} ${skill_name}(${skillmd_size}B)"
          fi
        fi

        # Check for external URL references in SKILL.md
        if [ -f "$skill_dir/SKILL.md" ]; then
          local ext_urls
          ext_urls=$(grep -cE 'https?://[^/]*(\.forum|\.xyz|\.tk|\.ml|\.ga|\.cf|openclawcli)' "$skill_dir/SKILL.md" 2>/dev/null | tr -d '[:space:]' || echo "0")
          if [ "${ext_urls:-0}" -gt 0 ]; then
            external_url_count=$((external_url_count + ext_urls))
          fi
          
          # Check for config modification instructions
          local config_refs
          config_refs=$(grep -cE '(openclaw\.json|config\.patch|config\.apply)' "$skill_dir/SKILL.md" 2>/dev/null | tr -d '[:space:]' || echo "0")
          if [ "${config_refs:-0}" -gt 0 ]; then
            config_mod_count=$((config_mod_count + config_refs))
          fi
        fi
      done < <(find "$sdir" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sort)
    fi
  done

  if [ "$skillmd_only_count" -gt 0 ]; then
    add_check "skills.prompt_only" "warn" "${skillmd_only_count} prompt-only skills (no code, large SKILL.md):${skillmd_only_list}"
  else
    add_check "skills.prompt_only" "ok" "No prompt-only skills detected"
  fi

  if [ "$external_url_count" -gt 0 ]; then
    add_check "skills.external_urls" "warn" "${external_url_count} suspicious external URL references in skills"
  else
    add_check "skills.external_urls" "ok" "No suspicious external URLs in skills"
  fi

  if [ "$config_mod_count" -gt 0 ]; then
    add_check "skills.config_mod" "warn" "${config_mod_count} config modification references in skills"
  else
    add_check "skills.config_mod" "ok" "No config modification instructions in skills"
  fi
}

# Main execution
main() {
  check_filesystem
  check_network
  check_firewall
  check_skills
  check_skill_threats
  check_sandbox
  check_operational

  # Close checks JSON object
  CHECKS_JSON="${CHECKS_JSON}}"

  # Build final JSON output
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  
  jq -nc \
    --arg ts "$timestamp" \
    --argjson checks "$CHECKS_JSON" \
    --argjson ok "$OK_COUNT" \
    --argjson warn "$WARN_COUNT" \
    --argjson fail "$FAIL_COUNT" \
    '{ts:$ts, checks:$checks, summary:{ok:$ok, warn:$warn, fail:$fail}}'
}

main
exit 0
