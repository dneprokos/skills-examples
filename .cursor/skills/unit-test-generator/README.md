# Unit Test Generator Skill

A portable skill for generating comprehensive C# unit tests using black-box test design techniques.

## What It Does

When triggered, this skill generates a complete unit test file for a specified C# class, applying:

- **Equivalence Partitioning** — valid, invalid, and special-value input groups
- **Boundary Value Analysis** — edge cases at domain boundaries
- **Decision Table Testing** — combinatorial input/output mapping
- **State Transition Testing** — stateful behavior verification

The generated tests use the AAA (Arrange-Act-Assert) pattern, follow a consistent naming convention (`Method_Scenario_Expected`), and include coverage for null/empty/whitespace/default inputs, exception paths, and async methods.

## How to Use

Mention the class you want to test:

- `Generate unit tests for MyService`
- `Create tests for the StringExtensions class`
- Open a class file in the editor and ask: `Write tests for this class`

The skill will refuse to generate tests if no class is specified or visible in context, and will ask you to provide one.

## Skill Structure

```
unit-test-generator/
├── SKILL.md                          # Core instructions (portable)
├── README.md                         # This file
├── references/
│   └── project-patterns.md           # Project-specific conventions (swap per repo)
└── evals/
    └── evals.json                    # Test cases for evaluating the skill
```

## Porting to Another Project

The core `SKILL.md` is project-agnostic. To use this skill in a different C# codebase:

1. Copy the `unit-test-generator/` folder to the target repo's `.github/skills/` directory
2. Replace `references/project-patterns.md` with your project's testing conventions:
   - Framework versions (NUnit/xUnit/MSTest, mocking library, assertion library)
   - Namespace patterns
   - Global usings
   - Mock setup patterns
   - Assertion style examples
   - File location conventions
   - Any project-specific test helpers
3. Keep `SKILL.md` unchanged — it references the patterns file automatically

## Current Project Configuration

This instance is configured for **HSCSimUIWin** with:

| Component      | Details                        |
| -------------- | ------------------------------ |
| Test Framework | NUnit 4.4.0                    |
| Mocking        | NSubstitute 5.3.0              |
| Assertions     | FluentAssertions 6.12.0        |
| Runtime        | .NET 9                         |
| Namespaces     | File-scoped                    |
| Global Usings  | `NUnit.Framework` (in .csproj) |
