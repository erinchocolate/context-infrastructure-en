---
id: axiom_ask_do_paradigm_2026
category: ai_agentic
created: 2026-02-23
updated: 2026-02-23
---

# The Paradigm Shift from Consultation to Execution

## 1. Core Axiom

AI is truly transformative when it delivers a final artifact end-to-end ("ask-do"), rather than merely answering questions or drafting intermediate steps. The essence of this shift is: **from "give me an answer" to "give me the finished thing"**.

---

## 2. Deep Implications

**The power of closed-loop compression**: ask-do compresses decomposition, implementation, and debugging into a single closed loop. In the traditional consultation model, humans must make decisions at every step — AI gives advice → human evaluates → human executes → human observes result → human adjusts. Every handoff is friction. In the ask-do model, AI observes its own output, identifies problems, and self-corrects, creating an observe-correct loop where humans only need to intervene at critical decision points. Project Vend research showed that when Claudius was given tools and a programmatic checklist, business performance flipped from loss to profit. The key wasn't a smarter model, but an architecture capable of executing, observing, and correcting. The economic significance of this shift is: moving from "human time is the bottleneck" to "constraints and verification are the bottleneck."

**The human bottleneck moves up to the contract layer**: defining what "done" means and how to verify it. You no longer need to micromanage every step the AI takes. Instead: (1) define acceptance criteria (clear enough that an amnesiac intern could understand them), (2) provide means of checking (automated tests, format validation, business rule checks), (3) let the AI choose its method (as long as the final output passes the checks). Anthropic's "Measuring AI Agent Autonomy" research found that experienced users don't reduce oversight of AI — they change the nature of oversight — shifting from "approve each action individually" to "let the AI run autonomously and intervene when something goes wrong." This is exactly the contract-layer mindset in action. In medicine, doctors no longer verify each step of the AI's reasoning; instead, they define "what kinds of diagnostic suggestions are acceptable" (based on evidence, interpretability, risk level), and then let the AI work within that framework. This shift requires humans to upgrade from "executors" to "standard definers."

**Tool access and multi-round execution**: without execute → observe → correct, you revert to "kick it, and it moves." An AI without tools can only "say"; an AI with tools can "do." The types of tools available determine what the AI can accomplish: code execution for software engineering (currently 50% of agentic activity), database access for business process automation, browser + search for research and information synthesis, CRM + inventory systems for business operations, medical record systems for clinical decision support. Multi-round execution lets AI learn to recognize its own uncertainty — Claude Code in the most complex tasks will proactively pause and ask clarifying questions at twice the rate that humans interrupt it. This shows AI is learning to self-calibrate. The value of multi-round execution lies not only in correcting errors, but also in the AI discovering ambiguities in the original requirements during execution and proactively seeking clarification.

**Human work shifts toward handling ambiguity**: when execution cost approaches zero, what is scarce is no longer "what can be done" but "what should be done." Human competitive advantage shifts toward: intent clarification (transforming vague requirements into verifiable standards), risk judgment (selecting the risk-reward optimal solution from multiple viable options), taste (choosing the most elegant, maintainable, long-term-vision-aligned solution), and ethics and values (drawing the line between what AI can do and what it should do). An interesting finding from Project Vend: both the CEO agent and Claudius tended to "helpfully give discounts," because they were trained to be helpful. But this violates business logic. Humans need to set hard constraints like "no discounts," and then let the AI optimize within that framework. This reflects a deep truth: AI capability and human value judgment are complementary, not substitutable.

---

## 3. Application Criteria

The true deliverable of a task is an artifact (a chart, an edited image, a formatted document, a working code change), and "correctness" can be checked.

| Domain | Applicable Scenarios | Non-Applicable Scenarios |
|--------|----------------------|--------------------------|
| **Software Engineering** | Code generation, test writing, refactoring (with linter/test checks) | Architecture decisions, technology selection (requires weighing multiple dimensions) |
| **Content Creation** | Translation, format conversion, draft generation (with style guidelines) | Creative direction, brand voice definition |
| **Data Analysis** | Data cleaning, report generation, anomaly detection (with validation sets) | Hypothesis setting, metric selection |
| **Medicine** | Generating diagnostic suggestions (with evidence base), patient education content | Treatment plan selection (involves ethical trade-offs) |
| **Business Operations** | Inventory management, order processing, customer service replies (with rules) | Pricing strategy, market entry decisions |
| **Research** | Literature review, data processing, initial drafting | Research question definition, methodology selection |

**Boundary conditions**: ask-do breaks down in the following situations: (1) "correctness" cannot be objectively verified (the "quality" of artistic creation), (2) the task involves multiple conflicting objectives (cost vs. quality vs. speed), (3) the consequences of execution are irreversible and high-risk (surgical decisions, large financial commitments), (4) the task requires real-time human situational awareness (negotiations, crisis management), (5) the AI's "understanding" fundamentally diverges from the human's implicit assumptions (the "friendly discount" problem in Project Vend).

