# HEARTBEAT.md

Heartbeats are **enabled** (every 55min) for Anthropic prompt cache warming.

## Purpose
Keep the prompt cache alive across idle gaps. The heartbeat is silent — if nothing needs attention, reply HEARTBEAT_OK. This avoids expensive cache-write costs on the next real message.

## Cron Jobs (isolated, Haiku)
- `clawdsure-daily-attest` — 9:30am daily — security attestation + full report to Telegram
- `vuln-scan-daily` — 10am daily — vulnerability scan
- `gap-alert-check` — 9am, 12pm, 3pm, 6pm — weather gap alerts
- `portfolio-morning` / `portfolio-lunch` / `portfolio-evening` — paper trading reports

## LaunchD (scripts, zero tokens)
- `com.clawdine.weather-tracker` — 9am daily — price data collection
- `com.clawdine.weather-forecast-collector` — forecast data
- `com.clawdine.weather-signal-gen` — signal generation
- `com.clawdine.weather-signal-alert` — signal alerts
- `com.clawdine.weather-paper-trader` — paper trading
- `com.clawdine.weather-live-trader` — live trading (currently failing, geo-restriction)
- `com.clawdine.kalshi-btc-monitor` — every 5min — BTC paper trading
- `com.clawdine.btc-scanners` — 6am/12pm/6pm — BTC intel scanners
- `com.clawdine.btc-report` — 8am daily — BTC email report
- `com.clawdine.context-alert` — every 30min — context budget alert
- `com.clawdine.daily-status-report` — 8pm daily — status report via Telegram
