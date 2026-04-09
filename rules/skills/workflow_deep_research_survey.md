# Deep Research Workflow

## Metadata

- **Type**: Workflow
- **Applicable Scenarios**: In-depth, comprehensive, verifiable third-party research on a topic
- **Output Location**: `contexts/research/`
- **Creation Date**: 2026-02-19
- **Last Updated**: 2026-03-09

## Core Principles

1. **Cross-validation**: Multiple independent researchers (sub-agents) research overlapping topics to discover contradictions
2. **Traceability**: All citations must retain URLs for subsequent verification and archiving
3. **Progressive Focus**: From broad to narrow; understand the full picture before diving into details
4. **Single Deliverable**: Only one consolidated report is delivered at the end; intermediate results are not saved

## Workflow

### Phase 1: Initial Scan

**Goal**: Quickly understand the full picture of the research subject, identify key dimensions

**Operations**:
1. Use Tavily for 2-3 searches covering:
   - Basic information about the subject (what it is)
   - Market evaluation (what others say)
   - Controversies (what criticisms exist)
2. Summarize 3-5 dimensions requiring deeper research

**Output**: Preliminary impressions notes (no need to save to file, kept in memory)

### Phase 2: Split and Parallel Research

**Goal**: In-depth multi-angle research, discover information contradictions and cross-validation points

**Splitting Principles**:
- Divide into 3-5 research dimensions
- **Key**: Dimensions must have ≥50% overlap
  - Example: Researching "Course A," Dimension 1 is "positive reviews," Dimension 2 is "user cases," Dimension 3 is "price comparison"
  - Dimensions 1 and 2 both collect user feedback; Dimensions 2 and 3 both discuss value perception
  - Overlap lets different agents potentially discover different interpretations of the same information, or mutually contradictory conclusions

**Launch Sub-agents**:

Launch 3-5 sub-agents simultaneously, each responsible for one dimension. Use the following types:

- `librarian` — preferred for external research, look up documentation, open-source code, official materials
- `deep` category — autonomous in-depth research, suitable for complex multi-source tasks

```
task(
  subagent_type="librarian",
  load_skills=[],
  description="Research dimension XX",
  run_in_background=true,
  prompt="[specific research dimension prompt]"
)

# Or use deep category for more autonomous research
task(
  category="deep",
  load_skills=[],
  description="Research dimension XX",
  run_in_background=true,
  prompt="[specific research dimension prompt]"
)
```

**Tavily Parameter Preferences** (for web search):
- `max_results=6` (can increase to 10 if coverage is insufficient)
- `search_depth="advanced"`
- `include_answer=true` (get aggregated summaries)
- Enable `include_images` / `include_image_descriptions` as needed

In each sub-agent's prompt, specify:
1. What exactly to research
2. Must return URLs and original excerpts (not summaries)
3. Other relevant dimensions that can be covered (to form overlap)
4. Results **do not need** to be written to files, just returned to the main agent

**Important**: Sub-agent results are **intermediate artifacts** and do not need to be saved to the file system

### Phase 3: Integration and Cross-Validation

**Goal**: Discover contradictions, form credible conclusions

**Operations**:
1. Compare results returned by each sub-agent
2. Focus on:
   - Information found by multiple agents → high credibility
   - Information from a single source only → annotate source, suggest verification
   - Mutually contradictory information → specifically annotate, analyze reasons
3. If major contradictions are found, can launch additional sub-agents for targeted verification

### Phase 4: Write Final Report

**Goal**: Output **one** storable, traceable English research report

**Format Requirements**:
- English Markdown
- All citations must have URLs (use Markdown link format)
- Key citations retain original text excerpts (not summaries)
- Clear structure: core conclusions → dimension-by-dimension analysis → cross-validation → conclusions and recommendations

**Storage Location**: `contexts/research/<topic>_survey_YYYYMMDD.md`

**Naming Convention**: 
- English topics: `<topic>_survey_YYYYMMDD.md`
- Non-English topics: use pinyin or English keywords

**Important**: 
- Generate only **one** final report file
- Do not save sub-agent intermediate results
- Do not save raw research notes

## URL Retention Standards

### When URLs Must Be Retained

1. **Direct citations**: Quoting another person's words or opinions
2. **Data sources**: Any numbers, statistics, scores
3. **Evaluation sources**: Source of positive or negative evaluations
4. **Official information**: Official descriptions of products/courses/companies

### URL Format

```markdown
**Source description** (URL)
> Original text excerpt

or

Someone commented on a platform (URL):
> "Original text"
> 
> (👍 X 👎 Y)  # Retain like/dislike data if available
```

### Problems to Avoid

- ❌ "Someone commented that..." (no URL)
- ❌ "There are articles online criticizing..." (no URL)
- ❌ Only summarizing without citing original text (cannot be verified)

## Common Research Dimension References

| Research Subject | Possible Dimensions |
|-----------------|---------------------|
| Products/Services | Feature evaluation, price comparison, user cases, negative feedback, competitor analysis |
| Courses/Training | Course content, instructor background, student reviews, price/value, alternatives |
| Companies/Organizations | Business model, market position, reputation, controversy, financial status |
| Technology/Tools | Technical principles, user experience, applicable scenarios, limitations, alternatives |
| Opinions/Frameworks | Consensus level, authoritative endorsement, opposing voices, real-world implementation, timeline accuracy |

## Traps and Countermeasures

| Trap | Countermeasure |
|-----|----------------|
| Only finding positive information | Specifically search "criticism", "negative review", "scam", "overpriced" |
| Single information source | Require sub-agents to find multiple independent sources |
| Over-summarizing loses details | Require original text excerpts, not just summaries |
| Dimension division too clean with no overlap | Deliberately blur edges when designing dimensions |
| Sub-agent returns too shallow information | Emphasize "depth," "specificity," "original text" in prompt |
| Intermediate files pile up | Generate only one final report, do not save intermediate results |
| Using wrong subagent type | Use `librarian` or `deep` for external research; `explore` only for internal codebase search |
