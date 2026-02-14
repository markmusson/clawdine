# ClawdSure Design Doc: Relay API

**This is a design document, not runtime instructions.**

Base URL: `https://api.clawdsure.io/v1` (production, future)  
Local dev: `http://localhost:8420/v1`

## Authentication

Agents authenticate via ECDSA signatures. No API keys needed.
- Sign the request payload with agent's private key
- Include `X-Agent-ID` and `X-Agent-Signature` headers

## Endpoints

### POST /v1/enroll
Register a new agent.

**Request:**
```json
{
  "agent_id": "CLWD-FFF4D493",
  "public_key_pem": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----",
  "genesis_attestation": { "v": 1, "seq": 1, "prev": "genesis", ... }
}
```

**Response:** 
```json
{
  "agent_id": "CLWD-FFF4D493",
  "enrolled_at": "2026-02-08T10:00:00Z",
  "status": "active"
}
```

### POST /v1/attestation
Submit a signed attestation. Called by `attest.sh` via `publish.sh`.

**Request:**
```json
{
  "agent_id": "CLWD-FFF4D493",
  "attestation": {
    "v": 1,
    "seq": 5,
    "prev": "hash...",
    "ts": "...",
    "result": "PASS",
    "audit_native": "sha256...",
    "audit_machine": "sha256...",
    "sig": "..."
  }
}
```

**Headers:** 
- `X-Agent-ID: CLWD-FFF4D493`
- `X-Agent-Signature: base64-signature-of-request-body`

**Response:** 
```json
{
  "received": true,
  "seq": 5,
  "chain_status": "valid"
}
```

**Validation:**
- Agent must be enrolled
- Signature valid against stored public key
- `prev` matches hash of server's last stored attestation
- `seq` is consecutive
- Timestamp within acceptable bounds

### GET /v1/agent/{agent_id}/chain
Full attestation history for an agent.

**Params:** `?limit=100&offset=0`

**Response:** 
```json
{
  "agent_id": "CLWD-FFF4D493",
  "chain": [
    {"v": 1, "seq": 1, ...},
    {"v": 1, "seq": 2, ...}
  ],
  "total": 42,
  "chain_status": "valid"
}
```

### GET /v1/agent/{agent_id}/status
Agent health summary.

**Response:**
```json
{
  "agent_id": "CLWD-FFF4D493",
  "chain_length": 42,
  "last_attestation": {
    "seq": 42,
    "ts": "2026-03-15T09:00:00Z",
    "result": "PASS"
  },
  "gap_hours": 23.5,
  "chain_status": "valid",
  "coverage_active": true
}
```

### POST /v1/manifest/generate
Generate daily manifest (internal/cron).

**Response:**
```json
{
  "date": "2026-02-07",
  "merkle_root": "sha256...",
  "agent_count": 42,
  "attestation_count": 38,
  "entries": [
    {
      "agent_id": "CLWD-FFF4D493",
      "seq": 5,
      "result": "PASS",
      "ts": "..."
    }
  ]
}
```

### GET /v1/manifest/{date}
Retrieve a daily manifest.

**Response:** Same as generate, plus:
```json
{
  "cid": "QmXXXXXXXXXXXXXXXX",
  "pinned_at": "2026-02-08T00:05:00Z"
}
```

### GET /v1/health
Service health.

**Response:** 
```json
{
  "status": "ok",
  "version": "0.1.0",
  "agents_enrolled": 127,
  "attestations_total": 5234
}
```

## Architecture

```
Agents (many)              ClawdSure API              IPFS/Storage
───────────               ─────────────              ────────────
attest.sh         →     POST /attestation    →     Daily manifest
  signs locally           validates + stores          aggregation
  chain.jsonl             SQLite                      merkle tree
                                                      (future)
```

Agents maintain local chains. The relay:
1. Validates attestations
2. Stores backup copy
3. Provides public verification endpoint
4. (Future) Aggregates into daily merkle tree for IPFS pinning

## Environment Variables (API server)

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `data/clawdsure.db` | SQLite path |
| `PORT` | `8420` | Server port |
| `IPFS_PIN_ENABLED` | `false` | Enable IPFS pinning of manifests |
| `PINATA_JWT` | (none) | Pinata JWT for manifest pinning |

## Rate Limiting

- 10 attestations per agent per hour (prevents spam)
- 1 enrollment per agent per 24h (prevents re-enrollment attacks)
- Global: 1000 req/min per IP

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Invalid attestation format |
| 401 | Signature verification failed |
| 409 | Sequence number conflict |
| 429 | Rate limit exceeded |
| 500 | Server error |
