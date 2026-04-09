# Setup Guide: Context Infrastructure

This is an AI-guided configuration walkthrough. Follow the steps in order — you'll feel the difference immediately after each one.

---

## Step 1: Fill in the Identity Files (Required, 5 minutes)

**Value**: Complete this step and the AI's behavior is immediately personalized. This is the highest-ROI step.

### 1a. Fill in USER.md

Open `rules/USER.md` and replace the template content with your own information.

At minimum, fill in these fields:
- **Name**: How you want the AI to address you
- **Timezone**: Avoid time confusion
- **Background**: Who you are and what you do
- **Technical interests**: The more specific, the better
- **What annoys you**: Help the AI avoid communication styles you dislike

**Verification**: After filling it in, ask the AI "Tell me what you know about me" and check whether it can describe you accurately.

### 1b. Customize SOUL.md (Optional but Recommended)

Open `rules/SOUL.md` and adjust the AI's core behavioral tone.

The default content is already a solid general foundation (direct, opinionated, no filler). If you have specific preferences, add them in the "Atmosphere" and "Core Truths" sections.

---

## Step 2: Explore and Extend Skills (Recommended, 15 minutes)

**Value**: Understand the skill format and start building your own reusable workflows.

### 2a. Browse Existing Skills

Open `rules/skills/INDEX.md` and quickly scan the available skill categories:

- **BestPractice**: Ready to use immediately, independent of your specific tools and projects
- **Workflow**: Research, slide creation, cognitive profiling, etc. — understand before adapting
- **API Guide**: ⚙️ marked ones require configuration, ✅ marked ones are ready to use

### 2b. Create Your First Skill

Find something you do frequently (calling an API, processing a certain type of data, running a workflow), and create `rules/skills/<category>_<name>.md` in the following format:

```markdown
# Skill: Name

## When to Use
What situation triggers this skill

## Prerequisites  
What tools/configuration are needed

## Steps
1. Step one
2. Step two

## Examples
Specific commands or code
```

Add the new skill to the appropriate category in `rules/skills/INDEX.md`.

### 2c. About Axioms

Recommendations:
- Browse `rules/axioms/INDEX.md` first to understand the categories and core meanings
- Note down any axioms that resonate with you
- Over time, accumulate your own axioms from your project experiences (follow the same format)
