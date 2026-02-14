# ClawdSafe Underwriting Platform API

**Version:** 1.0  
**Base URL:** `https://api.clawdsure.io/v1`

---

## Authentication

All requests must include agent signature:

```
X-Agent-ID: CLWD-FFF4D493
X-Agent-Signature: base64(ECDSA-SHA256(request_body, agent_private_key))
```

The platform verifies signature against registered public key.

---

## Endpoints

### Health Check

```
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "timestamp": "2026-02-07T10:00:00Z"
}
```

---

### Enrollment

```
POST /enroll
```

Register a new agent and initiate policy.

**Request:**
```json
{
  "action": "enroll",
  "agent": {
    "id": "CLWD-FFF4D493",
    "fingerprint": "fff4d493084465f4a5563f741f44ecbbf4055eb9c829e5677c9ae91ef6c40177",
    "publicKey": "base64(PEM public key)"
  },
  "genesis": {
    "attestation": {
      "seq": 1,
      "prev": "genesis",
      "ts": "2026-02-07T09:54:59Z",
      "agent": "CLWD-FFF4D493",
      "result": "PASS",
      "critical": 0,
      "warn": 1,
      "info": 1,
      "version": "2026.2.6-3",
      "sig": "MEYCIQD..."
    },
    "ipfsCid": "bagbaiera5opc3c6pheofnvwtjmilx4id7uu5pc5xbt7jqp5n33wqo45gjxha",
    "timestamp": "2026-02-07T09:54:59Z"
  },
  "audit": {
    "tool": "clawdstrike",
    "version": "2026.2.6-3",
    "result": "PASS",
    "findings": {
      "critical": 0,
      "warn": 1,
      "info": 1
    }
  },
  "policy": {
    "tier": "basic",
    "premium": 50,
    "payout": 500,
    "term": "annual"
  }
}
```

**Response (Success):**
```json
{
  "status": "ok",
  "enrollment": {
    "id": "ENR-20260207-001",
    "agentId": "CLWD-FFF4D493",
    "status": "pending_payment",
    "paymentUrl": "https://clawdsure.io/pay/ENR-20260207-001",
    "policy": {
      "id": "POL-20260207-001",
      "tier": "basic",
      "premium": 50,
      "payout": 500,
      "startsAt": null,
      "expiresAt": null
    }
  },
  "chain": {
    "genesisSeq": 1,
    "genesisCid": "bagbaiera5opc3c6pheofnvwtjmilx4id7uu5pc5xbt7jqp5n33wqo45gjxha",
    "verified": true
  }
}
```

**Response (Fail - Critical Findings):**
```json
{
  "status": "error",
  "code": "AUDIT_FAILED",
  "message": "Cannot enroll with critical findings",
  "details": {
    "critical": 2,
    "requiredAction": "Remediate critical findings and re-submit"
  }
}
```

---

### Submit Attestation

```
POST /attestation
```

Submit daily attestation to maintain chain.

**Request:**
```json
{
  "action": "attestation",
  "agent": {
    "id": "CLWD-FFF4D493",
    "fingerprint": "fff4d493..."
  },
  "attestation": {
    "seq": 42,
    "prev": "sha256(attestation_41)",
    "ts": "2026-03-15T09:00:00Z",
    "agent": "CLWD-FFF4D493",
    "result": "PASS",
    "critical": 0,
    "warn": 1,
    "info": 2,
    "version": "2026.2.8-1",
    "sig": "MEYCIQD..."
  },
  "ipfs": {
    "cid": "bafybeig...",
    "gateway": "https://gateway.pinata.cloud/ipfs/bafybeig..."
  },
  "chain": {
    "length": 42,
    "prevHash": "abc123..."
  }
}
```

**Response (Success):**
```json
{
  "status": "ok",
  "attestation": {
    "seq": 42,
    "verified": true,
    "chainIntact": true
  },
  "policy": {
    "id": "POL-20260207-001",
    "status": "active",
    "daysRemaining": 287,
    "chainLength": 42,
    "lastAttestationAt": "2026-03-15T09:00:00Z"
  }
}
```

**Response (Chain Break Warning):**
```json
{
  "status": "warning",
  "code": "CHAIN_GAP",
  "message": "Attestation gap detected",
  "details": {
    "lastSeq": 40,
    "submittedSeq": 42,
    "gapHours": 72,
    "graceRemaining": 0,
    "chainStatus": "broken"
  },
  "policy": {
    "status": "suspended",
    "action": "Re-enroll required"
  }
}
```

