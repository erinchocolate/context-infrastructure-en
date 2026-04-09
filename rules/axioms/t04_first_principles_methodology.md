---
id: axiom_first_principles_methodology_2026
category: tech_decisions
created: 2026-02-23
updated: 2026-02-23
---

# T4. First-Principles Methodology Design

## 1. Core Axiom

Before adopting any framework, restate the problem from first principles (uncertainty, constraints, success criteria), and borrow only the components that directly serve it. A methodology is not a fixed set of rituals — it is a product designed for a specific user, a specific task, and a specific failure mode.

## 2. Deep Reasoning

### 2.1 The Hidden Cost of Frameworks: Worldview Lock-In

Complete frameworks are often a form of worldview lock-in. They quietly smuggle in assumptions about roles, phases, and artifacts — assumptions that may not match your domain. When you choose a framework, you are not merely choosing a set of tools; you are choosing the framework author's understanding of "the correct way to solve problems." This is especially dangerous when the domain's foundations have not yet solidified. Agentic AI is still evolving rapidly, and any mid-to-high-level abstraction is inherently fragile — the transformation from AutoGen v0.3 to v0.4 was essentially a complete rewrite, demonstrating that even mature frameworks may face fundamental rethinking. Locking in too early not only creates technical debt but also limits your ability to fully understand the domain. When you are bound by a framework's abstractions, you cannot see the underlying real mechanisms; when new understanding emerges, you have already invested too much to pivot easily.

### 2.2 The Mismatch Between Human Organizational Methods and AI Systems

Methods built to coordinate humans (rituals, role granularity, process certainty) may backfire when the bottleneck is AI reliability or scientific uncertainty. The BMAD-METHOD case is instructive: it rigidly transplanted human professional roles (Analyst, PM, Architect, Scrum Master, Developer, QA) into the AI world. But this assumption itself deserves scrutiny. The reason human society has professional differentiation is that we are inherently limited — no single person can master product, design, engineering, and testing simultaneously through more than a decade of education. But LLMs are different. A sufficiently powerful model can simultaneously understand business, design architecture, write code, and do testing. When you give it a prompt saying "you are a senior software engineer," you are actually constraining it, not empowering it. You are pulling an omniscient LLM down to the level of a limited human being who can only wear one hat.

The true value of multi-agent systems should come from context isolation, not role-playing. The boundaries between different agents should be drawn based on the coupling of the task itself, not based on the professional divisions of human society. The division between a planning agent and an execution agent exists because planning and execution have completely different context requirements — not because "PM and Developer are different job titles in human society."

### 2.3 Methodology as Product: A Design Perspective

I treat methodology as a product: it needs a user (me/the team), a job-to-be-done, and measurable failure modes. This perspective changes everything. The question is not "does this framework seem disciplined?" but "does this methodology help me solve my specific problem?" In the post-mortem of the FCW/TTC debate, backward-engineering management conflicted with modeling uncertainty; this taught me to choose methods based on uncertainty intervals, not based on whether they look "disciplined."

When uncertainty is high (e.g., exploratory research, early stages of a new domain), heavy processes become a burden. What you need is a fast feedback loop, flexible iteration, and minimal documentation. When uncertainty is low (e.g., a well-understood engineering task, clear requirements), structured processes gain value — they ensure no detail is missed and no detours are taken. A methodology that claims to work equally well for both situations has not truly understood the nature of the problem.

### 2.4 The Cost of Process Overload: Using a Sledgehammer for a Nail

BMAD's standard workflow is: market research → project brief → PRD → architecture document → user stories → development cycle → acceptance and release. This workflow is reasonable for medium-to-large projects requiring long-term maintenance. The problem is that not all software development requires such a process. The AI era has seen the emergence of vast amounts of "user-generated software" — software that may serve a single person, be used once, and then discarded. For example, a script that checks whether a website has new content each day, or a script that renames thirty videos according to some rule. Forcing such tasks through a full PRD → Architecture → User Stories workflow is using a sledgehammer for a nail.

The more fundamental problem is that BMAD treats the agile process as a fixed template rather than a set of principles that must be adapted to circumstances. True agility is at its core about responding quickly to change. But BMAD's design, to some extent, uses process certainty as a substitute for the flexibility of judgment. This has value in certain scenarios, but you must be clear about its costs.

### 2.5 Composability and Exit Ramps

The best methodologies are composable: they preserve exit ramps (when costs exceed benefits, we stop doing X). This means every part of a methodology should be optional and replaceable — not a tightly coupled whole. If you find that a certain step (such as detailed architecture documents) isn't helping your project, you should be able to skip it directly rather than being forced to follow the entire process.

