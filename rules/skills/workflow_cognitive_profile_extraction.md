# Cognitive Profile Extraction Workflow

## Metadata

- **Type**: Workflow
- **Applicable Scenarios**: Extracting predictable cognitive profiles from unstructured conversation data (group chats, Slack, Discord, email, podcast transcripts, etc.)
- **Output**: A set of "axioms" — conditional trigger rules that can be used to predict a target person's response direction, argumentative stance, and rhetorical approach on new topics
- **Dependencies**: [Parallel Subagent Workflow](./workflow_parallel_subagents.md), [Deep Research Workflow](./workflow_deep_research_survey.md)
- **Creation Date**: 2026-03-13
- **Source**: Example observation project (8139 WeChat messages → 15 axioms, 89% predictive accuracy in back-testing)

---

## Model Guardrail

**Check before executing**: Confirm whether the current model ID contains `opus`.

- **Is Opus** → Continue. Your context window is extremely precious; your core capabilities are design, quality assurance, and writing. All research, data processing, and code writing must be delegated to sub-agents, and parallel by default. Writing — including axiom text, index, and final report — must be done by you directly and must not be outsourced.
- **Not Opus** → Pause and ask the user:

  > "This workflow is designed to be executed by Opus — Opus's context window and writing capability are core assumptions of the process. Your current model is not Opus. Do you confirm you want to continue? If the model was selected by mistake, it is recommended to switch to Opus before starting."

---

## Core Principles

### 1. Parallel + Delegation is the First Principle

Opus's context window is a scarce resource and should not be consumed by scanning and retrieval. Workflow division of labor:

| Role | Who Does It | Notes |
|------|-------------|-------|
| **Plan (Design)** | Opus main agent | Research plan, dimension breakdown, task boundaries for each iteration |
| **Execute (Research)** | Sub-agents (parallel) | Data scanning, keyword retrieval, counterexample hunting, statistical analysis |
| **Write (Writing)** | Opus main agent | Axiom text, index, report — conceptual consistency and stylistic unity can only be guaranteed by one agent |
| **QA (Quality Assurance)** | Opus main agent | Cross-validate sub-agent results, identify contradictions, judge convergence |

Sub-agent scheduling follows the rules in [Parallel Subagent Workflow](./workflow_parallel_subagents.md): parallelism ≤5, research overlap 30-50%, `run_in_background=true`.

### 2. Writing is Not Delegated (Hard Constraint)

