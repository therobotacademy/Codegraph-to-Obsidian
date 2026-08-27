#!/usr/bin/env python3
"""
Survey an OKF v0.2 CodeGraph vault to catalog all symbols for the Backbone Cockpit.
"""
import argparse
import sys
from pathlib import Path

def survey_vault(vault_path: Path):
    classes = []
    functions = []
    variables = []
    
    for p in vault_path.rglob("*.md"):
        if not p.is_file():
            continue
        try:
            content = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        
        lines = content.splitlines()
        node_type = ""
        fpath = ""
        title = p.stem
        start = ""
        desc = ""
        
        for line in lines:
            if line.startswith("type:"):
                node_type = line.split(":", 1)[1].strip().strip('"')
            elif line.startswith("file_path:"):
                fpath = line.split(":", 1)[1].strip().strip('"')
            elif line.startswith("title:"):
                title = line.split(":", 1)[1].strip().strip('"')
            elif line.startswith("start_line:"):
                start = line.split(":", 1)[1].strip()
            elif line.startswith("description:"):
                desc = line.split(":", 1)[1].strip().strip('"')
                
        line_num = int(start) if start.isdigit() else 0
        
        if node_type == "code/class":
            classes.append((fpath, line_num, title, desc, p.relative_to(vault_path).as_posix()))
        elif node_type == "code/function":
            functions.append((fpath, line_num, title, desc, p.relative_to(vault_path).as_posix()))
        elif node_type == "code/variable":
            variables.append((fpath, line_num, title, desc, p.relative_to(vault_path).as_posix()))

    classes.sort(key=lambda x: (x[0], x[1]))
    functions.sort(key=lambda x: (x[0], x[1]))
    variables.sort(key=lambda x: (x[0], x[1]))

    print(f"=== VAULT SURVEY: {vault_path} ===")
    print(f"Total Classes:   {len(classes)}")
    print(f"Total Functions: {len(functions)}")
    print(f"Total Variables: {len(variables)}")
    
    # Identify potential Protocols / Interfaces
    protocols = [c for c in classes if "protocol" in c[3].lower() or "interface" in c[3].lower() or "abstract" in c[3].lower()]
    print(f"\nPotential Protocols / Interfaces ({len(protocols)}):")
    for fp, sl, t, d, _ in protocols:
        print(f"  {t} ({fp}#L{sl})")
        
    # Identify custom exceptions
    exceptions = [c for c in classes if "error" in c[2].lower() or "exception" in c[2].lower()]
    print(f"\nPotential Custom Exceptions ({len(exceptions)}):")
    for fp, sl, t, d, _ in exceptions:
        print(f"  {t} ({fp}#L{sl})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Survey OKF v0.2 vault")
    parser.add_argument("--vault-path", type=Path, default=Path(".codegraph/67-obsidian_vault"), help="Path to vault")
    args = parser.parse_args()
    survey_vault(args.vault_path)