---

### Get Policy Status

```
GET /policy/:agentId
```

**Response:**
```json
{
  "status": "ok",
  "policy": {
    "id": "POL-20260207-001",
    "agentId": "CLWD-FFF4D493",
    "tier": "basic",
    "premium": 50,
    "payout": 500,
    "status": "active",
    "startsAt": "2026-02-07T12:00:00Z",
    "expiresAt": "2027-02-07T12:00:00Z",
    "daysRemaining": 365
  },
  "chain": {
    "length": 42,
    "lastSeq": 42,
    "lastCid": "bafybeig...",
    "lastAttestationAt": "2026-03-15T09:00:00Z",
    "status": "intact",
    "consecutivePasses": 42
  },
  "metrics": {
    "totalAttestations": 42,
    "passRate": 100,
    "avgFindingsWarn": 1.2,
    "avgFindingsInfo": 1.8
  }
}
```

---

### Report Incident

```
POST /incident
```

Report a security incident for claim processing.

**Request:**
```json
{
  "action": "report_incident",
  "agent": {
    "id": "CLWD-FFF4D493",
    "fingerprint": "fff4d493..."
  },
  "incident": {
    "type": "unauthorized_access",
    "detectedAt": "2026-06-15T14:32:00Z",
    "description": "Unauthorized command execution detected via compromised skill",
    "evidence": {
      "logs": "https://...",
      "ipfsCid": "bafybeig...",
      "additionalNotes": "Skill 'evil-weather' was installed from untrusted source"
    },
    "impact": {
      "dataExfiltrated": false,
      "credentialsCompromised": true,
      "serviceDisrupted": true
    }
  },
  "claim": {
    "requestPayout": true,
    "amount": 500
  }
}
```

**Response:**
```json
{
  "status": "ok",
  "incident": {
    "id": "INC-20260615-001",
    "status": "under_review",
    "reportedAt": "2026-06-15T15:00:00Z"
  },
  "claim": {
    "id": "CLM-20260615-001",
    "status": "pending_verification",
    "chainStatus": "intact",
    "estimatedReviewTime": "48h"
  },
  "nextSteps": [
    "Oracle will verify attestation chain integrity",
    "Incident evidence will be reviewed",
    "You will be notified of claim decision within 48h"
  ]
}
```

---

### Verify Chain (Public)

```
GET /verify/:agentId
```

Public endpoint to verify an agent's attestation chain.

**Response:**
```json
{
  "status": "ok",
  "agent": {
    "id": "CLWD-FFF4D493",
    "publicKey": "-----BEGIN PUBLIC KEY-----\n...",
    "registeredAt": "2026-02-07T12:00:00Z"
  },
  "chain": {
    "length": 42,
    "genesisAt": "2026-02-07T09:54:59Z",
    "lastAt": "2026-03-15T09:00:00Z",
    "status": "intact",
    "verified": true
  },
  "ipfs": {
    "latestCid": "bafybeig...",
    "gateway": "https://gateway.pinata.cloud/ipfs/bafybeig..."
  },
  "policy": {
    "active": true,
    "tier": "basic",
    "expiresAt": "2027-02-07T12:00:00Z"
  }
}
```

---

## Webhooks

The platform can notify agents of important events.

### Webhook Events

| Event | Trigger |
|-------|---------|
| `policy.activated` | Payment received, policy active |
| `policy.expiring` | 30 days before expiration |
| `policy.expired` | Policy expired |
| `chain.gap_warning` | No attestation for 24h |
| `chain.broken` | 48h without attestation |
| `claim.approved` | Claim verified, payout initiated |
| `claim.denied` | Claim denied with reason |

### Webhook Payload

```json
{
  "event": "chain.gap_warning",
  "timestamp": "2026-03-16T09:00:00Z",
  "agent": {
    "id": "CLWD-FFF4D493"
  },
  "data": {
    "lastAttestationAt": "2026-03-15T09:00:00Z",
    "hoursSinceLastAttestation": 24,
    "graceRemainingHours": 24
  },
  "action": {
    "required": true,
    "message": "Submit attestation within 24h to maintain chain"
  }
}
```

---

## Error Codes

