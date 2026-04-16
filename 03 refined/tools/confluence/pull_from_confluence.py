#!/usr/bin/env python3
"""
Pull Confluence pages back into the local docs/ directory.

Reads the page map produced by sync_docs_to_confluence.py, fetches each
page from Confluence, converts HTML → Markdown, and overwrites the local
file when the Confluence version is newer.

Usage:
    python tools/pull_from_confluence.py [--dry-run] [--force]

Flags:
    --dry-run   Print planned actions without changing any local files.
    --force     Ignore version cache; overwrite all files unconditionally.

Required env vars (set in .env — same as sync_docs_to_confluence.py):
    CONFLUENCE_URL          e.g. https://your-domain.atlassian.net
    CONFLUENCE_EMAIL        your Atlassian account email
    CONFLUENCE_API_TOKEN    API token from id.atlassian.com
    CONFLUENCE_SPACE_KEY    target Confluence Space key (e.g. MARVIN)

State files (gitignored):
    tools/.confluence_page_map.json       local path → page_id  (written by push script)
    tools/.confluence_pull_versions.json  local path → last pulled version number
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import html2text
import requests
from dotenv import load_dotenv

# ── Paths ────────────────────────────────────────────────────────────────────

TOOLS_DIR = Path(__file__).parent
REPO_ROOT = TOOLS_DIR.parent.parent
DOCS_ROOT = REPO_ROOT / "projects" / "marvin" / "docs"
PAGE_MAP_PATH = TOOLS_DIR / ".confluence_page_map.json"
VERSIONS_PATH = TOOLS_DIR / ".confluence_pull_versions.json"

load_dotenv(REPO_ROOT / ".env")

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_env() -> dict:
    required = [
        "CONFLUENCE_URL",
        "CONFLUENCE_EMAIL",
        "CONFLUENCE_API_TOKEN",
    ]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        print(f"ERROR: Missing required env vars: {', '.join(missing)}", file=sys.stderr)
        print("Copy .env.example → .env and fill in Confluence credentials.", file=sys.stderr)
        sys.exit(1)
    return {k: os.environ[k] for k in required}


def load_page_map() -> dict:
    if not PAGE_MAP_PATH.exists():
        print(
            "ERROR: Page map not found. Run sync_docs_to_confluence.py first to push "
            "documents and generate the page map.",
            file=sys.stderr,
        )
        sys.exit(1)
    return json.loads(PAGE_MAP_PATH.read_text())


def load_versions() -> dict:
    if VERSIONS_PATH.exists():
        return json.loads(VERSIONS_PATH.read_text())
    return {}


def save_versions(versions: dict) -> None:
    VERSIONS_PATH.write_text(json.dumps(versions, indent=2, ensure_ascii=False))


def html_to_markdown(html: str) -> str:
    """Convert Confluence export HTML to Markdown."""
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = True      # Confluence image attachments are not portable
    converter.body_width = 0            # don't wrap lines
    converter.protect_links = False
    converter.unicode_snob = True
    converter.ignore_tables = False
    return converter.handle(html).strip()


def clean_markdown(text: str) -> str:
    """Light cleanup of html2text output for readability."""
    # Collapse 3+ blank lines to 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def fetch_page(base_url: str, page_id: str, auth: tuple) -> dict | None:
    """
    GET /wiki/rest/api/content/{id}?expand=body.export_view,version
    Returns the parsed JSON or None on error.
    """
    url = f"{base_url}/wiki/rest/api/content/{page_id}"
    params = {"expand": "body.export_view,version"}
    try:
        resp = requests.get(url, params=params, auth=auth, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.HTTPError as e:
        print(f"    [ERROR] HTTP {e.response.status_code} for page {page_id}: {e}", file=sys.stderr)
        return None
    except requests.RequestException as e:
        print(f"    [ERROR] Request failed for page {page_id}: {e}", file=sys.stderr)
        return None


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    dry_run = "--dry-run" in sys.argv
    force = "--force" in sys.argv

    if dry_run:
        print("=== DRY RUN — no local files will be changed ===\n")

    env = load_env()
    base_url = env["CONFLUENCE_URL"].rstrip("/")
    auth = (env["CONFLUENCE_EMAIL"], env["CONFLUENCE_API_TOKEN"])

    page_map = load_page_map()
    versions = load_versions()

    updated = 0
    skipped = 0
    errors = 0

    for rel_path, page_id in sorted(page_map.items()):
        local_file = DOCS_ROOT / rel_path

        # Fetch page from Confluence
        data = fetch_page(base_url, page_id, auth)
        if data is None:
            errors += 1
            continue

        confluence_version = data["version"]["number"]
        title = data["title"]

        # Version check — skip if not changed since last pull
        cached = versions.get(rel_path, {})
        if not force and cached.get("version") == confluence_version:
            print(f"  [SKIP]   {rel_path!r}  (Confluence v{confluence_version}, up to date)")
            skipped += 1
            continue

        action = "UPDATE" if local_file.exists() else "CREATE"

        # Convert HTML → Markdown
        html_body = data["body"]["export_view"]["value"]
        markdown = clean_markdown(html_to_markdown(html_body))

        # Add "Last updated" header (matches the format expected by sync_docs_to_confluence.py)
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        final_content = f"> Last updated: {today}\n\n{markdown}\n"

        if dry_run:
            cached_ver = cached.get("version", "–")
            print(
                f"  [{action}]  {rel_path!r}  "
                f"'{title}'  "
                f"(local pulled v{cached_ver} → Confluence v{confluence_version})"
            )
            updated += 1
            continue

        # Write to disk
        local_file.parent.mkdir(parents=True, exist_ok=True)
        local_file.write_text(final_content, encoding="utf-8")
        print(
            f"  [{action}]  {rel_path}  "
            f"(v{cached.get('version', '–')} → v{confluence_version})"
        )

        versions[rel_path] = {
            "page_id": page_id,
            "version": confluence_version,
            "pulled_at": datetime.now(timezone.utc).isoformat(),
        }
        updated += 1

    if not dry_run:
        save_versions(versions)
        print(f"\nVersion cache saved to: {VERSIONS_PATH}")

    print(f"\nDone — updated: {updated}, skipped: {skipped}, errors: {errors}")


if __name__ == "__main__":
    main()
