---
id: axiom_results_certainty_2026
category: tech_decisions
created: 2026-02-23
updated: 2026-02-23
---

# T1. Result Certainty Over Process Certainty

## 1. Core Axiom

First define what counts as `correct` and verify it; don't try to make AI reliable by micromanaging every step.

## 2. Deep Reasoning

### 2.1 The Ceiling of Process Certainty

Traditional programming confidence comes from process certainty: every line of code is under your control, every branch and every edge case has been designed by you. This certainty is tangible, and it is the core ability we have trained over many years — translating outcomes into program behavior. But this pattern hits a fundamental wall in AI systems.

When you try to constrain AI behavior through rules, you find yourself trapped in an infinite defensive programming loop. One rule fixes one problem, but introduces a new problem in other situations. You add more rules to handle edge cases, but edge cases are infinite. Eventually, you discover that you are maintaining more rules than product logic. This is precisely the predicament I encountered in an AI translation project: chunking, retrying, glossaries, checkpoint resumption, Chinese character detection, timeout handling — each one was a defense against a specific failure mode. But these defensive rules became the primary source of system complexity, and could never cover all situations.

The ceiling of process certainty is determined by how many edge cases you can think of. In AI systems, edge cases are infinite, because AI's behavior is inherently non-deterministic. You can never fully constrain it through rules.

### 2.2 The Closed Loop of Result Certainty

Result certainty represents a completely different approach: rather than prescribing the process, define a clear target state and let the system find its own way to get there. The key to this approach is establishing a closed loop: execute → observe → verify → correct.

When I handed the translation task to Claude Code, this closed loop finally became truly possible. Claude Code's fundamental unit of operation is the file, which is stateful and persistent. This means AI can see what it did before, can run verification scripts to check results, and can make adjustments based on feedback. This is not a one-shot API call — it is an iterative, self-correcting process.

Specifically, when I define the criteria for "translation complete" — correct formatting, no residual Chinese characters, consistent terminology — I can encode these criteria as executable checks. AI not only has to complete the translation, but also has to run these checks, see the failure messages, and fix the problems itself. This process can repeat until all checks pass. The key transformation is: I no longer need to foresee all possible failure modes — I only need to define what success looks like.

This principle also has deep implications for cost structure. In traditional programming, code execution is nearly free, but human labor costs are high, so we invest enormous effort in designing perfect logic. But in the AI era, inference costs are rapidly falling. The cost of multiple attempts, checks, and corrections is often lower than writing defensive rules for every long-tail failure mode. This is a fundamental economic shift.

### 2.3 Making Acceptance Criteria Explicit

Result certainty requires the ability to clearly define "done." This sounds simple, but it is in fact the greatest bottleneck. Most failures are not because AI isn't smart enough, but because AI doesn't know what "done" means.

I use an analogy to understand this: imagine assigning a task to an amnesiac intern. This intern has no background knowledge, doesn't know what you discussed before, doesn't know your implicit expectations. They can only see the instructions you give them this one time. If you want them to reliably complete the task, you must write the acceptance criteria with extreme clarity — clear enough that they can judge whether they've finished based on those criteria. If they believe they haven't finished, they know what's missing.

This is exactly how Claude Code works. When I say "translate this file, then run this Python script to check for residual Chinese characters, and fix any that are found," I am in fact transforming implicit expectations into explicit, verifiable criteria. This transformation itself is the greatest leverage.

### 2.4 Architecture Over Rules

When a system is performing poorly, our first instinct is often "the model isn't good enough" or "we need more rules." But in practice, many failures stem from poor architectural design. The Wide Research example is instructive: rather than requiring a single AI call to perfectly execute a complex task, break the task into multiple smaller steps, each with clear acceptance criteria. This is not model magic — it is a management fix.

The same principle applies to translation. When API calls "slacked off" on long texts, I once thought it was a model problem. But in reality, it was an architectural problem: long outputs degrade instruction-following ability. The solution is not to ask the model to "be smarter," but to change the architecture — have AI translate chapter by chapter, with each chapter having clear inputs and outputs, and each chapter independently verifiable. The problem then shifts from "how do I make a single API call execute perfectly" to "how do I design a process where each small step is reliable."

## 3. Application Criteria

### When to Use

Result certainty applies to any task whose output can be checked. This includes:

- **Formatting tasks**: code generation, document conversion, data cleaning — all of these have clear success criteria
- **Validation tasks**: checking whether specific conditions are met (no residual Chinese characters, passing tests, conforming to specifications)
- **When guardrail rules start to outnumber product logic**: this is a signal that you should switch to result certainty

### How to Practice

1. **Write acceptance criteria first**: Don't say "generate high-quality code" — say "code must pass all unit tests, coverage > 80%, no security warnings." Turn implicit expectations into explicit, measurable criteria.

2. **Where possible, solidify criteria into executable checks**: Python scripts, unit tests, linters, regular expressions — anything that can be automatically verified should be automated. This way AI can run the checks itself, see the failures, and fix them.

3. **Let the agent choose its own method and iterate**: Don't prescribe how AI should do it — only define what success is. AI may use regex checking, or NLP, or some other method. As long as the final result meets the criteria, it is reliable.

4. **Establish feedback loops**: Ensure AI can see the results of validation and make adjustments based on failure messages. This closed loop is the core of result certainty.

## 4. Pitfalls and Boundaries

### When Not to Apply

- **Acceptance criteria cannot be defined**: If success is inherently subjective (e.g., "creative writing"), result certainty is difficult
- **Extremely high real-time requirements**: If the validation process causes unacceptable delays, it may be necessary to accept a higher level of risk
- **Cost-benefit mismatch**: If the cost of validation far exceeds the cost of failure, the investment may not be worthwhile

### Common Pitfalls

1. **False acceptance criteria**: Defining criteria that appear clear but are actually vague. For example, "good code quality" is not a criterion; "passes all tests and complexity < 10" is.

2. **Validation blindness**: The validation rules themselves have defects, so output that passes validation still fails. Validation rules need to be periodically reviewed to ensure they're truly measuring what you care about.

3. **Over-validation**: Designing overly complex validation processes for low-risk tasks, causing efficiency to decline. Validation should be matched to the level of risk.

4. **Trust drift**: Over time, gradually relaxing validation standards until the system becomes unreliable. Regular review and recalibration are needed.

## 5. Relationship to Other Axioms

- **A04 Reliability Is a Management Problem**: Result certainty is the core method of reliability management
- **V02 Verifiability Is the Foundation of Trust**: Result certainty depends on clear acceptance criteria and executable checks
- **T07 The Isolate-Process-Verify Closed Loop**: Result certainty is the verification phase of this closed loop
- **T01 Infrastructure Over Components**: Result certainty requires a runtime that supports feedback loops (such as Claude Code)
