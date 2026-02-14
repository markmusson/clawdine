#!/usr/bin/env bash
# ClawdSure vuln database helper
# Usage:
#   vuln-db.sh list [severity] [status]    — list vulns, optional filters
#   vuln-db.sh search <query>              — full-text search
#   vuln-db.sh add <json>                  — insert/update from JSON
#   vuln-db.sh stats                       — summary counts
#   vuln-db.sh unpatched                   — show unpatched vulns
#   vuln-db.sh export                      — dump as JSON array
set -euo pipefail

DB="${CLAWDSURE_VULN_DB:-$HOME/.openclaw/workspace/.clawdsure/vulns/vulns.db}"

case "${1:-list}" in
  list)
    severity="${2:-}"
    status="${3:-}"
    query="SELECT id, severity, title, status, discovered FROM vulns WHERE 1=1"
    [ -n "$severity" ] && query="$query AND severity='$severity'"
    [ -n "$status" ] && query="$query AND status='$status'"
    query="$query ORDER BY discovered DESC, severity"
    sqlite3 -header -column "$DB" "$query"
    ;;
  search)
    sqlite3 -header -column "$DB" \
      "SELECT v.id, v.severity, v.title, v.status, v.discovered FROM vulns_fts f JOIN vulns v ON f.rowid = v.rowid WHERE vulns_fts MATCH '${2}' ORDER BY v.discovered DESC"
    ;;
  add)
    # Expects JSON: {"id":"...","severity":"...","title":"...","status":"...","discovered":"...","source":"...","notes":"..."}
    json="${2}"
    id=$(echo "$json" | jq -r '.id')
    sev=$(echo "$json" | jq -r '.severity')
    title=$(echo "$json" | jq -r '.title')
    status=$(echo "$json" | jq -r '.status')
    disc=$(echo "$json" | jq -r '.discovered')
    src=$(echo "$json" | jq -r '.source // ""')
    notes=$(echo "$json" | jq -r '.notes // ""')
    sqlite3 "$DB" "INSERT INTO vulns (id, severity, title, status, discovered, source, notes) VALUES ('$id','$sev','$title','$status','$disc','$src','$notes') ON CONFLICT(id) DO UPDATE SET severity=excluded.severity, title=excluded.title, status=excluded.status, updated=CURRENT_DATE, source=excluded.source, notes=excluded.notes;"
    echo "✅ $id upserted"
    ;;
  stats)
    sqlite3 -header -column "$DB" \
      "SELECT severity, status, count(*) as count FROM vulns GROUP BY severity, status ORDER BY CASE severity WHEN 'critical' THEN 1 WHEN 'high' THEN 2 WHEN 'medium' THEN 3 WHEN 'low' THEN 4 ELSE 5 END"
    ;;
  unpatched)
    sqlite3 -header -column "$DB" \
      "SELECT id, severity, title, discovered FROM vulns WHERE status IN ('unpatched','investigating') ORDER BY CASE severity WHEN 'critical' THEN 1 WHEN 'high' THEN 2 WHEN 'medium' THEN 3 ELSE 4 END"
    ;;
  export)
    sqlite3 "$DB" "SELECT json_group_array(json_object('id',id,'severity',severity,'title',title,'status',status,'discovered',discovered,'source',source,'notes',notes)) FROM vulns"
    ;;
  *)
    echo "Usage: vuln-db.sh {list|search|add|stats|unpatched|export} [args]"
    exit 1
    ;;
esac
