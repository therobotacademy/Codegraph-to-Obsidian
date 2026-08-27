# CodeGraph to Obsidian Vault Exporter

Exports the CodeGraph SQLite property graph (`.codegraph/codegraph.db`) into an [Obsidian](https://obsidian.md/) markdown vault conforming to the **Open Knowledge Format (OKF) v0.2** specification.

---

## Repository Layout

When fully deployed, this is how the folder structure will look like:

```text
.codegraph/
├── export_obsidian.py                     # OKF v0.2 Obsidian vault exporter
├── codegraph.db                           # SQLite AST property graph database
├── docs/                                  # Architectural guides & cheatsheets
│   ├── cheatsheet-codegraph.md            # CodeGraph CLI command reference
│   ├── cheatsheet-obsidian.md             # Obsidian vault & Dataview reference
│   ├── Codegraph-vs-Obdidian.md           # CLI retrieval vs. spatial vault comparison
│   └── agent-using-DataView.md            # Living query nodes architecture
├── skills/                                # Agent skills for AI assistants
│   └── obsidian-dataview-codebase/
│       └── SKILL.md                       # Persistent Dataview query skill
└── 67-obsidian_vault/                     # Generated OKF v0.2 Obsidian vault
    ├── .obsidian/graph.json               # Graph view color mappings & physics
    ├── index.md                           # Vault root index & statistics
    └── src/                               # Codebase hierarchy with symbol notes
```

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
2. Select **Open folder as vault** and choose the `obsidian_vault` directory (or `67-obsidian_vault`).
3. Open the Graph View (`Ctrl + G` or `Cmd + G`) to inspect your codebase architecture.

---

## Documentation & Guides (`docs/`)

The repository includes in-depth guides and architectural references under [`docs/`](docs/):

| Guide                                                             | Primary Focus                                                                           | Key Topics                                                                                                                                                                                                            |
| :---------------------------------------------------------------- | :-------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`docs/cheatsheet-codegraph.md`](docs/cheatsheet-codegraph.md)   | **CodeGraph CLI Reference**                                                       | Indexing lifecycle (`init`, `index`, `sync`), AST node/edge definitions, CLI query syntax (`explore`, `query`, `callers`, `callees`, `impact`), and MCP integration.                                  |
| [`docs/cheatsheet-obsidian.md`](docs/cheatsheet-obsidian.md)     | **Obsidian Vault Reference**                                                      | Codebase as Knowledge Graph paradigm, OKF v0.2 schema, folder layout, hotkeys, graph views, Dataview queries, and recommended plugins.                                                                                |
| [`docs/Codegraph-vs-Obdidian.md`](docs/Codegraph-vs-Obdidian.md) | **Comparative Architectural Analysis**                                            | Deep architectural comparison between extractive CLI/agent retrieval (`codegraph explore`) and spatial knowledge browsing (Obsidian Vault).                                                                         |
| [`docs/agent-using-DataView.md`](docs/agent-using-DataView.md)   | **Living Query Node Architecture** (skill `skills/obsidian-dataview-codebase`) | Paradigm shift: replacing disposable, ephemeral chat responses with self-updating, persistent Dataview query nodes inside the vault. See section `Agent Skill: Obsidian Dataview Codeba` below to see how it works |

### 1. CodeGraph CLI Reference ([`docs/cheatsheet-codegraph.md`](docs/cheatsheet-codegraph.md))

- **Lifecycle Commands**: Run `codegraph init` at repository root, `codegraph index` for full rebuilds, and `codegraph sync` for incremental updates.
- **AST Semantic Graph**: Indexes nodes (`file`, `class`, `function`, `method`, `variable`) and edges (`calls`, `defines`, `imports`, `overrides`, `inherits`, `references`) into `.codegraph/codegraph.db`.
- **Querying**:
  - `codegraph explore "<question or symbols>"`: Extract source and dynamic call paths in a single pass.
  - `codegraph callers <symbol>` / `codegraph callees <symbol>`: Analyze inbound/outbound execution dependencies.
  - `codegraph impact <symbol>`: Transitive blast-radius analysis before refactoring.