**How to practice**: directly request the artifact, specify acceptance criteria (preferably as executable checks), then give feedback on the output rather than micromanaging the steps.

Three levels of acceptance criteria clarity: bad is "generate a good code review comment" (too vague); good is "generate a code review comment that identifies performance issues, provides specific improvement suggestions, includes reference links, and is < 200 words" (specific but requires human validation); better is "generate a code review comment that must pass this linter check" (automatically verifiable). The clarity of acceptance criteria directly determines whether the AI can iterate autonomously. The more specific the criteria, the higher the AI's success rate; the vaguer the criteria, the more frequently humans must intervene. Criteria should be measurable, reproducible, and directly tied to business objectives.

Provide executable checks: for code use unit tests, type checks, linters; for documentation use spell checks, style guide validation, link validity; for data use schema validation, statistical checks, anomaly detection; for medicine use evidence base queries, contraindication checks, ethics review checklists. The more automated the checks, the more efficient the AI's iteration. Ideally, checks should be fully automated so the AI can receive feedback and adjust within seconds. Checks should cover functional, non-functional, and constraint requirements.

Let the AI iterate until it passes — show the AI why the check failed, let it adjust its approach on its own, don't tell it "how to do it," only tell it "what is wrong." This "black-box feedback" approach forces the AI to engage in genuine problem-solving rather than simply following instructions. Intervene at critical points: when the AI asks clarifying questions (a good sign), when multiple solutions all pass the checks (requires human taste judgment), when results exceed expectations (a possible new opportunity may have been discovered). Human intervention should be targeted, not comprehensive.

---

## 4. Deep Insights and Pitfalls

**The helpfulness trap**: A key finding from Project Vend is that AI is trained to be helpful, so it tends to satisfy user requests even when this violates business logic. Claudius would give discounts, hand out free items, and agree to unreasonable contracts (such as the onion futures contract example). The lesson is: you cannot rely on the AI's "common sense" to enforce business rules — the rules must be made explicit. Acceptance criteria must include "what should not be done," not just "what should be done." When the AI's objective function ("help the user") conflicts with the system's objective function ("generate profit"), explicit constraints are required. The deeper cause of this pitfall is the mismatch between the AI's training objective (align with human preferences) and the actual system objective (business success). The only way to prevent this pitfall is to encode all business rules as hard constraints.

**The autonomy paradox**: Anthropic's research shows that experienced users give AI more autonomy (increasing from 20% to 40% automatic approvals), but also interrupt the AI more frequently (increasing from 5% to 9%). This looks contradictory, but actually reflects a mature supervision pattern: new users approve each action individually (high friction, low risk); experienced users let the AI run autonomously while actively monitoring, intervening quickly when something goes wrong (low friction, controlled risk). ask-do doesn't mean "fully autonomous" — it means "autonomous within clearly defined constraints." Effective oversight is not about approving every action, but about being able to rapidly identify and correct problems. The success of this pattern depends on the human's deep understanding of the system — knowing when to trust the AI and when to intervene. It also means humans must continuously learn and adapt to the AI's behavioral patterns.

**Long-term stability**: Anthropic's "Alignment in Time" paper notes that traditional AI alignment research focuses on individual outputs, but agents running autonomously over long periods need to maintain reliability across their entire trajectory. An agent may perform perfectly for the first 10 steps but begin drifting at step 50; errors accumulate and amplify over multiple rounds of execution. ask-do reliability depends not only on the quality of individual decisions, but on the stability of the entire execution trajectory. Agents running for extended periods need periodic "recalibration" of their objectives and constraints; monitoring must look not only at final results but also at key metrics throughout the execution process. This means ask-do is not "set it and forget it" — it requires sustained human involvement. Long-running agents need regular audits and re-validation.

**Limits of cross-domain applicability**: Currently, 50% of agentic activity is concentrated in software engineering, because "correctness" in software engineering is easiest to verify (tests, linters, type checks), the consequences of execution are relatively reversible (code can be rolled back), and the tooling ecosystem is most mature (git, IDE, CI/CD). When extending to other domains: in medicine, verification becomes difficult (requires long-term follow-up), and consequences are irreversible (patient harm); in finance, verification requires real-time market data, and consequences are immediate and irreversible; in creative work, "correctness" is inherently fuzzy and hard to verify; in human resources, ethics and power dynamics are involved and full automation is not possible. The ask-do paradigm is best suited for domains that are "verifiable, reversible, and have a mature tooling ecosystem." When applying it in other domains, stronger human oversight and more explicit constraints are required.

