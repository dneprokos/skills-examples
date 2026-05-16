# Unit Test Coder Skill

Generates a complete, compilable unit test file as **Phase 3** of the unit test generation pipeline.

## What It Does

Given an Analyst JSON test plan and an Architect strategy summary, this skill:

1. **Generates a complete test file** — compilable (or runnable) from the first line
2. **Applies language-specific patterns** — from `references/examples-{lang}.md`
3. **Creates real instances** for value objects, DTOs, and primitives; **mocks** interfaces and abstracts
4. **Injects and mocks abstractions** replacing non-deterministic calls (time, random, UUIDs)
5. **Writes constructor null-guard tests** for every interface/abstract constructor parameter
6. **Follows AAA pattern** with inline section comments in every test
7. **Uses parameterized tests** where multiple cases share the same logic
8. **Sets up before-each hooks** for mock creation and SUT instantiation

## Supported Languages

| Language        | Test Framework           | Mocking             | Assertions              |
| --------------- | ------------------------ | ------------------- | ----------------------- |
| **C#**          | NUnit 4 / xUnit / MSTest | NSubstitute / Moq   | FluentAssertions        |
| **Java**        | JUnit 5                  | Mockito             | AssertJ                 |
| **Python**      | pytest                   | unittest.mock       | plain assert / assertpy |
| **TypeScript**  | Vitest / Jest            | vi.fn() / jest.fn() | built-in + jest-dom     |
| **React (TSX)** | Vitest + Testing Library | vi.fn()             | jest-dom                |

## How to Use

### Standalone

Trigger with `/ut-coder` and provide both inputs:

```
/ut-coder
[paste Analyst JSON plan]
[paste Architect strategy summary]
```

### As Part of the Pipeline

The `unit-test-generator` agent invokes this skill automatically as Phase 3, passing the Analyst plan and Architect strategy directly.

## Skill Structure

```
ut-coder/
├── SKILL.md                                     # Core instructions (this skill)
├── README.md                                    # This file
├── references/
│   ├── project-patterns.md                      # Active project conventions (swap per repo)
│   ├── examples-csharp.md                       # C# code examples (NUnit + NSubstitute + FluentAssertions)
│   ├── examples-java.md                         # Java code examples (JUnit 5 + Mockito + AssertJ)
│   ├── examples-python.md                       # Python code examples (pytest + unittest.mock)
│   ├── examples-typescript.md                   # TypeScript/React examples (Vitest + Testing Library)
│   ├── project-patterns-java-example.md         # Java project-patterns template
│   ├── project-patterns-python-example.md       # Python project-patterns template
│   └── project-patterns-typescript-example.md  # TypeScript project-patterns template
└── evals/
    └── evals.json                               # Evaluation scenarios
```

## Updating Project Patterns

Replace `references/project-patterns.md` to adapt to a different project. Use the `project-patterns-{lang}-example.md` templates as starting points for Java, Python, or TypeScript projects.
