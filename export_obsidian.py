#!/usr/bin/env python3
"""Export CodeGraph SQLite database (.codegraph/codegraph.db) into an Obsidian vault.

Organizes notes into folders mirroring the source code structure, where the
innermost folder is the source file (e.g. `src/govagent/engine.py/`), formats
each node according to OKF v0.2, assigns semantic colors per type in frontmatter,
and writes native Obsidian graph view configuration (`.obsidian/graph.json`).
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import re
import sqlite3
from pathlib import Path
from typing import Any

FORBIDDEN_CHARS_PATTERN = re.compile(r'[<>:"/\\|?*]')

TYPE_COLORS: dict[str, str] = {
    "index": "#94A3B8",
    "code/file": "#EB082E",
    "code/class": "#F59E0B",
    "code/function": "#06B6D4",
    "code/method": "#0BFEAD",
    "code/variable": "#F7FF0E",
}


def hex_to_rgb_int(hex_code: str) -> int:
    h = hex_code.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (r << 16) + (g << 8) + b


def sanitize_filename(name: str) -> str:
    """Sanitizes qualified names into filesystem-safe note names."""
    sanitized = FORBIDDEN_CHARS_PATTERN.sub(".", name)
    sanitized = re.sub(r"\.+", ".", sanitized).strip(". ")
    return sanitized or "unnamed_node"


def write_obsidian_graph_config(output_dir: Path) -> None:
    obsidian_dir = output_dir / ".obsidian"
    obsidian_dir.mkdir(parents=True, exist_ok=True)
    graph_config = {
        "collapse-filter": False,
        "search": "",
        "localJumps": 1,
        "localBacklinks": True,
        "localForelinks": True,
        "localInterlinks": False,
        "showTags": False,
        "showAttachments": False,
        "hideUnresolved": False,
        "collapse-color-groups": False,
        "colorGroups": [
            {
                "query": "tag:#code/class",
                "color": {"a": 1, "rgb": hex_to_rgb_int(TYPE_COLORS["code/class"])},
            },
            {
                "query": "tag:#code/function",
                "color": {"a": 1, "rgb": hex_to_rgb_int(TYPE_COLORS["code/function"])},
            },
            {
                "query": "tag:#code/method",
                "color": {"a": 1, "rgb": hex_to_rgb_int(TYPE_COLORS["code/method"])},
            },
            {
                "query": "tag:#code/file",
                "color": {"a": 1, "rgb": hex_to_rgb_int(TYPE_COLORS["code/file"])},
            },
            {
                "query": "tag:#code/variable",
                "color": {"a": 1, "rgb": hex_to_rgb_int(TYPE_COLORS["code/variable"])},
            },
            {
                "query": "tag:#index",
                "color": {"a": 1, "rgb": hex_to_rgb_int(TYPE_COLORS["index"])},
            },
        ],
        "collapse-display": False,
        "showArrow": True,
        "textFadeMultiplier": 0,
        "nodeSizeMultiplier": 1.1,
        "lineSizeMultiplier": 1,
    }
    (obsidian_dir / "graph.json").write_text(json.dumps(graph_config, indent=2), encoding="utf-8")


def export_codegraph_to_obsidian(
    db_path: Path,
    output_dir: Path,
    include_variables: bool = False,
    include_incoming_links: bool = True,
) -> int:
    if not db_path.exists():
        raise FileNotFoundError(f"CodeGraph DB not found at: {db_path.resolve()}")

    output_dir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    allowed_kinds = ["class", "function", "method", "file"]
    if include_variables:
        allowed_kinds.append("variable")

    placeholders = ",".join("?" for _ in allowed_kinds)
    query_nodes = f"SELECT * FROM nodes WHERE kind IN ({placeholders})"
    raw_nodes = conn.execute(query_nodes, allowed_kinds).fetchall()

    nodes: dict[str, dict[str, Any]] = {row["id"]: dict(row) for row in raw_nodes}
    if not nodes:
        return 0

    now_iso = datetime.now(timezone.utc).isoformat()

    note_rel_paths: dict[str, Path] = {}
    for nid, n in nodes.items():
        file_folder = Path(n["file_path"])
        if n["kind"] == "file":
            rel_path = file_folder / "index.md"
        else:
            symbol_filename = sanitize_filename(n["name"])
            if n.get("signature") and "(" in n["signature"]:
                qparts = (n.get("qualified_name") or "").split(":")[-1].split(".")
                if len(qparts) > 1:
                    symbol_filename = sanitize_filename(".".join(qparts[-2:]))
            rel_path = file_folder / f"{symbol_filename}.md"
        note_rel_paths[nid] = rel_path

    node_ids = list(nodes.keys())
    chunk_size = 900
    edges: list[sqlite3.Row] = []
    for i in range(0, len(node_ids), chunk_size):
        chunk = node_ids[i : i + chunk_size]
        q = f"SELECT source, target, kind FROM edges WHERE source IN ({','.join('?' for _ in chunk)})"
        edges.extend(conn.execute(q, chunk).fetchall())

    outgoing: dict[str, list[tuple[str, str]]] = {nid: [] for nid in nodes}
    incoming: dict[str, list[tuple[str, str]]] = {nid: [] for nid in nodes}

    for edge in edges:
        src, tgt, kind = edge["source"], edge["target"], edge["kind"]
        if src in nodes and tgt in nodes:
            outgoing[src].append((kind, tgt))
            incoming[tgt].append((kind, src))

    count = 0
    for nid, n in nodes.items():
        rel_path = note_rel_paths[nid]
        note_file = output_dir / rel_path
        note_file.parent.mkdir(parents=True, exist_ok=True)

        links_by_kind: dict[str, list[str]] = {}
        for kind, tgt_id in outgoing[nid]:
            target_rel = note_rel_paths[tgt_id].as_posix().removesuffix(".md")
            target_symbol = nodes[tgt_id]["name"]
            links_by_kind.setdefault(kind, []).append(
                f"[[{target_rel}|{target_symbol}]]"
            )

        backlinks_by_kind: dict[str, list[str]] = {}
        if include_incoming_links:
            for kind, src_id in incoming[nid]:
                source_rel = note_rel_paths[src_id].as_posix().removesuffix(".md")
                source_symbol = nodes[src_id]["name"]
                backlinks_by_kind.setdefault(kind, []).append(
                    f"[[{source_rel}|{source_symbol}]]"
                )

        docstring = (n.get("docstring") or "").strip()
        first_line_desc = docstring.splitlines()[0] if docstring else f"{n['kind']} {n['name']}"
        escaped_desc = first_line_desc.replace('"', '\\"')

        node_type = f"code/{n['kind']}"
        node_color = TYPE_COLORS.get(node_type, "#94A3B8")

        frontmatter = [
            "---",
            "okf_version: \"0.2\"",
            f"type: \"{node_type}\"",
            f"title: \"{n['name']}\"",
            f"description: \"{escaped_desc}\"",
            f"color: \"{node_color}\"",
            f"resource: \"file:///{n['file_path']}#L{n['start_line']}-L{n['end_line']}\"",
            f"id: \"{nid}\"",
            f"file_path: \"{n['file_path']}\"",
            f"start_line: {n['start_line']}",
            f"end_line: {n['end_line']}",
            "provenance: \"codegraph.db\"",
            "verified: true",
            "status: \"active\"",
            f"updated: \"{now_iso}\"",
            "tags:",
            f"  - {node_type}",
            "aliases:",
            f"  - \"{n['name']}\"",
        ]
        if n.get("qualified_name") and n["qualified_name"] != n["name"]:
            frontmatter.append(f"  - \"{n['qualified_name']}\"")
        frontmatter.append("---\n")

        body = [
            f"# `{n['name']}`\n",
            f"**Type**: `{n['kind']}` | **Source**: [{n['file_path']}#L{n['start_line']}-L{n['end_line']}](file:///{n['file_path']}#L{n['start_line']}-L{n['end_line']})\n",
        ]

        if n.get("signature"):
            sig = n["signature"].strip()
            body.append(f"```python\n{sig}\n```\n")

        if docstring:
            quoted_doc = "\n".join(f"> {line}" for line in docstring.replace("\r\n", "\n").splitlines())
            body.append(f"{quoted_doc}\n")

        if links_by_kind:
            body.append("## Outgoing Relationships\n")
            for kind in sorted(links_by_kind.keys()):
                body.append(f"### {kind.capitalize()}")
                for target_link in sorted(set(links_by_kind[kind])):
                    body.append(f"- {target_link}")
                body.append("")

        if backlinks_by_kind:
            body.append("## Incoming References\n")
            for kind in sorted(backlinks_by_kind.keys()):
                body.append(f"### {kind.capitalize()} by")
                for source_link in sorted(set(backlinks_by_kind[kind])):
                    body.append(f"- {source_link}")
                body.append("")

        note_file.write_text("\n".join(frontmatter) + "\n" + "\n".join(body), encoding="utf-8")
        count += 1

    # Root index.md
    index_file = output_dir / "index.md"
    index_content = [
        "---",
        "okf_version: \"0.2\"",
        "type: \"index\"",
        "title: \"Codebase Knowledge Graph Index\"",
        "description: \"OKF v0.2 knowledge graph generated from CodeGraph SQLite DB.\"",
        f"color: \"{TYPE_COLORS['index']}\"",
        "provenance: \"codegraph.db\"",
        "verified: true",
        "status: \"active\"",
        f"updated: \"{now_iso}\"",
        "tags: [index, codegraph, okf]",
        "---",
        "# Codebase Knowledge Graph\n",
        f"- **Total Nodes**: {count}",
        f"- **Database**: `{db_path.name}`",
        f"- **Codebase Path**: `{db_path.parent.parent.resolve()}`\n",
        "## Navigation\n",
        "- Navigate folders by code layout (`<directory>/<filename.ext>/<symbol>.md`).",
        "- Use the Obsidian Graph View (`Ctrl + G`) to inspect relationship clusters.",
    ]
    index_file.write_text("\n".join(index_content), encoding="utf-8")

    # Native graph view settings
    write_obsidian_graph_config(output_dir)

    return count


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export .codegraph/codegraph.db into an OKF v0.2 Obsidian vault."
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=Path(__file__).parent / "codegraph.db",
        help="Path to codegraph.db (default: .codegraph/codegraph.db)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).parent / "obsidian_vault",
        help="Output directory for Obsidian vault (default: ./.codegraph/obsidian_vault)",
    )
    parser.add_argument(
        "--include-vars",
        action="store_true",
        help="Include variable nodes",
    )
    parser.add_argument(
        "--no-incoming",
        action="store_true",
        help="Do not generate incoming references sections",
    )

    args = parser.parse_args()

    total = export_codegraph_to_obsidian(
        db_path=args.db,
        output_dir=args.out,
        include_variables=args.include_vars,
        include_incoming_links=not args.no_incoming,
    )
    print(f"Exported {total} OKF v0.2 notes with color definitions to {args.out.resolve()}")


if __name__ == "__main__":
    main()
