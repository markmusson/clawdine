# ClawdSure MVP API

A prototype API server for receiving and aggregating agent attestations with cryptographic verification and daily manifest generation.

## Features

- **Agent Enrollment**: Register agents with ECDSA P-256 public keys
- **Attestation Chain**: Submit and verify cryptographically-signed attestations
- **Chain Integrity**: Automatic validation of sequence numbers and hash chains
- **Daily Manifests**: Generate merkle tree-based daily summaries
- **Health Monitoring**: Track agent status and chain health

## Quick Start

### Installation

```bash
cd /Users/clawdine/.openclaw/workspace/clawdsure-api/
pip install -r requirements.txt
```

### Run Server

```bash
uvicorn main:app --port 8420
```

The server will automatically create the SQLite database on first run at `data/clawdsure.db`.

### API Documentation

Once running, visit:
- Interactive docs: `http://localhost:8420/docs`
- ReDoc: `http://localhost:8420/redoc`

## API Endpoints

### Core Endpoints

#### `POST /v1/enroll`
Enroll a new agent with genesis attestation.

**Request:**
```json
{
  "agent_id": "clawdine-main",
  "fingerprint": "abc123...",
  "public_key_pem": "-----BEGIN PUBLIC KEY-----\n...",
  "genesis_attestation": {
    "seq": 0,
    "prev": "0000000000000000000000000000000000000000000000000000000000000000",
    "ts": 1735689600,
    "result": "pass",
    "critical": 0,
    "warn": 0,
    "info": 3,
    "version": "1.0.0",
    "findings": ["Agent enrolled", "Config validated"],
    "sig": "304502..."
  }
}
```

**Response:**
```json
{
  "agent_id": "clawdine-main",
  "enrolled_at": 1735689600,
  "status": "active"
}
```

#### `POST /v1/attestation`
Submit a new attestation.

**Request:**
```json
{
  "agent": {
    "id": "clawdine-main",
    "fingerprint": "abc123..."
  },
  "attestation": {
    "seq": 1,
    "prev": "7a8b9c...",
    "ts": 1735776000,
    "result": "pass",
    "critical": 0,
    "warn": 1,
    "info": 2,
    "version": "1.0.0",
    "findings": ["Memory check: OK", "Config check: OK"],
    "sig": "304502..."
  },
  "chain": {
    "length": 1,
    "prevHash": "7a8b9c..."
  }
}
```

**Response:**
```json
{
  "received": true,
  "seq": 1,
  "manifest_pending": true
}
```

#### `GET /v1/agent/{fingerprint}/chain`
Get full attestation history for an agent.

**Query Parameters:**
- `limit` (optional, default 100, max 1000): Number of attestations to return
- `offset` (optional, default 0): Offset for pagination

**Response:**
```json
{
  "agent_id": "clawdine-main",
  "fingerprint": "abc123...",
  "attestations": [
    {
      "seq": 0,
      "prev": "0000...",
      "ts": 1735689600,
      "result": "pass",
      "critical": 0,
      "warn": 0,
      "info": 3,
      "version": "1.0.0",
      "findings": ["Agent enrolled"],
      "sig": "304502...",
      "hash": "7a8b9c..."
    }
  ],
  "total": 42
}
```

#### `GET /v1/agent/{fingerprint}/status`
Get agent status and chain health.

**Response:**
```json
{
  "agent_id": "clawdine-main",
  "fingerprint": "abc123...",
  "enrolled_at": 1735689600,
  "chain_length": 42,
  "last_ts": 1735862400,
  "gap_hours": 2.5,
  "latest_result": "pass",
  "is_valid": true
}
```

### Manifest Endpoints

#### `POST /v1/manifest/generate`
Generate daily manifest (typically run via cron).

**Query Parameters:**
- `date` (optional, format YYYY-MM-DD): Date to generate manifest for. Defaults to today (UTC).

**Response:**
```json
{
  "date": "2025-01-01",
  "manifest_cid": "placeholder_2025-01-01_7a8b9c...",
  "merkle_root": "a1b2c3d4e5f6...",
  "agent_count": 5,
  "attestation_count": 127,
  "entries": [
    {
      "fingerprint": "abc123...",
      "seq": 42,
      "result": "pass",
      "ts": 1735689600
    }
  ]
}
```

#### `GET /v1/manifest/{date}`
Get manifest for a specific date.

**Response:** Same as generate endpoint.

#### `GET /v1/health`
Health check and system stats.

**Response:**
```json
{
  "status": "ok",
  "version": "0.1.0",
  "agents_enrolled": 5,
  "attestations_total": 847
}
```

## Architecture

### Project Structure

```
clawdsure-api/
├── main.py          # FastAPI app with all endpoints
├── models.py        # Pydantic request/response models
├── db.py            # SQLite setup and queries
├── crypto.py        # ECDSA signature verification
├── merkle.py        # Merkle tree implementation
├── requirements.txt # Python dependencies
├── README.md        # This file
└── data/            # SQLite database (auto-created)
    └── clawdsure.db
```

### Database Schema

**agents**
- `fingerprint` (PRIMARY KEY): Agent identifier
- `agent_id`: Human-readable agent name
- `public_key_pem`: ECDSA P-256 public key (PEM format)
- `enrolled_at`: Unix timestamp of enrollment
- `status`: Agent status (default: "active")