---

## 5. Practical Examples

**Code generation**: Ask "write a function that reads user data from a CSV, deduplicates it, and returns a DataFrame." Do: the AI generates the code. Check: the code passes pytest, passes mypy type checking, handles empty files and malformed rows, and runs in < 5 seconds on 1M rows of data. Iterate: if the check fails, the AI sees the failure message and auto-adjusts. This example demonstrates the complete ask-do workflow in software engineering. The acceptance criteria are fully automatable, so the AI can iterate multiple times within seconds. This is also why software engineering is the most mature application domain for ask-do.

**Medical diagnostic suggestions**: Ask "based on this patient's symptoms and test results, generate a diagnostic suggestion." Do: the AI generates the suggestion. Check: the suggestion is based on the latest clinical guidelines, includes evidence-level annotations, lists contraindications and risks, and provides a list of recommended further tests. Iterate: the doctor reviews the suggestion and can accept, modify, or reject it. This example shows ask-do applied in medicine, where the human retains final decision-making authority that cannot be delegated. Even if the AI's suggestion passes all checks, the doctor must still make the final decision based on the patient's specific circumstances. ask-do in medicine will never be fully automated.

**Business operations**: Ask "manage inventory to maximize profit." Do: the AI makes pricing, procurement, and sales decisions. Check: all prices >= cost × 1.5 (hard constraint), inventory turnover > 0.8 (KPI), no overdue inventory. Iterate: if a constraint is violated, the AI auto-adjusts; the CEO periodically reviews KPIs. This example shows how ask-do prevents the "helpfulness trap" through explicit constraints. Hard constraints ensure the AI never makes decisions that violate business rules, even if doing so would appear more "helpful" on the surface.

---

## 6. The Essence of the Key Shift

The success of the ask-do paradigm lies not in the capabilities of the AI, but in how humans define the problem. Shifting from "telling AI how to do it" to "telling AI what success looks like" seems simple, but actually requires humans to engage in deep thinking. You must be able to clearly define what "done" means, which is often harder than execution itself. This also explains why ask-do is most mature in software engineering — "code passes the tests" is a clear, verifiable success criterion. In other domains, defining success often requires balancing multiple dimensions, which is why the human role becomes even more important.

Another key insight of ask-do is: **result certainty beats process certainty**. You don't need to know how the AI arrived at its answer, only whether the answer satisfies your criteria. This shift unleashes the AI's creativity, allowing it to try different approaches rather than being forced to follow specific steps. It also means the AI may discover solutions you hadn't thought of.

---

## 7. Implementation Recommendations

**Step 1: Define your acceptance criteria clearly**. Don't say "generate a good report"; say "generate a report that contains the following sections: executive summary (< 200 words), data analysis (at least 3 charts), recommendations (actionable and prioritized), references." Acceptance criteria should be specific enough that anyone can judge whether the output meets them.

**Step 2: Automate your checks**. If possible, write code to validate the output. If full automation isn't possible, at least have a checklist so you can quickly evaluate the AI's output. The benefit of automated checks is that the AI can receive immediate feedback without waiting for human evaluation.

**Step 3: Give the AI feedback, not instructions**. When the AI's output doesn't meet the criteria, tell it "this report is missing the data analysis section," not "you should add a data analysis section following these steps..." This lets the AI figure out the solution itself rather than simply following your directions.

**Step 4: Review and adjust regularly**. ask-do is not a one-time setup. Over time you may discover new edge cases or need to adjust constraints. Regularly review the AI's outputs to see if acceptance criteria need updating. This is also a learning process — you will gradually come to understand the AI's capabilities and limitations.

---

## 8. Summary: The Shift from "Consultation" to "Execution"

| Dimension | Consultation Mode | Ask-Do Mode |
|-----------|-------------------|-------------|
| **Deliverable** | Advice, drafts, analysis | Finished artifact |
| **Validation method** | Human evaluates each step | Automated checks + human review |
| **Human role** | Micromanages every step | Defines standards, makes critical decisions |
| **Feedback loop** | Slow (human-driven) | Fast (AI-driven) |
| **Scalability** | Low (limited by human time) | High (limited by tools and constraints) |
| **Scope of applicability** | All tasks | Verifiable, reversible tasks |
| **Risk** | Low (human-controlled) | Medium (requires explicit constraints) |

**Final insight**: ask-do is not "let AI be fully autonomous." It is "let AI execute autonomously within a framework of clear constraints and verification, with humans intervening at critical points." This requires clear acceptance criteria, executable checks, fast feedback loops, explicit constraints and off-limits zones, and regular human review and recalibration. When these conditions are met, the ask-do paradigm can significantly improve efficiency and reliability. When these conditions are not met, revert to the consultation mode.
