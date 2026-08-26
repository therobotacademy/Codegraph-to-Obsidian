
# CodeGraph to Obsidian Vault Exporter

Exports the CodeGraph SQLite property graph (`.codegraph/codegraph.db`) into an [Obsidian](https://obsidian.md/) markdown vault conforming to the **Open Knowledge Format (OKF) v0.2** specification.

---

## CodeGraph Installation & Usage

Based on the [CodeGraph Installation Guide](https://colbymchenry.github.io/codegraph/getting-started/installation/) and [First Graph Guide](https://colbymchenry.github.io/codegraph/getting-started/your-first-graph/).

### 1. Install CodeGraph

#### Interactive Installer

Runs the guided wizard, auto-detects installed coding agents (Claude Code, Cursor, Codex CLI, Antigravity IDE, Gemini CLI, etc.), installs `codegraph` to `PATH`, and wires MCP configurations:

```bash
npx @colbymchenry/codegraph
```

#### Without Node.js

```PowerShell
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | sh

# Windows (PowerShell)
irm https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.ps1 | iex
```

#### Non-Interactive (Scripting / CI)

```bash
codegraph install --yes                         # Auto-detect agents, install globally
codegraph install --target=cursor,claude --yes  # Explicit target list
codegraph install --target=auto --location=local # Project-local configuration
codegraph install --print-config codex          # Print snippet without file writes
```

#### Restart Agent

Restart your agent / IDE (e.g. Antigravity IDE, Claude Code, Cursor) so the new MCP server is recognized.

---

### 2. Index a Project

Initialize CodeGraph at your repository root to create `.codegraph/` and build the full graph in one step:

```bash
codegraph init
```

A native file watcher maintains index synchronization automatically. When manual re-indexing is required:

```bash
codegraph index    # Full re-index
codegraph sync     # Incremental update of changed files
```

### 3. Check Status

Verify that the database is healthy and inspect node/edge counts:

```bash
codegraph status
```

### 4. Query the Graph

- **Exploration (Primary)**: Queries verbatim source and dynamic call paths in a single call:
  ```bash
  codegraph explore "how does Orchestrator work"
  codegraph explore "ApprovalAgent LangGraphApprovalAgent"
  ```
- **Focused Lookups** (all support `--json`):
  ```bash
  codegraph query Orchestrator         # Find symbols by name
  codegraph callers evaluate           # What calls a function/method
  codegraph callees evaluate           # What a function/method calls
  codegraph impact ApprovalAgent       # Blast radius / what a change affects
  ```

### 5. Agent / MCP Integration

When `.codegraph/` is present at the repository root, AI agents automatically discover and call the `codegraph_explore` MCP tool.

### 6. Uninstall

```bash
codegraph uninstall    # Removes MCP server configs and instructions from all agents
codegraph uninit       # Removes the local .codegraph/ directory and database
```

---

## Features

- **Folder Hierarchy**: Notes are structured according to source directories, with the source file (including extension) as the innermost folder:
  ```text
  obsidian_vault/
  ├── index.md                              # Root OKF v0.2 vault index
  ├── .obsidian/
  │   └── graph.json                        # Pre-configured color groups & graph view settings
  └── src/
      └── govagent/
          └── engine.py/                    # Folder for source file
              ├── index.md                  # File-level node (module summary & exported symbols)
              ├── Orchestrator.md           # Class node
              ├── Engine.md                 # Class node
              └── evaluate.md               # Function/method node
  ```
- **OKF v0.2 Metadata**: Every note includes standardized YAML frontmatter:
  ```yaml
  ---
  okf_version: "0.2"
  type: "code/class"
  title: "Orchestrator"
  description: "Lo que Engine necesita de un orquestador..."
  color: "#F59E0B"
  resource: "file:///src/govagent/engine.py#L36-L46"
  provenance: "codegraph.db"
  verified: true
  status: "active"
  tags:
    - code/class
  aliases:
    - "Orchestrator"
  ---
  ```
- **Bidirectional Links**:
  - `## Outgoing Relationships`: Grouped by relationship (`Calls`, `Instantiates`, `Extends`, `Contains`).
  - `## Incoming References`: Grouped by backlinks (`Called by`, `Instantiated by`, etc.).
- **Automatic Graph View Styling**: Writes `.obsidian/graph.json` so Obsidian's Graph View (`Ctrl + G`) immediately colors nodes.

---

## Semantic Color Palette

| Symbol Type                   | Tag                | Hex         | Color       |
| ----------------------------- | ------------------ | ----------- | ----------- |
| **Class / Protocol**    | `#code/class`    | `#F59E0B` | Warm Amber  |
| **Function**            | `#code/function` | `#06B6D4` | Cyan / Teal |
| **Method**              | `#code/method`   | `#38BDF8` | Sky Blue    |
| **File / Module**       | `#code/file`     | `#6366F1` | Deep Indigo |
| **Variable / Constant** | `#code/variable` | `#F43F5E` | Rose        |
| **Index**               | `#index`         | `#94A3B8` | Slate Gray  |

---

## Usage

### Quick Start

Run from the repository root:

```bash
python .codegraph/export_obsidian.py
```

### CLI Arguments

```text
options:
  -h, --help            Show help message and exit
  --db DB               Path to codegraph.db (default: .codegraph/codegraph.db)
  --out OUT             Output vault directory (default: ./obsidian_vault)
  --include-vars        Include variable nodes (omitted by default to reduce clutter)
  --no-incoming         Skip generating incoming reference sections
```

#### Examples

- **Export to a custom directory (`--out`)**:

  ```bash
  python .codegraph/export_obsidian.py --out ~/Documents/code_vault
  ```
- **Specify an alternate CodeGraph database path (`--db`)**:

  ```bash
  python .codegraph/export_obsidian.py --db /path/to/project/.codegraph/codegraph.db --out ./vault
  ```
- **Include module-level variables and constants (`--include-vars`)**:

  ```bash
  python .codegraph/export_obsidian.py --include-vars
  ```
- **Outbound links only, omit backlinks (`--no-incoming`)**:

  ```bash
  python .codegraph/export_obsidian.py --no-incoming
  ```
- **Combined invocation**:

  ```bash
  python .codegraph/export_obsidian.py --db .codegraph/codegraph.db --out ./docs/vault --include-vars --no-incoming
  ```

### Viewing in Obsidian

1. Open Obsidian.
2. Select **Open folder as vault** and choose the `obsidian_vault` directory.
3. Open the Graph View (`Ctrl + G` or `Cmd + G`) to inspect your codebase architecture.
