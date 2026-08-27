---
name: obsidian-backbone-architect
description: "Scaffold a complete, 5-tier human-grade architectural cockpit (Dataview queries, 2D Obsidian Canvas, Mermaid state maps, and narrative execution journeys) for ANY codebase indexed by CodeGraph / OKF v0.2."
---

# Obsidian Backbone Architect

## Overview

CodeGraph and OKF v0.2 generate an AST database and hundreds of atomic symbol notes (`.md`), but raw symbol notes are designed for machine retrieval, not human comprehension.

This skill provides an automated, repeatable methodology to transform **any codebase** indexed by CodeGraph into a **living 5-tier architectural cockpit** under `DATAVIEW/Backbone/`.

The resulting cockpit answers three questions in under 5 minutes:
1. **Anatomy**: What classes, interfaces, algorithms, and constants exist?
2. **Physiology**: How does a request/payload travel through the system step-by-step?
3. **Topography**: Where are the decoupled boundaries, state transitions, and coupling blast radiuses?

---

## When to Use This Skill

Activate this skill when:
* The user asks to *"document the codebase in Obsidian"*, *"create an architectural cockpit"*, *"generate a backbone for this repo"*, or *"make a 2D canvas of the code"*.
* A repository has a `.codegraph/` directory and needs human-grade documentation.
* An auditor, lead engineer, or external reviewer needs a self-contained, interactive orientation system inside Obsidian.

---

## The Universal 5-Tier Backbone Taxonomy

