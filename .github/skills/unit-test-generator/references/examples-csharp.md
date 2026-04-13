# C# Unit Test Examples — NUnit + NSubstitute + FluentAssertions

This file contains C#-specific code patterns and examples for the unit-test-generator skill. The project-specific settings (framework versions, namespace format, global usings) live in `project-patterns.md` — read that file alongside this one.

## File Structure

```csharp
using FluentAssertions;
using NSubstitute;
// ... other usings for the namespace under test

namespace MyProject.Tests.Services;

[TestFixture]
public class MyServiceTests
{
    private IMyDependency _dependency = null!;
    private MyService _sut = null!;

    [SetUp]
    public void SetUp()
    {
        _dependency = Substitute.For<IMyDependency>();
        _sut = new MyService(_dependency);
    }

    #region MethodA Tests

    [Test]
    public void MethodA_WithValidInput_ReturnsExpectedResult()
    {
        // ...
    }

    #endregion

    #region MethodB Tests

    [Test]
    public void MethodB_NullInput_ThrowsArgumentNullException()
    {
        // ...
    }

    #endregion
}
```

Key rules:

- Use **file-scoped namespaces** (no braces around the namespace — see `project-patterns.md` for the exact namespace pattern)
- Declare fields as `null!` for late-initialized fields (nullable annotations are enabled)
- Do **not** add `using NUnit.Framework;` — it is globally available (see `project-patterns.md`)
- Use `#region [MethodName] Tests` / `#endregion` to group tests when the class has more than two public methods
- For a class with only one or two public methods, omit `#region` blocks

## Naming Convention

Pattern: `[MethodUnderTest]_[Scenario]_[ExpectedOutcome]`

```
GetValue_WithValidInput_ReturnsExpectedResult
Initialize_WhenAlreadyInitialized_ThrowsInvalidOperationException
AddItem_NullInput_ThrowsArgumentNullException
Calculate_BoundaryMaxValue_ReturnsMaxResult
ProcessAsync_ServiceThrowsException_PropagatesException
GetItems_EmptyCollection_ReturnsEmptyList
Connect_WhenAlreadyConnected_CallsDependencyOnce
```

## AAA Pattern

```csharp
[Test]
public void MethodName_Scenario_ExpectedOutcome()
{
    // Arrange
    var input = "test";
    _dependency.GetValue().Returns("mocked");

    // Act
    var result = _sut.MethodName(input);

    // Assert
    result.Should().Be("expected");
}
```

For trivial arrange steps, `// Arrange & Act` or `// Act & Assert` combined labels are acceptable:

```csharp
[Test]
public void IsValid_EmptyString_ReturnsFalse()
{
    // Act & Assert
    _sut.IsValid(string.Empty).Should().BeFalse();
}
```

## Parameterized Tests

Use `[TestCase]` for inline data. Use `ExpectedResult` when the return value is the assertion:

```csharp
[TestCase("valid1", ExpectedResult = true)]
[TestCase("valid2", ExpectedResult = true)]
[TestCase("", ExpectedResult = false)]
[TestCase(null, ExpectedResult = false)]
[TestCase("   ", ExpectedResult = false)]
public bool IsValid_VariousInputs_ReturnsExpected(string? input)
{
    return _sut.IsValid(input);
}
```

For more complex multi-parameter cases use `[TestCase]` with explicit assertion:

```csharp
[TestCase(0, 1, 0)]
[TestCase(1, 1, 1)]
[TestCase(5, 3, 15)]
[TestCase(-2, 4, -8)]
public void Multiply_VariousInputs_ReturnsProduct(int a, int b, int expected)
{
    // Act
    var result = _sut.Multiply(a, b);

    // Assert
    result.Should().Be(expected);
}
```

For complex objects or long datasets, prefer `[TestCaseSource]`:

```csharp
private static IEnumerable<TestCaseData> InvalidInputCases()
{
    yield return new TestCaseData(null).SetName("NullInput");
    yield return new TestCaseData("").SetName("EmptyString");
    yield return new TestCaseData("   ").SetName("WhitespaceOnly");
}

[TestCaseSource(nameof(InvalidInputCases))]
public void Process_InvalidInput_ThrowsArgumentException(string? input)
{
    // Act
    var act = () => _sut.Process(input);

    // Assert
    act.Should().Throw<ArgumentException>();
}
```

