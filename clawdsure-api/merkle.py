"""Simple binary merkle tree implementation."""
import hashlib
import json
from typing import List


def compute_leaf_hash(attestation: dict) -> str:
    """
    Compute SHA-256 hash of attestation (canonical JSON).
    
    Args:
        attestation: Attestation dict
    
    Returns:
        Hex-encoded hash
    """
    canonical_json = json.dumps(attestation, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(canonical_json.encode()).hexdigest()


def hash_pair(left: str, right: str) -> str:
    """
    Hash two nodes together.
    
    Args:
        left: Left node hash (hex)
        right: Right node hash (hex)
    
    Returns:
        Combined hash (hex)
    """
    combined = left + right
    return hashlib.sha256(combined.encode()).hexdigest()


def build_merkle_tree(leaves: List[str]) -> str:
    """
    Build a binary merkle tree from leaf hashes.
    
    Args:
        leaves: List of hex-encoded leaf hashes
    
    Returns:
        Root hash (hex)
    """
    if not leaves:
        return hashlib.sha256(b"").hexdigest()
    
    if len(leaves) == 1:
        return leaves[0]
    
    # If odd number of leaves, duplicate the last one
    if len(leaves) % 2 == 1:
        leaves = leaves + [leaves[-1]]
    
    # Build next level
    next_level = []
    for i in range(0, len(leaves), 2):
        parent_hash = hash_pair(leaves[i], leaves[i + 1])
        next_level.append(parent_hash)
    
    # Recurse
    return build_merkle_tree(next_level)


def compute_merkle_root(attestations: List[dict]) -> str:
    """
    Compute merkle root from list of attestations.
    
    Args:
        attestations: List of attestation dicts
    
    Returns:
        Merkle root (hex)
    """
    leaves = [compute_leaf_hash(att) for att in attestations]
    return build_merkle_tree(leaves)
