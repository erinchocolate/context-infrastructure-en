# WORKSPACE.md - Directory Routing Quick Reference

Goal: Give the AI a fast way to know "where to find / put what" at the start of every session. **Check here before searching for any file.**

## Routing Rules

### Root-Level Knowledge Layers

The workspace uses a three-layer architecture at the root. Route content by its processing stage:

| Layer | Path | What goes here |
|---|---|---|
| Raw | `01 raw/` | All unprocessed inputs: conversation logs, one-off notes, scripts, unfiltered ideas |
| Trusted | `02 trusted/` | Refined observations and reflections: `OBSERVATIONS.md`, personal retrospectives, structured notes |
| Refined | `03 refined/` | Reusable, public-facing knowledge: axioms, skills, core guides, tools |

### Projects

- **Active project context** (docs, meeting notes, decisions, status): `projects/<project>/`
  - Each project mirrors the same three-layer structure internally:
    - `projects/<project>/01 raw/` — raw project inputs (meeting notes, requirements, AI outputs)
    - `projects/<project>/02 trusted/` — stable operational knowledge (architecture, design decisions, research)
    - `projects/<project>/03 refined/` — shareable output (stakeholder briefs, Confluence docs)

### System and Rules

- Reusable workflows and best practices (Skills): `03 refined/skills/`
- Decision principles (Axioms): `03 refined/axioms/`
- Utility scripts: `03 refined/tools/`

### Archived Content

- Anything no longer active: `archive/`

## Naming Conventions

- Directory and file names: lowercase + underscores (snake_case)
- Temporary projects: `tmp_<name>/`
- **Dated documents use the unified format: `YYYYMMDD_<name>.md`**
  - Example: `20260408_auto_trigger_chunking_on_table_change.md`
  - Applies to: all timestamped documents under `01 raw/`, `02 trusted/`, and project subdirectories
  - Use the document creation date; no separators (not `2026-04-08` or `2026_04_08`)

## Python Environment

- The root `.venv/` is the workspace-level environment; manage dependencies with `uv pip install`
- When isolation is needed, create a dedicated environment at `projects/<project>/.venv/`

## Tool Index

| File | Purpose |
|---|---|
| `03 refined/tools/confluence/convert_confluence_docs.py` | Batch conversion: Confluence .doc → Markdown (used with `03 refined/skills/workflow_confluence_sync.md`) |
| `03 refined/tools/confluence/sync_docs_to_confluence.py` | Push Markdown to Confluence |
| `03 refined/tools/confluence/pull_from_confluence.py` | Pull from Confluence (version-tracked, idempotent) |
| `03 refined/tools/semantic_search/` | Semantic search tool (see `03 refined/skills/semantic_search.md`) |

## Quick Reference

<!-- As projects grow, add quick routes for active projects here -->
<!-- Format: - `project-name` -> `projects/project_name/` (description) -->
- `marvin` → `projects/marvin/` (Contact Energy internal RAG information retrieval tool)
