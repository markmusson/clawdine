#!/usr/bin/env python3
import json
import re
import time
from urllib.parse import quote
from urllib.request import Request, urlopen
from pathlib import Path

BASE = "https://clawhub.com"
SEED_JSONL = Path("/Users/clawdine/.openclaw/workspace/trustgraph/seed/seed.jsonl")
SUMMARY_JSON = Path("/Users/clawdine/.openclaw/workspace/trustgraph/seed/summary.json")
CATALOG_LOG = Path("/Users/clawdine/.openclaw/workspace/trustgraph/catalog-scan.md")


def fetch_text(url, timeout=60):
    req = Request(url, headers={"User-Agent": "openclaw-trustgraph-seed"})
    with urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    return data.decode("utf-8", errors="ignore")


def fetch_json(url, timeout=60):
    return json.loads(fetch_text(url, timeout=timeout))


def make_id(prefix, value):
    safe = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower())
    return f"{prefix}:{safe}"


def fetch_all_skills():
    items = []
    cursor = None
    while True:
        url = f"{BASE}/api/v1/skills?limit=200"
        if cursor:
            url += f"&cursor={quote(cursor)}"
        data = fetch_json(url)
        page_items = data.get("items") or []
        items.extend(page_items)
        cursor = data.get("nextCursor")
        if not cursor:
            break
    return items


def extract_install_deps(text):
    deps = []
    # Try to find install objects with kind + package/module/formula
    for match in re.finditer(r"\{[^{}]*\"kind\"\s*:\s*\"([^\"]+)\"[^{}]*\}", text):
        block = match.group(0)
        kind = match.group(1)
        pkg = None
        for key in ("package", "module", "formula"):
            m = re.search(rf"\"{key}\"\s*:\s*\"([^\"]+)\"", block)
            if m:
                pkg = m.group(1)
                break
        if pkg:
            registry = kind
            if kind == "node":
                registry = "npm"
            elif kind == "brew":
                registry = "brew"
            elif kind == "go":
                registry = "go"
            elif kind == "uv":
                registry = "pypi"
            deps.append((pkg, registry))
    # Optional generic dependencies list
    for m in re.finditer(r"dependencies\s*[:=]\s*\[([^\]]+)\]", text, re.IGNORECASE | re.DOTALL):
        inner = m.group(1)
        for item in re.finditer(r"\"([^\"]+)\"|'([^']+)'", inner):
            dep = item.group(1) or item.group(2)
            if dep:
                deps.append((dep, "unknown"))
    # Dedup preserving order
    seen = set()
    out = []
    for name, reg in deps:
        key = (name, reg)
        if key in seen:
            continue
        seen.add(key)
        out.append((name, reg))
    return out


def main():
    # Load existing threats from summary.json (if present)
    threats = []
    if SUMMARY_JSON.exists():
        try:
            summary = json.loads(SUMMARY_JSON.read_text(encoding="utf-8"))
            threats = summary.get("threats") or []
        except Exception:
            threats = []

    items = fetch_all_skills()
    skills = []
    nodes = []
    edges = []

    package_nodes = {}
    author_nodes = {}

    for idx, item in enumerate(items, 1):
        slug = item.get("slug") or "unknown"
        try:
            detail = fetch_json(f"{BASE}/api/v1/skills/{quote(slug)}")
        except Exception:
            detail = {}
        skill_meta = detail.get("skill") or {}
        latest_version = None
        if detail.get("latestVersion"):
            latest_version = detail["latestVersion"].get("version")
        if not latest_version and item.get("latestVersion"):
            latest_version = item["latestVersion"].get("version")

        name = skill_meta.get("displayName") or item.get("displayName") or slug
        description = skill_meta.get("summary") or item.get("summary")
        owner = detail.get("owner") or {}
        author = owner.get("handle") or owner.get("displayName")
        source_url = f"{BASE}/skills/{slug}"

        skills.append({
            "dir": slug,
            "name": name,
            "description": description,
            "version": latest_version,
            "author": author,
            "source_url": source_url,
        })

        skill_id = make_id("skill", name)
        nodes.append({
            "type": "node",
            "label": "Skill",
            "id": skill_id,
            "properties": {
                "name": name,
                "version": latest_version,
                "author": author,
                "source_url": source_url,
                "description": description,
                "dir": slug,
            },
        })

        if author:
            author_id = make_id("author", author)
            if author_id not in author_nodes:
                author_nodes[author_id] = {
                    "type": "node",
                    "label": "Author",
                    "id": author_id,
                    "properties": {
                        "name": author,
                        "platform_id": author,
                    },
                }
            edges.append({
                "type": "edge",
                "label": "PUBLISHED_BY",
                "from": skill_id,
                "to": author_id,
                "properties": {},
            })

        deps = []
        if latest_version:
            try:
                skill_md = fetch_text(
                    f"{BASE}/api/v1/skills/{quote(slug)}/file?path=SKILL.md&version={quote(latest_version)}",
                    timeout=60,
                )
                deps = extract_install_deps(skill_md)
            except Exception:
                deps = []

        for dep_name, registry in deps:
            pkg_id = make_id("package", f"{registry}:{dep_name}")
            if pkg_id not in package_nodes:
                package_nodes[pkg_id] = {
                    "type": "node",
                    "label": "Package",
                    "id": pkg_id,
                    "properties": {
                        "name": dep_name,
                        "version": None,
                        "registry": registry,
                    },
                }
            edges.append({
                "type": "edge",
                "label": "DEPENDS_ON",
                "from": skill_id,
                "to": pkg_id,
                "properties": {},
            })

        if idx % 100 == 0:
            time.sleep(0.2)

    # Add threat + source nodes/edges from existing summary
    for t in threats:
        threat_id = make_id("threat", t.get("id", "unknown"))
        nodes.append({
            "type": "node",
            "label": "Threat",
            "id": threat_id,
            "properties": {
                "id": t.get("id"),
                "type": t.get("category") or t.get("type"),
                "severity": t.get("severity"),
                "description": t.get("detail") or t.get("description") or t.get("title"),
                "date": t.get("published_at") or t.get("date"),
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
    for n in nodes + list(author_nodes.values()) + list(package_nodes.values()):
        dedup[n["id"]] = n
    nodes = list(dedup.values())

    SEED_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with SEED_JSONL.open("w", encoding="utf-8") as f:
        for n in nodes:
            f.write(json.dumps(n) + "\n")
        for e in edges:
            f.write(json.dumps(e) + "\n")

    SUMMARY_JSON.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_JSON.write_text(json.dumps({
        "skills": skills,
        "threats": threats,
        "counts": {
            "skills": len(skills),
            "threats": len(threats),
            "nodes": len(nodes),
            "edges": len(edges),
        }
    }, indent=2))

    CATALOG_LOG.write_text(
        "# ClawHub Catalog Scan\n\n"
        f"- Total skills: {len(skills)}\n"
        f"- Total authors: {len(author_nodes)}\n"
        f"- Total packages: {len(package_nodes)}\n"
        f"- Total dependency edges: {sum(1 for e in edges if e['label']=='DEPENDS_ON')}\n"
        f"- Total published-by edges: {sum(1 for e in edges if e['label']=='PUBLISHED_BY')}\n"
        "\n"
        f"- Registry: {BASE}\n"
    )


if __name__ == "__main__":
    main()
