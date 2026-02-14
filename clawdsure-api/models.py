"""Pydantic models for ClawdSure API."""
from pydantic import BaseModel, Field
from typing import Optional, List, Any, Union


class AgentInfo(BaseModel):
    """Agent identifier info."""
    id: str
    fingerprint: str


class AttestationData(BaseModel):
    """Attestation payload — accepts both ISO timestamps and unix ints."""
    seq: int
    prev: str
    ts: Union[str, int]
    agent: Optional[str] = None
    result: str
    critical: int = 0
    warn: int = 0
    info: int = 0
    version: str = ""
    findings: Optional[List[Any]] = None
    sig: str


class ChainInfo(BaseModel):
    """Chain metadata."""
    length: int
    prevHash: Optional[str] = None


class EnrollRequest(BaseModel):
    """POST /v1/enroll payload."""
    agent_id: str
    fingerprint: str
    public_key_pem: str
    genesis_attestation: AttestationData


class EnrollResponse(BaseModel):
    """POST /v1/enroll response."""
    agent_id: str
    enrolled_at: int
    status: str


class AttestationRequest(BaseModel):
    """POST /v1/attestation payload."""
    agent: AgentInfo
    attestation: AttestationData
    chain: ChainInfo


class AttestationResponse(BaseModel):
    """POST /v1/attestation response."""
    received: bool
    seq: int
    manifest_pending: bool


class AttestationRecord(BaseModel):
    """Single attestation in chain."""
    seq: int
    prev: str
    ts: Union[str, int]
    result: str
    critical: int = 0
    warn: int = 0
    info: int = 0
    version: str = ""
    findings: Optional[List[Any]] = None
    sig: str
    hash: str


class ChainResponse(BaseModel):
    """GET /v1/agent/{fingerprint}/chain response."""
    agent_id: str
    fingerprint: str
    attestations: List[AttestationRecord]
    total: int


class AgentStatus(BaseModel):
    """GET /v1/agent/{fingerprint}/status response."""
    agent_id: str
    fingerprint: str
    enrolled_at: int
    chain_length: int
    last_ts: Optional[Union[str, int]]
    gap_hours: Optional[float]
    latest_result: Optional[str]
    is_valid: bool


class ManifestEntry(BaseModel):
    """Single entry in daily manifest."""
    fingerprint: str
    seq: int
    result: str
    ts: Union[str, int]


class ManifestResponse(BaseModel):
    """POST /v1/manifest/generate response."""
    date: str
    manifest_cid: str
    merkle_root: str
    agent_count: int
    attestation_count: int
    entries: List[ManifestEntry]


class HealthResponse(BaseModel):
    """GET /v1/health response."""
    status: str
    version: str
    agents_enrolled: int
    attestations_total: int
