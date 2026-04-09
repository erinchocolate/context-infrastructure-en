---
id: axiom_context_isolation_2026
category: tech_decisions
created: 2026-02-23
updated: 2026-02-23
---

# T2. Context Isolation: The Source of Multi-Agent Value

## 1. Core Axiom

The leverage of multi-agent systems comes from information domain isolation (each with its own independent context + a shared scratchpad), not from mimicking organizational hierarchies. The purpose of isolation is not division of labor — it is to enable each Agent to make better decisions within a clean information environment.

## 2. Deep Reasoning

### Cognitive Load and Context Competition

The fundamental reason Cursor falls into loops (re-introducing Bug A while fixing Bug B) is that planning and execution details compete for attention within the same context window. When a single model carries both high-level planning and low-level implementation simultaneously, it must first filter through a pile of mixed information for the parts actually relevant to planning before it can make a decision. This places an enormous cognitive burden on the model. The reverse also holds: if the model dives directly into execution, it easily loses track of what the planner said among the flood of execution details, or loses focus entirely. The result is that neither planning nor execution is done well — a lose-lose situation. This is not a failure of model capability; it is a failure of information architecture — mixing together things that should not be mixed.

Splitting the Planner and the Executor immediately reduces cognitive load and error rates, even without switching to a stronger model. The Planner can focus on global decision-making, verification, and reflection; the Executor can concentrate on low-level implementation and debugging. This simple layering allows each role to work within a relatively clean information environment and make better decisions. The key is: isolation is not to mimic organizational structure — it is to make information flow manageable.

### Persistent State and the Problem of Amnesia

But simply splitting roles is not enough. If the Planner and Executor still communicate through conversation, they face a fatal problem: as soon as the context window grows long or is truncated, the Planner's instructions are completely lost. For example, if the Planner earlier says "remember to run a version-compatibility test," then after several rounds of debugging by the Executor, Cursor truncates the context window — that instruction simply disappears. Because it is no longer in the Executor's context window, the Executor will have no memory of it the next time it executes. This is like a company where management and the execution team are both swamped, grinding away, and no one bothers to write documentation because it seems minor. The result is that the execution team has no way to track progress and relies entirely on being reminded by the manager. The manager can't remember the technical details either, and ends up asking the same questions every day.

The solution is to mandate the use of a shared Scratchpad document. Any analytical reasoning, test results, bugs encountered, and final discussion conclusions are all written into this file. This way, the Planner can check the document at any time for current difficulties and progress, and can leave new task instructions; the Executor updates the document with results and feedback after completing a feature or hitting a problem, so the Planner reads it and won't forget. By converting the conversation pipeline into a persistent notebook, we largely solve the problem of LLM context loss. Even if the conversation is refreshed temporarily, simply re-referencing the document is enough. The probability of amnesia and falling into the same trap is immediately reduced significantly. This is not merely an engineering trick — it transforms the fragility of chat into a durable state machine.

### Over-Engineering and the Necessity of Constraints

A stronger Planner (such as o1) brings deeper thinking, but also raises the risk of over-engineering. An experienced senior engineer validates on small-scale data first, then deploys to large-scale data — this saves a lot of debugging time. But an unconstrained Planner will often go straight to debugging on the final large-scale data, or design a small program into a Concurrent Large-Scale Platform, making the process extremely bloated. This is like bringing in a famous consulting firm for your human team: these consultants, in an effort to demonstrate their sophistication, often produce solutions that are especially elaborate, large, and bloated. The people below toil away, but none of it actually serves the final business goal or necessarily improves efficiency.

Therefore, isolation must be paired with constraints and explicit validation. Use prompting to give the Planner a Founder Mindset — don't always try to build the industry's most impressive entire platform all at once; instead, have a Bias for Action and seize opportunities as they arise. Start with a simple prototype, and only after validating feasibility add more features step by step. In particular, when the Planner assigns tasks to the Executor, it should clearly state the necessity and validation method for each decomposed step. At the same time, let the Executor also be able to raise questions in the document's feedback section: if the Executor thinks a plan is too complex, it can challenge the Planner to reconsider whether it's truly necessary, or to decompose it further. Use this interactive and acceptance mechanism to govern the Planner's reasoning.

### Cross-Validation and Abstract Thinking

Only when context stays clean can a multi-agent system do true cross-validation and abstract thinking, rather than being drowned in each other's noise. A clean Planner context means it can see the full history of decisions and validation results, rather than being overwhelmed by execution details. A clean Executor context means it can focus on the current task, rather than being distracted by past planning discussions. This isolation allows both agents to make high-quality decisions within their respective information domains, then coordinate effectively through the shared Scratchpad. The result is a system that can both make well-considered plans and execute with precision — rather than compromising both.

## 3. Application Criteria

**When to use**:
- Tasks that simultaneously require macro-level planning and low-level editing/debugging
- When agents start looping or regressing due to context overload
- Long-duration tasks that span multiple context window truncations
- When the failure modes of planning and execution differ (planning failures are directional errors, execution failures are detail errors)

**How to practice**:
1. Define roles by information domain (Planner, Executor, optional Evaluator), not by organizational structure
2. Provide each role with an independent context; clearly specify what information each should see
3. Mandate the use of a shared scratchpad to record goals, decisions, test results, and next actions
4. Design clear handoff artifacts: the Planner outputs validation criteria and decomposition plans; the Executor outputs execution results and feedback
5. Perform explicit acceptance checks in the scratchpad at regular intervals, rather than relying on implicit understanding

## 4. Pitfalls

**Pitfall 1: Isolation becomes an island**. If the Planner and Executor contexts are completely isolated but there is no effective communication mechanism, they become two independent systems each doing their own thing. The scratchpad must be alive and regularly updated — not a dead document.

**Pitfall 2: Over-designing handoff artifacts**. Trying to guarantee perfect communication through complex handoff protocols actually increases system complexity. The best handoff artifacts are simple, verifiable, and human-readable.

**Pitfall 3: Isolation becomes an excuse to dodge responsibility**. The Executor cannot use "that's not in my context" as an excuse to ignore obvious problems. Isolation is for improving efficiency, not for shirking responsibility.

**Pitfall 4: Ignoring the cost of isolation**. The coordination overhead of a multi-agent system is real. Only when the task's complexity is sufficiently high, or when a single agent's context truly becomes a bottleneck, do the benefits of isolation outweigh the costs.

## 5. Related Axioms

- **T2 Result Certainty Over Process Certainty**: The purpose of isolation is to allow each Agent to better verify its own output, rather than trying to guarantee correctness through micromanagement.
- **T5 Cognition Is an Asset, Code Is a Commodity**: Isolation allows the Planner to focus on capturing cognition (understanding, validation criteria, decision rationale) rather than being overwhelmed by execution details.
- **T6 Dependency Topology Over Task Count**: The granularity of isolation should be determined by information dependencies, not by arbitrarily splitting tasks.
- **T7 The Isolate-Process-Verify Closed Loop**: Context isolation is the foundation of this closed loop: the Planner isolates to collect facts and make plans; the Executor isolates to process; the shared Scratchpad is the interface for verification.
