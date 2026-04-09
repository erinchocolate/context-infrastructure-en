# Workflow: Confluence Document Bidirectional Sync

## Metadata

- **Type**: Workflow
- **Applicable Scenarios**: Confluence ↔ Repo document bidirectional sync; converting Confluence export files to Markdown; pushing local Markdown to Confluence
- **Creation Date**: 2026-04-09
- **Updated Date**: 2026-04-09
- **Tool Path**: `tools/confluence/`
- **Tool Dependencies**: `html2text`, `requests`, `python-dotenv`, `mistune`, `md2cf`

---

## Tool Overview

All scripts are located in `context-infrastructure/tools/confluence/`, run using the workspace venv:

```bash
source /opt/processes/mc_platform/venv/bin/activate
cd /opt/processes/mc_platform/context-infrastructure
```

| Script | Purpose |
|--------|---------|
| `sync_docs_to_confluence.py` | Push: push Markdown files under `projects/marvin/docs/` to Confluence (create new or update existing) |
| `pull_from_confluence.py` | Pull: pull pages from Confluence to local, skipping unchanged pages by version number |
| `convert_confluence_docs.py` | Convert: batch-convert `.doc`/`.docx` files exported from Confluence to Markdown, categorized by type |

State files (stored in `tools/confluence/`, gitignored):
- `.confluence_page_map.json` — mapping from local path → Confluence page ID (written by push script)
- `.confluence_pull_versions.json` — version number of each page at last pull (written by pull script)

---

## Environment Configuration

Set in `context-infrastructure/.env` (refer to `.env.example`):

```bash
CONFLUENCE_URL=https://your-domain.atlassian.net
CONFLUENCE_EMAIL=your@email.com
CONFLUENCE_API_TOKEN=<token from id.atlassian.com>
CONFLUENCE_SPACE_KEY=MARVIN
CONFLUENCE_ROOT_TITLE=Project Marvin - AI Context  # optional, this is the default value
```

---

## Usage

### 1. Push: Local Markdown → Confluence

Push all Markdown files under `projects/marvin/docs/` to Confluence. First run creates pages automatically; subsequent runs update existing pages.

```bash
# Dry run (only print plan, no actual push)
python tools/confluence/sync_docs_to_confluence.py --dry-run

# Actual push
python tools/confluence/sync_docs_to_confluence.py
```

**Directory structure mapping** (hierarchy automatically created in Confluence):
```
Root page (CONFLUENCE_ROOT_TITLE)
├── Architecture  ← docs/architecture/*.md
├── Design        ← docs/design/*.md
├── SOPs          ← docs/sops/*.md
└── Research      ← docs/research/*.md
```

After push completes, `.confluence_page_map.json` is automatically updated, saving page ID mappings for subsequent incremental updates.

---

### 2. Pull: Confluence → Local Markdown

Pull page content from Confluence to update local files. Implements idempotency through version number caching (unchanged pages are automatically skipped).

```bash
# Dry run
python tools/confluence/pull_from_confluence.py --dry-run

# Actual pull (only updates pages where Confluence version is newer than local)
python tools/confluence/pull_from_confluence.py

# Force overwrite all pages
python tools/confluence/pull_from_confluence.py --force
```

**Prerequisite**: At least one push must have been executed, otherwise `.confluence_page_map.json` does not exist and pull will error.

---

### 3. Convert: Batch-Convert Confluence Export Files

Batch-convert `.doc` (MIME/HTML format) files exported from Confluence pages to Markdown, automatically categorized by content type.

```bash
# Default: convert projects/marvin/docs/*.doc, output to subdirectory in same directory
python tools/confluence/convert_confluence_docs.py

# Specify input/output directories
python tools/confluence/convert_confluence_docs.py \
  --input-dir projects/marvin/context \
  --output-dir projects/marvin/docs
```

**Auto-categorization rules** (based on filename keywords):
- `architecture/`: system overview, architecture, chatbot, loading, rag, vector, codebase
- `prd/`: prerequisites, requirements
- `sops/`: how-to, common changes, setup, configuration, optimisation
- `research/`: evaluation, mlflow, dab, and default fallback

**How to get export files**: Confluence page → `···` → `Export` → `Word (.doc)`

---

## Typical Workflows

### Scenario A: Initial Sync (Existing Confluence Documents → Repo)

```bash
# Step 1: Export .doc files from Confluence to projects/marvin/docs/
# Step 2: Batch convert
python tools/confluence/convert_confluence_docs.py

# Step 3: Check conversion results, manually categorize unrecognized files

# Step 4: Push back to Confluence, establish page map
python tools/confluence/sync_docs_to_confluence.py --dry-run
python tools/confluence/sync_docs_to_confluence.py
```

### Scenario B: Daily Maintenance (Repo as Primary Source)

```bash
# Edit Markdown in repo → Push to Confluence
python tools/confluence/sync_docs_to_confluence.py
```

### Scenario C: Daily Maintenance (Confluence as Primary Source)

```bash
# Pull latest content from Confluence
python tools/confluence/pull_from_confluence.py
```

---

## Notes

- **Diagrams are not part of auto-sync**: Confluence drawio/diagram charts must be maintained manually; scripts do not handle image attachments
- **Internal links**: Cross-page links in Confluence are invalid in local Markdown and must be manually replaced with relative paths
- **File naming conventions**: Local files should use `YYYY-MM-DD_<title-snake-case>.md` format
- **Page map lost**: If `.confluence_page_map.json` is lost, next push will create duplicate pages on the Confluence side; manually delete duplicates and rebuild

---

## Dependency Installation

```bash
source /opt/processes/mc_platform/venv/bin/activate
pip install html2text requests python-dotenv mistune md2cf
```
