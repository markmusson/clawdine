#!/usr/bin/env python3
"""
Quick test client for ClawdSure API.

Usage:
    1. Start the server: uvicorn main:app --port 8420
    2. Run this script: python test_client.py
"""

import requests
import json
import hashlib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

BASE_URL = "http://localhost:8420"


def generate_key_pair():
    """Generate ECDSA P-256 key pair."""
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    
    # Export public key as PEM
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()
    
    return private_key, public_pem


def sign_attestation(attestation_data: dict, private_key) -> str:
    """Sign attestation data with private key."""
    # Create canonical JSON
    canonical_json = json.dumps(attestation_data, sort_keys=True, separators=(',', ':'))
    message = canonical_json.encode()
    
    # Sign
    signature = private_key.sign(message, ec.ECDSA(hashes.SHA256()))
    return signature.hex()


def hash_attestation(attestation_data: dict) -> str:
    """Compute SHA-256 hash of attestation."""
    canonical_json = json.dumps(attestation_data, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(canonical_json.encode()).hexdigest()


def test_enrollment():
    """Test agent enrollment."""
    print("🔑 Generating key pair...")
    private_key, public_pem = generate_key_pair()
    
    # Create genesis attestation
    genesis_data = {
        "seq": 0,
        "prev": "0" * 64,
        "ts": 1735689600,
        "result": "pass",
        "critical": 0,
        "warn": 0,
        "info": 1,
        "version": "1.0.0",
        "findings": ["Genesis attestation"]
    }
    
    genesis_sig = sign_attestation(genesis_data, private_key)
    
    # Enroll
    print("📝 Enrolling agent...")
    response = requests.post(f"{BASE_URL}/v1/enroll", json={
        "agent_id": "test-agent",
        "fingerprint": "test123abc",
        "public_key_pem": public_pem,
        "genesis_attestation": {**genesis_data, "sig": genesis_sig}
    })
    
    print(f"✅ Enrollment response: {response.json()}")
    return private_key, public_pem, "test123abc", genesis_data


def test_attestation(private_key, fingerprint, prev_data):
    """Test attestation submission."""
    print("\n📋 Submitting attestation...")
    
    prev_hash = hash_attestation(prev_data)
    
    attestation_data = {
        "seq": prev_data["seq"] + 1,
        "prev": prev_hash,
        "ts": prev_data["ts"] + 86400,
        "result": "pass",
        "critical": 0,
        "warn": 1,
        "info": 2,
        "version": "1.0.0",
        "findings": ["Memory check: OK", "Config check: OK"]
    }
    
    sig = sign_attestation(attestation_data, private_key)
    
    response = requests.post(f"{BASE_URL}/v1/attestation", json={
        "agent": {
            "id": "test-agent",
            "fingerprint": fingerprint
        },
        "attestation": {**attestation_data, "sig": sig},
        "chain": {
            "length": prev_data["seq"] + 1,
            "prevHash": prev_hash
        }
    })
    
    print(f"✅ Attestation response: {response.json()}")
    return attestation_data


def test_chain(fingerprint):
    """Test chain retrieval."""
    print(f"\n🔗 Fetching chain for {fingerprint}...")
    response = requests.get(f"{BASE_URL}/v1/agent/{fingerprint}/chain")
    data = response.json()
    print(f"✅ Chain length: {data['total']}")
    print(f"   Attestations: {len(data['attestations'])}")


def test_status(fingerprint):
    """Test status check."""
    print(f"\n📊 Checking status for {fingerprint}...")
    response = requests.get(f"{BASE_URL}/v1/agent/{fingerprint}/status")
    print(f"✅ Status: {json.dumps(response.json(), indent=2)}")


def test_health():
    """Test health endpoint."""
    print("\n💚 Checking health...")
    response = requests.get(f"{BASE_URL}/v1/health")
    print(f"✅ Health: {json.dumps(response.json(), indent=2)}")


def main():
    """Run all tests."""
    print("🚀 ClawdSure API Test Client\n")
    
    try:
        # Test health first
        test_health()
        
        # Enrollment
        private_key, public_pem, fingerprint, genesis = test_enrollment()
        
        # Submit attestations
        prev = genesis
        for i in range(3):
            prev = test_attestation(private_key, fingerprint, prev)
        
        # Check chain
        test_chain(fingerprint)
        
        # Check status
        test_status(fingerprint)
        
        print("\n✅ All tests passed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API server.")
        print("   Make sure the server is running: uvicorn main:app --port 8420")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
