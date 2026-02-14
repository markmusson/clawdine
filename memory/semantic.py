#!/usr/bin/env python3
"""
Semantic Memory for OpenClaw Agents
Drop-in replacement for Hindsight using LanceDB + FastEmbed

Usage:
    from memory.semantic import Memory
    mem = Memory()
    mem.add("The weather trading edge is betting against precision")
    results = mem.search("what's the trading strategy?")
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

import lancedb
from fastembed import TextEmbedding


class Memory:
    def __init__(self, path: str = None, model: str = "BAAI/bge-small-en-v1.5"):
        """Initialize semantic memory.
        
        Args:
            path: Directory for LanceDB storage. Defaults to ~/.openclaw/workspace/memory/lance
            model: FastEmbed model name. bge-small-en-v1.5 is 384 dims, fast, good quality.
        """
        if path is None:
            path = Path.home() / ".openclaw" / "workspace" / "memory" / "lance"
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)
        
        self.db = lancedb.connect(str(self.path))
        self._embedder = None
        self._model_name = model
    
    @property
    def embedder(self):
        """Lazy-load embedder (downloads model on first use)."""
        if self._embedder is None:
            self._embedder = TextEmbedding(model_name=self._model_name)
        return self._embedder
    
    def _embed(self, text: str) -> list[float]:
        """Generate embedding for text."""
        return list(self.embedder.embed([text]))[0].tolist()
    
    def add(
        self,
        text: str,
        *,
        fact_type: str = "world",
        source: str = None,
        tags: list[str] = None,
        metadata: dict = None,
    ) -> str:
        """Add a memory.
        
        Args:
            text: The memory content
            fact_type: "world" (facts), "experience" (things that happened), "observation"
            source: Where this came from (e.g., "chat", "document", "web")
            tags: Optional tags for filtering
            metadata: Any additional metadata
            
        Returns:
            Memory ID
        """
        import uuid
        
        memory_id = str(uuid.uuid4())
        now = datetime.now(tz=__import__("datetime").UTC).isoformat() + "Z"
        
        record = {
            "id": memory_id,
            "text": text,
            "vector": self._embed(text),
            "fact_type": fact_type,
            "source": source or "unknown",
            "tags": json.dumps(tags or []),
            "metadata": json.dumps(metadata or {}),
            "created_at": now,
        }
        
        if "memories" not in self.db.list_tables().tables:
            self.db.create_table("memories", [record])
        else:
            self.db["memories"].add([record])
        
        return memory_id
    
    def search(
        self,
        query: str,
        *,
        limit: int = 10,
        fact_type: str = None,
    ) -> list[dict]:
        """Search memories by semantic similarity.
        
        Args:
            query: Search query
            limit: Max results
            fact_type: Filter by fact type
            
        Returns:
            List of matching memories with scores
        """
        if "memories" not in self.db.list_tables().tables:
            return []
        
        vector = self._embed(query)
        results = self.db["memories"].search(vector).limit(limit)
        
        if fact_type:
            results = results.where(f"fact_type = '{fact_type}'")
        
        rows = results.to_list()
        
        # Clean up results
        for row in rows:
            row["tags"] = json.loads(row.get("tags", "[]"))
            row["metadata"] = json.loads(row.get("metadata", "{}"))
            row.pop("vector", None)  # Don't return the embedding
        
        return rows
    
    def delete(self, memory_id: str) -> bool:
        """Delete a memory by ID."""
        if "memories" not in self.db.list_tables().tables:
            return False
        self.db["memories"].delete(f"id = '{memory_id}'")
        return True
    
    def count(self) -> int:
        """Count total memories."""
        if "memories" not in self.db.list_tables().tables:
            return 0
        return self.db["memories"].count_rows()
    
    def import_from_hindsight(self, csv_path: str) -> int:
        """Import memories from Hindsight CSV export.
        
        Args:
            csv_path: Path to memory_units.csv
            
        Returns:
            Number of imported memories
        """
        import csv
        
        count = 0
        with open(csv_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                text = row.get("text", "").strip()
                if not text:
                    continue
                
                self.add(
                    text,
                    fact_type=row.get("fact_type", "world"),
                    source="hindsight-import",
                    metadata={
                        "original_id": row.get("id"),
                        "original_created": row.get("created_at"),
                    }
                )
                count += 1
        
        return count


# CLI for quick testing
if __name__ == "__main__":
    import sys
    
    mem = Memory()
    
    if len(sys.argv) < 2:
        print(f"Memories: {mem.count()}")
        print("\nUsage:")
        print("  python semantic.py add 'some memory text'")
        print("  python semantic.py search 'query'")
        print("  python semantic.py import /path/to/memory_units.csv")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "add" and len(sys.argv) > 2:
        text = " ".join(sys.argv[2:])
        mid = mem.add(text)
        print(f"Added: {mid}")
    
    elif cmd == "search" and len(sys.argv) > 2:
        query = " ".join(sys.argv[2:])
        results = mem.search(query, limit=5)
        for i, r in enumerate(results, 1):
            score = r.get("_distance", "?")
            print(f"{i}. [{r['fact_type']}] {r['text'][:100]}... (score: {score})")
    
    elif cmd == "import" and len(sys.argv) > 2:
        path = sys.argv[2]
        count = mem.import_from_hindsight(path)
        print(f"Imported {count} memories")
    
    else:
        print("Unknown command")
