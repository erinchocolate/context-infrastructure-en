# Skill: PR Code Review Workflow

## Metadata

- **Type**: Workflow
- **Use Case**: AI-assisted code review for PRs/branches in the `data_platform` repository
- **Output Location**: `context-infrastructure/01 raw/YYYYMMDD_pr_review_<branch>.md`
- **Dependent Script**: `context-infrastructure/03 refined/tools/pr_review.sh`
- **Created**: 2026-04-14
- **Last Updated**: 2026-04-14

---

## Trigger Phrases

Activate this skill when the user says any of the following:

- "Help me review this PR"
- "Review the `<branch_name>` branch"
- "My colleague made some changes to XXX, can you take a look?"
- "code review", "PR review"

---

## Core Principles

1. **Analyze first, ask second**: Automatically analyze code changes before asking the user whether they have project documentation to supplement the review — don't ask the user to provide everything upfront.
2. **Guidelines-driven**: All review comments must cite a guideline as their basis; never make suggestions without backing.
3. **Tiered severity**: Issues are classified as Critical / Major / Minor so users can quickly prioritize.
4. **Actionable, not preachy**: Every issue must include a concrete suggestion for how to fix it, not just point out the problem.

---

## Workflow

### Phase 1: Pull the Diff

**After confirming the branch name with the user, run:**

```bash
bash "/opt/processes/mc_platform/context-infrastructure/03 refined/tools/pr_review.sh" \
    --branch <branch_name> \
    [--base master] \
    [--repo /opt/processes/data_platform]
```

Extract from the script output:
- List of changed files and their types
- Commit summary (to understand the intent of the changes)
- Full diff (for analysis in later phases)

If the script errors (branch not found), prompt the user to check the branch name and list any candidate branches returned by the script.

---

### Phase 2: Auto-Match Guidelines

Based on the types and paths of the changed files, **automatically** determine which guidelines to reference.

**File type → Guidelines mapping:**

| Condition | Reference File |
|-----------|---------------|
| Contains `.py` files | `projects/guidelines/python_standards.md` |
| Contains `.sql` files | `projects/guidelines/sql_standards.md` |
| Contains Databricks bundle/DAB config (`.yml`) or notebooks | `projects/guidelines/databricks_standards.md` |
| Changes involve Delta tables, schema, `CREATE TABLE`, `LOCATION` | `projects/guidelines/tables.md` |
| Changes involve transformation pipelines or ETL processes | `projects/guidelines/transformation.md` |
| Changes involve lineage framework calls | `projects/guidelines/lineage_standards.md` |
| Changes involve vector search, embeddings, or chunking | `projects/guidelines/vector_search.md` |
| Changes involve Databricks Apps | `projects/guidelines/databricks_apps.md` |
| Changes involve Spark code (`spark.`, `DataFrame`, `pyspark`) | `projects/guidelines/spark_standards.md` |

**All guidelines file path prefix:**
`/opt/processes/mc_platform/context-infrastructure/projects/guidelines/`

List the matched guidelines and read their contents (keep in context for later use).

---

### Phase 3: Ask for Project Documentation

Show the user a brief summary of the code changes (1–2 sentences describing the topic), then ask:

> The changes above involve **[change topic]**.
>
> If there are relevant requirement, plan, or design documents under `context-infrastructure/projects/`, please provide the path. If not, feel free to skip this step.

If the user provides a path (e.g., `projects/my_project/01 raw/chunking_design.md`), read those documents and include an additional analysis dimension in Phase 4.

---

### Phase 4: Parallel Review

**Assess whether parallelization is worthwhile:**
- If the changes are small (< 50 lines / single simple file), analyze serially — no need for parallelization.
- If the changes are larger (multiple files, multiple modules), launch parallel sub-agents.

**Parallel split (code tasks, overlap ≤ 20%):**

**Sub-agent A — Code Quality & Correctness**
Analyze:
- Logical correctness (algorithms, edge cases, data type handling)
- Error handling: are exceptional cases handled?
- Performance: any obviously inefficient operations (e.g., full table scans inside loops)?
- Readability: naming, function decomposition, comments
- Security: injection risks, sensitive data exposure, etc. (OWASP Top 10)
- Test coverage: are there unit tests, and do they cover the critical paths?

