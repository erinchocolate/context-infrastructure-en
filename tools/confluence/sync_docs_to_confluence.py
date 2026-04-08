#!/usr/bin/env python3
"""
Push projects/marvin/docs/ Markdown files to Confluence Cloud.

Usage:
    python tools/sync_docs_to_confluence.py [--dry-run] [--project marvin]

Required env vars (set in .env):
    CONFLUENCE_URL          e.g. https://your-domain.atlassian.net
    CONFLUENCE_EMAIL        your Atlassian account email
    CONFLUENCE_API_TOKEN    API token from id.atlassian.com
    CONFLUENCE_SPACE_KEY    target Confluence Space key (e.g. MARVIN)

Optional env vars:
    CONFLUENCE_ROOT_TITLE   default: "Project Marvin - AI Context"

Page map: tools/.confluence_page_map.json (gitignored)
    Maps local relative file path → Confluence page ID for idempotent updates.
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import mistune
from md2cf.api import MinimalConfluence
from md2cf.confluence_renderer import ConfluenceRenderer

# ── Paths ───────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent.parent.parent
DOCS_ROOT = REPO_ROOT / "projects" / "marvin" / "docs"
PAGE_MAP_PATH = Path(__file__).parent / ".confluence_page_map.json"

# Load .env from repo root
load_dotenv(REPO_ROOT / ".env")

SUBDIR_LABELS = {
    "architecture": "Architecture",
    "design": "Design",
    "sops": "SOPs",
    "research": "Research",
}

# ── Helpers ──────────────────────────────────────────────────────────────────

def load_env() -> dict:
    required = [
        "CONFLUENCE_URL",
        "CONFLUENCE_EMAIL",
        "CONFLUENCE_API_TOKEN",
        "CONFLUENCE_SPACE_KEY",
    ]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        print(f"ERROR: Missing required env vars: {', '.join(missing)}", file=sys.stderr)
        print("Copy .env.example → .env and fill in Confluence credentials.", file=sys.stderr)
        sys.exit(1)
    return {k: os.environ[k] for k in required}


def load_page_map() -> dict:
    if PAGE_MAP_PATH.exists():
        return json.loads(PAGE_MAP_PATH.read_text())
    return {}


def save_page_map(page_map: dict) -> None:
    PAGE_MAP_PATH.write_text(json.dumps(page_map, indent=2, ensure_ascii=False))


def md_to_storage(md_text: str) -> str:
    """Convert Markdown to Confluence storage format using md2cf renderer."""
    renderer = ConfluenceRenderer(use_xhtml=True)
    md = mistune.Markdown(renderer=renderer)
    return md(md_text)


def file_title(md_file: Path) -> str:
    """Convert filename to a human-readable Confluence page title."""
    stem = md_file.stem
    # Remove date prefix like "2026-04-07_" if present
    parts = stem.split("_", 1)
    if len(parts) == 2 and len(parts[0]) == 10 and parts[0][4] == "-":
        stem = parts[1]
    return stem.replace("_", " ").replace("-", " ").title()


def get_or_create_page(
    cf: MinimalConfluence,
    space_key: str,
    title: str,
    body: str = "<p></p>",
    parent_id: str = None,
    dry_run: bool = False,
) -> tuple[str, bool]:
    """Return (page_id, was_created). Creates the page if it doesn't exist."""
    page = cf.get_page(title=title, space_key=space_key)
    if page is not None:
        return str(page.id), False
    if dry_run:
        return f"[dry-run:{title}]", True
    page = cf.create_page(
        space=space_key,
        title=title,
        body=body,
        parent_id=parent_id,
    )
    return str(page.id), True


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    dry_run = "--dry-run" in sys.argv

    env = load_env()  # validates credentials before anything else

    if dry_run:
        print("=== DRY RUN — no changes will be made to Confluence ===\n")
    cf = MinimalConfluence(
        host=env["CONFLUENCE_URL"].rstrip("/") + "/wiki/rest/api/",
        username=env["CONFLUENCE_EMAIL"],
        password=env["CONFLUENCE_API_TOKEN"],
    )
    space = env["CONFLUENCE_SPACE_KEY"]
    root_title = os.environ.get("CONFLUENCE_ROOT_TITLE", "Project Marvin - AI Context")

    page_map = load_page_map()

    # ── Root parent page ──────────────────────────────────────────────────
    root_id, created = get_or_create_page(cf, space, root_title, dry_run=dry_run)
    print(f"{'[CREATE]' if created else '[FOUND] '} Root page: '{root_title}' (id={root_id})")

    # ── Subdirectories → section pages ───────────────────────────────────
    for subdir, label in SUBDIR_LABELS.items():
        subdir_path = DOCS_ROOT / subdir
        if not subdir_path.exists():
            continue

        section_id, created = get_or_create_page(
            cf, space, label, parent_id=root_id, dry_run=dry_run
        )
        if created:
            print(f"\n  [CREATE] Section: '{label}' (id={section_id})")
        else:
            print(f"\n  [FOUND]  Section: '{label}' (id={section_id})")

        # ── Markdown files → child pages ──────────────────────────────
        for md_file in sorted(subdir_path.glob("*.md")):
            if md_file.stem.startswith("."):
                continue

            rel = str(md_file.relative_to(DOCS_ROOT))
            title = file_title(md_file)
            body = md_to_storage(md_file.read_text())

            if dry_run:
                action = "UPDATE" if rel in page_map else "CREATE"
                print(f"    [{action}] {rel!r} → '{title}'")
                continue

            if rel in page_map:
                # Fetch current page (needed for version number) then update
                try:
                    page = cf.get_page(page_id=page_map[rel])
                    cf.update_page(
                        page,
                        body=body,
                        update_message="Synced from context-infrastructure repo",
                    )
                    print(f"    [UPDATE] {rel}")
                except Exception as e:
                    print(f"    [ERROR]  {rel}: {e}")
            else:
                try:
                    page = cf.create_page(
                        space=space,
                        title=title,
                        body=body,
                        parent_id=section_id,
                        update_message="Initial sync from context-infrastructure repo",
                    )
                    page_map[rel] = str(page.id)
                    print(f"    [CREATE] {rel} (id={page.id})")
                except Exception as e:
                    print(f"    [ERROR]  {rel}: {e}")

    if not dry_run:
        save_page_map(page_map)
        print(f"\nPage map saved to: {PAGE_MAP_PATH}")

    print("\nDone.")


if __name__ == "__main__":
    main()
