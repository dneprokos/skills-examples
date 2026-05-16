---
name: ut-coder
description: "Generate a complete, compilable unit test file from an Analyst test plan and Architect strategy. Uses AAA pattern, language-specific frameworks (NUnit, JUnit 5, pytest, Vitest), correct mock/real dependency instantiation, constructor null-guard tests, parameterized tests, and setup/teardown hooks. Input is the Analyst JSON plan plus Architect strategy summary. Use when asked to generate test code, write test implementation, create test file, or implement tests from a plan. Also invoked as Phase 3 by the unit-test-generator agent."
argument-hint: "paste Analyst JSON plan and Architect strategy summary"
---

# Unit Test Coder

Generate the complete, compilable test file using the Analyst's test plan and the Architect's strategy decisions. This is Phase 3 of the unit test generation pipeline.

> **Standalone vs. orchestrated** — This skill can run independently given both a JSON test plan (from `ut-analyst`) and an Architect strategy summary (from `ut-architect`), or it can be invoked as Phase 3 by the `unit-test-generator` agent, which passes both outputs directly.

## Input

Both of the following are required:

1. **Analyst JSON test plan** — produced by `ut-analyst` (Phase 1). Provides the list of methods, test cases, dependency classifications, null-guard requirements, and non-deterministic call warnings.
2. **Architect strategy summary** — produced by `ut-architect` (Phase 2). Provides the mock/real assignment per dependency, the test file path, assertion style, null-guard exception types, and abstraction interfaces for non-deterministic calls.

If either input is missing, respond with:

> Please provide both the Analyst JSON test plan and the Architect strategy summary. Run `/ut-analyst` then `/ut-architect` first.

## Preparation

1. **Read language-specific examples** — load the reference file matching the language in the Analyst plan:
   - [`references/examples-csharp.md`](references/examples-csharp.md) for C#
   - [`references/examples-java.md`](references/examples-java.md) for Java
   - [`references/examples-python.md`](references/examples-python.md) for Python
   - [`references/examples-typescript.md`](references/examples-typescript.md) for TypeScript / React
2. **Read [`references/project-patterns.md`](references/project-patterns.md)** — load the project-specific conventions (framework versions, namespace format, global usings, mock patterns). If the file doesn't exist or doesn't match the detected language, check for a matching `references/project-patterns-{lang}-example.md` as a starting template.

## Coder Actions

1. **Mirror the source file's folder structure** in the test directory following `project-patterns.md` conventions. Use the exact test file path from the Architect strategy.
2. **Use real instances** for all dependencies classified as `real` — never mock them
3. **Mock** all dependencies classified as `mock` using the project's mocking library
4. **Inject abstractions** for non-deterministic calls as specified by the Architect and mock those abstractions
5. **Write all test cases** from the Analyst JSON plan, including constructor null-guard tests
6. **Follow the output format rules** and language examples from the loaded reference file

## Output Format

Generate a complete, compilable (or runnable) test file. Follow these structural rules — language-specific syntax and code examples are in the loaded `references/examples-{lang}.md` file.

### File Structure

Mirror the source file's folder structure in the test directory. The test file name follows the language convention (e.g., `MyClassTests.cs`, `MyClassTest.java`, `test_my_class.py`, `MyClass.test.ts`). Follow the exact structure shown in the language reference file.

### Naming Convention

Test names communicate intent without needing to read the test body. The general pattern is:

```
[MethodUnderTest] / [scenario description] / [expected outcome]
```

The separator style varies by language — underscores for C# and Java, descriptive strings for Python and TypeScript. Examples and exact conventions are in the language reference file. Either style can use:

- `WithValidInput` / `NullArgument` / `WhenAlreadyInitialized` for scenarios
- `ReturnsExpectedResult` / `ThrowsArgumentNullException` / `CallsDependencyOnce` for outcomes

### AAA Pattern

Every test uses Arrange-Act-Assert with inline comments marking each section. For very short tests where one section is trivial, combined labels (`// Arrange & Act`, `// Act & Assert`) are acceptable — match the style of the surrounding codebase.

### Parameterized Tests

When multiple inputs exercise the same logic with different values, use the language's parameterized test feature rather than duplicating test methods. Keep each case data-only; the test body should be identical across cases. See the language reference for the exact attribute or decorator syntax.

### Setup and Teardown

Create mocks for all constructor-injected dependencies and instantiate the system-under-test (SUT) in the before-each hook. If cleanup is needed (open resources, temp files), use the after-each hook. See the language reference for the exact hook syntax.

### Grouping

Group tests by the method or behaviour being tested using the language's grouping mechanism (regions, nested classes, or nested describe blocks). For classes with only one or two public methods, grouping is usually unnecessary. See the language reference for the preferred grouping pattern.

## Output Checklist

Before finishing, verify each item:

- [ ] Test file is in the correct location mirroring the source structure
- [ ] AAA pattern used consistently with section labels
- [ ] Happy path cases covered for every public method
- [ ] Edge cases identified and tested (null, empty, boundaries, special values)
- [ ] Error cases tested — exceptions verified with type and message
- [ ] Async methods tested with proper async/await
- [ ] Behavioral interfaces mocked; Value Objects and DTOs use real instances
- [ ] Constructor null-guard test generated for every interface/abstract constructor parameter
- [ ] Non-deterministic calls handled via injected abstractions (not called directly)
- [ ] Interactions verified where the call itself is part of the contract
- [ ] Test names are descriptive and self-documenting
- [ ] Setup / teardown hooks used appropriately
- [ ] Parameterized tests used where multiple cases share the same logic

## What NOT to Do

- Don't test private / internal methods directly — test them through the public API
- Don't create tests that depend on each other or share mutable state between tests
- Don't add excessive comments explaining obvious things — the test name should be self-documenting
- Don't mock concrete classes — only mock interfaces or abstract types
- **Don't mock Value Objects, DTOs, records, or data classes** — construct real instances instead
- **Don't skip constructor null-guard tests** — every interface/abstract constructor parameter must be tested with null
- Don't import the test framework explicitly if the project uses a global import config — check `references/project-patterns.md` for what's already globally available
- Don't force all four design techniques onto every method — follow the techniques in the Analyst plan
- Don't change dependency classifications or mock assignments — follow the Architect strategy as given
- Check the loaded language reference file for additional language-specific anti-patterns