**attestations**
- `id` (PRIMARY KEY): Auto-increment ID
- `fingerprint`: Reference to agent
- `seq`: Sequence number (starts at 0)
- `prev`: Hash of previous attestation (chain link)
- `ts`: Attestation timestamp
- `result`: "pass" or "fail"
- `critical`, `warn`, `info`: Finding counts
- `version`: Agent version
- `findings`: JSON array of findings
- `sig`: ECDSA signature (hex)
- `hash`: SHA-256 hash of this attestation
- `received_at`: Server timestamp

**manifests**
- `date` (PRIMARY KEY): Date in YYYY-MM-DD format
- `merkle_root`: Root hash of daily merkle tree
- `manifest_cid`: IPFS CID placeholder
- `agent_count`: Number of unique agents
- `attestation_count`: Total attestations for this day
- `entries`: JSON array of manifest entries
- `generated_at`: Generation timestamp

### Cryptography

**Signature Algorithm**: ECDSA with P-256 curve (secp256r1)

**Signing Process:**
1. Create canonical JSON (sorted keys, no whitespace)
2. SHA-256 hash of canonical JSON
3. Sign with private key
4. Encode signature as hex

**Verification:**
- Public keys stored as PEM
- Signatures verified against canonical attestation JSON
- Genesis attestation verified during enrollment
- All subsequent attestations verified against stored public key

### Merkle Tree

**Implementation:**
- Binary merkle tree
- Leaves: SHA-256 of canonical attestation JSON
- If odd number of leaves, duplicate the last one
- Parent nodes: SHA-256 of concatenated child hashes

**Purpose:**
- Provides cryptographic proof of daily attestation set
- Enables efficient verification without full chain replay
- Future: Will be pinned to IPFS for immutability

## Security Notes

### Current Limitations (MVP)

⚠️ **No API Authentication**: The API itself has no auth layer. Agents authenticate via signatures, but anyone can query the API.

⚠️ **No IPFS Pinning**: Manifest CIDs are placeholder strings. Real IPFS pinning not yet implemented.

⚠️ **No Rate Limiting**: No protection against spam or DoS.

⚠️ **No TLS**: Run behind a reverse proxy (nginx, Caddy) for production.

### Security Best Practices

✅ **Signature Verification**: All attestations cryptographically verified
✅ **Chain Integrity**: Automatic validation of sequence and hash chain
✅ **Immutable Records**: SQLite constraints prevent duplicate sequences
✅ **Public Key Pinning**: Agent public keys fixed at enrollment

### Future Security Enhancements

- [ ] API key authentication
- [ ] Rate limiting per agent/IP
- [ ] IPFS pinning for manifest immutability
- [ ] Optional attestation encryption
- [ ] Webhook notifications for critical findings
- [ ] Multi-party verification (witness nodes)

## Testing

### Manual Testing

1. Start the server:
   ```bash
   uvicorn main:app --port 8420
   ```

2. Check health:
   ```bash
   curl http://localhost:8420/v1/health
   ```

3. Test enrollment (requires generating a key pair and signing genesis attestation):
   ```bash
   # Generate key pair
   openssl ecparam -genkey -name prime256v1 -noout -out private.pem
   openssl ec -in private.pem -pubout -out public.pem
   
   # Sign and enroll (see crypto.py for signing logic)
   ```

### Development

```bash
# Install dev dependencies
pip install pytest pytest-asyncio httpx

# Run tests (when implemented)
pytest
```

## Production Deployment

### Recommended Setup

1. **Reverse Proxy**: Use nginx or Caddy for TLS termination
2. **Process Manager**: Use systemd or supervisor to keep server running
3. **Monitoring**: Set up health check monitoring
4. **Backups**: Regular SQLite database backups
5. **Log Rotation**: Configure uvicorn logging with rotation

### Example systemd Service

```ini
[Unit]
Description=ClawdSure API Server
After=network.target

[Service]
Type=simple
User=clawdsure
WorkingDirectory=/opt/clawdsure-api
ExecStart=/usr/bin/uvicorn main:app --host 127.0.0.1 --port 8420
Restart=always

[Install]
WantedBy=multi-user.target
```

### Environment Variables

```bash
export CLAWDSURE_DB_PATH=/var/lib/clawdsure/clawdsure.db
export CLAWDSURE_PORT=8420
export CLAWDSURE_HOST=127.0.0.1
```

## Daily Manifest Generation

### Cron Setup

Add to crontab:
```bash
# Generate daily manifest at 00:05 UTC
5 0 * * * curl -X POST http://localhost:8420/v1/manifest/generate
```

Or use a dedicated script:
```bash
#!/bin/bash
# generate_manifest.sh

DATE=$(date -u +%Y-%m-%d)
YESTERDAY=$(date -u -d "yesterday" +%Y-%m-%d)

# Generate yesterday's manifest (let day complete fully)
curl -X POST "http://localhost:8420/v1/manifest/generate?date=$YESTERDAY"
```

## Contributing

This is a prototype. Contributions welcome for:
- Unit tests
- API authentication
- IPFS integration
- Performance optimization
- Security hardening

## License

MIT (or your preferred license)

## Version

**0.1.0** - MVP Release
- Core enrollment and attestation endpoints
- Chain validation and integrity checks
- Daily manifest generation
- SQLite storage
- ECDSA signature verification
