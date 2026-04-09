# mc-context-infrastructure

Meiqiao's personal AI context infrastructure system, built on the design philosophy of [grapeot/context-infrastructure](https://github.com/grapeot/context-infrastructure).

## Design Philosophy

The value of AI comes not from model intelligence, but from the context environment you build for it. This environment must accumulate continuously over time, forming a flywheel of "observe -> reflect -> distill -> improve work."

## Three-Layer Memory Architecture

```
L3 (global constraints): all files under rules/ -> passively loaded each session
L1 (daily observations): contexts/memory/OBSERVATIONS.md -> manually triggered
L2 (weekly reflections): distilled from L1, promoted to L3
```

## Directory Structure

```
CLAUDE.md                        # Session entry point (auto-loaded by Claude Code)
rules/
  SOUL.md                        # AI identity and behavioral principles
  USER.md                        # User profile
  COMMUNICATION.md               # Communication style guide
  WORKSPACE.md                   # Directory routing quick reference
  axioms/                        # Decision principles distilled from experience
    INDEX.md
  skills/                        # Reusable workflows and best practices
    INDEX.md
contexts/
  memory/                        # Memory system
    OBSERVATIONS.md              # Daily observations + weekly reflections
    PROMPTS.md                   # Observer/Reflector prompt templates
  research/                      # Research reports
  learning/                      # Things learned / retrospectives
  daily_log/                     # Daily personal activity log
adhoc_jobs/                      # Temporary projects
```

## Acknowledgements

Architecture design references [grapeot/context-infrastructure](https://github.com/grapeot/context-infrastructure).
