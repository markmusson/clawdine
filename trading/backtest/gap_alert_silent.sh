#!/bin/bash
# Gap Alert + Paper Trader — Silent on no alerts
# Runs gap alert, feeds signals to paper trader, settles pending positions.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRADER="$(dirname "$SCRIPT_DIR")/weather_paper_trader.py"

# Run the full pipeline: gap alert → trade → settle
python3 "$TRADER" both 2>&1

# Check if any alerts were found (grep for the alert marker)
if python3 "$SCRIPT_DIR/gap_alert.py" 2>&1 | grep -q "🚨 ALERTS"; then
    exit 1  # Signal there's work to do
fi

exit 0
