# WORKSPACE.md - Directory Routing Quick Reference

Goal: Give the AI a fast way to know "where to find / put what" at the start of every session. **Check here before searching for any file.**

## Routing Rules

### Projects and Code
- **Ongoing project context** (documents, meeting notes, decisions, status): `projects/<project>/`
- Writing code / running scripts / one-off projects: `adhoc_jobs/<project>/`
- Utility scripts (email, semantic search, sharing reports, etc.): `tools/`

### Knowledge and Records
- General research reports: `contexts/research/`
- Things learned / retrospectives / methodology: `contexts/learning/`
- Daily personal activity log (unrelated to any project): `contexts/daily_log/`

### System and Rules
- Reusable technical solutions / Skills: `rules/skills/`
- Core axioms: `rules/axioms/`

## Naming Conventions
- Directory and file names: lowercase + underscores (snake_case)
- Temporary projects: `tmp_<name>/`
- **Dated documents use the unified format: `YYYYMMDD_<name>.md`**
  - Example: `20260408_auto_trigger_chunking_on_table_change.md`
  - Applies to: all timestamped documents under meetings, decisions, adhoc_jobs, and daily_log
  - Use the document creation date; no separators (not `2026-04-08` or `2026_04_08`)

## Python Environment
- The root `.venv/` is the workspace-level environment; manage dependencies with `uv pip install`
- When isolation is needed, create a dedicated environment at `adhoc_jobs/<project>/.venv/`

## Tool Index

| File | Purpose |
|---|---|
| `tools/convert_confluence_docs.py` | Batch conversion script: Confluence .doc → Markdown (used with `rules/skills/workflow_confluence_import.md`) |
| `tools/semantic_search/` | Semantic search tool (see `rules/skills/semantic_search.md`) |

## Quick Reference

<!-- As projects grow, add quick routes for active projects here -->
<!-- Format: - `project-name` -> `projects/project_name/` (description) -->
- `marvin` → `projects/marvin/` (Contact Energy internal RAG information retrieval tool)
