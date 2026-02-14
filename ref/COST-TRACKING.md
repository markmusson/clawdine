# Cost Tracking

## How to Check
```bash
openclaw gateway usage-cost --days 7 --json
```

## Baseline (Feb 6-12, 2026)
- 7-day total: $499.88
- Peak day: $120.03 (Feb 7)
- Cache writes: 66% of total cost ($329)
- Output tokens: 5% of total cost ($25)
- Cache reads: 29% of total cost ($146)

## Optimizations Applied (Feb 11-12)
- `cacheRetention: "long"` (1hr vs 5min)
- Heartbeat every 55min (keeps cache warm)
- Context pruning TTL 55min
- Trimmed root context files
- Feb 12 tracking ~$40 (vs $120 peak) — 3x improvement

## Cost Levers
1. **Cache writes** — biggest cost. Minimize by keeping context stable (fewer file changes per session)
2. **Model routing** — Haiku for cron jobs, Sonnet for moderate tasks, Opus for complex only
3. **Context size** — fewer root files = smaller cache writes per turn
4. **Session length** — longer sessions amortize cache cost over more turns
5. **Sub-agent model** — always Haiku unless task requires more

## Monitoring
- Morning brief includes daily cost
- Weekly cost report (Sunday)
- Alert if daily cost > $80

---

*Updated: 2026-02-12*
