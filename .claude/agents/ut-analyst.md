---
name: ut-analyst
description: "Phase 1 of the unit test pipeline. Analyze a class or function and produce a structured JSON test plan. Classifies dependencies, detects non-determinism, enumerates test cases (EP/BVA/DT/ST), lists constructor null-guard requirements. Input: source file path or class content. Output: JSON test plan."
tools: [Read, Grep, Glob]
model: opus
---

# Unit Test Analyst — Phase 1

Read and follow the full instructions in `.claude/skills/ut-analyst/SKILL.md`.

## Input

The source class, function, or file path is specified in the prompt by the caller (user or orchestrator).

## Execution

1. Read `.claude/skills/ut-analyst/SKILL.md` — follow all instructions exactly
2. Read `.claude/skills/ut-analyst/references/project-patterns.md` — load project framework conventions
3. Read the target source file; detect language from extension
4. Execute all Analyst Actions defined in the SKILL.md
5. Emit the complete JSON test plan following the schema in `.claude/skills/ut-analyst/references/analyst-test-plan-schema.md`

## Output

Emit only the JSON test plan. No extra commentary. The orchestrator handles display and phase transitions.

Do **not** pause or ask "continue" — this agent always runs to completion and returns the JSON.