- **MCP Server**: Provides the `codegraph_explore` tool for autonomous agents.

### 2. Obsidian Codebase Vault Reference ([`docs/cheatsheet-obsidian.md`](docs/cheatsheet-obsidian.md))

- **Knowledge Graph Paradigm**: Every class, function, method, and file is a distinct Markdown note interconnected via bidirectional `[[wikilinks]]`.
- **Mirror Hierarchy**: Vault folders strictly mirror source paths, where the innermost folder is the source file itself (e.g. `src/govagent/engine.py/index.md`, `GovernanceEngine.md`).
- **Spatial Exploration**:
  - Global Graph View (`Ctrl + G`): System-wide architectural topology and hub discovery.
  - Local Graph (`depth 1-2`): Immediate inbound callers and outbound callees for the active note.
  - Hover Previews (`Ctrl + Hover`): Inline docstrings and signatures without losing context.
  - Direct Source Links: Clickable `file:///` URIs jump straight to source line numbers in the IDE.
- **Dataview Recipes**: Pre-built queries for class indexing, inbound coupling hotspots, and missing docstrings.

### 3. CodeGraph vs. Obsidian Comparison ([`docs/Codegraph-vs-Obdidian.md`](docs/Codegraph-vs-Obdidian.md))

- **Extractive vs. Spatial**: `codegraph explore` is optimized for rapid programmatic extraction by AI agents and CLI users; the Obsidian vault is designed for human architectural intuition, cluster visualization, and associative thinking.
- **Query-Driven vs. Hyperlink-Driven**: CodeGraph requires knowing target symbols; Obsidian enables serendipitous traversal via backlinks and visual clusters.
- **Ephemeral vs. Persistent**: CodeGraph SQLite regenerates from code; Obsidian notes can be augmented with thesis cross-references, audit findings, tags, callouts, and Dataview queries.

### 4. Living Dataview Dashboards ([`docs/agent-using-DataView.md`](docs/agent-using-DataView.md))

- **Persistent vs. Disposable**: Chat answers become obsolete immediately after code refactoring. Query nodes generated in the vault recalculate dynamically on every vault export.
- **Embeddable**: Query notes can be transcluded into architectural specs or Obsidian Canvases (`![[queries/my-query]]`).
- **Design Invariants**: All agent-generated query nodes are stored in dedicated `<vault>/queries/` directory to prevent collisions with source nodes exported by `export_obsidian.py`.

---

## Agent Skill: Obsidian Dataview Codebase (`skills/obsidian-dataview-codebase/`)

The repository includes an agent skill located at [`skills/obsidian-dataview-codebase/SKILL.md`](skills/obsidian-dataview-codebase/SKILL.md).

### Overview

When exploring or auditing a codebase, answering questions via chat creates disposable text that quickly becomes obsolete. The **`obsidian-dataview-codebase`** skill equips AI agents (such as Google Antigravity, Claude Code, Cursor, or Gemini CLI) to generate **living, persistent query notes** inside the OKF v0.2 Obsidian vault (e.g. `.codegraph/67-obsidian_vault/queries/`).

These notes leverage the **Dataview** plugin to dynamically query the code graph's metadata, staying synchronized with codebase changes while providing clickable, spatial navigation.

### When to Use

- **Architectural & Structural Audits**: Questions such as *"Show all perception classes and what calls them"*, *"Which modules have high inbound coupling?"*, or *"Find all boundary test cases"*.
- **Subsystem Indexes & Checklists**: Creating interactive inventories for compliance or QA review.
- **Dynamic Dashboards**: Generating widgets for embedding into Obsidian Canvases or architectural reports.

### OKF v0.2 Vault Metadata Contract

Every note exported by `export_obsidian.py` exposes standardized YAML frontmatter and native Dataview page attributes:

