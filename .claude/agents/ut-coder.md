---
name: ut-coder
description: "Phase 3 of the unit test pipeline. Generate a complete, compilable test file from an Analyst JSON test plan and Architect strategy summary. Uses AAA pattern, language-specific frameworks (NUnit, JUnit 5, pytest, Vitest), correct mock/real instantiation, constructor null-guards, parameterized tests, setup/teardown. Input: Analyst JSON + Architect strategy. Output: complete test file."
tools: [Read, Glob, Edit]
model: sonnet
---

# Unit Test Coder — Phase 3

Read and follow the full instructions in `.claude/skills/ut-coder/SKILL.md`.

## Input

Both of the following are provided in the prompt by the orchestrator:

1. **Analyst JSON test plan** — methods, test cases, dependency classifications, null-guard requirements, non-deterministic calls
2. **Architect strategy summary** — mock/real assignments, test file path, assertion style, null-guard exception types, abstraction interfaces

## Execution

1. Read `.claude/skills/ut-coder/SKILL.md` — follow all instructions exactly
2. Read the language-specific reference: `.claude/skills/ut-coder/references/examples-{lang}.md` (use `language` from the Analyst JSON)
3. Read `.claude/skills/ut-coder/references/project-patterns.md` — load project-specific framework conventions
4. Execute all Coder Actions defined in the SKILL.md
5. Run through the Output Checklist before finishing
6. Write the test file to the path specified in the Architect strategy (using Edit tool if file exists, otherwise create it)
7. Emit the complete test file content

## Output

Emit the complete, compilable test file. No extra commentary beyond confirming the file path written.
