# Parallel Subagent Workflow

## Metadata

- **Type**: Workflow
- **Applicable Scenarios**: Calling background agents, executing multiple independent sub-tasks in parallel
- **Creation Date**: 2026-02-20
- **Last Updated**: 2026-03-01

---

## When to Use Parallel Mode

Parallel mode is only worthwhile when all of the following conditions are met:

1. **Task is splittable**: Can be decomposed into at least 2 relatively independent sub-tasks
2. **Sub-tasks have scale**: Each sub-task is expected to require ≥5 tool calls to complete
3. **Sub-tasks have value**: Parallel execution saves significantly more time than serial execution

When these conditions are not met, execute serially — don't parallelize for the sake of parallelizing.

---

## Parallel Execution Process

### 1. Evaluate and Split

After identifying 3-5 key dimensions, determine overlap based on task type:

| Task Type | Overlap Range | Reason |
|-----------|--------------|--------|
| Research/Creative tasks | 30% - 50% | Cross-validation, gap-filling |
| Code/Execution tasks | 0% - 20% | Efficiency first, reduce duplication |

### 2. Launch in Parallel

Issue all calls in the same message. Use `mcp_task()` to select category or subagent_type based on task type:

```python
# Research/analysis tasks → use subagent_type
mcp_task(
    subagent_type="explore",
    run_in_background=True,
    prompt="specific dimension description..."
)

# Implementation tasks → use category delegation
mcp_task(
    category="deep",
    load_skills=["git-master"],
    run_in_background=True,
    prompt="specific implementation requirements..."
)
```

Each subagent's prompt should include:
- The specific dimension/scope they are responsible for
- Expected overlap areas (let the agent know others are also looking at this part)
- Output format requirements

### 3. Wait and Integrate

After launching, do nothing — wait for system notification. The system will automatically push a `<system-reminder>` notification when a subagent completes. After receiving the notification, use `mcp_background_output(task_id="...")` to retrieve results, then cross-validate information in overlapping areas and synthesize final output.

**⚠️ Common Misconceptions About `background_output`:**

The `block` and `timeout` parameters of `background_output` **do not** cause the call to block waiting for task completion. Regardless of whether you set `timeout=120` or `timeout=600`, it **immediately returns whatever output currently exists**. This means:

- **Wrong approach**: Repeatedly calling `background_output(block=true, timeout=600)` trying to "wait" for task completion — each call will immediately return the same partial result, causing meaningless polling.
- **Correct approach**: After issuing a background task, **end your current response**, wait for the system-pushed `<system-reminder>` notification, then call `background_output` once to retrieve the complete result.

In short: `background_output` is a tool for **retrieving results**, not for **waiting for results**. Waiting is handled by the system notification mechanism.

---

## Examples

### Research Task (30-50% overlap)

```
Research "adoption status of a technology framework"
├─ Agent 1 (explore): Core features + community activity
├─ Agent 2 (librarian): Community activity + enterprise cases
├─ Agent 3 (oracle): Enterprise cases + competitor comparison
└─ Overlap: Community and enterprise cases both covered, enables cross-validation
```

### Code Task (0-20% overlap)

```
Implement "user authentication system"
├─ Task 1: Core authentication logic + Token management
├─ Task 2: Database models + migration scripts
├─ Task 3: API endpoints + test cases
└─ Overlap: Small overlap at interface definitions, ensure correct integration
```

---

## Notes

- **Don't over-parallelize**: 2-3 carefully designed subagents usually beat 5 loosely defined ones
- **Prompt quality**: Subagent prompts must be specific enough, otherwise results will be shallow
- **Cost awareness**: Parallelism consumes more tokens — evaluate whether it is worthwhile
- **Intermediate results**: Usually do not need to be saved; integrate only in the main agent
