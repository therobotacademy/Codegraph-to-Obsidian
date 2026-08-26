# Codegraph vs. Obsidian fot code exploration

**`codegraph explore`** is an *extractive retrieval engine* optimized for rapid question-answering and agent contexts, while the **Obsidian Vault** is an *interactive spatial knowledge canvas* optimized for human architectural intuition, topological discovery, and persistent annotation.

### 1. Spatial Topology & Cluster Discovery (Global & Local Graph)

* **Visual Macro-Architecture**: In Obsidian, opening the global graph view (`Ctrl + G`) immediately reveals architectural topology:
  - **Hub nodes**: Heavily connected classes (e.g., `GovernanceEngine`, `MockErpConnector`, `PerceptionResult`) emerge visually as high-degree clusters.
  - **Islands & Decoupling**: Standalone utilities, isolated modules, or orphan functions become visually obvious without running dependency check scripts.
* **Neighborhood Exploration via Local Graph**: In a note (e.g., `FaturaParser.md`), Obsidian's Local Graph set to depth 1 or 2 lets you see incoming callers and outgoing callees dynamically as an interactive force-directed graph.
* **Semantic Color Coding**: With the configured `TYPE_COLORS` (`code/class` in amber `#F59E0B`, `code/function` in cyan `#06B6D4`, `code/file` in red `#EB082E`), your visual cortex distinguishes types instantly without reading code headers.

### 2. Nonlinear Navigation & Serendipitous Browsing

* **`codegraph explore` is Query-Driven**: You must already know what symbol or question to query. If you don't know the exact symbol name, you have to search or guess.
* **The Vault is Hyperlink-Driven**:
  - Click-through navigation across `[[wikilinks]]` lets you traverse execution paths forwards (calls) and backwards (backlinks / incoming references).
  - Hover previews (`Ctrl + Hover`) allow inspecting function signatures and docstrings without leaving your current place in the call chain.
  - Split views / Canvas: You can open two or three related notes side-by-side to cross-check contracts (e.g., `GoldenExtractor` alongside `VLMExtractor` and `PerceptionResult`).

### 3. Human Annotation & Knowledge Augmentation (OKF v0.2)

* **CodeGraph SQLite is Ephemeral**: Re-indexing re-generates the database from the AST. You cannot attach thoughts, questions, or architectural intent to a node inside `codegraph.db`.
* **Markdown Notes are Extensible**:
  - You can write notes directly into symbol pages: link them to thesis chapters, add warning callouts (`> [!WARNING]`), document edge cases, or embed Mermaid sequence diagrams.
  - **Tagging & Metadata**: You can tag notes with `#review-needed`, `#phase3`, or `#boundary-test`.
  - **Dataview Queries**: You can write dynamic queries inside Obsidian, e.g.:
    ```dataview
    TABLE file_path, start_line, description
    FROM #code/class
    WHERE contains(file_path, "perception")
    ```

### 4. Direct IDE Source Linking

* Each exported note's frontmatter and header contain a direct `file:///` URI link with line numbers (e.g., `file:///src/govagent/engine.py#L45-L120`).
* In Obsidian, clicking the source link jumps directly into your editor at the exact line of implementation.

### Summary: Complementary Use Cases

| Dimension                   | `codegraph explore`                                          | Obsidian Vault (`.codegraph/67-obsidian_vault`)          |
| :-------------------------- | :------------------------------------------------------------- | :--------------------------------------------------------- |
| **Primary Consumer**  | AI Assistant / Terminal user looking for immediate source code | Human software architect / auditor building a mental model |
| **Interaction Model** | Discrete linear queries (`symbol` $\to$ text output)       | Visual, spatial, associative browsing & graph interaction  |
| **Scope**             | Point-to-point call path retrieval                             | System-wide structural clustering & hub discovery          |
| **Annotation**        | Read-only extraction                                           | Read/write knowledge base with OKF metadata & tags         |
| **Backlinks**         | Follows edges on request                                       | Persistent bidirectional cross-reference index             |
