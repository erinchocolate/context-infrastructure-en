#!/usr/bin/env python3
"""
rst_to_markdown.py - Pure Python RST to Markdown converter.

No third-party dependencies. Works with Python 3.8+.

Handles:
  - Section headings (underline-based hierarchy → # ## ###)
  - Code blocks (.. code-block:: lang → fenced ```)
  - Admonitions (.. note:: / .. warning:: → blockquote)
  - Inline code (:code:`text` → `text`)
  - Cross-references (:ref:`label` → plain label text)
  - External hyperlinks (`text <url>`_ → [text](url))
  - RST simple tables (=== separators → GFM pipe table)
  - RST grid tables (+--+ borders → GFM pipe table)
  - Images (.. image:: → ![](path))
  - UML blocks (.. uml:: → ```plantuml)
  - Auto-numbered lists (#. → 1. 2. 3.)
  - Reference anchors (.. _label: → dropped)
  - Navigation directives (toctree, contents → dropped)

Usage:
    # Single file
    python rst_to_markdown.py input.rst output.md

    # Batch mode
    python rst_to_markdown.py --batch file1.rst file2.rst --output-dir /path/to/out/

    # Batch with shell glob (expand before passing)
    python rst_to_markdown.py --batch /src/*.rst --output-dir /out/
"""

import re
import sys
import argparse
from pathlib import Path


# Valid RST heading adornment characters
HEADING_CHARS = set('=-~^+#*._@<>!&')


def is_heading_underline(line: str) -> bool:
    """Return True if line is an RST heading adornment (single char repeated ≥ 2 times)."""
    s = line.rstrip()
    return len(s) >= 2 and len(set(s)) == 1 and s[0] in HEADING_CHARS


def convert_inline(text: str) -> str:
    """Convert RST inline markup to Markdown equivalents."""
    # :code:`text` → `text`
    text = re.sub(r':code:`([^`]*)`', r'`\1`', text)
    # :ref:`display <target>` → display
    text = re.sub(r':ref:`([^`<]+?)\s*<[^>`]+>`', lambda m: m.group(1).strip(), text)
    # :ref:`label` → label
    text = re.sub(r':ref:`([^`]+)`', r'\1', text)
    # `display text <url>`_ or `display text <url>`__ → [display text](url)
    text = re.sub(r'`([^`<]+?)\s*<(https?://[^>]+)>`__?', r'[\1](\2)', text)
    # Pipe characters in table cells need escaping (handled at emit time)
    return text


def is_simple_sep(line: str) -> bool:
    """Return True if line is an RST simple table separator (e.g. '=== === ===')."""
    s = line.strip()
    if not s:
        return False
    parts = s.split()
    return len(parts) >= 1 and all(re.match(r'^=+$', p) for p in parts)


