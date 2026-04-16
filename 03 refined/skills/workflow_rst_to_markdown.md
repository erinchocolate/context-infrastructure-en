# Workflow: RST → Markdown Document Conversion

## Metadata

- **Type**: Workflow
- **Use Case**: Batch-convert Sphinx RST documentation to Markdown for import into the Marvin project's guidelines or any Markdown-native context
- **Created**: 2026-04-13
- **Tool Path**: `03 refined/tools/rst_to_markdown.py`
- **Dependencies**: Python 3.8+ (standard library only — no third-party packages required)

---

## Script Capabilities

`rst_to_markdown.py` is a pure-Python state-machine converter that handles the following RST constructs:

| RST Construct | Markdown Output | Notes |
|---|---|---|
| Headings (underline chars `= - ~ ^`) | `# ## ###` | Heading level determined dynamically by first-occurrence order |
| `.. code-block:: lang` | ` ```lang ``` ` | Language annotation preserved |
| `.. note::` / `.. warning::` | `> **Note:** ...` blockquote | Supports note / warning / tip / important / caution |
| `:code:\`text\`` | `` `text` `` | Inline code |
| `:ref:\`label\`` | Plain text label | Cross-document references cannot be resolved; text is kept as-is |
| `` `text <url>`_ `` | `[text](url)` | External links converted to Markdown links |
| Simple tables (`===`) | GFM pipe table | Multi-line cell content joined into a single line |
| Grid tables (`+--+`) | GFM pipe table | Multi-line cells merged |
| `.. image:: path` | `![alt](path)` | Extracts the `:alt:` option |
| `.. uml::` | ` ```plantuml ``` ` | UML body preserved |
| `.. _label:` anchors | Dropped | Cross-document anchors have no meaning in Markdown |
| `.. toctree::` / `.. contents::` | Dropped | Navigation directives are irrelevant in Markdown |
| `#.` auto-numbered lists | `1. 2. 3.` | Expanded in order |

---

## Usage

```bash
cd /opt/processes/mc_platform/context-infrastructure

# Single file conversion
python3 "03 refined/tools/rst_to_markdown.py" input.rst output.md

# Batch conversion (shell glob expanded before passing in)
python3 "03 refined/tools/rst_to_markdown.py" \
  --batch /path/to/docs/*.rst \
  --output-dir "projects/marvin/02 trusted/guidelines"
```

---

## Typical Workflow: Importing New RST Standard Documents

### Steps

1. **Confirm the source file location**

   Data Platform documentation source is at:
   ```
   /opt/processes/documentation/docs/src/standards/
   ```

2. **Run batch conversion**

   ```bash
   cd /opt/processes/mc_platform/context-infrastructure
   python3 "03 refined/tools/rst_to_markdown.py" \
     --batch /opt/processes/documentation/docs/src/standards/<name>.rst \
     --output-dir "projects/marvin/02 trusted/guidelines"
   ```

3. **Review output quality**

   Key things to check:
   - Are heading levels correct? (h1 = document title, h2 = major section, h3 = subsection)
   - Do code blocks have language annotations? (SQL / Python should be preserved)
   - Are multi-line cells in large tables joined reasonably?
   - Have `:ref:` references degraded gracefully to readable text?

4. **Manually correct where necessary**

   The following cases require manual handling:
   - `.. image::` image paths (relative paths break in the new location; replace with absolute paths or comment out)
   - `.. uml::` PlantUML blocks (delete if the rendering environment doesn't support them)
   - Overly complex tables (multi-column + multi-row + nested lists) — consider rewriting as definition lists manually

5. **Update `WORKSPACE.md`** (if a new document category was added)

---

## Converted Standard Documents

Stored at: `projects/guidelines/`

### 2026-04-13 First Batch

| File | Content |
|---|---|
| `tables.md` | Delta Lake table structure standards (primary keys, foreign keys, partitioning, DDL) |
| `sql_standards.md` | SQL writing conventions (identifiers, indentation, alignment, ANSI) |
| `transformation.md` | Data transformation job standards (idempotency, scheduling, lineage, parameters) |
| `spark_standards.md` | PySpark coding conventions |
| `python_standards.md` | Python writing conventions |
| `lineage_standards.md` | Lineage framework usage guide (constant definitions, event recording) |
| `databricks_standards.md` | Databricks standards (compute type selection, Airflow operators) |
| `databricks_apps.md` | Databricks Apps usage conventions |
| `vector_search.md` | Vector Search standards (endpoints, indexes, code examples) |

### 2026-04-15 Additions

| File | RST Source | Content |
|---|---|---|
| `design.md` | `standards/design.rst` | Design standards (Canvas, data product design, templates, impact assessment) |
| `data_quality.md` | `standards/data_quality.rst` | Data quality framework (dimensions, check syntax, transform integration) |
| `local_dab_development.md` | `user_guides/development_process/local_dab_development.rst` | Local DAB development and testing process |

---

## Notes

- **Image paths**: After conversion, `![](./assets/xxx.svg)` paths are relative to the original RST file and may break in the new location. Fix paths manually or remove the image line if display is not needed.
- **`:ref:` cross-document links**: All `:ref:\`...\`` references degrade to plain text. If the target document has also been converted, you can manually replace them with relative Markdown links.
- **Multi-line table cells**: Multi-line content in RST simple tables is joined into a single line. Information is preserved but formatting is lossy. If the original had a bullet list inside a cell (e.g., enumerated values for `PROCESS_TYPE`), it will be flattened into space-separated text.
- **Python environment**: The script uses only the standard library and runs directly in any Python 3.8+ environment — no venv activation or package installation required.
