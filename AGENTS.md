# AGENTS.md - meiqiao's Context Infrastructure

This folder is home. Treat it that way.

## Every Session

Before doing anything else:

1. Read `03 refined/SOUL.md` — this is who you are
2. Read `03 refined/USER.md` — this is who you're helping
3. Read `03 refined/WORKSPACE.md` — file routing table, check before searching for files
4. Read `03 refined/COMMUNICATION.md` — how to think and communicate (especially for non-coding tasks)
5. Read `03 refined/skills/INDEX.md` — understand available skills

## File Routing

**Before searching for any file, check `03 refined/WORKSPACE.md` first.** WORKSPACE.md is the directory index for this workspace — it records where each type of content lives. In most cases a quick look will point you to the right directory without needing to glob or grep everything. If you discover a new directory or project that isn't listed, update WORKSPACE.md.

**Before working on a specific project, read `projects/<name>/README.md`.** This is the entry point for each project, containing the project overview, document index, and current focus. For a list of active projects, see the Quick Reference section in WORKSPACE.md.

## Skills

**Skills** are reusable AI capabilities — workflows, API guides, best practices, and more.

**Important: when you need to do X, check skills before reaching for system tools.** Search order: (1) quick reference below → (2) `03 refined/skills/INDEX.md` → (3) system tools.

**Need to execute a task** → check `03 refined/skills/INDEX.md` for the right skill  
**Want to add a new capability** → follow the existing skill format and update INDEX.md

### Skills Quick Reference (INDEX.md is the source of truth)

**Import Confluence Docs** → `03 refined/skills/workflow_confluence_sync.md`  
- Convert Confluence pages to Markdown and file them under `projects/<name>/`  
- Companion script: `03 refined/tools/confluence/convert_confluence_docs.py`

## Axioms

Decision principles distilled from personal experience, used to inspire deeper thinking. For the categorized index, usage guide, and trigger words, see `03 refined/axioms/INDEX.md`.

## Memory System

The **root-level** three-layer architecture is organized by **degree of knowledge processing** (capture → personal understanding → canonicalization):
- **01 raw/**: all raw inputs (conversation logs, scripts, unprocessed notes) — stored locally
- **02 trusted/**: refinements of raw (`OBSERVATIONS.md` daily observations + weekly reflections) 
- **03 refined/**: passively loaded reusable knowledge system (axioms, skills, core guides)

The **project-level** three-layer architecture is organized by **direction of information flow**:
- **01 raw/**: all raw inputs (meeting notes, requirements docs, bug reports, AI conversation outputs) — stored locally
- **02 trusted/**: stable knowledge that helps me/AI understand and operate the project — architecture docs, design decisions, research conclusions, SOPs
- **03 refined/**: content prepared for audiences outside the project — stakeholder briefs, team presentations, Confluence output docs

## Safety

- Don't exfiltrate private data. Ever.
- Don't run destructive commands without asking.
- When in doubt, ask.
