# context-infrastructure-en

meiqiao's context infrastructure, built on the design philosophy of [grapeot/context-infrastructure](https://github.com/grapeot/context-infrastructure).

## Design Philosophy

AI agent's value comes not from model intelligence, but from the context environment you build around it. That environment must accumulate over time, forming a flywheel: input → refine → distill → improve work.

## Three-Layer Knowledge Architecture - root level

```
01 raw/       Raw inputs, unprocessed: conversation logs, one-off scripts, unfiltered notes
02 trusted/   Refinements of raw: OBSERVATIONS.md, personal-understanding retrospectives, structured reflections
03 refined/   Public-facing, reusable: Axioms, Skills, core guides
```

## Three-Layer Knowledge Architecture - project level

```
01 raw/       Raw inputs: meeting notes, requirements docs, bug reports, AI conversation outputs
02 trusted/   Stable knowledge that helps me/AI understand and operate the project — architecture docs, design decisions, research conclusions, SOPs
03 refined/   Shareable artifacts: stakeholder briefs, team presentations, documentations etc
```

## Directory Structure

```
AGENTS.md                        # Session entry point
README.md
01 raw/                          # All raw inputs (local, not synced)
02 trusted/                      # Refined observations and reflections (local, not synced)
03 refined/                      # Public reusable knowledge system
  SOUL.md                        # AI identity and behavioral principles
  USER.md                        # User profile
  COMMUNICATION.md               # Communication style guide
  WORKSPACE.md                   # Directory routing quick reference
  SOP.md                         # Daily work operations manual
  axioms/                        # Decision principles distilled from experience
    INDEX.md
  skills/                        # Reusable workflows and best practices
    INDEX.md
  tools/                         # Utility scripts (Confluence sync, semantic search, etc.)
projects/                        # Active project contexts
archive/                         # Archived content
```