| Field / Attribute             | Type    | Description                                 | Example                                                                   |
| :---------------------------- | :------ | :------------------------------------------ | :------------------------------------------------------------------------ |
| `type`                      | string  | Symbol classification                       | `"code/class"`, `"code/function"`, `"code/method"`, `"code/file"` |
| `file_path`                 | string  | Relative source file path                   | `"src/govagent/engine.py"`                                              |
| `start_line` / `end_line` | integer | Source line boundaries                      | `45` / `130`                                                          |
| `description`               | string  | Sanitized docstring header                  | `"Core event dispatcher..."`                                            |
| `resource`                  | string  | IDE file URI with line anchor               | `"file:///src/govagent/engine.py#L45-L130"`                             |
| `tags`                      | list    | Semantic tags                               | `["code/class"]`, `["code/function"]`                                 |
| `aliases`                   | list    | Qualified and short names                   | `["GovernanceEngine", "govagent.engine.GovernanceEngine"]`              |
| `file.link`                 | link    | Clickable wikilink                          | `[[GovernanceEngine]]`                                                  |
| `file.inlinks`              | array   | Incoming references (callers, importers)    | `[ [[engine.py/index]], [[runner.py/run_pipeline]] ]`                   |
| `file.outlinks`             | array   | Outgoing references (callees, dependencies) | `[ [[AuthoritySpec]], [[AuditLog]] ]`                                   |
| `file.folder`               | string  | Directory path within vault                 | `"src/govagent/perception/golden.py"`                                   |

### Workflow Protocol

1. **Isolate Destination**: Always write query notes to `<vault>/queries/<topic-slug>.md` to avoid collisions with exported source notes.
2. **Select Engine**:
   - **Dataview Query Language (DQL)**: Best for tabular catalogs, sorting, and attribute filtering.
   - **DataviewJS**: Best for recursive dependency walks, multi-hop call tracing, and programmatic graph traversals.
3. **Structure the Note**:
   - YAML frontmatter with `type: "view/query"`.
   - Clear objective callout.
   - Live Dataview code block(s).
   - Agent architectural synthesis highlighting primary abstractions, invariants, and audit findings.

### DQL & DataviewJS Recipes

#### Subsystem Class Catalog (DQL)

```dataview
TABLE description AS "Docstring", file_path AS "Source", length(file.inlinks) AS "Callers"
FROM #code/class
WHERE contains(file_path, "perception")
SORT length(file.inlinks) DESC
```

#### High Inbound Coupling / Architectural Hotspots (DQL)

```dataview
TABLE length(file.inlinks) AS "Inbound Callers", file.inlinks AS "Called By"
FROM #code/class OR #code/function
WHERE length(file.inlinks) >= 5
SORT length(file.inlinks) DESC
```

#### Cross-Module Dependency Check (DQL)

```dataview
TABLE file.folder AS "Module", length(file.outlinks) AS "Total Calls"
FROM "src/govagent"
WHERE any(file.outlinks, (out) => contains(out.path, "connectors"))
```

#### Multi-Hop Call Path Tracing (DataviewJS)

````markdown
```dataviewjs
const targetPath = "src/govagent/connectors/mock_erp.py/MockErpConnector";
const callers = dv.pages("#code/class")
    .where(p => p.file.outlinks.some(l => l.path.includes("MockErpConnector")));

dv.table(
    ["Class", "File Path", "Docstring"],
    callers.map(p => [p.file.link, p.file_path, p.description])
);
```
````

### Agent Integration

To make the skill available to AI agents:

- **Project-Level**: Reference or symlink [`skills/obsidian-dataview-codebase`](skills/obsidian-dataview-codebase/) into `.agents/skills/obsidian-dataview-codebase`.
- **Global Configuration**: Add to your agent configuration directory (e.g. `~/.gemini/config/skills/` or `~/.claude/skills/`).
- **Prompt Execution**: Invoke with instructions such as *"Generate an Obsidian Dataview query note analyzing all perception classes and their caller footprints in queries/perception_analysis.md"*.
