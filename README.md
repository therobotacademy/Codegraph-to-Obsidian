# CodeGraph to Obsidian Vault Exporter

Exports the CodeGraph SQLite property graph (`.codegraph/codegraph.db`) into an [Obsidian](https://obsidian.md/) markdown vault conforming to the **Open Knowledge Format (OKF) v0.2** specification.

---

## Table of Contents

- [Repository Layout](#repository-layout)
- [CodeGraph Installation &amp; Usage](#codegraph-installation--usage)
  - [1. Install CodeGraph](#1-install-codegraph)
  - [2. Index a Project](#2-index-a-project)
  - [3. Check Status](#3-check-status)
  - [4. Query the Graph](#4-query-the-graph)
  - [5. Agent / MCP Integration](#5-agent--mcp-integration)
  - [6. Uninstall](#6-uninstall)
- [Features](#features)
- [Semantic Color Palette](#semantic-color-palette)
- [Usage](#usage)
  - [Quick Start](#quick-start)
  - [CLI Arguments](#cli-arguments)
  - [Viewing in Obsidian](#viewing-in-obsidian)
- [Documentation &amp; Guides (`docs/`)](#documentation--guides-docs)
  - [1. CodeGraph CLI Reference](#1-codegraph-cli-reference)
  - [2. Obsidian Codebase Vault Reference](#2-obsidian-codebase-vault-reference)
  - [3. CodeGraph vs. Obsidian Comparison](#3-codegraph-vs-obsidian-comparison)
  - [4. Living Dataview Dashboards](#4-living-dataview-dashboards)
- [Agent Skill: Obsidian Dataview Codebase](#agent-skill-obsidian-dataview-codebase)
  - [Overview](#overview)
  - [When to Use](#when-to-use)
  - [OKF v0.2 Vault Metadata Contract](#okf-v02-vault-metadata-contract)
  - [Workflow Protocol](#workflow-protocol)
  - [DQL &amp; DataviewJS Recipes](#dql--dataviewjs-recipes)
  - [Agent Integration](#agent-integration)
- [Agent Skill: Obsidian Backbone Architect](#agent-skill-obsidian-backbone-architect)
  - [Overview](#overview-1)
  - [When to Use](#when-to-use-1)
  - [The Universal 5-Tier Backbone Taxonomy](#the-universal-5-tier-backbone-taxonomy)
  - [Standard Node Architecture (The 3-Layer Triad)](#standard-node-architecture-the-3-layer-triad)
  - [2D Visual System Flow (`Architecture-Canvas.canvas`)](#2d-visual-system-flow-architecture-canvascanvas)
  - [Narrative Execution Journeys (`Walkthrough-Journeys.md`)](#narrative-execution-journeys-walkthrough-journeysmd)
  - [Bundled Automation Scripts (`scripts/`)](#bundled-automation-scripts-scripts)
  - [7-Step Workflow Protocol](#7-step-workflow-protocol)
  - [Domain Adaptation Matrix](#domain-adaptation-matrix)
  - [Agent Integration](#agent-integration-1)
- [Comparison: Choosing the Right Agent Skill](#comparison-choosing-the-right-agent-skill)

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
│   ├── obsidian-dataview-codebase/        # Living Dataview query generator
│   │   └── SKILL.md                       # Persistent query skill specification
│   └── obsidian-backbone-architect/       # 5-tier architectural cockpit scaffolding
│       ├── SKILL.md                       # Full cockpit methodology & taxonomy
│       └── scripts/                       # Survey, canvas generation & link auditing
│           ├── survey_codebase.py         # AST symbol survey & statistics
│           ├── generate_canvas.py         # 2D Obsidian Canvas generator
│           └── verify_links.py            # Graph integrity & link validator
└── 67-obsidian_vault/                     # Generated OKF v0.2 Obsidian vault
    ├── .obsidian/graph.json               # Graph view color mappings & physics
    ├── Architecture.canvas                # 2D visual system flow & component board
    ├── index.md                           # Vault root index & statistics
    ├── DATAVIEW/                          # Persistent queries & architectural cockpit
    │   └── Backbone/                      # Universal 5-tier living cockpit
    │       ├── index.md                   # Cockpit master dashboard & telemetry
    │       ├── 00-Navigation/             # Spatial exploration, maps & narrative journeys
    │       ├── 01-Architecture-and-Seams/ # Protocols, execution seams & coupling hotspots
    │       ├── 02-Governance-and-Engine/  # Business rules, lifecycle & error taxonomy
    │       ├── 03-Domain-and-Contracts/   # Data models, normalizers & registries
    │       └── 04-Inventory-and-CLI/      # OOP catalog & CLI entry points
    ├── src/                               # Codebase hierarchy with symbol notes
    └── tests/                             # Test suite hierarchy with symbol notes
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

| Guide                                                             | Primary Focus                                                                          | Key Topics                                                                                                                                                                                                            |
| :---------------------------------------------------------------- | :------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`docs/cheatsheet-codegraph.md`](docs/cheatsheet-codegraph.md)   | **CodeGraph CLI Reference**                                                      | Indexing lifecycle (`init`, `index`, `sync`), AST node/edge definitions, CLI query syntax (`explore`, `query`, `callers`, `callees`, `impact`), and MCP integration.                                  |
| [`docs/cheatsheet-obsidian.md`](docs/cheatsheet-obsidian.md)     | **Obsidian Vault Reference**                                                     | Codebase as Knowledge Graph paradigm, OKF v0.2 schema, folder layout, hotkeys, graph views, Dataview queries, and recommended plugins.                                                                                |
| [`docs/Codegraph-vs-Obdidian.md`](docs/Codegraph-vs-Obdidian.md) | **Comparative Architectural Analysis**                                           | Deep architectural comparison between extractive CLI/agent retrieval (`codegraph explore`) and spatial knowledge browsing (Obsidian Vault).                                                                         |
| [`docs/agent-using-DataView.md`](docs/agent-using-DataView.md)   | **Living Query Node Architecture** (skill `skills/obsidian-dataview-codebase`) | Paradigm shift: replacing disposable, ephemeral chat responses with self-updating, persistent Dataview query nodes inside the vault. See section`Agent Skill: Obsidian Dataview Codebase` below to see how it works |

<a id="1-codegraph-cli-reference"></a>

### 1. CodeGraph CLI Reference ([`docs/cheatsheet-codegraph.md`](docs/cheatsheet-codegraph.md))

- **Lifecycle Commands**: Run `codegraph init` at repository root, `codegraph index` for full rebuilds, and `codegraph sync` for incremental updates.
- **AST Semantic Graph**: Indexes nodes (`file`, `class`, `function`, `method`, `variable`) and edges (`calls`, `defines`, `imports`, `overrides`, `inherits`, `references`) into `.codegraph/codegraph.db`.
- **Querying**:
  - `codegraph explore "<question or symbols>"`: Extract source and dynamic call paths in a single pass.
  - `codegraph callers <symbol>` / `codegraph callees <symbol>`: Analyze inbound/outbound execution dependencies.
  - `codegraph impact <symbol>`: Transitive blast-radius analysis before refactoring.
- **MCP Server**: Provides the `codegraph_explore` tool for autonomous agents.

<a id="2-obsidian-codebase-vault-reference"></a>

### 2. Obsidian Codebase Vault Reference ([`docs/cheatsheet-obsidian.md`](docs/cheatsheet-obsidian.md))

- **Knowledge Graph Paradigm**: Every class, function, method, and file is a distinct Markdown note interconnected via bidirectional `[[wikilinks]]`.
- **Mirror Hierarchy**: Vault folders strictly mirror source paths, where the innermost folder is the source file itself (e.g. `src/govagent/engine.py/index.md`, `GovernanceEngine.md`).
- **Spatial Exploration**:
  - Global Graph View (`Ctrl + G`): System-wide architectural topology and hub discovery.
  - Local Graph (`depth 1-2`): Immediate inbound callers and outbound callees for the active note.
  - Hover Previews (`Ctrl + Hover`): Inline docstrings and signatures without losing context.
  - Direct Source Links: Clickable `file:///` URIs jump straight to source line numbers in the IDE.
- **Dataview Recipes**: Pre-built queries for class indexing, inbound coupling hotspots, and missing docstrings.

<a id="3-codegraph-vs-obsidian-comparison"></a>

### 3. CodeGraph vs. Obsidian Comparison ([`docs/Codegraph-vs-Obdidian.md`](docs/Codegraph-vs-Obdidian.md))

- **Extractive vs. Spatial**: `codegraph explore` is optimized for rapid programmatic extraction by AI agents and CLI users; the Obsidian vault is designed for human architectural intuition, cluster visualization, and associative thinking.
- **Query-Driven vs. Hyperlink-Driven**: CodeGraph requires knowing target symbols; Obsidian enables serendipitous traversal via backlinks and visual clusters.
- **Ephemeral vs. Persistent**: CodeGraph SQLite regenerates from code; Obsidian notes can be augmented with thesis cross-references, audit findings, tags, callouts, and Dataview queries.

<a id="4-living-dataview-dashboards"></a>

### 4. Living Dataview Dashboards ([`docs/agent-using-DataView.md`](docs/agent-using-DataView.md))

- **Persistent vs. Disposable**: Chat answers become obsolete immediately after code refactoring. Query nodes generated in the vault recalculate dynamically on every vault export.
- **Embeddable**: Query notes can be transcluded into architectural specs or Obsidian Canvases (`![[queries/my-query]]`).
- **Design Invariants**: All agent-generated query nodes are stored in dedicated `<vault>/queries/` directory to prevent collisions with source nodes exported by `export_obsidian.py`.

---

<a id="agent-skill-obsidian-dataview-codebase"></a>

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

---

## <a id="agent-skill-obsidian-backbone-architect"></a>Agent Skill: Obsidian Backbone Architect (`skills/obsidian-backbone-architect/`)

The repository includes an agent skill located at [`skills/obsidian-backbone-architect/SKILL.md`](skills/obsidian-backbone-architect/SKILL.md).

### Overview

While `export_obsidian.py` and OKF v0.2 produce an accurate AST database and hundreds of atomic symbol notes, raw symbol notes are designed for machine retrieval rather than human orientation.

The **`obsidian-backbone-architect`** skill provides an automated, repeatable methodology to transform any codebase indexed by CodeGraph into a **living 5-tier architectural cockpit** under `<vault>/DATAVIEW/Backbone/`.

The resulting cockpit answers three core architectural questions in under 5 minutes:

1. **Anatomy**: What classes, interfaces, algorithms, and constants exist?
2. **Physiology**: How does a request or data payload travel through the system step-by-step?
3. **Topography**: Where are the decoupled boundaries, state transitions, and coupling blast radiuses?

### When to Use

- **Complete Architectural Scaffolding**: When asking an AI assistant to *"document the codebase in Obsidian"*, *"create an architectural cockpit"*, *"generate a backbone for this repo"*, or *"make a 2D canvas of the code"*.
- **Onboarding & Code Audits**: When an auditor, new engineer, or external reviewer needs a self-contained, spatial navigation system inside Obsidian.
- **Architectural Refactoring**: When assessing coupling hotspots, boundary leaks, or domain invariants before executing major refactoring.

### The Universal 5-Tier Backbone Taxonomy

Regardless of language or system architecture, the codebase is structured into 5 standard functional tiers:

| Tier           | Directory                                                           | Core Notes                                                                       | Purpose                                                                                                                    |
| :------------- | :------------------------------------------------------------------ | :------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------- |
| **00**   | `00-Navigation/`                                                  | `Architecture-Canvas.canvasArchitecture-Map.md``Walkthrough-Journeys.md`       | Spatial orientation, interactive Mermaid state/subsystem diagrams, and 3-path narrative execution journeys.                |
| **01**   | `01-Architecture-and-Seams/`                                      | `Protocols-and-Seams.mdExecution-Seams.md``Coupling-Hotspots.md`               | Abstract boundaries/protocols, end-to-end data transformation pipeline, and high fan-in/fan-out refactoring risk register. |
| **02**   | `02-Core-Engine-and-Logic/`*(or `02-Governance-and-Engine/`)* | `Business-Rules-and-Specs.mdEvent-Lifecycle.md``Error-Taxonomy.md`             | Core domain rules, event bus/lifecycle, and custom exception hierarchy with fallback/containment strategies.               |
| **03**   | `03-Domain-and-Contracts/`                                        | `Domain-Contracts.mdFunctions-and-Normalizers.md``Constants-and-Registries.md` | Immutable data structures/DTOs/enums, pure stateless transformation functions, and system constants/registries.            |
| **04**   | `04-Inventory-and-CLI/`                                           | `Classes.mdEntrypoints-and-CLI.md`                                             | Exhaustive OOP class catalog (with callers & source anchors) and public CLI console commands / API entrypoints.            |
| **Root** | `index.md`                                                        | `DATAVIEW/Backbone/index.md`                                                   | Master Cockpit Dashboard: complete navigation matrix and live Dataview telemetry.                                          |

### Standard Node Architecture (The 3-Layer Triad)

Every backbone note adheres to the OKF v0.2 metadata contract (`type: "view/query"`) and contains three complementary layers:

1. **Live Dataview Query**: Dynamic DQL blocks that re-index in real time whenever the vault or code changes.
2. **Pre-Rendered Static Reference Table**: A resilient markdown table with direct source links (`file:///...#L...`) ensuring full usability in non-plugin environments (Obsidian mobile, standard Markdown viewers, GitHub, or IDEs).
3. **Architectural Synthesis & Invariants**: Agent-authored synthesis highlighting non-obvious contracts, boundary guarantees, thread-safety considerations, and immutability invariants.

### 2D Visual System Flow (`Architecture-Canvas.canvas`)

The skill generates an interactive 2D Obsidian Canvas positioned across 6 horizontal functional stages:

```text
[Input Ingestion] ➔ [Perception & Normalization] ➔ [Domain Model & Context] ➔ [Decision Engine] ➔ [Gate & Governor] ➔ [Persistence & Audit]
    x ≈ -850                    x ≈ -450                    x ≈ -50                  x ≈ 370               x ≈ 790               x ≈ 1200
```

Each card contains real payload schemas, component definitions, and clickable wikilinks to atomic symbol notes.

### Narrative Execution Journeys (`Walkthrough-Journeys.md`)

Rather than relying solely on static catalogs, the cockpit includes narrative execution journeys tracing "A Day in the Life" of 3 archetypal execution paths:

1. **The Happy / Routine Path**: Standard payload with zero defects. Demonstrates normal flow from ingestion to persistence.
2. **The Edge / Escalation Path**: Payload with soft anomalies or threshold breaches. Traces escalation gates, policy suspensions, or human-in-the-loop warnings.
3. **The Failure / Security Path**: Malicious input, schema violation, or security boundary breach. Traces early interception, audit trail recording, and error containment.

Every step in each journey documents exact file line numbers, intermediate state snippets, and the specific invariant that protected the system.

### Bundled Automation Scripts (`scripts/`)

The skill includes three standalone Python automation scripts under [`skills/obsidian-backbone-architect/scripts/`](skills/obsidian-backbone-architect/scripts/):

#### 1. Codebase & Vault Symbol Survey (`survey_codebase.py`)

Scans all OKF v0.2 Markdown notes in the vault, extracting classes, functions, module variables, candidate protocols/interfaces, and custom exception hierarchies with line numbers and source anchors:

```bash
python .codegraph/skills/obsidian-backbone-architect/scripts/survey_codebase.py --vault-path .codegraph/67-obsidian_vault
```

#### 2. 2D Canvas Generator (`generate_canvas.py`)

Programmatically lays out cards and directional edge connections on a 2D plane adhering to Obsidian's JSON canvas format (`.canvas`):

```bash
python .codegraph/skills/obsidian-backbone-architect/scripts/generate_canvas.py --output .codegraph/67-obsidian_vault/DATAVIEW/Backbone/00-Navigation/Architecture-Canvas.canvas
```

#### 3. Graph Integrity & Link Auditor (`verify_links.py`)

Audits all `[[wikilinks]]` across the generated backbone nodes to guarantee 100% graph integrity with zero broken links:

```bash
python .codegraph/skills/obsidian-backbone-architect/scripts/verify_links.py \
  --vault-path .codegraph/67-obsidian_vault \
  --target-dir .codegraph/67-obsidian_vault/DATAVIEW/Backbone
```

### 7-Step Workflow Protocol

When invoked, the agent executes the following standardized workflow:

1. **Detect CodeGraph Vault & Inspect AST**: Run `survey_codebase.py` against the vault.
2. **Scaffold 5 Functional Directories**: Create `00-Navigation` through `04-Inventory-and-CLI`.
3. **Author Core Backbone Nodes**: Write the 12 standard notes with DQL queries, static tables, and invariants.
4. **Generate the 2D Obsidian Canvas**: Create the horizontal component flow canvas.
5. **Write Archetypal Narrative Journeys**: Trace Happy, Edge, and Failure paths with line-level references.
6. **Build Cockpit Dashboard**: Generate `DATAVIEW/Backbone/index.md` and link it from vault root `index.md`.
7. **Verify Graph Integrity**: Run `verify_links.py` to ensure zero broken links.

### Domain Adaptation Matrix

The 5 tiers adapt naturally to various software architectures:

| Codebase Type                    | Tier 01 (Seams)                | Tier 02 (Core Logic)            | Tier 03 (Domain)           | Tier 04 (Surface)            |
| :------------------------------- | :----------------------------- | :------------------------------ | :------------------------- | :--------------------------- |
| **Agent Governance**       | Extractor & ERP Seams          | Authority Specs & Rules         | Domain Entities & Decimals | Stories & Explainer GUI      |
| **Web API / Microservice** | HTTP Middlewares & DB Adapters | Controllers, Services & Auth    | DTOs, Schemas & Pydantic   | FastAPI Routes & CLI Tools   |
| **Data / ML Pipeline**     | Ingestion & Storage Connectors | Transformers & Pipeline DAG     | Feature Records & Enums    | Pipeline Runners & Notebooks |
| **Compiler / CLI Tool**    | Lexer & Parser Interfaces      | AST Passes, Optimizer & Codegen | AST Nodes & Type Tables    | CLI Commands & Flags         |

### Agent Integration

To make the skill available to AI assistants:

- **Project-Level**: Reference or symlink [`skills/obsidian-backbone-architect`](skills/obsidian-backbone-architect/) into `.agents/skills/obsidian-backbone-architect`.
- **Global Configuration**: Add to your agent configuration directory (e.g. `~/.gemini/config/skills/` or `~/.claude/skills/`).
- **Prompt Execution**: Invoke with instructions such as *"Scaffold a 5-tier Obsidian architectural backbone cockpit for this codebase under DATAVIEW/Backbone/"*.

---

## Comparison: Choosing the Right Agent Skill

| Feature / Dimension          | `obsidian-dataview-codebase`                          | `obsidian-backbone-architect`                              |
| :--------------------------- | :------------------------------------------------------ | :----------------------------------------------------------- |
| **Primary Scope**      | Micro / Targeted query generation                       | Macro / Full architectural scaffolding                       |
| **Primary Use Case**   | Answering ad-hoc queries with persistent Dataview notes | Creating an end-to-end 5-tier cockpit for an entire codebase |
| **Output Location**    | `<vault>/queries/<topic>.md` or `<vault>/DATAVIEW/` | `<vault>/DATAVIEW/Backbone/` (5 directories + 12+ nodes)   |
| **Visual Artifacts**   | Dataview tables and lists                               | 2D Obsidian Canvas (`.canvas`) + Mermaid state diagrams    |
| **Narrative Traces**   | Summary notes & findings                                | 3 archetypal execution journeys with line anchors            |
| **Automation Tooling** | Direct agent prompt & DQL/DataviewJS                    | Bundled Python survey, canvas generator, and link auditor    |
| **Static Fallback**    | Optional                                                | Required (resilient static markdown tables in all nodes)     |
