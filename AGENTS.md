# AGENTS.md - Meiqiao's Context Infrastructure

This folder is home. Treat it that way.

## Every Session

Before doing anything else:

1. Read `rules/SOUL.md` — this is who you are
2. Read `rules/USER.md` — this is who you're helping
3. Read `rules/WORKSPACE.md` — file routing table, check before searching for files
4. Read `rules/COMMUNICATION.md` — how to think and communicate (especially for non-coding tasks)
5. Read `rules/skills/INDEX.md` — understand available skills

## File Routing

**When looking for a file, check `rules/WORKSPACE.md` first, then search.** WORKSPACE.md is the directory index for this workspace, recording where each type of content lives. In most cases a quick look will locate the target directory — no need for a full glob/grep sweep. If you discover a new directory or project that isn't listed, update WORKSPACE.md while you're at it.

**Before working on a specific project task, read the corresponding `projects/<name>/README.md`.** This is the AI entry point for each project, containing the project overview, documentation index, and current focus. See WORKSPACE.md for the active project list.

## Skills

**Skills** are reusable AI capabilities, including workflows, API guides, best practices, and more.

**Important: When faced with "how do I do X," check skills before checking system tools.** Search order: (1) quick reference below → (2) `rules/skills/INDEX.md` → (3) system tools.

**Need to execute a task** → check `rules/skills/INDEX.md` first to find the relevant skill
**Want to add a new capability** → follow the existing skill format, then update INDEX.md

### Common Skill Quick Reference (INDEX.md is authoritative)

**Deep research tasks** → `rules/skills/workflow_deep_research_survey.md`
- Initial scan → dimension splitting → multi-Agent parallel → cross-validation → write report
- Output: `contexts/research/`

**Running background Agents / parallel Subagents** → `rules/skills/workflow_parallel_subagents.md`
- When to split tasks, how to dispatch multiple subagents in parallel
- Before calling `run_in_background=True`, read this skill first
- After dispatching agents, wait for system notifications — no polling needed

**Import Confluence documents** → `rules/skills/workflow_confluence_import.md`
- Convert Confluence pages to Markdown and categorize into `projects/<name>/docs/`
- Companion script: `tools/convert_confluence_docs.py`

## Axioms

Decision principles distilled from personal experience, used to inspire deep thinking. For the categorized index, usage guide, and trigger words, see `rules/axioms/INDEX.md`.

## Memory System

Three-layer memory architecture:
- **L3 (global constraints)**: all files under `rules/`, passively loaded each session
- **L1/L2 (dynamic memory)**: `contexts/memory/OBSERVATIONS.md`, actively retrieved by agents
- **How to accumulate**: manually trigger daily observations + weekly reflections (see prompt templates in `contexts/memory/`)

## Safety

- Don't exfiltrate private data. Ever.
- Don't run destructive commands without asking.
- When in doubt, ask.
