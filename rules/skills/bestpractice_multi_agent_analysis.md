# Multi-Agent Parallel Analysis Best Practices

## Metadata

- **Type**: BestPractice
- **Applicable Scenarios**: Document analysis, research tasks, complex information integration
- **Creation Date**: 2026-02-21
- **Source**: 2026-02-16 "4+4" Multi-Agent Document Analysis Experiment

---

## Experiment Background

Parallel analysis of real estate research documents using a "4 comprehensive + 4 specialized + 1 cross-validation" 9-agent architecture.

Final output: 11 analysis JSONs (4108 lines) and a visualization website.

---

## Core Findings
### The True Value of Multi-Agent: Context Window Isolation

The true value of multi-agent frameworks is not role-playing (PM/Dev/QA division of labor), but **context window isolation**.

- The management agent does not need to know low-level details like syntax errors — only high-level planning
- Each agent focuses on its own abstraction level, reducing information overload
- Blindly imitating human collaboration patterns (e.g., mechanical PM/Dev/QA division) is incorrect AI-native design

### Topic Splitting with 50% Overlap

Don't completely partition tasks — let adjacent agents have 50% overlap in responsibilities.

Reasons:
- Overlap areas are most likely to be missed
- Overlap allows cross-validation
- Different agents may discover different angles on the same content

### Cross-Validation Discovers Inconsistencies

Key inconsistencies discovered in the experiment:
- Contradictory feasibility assessment of garage conversion (Agent A considered feasible, Agent B pointed out regulatory restrictions)
- Discrepancies in interpretation of the 750 square foot threshold across different documents

Inconsistencies are not bugs — they are features. They expose contradictions and ambiguities in the information.

### Specialized Agents More Easily Discover Cross-Dimensional Insights

Specialized agents more easily discover than comprehensive agents:
- Patterns across documents
- Numerical thresholds (such as 750 square feet)
- Hidden constraints

---

## Recommended Architecture

### Small Tasks (≤3 documents)

```
2-3 comprehensive agents (50% overlap)
```

### Medium Tasks (3-10 documents)

```
3-4 comprehensive agents + 2-3 specialized agents
```

### Large Tasks (>10 documents)

```
4 comprehensive agents + 4 specialized agents + 1 cross-validation agent
```

### Agent Division Example

| Type | Count | Responsibility |
|------|-------|----------------|
| Comprehensive | 4 | Each covers the full document set, 50% overlap |
| Specialized | 4 | Focus on: Finance / Regulations / Technical / Market respectively |
| Cross-validation | 1 | Compare outputs from the first 8 agents, flag inconsistencies |

---

## Output Format

Recommended structured JSON:

```json
{
  "agent_id": "comprehensive_1",
  "scope": ["doc1.md", "doc2.md", "doc3.md"],
  "findings": [
    {
      "topic": "topic",
      "summary": "summary",
      "evidence": "quoted original text",
      "confidence": "high/medium/low"
    }
  ],
  "cross_refs": ["related to finding X of comprehensive_2"]
}
```

---

## Relationship to Other Skills

This bestpractice is a **case study and extension** of [Parallel Subagent Workflow](./workflow_parallel_subagents.md): the workflow defines when to use it, core parameters, and execution process; this document provides the methodological summary and output format from the "4+4" experiment.

- Works with the parallel execution framework in `workflow_parallel_subagents.md`
- Works with the research workflow in `workflow_deep_research_survey.md`
- Output can be used for Stage 2 processing in `bestpractice_staged_approach.md`

## Change Log
| Date | Change |
|------|--------|
| 2026-02-22 | Added core finding: context window isolation is the true value of multi-agent |
| 2026-02-21 | Initial version, from 2026-02-16 experiment summary |
