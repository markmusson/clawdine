#!/usr/bin/env python3
import json
import re
from pathlib import Path

SKILLS_DIR = Path("/Users/clawdine/.openclaw/workspace/skills")
OUTPUT_JSONL = Path("/Users/clawdine/.openclaw/workspace/trustgraph/seed/seed.jsonl")
OUTPUT_SUMMARY = Path("/Users/clawdine/.openclaw/workspace/trustgraph/seed/summary.json")


def parse_front_matter(text: str):
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    fm = parts[1]
    data = {}
    for line in fm.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        data[key.strip()] = val.strip().strip('"')
    return data


def parse_skill_name(text: str):
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def load_skills():
    skills = []
    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        text = skill_md.read_text(encoding="utf-8", errors="ignore")
        fm = parse_front_matter(text)
        name = fm.get("name") or parse_skill_name(text) or skill_dir.name
        description = fm.get("description")
        skills.append({
            "dir": skill_dir.name,
            "name": name,
            "description": description,
            "version": None,
            "author": None,
            "source_url": None,
        })
    return skills


def load_threats():
    threats = []
    threats_path = SKILLS_DIR / "clawdsure.bak" / "threats.json"
    if threats_path.exists():
        try:
            threats = json.loads(threats_path.read_text(encoding="utf-8"))
        except Exception:
            threats = []
    return threats


def make_id(prefix, value):
    safe = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower())
    return f"{prefix}:{safe}"


def main():
    nodes = []
    edges = []

    skills = load_skills()
    for s in skills:
        skill_id = make_id("skill", s["name"])
        nodes.append({
            "type": "node",
            "label": "Skill",
            "id": skill_id,
            "properties": {
                "name": s["name"],
                "version": s["version"],
                "author": s["author"],
                "source_url": s["source_url"],
                "description": s["description"],
                "dir": s["dir"],
            },
        })

    threats = load_threats()
    for t in threats:
        threat_id = make_id("threat", t.get("id", "unknown"))
        nodes.append({
            "type": "node",
            "label": "Threat",
            "id": threat_id,
            "properties": {
                "id": t.get("id"),
                "type": t.get("category"),
                "severity": t.get("severity"),
                "description": t.get("detail") or t.get("title"),
                "date": t.get("published_at"),
                "confidence": t.get("confidence"),
                "action": t.get("action"),
                "title": t.get("title"),
            },
        })
        src = t.get("source")
        if src:
            source_id = make_id("source", src)
            nodes.append({
                "type": "node",
                "label": "Source",
                "id": source_id,
                "properties": {
                    "url": None,
                    "platform": src,
                },
            })
            edges.append({
                "type": "edge",
                "label": "REPORTED_BY",
                "from": threat_id,
                "to": source_id,
                "properties": {},
            })

    # Deduplicate nodes by id
    dedup = {}
    for n in nodes:
        dedup[n["id"]] = n
    nodes = list(dedup.values())

    OUTPUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_JSONL.open("w", encoding="utf-8") as f:
        for n in nodes:
            f.write(json.dumps(n) + "\n")
        for e in edges:
            f.write(json.dumps(e) + "\n")

    OUTPUT_SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_SUMMARY.write_text(json.dumps({
        "skills": skills,
        "threats": threats,
        "counts": {
            "skills": len(skills),
            "threats": len(threats),
            "nodes": len(nodes),
            "edges": len(edges),
        }
    }, indent=2))


if __name__ == "__main__":
    main()
