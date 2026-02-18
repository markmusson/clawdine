# Codex Task: OpenClaw Attestation Integration Analysis

## Run from
`~/.openclaw/workspace/openclaw-src`

## Command
```
codex exec --full-auto "< paste prompt below >"
```

---

## Prompt

You are analyzing the OpenClaw codebase to find the best path to bake cryptographic attestation into the platform natively.

**CONTEXT:**
Read VISION.md first. Key constraints: security is top priority, new features should ship as plugins unless there's a strong security reason to go into core, memory is a special plugin slot.

**WHAT ATTESTATION IS:**
A daily hash chain — machine fingerprint + installed skills + config + firewall state — signed with ECDSA, chained to the previous day's hash, pinned to IPFS. Think telematics black box for an AI agent. If anything changes unexpectedly, the chain breaks. Goal: cryptographic proof that an agent has been behaving and hasn't been silently compromised. This is the foundation of ClawdSure (causal.insure) — an insurance product for AI agents.

**YOUR TASK:**
1. Read VISION.md and SECURITY.md — understand contribution rules and where security features land
2. Explore the plugin/hook/skill architecture (docs/tools/plugin.md, hooks/, skills/)
3. Find where machine fingerprinting, config hashing, and skill integrity checks would naturally plug in
4. Look at how existing security hooks work (search for any audit/integrity touchpoints)
5. Identify the BEST path for attestation: core security module, internal hook, plugin, or skill — with reasoning against VISION.md constraints
6. Check if any existing integrity/audit touchpoints already exist in the codebase
7. Produce a SHORT structured report covering:
   - Best insertion point and why
   - What already exists that we can hook into
   - What needs building
   - Core vs plugin recommendation per VISION.md rules

**Save output to:**
`/Users/clawdine/.openclaw/workspace/projects/clawdsure-attestation/OPENCLAW-INTEGRATION-ANALYSIS.md`

When completely finished, run:
`openclaw system event --text "Done: OpenClaw attestation integration analysis complete" --mode now`
