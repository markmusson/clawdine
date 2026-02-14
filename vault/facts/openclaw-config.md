---
title: OpenClaw config
date: '2026-02-14'
memoryType: fact
---
Model routing: primary → fallbacks. Context window: explicit 1M (default 200k). Cache-TTL pruning 55m. Compaction: safeguard mode. Heartbeat every 55m for Anthropic cache warming. Hybrid search: 0.7 vector / 0.3 BM25, candidateMultiplier 4. OpenAI embeddings, batch mode. Session memory experimental.
