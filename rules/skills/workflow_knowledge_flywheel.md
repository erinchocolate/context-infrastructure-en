# Knowledge Flywheel Design Pattern

## Metadata

- **Type**: Workflow
- **Applicable Scenarios**: Knowledge engineering, unstructured information processing, knowledge graph construction
- **Creation Date**: 2026-02-21
- **Source**: Knowledge graph project practice

---

## Core Formula

**Dumb data + Dumb methods + Dumb models = Smart knowledge**

Accept the imperfection of starting data, and gradually improve knowledge purity through an iterable system.

---

## Why Choose "Dumb Methods"?

### The Dual Shackle of Closed-Source APIs

1. **Cost anxiety**: Per-token billing discourages trying computation-intensive dumb methods
2. **Pace disruption**: Batch request response times measured in hours, interrupting the fluid "think-validate-adjust" rhythm

### The Liberation of Local Deployment

After switching to locally deployed open-source models:
- Marginal cost approaches zero
- Large-scale iteration becomes a viable path
- 5090 cluster + vLLM: 32B model with 128k context requires only two GPUs

---

## The Four-Step Flywheel Loop

```
Trigger → Invoke Basic Module → Produce Incremental Progress → Refine
  ↑                                                                ↓
  ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

### 1. Trigger

Identify a small, verifiable sub-problem.

### 2. Invoke Basic Module

Use simple, reliable atomic operations:
- Linear scan (rather than complex indexing)
- Semantic retrieval (embedding + cosine)
- Structured output (JSON/table)

### 3. Produce Incremental Progress

Each loop must have a measurable output:
- Extract one entity relationship
- Clarify one ambiguous concept
- Fill one information gap

### 4. Refine

Solidify progress into the knowledge base, making it the foundation module for the next round.

---

## Design Principles

### 1. Problem Decomposition

Break grand problems down into countless small, verifiable sub-problems.

### 2. Independence

Each loop is an independent, logically clear process, not dependent on complex state.

### 3. High Success Rate

Each sub-task is designed to succeed inevitably, avoiding discouragement.

### 4. Convergence

The flywheel direction is clear; each iteration moves closer to the goal.
### 5. Stagnation Point Breakthrough Strategy

Methods for breaking through data flywheel "stagnation points" (extremely rare data):
 Use VLM for initial harvesting
 Correct via Human-in-the-loop
 Form cold-start seed data

---

## Basic Module Examples

### Linear Scan

```python
# Don't over-design indexes, get it running with linear scan first
for chunk in text_chunks:
    if is_relevant(chunk, query):
        yield extract_info(chunk)
```

### Semantic Retrieval

```python
# embedding + cosine similarity handles most scenarios adequately
def semantic_search(query, corpus, top_k=10):
    query_emb = embed(query)
    scores = [cosine(query_emb, doc_emb) for doc_emb in corpus_embs]
    return top_k_indices(scores)
```

### Structured Output

```python
# Force JSON output for easier downstream processing
prompt = """
Extract character relationships from the following text, output in JSON format:
{"relations": [{"person_a": "...", "relation": "...", "person_b": "..."}]}
"""
```

---

## Model Selection Recommendations

### Recommended: Controllable Local Models

- **Qwen3-32B**: Validated for stability in knowledge engineering tasks, can produce stable output without special prompt tuning
- **Quantization**: INT4 quantized 32B model with 128k context window requires only two GPUs

### Not Recommended

- Expensive closed-source APIs (unless budget is unlimited)
- Models requiring complex prompt engineering to format output

---

## Pitfalls to Avoid

1. **Over-designing indexes**: Get it running with dumb methods first, then consider optimization
2. **Pursuing perfect data**: Accept imperfect starting point, let the flywheel iterate
3. **Complex pipelines**: Every additional step adds another failure point
4. **Premature optimization**: Ship version 1.0 first, then talk about optimization

---

## Real-World Case

### Example: Structured Knowledge Graph

- **Input**: Tens of millions of characters of novel text
- **Output**: Interactively queryable structured knowledge graph
- **Method**: Linear scan + semantic retrieval + four-step flywheel
- **Deployment**: *(your own deployment address)*
- **Cost**: First version using closed-source API was relatively expensive; after switching to local deployment, marginal cost is zero

---

## See Also

- [T9. Data Strategy and MDP](../axioms/t09_data_strategy_mdp.md) — MDP concept, data flywheel stagnation point breakthrough, data sovereignty and accumulation

---

## Change Log

| Date | Change |
|------|--------|
| 2026-02-21 | Promoted from OBSERVATIONS.md, organized as independent skill |
