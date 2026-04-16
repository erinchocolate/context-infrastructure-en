# Daily Work SOP

> This document is the operational manual for day-to-day work. Treat it as a checklist of "what needs to happen each day," not a theoretical document.
>
> The design philosophy behind it: **Context Rot is the number one enemy of AI workflows.**
> The AI's context window has seven-second memory — every new session, all previous understanding resets to zero.
> The solution is to continuously write daily work outputs into files, letting knowledge slowly sediment into axioms and skills, which then take effect automatically in the next session.
> Once this flywheel is spinning, what you write today will make work three months from now more precise.

---

## I. Daily Workflow

### ☀️ Morning: Before Starting Work (5 minutes)

1. Open Claude Code and give the AI a single sentence summarizing what you're doing today:

   > "Today's task is [specific goal]. The success criterion is [verifiable outcome]. The relevant files are [paths]."

   **Why**: 70% of AI coding problems come from unclear context and success criteria. This one sentence is the highest-ROI investment.

2. If starting a new project today, first update or create `projects/<name>/README.md`

---

### 🔧 During Work: Maintain Context as You Go

**Tell the files what you would otherwise tell a colleague.**

#### Maintain the Project README

`projects/<name>/README.md` is the AI's entry point for a project. Update it when:

- You make an important architectural decision
- You complete a phase or milestone
- You discover an important constraint or pitfall
- You introduce a new tool or dependency
- The current focus of work changes

A sentence or two is enough — it doesn't need to be perfect.

#### Put New Documents in the Right Place

| Content | Storage Path |
|---|---|
| Daily personal activity log (unrelated to any project) | `01 raw/YYYYMMDD_<name>.md` |
| Meeting notes, decision documents | `projects/<project>/01 raw/` |
| Technical research, research reports | `01 raw/YYYYMMDD_<name>.md` |
| Things learned, architecture retrospectives, methodology thinking | `02 trusted/<name>.md` |
| Code experiments, one-off scripts | `projects/<project>/01 raw/` |

Remember to update `03 refined/WORKSPACE.md` when adding new directories or projects.

---

### 🌆 End of Work: Daily Observation (5 minutes)

**This is the most important step in the entire system.**

Paste this into Claude Code (template also available in `02 trusted/PROMPTS.md`):

```
Review our work today. Summarize key observations using the red/yellow/green system and append to 02 trusted/OBSERVATIONS.md:

- 🔴 Red: Cross-project methodology or constraint insights (cognitive crystallizations with reuse value 3 months from now)
- 🟡 Yellow: Key decisions, progress, and problems encountered on active projects
- 🟢 Green: Routine task completion records

Filtering criteria:
- Only record content with cognitive value; don't mechanically log every action
- If there's nothing worth recording today, write nothing
- Each observation should be no longer than 2-3 sentences
```

---

## II. Weekly Workflow

### 📅 Weekend: Weekly Reflection (15 minutes)

Trigger after accumulating 3+ days of observations.

#### Method A: Manual

```
Read 02 trusted/OBSERVATIONS.md and analyze this week's observation records:

1. Identify recurring patterns (especially red and high-priority yellow entries)
2. Check whether any entries meet promotion criteria:
   - Cross-project generality (not limited to one specific scenario)
   - Multiple validations (appeared 2+ times)
   - Clear application context (you know when to use it)
3. For entries that qualify, draft them as axiom or skill candidates (place in the corresponding directory)
4. Clean up expired green entries
5. Merge duplicate yellow entries
6. Append the reflection results to the "Weekly Reflection" section of OBSERVATIONS.md
```

**Promotion target files**:

| Content Type | Target File |
|---|---|
| Decision principles, thinking frameworks | `03 refined/axioms/<name>.md` + update `INDEX.md` |
| Reusable workflows, operational procedures | `03 refined/skills/<name>.md` + update `INDEX.md` |
| AI behavior/communication preferences | `03 refined/COMMUNICATION.md` |
| User profile updates | `03 refined/USER.md` |
| Workspace routing changes | `03 refined/WORKSPACE.md` |

---

## III. Monthly Workflow

### 🗓️ Monthly System Health Check (30 minutes)

```
Perform a health check on the entire context system:

1. Read 03 refined/axioms/INDEX.md: Are the existing axioms still accurate? Do they need updating based on new evidence?
2. Read 03 refined/skills/INDEX.md: Are there skills that should be retired or merged?
3. Read 02 trusted/OBSERVATIONS.md: Are there red observations that have been sitting unpromotioned for several weeks? Why?
4. Read AGENTS.md: Is it too long? Does it need to be split into sub-files?
5. Summarize the system health status and next action items.
```

---

## IV. Key Principles

### Axiom vs Skill

| | Axiom | Skill |
|---|---|---|
| Answers | How to **think** | How to **do** |
| Example | "AI is an amplifier, not a replacement" | "Deep research workflow" |
| Source | Can only be distilled from personal experience, not copied from others | Portable, needs adapting |
| Location | `03 refined/axioms/` | `03 refined/skills/` |

### What to Do When AI Keeps Failing

Diagnose these three questions before switching strategies:
1. Does the AI have enough context? (error messages, logs, relevant files)
2. Is the success criterion clearly stated? ("no errors" is too vague; "row count matches" is concrete)
3. Does the AI have a way to verify its work?

If all three are satisfied and it still can't fix things, only then is it a model/architecture problem.

### When to Write a Skill

**Every time you need to explain the same process to AI a second time — write it as a skill.**

---

## V. System File Quick Reference

| File | Purpose |
|---|---|
| `AGENTS.md` | Session entry point, AI must read this on every startup |
| `03 refined/WORKSPACE.md` | Directory routing table, check here before searching for files |
| `03 refined/axioms/INDEX.md` | Index of all axioms |
| `03 refined/skills/INDEX.md` | Index of all skills |
| `02 trusted/OBSERVATIONS.md` | Accumulation point for daily observations |
| `02 trusted/PROMPTS.md` | Prompt templates for manually triggering observations/reflections |
