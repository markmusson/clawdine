# The Harness Thesis
*Crystallised Feb 19, 2026*

## The Stack

Four layers. Everything else is disposable.

1. **Infra layer** — compute, networking, storage (AWS, GCP, NVIDIA)
2. **Model layer** — foundation models (Anthropic, OpenAI, Google)
3. **Harness layer** — the runtime: agent identity, tools, memory, context, persistence (OpenClaw, Claude Code)
4. **Knowledge layer** — proprietary data, domain expertise, accumulated intelligence

All workflows are disposable. Orchestration tools, no-code agents, LangChain, n8n — everything between layers gets commoditised or absorbed. The harness is the surviving substrate.

## Why Harness Wins

The harness is where the agent lives. It controls everything:
- What tools the agent can use
- What the agent remembers
- What credentials the agent holds
- What decisions the agent makes
- What the agent IS across sessions

Workflows are ephemeral. The harness is persistent. OpenClaw and Claude Code are early signals. The harness layer is where identity accumulates.

## Where ClawdSure Plays

If harness is the surviving substrate, harness trust is the only trust that matters.

- Can't insure workflows — disposable
- Can't insure models — Anthropic carries that risk  
- Can't insure infra — AWS does
- **Harness is the gap.** That's where the agent can be compromised. That's where real damage happens.

ClawdSure is attestation infrastructure for the harness layer — cryptographic proof that the harness hasn't been tampered with. The chain makes harness trustworthy enough to be a substrate at all. Insurance is what you build on top of that proof.

## The Pitch

**"We're not insuring AI. We're making harness infrastructure insurable. If harness wins, harness trust wins with it."**

## The Moat

This requires:
- Insurance domain expertise (built and sold an MGA to AON for £40m GWP)
- Harness-layer understanding (running OpenClaw, contributing to core)
- Actuarial data nobody else is collecting (attestation chain = proprietary incident dataset)

Most people have one of these. We have all three.
