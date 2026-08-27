#!/usr/bin/env python3
"""
Audit all Obsidian wikilinks inside an OKF v0.2 vault and assert zero broken links.
"""
import argparse
import re
import sys
from pathlib import Path

def audit_links(vault_path: Path, target_dir: Path):
    print(f"Auditing links in {target_dir} against {vault_path}...")
    broken = []
    checked = 0

    for file_path in target_dir.rglob("*"):
        if not file_path.is_file() or file_path.suffix not in (".md", ".canvas"):
            continue
            
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        # Extract [[link]] patterns
        links = re.findall(r"\[\[([^\]\|]+)", content)
        
        for link in links:
            link_clean = link.strip().rstrip("\\")
            checked += 1
            
            # 1. Exact match
            target = vault_path / link_clean
            # 2. Markdown extension match
            target_md = vault_path / (link_clean + ".md")
            # 3. Relative to current file
            target_rel = file_path.parent / link_clean
            target_rel_md = file_path.parent / (link_clean + ".md")
            
            exists = target.exists() or target_md.exists() or target_rel.exists() or target_rel_md.exists()
            
            if not exists:
                broken.append((file_path.relative_to(vault_path).as_posix(), link_clean))

    print(f"Total links inspected: {checked}")
    if broken:
        print(f"FAIL: Found {len(broken)} broken link(s):")
        for src, dest in broken:
            print(f"  In {src} ➔ [[{dest}]]")
        sys.exit(1)
    else:
        print("SUCCESS: 0 broken links! Vault graph integrity verified.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit vault links")
    parser.add_argument("--vault-path", type=Path, default=Path(".codegraph/67-obsidian_vault"))
    parser.add_argument("--target-dir", type=Path, default=Path(".codegraph/67-obsidian_vault/DATAVIEW/Backbone"))
    args = parser.parse_args()
    audit_links(args.vault_path, args.target_dir)
