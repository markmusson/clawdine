# Voice Agent — Clawdine Calls People

## The Vision
WhatsApp voice calls, Boardy-style. Mark calls me, I call David, full conversations with memory and context.

## Architecture
```
WhatsApp/Phone → Twilio SIP → Vapi (orchestration) → OpenClaw /v1/chat/completions
                                 ↓                         ↓
                            STT + TTS              Brain + Memory + Tools
                         (Deepgram/11Labs)        (Haiku for speed)
```

## Stack Components

### 1. Twilio ($)
- Phone number: ~$1/month
- Per-minute voice: ~$0.015/min
- WhatsApp Business API: requires Meta business verification (1-2 weeks)
- SIP trunking to Vapi

### 2. Vapi ($)
- Platform orchestration: $0.05/min
- Handles: call state, STT↔LLM↔TTS pipeline, real-time streaming
- Bring your own keys (STT, TTS, LLM)
- $10 free credit to start
- Near-zero latency when configured right

### 3. STT — Deepgram or Whisper
- Deepgram: ~$0.01-0.05/min (real-time streaming, fastest)
- Whisper API: ~$0.006/min (batch, too slow for live)

### 4. TTS — ElevenLabs (we already have this via sag skill)
- ~$0.05-0.08/min for premium voices
- We already pay for this

### 5. OpenClaw
- Expose /v1/chat/completions via Tailscale funnel or ngrok
- Voice-specific agent: `thinkingDefault: "off"`, Haiku for speed
- Sub-2 second latency (proven in Discussion #10588)
- Transcript → memory pipeline (already works)

## Cost Per Minute (estimated)
| Component | $/min |
|-----------|-------|
| Vapi orchestration | $0.05 |
| Twilio telephony | $0.015 |
| Deepgram STT | $0.03 |
| ElevenLabs TTS | $0.06 |
| Haiku LLM | ~$0.01 |
| **Total** | **~$0.17/min** |

A 30-minute interview with David: ~$5. Cheap.

## Setup Steps

### Phase 1: Proof of Concept (1-2 days)
1. [ ] Sign up for Vapi ($10 free credit)
2. [ ] Sign up for Twilio (if not already)
3. [ ] Get a Twilio phone number
4. [ ] Create OpenClaw voice agent (id: "voice", Haiku, thinking: off)
5. [ ] Expose OpenClaw API (ngrok or Tailscale funnel)
6. [ ] Configure Vapi: Twilio SIP → Vapi → OpenClaw endpoint
7. [ ] Test: phone call to the Twilio number, talk to Clawdine
8. [ ] Verify transcript lands in memory

### Phase 2: WhatsApp (1-2 weeks)
1. [ ] Apply for WhatsApp Business API via Twilio
2. [ ] Meta business verification (the bottleneck)
3. [ ] Configure WhatsApp voice channel in Twilio
4. [ ] Test: WhatsApp voice call to Clawdine

### Phase 3: Outbound Calls (after Phase 1)
1. [ ] Vapi outbound call API — Clawdine initiates calls
2. [ ] Interview flow: structured questions + freeform
3. [ ] Post-call: transcript → extract → context graph
4. [ ] Test: Clawdine calls David, interviews him about Brandy

## Blockers
- **WhatsApp Business API approval** — 1-2 weeks, requires Meta verification
- **OpenClaw exposure** — need stable public URL (Tailscale funnel preferred over ngrok)
- **Per-agent thinkingDefault** — PR exists (Discussion #10588), may need to apply patch

## Alternatives to Vapi
- **Retell AI** — simpler, $0.07/min all-in, but less configurable
- **LiveKit** — open source, self-hosted, more work but no per-minute platform fee
- **Deepgram Voice Agent API** — direct, used in the OpenClaw discussion

## Notes
- Boardy uses regular phone calls, not WhatsApp voice specifically
- The memory/context graph scaling problem is real but separate
- Peter Yang (@peteryang) confirmed near-zero latency with Vapi
