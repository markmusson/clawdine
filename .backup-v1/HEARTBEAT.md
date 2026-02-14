# HEARTBEAT.md

Heartbeats are **disabled**. All recurring tasks run via cron or launchd (zero tokens).

## Cron Jobs (isolated, Haiku)
- `gap-alert-check` — 9am, 12pm, 3pm, 6pm — weather gap alerts
- `clawdsure-daily-attest` — 9:30am daily — security attestation + Telegram notify

## LaunchD (scripts, zero tokens)
- `com.clawdine.weather-tracker` — 9am daily — price data collection
- `com.clawdine.context-alert` — every 30min — context budget alert (≥50% → Telegram)

## LaunchD (scripts, zero tokens) — continued
- `com.clawdine.kalshi-btc-monitor` — every 5min — BTC 15-min paper trading monitor
- `com.clawdine.daily-status-report` — 8pm daily — cron + launchd status report via Telegram

## Removed
- `com.clawdsure.daily` — removed (duplicate of cron job)
- Heartbeat config — removed from openclaw.json
