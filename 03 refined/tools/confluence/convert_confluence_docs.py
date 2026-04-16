"""
Convert Confluence-exported .doc files (MIME/HTML format) to Markdown
and categorize them into the appropriate subdirectory.

Usage:
    python tools/convert_confluence_docs.py
    python tools/convert_confluence_docs.py --input-dir projects/marvin/context --output-dir projects/marvin/context

Reads from:  projects/marvin/docs/*.doc  (default)
Writes to:   projects/marvin/docs/{prd,architecture,sops,research}/  (default)

Options:
    --input-dir   DIR   Source directory containing .doc/.docx files (default: projects/marvin/docs)
    --output-dir  DIR   Destination base directory for converted Markdown (default: same as input-dir)
"""

import argparse
import email
import html2text
import os
import re
import sys
from pathlib import Path

# Categorization rules: filename keywords → target subdirectory
CATEGORY_RULES = [
    # (list of keywords to match in filename, target dir)
    (["system overview", "overview"],                       "architecture"),
    (["architecture", "diagram"],                           "architecture"),
    (["chatbot"],                                           "architecture"),
    (["loading", "chunking"],                               "architecture"),
    (["rag", "model", "endpoint"],                          "architecture"),
    (["vector", "index", "search"],                         "architecture"),
    (["codebase", "structure"],                             "architecture"),
    (["prerequisites", "requirements"],                     "prd"),
    (["how-to", "how to", "common changes"],                "sops"),
    (["repo", "databricks", "setup", "configuration"],      "sops"),
    (["optimisation", "optimization", "process"],           "sops"),
    (["evaluation"],                                        "research"),
    (["basics", "mlflow", "dab"],                           "research"),
]

def categorize(filename: str) -> str:
    name_lower = filename.lower().replace("+", " ").replace("_", " ")
    for keywords, category in CATEGORY_RULES:
        if any(kw in name_lower for kw in keywords):
            return category
    return "research"  # default fallback


def extract_html_from_mime(raw: bytes) -> str | None:
    msg = email.message_from_bytes(raw)
    for part in msg.walk():
        if part.get_content_type() == "text/html":
            payload = part.get_payload(decode=True)
            charset = part.get_content_charset() or "utf-8"
            return payload.decode(charset, errors="replace")
    return None


def html_to_markdown(html: str) -> str:
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = True   # images from Confluence are local paths, useless
    converter.body_width = 0         # don't wrap lines
    converter.protect_links = False
    converter.unicode_snob = True
    return converter.handle(html)


def clean_filename(name: str) -> str:
    # URL-decode + (plus signs → spaces), then snake_case
    name = name.replace("+", "_").replace(" ", "_").replace("&", "and")
    name = re.sub(r"[^\w\-]", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    return name.lower()


def main():
    parser = argparse.ArgumentParser(description="Convert Confluence .doc files to Markdown")
    parser.add_argument(
        "--input-dir",
        default=None,
        help="Source directory containing .doc/.docx files (default: projects/marvin/docs relative to repo root)",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Destination base directory for converted Markdown (default: same as --input-dir)",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent.parent
    if args.input_dir:
        base = Path(args.input_dir) if Path(args.input_dir).is_absolute() else repo_root / args.input_dir
    else:
        base = repo_root / "projects" / "marvin" / "docs"

    out_base = Path(args.output_dir) if args.output_dir else base
    if args.output_dir and not Path(args.output_dir).is_absolute():
        out_base = repo_root / args.output_dir

    doc_files = list(base.glob("*.doc")) + list(base.glob("*.docx"))

    if not doc_files:
        print("No .doc/.docx files found in", base)
        sys.exit(0)

    converted, skipped = 0, 0

    for doc_path in sorted(doc_files):
        raw = doc_path.read_bytes()

        html = extract_html_from_mime(raw)
        if not html:
            print(f"  SKIP (no HTML part): {doc_path.name}")
            skipped += 1
            continue

        markdown = html_to_markdown(html)

        category = categorize(doc_path.stem)
        out_dir = out_base / category
        out_dir.mkdir(parents=True, exist_ok=True)

        out_name = clean_filename(doc_path.stem) + ".md"
        out_path = out_dir / out_name

        out_path.write_text(markdown, encoding="utf-8")
        print(f"  [{category:12s}] {doc_path.name}  →  {out_dir}/{out_name}")
        converted += 1

    print(f"\nDone: {converted} converted, {skipped} skipped.")
    if converted > 0:
        print("Original .doc files kept — delete manually once you've verified the output.")


if __name__ == "__main__":
    main()