## SetUp — Mocking Pattern (NSubstitute)

```csharp
[SetUp]
public void SetUp()
{
    _repository = Substitute.For<IUserRepository>();
    _emailService = Substitute.For<IEmailService>();
    _sut = new UserService(_repository, _emailService);
}
```

Verify that a dependency was called:

```csharp
_emailService.Received(1).SendWelcomeEmail(Arg.Any<string>());
```

Verify a dependency was NOT called:

```csharp
_emailService.DidNotReceive().SendWelcomeEmail(Arg.Any<string>());
```

Configure a return value:

```csharp
_repository.GetByIdAsync(userId).Returns(Task.FromResult<User?>(existingUser));
```

Configure a thrown exception:

```csharp
_repository.GetByIdAsync(Arg.Any<int>()).Throws(new DatabaseException("connection lost"));
```

## Exception Assertions (FluentAssertions)

```csharp
[Test]
public void AddItem_NullItem_ThrowsArgumentNullException()
{
    // Act
    var act = () => _sut.AddItem(null);

    // Assert
    act.Should().Throw<ArgumentNullException>()
       .WithParameterName("item");
}

[Test]
public void Initialize_AlreadyInitialized_ThrowsInvalidOperationException()
{
    // Arrange
    _sut.Initialize();

    // Act
    var act = () => _sut.Initialize();

    // Assert
    act.Should().Throw<InvalidOperationException>()
       .WithMessage("*already initialized*");
}
```

## Async Test Pattern

Test methods for async methods must be `async Task`:

```csharp
[Test]
public async Task GetUserAsync_ValidId_ReturnsUser()
{
    // Arrange
    var userId = 42;
    var expected = new User { Id = userId, Name = "Alice" };
    _repository.GetByIdAsync(userId).Returns(Task.FromResult<User?>(expected));

    // Act
    var result = await _sut.GetUserAsync(userId);

    // Assert
    result.Should().BeEquivalentTo(expected);
}

[Test]
public async Task GetUserAsync_UserNotFound_ThrowsNotFoundException()
{
    // Arrange
    _repository.GetByIdAsync(Arg.Any<int>()).Returns(Task.FromResult<User?>(null));

    // Act
    var act = async () => await _sut.GetUserAsync(99);

    // Assert
    await act.Should().ThrowAsync<NotFoundException>();
}
```

## Verifying Collections (FluentAssertions)

```csharp
result.Should().HaveCount(3);
result.Should().Contain(x => x.Name == "Alice");
result.Should().BeEquivalentTo(expected, options => options.WithStrictOrdering());
result.Should().BeEmpty();
result.Should().NotBeEmpty();
```

## WPF-Specific Attributes

Only add these when the class requires STA thread (WPF controls, dispatcher access):

```csharp
[TestFixture]
[Apartment(ApartmentState.STA)]
[NonParallelizable]
public class MyViewModelTests
{
    // ...
}
```

If the test creates or accesses `Application.Current`:

```csharp
[OneTimeSetUp]
public void OneTimeSetUp()
{
    if (Application.Current == null)
        _ = new Application();
}
```

## C#-Specific Anti-Patterns

- **Don't add** `using NUnit.Framework;` — it's globally available via the `.csproj` global usings (check `project-patterns.md`)
- **Don't add** `[Apartment(ApartmentState.STA)]` unless the SUT involves WPF UI components
- **Don't use** `Assert.That(...)` or `Assert.AreEqual(...)` — use FluentAssertions (`.Should()`) consistently
- **Don't mock** `string`, `int`, or other value types / concrete sealed classes — only mock interfaces
- **Don't use** `[TearDown]` for mock verification — NSubstitute's `Received()`/`DidNotReceive()` assertions in the test body are cleaner
- **Don't write** `var result = await Task.Run(() => _sut.SyncMethod())` to test synchronous code — call synchronous methods directly
