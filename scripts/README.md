# Automated Architectural PDF Publisher (`publish_pdf.py`)

## Overview

`publish_pdf.py` is a deterministic, general-purpose documentation publishing utility. It compiles any Markdown architectural documentation suite (such as an Obsidian OKF v0.2 vault or a 5-tier Backbone cockpit) into a single, unified, navigable HTML book and exports it to a publication-grade PDF via headless Microsoft Edge or Google Chrome.

---

## Key Capabilities & Guarantees

1. **Dynamic Chapter Auto-Discovery**:
   - Automatically discovers numbered subdirectories (`00-Navigation/`, `01-Architecture-and-Seams/`, etc.) in natural numerical order.
   - Extracts chapter titles from YAML frontmatter (`title: "..."`) or the first `# Heading`.
   - Generates an interactive Table of Contents with hyperlinked section bookmarks.

2. **Diagram Size & Width Control**:
   - **Zero Pandoc Escaping Corruption**: Extracts ````mermaid```` blocks *before* Pandoc parses Markdown, preventing HTML entity corruption (`--&gt;`, `&quot;`, `&lt;&lt;`) that causes Mermaid syntax crashes.
   - **Full-Page Responsive Vector SVGs**: Forces `.mermaid svg { width: 100% !important; max-width: 100% !important; height: auto !important; }` combined with `useMaxWidth: false`, allowing diagrams to expand to the full printable width of the A4 page.
   - **Token Neutralization**: Automatically sanitizes illegal tokens inside node labels (`<<Protocol>>`, `<<interface>>`, `<<Abstract>>` are neutralized to `Protocol:`, `Interface:`, `Abstract:`).
   - **Click Transmutation**: Automatically rewrites Obsidian wikilinks inside Mermaid click statements (`click Node href "[[...]]"`) into clean internal PDF anchors (`click Node href "#ch-..."`).

3. **Internal Wikilink Transmutation**:
   - Automatically converts all `[[Target|Label]]` and `[[Target]]` links into internal jump anchors (`<a href="#ch-target">Label</a>`), creating a fully hyperlinked, cross-referenced document.

4. **100% Offline & Hermetic**:
   - Bundles local `assets/book_style.css` and `assets/mermaid.min.js` (3.3 MB offline engine). Zero CDN or network dependencies during compilation.

---

## Installation & Prerequisites

`publish_pdf.py` requires:
* **Python 3.10+**
* **Pandoc**: `pandoc` must be installed and on your system `PATH` (used for clean Markdown $\to$ HTML table & typography parsing).
* **Microsoft Edge or Google Chrome**: Standard browser installed (used in headless mode for vector PDF printing).

---

## Directory Structure

```
.codegraph/scripts/
├── publish_pdf.py             # Master publisher script
├── README.md                  # Documentation and sizing guide
└── assets/
    ├── book_style.css         # Publication-grade print CSS (A4 margins, typography, tables)
    └── mermaid.min.js         # Offline bundled Mermaid 10 vector engine
```

---

## Usage

### Basic Execution
Run directly from the root of the repository:

```bash
python .codegraph/scripts/publish_pdf.py
```

### Custom Arguments & Generalization to Any Repository
Pass custom parameters to publish any codebase documentation:

```bash
python .codegraph/scripts/publish_pdf.py \
  --backbone-dir "path/to/documentation/folder" \
  --output "path/to/export/My-Project-Architecture.pdf" \
  --title "My Project Name" \
  --subtitle "System Architecture, Data Contracts & Operational Specification" \
  --badge "Technical Reference Manual" \
  --repo "my-org/my-repository"
```

### Command-Line Arguments Reference

| Argument | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--backbone-dir` | `Path` | `.codegraph/67-obsidian_vault/DATAVIEW/Backbone` | Directory containing the documentation subfolders. |
| `--output` | `Path` | `.../Backbone-Architecture-Guide.pdf` | Destination PDF path. |
| `--assets-dir` | `Path` | `.codegraph/scripts/assets` | Path to `book_style.css` and `mermaid.min.js`. |
| `--title` | `str` | `"Agent Governance Framework"` | Title displayed on cover page and headers. |
| `--subtitle` | `str` | `"Architectural Backbone..."` | Subtitle displayed on cover page. |
| `--badge` | `str` | `"Technical Specification & Reference Guide"` | Badge text above cover title. |
| `--repo` | `str` | `"67-Agent-Governance-Framework-CODE"` | Repository name printed in metadata block. |

---

## Diagram Sizing & Aspect Ratio Guidelines for Authors

To guarantee that diagrams render large, crisp, and readable on an A4 page without shrinking into micro-print or stretching into tall skinny columns, follow these 3 authoring rules:

### Rule 1: The Golden Aspect Ratio ($0.35 \le H/W \le 1.0$)
* In print, an A4 page width is approximately **$186\text{ mm}$** of printable area ($~750\text{--}950\text{ px}$ in layout engine terms).
* A diagram with $W \approx 800\text{--}1000\text{ px}$ and $H \approx 300\text{--}500\text{ px}$ renders at **100% native scale**.
* **Anti-Pattern (Ultra-Wide Strip)**: A diagram that is $1800\text{ px}$ wide and only $400\text{ px}$ high (aspect ratio $< 0.25$) will be forced to downscale by **$50\%\text{--}60\%$** to fit on the page, rendering text unreadable.  
  *Fix*: Split wide class hierarchies into focused subsystem diagrams (e.g. *Perception Contracts* and *Governance Contracts*).
* **Anti-Pattern (Tall Skinny Tower)**: A vertical flowchart with 10+ items chained top-to-bottom ($W \approx 500\text{ px}, H \approx 900\text{ px}$) creates large empty white margins on both sides.  
  *Fix*: Use top-down subgraphs side-by-side (`P1 & P2 & P3`) with `direction TB` inside each subgraph.

### Rule 2: Flowchart Orientation
* For multi-phase pipelines (e.g. Phase 1, Phase 2, Phase 3), use:
  ```mermaid
  flowchart TD
      Root --> P1 & P2 & P3
      subgraph P1 ["Phase 1"]
          direction TB
          A --> B
      end
      subgraph P2 ["Phase 2"]
          direction TB
          C --> D
      end
      subgraph P3 ["Phase 3"]
          direction TB
          E --> F
      end
  ```
  This creates a balanced 3-column grid that naturally spans the entire page width.

### Rule 3: Avoid Reserved Stereotype Delimiters in Labels
* Do **not** use `<<Protocol>>`, `<<interface>>`, or `<<Abstract>>` inside flowchart node labels (`Doc["<<Protocol>> Extractor"]`) or inside class attribute braces.
* Use clean prefixes instead: `Doc["Protocol: Extractor"]` or `class Extractor { +extract() }`.
