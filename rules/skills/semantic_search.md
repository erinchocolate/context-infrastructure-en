# Semantic Search Skill
## 1. Skill Overview

`semantic-search` is a **general-purpose semantic search tool** that can index any local text files and perform natural language queries. It goes beyond keyword matching to understand semantic-level associations, and is suitable for any scenario requiring content retrieval by meaning rather than literal text from large volumes of text.

The most typical use case is searching the user's personal knowledge base (blog posts, logs, research reports), but the tool is not limited to this. `--file-list` can point to any collection of text files: chat records, third-party documents, research materials, code comments, etc.

**For the user's knowledge base, this is the core tool for accessing deep preferences and personal philosophy, and is the key infrastructure for implementing AI Heartbeat Step 2 (Reflection Layer).**

### 1.1 When to Use

**Scenario A: Searching the user's knowledge base (most common)**
 **Deep background mining**: Understand the user's long-term evolution of views on a topic (e.g., "Agentic AI," "astrophotography").
 **Associative thinking**: Find historical experiments, essays, or reflections related to the current task, even when keywords don't exactly match.
 **Decision support**: Retrieve past reviews or design discussions to provide reference for current architectural decisions.
 **Disambiguation**: When the user mentions a vague concept, find the most relevant historical definition.
 **Building Axioms / Digital Twin**: When consolidating axioms or deep reflections, **must** first perform semantic search to align with historical cognition.

**Scenario B: Analyzing any text collection**
 **Third-party content analysis**: Search by topic in chat records, interview transcripts, meeting minutes (e.g., "find all discussions about AI from a specific person").
 **Research material mining**: Do semantic retrieval in a batch of downloaded documents/reports, finding relevant paragraphs that keyword search wouldn't find.
 **Cognitive profile extraction**: Extract patterns by dimension (technical opinions, values, methodology) from large amounts of conversational data.
 **Cross-document topic discovery**: Discover semantically related but differently phrased content in heterogeneous text collections.

### 1.2 Trigger Recommendations

**Active triggers (must execute)**:
 When you are building axiom documents under `rules/axioms/`
 When the task involves the user's core values, methodology, or philosophical system
 When you need to understand the user's "intellectual evolution history" in a certain domain
 When doing reflection-layer work (consolidating axioms, deep reviews)
 When you need to extract information from large volumes of text by topic or semantic dimension (not limited to the user's content)

**Passive triggers (user explicitly requests)**:
 "Search what I thought about X before"
 "Look for whether there is relevant background material"
 "Help me summarize thinking on topic Y"
 "How did I solve similar problems before?"
 "Find X-related content in this batch of chat records/documents"
 "Analyze someone's views on topic Y"

---

## 2. Usage Instructions

### 2.1 Core Command
```bash
python tools/semantic_search/main.py \
    --file-list tmp/search_files.txt \
    --query "<natural language query>" \
    --top-k 10 \
    --cache-dir .knowledge_cache
```

### 2.2 Parameter Specifications
- `--file-list`: Required. Points to a text file containing a list of file paths to search. Recommended to place in `tmp/` directory.
- `--query`: Required. A complete, descriptive sentence. For example, "user's latest thinking on the core contradictions of Agentic AI" is better than "Agentic AI."
- `--top-k`: Optional. Number of relevant fragments to return, default 5, recommended to set to 10 for broader context.
- `--cache-dir`: **Must specify as `.knowledge_cache`** (in root directory), to reuse pre-computed feature vectors and significantly improve response speed.

---

## 3. Standard Workflow

1.  **Prepare file list**: Filter knowledge base areas based on requirements (see `rules/WORKSPACE.md`).
    ```bash
    mkdir -p tmp
    # Example: search blog posts and research reports
    find contexts/blog/content contexts/research -name "*.md" > tmp/search_files.txt
    ```
2.  **Execute semantic search**:
    ```bash
    source .venv/bin/activate
    export OPENAI_API_KEY=$(grep OPENAI_API_KEY .env | cut -d '=' -f2)
    python tools/semantic_search/main.py --file-list tmp/search_files.txt --query "..." --top-k 10 --cache-dir .knowledge_cache
    ```
3.  **Analyze and synthesize**: Read search results (usually including score, source_file, text), conduct comprehensive analysis combined with metadata (date, category).
4.  **Clean up**: Delete `tmp/search_files.txt` after task completion.

---

## 4. Common Search Paths

When searching the user's knowledge base, prioritize the following paths:
- `contexts/blog/content/`: In-depth technical articles and core thinking.
- `contexts/daily_log/`: Daily personal activity records, capturing the most authentic evolution of ideas.
- `contexts/research/`: In-depth research conclusions.
- `contexts/life_record/data/`: Life recording transcripts (including daily life summaries and meeting records).
  - 2026 data: `contexts/life_record/data/<YYYYMMDD>/`
  - 2025 data: `contexts/life_record/data/2025/<YYYYMMDD>/`
  - Both daily summary `.md` and raw transcript `.csv` are searchable
- `rules/skills/`: Methodology consolidation.

These are common shortcut paths. `--file-list` can point to any collection of text files, for example:
```bash
# Search life transcripts (including 2025 and 2026)
find contexts/life_record/data -name "*.md" -not -path "*/.venv/*" > tmp/search_files.txt

# Search WeChat chat records
find contexts/wechat -name "*.csv" > tmp/search_files.txt

# Search all materials for a research project
find contexts/<your-project> -name "*.md" > tmp/search_files.txt

# Search any temporary documents
ls adhoc_jobs/some_project/*.txt > tmp/search_files.txt
```

---
**Version**: 1.2.0
**Last Updated**: 2026-03-15
