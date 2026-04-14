# Unit Test Analyst Skill

Analyzes a class or function and produces a structured JSON test plan as **Phase 1** of the unit test generation pipeline.

## What It Does

Given a source class, function, or component, this skill:

1. **Classifies all constructor dependencies** — `interface`, `abstract`, `valueObject`, `dto`, or `primitive`
2. **Detects non-deterministic calls** — `DateTime.Now`, `Guid.NewGuid()`, `Math.random()`, etc.
3. **Enumerates test cases** per public method using four black-box techniques:
   - **Equivalence Partitioning** — valid, invalid, and special-value input groups
   - **Boundary Value Analysis** — edge cases at domain boundaries
   - **Decision Table Testing** — combinatorial input/output mapping
   - **State Transition Testing** — stateful behavior verification
4. **Lists constructor null-guard requirements** — one entry per interface/abstract constructor parameter

## Output

A complete JSON test plan following the schema in [`references/analyst-test-plan-schema.md`](references/analyst-test-plan-schema.md). This JSON is consumed by the `ut-architect` skill in Phase 2.

## How to Use

### Standalone

Trigger with `/ut-analyst` and specify the class:

```
/ut-analyst analyze MyService
/ut-analyst analyze the open file
```

### As Part of the Pipeline

The `unit-test-generator` agent invokes this skill automatically as Phase 1. Provide your source class or file to the agent and it handles the sequencing.

### Passing Output to Architect

When running standalone, copy the JSON output and provide it to `ut-architect`:

```
/ut-architect [paste JSON plan here]
```

## Skill Structure

```
ut-analyst/
├── SKILL.md                         # Core instructions (this skill)
├── README.md                        # This file
├── references/
│   ├── analyst-test-plan-schema.md  # JSON schema the Analyst must emit
│   └── project-patterns.md          # Active project conventions (swap per repo)
└── evals/
    └── evals.json                   # Evaluation scenarios
```

## Updating Project Patterns

Replace `references/project-patterns.md` to adapt to a different project. For templates, see the `ut-coder` skill which contains `project-patterns-java-example.md`, `project-patterns-python-example.md`, and `project-patterns-typescript-example.md`.
