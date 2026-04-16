#!/usr/bin/env bash
# =============================================================================
# pr_review.sh — Pull Request diff extractor for AI code review
#
# Usage:
#   bash pr_review.sh --branch <branch_name> [OPTIONS]
#
# Options:
#   --branch  <name>    (required) The feature/PR branch to review
#   --base    <name>    (optional) Base branch to diff against. Default: master
#   --repo    <path>    (optional) Path to the git repo. Default: /opt/processes/data_platform
#   --output  <path>    (optional) Write output to file instead of stdout
#
# Examples:
#   bash pr_review.sh --branch ann/cdringest
#   bash pr_review.sh --branch GT/xy-acquire_pi_summary-sprint68 --base master
#   bash pr_review.sh --branch my-feature --output /tmp/pr_diff.txt
# =============================================================================

set -euo pipefail

# ---------- defaults ----------
BRANCH=""
BASE="master"
REPO="/opt/processes/data_platform"
OUTPUT=""

# ---------- parse args ----------
while [[ $# -gt 0 ]]; do
    case "$1" in
        --branch)  BRANCH="$2";  shift 2 ;;
        --base)    BASE="$2";    shift 2 ;;
        --repo)    REPO="$2";    shift 2 ;;
        --output)  OUTPUT="$2";  shift 2 ;;
        *) echo "Unknown argument: $1" >&2; exit 1 ;;
    esac
done

if [[ -z "$BRANCH" ]]; then
    echo "Error: --branch is required." >&2
    echo "Usage: bash pr_review.sh --branch <branch_name> [--base master] [--repo /path/to/repo]" >&2
    exit 1
fi

if [[ ! -d "$REPO/.git" ]]; then
    echo "Error: '$REPO' is not a git repository." >&2
    exit 1
fi

# ---------- helper: write to file or stdout ----------
write_output() {
    if [[ -n "$OUTPUT" ]]; then
        printf '%s\n' "$1" >> "$OUTPUT"
    else
        printf '%s\n' "$1"
    fi
}

# ---------- clear output file if specified ----------
if [[ -n "$OUTPUT" ]]; then
    > "$OUTPUT"
fi

cd "$REPO"

# ---------- fetch latest ----------
echo "Fetching latest from origin..." >&2
git fetch origin --quiet 2>&1 || {
    echo "Warning: git fetch failed. Using cached remote refs." >&2
}

# ---------- validate branches ----------
if ! git rev-parse --verify "origin/$BRANCH" &>/dev/null; then
    echo "Error: Branch 'origin/$BRANCH' not found. Check branch name." >&2
    echo "Available remote branches matching your input:" >&2
    git branch -r | grep -i "$(basename "$BRANCH")" || true
    exit 1
fi

if ! git rev-parse --verify "origin/$BASE" &>/dev/null; then
    echo "Error: Base branch 'origin/$BASE' not found." >&2
    exit 1
fi

# ---------- gather info ----------
REVIEW_DATE=$(date +"%Y-%m-%d %H:%M")
MERGE_BASE=$(git merge-base "origin/$BASE" "origin/$BRANCH")
COMMIT_COUNT=$(git rev-list "origin/$BASE..origin/$BRANCH" --count)

# ---------- section: header ----------
write_output "# PR Review Input — Branch: \`$BRANCH\`"
write_output ""
write_output "| Field | Value |"
write_output "|-------|-------|"
write_output "| Branch | \`$BRANCH\` |"
write_output "| Base | \`$BASE\` |"
write_output "| Repo | \`$REPO\` |"
write_output "| Date | $REVIEW_DATE |"
write_output "| Commits since base | $COMMIT_COUNT |"
write_output ""

# ---------- section: commit log ----------
write_output "## Commit Log"
write_output ""
write_output '```'
git log "origin/$BASE..origin/$BRANCH" --oneline --no-decorate
write_output '```'
write_output ""

# ---------- section: changed files ----------
write_output "## Changed Files"
write_output ""
write_output '```'
git diff "origin/$BASE...origin/$BRANCH" --name-status
write_output '```'
write_output ""

# ---------- section: file type summary ----------
write_output "## File Type Summary"
write_output ""
PY_COUNT=$(git diff "origin/$BASE...origin/$BRANCH" --name-only | grep -c '\.py$' || true)
SQL_COUNT=$(git diff "origin/$BASE...origin/$BRANCH" --name-only | grep -c '\.sql$' || true)
NB_COUNT=$(git diff "origin/$BASE...origin/$BRANCH" --name-only | grep -c '\.ipynb$' || true)
YAML_COUNT=$(git diff "origin/$BASE...origin/$BRANCH" --name-only | grep -c '\.ya\?ml$' || true)
JSON_COUNT=$(git diff "origin/$BASE...origin/$BRANCH" --name-only | grep -c '\.json$' || true)
OTHER_COUNT=$(git diff "origin/$BASE...origin/$BRANCH" --name-only | grep -vcE '\.(py|sql|ipynb|ya?ml|json)$' || true)

write_output "| Type | Count |"
write_output "|------|-------|"
[[ "$PY_COUNT"    -gt 0 ]] && write_output "| Python (.py) | $PY_COUNT |"
[[ "$SQL_COUNT"   -gt 0 ]] && write_output "| SQL (.sql) | $SQL_COUNT |"
[[ "$NB_COUNT"    -gt 0 ]] && write_output "| Notebooks (.ipynb) | $NB_COUNT |"
[[ "$YAML_COUNT"  -gt 0 ]] && write_output "| YAML | $YAML_COUNT |"
[[ "$JSON_COUNT"  -gt 0 ]] && write_output "| JSON | $JSON_COUNT |"
[[ "$OTHER_COUNT" -gt 0 ]] && write_output "| Other | $OTHER_COUNT |"
write_output ""

# ---------- section: full diff ----------
write_output "## Full Diff"
write_output ""
write_output '```diff'
git diff "origin/$BASE...origin/$BRANCH"
write_output '```'
write_output ""

echo "Done. Branch '$BRANCH' vs '$BASE': $COMMIT_COUNT commit(s) extracted." >&2
