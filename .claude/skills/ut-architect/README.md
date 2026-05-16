# Unit Test Architect Skill

Defines the mocking strategy and test structure as **Phase 2** of the unit test generation pipeline.

## What It Does

Given a JSON test plan from `ut-analyst`, this skill:

1. **Assigns mock strategy to every dependency** — interfaces/abstracts → mock; value objects/DTOs/primitives → real
2. **Resolves assertion style and test file location** from `references/project-patterns.md`
3. **Lists constructor null-guard tests** with expected exception type per parameter
4. **Specifies abstraction interfaces** for non-deterministic calls that must be injected and mocked

## Output

A concise strategy summary consumed by `ut-coder` in Phase 3:

```
## Architect Strategy
- Mocked: [IRepository, IEmailService]
- Real instances: [Address, Money, CreateUserDto]
- Constructor null-guards: [repository → ArgumentNullException("repository"), ...]
- Non-deterministic abstractions: [DateTime.UtcNow → inject IDateTimeProvider]
- Test file: [path/to/MyClassTests.cs]
- Assert style: FluentAssertions (.Should())
```

## How to Use

### Standalone

Trigger with `/ut-architect` and provide the Analyst JSON:

```
/ut-architect [paste JSON test plan from ut-analyst]
```

### As Part of the Pipeline

The `unit-test-generator` agent invokes this skill automatically as Phase 2, passing the Analyst's JSON output directly.

### Passing Output to Coder

When running standalone, copy the strategy summary and provide it alongside the Analyst JSON to `ut-coder`:

```
/ut-coder [Analyst JSON] + [Architect strategy]
```

## Skill Structure

```
ut-architect/
├── SKILL.md                  # Core instructions (this skill)
├── README.md                 # This file
├── references/
│   └── project-patterns.md  # Active project conventions (swap per repo)
└── evals/
    └── evals.json            # Evaluation scenarios
```

## Updating Project Patterns

Replace `references/project-patterns.md` to adapt to a different project. For templates, see the `ut-coder` skill which contains `project-patterns-java-example.md`, `project-patterns-python-example.md`, and `project-patterns-typescript-example.md`.
