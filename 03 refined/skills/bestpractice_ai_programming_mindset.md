# AI Programming Core Methodology

## Metadata

- **Type**: BestPractice
- **Applicable Scenarios**: AI-assisted programming, Agent system design
- **Creation Date**: 2026-02-21
- **Source**: Summary from multiple AI programming practices
- **Last Updated**: 2026-03-01

---

## Foundational Axioms (see axioms for details)

The methodology in this file is built on the following axioms, not repeated here:
- **T05**: Cognition is an asset, code is a consumable
- **T02**: Outcome certainty over process certainty
---

## Diagnosing and Solving the "70% Problem"

### The Nature of the Problem

The common "70% problem" in AI programming — AI can complete 70%, but the last 30% always has various issues — has a root cause in the **self-iteration feedback loop being broken**:

1. **AI cannot perceive whether its output meets expectations**: No "eyes" to see results
2. **Success criteria are too subjective**: Lacks a clear definition of "good," AI doesn't know which direction to iterate toward

### Solutions

1. **Open a perception channel for AI**:
   - Let AI see run results (screenshots, logs, test output)
   - Provide visual feedback when providing UI
   - Return complete output after executing commands

2. **Establish clear success criteria**:
   - Specify "what is good" (not just "it runs")
   - Quantitative metrics are better than subjective descriptions
   - Provide reference examples or expected output

---

## Reasoning Models and Agentic Workflows

### Complementary, Not Substitutes

- **Reasoning Model**: Excels at deep analysis, complex reasoning, planning
- **Agentic Workflow**: Excels at coordinating execution, tool calls, state management

### Limitations of Reasoning Models

A Reasoning Model's "reflection" is stateless — it cannot perceive changes in the external world. After thinking ends, the world has already changed.

### Recommended Architecture

Production environments use a **hybrid architecture**:
- Reasoning Model for deep analysis and planning
- Agentic Workflow for coordinated execution and state management
- External orchestration responsible for overall process control

---

## Limits of Cognitive Outsourcing

In an era of increasingly capable and increasingly affordable AI, it is important to clarify which tasks can be outsourced and which must be retained:

### Can Be Outsourced

- Gap-filling: information gathering, format organization
- Mechanical execution: repetitive coding, document generation
- Rapid prototyping: exploratory implementation

### Must Be Retained

- Forming your own opinions
- Defining problems and success criteria
- Value judgments in critical decisions
- Final review of output quality

---

## The Tipping Point: "Intuition" Over "Programs"

For complex semantic tasks, an LLM's "black-box intuition" may be more resilient and efficient than explicit logical code.

When tasks involve:
- Complex semantic understanding
- Multi-factor trade-offs
- Judgment with blurry boundaries

End-to-end LLM processing may be more robust than explicit rules. This is a paradigm shift from "program thinking" to "intuition thinking."

---

## File System as a Natural State Machine

The core design principle of the local Agent pattern:
- The file system itself is the most reliable state persistence layer
- State change = file operation, naturally auditable and rollback-capable
- Avoids the complexity of "in-memory state + manual persistence"

---

## Three Archetypes of Data Scientists in the AI Era

Skills are depreciating, but traits and character are becoming increasingly important. Three roles:

1. **Architect**: Define problems, design systems, orchestrate capability boundaries
2. **Auditor**: Evaluate quality, identify patterns, cross-validate
3. **Full-stack Builder**: End-to-end delivery, rapid prototyping, integration validation

Core insight: the same person can play different roles, but being clear about the current role avoids cognitive confusion.

## Notes

- **Productivity trap**: Sacrificing developer mental bandwidth and Flow state to save tiny Token costs is premature optimization
- **Physical anchor**: The ultimate safeguard for verifying complex logic is physical common sense (see `bestpractice_temporal_info_verification.md`)
- **Context rot**: Regularly reflect on and solidify methodology to prevent context loss between sessions

---

## Core AI Deployment Decisions

Distilled from "Using a Simple Task to Examine Key Decisions in AI Deployment":

### 1. Use a Local Coding Agent, Not ChatGPT

- Reduces context transfer and deployment friction
- Agent operates directly on the codebase, no copy-pasting
- ChatGPT is suitable for quick Q&A, not system development

### 2. Define Success Criteria Before Starting

- Build tests as feedback loops
- Clarify "what is good," not just "it runs"
- Tests are navigation signals for AI

### 3. Let the Agent Handle Corner Cases Itself

- Outcome certainty vs. process certainty
- Don't specify every step in detail — let AI decide the implementation path
- Focus on whether the output meets expectations, not whether the implementation process is "correct"

### 4. Divide and Conquer for Context Window Saturation

- 8 sub-agents working in parallel
- Each sub-agent has a single responsibility
- Aggregate at the end rather than stuffing all information in at once

### 5. Self-Bootstrapping and Results-Oriented Prompts

- Let AI iterate and improve on its own
- Don't prescribe every step
- Use 2 minutes to leverage 45 minutes of AI work — AI is leverage

---

**Last Updated**: 2026-03-01
