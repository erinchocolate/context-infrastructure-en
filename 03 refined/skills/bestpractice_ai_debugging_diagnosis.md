# AI-Assisted Debugging Diagnosis

## Metadata

- **Type**: BestPractice
- **Applicable Scenarios**: Situations where "AI can't fix the code" in AI-assisted development
- **Creation Date**: 2026-02-21
- **Source**: Observation records from 2026-01-19

---

## Core Insight

**In the vast majority of cases where "AI can't fix the code," the root cause is a human user problem, not a system architecture problem.**

Common misconceptions:
- "The codebase is a mess, AI can't handle it" → Actually insufficient context
- "AI isn't smart enough" → Actually unclear instructions
- "Needs refactoring" → Actually lacking success criteria

---

## Diagnostic Decision Tree

```
AI can't fix the code
    │
    ├─→ Was sufficient context provided?
    │       │
    │       └─→ No → Add context (relevant files, error logs, expected behavior)
    │       │
    │       └─→ Yes → Continue
    │
    ├─→ Were clear success criteria defined?
    │       │
    │       └─→ No → Clarify "what is good" (not just "it runs")
    │       │
    │       └─→ Yes → Continue
    │
    ├─→ Was a feedback channel provided?
    │       │
    │       └─→ No → Let AI see results (test output, screenshots, logs)
    │       │
    │       └─→ Yes → Continue
    │
    └─→ May be a genuine architecture problem
            │
            └─→ Consider partial refactoring or problem decomposition
```

---

## Common Problems and Solutions

### 1. Insufficient Context

Symptoms:
- AI's proposed solution deviates from actual requirements
- The same piece of code is revised repeatedly
- Non-existent dependencies or functions are introduced

Solutions:
- Provide relevant files (not just the one with the error)
- Provide a project structure overview
- Provide a similar correct implementation as reference

### 2. Vague Success Criteria

Symptoms:
- AI asks "is this okay?" and the human says "make more changes"
- Still unsatisfied after multiple rounds of revision, but can't articulate the specific problem

Solutions:
- Specify quantitative metrics (performance, coverage, error types)
- Provide expected output examples
- Break down into smaller, verifiable steps

### 3. Missing Feedback Channel

Symptoms:
- Don't know whether AI's modifications worked
- Humans need to manually test to discover problems

Solutions:
- Provide test commands and expected output
- Let AI execute and view results
- Provide screenshots when dealing with UI

---

## When It Is Actually an Architecture Problem

Signals that genuine refactoring is needed:
- The same problem recurs in different places
- Still unresolved after adding context
- Multiple AI-proposed solutions all have obvious defects
- The problem crosses multiple module boundaries

Even then, first try:
- Partial refactoring rather than large-scale rewriting
- Increasing test coverage
- Improving documentation and comments

---

## Relationship to Other Skills

- Works with the "70% problem" diagnosis in `bestpractice_ai_programming_mindset.md`
- Works with the Todo task management mechanism in system prompts for task decomposition

## Change Log

| Date | Change |
|------|--------|
| 2026-02-21 | Initial version, from 2026-01-19 observation records |