All text in the final output — axiom definitions, index, methodology report — must be written directly by Opus. Rationale:
- Conceptual consistency between axioms (the same phenomenon described in different axioms must not contradict each other)
- Precision of cross-references (V05 referencing V07's tension description must align on both sides)
- Stylistic unity (15 axioms should read as if written by the same person, not patchworked from 5 agents)

Sub-agent output is **raw research material**, not any part of the final draft.

### 3. Iteration Rounds are Dynamically Rolling

**Minimum floor**: 3 rounds (broad scan + deep validation + at least one round of stress testing/finalization).

**No upper limit set**, but before each round begins, evaluate whether to continue (see "Convergence Criteria"). Empirical experience: 3-4 rounds is a common convergence point; over 5 rounds shows clear diminishing returns and overfitting risk.

### 4. Axioms are Conditional Trigger Rules, Not Absolute Laws

Each axiom should have counterexamples and boundary conditions. An axiom without counterexamples is either too broad ("he cares about AI") or has insufficient evidence (appears perfect only because counterexamples haven't been seriously sought).

---

## Workflow

### Phase 0: Data Preparation

**Goal**: Transform raw data into a searchable collection of the target person's messages.

**Input Requirements**:
- A collection of the target person's text messages
- Ideally with timestamps (required: for temporal evolution analysis)
- Ideally with source labels — group name/channel name/conversation type (required: for cross-source comparison)
- Optional: version with context (each message accompanied by N preceding/following messages from others, for understanding interaction patterns)

**Pre-processing Steps** (delegate to sub-agent):
1. Extract target person's messages from raw format (filter by ID, not display name — display names may vary across groups)
2. Produce statistical summary: total message count, time span, message distribution across sources
3. If multiple conversation sources, produce context-enriched version

**Scale Assessment → Determine Validation Tier**:

| Data Scale | Recommended Axiom Count | Validation Tier | Notes |
|-----------|------------------------|-----------------|-------|
| < 500 messages | 3-5 | Lightweight | Sparse data, skip stress testing |
| 500-2000 messages | 5-8 | Standard | Simplified stress testing (mutual exclusivity + counterexamples, skip predictive back-testing) |
| 2000-5000 messages | 8-12 | Standard+ | Can do simplified predictive back-testing (3 topics) |
| 5000+ messages | 10-15 | Full | All three validation layers, including predictive back-testing (5+ topics) |

**Semantic Search Preparation** (recommended): If data volume ≥ 1000 messages, it is recommended to build an embedding cache at this stage (see [Semantic Search Skill](./semantic_search.md)). Split messages into individual text files or chunks, run a single embedding pass to build the cache. Sub-agents in Phase 1/2 can use semantic search instead of pure keyword grep — semantic search can find messages that "have different keywords but similar meaning," especially valuable for discovering implied opinions and edge cases.

**Phase 0 Output**: Data overview report, validation tier decision, preliminary dimension hypotheses, embedding cache (if applicable).

---

### Phase 1: Broad Scan (R0)

**Goal**: Parallel scan across five orthogonal dimensions to produce a candidate axiom pool.

**What Opus Does (Plan)**:
1. Determine 5 scanning dimensions — suggested default dimensions:

| Dimension | Focus | Typical Keywords |
|-----------|-------|-----------------|
| Domain opinions | Core judgments in the target person's professional domain (technical, business, academic, etc.) | Domain-dependent |
| Methodological preferences | How they do things, make decisions, evaluate | process, standards, methods, principles |
| Values and stances | Social issues, ethical judgments, institutional preferences | fairness, efficiency, should, should not |
| Argumentative style | How they refute, persuade, concede | refutation markers, concession markers |
| Language and expression patterns | Sentence preferences, analogy habits, emotional markers | high-frequency phrases, punctuation usage |

2. Write prompts for each sub-agent, specifying: search scope, output format (timestamp + source + original text + candidate axiom), allowed overlap range
3. Deploy 5 sub-agents in parallel (`run_in_background=true`)

**What Sub-agents Do (Execute)**:
- Scan all data, extract patterns by assigned dimension
- Produce 3-5 candidate axioms per dimension, each with 3+ timestamped evidence items
- Annotate cross-dimensional findings (for cross-validation use)

**What Opus Does (Consolidate)**:
1. Collect results from 5 sub-agents
2. Merge overlapping candidate axioms (merge criterion: same underlying judgment, not similar phrasing)
3. Split overly broad candidate axioms
4. Produce **candidate axiom list** (estimated 12-20 candidates) and **preliminary synthesis analysis**

---

### Phase 2: Deep Validation (R1)

**Goal**: Validate the stability, uniqueness, and boundary conditions of candidate axioms.

**What Opus Does (Plan)**:
1. Design 5 validation tasks — suggested default configuration:

| Task | Goal | Method |
|------|------|--------|
| Core validation | 3-5 highest-credibility candidates, deep evidence chain excavation | Exhaustive search of related messages |
| Cross-source comparison | Variations of the same opinion across different sources | Compare by source grouping |
| Gap identification | Topics or patterns possibly missed by R0 | Open-ended scan of keywords not covered by R0 |
| Style validation | Consistency of argumentative style and language patterns | Marker word frequency statistics + pattern matching |
| Time series | Temporal stability and evolution trajectory of opinions | Group by month/quarter, annotate turning points |

2. **Critical deduplication constraint**: Inform each sub-agent "do not repeat evidence already cited in the previous round" — this single instruction produces the greatest improvement in report quality
3. Deploy 5 sub-agents in parallel

**What Sub-agents Do (Execute)**:
- Conduct deep validation per assigned task
- For each candidate axiom: provide credibility score (1-10), list of counterexamples, boundary condition suggestions

**What Opus Does (Consolidate)**:
1. Cross-validate findings from each sub-agent
2. Update credibility and add boundary conditions for each candidate axiom
3. Eliminate candidates with too-low credibility (suggested threshold: < 6.0)
4. **Judge convergence**: Is it necessary to proceed to Phase 3?

---

### Phase 3: Stress Testing (R2)

**Applicable Conditions**: Standard tier and above (data ≥ 500 messages).

**Goal**: Actively attack weaknesses in the axioms, test the predictive power of the overall framework.

**What Opus Does (Plan)**: Design 3-5 stress testing tasks. Three core things:

#### 3a. Mutual Exclusivity Check

Check whether logical contradictions exist between axioms.

Operation: Group axioms by relevance (3-4 per group), have sub-agents check for mutual exclusivity within each group. Mutual exclusivity does not necessarily need to be eliminated — it can be absorbed through layered explanations like "descriptive vs. normative" or "default mode vs. boundary mode." But conflicts must be annotated with a conflict level (1-10).

#### 3b. Counterexample Hunting

Explicitly require sub-agents to **actively look for messages that refute axioms**.

Operation: Find at least 2 counterexamples for each axiom, assign each counterexample a destructiveness score (1-10). Counterexamples are not signals of axiom failure — counterexamples that can be absorbed by boundary conditions actually make the axiom more precise.

#### 3c. Predictive Back-Testing (Full Version)

Test the effectiveness of the axiom set as a predictor.

Operation (strict order):
1. Design 5-10 hypothetical topics (covering different axiom combinations)
2. **Without searching the original data**, use axioms to make prior predictions: stance direction, argumentative strategy, possible analogies/short phrases
3. Search original data, look for semantically similar real conversations
4. Compare consistency between predictions and reality, assign scores

**Improved Back-Testing Protocol** (optional, more credible but more expensive):
- Topics randomly sampled from real data rather than self-selected by agent
- Use an **independent agent that did not participate in axiom creation** for consistency judgment
- Prediction confidence and consistency scored separately

**Known Limitations** (must be disclosed in report):
- Small sample (5-10 topics), statistical conclusions are not robust
- LLM evaluating LLM predictions has systematic bias
- Continuous scale (e.g., 89%) and binary scale (e.g., 60%) differ greatly; recommend reporting both numbers

**What Opus Does (Consolidate)**:
1. Revise each axiom's boundary conditions and credibility based on stress test results
2. Annotate inter-axiom relationship graph (closed loops, tensions, orthogonal relationships)
3. **Judge convergence**: Are additional rounds needed?

---

### Phase 4+: Finalization (R3+)

**Goal**: Opus directly writes all axiom text.

**Hard Constraint**: This Phase is not delegated. All axiom text is written by Opus alone.

**Axiom File Template**:

```markdown
# Number Title

## Core Statement
One sentence, can be cited independently.

## Elaboration
2-3 paragraphs. Explain the logical chain, describe relationships with other axioms.

## Boundary Conditions
Scenarios where this weakens or does not apply. Includes counterexamples and tensions discovered in R2.

## Representative Evidence
Original statements with timestamps and sources (3-5 items).

## Cross-Source Performance
Differences in how the same opinion is expressed across different sources.

## Credibility
Score 1-10, with brief rationale.
```

**Additional Fields for Style Axioms**:
- **Scope/Default Mode**: Specify in what contexts the style axiom activates, and when it switches

**Index File**:
- Quick reference table for all axioms (number, title, core statement, credibility)
- Inter-axiom relationship graph (closed loops, tensions, orthogonal)
- Summary of key stress testing findings

**If stress testing feedback requires extensive revision** (not just boundary condition fine-tuning), add one more round R3→R4: after revision, run a simplified stress test to verify revision effectiveness, then finalize.

---

### Phase 5: Publish as Web Site (Only When User Explicitly Requests)

**Do not publish proactively.** Finalization is completion. Only enter this stage when the user explicitly says "publish," "go live," or "give me a link."

Basic conversion process is in [Share Report to Web](./share_report.md); the following are additional notes for a **multi-page axiom site**:

**Structure**: Index page (index.html) + one sub-page per axiom. The index page uses a table listing all axioms (number, title, core statement, credibility), with each row's title being a hyperlink to the sub-page. Each sub-page has a "← Back to Index" navigation link at the top.

**Practical Notes**:
1. Add inter-page links in the Markdown source files first (`[V01](V01_xxx.html)`), and pandoc will automatically preserve the links during conversion
2. Each HTML file is independently self-contained (CSS inlined with `--embed-resources`), not dependent on external style sheets — this way any sub-page can display correctly when opened individually
3. Use rsync to upload the entire folder rather than file by file — ensures directory structure and link consistency
4. After uploading, verify the index page and at least 2 sub-pages return HTTP 200 with curl

**Delegation rules**: HTML conversion and upload can be delegated to sub-agents, but the Markdown source file of the index page (inter-axiom relationship graph, summary text) is written by Opus directly — this is writing, not mechanical conversion.

---

## Convergence Criteria

After each round, evaluate the following four signals:

| Signal | Meaning |
|--------|---------|
| Revision instructions can be directly executed | No more data needed to revise → can converge |
| Predictive power has reached usable level | Continuous scale ≥ 80% → framework has captured core structure |
| Counterexample types start repeating | New round finds same types of counterexamples as before → diminishing returns |
| Inter-axiom relationships have stabilized | No longer need to add, merge, or significantly reorganize → structural convergence |

**Meeting 3 of the 4 signals allows convergence.** When 2 are met, it is recommended to do one more lightweight validation round to confirm.

**Risk of over-iteration**: After 4-5 rounds, each revision round tends to grind axioms from "generalizable cognitive patterns" into "precise fitting of training data." It is better to retain some roughness than to overfit.

---

## Axiom Design Criteria

A good axiom should satisfy:

1. **Persistence**: Recurs repeatedly across time periods and topics, not a one-time statement
2. **Uniqueness**: Specific to the target person, not common wisdom most people would express
3. **Predictiveness**: Can be used to predict their stance and expression on new topics
4. **Specificity**: Multiple original statements as evidence, with evidence from multiple independent time points
5. **Non-redundancy**: Axioms do not overlap; each covers a different facet
6. **Has boundaries**: Annotates scenarios where it weakens or does not apply

**Axiom Types**: Recommended two categories —
- **Opinion type**: Defines "what stance they will take"
- **Style type**: Defines "how they will express it"

**Merge vs. Split Judgment**: Same underlying judgment → merge (even if phrasing differs); logically orthogonal underlying logic → retain as independent axiom (even if domains are similar).

---

## Methodological Insights

The following experience is distilled from the example project and applies to all cognitive profile extraction tasks:

### 1. Predictive Power is the Ultimate Validation Criterion

Evidence count and credibility scores are intermediate metrics. The final criterion for judging whether an axiom holds is whether it can be used to predict reactions to new topics.

### 2. Counterexamples are More Valuable than Positive Examples

Actively seeking counterexamples, quantifying destructiveness, absorbing counterexamples with boundary conditions — this process is much more useful than accumulating positive evidence. An axiom that has not been stress-tested with counterexamples is only an observation; one that has passed is an axiom.

### 3. Axioms Should Be Anchored at Stable Judgment Levels

When the target person begins to question a specific method but insists on the higher-level concept, the axiom should be anchored at the higher-level concept. For example: anchor on "verification is the control surface" rather than "TDD is the control surface" — the former can absorb methodological drift, the latter will be invalidated by new data.

### 4. Cross-Source Comparison Distinguishes "True Opinions" from "Social Performance"

Differences in the same person's expression across different contexts reveal which are underlying beliefs and which are audience-adapted. If an opinion only appears in one source, it may be a product of context; if it is consistent in direction across sources but expressed differently, it is more likely a genuine stance.

### 5. Time Series Distinguishes "Beliefs" from "Positions"

Without the time dimension, it is impossible to distinguish stable opinions from momentary enthusiasm. The temporal evolution of opinions is itself part of the axiom — record turning points and evolution trajectories.

### 6. Emotional Deviations Need Quantification

When you find the target person deviating from axiom predictions in certain scenarios, quantify the deviation rate (e.g., "strict scale 2%, comprehensive destructiveness 6.5/10"), rather than vaguely saying "sometimes deviates."

### 7. Deduplication Constraints Produce the Greatest Improvement in Sub-Agent Quality

Informing sub-agents "do not repeat evidence already cited in the previous round" — this single simple constraint significantly reduces redundancy and forces agents to find new evidence.

### 8. Style Axioms are Default Strategy Clusters

Target persons typically have audience-adaptive ability. Style axioms describe the default high-frequency pattern, not the only pattern. Axiom text needs to clearly annotate activation conditions and mode-switching scenarios.

### 9. Convergence Signals > Fixed Rounds

Don't preset "do N rounds" — monitor convergence signals. Over-iteration has two costs: context window consumption, and overfitting.

---

## Traps and Countermeasures

| Trap | Countermeasure |
|------|----------------|
| Axiom too broad ("he cares about AI") | Ask: what specific behavior can this predict? If not → not an axiom |
| Axiom too narrow ("he opposes TDD") | Elevate to a higher conceptual level |
| Evidence selection bias (only finding supportive evidence) | R2 counterexample hunting forces counterbalancing |
| Conceptual inconsistency across axioms | Writing not delegated; one person drafts the whole |
| Treating forwarded content as the person's own opinion | Distinguish "forwarding behavior" from "expressing stance on forwarded content" |
| Treating social-context statements as stable beliefs | Cross-source comparison + time series validation |
| Inflated predictive back-testing scores | Report both continuous and binary scale, disclose evaluator limitations |
| Over-iteration leading to overfitting | Monitor convergence signals, stop when ≥3 signals are met |
| Sub-agent research depth insufficient | Prompt explicitly requires original text excerpts + timestamps, does not accept pure summaries |
| Context window consumed by research | Strictly maintain the division: Plan/Write done by self, Execute fully delegated |

---

## Scale and Cost Reference

| Data Scale | Total Sub-Agent Calls | Estimated Rounds |
|-----------|----------------------|-----------------|
| < 500 messages | 10-12 | 2-3 rounds |
| 500-2000 messages | 12-15 | 3 rounds |
| 2000-5000 messages | 15-20 | 3-4 rounds |
| 5000+ messages | 18-25 | 3-5 rounds |

5 parallel sub-agents per round is the default configuration. Adjustable to 3-7 based on data volume and dimension complexity.

---

## See Also

- [Semantic Search Skill](./semantic_search.md) — Go beyond keyword matching; use embedding similarity to discover semantically related messages
- [Parallel Subagent Workflow](./workflow_parallel_subagents.md) — Execution rules for sub-agent scheduling
- [Deep Research Workflow](./workflow_deep_research_survey.md) — Foundation architecture of multi-agent parallel + cross-validation
- [Multi-Agent Parallel Analysis](./bestpractice_multi_agent_analysis.md) — 50% overlap, cross-validation methodology
- Example observation project (original source of this skill) — `contexts/people/magong/`

---

## Change Log

| Date | Change |
|------|--------|
| 2026-03-13 | Initial version, abstracted and generalized from example observation project methodology.md |