The benefit of this design is that it allows you to adjust based on actual circumstances. You can start with a lightweight version, then gradually add more structure as the project grows in complexity. When a project's complexity decreases, you can also simplify the process. This flexibility is essential for surviving in a rapidly changing environment.

## 3. Application Criteria

### When to Use

Apply first-principles methodology design when evaluating popular AI development frameworks (e.g., agent role-playing workflows), choosing between research and engineering cadence, and standardizing team practices. Specific scenarios include:

- **Framework selection**: Before adopting BMAD, LangGraph, AutoGen, or similar frameworks, first ask: what are the core assumptions of this framework? Do these assumptions match my problem? If not, should I change my problem to fit the framework, or should I reject the framework?
- **Process design**: When designing workflows for a team or project, don't directly copy industry best practices — start from your specific constraints. What is your primary uncertainty? What are your failure modes? What kind of process most effectively addresses these challenges?
- **Tool selection**: When choosing development tools, frameworks, or methodologies, evaluate whether they truly solve your core problem rather than being dazzled by marketing.

### How to Practice

**Step 1: Make assumptions explicit**

Write down the core assumptions of the framework or methodology. For example, BMAD's assumptions include:
- Software development requires clearly defined phases
- Different roles should have different responsibilities and contexts
- Documentation is an important project deliverable
- Process certainty can improve quality

**Step 2: Map assumptions to constraints**

Map each assumption to your specific constraints. Does your project truly require this kind of phase division? Does your team truly need this kind of role separation? Is your uncertainty low enough that process certainty can deliver benefits?

**Step 3: Small-scale pilot**

Run a small-scale pilot with explicit success metrics. Don't fully adopt it from the start; test the methodology within a limited scope. The metrics to measure: does this methodology actually help us complete tasks faster? Does it reduce errors? Does it improve code quality?

**Step 4: Keep the templates, discard the rituals**

If the pilot succeeds, retain the parts that are truly valuable (such as PRD templates, architecture document structures), but discard the purely ritualistic parts (such as daily standups, lengthy review processes). The value of a methodology lies in its artifacts and ways of thinking, not in its rituals.

**Step 5: Continuously iterate**

Periodically review your methodology. Ask yourself every three months: is this methodology still effective? Have any new constraints or failure modes emerged? Does it need adjustment? Methodologies are not immutable — they should evolve as your understanding of the problem deepens.

## 4. Pitfalls and Insights

### 4.1 The "Framework Worship" Trap

Many people say "we've adopted BMAD" or "we use Scrum" as if choosing a framework solves all problems. But in reality, a framework is only a reference, not a bible. Tools go out of fashion; understanding the essence of tools does not. What's worth learning from BMAD is its engineering thinking about agile processes — not its framework worship. Treat it as a reference, not a mandatory standard.

### 4.2 The "One-Size-Fits-All" Trap

A methodology that claims to apply equally to all projects has not truly understood the nature of the problem. A good methodology should be adjustable to specific circumstances. If you find yourself forcibly adapting to a methodology rather than the methodology adapting to your problem, it's time to reassess.

### 4.3 The "Cost-Benefit Imbalance" Trap

Many teams invest large amounts of time and energy following a methodology but never ask whether this investment is truly yielding returns. When costs exceed benefits, you should have the courage to abandon the methodology rather than persist. This is why "exit ramps" are important — they give you a graceful way to step away.

## 5. Related Axioms

- **A06. Framework Selection Is Worldview Lock-In** — The purpose of first-principles methodology design is to help you make conscious decisions when choosing frameworks, rather than passively accepting the worldview of the framework's author.
- **A07. Design Philosophy Determines the Capability Ceiling** — Different methodologies embody different design philosophies. Understanding the differences between these philosophies helps you choose the methodology best suited to you.
- **T01. Infrastructure Over Components** — The value of a methodology lies in its infrastructure (document structure, context management, observability), not in its components (tools, frameworks, processes).
- **T02. Result Certainty** — The ultimate goal of first-principles methodology design is to ensure you can reliably achieve intended results.

## 6. Summary

The core idea of first-principles methodology design is simple: don't blindly adopt frameworks — start from your specific problem and design a methodology tailored to it. This process involves making assumptions explicit, mapping them to constraints, running small-scale pilots, retaining the valuable parts, and continuously iterating.

In the AI era, this principle becomes even more important. Because AI's capability boundaries are still changing rapidly, the assumptions of any framework may quickly become outdated. The wisest approach is to remain framework-neutral, start from first principles, use libraries rather than frameworks, and embrace the builder's mindset. The cost of doing so is low (because the underlying system is simple), but the return is high (because you retain complete flexibility and depth of understanding).

Finally, remember: methodologies exist to serve people, not people to serve methodologies. When a methodology becomes a burden, it's time to reassess.
