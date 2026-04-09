# Staged Approach

## Metadata

- **Type**: BestPractice
- **Applicable Scenarios**: AI-assisted automation, batch processing, destructive operations
- **Creation Date**: 2026-02-21
- **Source**: Observation records from 2026-01-07

---

## Core Framework

Break complex automation tasks into three stages:

```
Stage 1: Data Collection → Stage 2: Batch Processing → Stage 3: Confirmation and Release
```

### Stage 1: Data Collection

- Fully pull source data to local
- Isolated from online systems
- Data persisted to disk before moving to the next stage
- Goal: Ensure subsequent processing has a stable data foundation

### Stage 2: Batch Processing

- Call AI in local environment
- Fully isolated from online systems
- Repeatable, rollback-capable
- Goal: Complete AI non-deterministic operations in a safe sandbox

### Stage 3: Confirmation and Release

- Human review of processing results
- One-click publish or batch apply
- Record change log
- Goal: Human oversight as the final line of defense

---

## Core Principles

### Isolate-Process-Verify Closed Loop

```
Online Environment ←→ Local Sandbox ←→ Human Confirmation
       ↓                    ↓                  ↓
    Read-only           AI Operations      Release Decision
```

### Dry Run First

**Any destructive operation must first be Dry Run.**

Destructive operations include:
- File overwrite/deletion
- Database writes
- API POST/PUT/DELETE
- Email/message sending
- Any irreversible operation

Dry Run checklist:
- [ ] Confirm scope of operation (which files/records are affected)
- [ ] Confirm operation content (what exactly changes)
- [ ] Confirm rollback capability (backup or version control exists)
- [ ] Confirm execution environment (not production environment)

---

## Typical Application Scenarios

### Content Translation and Publishing

1. Stage 1: Pull content to be translated to local
2. Stage 2: Call AI for batch translation, generate preview
3. Stage 3: Human review, then one-click publish

### Data Processing Pipeline

1. Stage 1: Export source data (CSV/JSON)
2. Stage 2: AI processing + validation
3. Stage 3: Import to target system after confirmation

### Batch Code Modifications

1. Stage 1: Create independent branch
2. Stage 2: AI executes modifications + local testing
3. Stage 3: Merge after review

---

## Relationship to Other Skills

- Works with the "outcome certainty" principle in `bestpractice_ai_programming_mindset.md`
- Works with the parallel processing in `workflow_parallel_subagents.md`
- Works with the verification mechanism in `bestpractice_temporal_info_verification.md`

## Change Log

| Date | Change |
|------|--------|
| 2026-02-21 | Initial version, from 2026-01-07 observation records |
