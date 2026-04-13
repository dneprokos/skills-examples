# Unit Test Generator Skill

A portable, multi-language skill for generating comprehensive unit tests using black-box test design techniques.

## Supported Languages

| Language        | Test Framework           | Mocking             | Assertions              |
| --------------- | ------------------------ | ------------------- | ----------------------- |
| **C#**          | NUnit 4 / xUnit / MSTest | NSubstitute / Moq   | FluentAssertions        |
| **Java**        | JUnit 5                  | Mockito             | AssertJ                 |
| **Python**      | pytest                   | unittest.mock       | plain assert / assertpy |
| **TypeScript**  | Vitest / Jest            | vi.fn() / jest.fn() | built-in + jest-dom     |
| **React (TSX)** | Vitest + Testing Library | vi.fn()             | jest-dom                |

## What It Does

When triggered, this skill generates a complete unit test file for a specified class, function, or component, applying:

- **Equivalence Partitioning** — valid, invalid, and special-value input groups
- **Boundary Value Analysis** — edge cases at domain boundaries
- **Decision Table Testing** — combinatorial input/output mapping
- **State Transition Testing** — stateful behavior verification

The generated tests use the AAA (Arrange-Act-Assert) pattern, follow a consistent naming convention (`Method_Scenario_Expected` or `should [do X] when [Y]`), and include coverage for null/empty/whitespace/default inputs, exception paths, and async methods.

## How to Use

Mention the class, function, or component you want to test:

- `Generate unit tests for MyService`
- `Create tests for the string_utils.py module`
- `Write tests for the UserList component`
- Open a source file in the editor and ask: `Write tests for this class`

The skill detects the programming language from the file extension and loads the appropriate examples. If the language is ambiguous, it will ask you before generating tests.

## Skill Structure

```
unit-test-generator/
├── SKILL.md                                       # Core instructions (language-agnostic, portable)
├── README.md                                      # This file
├── references/
│   ├── project-patterns.md                        # Active project-specific conventions (swap per repo)
│   ├── examples-csharp.md                         # C# code examples (NUnit + NSubstitute + FluentAssertions)
│   ├── examples-java.md                           # Java code examples (JUnit 5 + Mockito + AssertJ)
│   ├── examples-python.md                         # Python code examples (pytest + unittest.mock)
│   ├── examples-typescript.md                     # TypeScript/React examples (Vitest + Testing Library)
│   ├── project-patterns-java-example.md           # Java project-patterns template
│   ├── project-patterns-python-example.md         # Python project-patterns template
│   └── project-patterns-typescript-example.md    # TypeScript/React project-patterns template
└── evals/
    └── evals.json                                 # Test cases for evaluating the skill
```

## Porting to Another Project

The core `SKILL.md` and the `examples-{lang}.md` reference files are project-agnostic. To use this skill in a different codebase:

1. Copy the `unit-test-generator/` folder to the target repo's `.github/skills/` directory
2. Replace (or update) `references/project-patterns.md` with your project's testing conventions:
   - Framework versions (test framework, mocking library, assertion library)
   - Namespace / package conventions
   - Global imports already available (e.g., via `.csproj` global usings or `vitest.config.ts` globals)
   - Mock setup patterns specific to your project
   - Assertion style examples
   - File location and naming conventions
   - Any project-specific test helpers or base classes
3. Use the provided `project-patterns-{lang}-example.md` templates as a starting point for step 2
4. Keep `SKILL.md` and the `examples-*.md` files unchanged

## Adding Support for New Languages or UI Frameworks

To extend the skill to a new language or framework:

1. Create `references/examples-{lang}.md` following the same structure as the existing language files
2. Create `references/project-patterns-{lang}-example.md` as a template users can customize
3. Add a language detection entry in `SKILL.md`'s Workflow step 2 (map the file extension to the new language)

_(Angular, Vue, and other frameworks can be added this way without changing the core SKILL.md.)_

## Current Project Configuration

This instance is configured for **HSCSimUIWin** (C#/.NET) with:

| Component      | Details                        |
| -------------- | ------------------------------ |
| Test Framework | NUnit 4.4.0                    |
| Mocking        | NSubstitute 5.3.0              |
| Assertions     | FluentAssertions 6.12.0        |
| Runtime        | .NET 9                         |
| Namespaces     | File-scoped                    |
| Global Usings  | `NUnit.Framework` (in .csproj) |