class RstConverter:
    def __init__(self):
        self.heading_chars: list = []  # first-seen order → determines level
        self.lines: list = []
        self.output: list = []
        self.i: int = 0

    def _get_heading_level(self, char: str) -> int:
        if char not in self.heading_chars:
            self.heading_chars.append(char)
        return self.heading_chars.index(char) + 1

    def _line(self, offset: int = 0) -> str:
        idx = self.i + offset
        return self.lines[idx] if 0 <= idx < len(self.lines) else ''

    def _advance(self, n: int = 1):
        self.i += n

    # ── Public entry point ────────────────────────────────────────────────────

    def convert(self, text: str) -> str:
        self.heading_chars = []
        self.lines = text.split('\n')
        self.output = []
        self.i = 0

        while self.i < len(self.lines):
            self._process_line()

        result = '\n'.join(self.output)
        result = re.sub(r'\n{3,}', '\n\n', result)
        return result.strip() + '\n'

    # ── Main dispatch ─────────────────────────────────────────────────────────

    def _process_line(self):
        line = self._line()
        stripped = line.strip()

        # ── Drop RST cross-reference anchors: .. _something: ─────────────────
        if re.match(r'^\.\.\s+_[^:]+:\s*$', stripped):
            self._advance()
            return

        # ── Heading: current line = title, next line = underline ──────────────
        next_line = self._line(1)
        if (stripped
                and not stripped.startswith('..')
                and not stripped.startswith('|')
                and is_heading_underline(next_line)
                and len(next_line.rstrip()) >= max(2, len(stripped) // 2)):
            char = next_line.strip()[0]
            level = self._get_heading_level(char)
            self.output.append('')
            self.output.append('#' * level + ' ' + stripped)
            self.output.append('')
            self._advance(2)
            return

        # ── Heading: overline + title + underline (all same char) ─────────────
        if (is_heading_underline(line)
                and self._line(1).strip()
                and is_heading_underline(self._line(2))):
            char = line.strip()[0]
            level = self._get_heading_level(char)
            self.output.append('')
            self.output.append('#' * level + ' ' + self._line(1).strip())
            self.output.append('')
            self._advance(3)
            return

        # ── Stray adornment line (already consumed by heading or table) ───────
        if is_heading_underline(line):
            self._advance()
            return

        # ── Directives ────────────────────────────────────────────────────────

        # code-block / code
        m = re.match(r'^\.\.\s+code(?:-block)?::\s*(\S*)', stripped)
        if m:
            self._handle_code_block(m.group(1))
            return

        # admonitions
        m = re.match(
            r'^\.\.\s+(note|warning|tip|important|caution|danger|attention|hint)::\s*(.*)',
            stripped, re.IGNORECASE)
        if m:
            self._handle_admonition(m.group(1).capitalize(), m.group(2).strip())
            return

        # image
        m = re.match(r'^\.\.\s+image::\s+(\S+)', stripped)
        if m:
            self._handle_image(m.group(1))
            return

        # figure (treat like image)
        m = re.match(r'^\.\.\s+figure::\s+(\S+)', stripped)
        if m:
            self._handle_image(m.group(1))
            return

        # uml
        if re.match(r'^\.\.\s+uml::', stripped):
            self._handle_uml()
            return

        # drop navigation directives
        if re.match(r'^\.\.\s+(contents|toctree|include)::', stripped):
            self._skip_directive_body()
            return

        # other unknown directives — skip body
        if re.match(r'^\.\.\s+\w[\w-]*::', stripped):
            self._skip_directive_body()
            return

        # RST comment: just ".." with no content
        if re.match(r'^\.\.\s*$', stripped):
            self._skip_directive_body()
            return

        # ── RST simple table (=== === ===) ────────────────────────────────────
        if is_simple_sep(line):
            self._handle_simple_table()
            return

        # ── RST grid table (+---+---+) ────────────────────────────────────────
        if re.match(r'^\+[-=+]{2,}', stripped):
            self._handle_grid_table()
            return

        # ── Auto-numbered list (#. item) ──────────────────────────────────────
        if re.match(r'^#\.\s', stripped):
            self._handle_numbered_list()
            return

        # ── Regular line ──────────────────────────────────────────────────────
        self.output.append(convert_inline(line))
        self._advance()

    # ── Block collectors ──────────────────────────────────────────────────────

    def _collect_indented_block(self) -> list:
        """Advance past the directive line, then collect its indented body."""
        self._advance()  # past the directive line itself
        # Skip leading blank lines
        while self.i < len(self.lines) and not self.lines[self.i].strip():
            self._advance()
        if self.i >= len(self.lines):
            return []
        # Detect block indent from first non-blank line
        first = self.lines[self.i]
        block_indent = len(first) - len(first.lstrip())
        if block_indent == 0:
            return []
        # Collect lines until indentation returns to base level
        block = []
        while self.i < len(self.lines):
            ln = self.lines[self.i]
            if not ln.strip():
                block.append('')
                self._advance()
                continue
            cur_indent = len(ln) - len(ln.lstrip())
            if cur_indent < block_indent:
                break
            block.append(ln[block_indent:])
            self._advance()
        # Strip trailing blank lines
        while block and not block[-1]:
            block.pop()
        return block

    def _skip_directive_body(self):
        """Skip current directive line and its indented body."""
        self._advance()
        while self.i < len(self.lines) and not self.lines[self.i].strip():
            self._advance()
        if self.i >= len(self.lines):
            return
        first = self.lines[self.i]
        block_indent = len(first) - len(first.lstrip())
        if block_indent == 0:
            return
        while self.i < len(self.lines):
            ln = self.lines[self.i]
            if not ln.strip():
                self._advance()
                continue
            if len(ln) - len(ln.lstrip()) < block_indent:
                break
            self._advance()

    # ── Directive handlers ────────────────────────────────────────────────────

    def _handle_code_block(self, lang: str):
        block = self._collect_indented_block()
        self.output.append('')
        self.output.append(f'```{lang}')
        self.output.extend(block)
        self.output.append('```')
        self.output.append('')

    def _handle_admonition(self, kind: str, inline_text: str):
        block = self._collect_indented_block()
        all_lines = ([inline_text] if inline_text else []) + block
        self.output.append('')
        for j, bline in enumerate(all_lines):
            prefix = f'> **{kind}:** ' if j == 0 else '> '
            self.output.append(prefix + convert_inline(bline))
        self.output.append('')

    def _handle_image(self, path: str):
        alt = ''
        self._advance()  # past `.. image:: path`
        # Consume option lines (:alt:, :width:, etc.)
        while self.i < len(self.lines):
            ln = self.lines[self.i]
            if not ln.strip():
                break
            m = re.match(r'^\s+:alt:\s+(.+)$', ln)
            if m:
                alt = m.group(1)
                self._advance()
            elif re.match(r'^\s+:\w[\w-]*:', ln):
                self._advance()
            else:
                break
        self.output.append('')
        self.output.append(f'![{alt}]({path})')
        self.output.append('')

    def _handle_uml(self):
        block = self._collect_indented_block()
        self.output.append('')
        self.output.append('```plantuml')
        self.output.extend(block)
        self.output.append('```')
        self.output.append('')

    def _handle_numbered_list(self):
        """Convert RST #. auto-numbered items to Markdown 1. 2. 3. list."""
        items = []
        while self.i < len(self.lines):
            ln = self.lines[self.i]
            stripped = ln.strip()
            m = re.match(r'^#\.\s+(.+)$', stripped)
            if m:
                items.append(m.group(1))
                self._advance()
                # Absorb indented continuation lines
                while self.i < len(self.lines):
                    cont = self.lines[self.i]
                    if (cont.strip()
                            and not re.match(r'^#\.', cont.strip())
                            and len(cont) - len(cont.lstrip()) > 0):
                        items[-1] += ' ' + cont.strip()
                        self._advance()
                    else:
                        break
            else:
                break
        self.output.append('')
        for idx, item in enumerate(items, 1):
            self.output.append(f'{idx}. {convert_inline(item)}')
        self.output.append('')

    # ── Table handlers ────────────────────────────────────────────────────────

    @staticmethod
    def _parse_simple_col_positions(sep_line: str) -> list:
        """Extract (start, end) column ranges from a simple table separator line."""
        cols = []
        in_col = False
        start = None
        for j, c in enumerate(sep_line.rstrip() + ' '):
            if c == '=' and not in_col:
                start = j
                in_col = True
            elif c != '=' and in_col:
                cols.append((start, j))
                in_col = False
        return cols

    def _handle_simple_table(self):
        """Convert RST simple table (=== separators) to GFM pipe table."""
        sep_line = self._line().rstrip()
        cols = self._parse_simple_col_positions(sep_line)

        if not cols:
            self._advance()
            return

        # Collect all table lines, stopping after the 3rd separator
        all_lines = []
        sep_positions = []
        while self.i < len(self.lines):
            ln = self.lines[self.i].rstrip()
            all_lines.append(ln)
            if is_simple_sep(ln):
                sep_positions.append(len(all_lines) - 1)
            self._advance()
            if len(sep_positions) >= 3:
                break

        # Need at least 2 separators (start + end-of-header)
        if len(sep_positions) < 2:
            for ln in all_lines:
                self.output.append(ln)
            return

        sep0 = sep_positions[0]
        sep1 = sep_positions[1]
        sep2 = sep_positions[2] if len(sep_positions) >= 3 else len(all_lines) - 1

        header_lines = all_lines[sep0 + 1:sep1]
        data_lines = all_lines[sep1 + 1:sep2]

        def extract_row(line: str) -> list:
            cells = []
            for s, e in cols:
                cell = line[s:min(e, len(line))].strip() if len(line) > s else ''
                cells.append(cell)
            return cells

        # Build header (may span multiple lines)
        header = [''] * len(cols)
        for hline in header_lines:
            if not hline.strip():
                continue
            for idx, cell in enumerate(extract_row(hline)):
                if cell:
                    header[idx] = (header[idx] + ' ' + cell).strip()

        # Build data rows — continuation lines have empty first column
        rows = []
        current: list | None = None
        for dline in data_lines:
            if not dline.strip():
                continue
            cells = extract_row(dline)
            if cells[0]:  # new row starts when first col is non-empty
                if current is not None:
                    rows.append(current)
                current = cells[:]
            elif current is not None:
                for idx, cell in enumerate(cells):
                    if cell:
                        current[idx] = (current[idx] + ' ' + cell).strip()
        if current is not None:
            rows.append(current)

        self._emit_md_table(header, rows)

    def _handle_grid_table(self):
        """Convert RST grid table (+--+ borders) to GFM pipe table."""
        # Collect all grid table lines (they start with + or |)
        table_lines = []
        while self.i < len(self.lines):
            ln = self.lines[self.i].rstrip()
            if not ln.strip():
                break
            if not re.match(r'^[+|]', ln):
                break
            table_lines.append(ln)
            self._advance()

        if not table_lines:
            return

        # Parse column ranges from the first border line
        sep = table_lines[0]
        plus_pos = [j for j, c in enumerate(sep) if c == '+']
        if len(plus_pos) < 2:
            for ln in table_lines:
                self.output.append(ln)
            return

        col_ranges = [(plus_pos[k] + 1, plus_pos[k + 1])
                      for k in range(len(plus_pos) - 1)]
        num_cols = len(col_ranges)

        headers = [''] * num_cols
        rows = []
        current = [''] * num_cols
        header_done = False

        for tline in table_lines:
            if re.match(r'^\+[=+]+\+', tline):
                # Header separator row — finalize header accumulation
                if any(h.strip() for h in headers):
                    header_done = True
                current = [''] * num_cols
                continue
            if re.match(r'^\+[-+]+\+', tline):
                # Data row separator — save current row
                if any(c.strip() for c in current):
                    if not header_done:
                        for k, c in enumerate(current):
                            if c.strip():
                                headers[k] = (headers[k] + ' ' + c).strip()
                    else:
                        rows.append([c.strip() for c in current])
                current = [''] * num_cols
                continue
            if tline.startswith('|'):
                for idx, (s, e) in enumerate(col_ranges):
                    if idx >= num_cols:
                        break
                    cell = tline[s:min(e, len(tline))].strip() if len(tline) > s else ''
                    if cell:
                        current[idx] = (current[idx] + ' ' + cell).strip()

        # Flush last accumulated row
        if any(c.strip() for c in current):
            if not header_done:
                for k, c in enumerate(current):
                    if c.strip():
                        headers[k] = (headers[k] + ' ' + c).strip()
            else:
                rows.append([c.strip() for c in current])

        if not any(h.strip() for h in headers) and rows:
            headers = rows.pop(0)

        self._emit_md_table(headers, rows)

    def _emit_md_table(self, headers: list, rows: list):
        """Emit a GFM pipe table."""
        if not headers:
            return

        def fmt_cell(c: str) -> str:
            # Escape pipe chars and apply inline conversion
            return convert_inline(c.replace('|', '\\|'))

        self.output.append('')
        self.output.append('| ' + ' | '.join(fmt_cell(h) for h in headers) + ' |')
        self.output.append('| ' + ' | '.join('---' for _ in headers) + ' |')
        for row in rows:
            while len(row) < len(headers):
                row.append('')
            self.output.append(
                '| ' + ' | '.join(fmt_cell(c) for c in row[:len(headers)]) + ' |')
        self.output.append('')


# ── File I/O ──────────────────────────────────────────────────────────────────

def convert_file(input_path: Path, output_path: Path):
    text = input_path.read_text(encoding='utf-8')
    converter = RstConverter()
    result = converter.convert(text)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(result, encoding='utf-8')
    print(f'  ✓ {input_path.name} → {output_path}')


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Convert RST documentation to Markdown (pure Python, no dependencies).',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__)
    parser.add_argument('input', nargs='?', help='Input RST file')
    parser.add_argument('output', nargs='?',
                        help='Output Markdown file (default: same stem, .md extension)')
    parser.add_argument('--batch', nargs='+', metavar='FILE',
                        help='Batch mode: one or more input RST files')
    parser.add_argument('--output-dir', metavar='DIR',
                        help='Output directory (required for --batch)')
    args = parser.parse_args()

    if args.batch:
        if not args.output_dir:
            print('Error: --output-dir is required for batch mode.', file=sys.stderr)
            sys.exit(1)
        out_dir = Path(args.output_dir)
        for f in args.batch:
            in_path = Path(f)
            out_path = out_dir / (in_path.stem + '.md')
            convert_file(in_path, out_path)
    elif args.input:
        in_path = Path(args.input)
        out_path = Path(args.output) if args.output else in_path.with_suffix('.md')
        convert_file(in_path, out_path)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
