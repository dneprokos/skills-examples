---
name: ut-architect
description: "Define the mocking strategy and assertion style for a unit test plan. Classifies each dependency as mock or real, resolves assertion framework and test file location from project patterns, lists constructor null-guard tests with expected exception types, and specifies abstraction interfaces for non-deterministic calls. Input is a JSON test plan from ut-analyst. Use when asked to define mocking strategy, plan test architecture, classify dependencies as mock vs real, or design test structure. Also invoked as Phase 2 by the unit-test-generator agent."
argument-hint: "paste Analyst JSON test plan"
---

# Unit Test Architect

Define the mocking strategy, assertion style, and test structure from the Analyst's dependency classification. This is Phase 2 of the unit test generation pipeline.

> **Standalone vs. orchestrated** — This skill can run independently given a JSON test plan produced by `ut-analyst`, or it can be invoked as Phase 2 by the `unit-test-generator` agent, which passes the Analyst's output directly.

## Input

A JSON test plan produced by the `ut-analyst` skill (Phase 1). The plan must include:

- `dependencies[]` with `classification` set for every entry
- `constructorNullGuards[]` listing interface/abstract constructor parameters
- `nonDeterministicCalls[]` if any were detected
- `language` and `testFilePath`

If no JSON plan is provided and the user has not run Phase 1, respond with:

> Please provide the Analyst JSON test plan first. Run `/ut-analyst` on your source class to generate it, then paste the output here.

## Preparation

1. **Read [`references/project-patterns.md`](references/project-patterns.md)** — load the active project's test framework, assertion library, null-exception convention, and test file path rules. This determines assertion style (e.g., FluentAssertions vs. AssertJ vs. plain assert) and the exact exception type to expect in null-guard tests.

## Architect Actions

### 1. Assign Mock Strategy

For each dependency in the plan:

| Classification | Strategy | Rationale |
|---|---|---|
| `interface` | `mock` | Behavioral contract — must be isolated |
| `abstract` | `mock` | Behavioral contract — must be isolated |
| `valueObject` | `real` | Immutable data — real instances are simpler and more accurate |
| `dto` | `real` | Data container — construct with real values |
| `primitive` | `real` | Value type — no isolation needed |

**Rule:** Never mock Value Objects, DTOs, records, data classes, or primitives. Construct real instances. This is mandatory and overrides any other guidance.

### 2. Resolve Test File Location

Use `references/project-patterns.md` to determine:
- The exact test project name and folder structure
- Whether the file mirrors the source folder hierarchy
- The test file naming convention (`MyClassTests.cs`, `MyClassTest.java`, `test_my_class.py`, `MyClass.test.ts`)

### 3. List Constructor Null-Guard Tests

For each entry in `constructorNullGuards[]`:
- Confirm the expected exception type matches the project's language convention (from `project-patterns.md`)
- List the parameter name alongside its expected exception

Language defaults if not specified in `project-patterns.md`:

| Language | Null exception |
|---|---|
| C# | `ArgumentNullException` |
| Java | `NullPointerException` |
| Python | `TypeError` or `ValueError` |
| TypeScript | `TypeError` |

### 4. Specify Abstractions for Non-Deterministic Calls

For each entry in `nonDeterministicCalls[]`, specify:
- The abstraction interface to inject (e.g., `IDateTimeProvider`)
- That the abstraction will be classified as `interface` → `mock`
- The mock should return a fixed, predictable value in tests

## Output

Emit a concise strategy summary:

```
## Architect Strategy
- Mocked: [IRepository, IEmailService, IDateTimeProvider]
- Real instances: [Address, Money, CreateUserDto]
- Constructor null-guards: [repository → ArgumentNullException("repository"), emailService → ArgumentNullException("emailService")]
- Non-deterministic abstractions: [DateTime.UtcNow → inject IDateTimeProvider → mock with fixed DateTimeOffset]
- Test file: [path/to/MyClassTests.cs]
- Assert style: FluentAssertions (.Should())
```

**If running standalone (not `skipReview: true`):** After emitting the summary, stop and ask:

> _"Architect phase complete. Review the strategy above. Reply 'continue' to generate the test code, or provide feedback to adjust."_

**If `skipReview: true`** (passed by user or orchestrator): Emit the summary and continue without pausing.

## What NOT to Do

- Don't enumerate test cases — that is the Analyst's responsibility
- Don't generate any test code — that is the Coder's responsibility
- Don't mock concrete classes — only interfaces and abstract types
- **Don't mock Value Objects, DTOs, records, or data classes** — construct real instances instead
- **Don't skip constructor null-guard tests** — every interface/abstract constructor parameter must be listed
- Don't override dependency classifications set by the Analyst — work from the plan as provided
