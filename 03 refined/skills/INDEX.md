# Skills Index

This index points to reusable Skills — tools, processes, and best practices that AI can invoke.

- **Want to use a capability** → Browse the categories below and find the corresponding skill file
- **Want to add a new skill** → Follow the existing file format and add it to the appropriate category

---

## Component Status

### Tier 1: Core (Ready to Use)
- ✅ Rules framework (SOUL/USER/COMMUNICATION/WORKSPACE) — fill in and use
- ✅ Skills framework (this directory) — fill in and use
- ✅ Three-layer memory system — requires configuring Claude Code memory + manually triggering observer/reflector

### Tier 2: Extensions (Require Additional Configuration)
- ⚙️ Semantic Search — requires LLM Studio or OpenAI API

### Notes
✅ = Ready to use in 15 minutes or less
⚙️ = Requires additional configuration; core functionality works without it

---

## Category Index

### Workflow

Complete workflows for specific tasks.

- [Confluence Bidirectional Sync](./workflow_confluence_sync.md) ✅ — Confluence ↔ Repo document bidirectional sync (all scripts in `tools/confluence/`)
  - **Push** (repo → Confluence): `tools/confluence/sync_docs_to_confluence.py`
  - **Pull** (Confluence → repo): `tools/confluence/pull_from_confluence.py` (version-tracked, idempotent)
  - **Convert** (batch `.doc` to Markdown): `tools/confluence/convert_confluence_docs.py`
  - **Diagram strategy**: Diagrams maintained manually in Confluence, not part of auto-sync
- [Cognitive Profile Extraction Workflow](./workflow_cognitive_profile_extraction.md) — Extract predictable cognitive axioms from unstructured conversation data
  - Applicable to: group chats / Slack / Discord / email / podcast transcripts and any conversational data
  - Process: broad scan → deep validation → stress testing → finalization (≥3 dynamic rolling rounds)
  - **Requires Opus model**: writing done by Opus directly, all research fully delegated + parallelized
- [Semantic Search Skill](./semantic_search.md) ⚙️ — Use vector similarity to retrieve deep context and evolution of views

### BestPractice

General best practices and lessons learned.

- [AI Programming Core Methodology](./bestpractice_ai_programming_mindset.md) ✅ — The 70% problem, success criteria, verifiability
- [Staged Approach](./bestpractice_staged_approach.md) ✅ — Isolate-process-verify closed loop, Dry Run before destructive operations
- [Multi-Agent Parallel Analysis](./bestpractice_multi_agent_analysis.md) ✅ — Topic splitting with 50% overlap, cross-validation
- [AI-Assisted Debugging Diagnosis](./bestpractice_ai_debugging_diagnosis.md) ✅ — Root cause diagnosis decision tree for "code that AI can't fix"

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
