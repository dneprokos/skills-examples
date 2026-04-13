---
name: unit-test-generator
description: "Generate comprehensive unit tests for a given class or module using black-box test design techniques (Equivalence Partitioning, Boundary Value Analysis, Decision Table, State Transition). Supports C#, Java, Python, and TypeScript/React. ALWAYS use this skill when the user asks to generate unit tests, create tests, write tests for a class or function, test a class, or mentions #prompt:UnitTests. Also use when the user says things like 'add tests for X', 'cover X with tests', 'I need tests for this', or 'test this'. Even if the user doesn't say 'unit test' explicitly — if they want test code for any class, function, or component in a supported language, use this skill."
---

# Unit Test Generator

Generate comprehensive, high-quality unit tests using black-box test design techniques. This skill supports C#, Java, Python, and TypeScript/React — it adapts to whichever language your project uses.

## Prerequisites: Class Context Check

Before generating any tests, verify that you have a target class, function, or component to test. You need one of these:

1. The user specified a name (e.g., "generate tests for `MyService`")
2. A source file is open in the editor or attached to the conversation
3. The user referenced a class or function in the conversation history

**If none of these are true**, respond with:

> Please specify the class or function you want to create unit tests for. You can either:
>
> - Provide the name (e.g., "generate tests for `MyService`")
> - Open the source file in the editor
> - Attach the source file to the conversation

Do not generate tests without a concrete target.

## Workflow

Once you have the target:

1. **Read the source file** — understand all public methods, constructors, properties, dependencies (constructor-injected interfaces or function parameters), and edge cases
2. **Detect the programming language** — use the file extension or explicit user context:
   - `.cs` → C# | `.java` → Java | `.py` → Python | `.ts` / `.tsx` → TypeScript
   - If the language is ambiguous, ask the user before proceeding
3. **Read `references/examples-{lang}.md`** — load the language-specific code examples and patterns. Use:
   - [`references/examples-csharp.md`](references/examples-csharp.md) for C#
   - [`references/examples-java.md`](references/examples-java.md) for Java
   - [`references/examples-python.md`](references/examples-python.md) for Python
   - [`references/examples-typescript.md`](references/examples-typescript.md) for TypeScript / React
4. **Read `references/project-patterns.md`** — load the project-specific conventions (framework versions, namespace format, mock patterns, assertion style). This is the file that changes per-project; the rest of this skill is portable. If the file doesn't exist or doesn't match the detected language, check for a matching `references/project-patterns-{lang}-example.md` as a starting template.
5. **Identify the test file location** — mirror the source file's folder structure in the test directory following the conventions in `project-patterns.md`
6. **Design test cases** using black-box techniques (see below)
7. **Generate the complete test file** following the output format rules and the examples in the loaded language reference

## Black-Box Test Design Techniques

Apply these techniques systematically to every public method or exported function:

### Equivalence Partitioning

Divide input domains into groups that should behave the same way. Write at least one test per partition. Typical partitions include: valid inputs, invalid inputs, boundary-adjacent values, and special values (null, empty, zero, negative).

### Boundary Value Analysis

Test at the exact boundaries of input domains. For a range `[min, max]`, test: `min-1`, `min`, `min+1`, `max-1`, `max`, `max+1`. For strings: empty string, single char, very long string. For collections: empty, single item, many items.

### Decision Table Testing

When a method's behavior depends on combinations of conditions, enumerate the meaningful combinations. Each unique combination of inputs that produces a distinct outcome gets its own test case. Use the language's parameterized test feature to keep these compact.

### State Transition Testing

When the class has internal state that affects behavior (e.g., initialization state, connection status, mode flags), test:

- Each valid state transition
- Invalid transitions (calling methods in wrong order/state)
- The behavior of the same method in different states

Not every technique applies to every method — use judgment. A simple utility method might only need Equivalence Partitioning and Boundary Value Analysis. A stateful service might need all four.

## Test Case Coverage Requirements

For each public method or exported function, cover all three categories:

### Happy Path

- Typical valid inputs that produce the expected successful outcome
- Cover the most common use cases a real caller would exercise

### Edge Cases

- `null` / `None` / `undefined` inputs
- Empty string, empty collection, empty object
- Whitespace-only strings
- Zero, negative numbers, very large numbers, `NaN`, `Infinity`
- Default / zero-value objects
- Single-element collections
- Very long strings or collections (near limits)

### Error Cases

- Invalid input values (wrong type, out of range, malformed)
- Missing required dependencies or resource not found
- Expected exceptions — verify the exception type, message, and parameter name where applicable
- Async methods must test both resolved and rejected/thrown paths

For async methods, always write async test methods that properly `await` the call. For dependencies, mock all injected interfaces and verify interactions where the interaction itself is part of the contract.

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
- [ ] Mocks used for all injected dependencies
- [ ] Interactions verified where the call itself is part of the contract
- [ ] Test names are descriptive and self-documenting
- [ ] Setup / teardown hooks used appropriately
- [ ] Parameterized tests used where multiple cases share the same logic

## What NOT to Do

- Don't test private / internal methods directly — test them through the public API
- Don't create tests that depend on each other or share mutable state between tests
- Don't add excessive comments explaining obvious things — the test name should be self-documenting
- Don't mock concrete classes — only mock interfaces or abstract types
- Don't import the test framework explicitly if the project uses a global import config — check `references/project-patterns.md` for what's already globally available
- Don't force all four design techniques onto every method — a simple pure function may only need EP and BVA
- Check the loaded language reference file for additional language-specific anti-patterns
