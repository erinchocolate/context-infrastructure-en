# Skills Index

This index points to reusable Skills — tools, processes, and best practices that AI can invoke.

- **Want to use a capability** → Browse the categories below and find the corresponding skill file
- **Want to add a new skill** → Follow the existing file format and add it to the appropriate category

---

## Category Index

### Workflow

Complete workflows for specific tasks.

- [Confluence Bidirectional Sync](./workflow_confluence_sync.md) — Confluence ↔ Repo document bidirectional sync (all scripts in `tools/confluence/`)
  - **Push** (repo → Confluence): `tools/confluence/sync_docs_to_confluence.py`
  - **Pull** (Confluence → repo): `tools/confluence/pull_from_confluence.py` (version-tracked, idempotent)
  - **Convert** (batch `.doc` to Markdown): `tools/confluence/convert_confluence_docs.py`
  - **Diagram strategy**: Diagrams maintained manually in Confluence, not part of auto-sync
- [PR Code Review](./workflow_pr_review.md) — AI-assisted code review for PRs/branches in the `data_platform` repo; auto-matches guidelines, parallel sub-agents, generates a structured report
- [RST → Markdown Conversion](./workflow_rst_to_markdown.md) — Batch-convert Sphinx RST documentation to Markdown; covers headings, code blocks, tables, directives

### BestPractice

General best practices and lessons learned.

- [AI Programming Core Methodology](./bestpractice_ai_programming_mindset.md) — The 70% problem, success criteria, verifiability
- [AI-Assisted Debugging Diagnosis](./bestpractice_ai_debugging_diagnosis.md) — Root cause diagnosis decision tree for "code that AI can't fix"

---

## How to Add Your Own Skill

1. Follow the format of existing skill files (metadata, core description, steps, examples)
2. Name it `<category>_<name>.md` (e.g., `workflow_my_process.md`, `bestpractice_my_insight.md`)
3. Add a line in the corresponding category in INDEX.md

Skill format reference (minimal version):
```markdown
# Skill: Name

## When to Use
What situation triggers this skill

## Prerequisites
What tools/configuration are needed

## Steps
1. Step one
2. Step two
```

## Progressive Disclosure

Skills follow the progressive disclosure principle:
- **INDEX.md** provides an overview for quick navigation
- **Specific skill files** contain complete operational steps and examples
