"""SQLite database setup and queries for ClawdSure."""
import sqlite3
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from contextlib import contextmanager


DB_PATH = Path(__file__).parent / "data" / "clawdsure.db"


def init_db():
    """Initialize database schema."""
    DB_PATH.parent.mkdir(exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Agents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            fingerprint TEXT PRIMARY KEY,
            agent_id TEXT NOT NULL,
            public_key_pem TEXT NOT NULL,
            enrolled_at INTEGER NOT NULL,
            status TEXT DEFAULT 'active'
        )
    """)
    
    # Attestations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attestations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fingerprint TEXT NOT NULL,
            seq INTEGER NOT NULL,
            prev TEXT NOT NULL,
            ts INTEGER NOT NULL,
            result TEXT NOT NULL,
            critical INTEGER NOT NULL,
            warn INTEGER NOT NULL,
            info INTEGER NOT NULL,
            version TEXT NOT NULL,
            findings TEXT NOT NULL,
            sig TEXT NOT NULL,
            hash TEXT NOT NULL,
            received_at INTEGER NOT NULL,
            UNIQUE(fingerprint, seq),
            FOREIGN KEY(fingerprint) REFERENCES agents(fingerprint)
        )
    """)
    
    # Manifests table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS manifests (
            date TEXT PRIMARY KEY,
            merkle_root TEXT NOT NULL,
            manifest_cid TEXT NOT NULL,
            agent_count INTEGER NOT NULL,
            attestation_count INTEGER NOT NULL,
            entries TEXT NOT NULL,
            generated_at INTEGER NOT NULL
        )
    """)
    
    # Indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_attestations_fingerprint ON attestations(fingerprint)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_attestations_ts ON attestations(ts)")
    
    conn.commit()
    conn.close()


@contextmanager
def get_db():
    """Context manager for database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def enroll_agent(agent_id: str, fingerprint: str, public_key_pem: str, enrolled_at: int) -> bool:
    """
    Enroll a new agent.
    
    Returns:
        True if enrolled, False if already exists
    """
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO agents (fingerprint, agent_id, public_key_pem, enrolled_at) VALUES (?, ?, ?, ?)",
                (fingerprint, agent_id, public_key_pem, enrolled_at)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False


def get_agent(fingerprint: str) -> Optional[Dict[str, Any]]:
    """Get agent by fingerprint."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM agents WHERE fingerprint = ?", (fingerprint,))
        row = cursor.fetchone()
        return dict(row) if row else None


def store_attestation(
    fingerprint: str,
    seq: int,
    prev: str,
    ts: int,
    result: str,
    critical: int,
    warn: int,
    info: int,
    version: str,
    findings: List[str],
    sig: str,
    att_hash: str,
    received_at: int
) -> bool:
    """Store attestation."""
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO attestations 
                   (fingerprint, seq, prev, ts, result, critical, warn, info, version, findings, sig, hash, received_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (fingerprint, seq, prev, ts, result, critical, warn, info, version, 
                 json.dumps(findings), sig, att_hash, received_at)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False


def get_last_attestation(fingerprint: str) -> Optional[Dict[str, Any]]:
    """Get the most recent attestation for an agent."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM attestations WHERE fingerprint = ? ORDER BY seq DESC LIMIT 1",
            (fingerprint,)
        )
        row = cursor.fetchone()
        if row:
            result = dict(row)
            result['findings'] = json.loads(result['findings'])
            return result
        return None


def get_attestation_chain(fingerprint: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """Get attestation chain for an agent."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM attestations WHERE fingerprint = ? ORDER BY seq ASC LIMIT ? OFFSET ?",
            (fingerprint, limit, offset)
        )
        rows = cursor.fetchall()
        results = []
        for row in rows:
            result = dict(row)
            result['findings'] = json.loads(result['findings'])
            results.append(result)
        return results


def get_chain_count(fingerprint: str) -> int:
    """Get total attestation count for an agent."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM attestations WHERE fingerprint = ?", (fingerprint,))
        return cursor.fetchone()[0]


def get_attestations_by_date(date: str) -> List[Dict[str, Any]]:
    """Get all attestations for a given date (YYYY-MM-DD)."""
    # Convert date to unix timestamp range
    from datetime import datetime, timezone
    dt = datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    start_ts = int(dt.timestamp())
    end_ts = start_ts + 86400  # +24 hours
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM attestations WHERE ts >= ? AND ts < ? ORDER BY ts ASC",
            (start_ts, end_ts)
        )
        rows = cursor.fetchall()
        results = []
        for row in rows:
            result = dict(row)
            result['findings'] = json.loads(result['findings'])
            results.append(result)
        return results


def store_manifest(
    date: str,
    merkle_root: str,
    manifest_cid: str,
    agent_count: int,
    attestation_count: int,
    entries: List[Dict],
    generated_at: int
) -> bool:
    """Store daily manifest."""
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT OR REPLACE INTO manifests 
                   (date, merkle_root, manifest_cid, agent_count, attestation_count, entries, generated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (date, merkle_root, manifest_cid, agent_count, attestation_count, 
                 json.dumps(entries), generated_at)
            )
            conn.commit()
            return True
        except Exception:
            return False


def get_manifest(date: str) -> Optional[Dict[str, Any]]:
    """Get manifest for a given date."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM manifests WHERE date = ?", (date,))
        row = cursor.fetchone()
        if row:
            result = dict(row)
            result['entries'] = json.loads(result['entries'])
            return result
        return None


def get_stats() -> Dict[str, int]:
    """Get global stats."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM agents")
        agents_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM attestations")
        attestations_count = cursor.fetchone()[0]
        return {
            "agents_enrolled": agents_count,
            "attestations_total": attestations_count
        }
