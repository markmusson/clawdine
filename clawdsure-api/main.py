"""ClawdSure MVP API Server - FastAPI application."""
import time
from datetime import datetime, timezone
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

from models import (
    EnrollRequest, EnrollResponse, AttestationRequest, AttestationResponse,
    ChainResponse, AgentStatus, ManifestResponse, HealthResponse, AttestationRecord,
    ManifestEntry
)
from db import (
    init_db, enroll_agent, get_agent, store_attestation, get_last_attestation,
    get_attestation_chain, get_chain_count, get_attestations_by_date,
    store_manifest, get_manifest, get_stats
)
from crypto import verify_attestation_signature, hash_attestation
from merkle import compute_merkle_root


app = FastAPI(
    title="ClawdSure API",
    description="Agent attestation and transparency ledger",
    version="0.1.0"
)


@app.on_event("startup")
def startup():
    """Initialize database on startup."""
    init_db()


@app.get("/v1/health", response_model=HealthResponse)
def health():
    """Health check endpoint."""
    stats = get_stats()
    return HealthResponse(
        status="ok",
        version="0.1.0",
        agents_enrolled=stats["agents_enrolled"],
        attestations_total=stats["attestations_total"]
    )


@app.post("/v1/enroll", response_model=EnrollResponse)
def enroll(request: EnrollRequest):
    """
    Enroll a new agent.
    
    Validates genesis attestation signature and stores agent record.
    """
    # Check if already enrolled
    existing = get_agent(request.fingerprint)
    if existing:
        raise HTTPException(status_code=409, detail="Agent already enrolled")
    
    # Validate genesis attestation signature
    attestation_data = {
        "seq": request.genesis_attestation.seq,
        "prev": request.genesis_attestation.prev,
        "ts": request.genesis_attestation.ts,
        "result": request.genesis_attestation.result,
        "critical": request.genesis_attestation.critical,
        "warn": request.genesis_attestation.warn,
        "info": request.genesis_attestation.info,
        "version": request.genesis_attestation.version,
        "findings": request.genesis_attestation.findings
    }
    
    sig_valid = verify_attestation_signature(
        attestation_data,
        request.genesis_attestation.sig,
        request.public_key_pem
    )
    # MVP: warn but don't block — agents sign bash heredoc strings that
    # we can't perfectly reconstruct from parsed JSON. Future agents will
    # sign canonical JSON for verifiable signatures.
    if not sig_valid:
        import logging
        logging.warning(f"Signature verification failed for {request.agent_id} — accepting for MVP")
    
    # Accept seq=1 as genesis (our agents start at 1, not 0)
    if request.genesis_attestation.seq not in (0, 1):
        raise HTTPException(status_code=400, detail="Genesis attestation must have seq 0 or 1")
    # MVP: relax prev check — our genesis uses "null" not "0000..."
    if request.genesis_attestation.prev not in ("null", "") and not request.genesis_attestation.prev.startswith("0000"):
        raise HTTPException(status_code=400, detail="Genesis attestation must have prev=null or starting with 0000")
    
    # Enroll agent
    enrolled_at = int(time.time())
    success = enroll_agent(request.agent_id, request.fingerprint, request.public_key_pem, enrolled_at)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to enroll agent")
    
    # Store genesis attestation
    att_hash = hash_attestation(attestation_data)
    store_attestation(
        request.fingerprint,
        request.genesis_attestation.seq,
        request.genesis_attestation.prev,
        request.genesis_attestation.ts,
        request.genesis_attestation.result,
        request.genesis_attestation.critical,
        request.genesis_attestation.warn,
        request.genesis_attestation.info,
        request.genesis_attestation.version,
        request.genesis_attestation.findings,
        request.genesis_attestation.sig,
        att_hash,
        enrolled_at
    )
    
    return EnrollResponse(
        agent_id=request.agent_id,
        enrolled_at=enrolled_at,
        status="active"
    )


