---
name: unit-test-generator
description: "Generate comprehensive C# unit tests for a given class using black-box test design techniques (Equivalence Partitioning, Boundary Value Analysis, Decision Table, State Transition). ALWAYS use this skill when the user asks to generate unit tests, create tests, write tests for a class, test a class, or mentions #prompt:UnitTests. Also use when the user says things like 'add tests for X', 'cover X with tests', 'I need tests for this', or 'test this'. Even if the user doesn't say 'unit test' explicitly — if they want test code for a C# class, use this skill."
---

# Unit Test Generator

Generate comprehensive, high-quality unit tests for C# classes using black-box test design techniques.

## Prerequisites: Class Context Check

Before generating any tests, verify that you have a target class to test. You need one of these:

1. The user specified a class name (e.g., "generate tests for `MyService`")
2. A class file is open in the editor or attached to the conversation
3. The user referenced a class in the conversation history

**If none of these are true**, respond with:

> Please specify the class you want to create unit tests for. You can either:
>
> - Provide the class name (e.g., "generate tests for `MyService`")
> - Open the class file in the editor
> - Attach the class file to the conversation

Do not generate tests without a concrete target class.

## Workflow

Once you have the target class:

1. **Read the source class** — understand all public methods, constructors, properties, dependencies (constructor-injected interfaces), and edge cases
2. **Read `references/project-patterns.md`** — load the project-specific testing conventions (frameworks, namespace format, mock patterns, assertion style). This file is the only part that changes between projects — the rest of this skill is portable.
3. **Identify the test file location** — mirror the source file's folder structure in the corresponding `Tests` project
4. **Design test cases** using black-box techniques (see below)
5. **Generate the complete test file** following the output format rules

## Black-Box Test Design Techniques

Apply these techniques systematically to every public method in the class:

### Equivalence Partitioning

Divide input domains into groups that should behave the same way. Write at least one test per partition. Typical partitions include: valid inputs, invalid inputs, boundary-adjacent values, and special values (null, empty, zero, negative).

### Boundary Value Analysis

Test at the exact boundaries of input domains. For a range `[min, max]`, test: `min-1`, `min`, `min+1`, `max-1`, `max`, `max+1`. For strings: empty string, single char, very long string. For collections: empty, single item, many items.

### Decision Table Testing

When a method's behavior depends on combinations of conditions, enumerate the meaningful combinations. Each unique combination of inputs that produces a distinct outcome gets its own test case. Use `[TestCase]` or `[TestCaseSource]` to keep these compact.

### State Transition Testing

When the class has internal state that affects behavior (e.g., initialization state, connection status, mode flags), test:

- Each valid state transition
- Invalid transitions (calling methods in wrong order/state)
- The behavior of the same method in different states

Not every technique applies to every method — use judgment. A simple utility method might only need Equivalence Partitioning and Boundary Value Analysis. A stateful service might need all four.

## Test Case Coverage Requirements

For each public method, ensure coverage of:

- **Valid inputs** — happy path with typical values
- **Invalid inputs** — wrong types, out-of-range, malformed
- **Edge cases** — null, empty string, whitespace, default values, zero, negative numbers, max/min values
- **Exception paths** — verify that expected exceptions are thrown with correct messages/parameter names
- **Async methods** — use `async Task` test methods with `await`
- **Dependencies** — mock all constructor-injected interfaces; verify interactions where meaningful

## Output Format

Generate a complete, compilable test file. Follow these structural rules:

### File Structure

```
[Using statements]
[blank line]
[File-scoped namespace];
[blank line]
[TestFixture attribute]
public class [ClassName]Tests
{
    [Private fields for SUT and mocks]
    [blank line]
    [SetUp method]
    [blank line]
    [Test methods grouped by method-under-test, separated by #region]
}
```

### Naming Convention

Test methods follow this pattern: `[MethodUnderTest]_[Scenario]_[ExpectedOutcome]`

Examples:

- `GetValue_WithValidInput_ReturnsExpectedResult`
- `Initialize_WhenAlreadyInitialized_ThrowsInvalidOperationException`
- `AddItem_NullInput_ThrowsArgumentNullException`
- `Calculate_BoundaryMaxValue_ReturnsMaxResult`

### AAA Pattern

Every test method uses Arrange-Act-Assert with comments:

```csharp
[Test]
public void MethodName_Scenario_ExpectedOutcome()
{
    // Arrange
    var input = "test";

    // Act
    var result = _sut.MethodName(input);

    // Assert
    result.Should().Be("expected");
}
```

For very short tests where Arrange is trivial, `// Arrange & Act` or `// Act & Assert` is acceptable (matching existing codebase style).

### Parameterized Tests

When testing multiple inputs with the same logic, prefer `[TestCase]` over duplicate test methods:

```csharp
[TestCase("valid1", ExpectedResult = true)]
[TestCase("valid2", ExpectedResult = true)]
[TestCase("", ExpectedResult = false)]
[TestCase(null, ExpectedResult = false)]
public bool IsValid_VariousInputs_ReturnsExpected(string input)
{
    return _sut.IsValid(input);
}
```

For complex test data, use `[TestCaseSource]` with a static method or property.

### SetUp Method

Create mocks for all constructor-injected dependencies in `[SetUp]` and instantiate the system-under-test (SUT):

```csharp
[SetUp]
public void SetUp()
{
    _dependency = Substitute.For<IDependency>();
    _sut = new MyClass(_dependency);
}
```

### Regions

Group tests by the method they're testing using `#region` blocks when the class has multiple public methods:

```csharp
#region MethodA Tests
// tests for MethodA
#endregion

#region MethodB Tests
// tests for MethodB
#endregion
```

For classes with only one or two public methods, `#region` blocks are unnecessary.

## What NOT to Do

- Don't test private methods directly — test them through the public API
- Don't create tests that depend on each other or share mutable state
- Don't add excessive comments explaining obvious things — the test name should be self-documenting
- Don't mock concrete classes — only mock interfaces
- Don't add `[Apartment(ApartmentState.STA)]` or `[NonParallelizable]` unless the class under test involves WPF UI components (check `references/project-patterns.md` for when these are needed)
- Don't import `NUnit.Framework` explicitly if the project has a global using for it (check `references/project-patterns.md`)
