# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

### RPC / Blockchain

All keys in macOS Keychain (account: clawdine):
- `alchemy-api-key` — Alchemy API key (ETH, Base, Solana)
- `quicknode-polygon` — Polygon RPC (for Polymarket on-chain)
- `quicknode-ethereum` — Ethereum mainnet RPC
- `quicknode-bsc` — Binance Smart Chain RPC
- `quicknode-avalanche` — Avalanche C-Chain RPC
- `quicknode-base` — Base mainnet RPC
- `quicknode-arbitrum` — Arbitrum mainnet RPC

Retrieve: `security find-generic-password -a clawdine -s "quicknode-polygon" -w`

### Alchemy Endpoints (public-facing)
- ETH mainnet: `https://eth-mainnet.g.alchemy.com/v2/{key}`
- Base mainnet: `https://base-mainnet.g.alchemy.com/v2/{key}`
- Solana mainnet: `https://solana-mainnet.g.alchemy.com/v2/{key}`

### summarize.sh (steipete)
- v0.11 — summarize any URL, YouTube, podcast, local file
- `summarize <url> --slides` — best way to consume YT/podcasts
- Can use Cursor for free tokens, Groq for fast TTS inference
- Powers OpenClaw's content summarization skill
- Chrome extension: chromewebstore.google.com/detail/summari…
- GitHub: github.com/steipete/summarize.sh
- Also `--slides` mode for visual summaries

Add whatever helps you do your job. This is your cheat sheet.
