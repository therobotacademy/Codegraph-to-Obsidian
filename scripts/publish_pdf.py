#!/usr/bin/env python3
"""
publish_pdf.py — Generalized, deterministic documentation publisher.

Compiles any Markdown architectural documentation (e.g. Obsidian OKF v0.2 / Backbone)
into a unified, navigable HTML book and exports it to a publication-grade PDF
using headless Microsoft Edge.

Features:
- Dynamic chapter auto-discovery across numbered subdirectories.
- Robust Mermaid size and full-width control (prevents Pandoc HTML escaping and micro-scaling).
- Full internal wikilink-to-anchor transmutation.
- Self-contained offline assets (CSS + Mermaid.js).
- Interactive Table of Contents & PDF Bookmarks.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_EDGE_PATHS = [
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
]

def find_browser_exe() -> Path:
    for p in DEFAULT_EDGE_PATHS:
        if p.exists():
            return p
    # Try finding in PATH
    for name in ["msedge.exe", "chrome.exe", "google-chrome", "chromium"]:
        found = shutil.which(name)
        if found:
            return Path(found)
    raise FileNotFoundError("Could not find Microsoft Edge or Google Chrome executable for PDF printing.")

def make_slug(name_or_path: str) -> str:
    name = Path(name_or_path).stem
    return re.sub(r'[^a-zA-Z0-9]+', '-', name).strip('-').lower()

def extract_title_from_md(content: str, default_name: str) -> str:
    # Check YAML frontmatter: title: "..."
    fm_match = re.search(r"^---\n(.*?)\n---", content, re.DOTALL)
    if fm_match:
        for line in fm_match.group(1).splitlines():
            if line.startswith("title:"):
                return line.split(":", 1)[1].strip().strip('"').strip("'")
    
    # Check first # Heading
    for line in content.splitlines():
        if line.startswith("# ") and not line.startswith("##"):
            return line.replace("# ", "").strip()
            
    # Default fallback to filename
    clean_name = re.sub(r"^\d+[\-_]?", "", default_name)
    return clean_name.replace("-", " ").replace("_", " ").title()

def auto_discover_chapters(backbone_dir: Path):
    """
    Dynamically discover all chapters in the backbone directory:
    - Finds subfolders matching '00-*', '01-*', etc. in numerical order.
    - Inside each, finds .md files.
    - If no subfolders exist, uses all .md files in the root folder.
    """
    chapters = []
    
    subdirs = sorted([d for d in backbone_dir.iterdir() if d.is_dir() and not d.name.startswith((".", "_", "EXPORT"))])
    numbered_subdirs = [d for d in subdirs if re.match(r"^\d+", d.name)]
    
    dirs_to_scan = numbered_subdirs if numbered_subdirs else (subdirs if subdirs else [backbone_dir])
    
    chapter_num = 1
    for d in dirs_to_scan:
        md_files = sorted([f for f in d.glob("*.md") if f.is_file() and f.name.lower() != "index.md"])
        for md_file in md_files:
            rel_path = md_file.relative_to(backbone_dir).as_posix()
            content = md_file.read_text(encoding="utf-8", errors="ignore")
            title = extract_title_from_md(content, md_file.stem)
            chapter_label = f"{chapter_num:02d}. {title}"
            chapters.append((rel_path, chapter_label))
            chapter_num += 1
            
    return chapters

def clean_mermaid_code(code: str) -> str:
    """
    Sanitizes Mermaid code to prevent parsing crashes and control sizing:
    1. Rewrites Obsidian wikilinks inside click statements to HTML anchors.
    2. Neutralizes reserved token collisions (e.g. <<Protocol>> -> Protocol:).
    """
    def click_replacer(match):
        node_id = match.group(1)
        raw_target = match.group(2)
        target_name = Path(raw_target.split('|')[0]).stem
        slug = make_slug(target_name)
        return f'click {node_id} href "#ch-{slug}"'

    cleaned = re.sub(r'click\s+(\w+)\s+href\s+"\[\[([^\]]+)\]\]"', click_replacer, code)
    cleaned = re.sub(r'click\s+(\w+)\s+href\s+"\[([^\]]+)\]\([^)]+\)"', r'click \1 href "#ch-\1"', cleaned)
    
    # Neutralize invalid double angle-bracket stereotypes in labels
    cleaned = re.sub(r'<<Protocol>>', 'Protocol:', cleaned)
    cleaned = re.sub(r'<<interface>>', 'Interface:', cleaned)
    cleaned = re.sub(r'<<Abstract>>', 'Abstract:', cleaned)
    
    return cleaned.strip()

def process_markdown_file(file_path: Path):
    raw_md = file_path.read_text(encoding="utf-8")
    
    # 1. Remove YAML frontmatter
    md = re.sub(r"^---\n.*?\n---\n", "", raw_md, flags=re.DOTALL)
    
    # 2. Remove breadcrumbs to index
    md = re.sub(r">\s*\[\[.*?Back to Backbone Index\]\]\n*", "", md)
    
    # 3. Suppress raw ```dataview blocks in favor of pre-rendered tables
    md = re.sub(
        r"```dataview\n.*?\n```",
        "> [!NOTE]\n> *Live Obsidian Dataview telemetry is active in Obsidian. In this static export, the complete verified reference catalog is rendered in the table below.*",
        md,
        flags=re.DOTALL
    )
    
    # 4. Extract Mermaid blocks BEFORE Pandoc HTML-escapes them
    mermaid_blocks = []
    def mermaid_placeholder(match):
        code = match.group(1)
        idx = len(mermaid_blocks)
        cleaned_code = clean_mermaid_code(code)
        mermaid_blocks.append(cleaned_code)
        return f"\n\n<!-- MERMAID_BLOCK_{idx} -->\n\n"
        
    md = re.sub(r"```mermaid\n(.*?)```", mermaid_placeholder, md, flags=re.DOTALL)
    
    # 5. Rewrite Obsidian wikilinks to internal chapter anchors
    def link_replacer(match):
        full = match.group(1).strip()
        label = match.group(2).strip() if match.group(2) else ""
        
        target_name = Path(full).stem
        slug = make_slug(target_name)
        display = label if label else target_name
        return f"[{display}](#ch-{slug})"
        
    md = re.sub(r"\[\[([^\]\|]+)(?:\|([^\]]+))?\]\]", link_replacer, md)
    
    # 6. Convert Markdown chunk to HTML using Pandoc
    pandoc_cmd = ["pandoc", "-f", "markdown+pipe_tables+gfm_auto_identifiers", "-t", "html"]
    proc = subprocess.run(pandoc_cmd, input=md, text=True, capture_output=True, encoding="utf-8")
    if proc.returncode != 0:
        html_output = f"<pre>{md}</pre>"
    else:
        html_output = proc.stdout
        
    # 7. Re-inject pristine unescaped Mermaid divs with full-width responsive wrapper
    for idx, code in enumerate(mermaid_blocks):
        placeholder = f"<!-- MERMAID_BLOCK_{idx} -->"
        mermaid_html = f'<div class="mermaid-container"><div class="mermaid">\n{code}\n</div></div>'
        html_output = html_output.replace(placeholder, mermaid_html)
        html_output = html_output.replace(f"<p>{placeholder}</p>", mermaid_html)
        
    return html_output

def publish(
    backbone_dir: Path,
    output_pdf: Path,
    assets_dir: Path,
    title: str = "Architectural Backbone Guide",
    subtitle: str = "Technical Architecture, Boundary Contracts & Runtime Specification",
    badge: str = "Technical Reference Manual",
    repo_name: str = "",
    keep_html: bool = True
):
    print(f"=== PUBLISHING ARCHITECTURAL BOOK ===")
    print(f"Source Backbone Directory: {backbone_dir}")
    print(f"Output PDF Target:         {output_pdf}")
    print(f"Assets Directory:          {assets_dir}")
    
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    
    # Auto-discover chapters
    chapters = auto_discover_chapters(backbone_dir)
    print(f"Discovered {len(chapters)} chapters:")
    for rel, name in chapters:
        print(f"  [{rel}] -> {name}")
        
    rendered_chapters = []
    toc_items = []
    
    for rel_path, chapter_title in chapters:
        file_path = backbone_dir / rel_path
        if not file_path.exists():
            continue
            
        slug = make_slug(rel_path)
        toc_items.append((slug, chapter_title))
        
        chapter_html = process_markdown_file(file_path)
        section = f"""
        <section class="chapter" id="ch-{slug}">
            {chapter_html}
        </section>
        """
        rendered_chapters.append(section)

    toc_html = "\n".join([
        f'<div class="toc-item"><a href="#ch-{s}" class="part-name">{t}</a><span class="part-desc">#ch-{s}</span></div>'
        for s, t in toc_items
    ])

    # Copy assets to output directory if needed
    dest_assets = output_pdf.parent / "assets"
    dest_assets.mkdir(parents=True, exist_ok=True)
    if assets_dir.exists():
        for asset in assets_dir.glob("*"):
            shutil.copy(asset, dest_assets / asset.name)

    repo_str = f"<p><strong>Repository</strong>: <code>{repo_name}</code></p>" if repo_name else ""

    book_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <link rel="stylesheet" href="assets/book_style.css">
    <script src="assets/mermaid.min.js"></script>
    <script>
      document.addEventListener("DOMContentLoaded", function() {{
        mermaid.initialize({{
          startOnLoad: true,
          theme: 'neutral',
          securityLevel: 'loose',
          fontFamily: "'Segoe UI', -apple-system, sans-serif",
          themeVariables: {{
            fontSize: "14px",
            fontFamily: "'Segoe UI', -apple-system, sans-serif"
          }},
          flowchart: {{
            useMaxWidth: false,
            htmlLabels: true,
            nodeSpacing: 45,
            rankSpacing: 45
          }},
          sequence: {{
            useMaxWidth: false,
            actorWidth: 140,
            messageMargin: 35
          }},
          state: {{
            useMaxWidth: false
          }},
          class: {{
            useMaxWidth: false
          }}
        }});
      }});
    </script>
</head>
<body>

<!-- Cover Page -->
<div class="cover-page">
    <div class="badge">{badge}</div>
    <div class="cover-title">{title}</div>
    <div class="cover-subtitle">{subtitle}</div>
    <div class="cover-meta">
        {repo_str}
        <p><strong>Published Date</strong>: August 2026</p>
        <p><strong>Published By</strong>: <code>publish_pdf.py</code></p>
    </div>
</div>

<!-- Table of Contents -->
<div class="toc-section">
    <div class="toc-title">Table of Contents</div>
    <div class="toc-grid">
        {toc_html}
    </div>
</div>

<!-- Chapters Body -->
{"".join(rendered_chapters)}

</body>
</html>
"""
    output_html = output_pdf.parent / (output_pdf.stem + ".html")
    output_html.write_text(book_html, encoding="utf-8")
    print(f"HTML book written to {output_html} ({len(book_html)} bytes)")

    # Print to PDF using Headless Browser
    browser_exe = find_browser_exe()
    print(f"Rendering PDF with: {browser_exe}...")
    
    edge_args = [
        str(browser_exe),
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=8000",
        f"--print-to-pdf={str(output_pdf)}",
        f"file:///{output_html.resolve().as_posix()}"
    ]
    
    res = subprocess.run(edge_args, capture_output=True, text=True)
    if output_pdf.exists() and output_pdf.stat().st_size > 10000:
        print(f"SUCCESS: Publication PDF generated at {output_pdf} ({output_pdf.stat().st_size} bytes)")
    else:
        print(f"ERROR: PDF generation failed or empty. Stderr: {res.stderr}")
        sys.exit(1)
        
    if not keep_html:
        output_html.unlink(missing_ok=True)