Regardless of language (Python, TypeScript, Go, Rust, Java, C#) or architecture (web API, CLI, compiler, distributed pipeline, autonomous agent), the codebase is organized into **5 standard functional tiers**:

```
<VAULT>/DATAVIEW/Backbone/
├── index.md                                # Master Cockpit Dashboard & Telemetry
├── 00-Navigation/                          # Orientation & Spatial Exploration
│   ├── Architecture-Canvas.canvas          # 2D visual board with real payload cards
│   ├── Architecture-Map.md                 # Interactive Mermaid diagrams (subsystems & state machines)
│   └── Walkthrough-Journeys.md             # Narrative Trace: "A Day in the Life" of 3 archetypal paths
├── 01-Architecture-and-Seams/              # Boundaries, Pipeline & Blast Radius
│   ├── Protocols-and-Seams.md              # Abstract interfaces, traits, or protocols
│   ├── Execution-Seams.md                  # Step-by-step end-to-end data transformation pipeline
│   └── Coupling-Hotspots.md                # High fan-in/fan-out symbols & refactoring risk register
├── 02-Core-Engine-and-Logic/               # Business Logic, State & Error Containment
│   ├── Business-Rules-and-Specs.md         # Policies, decision boundaries, or validators
│   ├── Event-Lifecycle.md                  # Event bus, message stream, or audit trail
│   └── Error-Taxonomy.md                   # Custom exceptions, fallback defaults & rollbacks
├── 03-Domain-and-Contracts/                # Data Models & Algorithms
│   ├── Domain-Contracts.md                 # Immutable entities, DTOs, schemas, and enums
│   ├── Functions-and-Normalizers.md        # Pure stateless algorithms, sanitizers & helpers
│   └── Constants-and-Registries.md         # Statutory field tuples, defaults & registries
└── 04-Inventory-and-CLI/                   # Catalog & Execution Surface
    ├── Classes.md                          # Comprehensive OOP/struct catalog with callers & line ranges
    └── Entrypoints-and-CLI.md              # Public API routes, CLI console scripts, main runners
```

---

## Workflow: Step-by-Step Execution

### Step 1: Detect CodeGraph Vault & Inspect AST
Locate the Obsidian vault directory (typically `.codegraph/<vault-name>/`). Check `codegraph.db` or run a symbol survey using the bundled helper script:

```bash
python scripts/survey_codebase.py --vault-path <VAULT_PATH>
```

The survey catalogs:
* All classes (`type: "code/class"`) and their line numbers, docstrings, and callers (`length(file.inlinks)`).
* All interfaces/protocols (`typing.Protocol`, abstract base classes, interfaces).
* All pure functions (`type: "code/function"`).
* All constants & module variables (`type: "code/variable"`).
* All custom exceptions inheriting from `Exception`.
* All CLI commands and public entry points.

### Step 2: Scaffold the 5 Directories
Create the 5 folders under `<VAULT>/DATAVIEW/Backbone/`:
1. `00-Navigation/`
2. `01-Architecture-and-Seams/`
3. `02-Core-Engine-and-Logic/` (or `02-Governance-and-Engine/` if governance-centric)
4. `03-Domain-and-Contracts/`
5. `04-Inventory-and-CLI/`

### Step 3: Author the Core Backbone Nodes
Each note must follow the OKF v0.2 metadata contract:

```markdown
---
okf_version: "0.2"
type: "view/query"
title: "[Node Title]"
created: "YYYY-MM-DD"
tags:
  - query/[topic]
  - architecture/[topic]
---

# [Node Title]

> [[DATAVIEW/Backbone/index|← Back to Backbone Index]]

> **Objective**: [1-sentence statement of what this document specifies].

## 1. Live Dataview Query
[Targeted DQL block]

## 2. Pre-Rendered Static Reference Table
[Markdown table for non-plugin environments with direct source links file:///...]

## 3. Architectural Synthesis & Invariants
[Invariants observed, boundary rules, immutability, thread safety]
```

### Step 4: Generate the 2D Obsidian Canvas (`.canvas`)
Obsidian Canvas files are JSON files mapping nodes and edges onto a 2D plane.  
Run or execute the canvas generator script to position nodes in **horizontal functional columns**:

* **Column 1 ($x \approx -850$)**: Input Ingestion (`DocumentRef`, Request DTO, Message payload).
* **Column 2 ($x \approx -450$)**: Perception & Normalization (Parsing, sanitization, validation).
* **Column 3 ($x \approx -50$)**: Domain Model & Context (Entity assembly, master catalog lookup).
* **Column 4 ($x \approx 370$)**: Decision Engine (Rules group, validators, policies).
* **Column 5 ($x \approx 790$)**: Gate & Governor (Orchestrator, HITL safety nets, coordinators).
* **Column 6 ($x \approx 1200$)**: Persistence & Audit (Database ledger, commit, rollback, audit trail).

Every card must contain clickable wikilinks to symbol notes: `[[src/.../Symbol|Symbol]]`.

### Step 5: Write the Archetypal Narrative Journeys (`Walkthrough-Journeys.md`)
Never stop at static catalogs. Write "A Day in the Life" tracing **three archetypal paths**:
1. **The Happy / Routine Path**: Standard payload with zero defects. Shows automated completion.
2. **The Edge / Escalation Path**: Payload exceeding thresholds or with soft anomalies. Shows escalation gates, suspensions, or warnings.
3. **The Failure / Security Path**: Malicious input, fatal schema error, or security violation. Shows interception, rollback, and incident generation.

For each journey, document:
* Exact line numbers running the step.
* Intermediate memory state / payload snippets.
* The invariant that protected the system at that boundary.

### Step 6: Build the Cockpit `index.md`
Assemble the root cockpit note at `DATAVIEW/Backbone/index.md`:
* Master Navigation Matrix listing all 12+ nodes with their relative links.
* Live Dataview Telemetry (class counts by subsystem, function distribution, protocol overview).
* Update the Vault Root `index.md` to link directly into `Backbone/`.

### Step 7: Verify Zero Broken Links
Run link verification across the generated files:
* Ensure wikilinks in tables do NOT use escaped pipes (`\|`), which Obsidian interprets as part of the filename. Use clean `[[path]]` or `[label](path.md)`.
* Verify every `[[...]]` link resolves to an existing file. Zero tolerance for broken links.

---

## Domain Adaptation Matrix

Adapt folder and node names to fit the codebase's domain:

| Codebase Type | Tier 01 (Seams) | Tier 02 (Core Logic) | Tier 03 (Domain) | Tier 04 (Surface) |
| :--- | :--- | :--- | :--- | :--- |
| **Agent Governance** | Extractor & ERP Seams | Authority Specs & Rules | Domain Entities & Decimals | Stories & Explainer GUI |
| **Web API / Microservice** | HTTP Middlewares & DB Adapters | Controllers, Services & Auth | DTOs, Schemas & Pydantic | FastAPI Routes & CLI Tools |
| **Data / ML Pipeline** | Ingestion & Storage Connectors | Transformers & Pipeline DAG | Feature Records & Enums | Pipeline Runners & Notebooks |
| **Compiler / CLI Tool** | Lexer & Parser Interfaces | AST Passes, Optimizer & Codegen | AST Nodes & Type Tables | CLI Commands & Flags |