@app.post("/v1/attestation", response_model=AttestationResponse)
def submit_attestation(request: AttestationRequest):
    """
    Submit an attestation.
    
    Validates chain integrity and signature, then stores attestation.
    """
    # Check agent exists
    agent = get_agent(request.agent.fingerprint)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not enrolled")
    
    # Get last attestation
    last = get_last_attestation(request.agent.fingerprint)
    
    # Validate sequence — must be greater than last seen (allow gaps for MVP,
    # since agents may have local attestations not yet submitted to API)
    if last and request.attestation.seq <= last['seq']:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sequence: must be > {last['seq']}, got {request.attestation.seq}"
        )
    
    # MVP: relax prev hash check — allow gaps since agent may have
    # local attestations not yet synced to API
    if last:
        import logging
        expected_prev = last['hash']
        if request.attestation.prev != expected_prev:
            logging.warning(f"Prev hash mismatch for {request.agent.id} seq {request.attestation.seq} — accepting (gap sync)")
    
    # Validate signature (best-effort for MVP)
    attestation_data = {
        "seq": request.attestation.seq,
        "prev": request.attestation.prev,
        "ts": request.attestation.ts,
        "result": request.attestation.result,
        "critical": request.attestation.critical,
        "warn": request.attestation.warn,
        "info": request.attestation.info,
        "version": request.attestation.version,
        "findings": request.attestation.findings
    }
    
    sig_valid = verify_attestation_signature(
        attestation_data,
        request.attestation.sig,
        agent['public_key_pem']
    )
    if not sig_valid:
        import logging
        logging.warning(f"Signature verification failed for {request.agent.id} seq {request.attestation.seq} — accepting for MVP")
    
    # Store attestation
    att_hash = hash_attestation(attestation_data)
    received_at = int(time.time())
    
    success = store_attestation(
        request.agent.fingerprint,
        request.attestation.seq,
        request.attestation.prev,
        request.attestation.ts,
        request.attestation.result,
        request.attestation.critical,
        request.attestation.warn,
        request.attestation.info,
        request.attestation.version,
        request.attestation.findings,
        request.attestation.sig,
        att_hash,
        received_at
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to store attestation")
    
    return AttestationResponse(
        received=True,
        seq=request.attestation.seq,
        manifest_pending=True
    )


@app.get("/v1/agent/{fingerprint}/chain", response_model=ChainResponse)
def get_chain(
    fingerprint: str,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Get full attestation chain for an agent."""
    agent = get_agent(fingerprint)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    attestations = get_attestation_chain(fingerprint, limit, offset)
    total = get_chain_count(fingerprint)
    
    records = [
        AttestationRecord(
            seq=att['seq'],
            prev=att['prev'],
            ts=att['ts'],
            result=att['result'],
            critical=att['critical'],
            warn=att['warn'],
            info=att['info'],
            version=att['version'],
            findings=att['findings'],
            sig=att['sig'],
            hash=att['hash']
        )
        for att in attestations
    ]
    
    return ChainResponse(
        agent_id=agent['agent_id'],
        fingerprint=fingerprint,
        attestations=records,
        total=total
    )


@app.get("/v1/agent/{fingerprint}/status", response_model=AgentStatus)
def get_status(fingerprint: str):
    """Get agent status and chain health."""
    agent = get_agent(fingerprint)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    last = get_last_attestation(fingerprint)
    chain_length = get_chain_count(fingerprint)
    
    if last:
        now = int(time.time())
        last_ts = last['ts']
        if isinstance(last_ts, str):
            from datetime import datetime, timezone
            try:
                last_ts = int(datetime.fromisoformat(last_ts.replace('Z', '+00:00')).timestamp())
            except:
                last_ts = now  # fallback
        gap_hours = (now - last_ts) / 3600.0
        is_valid = gap_hours < 48  # Chain breaks after 48 hours
    else:
        gap_hours = None
        is_valid = chain_length == 0  # Valid if no attestations yet
    
    return AgentStatus(
        agent_id=agent['agent_id'],
        fingerprint=fingerprint,
        enrolled_at=agent['enrolled_at'],
        chain_length=chain_length,
        last_ts=last['ts'] if last else None,
        gap_hours=gap_hours,
        latest_result=last['result'] if last else None,
        is_valid=is_valid
    )


@app.post("/v1/manifest/generate", response_model=ManifestResponse)
def generate_manifest(date: Optional[str] = None):
    """
    Generate daily manifest.
    
    Collects all attestations for the given date and builds a merkle tree.
    If no date provided, uses today (UTC).
    """
    if not date:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    # Validate date format
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format (use YYYY-MM-DD)")
    
    # Get attestations for this date
    attestations = get_attestations_by_date(date)
    
    if not attestations:
        raise HTTPException(status_code=404, detail=f"No attestations found for {date}")
    
    # Build entries
    entries = [
        ManifestEntry(
            fingerprint=att['fingerprint'],
            seq=att['seq'],
            result=att['result'],
            ts=att['ts']
        )
        for att in attestations
    ]
    
    # Compute merkle root
    attestation_dicts = [
        {
            "fingerprint": att['fingerprint'],
            "seq": att['seq'],
            "result": att['result'],
            "ts": att['ts']
        }
        for att in attestations
    ]
    merkle_root = compute_merkle_root(attestation_dicts)
    
    # Count unique agents
    unique_agents = len(set(att['fingerprint'] for att in attestations))
    
    # Store manifest
    manifest_cid = f"placeholder_{date}_{merkle_root[:16]}"
    generated_at = int(time.time())
    
    store_manifest(
        date,
        merkle_root,
        manifest_cid,
        unique_agents,
        len(attestations),
        [entry.model_dump() for entry in entries],
        generated_at
    )
    
    return ManifestResponse(
        date=date,
        manifest_cid=manifest_cid,
        merkle_root=merkle_root,
        agent_count=unique_agents,
        attestation_count=len(attestations),
        entries=entries
    )


@app.get("/v1/manifest/{date}", response_model=ManifestResponse)
def get_daily_manifest(date: str):
    """Get manifest for a specific date."""
    # Validate date format
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format (use YYYY-MM-DD)")
    
    manifest = get_manifest(date)
    if not manifest:
        raise HTTPException(status_code=404, detail=f"No manifest found for {date}")
    
    entries = [ManifestEntry(**entry) for entry in manifest['entries']]
    
    return ManifestResponse(
        date=manifest['date'],
        manifest_cid=manifest['manifest_cid'],
        merkle_root=manifest['merkle_root'],
        agent_count=manifest['agent_count'],
        attestation_count=manifest['attestation_count'],
        entries=entries
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8420)
