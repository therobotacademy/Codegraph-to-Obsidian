# CodeGraph Cheatsheet

`CodeGraph` is an AST-level semantic indexer and structural query tool. It parses source files into an SQLite graph database (`.codegraph/codegraph.db`), tracking classes, methods, functions, files, call hierarchies, inheritance, and dynamic dispatch edges.

---

## 1. Quick Reference Commands

| Command | Purpose |
| :--- | :--- |
| `codegraph init` | Scans workspace, parses AST, resolves refs, builds `.codegraph/codegraph.db`. |
| `codegraph explore "<query>"` | Queries the graph for symbols, relationships, call paths, or source snippets. |
| `python .codegraph/export_obsidian.py` | Exports SQLite graph database into an OKF v0.2 Obsidian Markdown vault. |

---

## 2. Indexing Lifecycle (`codegraph init`)

Run `codegraph init` from the repository root:

```bash
codegraph init
```

### When to Re-index
* After creating or modifying classes, functions, or imports across phases.
* After renaming files, functions, or domain models.
* When adding new test suites or perception components.

### What CodeGraph Indexes
* **Nodes**: `file`, `class`, `function`, `method`, `variable`.
* **Edges**: `calls`, `defines`, `imports`, `overrides`, `inherits`, `references`.
* **Metadata**: Start/end line numbers, signatures, docstrings, qualified paths.

---

## 3. Querying with `codegraph explore`

The `explore` command operates either via the terminal CLI or through the MCP tool `codegraph_explore`.

### A. Direct Symbol Lookup
Inspect definition, signature, docstring, and immediate relationships:

```bash
codegraph explore "GovernanceEngine"
codegraph explore "FaturaParser.parse_dict"
codegraph explore "GoldenExtractor"
```

### B. Call Path & Relationship Tracing
Query how components connect across modules:

```bash
# Where is a function or method called?
codegraph explore "who calls normalize_amount"

# How does an engine or orchestrator dispatch?
codegraph explore "how does GovernanceEngine interact with GateManager"

# Flow between layers
codegraph explore "call path from FaturaParser to Invoice"
```

### C. File-Level Structural Survey
Understand symbols defined within a file:

```bash
codegraph explore "src/govagent/perception/rebuild.py"
codegraph explore "src/govagent/authority/spec.py"
```

---

## 4. MCP Tool Usage (AI Agent Mode)

When pair-programming with AI assistants (e.g. Antigravity), the assistant accesses the lazy MCP tool `codegraph_explore`:

```json
{
  "ServerName": "codegraph",
  "ToolName": "codegraph_explore",
  "Arguments": {
    "query": "VLMExtractor"
  }
}
```

**Benefits for Agent Collaboration**:
* Returns verbatim line-numbered source in a single call.
* Resolves dynamic dispatch hops that `grep` or text searches miss.
* Avoids cluttered token contexts from dumping whole files.

---

## 5. Direct SQLite Database Inspection

The underlying graph resides in `.codegraph/codegraph.db`. You can query it directly with `sqlite3` or GUI tools:

```bash
sqlite3 .codegraph/codegraph.db
```

### Useful SQL Queries

```sql
-- 1. Count nodes by type
SELECT kind, COUNT(*) AS count 
FROM nodes 
GROUP BY kind 
ORDER BY count DESC;

-- 2. Find most connected symbols (highest in-degree callers)
SELECT n.name, n.kind, COUNT(e.source) AS incoming_refs
FROM nodes n
JOIN edges e ON n.id = e.target
WHERE e.kind = 'calls'
GROUP BY n.id
ORDER BY incoming_refs DESC
LIMIT 10;

-- 3. List all classes defined in a module
SELECT name, file_path, start_line, end_line
FROM nodes
WHERE kind = 'class' AND file_path LIKE '%perception%'
ORDER BY name;

-- 4. Inspect relationships from a specific class
SELECT e.kind, target_node.name, target_node.file_path
FROM edges e
JOIN nodes source_node ON e.source = source_node.id
JOIN nodes target_node ON e.target = target_node.id
WHERE source_node.name = 'GovernanceEngine';
```

---

## 6. Exporting to Obsidian Knowledge Graph

Export the graph database into visual, hyperlinked Markdown notes:

```bash
# Standard export (classes, functions, methods, files)
python .codegraph/export_obsidian.py --out .codegraph/67-obsidian_vault

# Include variables as discrete nodes
python .codegraph/export_obsidian.py --out .codegraph/67-obsidian_vault --include-vars

# Target custom output path
python .codegraph/export_obsidian.py --out docs/knowledge-vault
```
