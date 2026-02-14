"""Cryptographic signature verification for ClawdSure."""
import base64
import hashlib
import json
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.exceptions import InvalidSignature


def verify_attestation_signature(
    attestation_data: dict,
    signature_b64: str,
    public_key_pem: str
) -> bool:
    """
    Verify ECDSA P-256 signature on attestation data.
    
    Agents sign the raw JSON string of the attestation (without sig field)
    using: echo -n "$JSON" | openssl dgst -sha256 -sign key | base64
    
    We reconstruct the signed message by re-serializing without 'sig'.
    Since agents use non-canonical JSON, we try multiple serializations.
    """
    try:
        public_key = serialization.load_pem_public_key(public_key_pem.encode())
        
        # Decode base64 signature (agents encode with base64, not hex)
        try:
            signature_bytes = base64.b64decode(signature_b64)
        except Exception:
            # Try hex as fallback
            signature_bytes = bytes.fromhex(signature_b64)
        
        # Build the message that was signed — attestation JSON without 'sig'
        data_without_sig = {k: v for k, v in attestation_data.items() if k != 'sig'}
        
        # Try canonical JSON first (sorted keys, compact)
        candidates = [
            json.dumps(data_without_sig, sort_keys=True, separators=(',', ':')),
            json.dumps(data_without_sig, separators=(',', ':')),  # unsorted compact
            json.dumps(data_without_sig),  # default with spaces
        ]
        
        for candidate in candidates:
            try:
                public_key.verify(
                    signature_bytes,
                    candidate.encode(),
                    ec.ECDSA(hashes.SHA256())
                )
                return True
            except InvalidSignature:
                continue
        
        return False
    except Exception:
        return False


def hash_attestation(attestation_data: dict) -> str:
    """Compute SHA-256 hash of attestation (canonical JSON, with sig)."""
    canonical_json = json.dumps(attestation_data, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(canonical_json.encode()).hexdigest()
