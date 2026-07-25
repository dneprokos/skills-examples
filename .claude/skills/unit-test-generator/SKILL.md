---
name: unit-test-generator
description: >-
  Generate unit tests via a 3-phase pipeline with per-phase model selection: Analyst (opus, test plan) → Architect (opus, mock strategy) → Coder (sonnet, test file). Supports C#, Java, Python, TypeScript/React. Use when asked to generate, create, or write unit tests for any class or function. Add 'skipReview: true' to skip phase reviews and run all phases in one pass.
argument-hint: "class name or attach source file; add 'skipReview: true' to skip phase reviews"
tools: [read, search, edit]
---

# Unit Test Generator — Orchestrator Skill

Coordinate the three-phase unit test pipeline by spawning a dedicated subagent per phase. Each agent runs on its own model. **Never combine responsibilities across phases.**

## First: Class Context Check

Before starting, verify you have a target:

1. User specified a class/function name
2. A source file is attached or open in the editor
3. A class or function was referenced in the conversation

**If none are true**, respond:

> Please specify the class or function you want to create unit tests for. You can either:
>
> - Provide the name (e.g., "generate tests for `MyService`")
> - Open the source file in the editor
> - Attach the source file to the conversation

Do not start the pipeline without a concrete target.

## Pipeline Overview

```
Source class
     │
     ▼
Phase 1 — ut-analyst agent (opus)    → JSON test plan
     │          pause for review (unless skipReview)
     ▼
Phase 2 — ut-architect agent (opus)  → Strategy summary
     │          pause for review (unless skipReview)
     ▼
Phase 3 — ut-coder agent (sonnet)    → Complete test file
```

> **`skipReview` parameter** — by default, this skill **pauses after each phase** and asks for confirmation before continuing. Pass `skipReview: true` to run all three phases without pausing.

---

## Phase 1 — Analyst (opus)

Spawn the `ut-analyst` subagent. Construct its prompt with:

- The source file path or class content provided by the user
- Instruction to emit only the JSON test plan

Wait for the agent to return the JSON test plan. Display it to the user.

**If `skipReview` is false (default):** Stop and ask:

> _"Phase 1 — Analyst complete. Review the test plan above. Reply 'continue' to proceed to Phase 2 (Architect), or provide feedback to adjust the plan."_

Wait for "continue" (or feedback) before proceeding.

---

## Phase 2 — Architect (opus)

Spawn the `ut-architect` subagent. Construct its prompt with:

- The full Analyst JSON test plan from Phase 1
- Instruction to emit only the strategy summary

Wait for the agent to return the strategy summary. Display it to the user.

**If `skipReview` is false (default):** Stop and ask:

> _"Phase 2 — Architect complete. Review the strategy above. Reply 'continue' to generate the test code, or provide feedback to adjust."_

Wait for "continue" (or feedback) before proceeding.

---

## Phase 3 — Coder (sonnet)

Spawn the `ut-coder` subagent. Construct its prompt with:

- The full Analyst JSON test plan from Phase 1
- The full Architect strategy summary from Phase 2
- Instruction to generate the complete test file and write it to disk

Wait for the agent to return the completed test file. Display the file path and content to the user.

---

## Hard Rules

- **Never combine Analyst, Architect, and Coder responsibilities in a single step** — each phase produces its own explicit output before the next begins
- **Never skip Phase 1 or Phase 2** — the Coder requires both the JSON plan and the Architect strategy
- **Pass full phase outputs between agents** — do not summarize or truncate the JSON or strategy when building each agent's prompt
- **Preserve user feedback** — if the user provides corrections after a phase review, incorporate them into the next agent's prompt before spawning

---

## Error Recovery

### Phase 1 returns malformed JSON

Ask the user whether to re-run Phase 1 or provide a corrected JSON plan manually before proceeding to Phase 2.

### Unsupported language

If the detected language is not C#, Java, Python, or TypeScript:

> This pipeline currently supports C#, Java, Python, and TypeScript/React. The detected language `{lang}` does not have a matching reference file. You can still proceed, but adapt the generated output to your project's framework conventions.

### User provides feedback after a phase

Incorporate the feedback into the next agent's prompt. State clearly what was adjusted before spawning the next phase.