def main():
    parser = argparse.ArgumentParser(description="Deterministic Architectural PDF Publisher")
    parser.add_argument("--backbone-dir", type=Path, default=Path(".codegraph/67-obsidian_vault/DATAVIEW/Backbone"), help="Backbone folder")
    parser.add_argument("--output", type=Path, default=Path(".codegraph/67-obsidian_vault/DATAVIEW/EXPORT/Backbone-Architecture-Guide.pdf"), help="Output PDF path")
    parser.add_argument("--assets-dir", type=Path, default=Path(__file__).resolve().parent / "assets", help="Assets folder (CSS, JS)")
    parser.add_argument("--title", type=str, default="Agent Governance Framework", help="Book title")
    parser.add_argument("--subtitle", type=str, default="Architectural Backbone, Authority Boundaries & Audit Specification", help="Subtitle")
    parser.add_argument("--badge", type=str, default="Technical Specification & Reference Guide", help="Cover badge")
    parser.add_argument("--repo", type=str, default="67-Agent-Governance-Framework-CODE", help="Repository name")
    
    args = parser.parse_args()
    publish(
        backbone_dir=args.backbone_dir,
        output_pdf=args.output,
        assets_dir=args.assets_dir,
        title=args.title,
        subtitle=args.subtitle,
        badge=args.badge,
        repo_name=args.repo
    )

if __name__ == "__main__":
    main()