| Code | HTTP | Description |
|------|------|-------------|
| `INVALID_SIGNATURE` | 401 | Signature verification failed |
| `AGENT_NOT_FOUND` | 404 | Agent ID not registered |
| `POLICY_NOT_ACTIVE` | 403 | No active policy |
| `CHAIN_BROKEN` | 400 | Attestation chain is broken |
| `AUDIT_FAILED` | 400 | Cannot enroll with critical findings |
| `DUPLICATE_ATTESTATION` | 409 | Attestation seq already submitted |
| `RATE_LIMITED` | 429 | Too many requests |

---

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| `/enroll` | 5/hour |
| `/attestation` | 10/hour |
| `/incident` | 3/day |
| `/policy/:id` | 60/hour |
| `/verify/:id` | 120/hour |

---

## SDK Example (Python)

```python
import requests
import json
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
import base64

class ClawdSafeClient:
    def __init__(self, agent_id, private_key_path, api_base="https://api.clawdsure.io/v1"):
        self.agent_id = agent_id
        self.api_base = api_base
        with open(private_key_path, 'rb') as f:
            self.private_key = serialization.load_pem_private_key(f.read(), password=None)
    
    def sign(self, payload):
        data = json.dumps(payload, separators=(',', ':')).encode()
        signature = self.private_key.sign(data, ec.ECDSA(hashes.SHA256()))
        return base64.b64encode(signature).decode()
    
    def submit_attestation(self, attestation, ipfs_cid, chain_length, prev_hash):
        payload = {
            "action": "attestation",
            "agent": {"id": self.agent_id},
            "attestation": attestation,
            "ipfs": {"cid": ipfs_cid},
            "chain": {"length": chain_length, "prevHash": prev_hash}
        }
        
        headers = {
            "Content-Type": "application/json",
            "X-Agent-ID": self.agent_id,
            "X-Agent-Signature": self.sign(payload)
        }
        
        response = requests.post(f"{self.api_base}/attestation", json=payload, headers=headers)
        return response.json()

# Usage
client = ClawdSafeClient("CLWD-FFF4D493", "~/.clawdsure/agent.key")
result = client.submit_attestation(attestation, cid, 42, prev_hash)
```

---

## Database Schema (Reference)

```sql
-- Agents
CREATE TABLE agents (
  id VARCHAR(20) PRIMARY KEY,        -- CLWD-FFF4D493
  fingerprint VARCHAR(64) NOT NULL,
  public_key TEXT NOT NULL,
  registered_at TIMESTAMP NOT NULL,
  status VARCHAR(20) DEFAULT 'active'
);

-- Policies  
CREATE TABLE policies (
  id VARCHAR(30) PRIMARY KEY,        -- POL-20260207-001
  agent_id VARCHAR(20) REFERENCES agents(id),
  tier VARCHAR(20) NOT NULL,
  premium_cents INT NOT NULL,
  payout_cents INT NOT NULL,
  starts_at TIMESTAMP,
  expires_at TIMESTAMP,
  status VARCHAR(20) DEFAULT 'pending_payment'
);

-- Attestations
CREATE TABLE attestations (
  id SERIAL PRIMARY KEY,
  agent_id VARCHAR(20) REFERENCES agents(id),
  seq INT NOT NULL,
  prev_hash VARCHAR(64),
  timestamp TIMESTAMP NOT NULL,
  result VARCHAR(10) NOT NULL,
  critical INT DEFAULT 0,
  warn INT DEFAULT 0,
  info INT DEFAULT 0,
  version VARCHAR(30),
  signature TEXT NOT NULL,
  ipfs_cid VARCHAR(100),
  received_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(agent_id, seq)
);

-- Incidents
CREATE TABLE incidents (
  id VARCHAR(30) PRIMARY KEY,
  agent_id VARCHAR(20) REFERENCES agents(id),
  type VARCHAR(50) NOT NULL,
  detected_at TIMESTAMP NOT NULL,
  reported_at TIMESTAMP DEFAULT NOW(),
  description TEXT,
  evidence JSONB,
  status VARCHAR(20) DEFAULT 'under_review',
  reviewed_at TIMESTAMP,
  reviewer_notes TEXT
);

-- Claims
CREATE TABLE claims (
  id VARCHAR(30) PRIMARY KEY,
  incident_id VARCHAR(30) REFERENCES incidents(id),
  policy_id VARCHAR(30) REFERENCES policies(id),
  amount_cents INT NOT NULL,
  status VARCHAR(20) DEFAULT 'pending',
  chain_verified BOOLEAN,
  payout_at TIMESTAMP,
  payout_tx VARCHAR(100)
);
```

---

*ClawdSafe: Underwriting the autonomous economy.*