**Sub-agent B — Guidelines Compliance Review**
Analyze:
- Check each matched guideline item by item
- Compliance status per guideline: ✅ Compliant / ⚠️ Partially Compliant / ❌ Non-compliant
- Provide specific remediation suggestions for ⚠️ and ❌ items

**Sub-agent C (only if the user provided project documentation) — Requirements Alignment**
Analyze:
- Does the implementation match what is described in the requirement/design documents?
- Which requirements are not covered?
- Where does the implementation diverge from the design?

---

### Phase 5: Generate the Review Report

Consolidate results from Phase 4 into a final Markdown report and save it.

**Report file path:**
```
/opt/processes/mc_platform/context-infrastructure/01 raw/<YYYYMMDD>_pr_review_<branch_safe_name>.md
```
(`branch_safe_name` = replace `/` with `_`, e.g., `ann/cdringest` → `ann_cdringest`)

---

## Report Template

```markdown
# PR Review: `<branch_name>`

| Field | Value |
|-------|-------|
| Branch | `<branch_name>` |
| Base | `master` |
| Review Date | YYYY-MM-DD |
| Reviewer | AI (GitHub Copilot) |
| Guidelines Referenced | python_standards, tables (list actual matches) |
| Project Docs | `projects/xxx/01 raw/xxx.md` (if any) / None |

---

## Change Summary

<!-- 2–4 sentences describing what this PR does, the size of the changes, and which modules are affected -->

## Changed Files

| Status | File |
|--------|------|
| M | `path/to/file.py` |
| A | `path/to/new_file.py` |

---

## Code Quality

### 🔴 Critical (Must Fix)

<!-- Issues affecting correctness, security, or data integrity -->

- **[filename:line]** Issue description
  - **Suggestion**: Specific fix

### 🟡 Major (Should Fix)

<!-- Performance issues, design decisions that violate guidelines -->

- **[filename:line]** Issue description
  - **Suggestion**: Specific fix

### 🟢 Minor (Optional Improvement)

<!-- Readability, naming, comments, etc. -->

- **[filename:line]** Issue description
  - **Suggestion**: Specific fix

---

## Guidelines Compliance

### `python_standards.md`

| # | Guideline | Status | Notes |
|---|-----------|--------|-------|
| 1 | PEP8 formatting | ✅ | - |
| 2 | Google docstring format | ❌ | `chunk()` function is missing a docstring |

<!-- Expand per matched guidelines file, one section each -->

---

## Requirements Alignment

<!-- Only include this section if the user provided project documentation in Phase 3 -->

| Requirement | Status | Notes |
|-------------|--------|-------|
| Support paragraph-level splitting | ✅ | Implemented |
| Support overlapping windows (overlap) | ⚠️ | Logic exists but overlap size has no boundary check |
| Max chunk size configurable | ❌ | Hardcoded as 512; not read from config |

---

## Overall Recommendations

<!-- 3–5 high-level recommendations to help the author quickly understand the most important improvements -->

1. ...
2. ...

---

## Conclusion

<!-- One sentence: Approve / Approve with minor comments / Request changes -->

> **Recommendation**: Request changes — resolve X Critical issue(s) before merging
```

---

## Usage Example

**User**: Help me review the `ann/cdringest` branch.

**Agent actions**:
1. Run `pr_review.sh --branch ann/cdringest`
2. Parse output — changes include `.py` and `.sql` files
3. Auto-load `python_standards.md` and `sql_standards.md`
4. Ask the user: "This PR involves changes to the CDR ingest pipeline, including X Python files and Y SQL files. Do you have any related requirement or design documents?"
5. User replies: "Yes, at `projects/cdr_ingest/01 raw/design.md`"
6. Read that document, then launch 3 parallel sub-agents
7. Merge results, generate the report, save to `01 raw/20260414_pr_review_ann_cdringest.md`
