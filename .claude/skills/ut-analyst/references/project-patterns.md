# Project-Specific Test Patterns — HSCSimUIWin

> **Note:** This is a C#/NUnit-specific configuration for the HSCSimUIWin project. It serves as a concrete example of what a `project-patterns.md` should contain. When porting this skill to a different project or language, replace the contents of this file with your own project's conventions. See `project-patterns-java-example.md`, `project-patterns-python-example.md`, and `project-patterns-typescript-example.md` for equivalent templates in other languages.

> **Sync:** This file is replicated across `ut-analyst/references/`, `ut-architect/references/`, and `ut-coder/references/`. **This copy is the canonical source.** Update all three skill folders (and their `.cursor/skills/` mirrors) together when changing project conventions.

This reference file contains testing conventions specific to this project. The main SKILL.md is portable across projects; swap this file to adapt to a different codebase.

## Frameworks & Versions

| Library          | Version | Purpose                                                       |
| ---------------- | ------- | ------------------------------------------------------------- |
| NUnit            | 4.4.0   | Test framework                                                |
| NSubstitute      | 5.3.0   | Mocking                                                       |
| FluentAssertions | 6.12.0  | Assertion library                                             |
| .NET             | 9       | Runtime (except SetupManaged which uses .NET Framework 4.8.1) |

## Project Structure

Tests live in dedicated test projects that mirror the source project structure:

| Source Project                   | Test Project                           |
| -------------------------------- | -------------------------------------- |
| `Metso.HSC.SimUI.Windows`        | `Metso.HSC.SimUI.Windows.Tests`        |
| `Metso.HSC.SimUI.Windows.Common` | `Metso.HSC.SimUI.Windows.Common.Tests` |

Test files mirror the source folder hierarchy. If the source class is at `Services/MyService.cs`, the test file goes to `Services/MyServiceTests.cs` in the test project.

## Namespace Conventions

Use **file-scoped namespaces** (mandatory).

The namespace follows this pattern:

```csharp
// For Metso.HSC.SimUI.Windows.Tests:
namespace Metso.HSC.SimUI.Windows.Tests.[Subfolder];

// For Metso.HSC.SimUI.Windows.Common.Tests:
namespace Metso.HSC.SimUI.Windows.Common.Tests.[Subfolder];
// or
namespace Metso.HSC.SimUI.Windows.Common.Testing.[Subfolder];
```

Both `Tests` and `Testing` namespace variants exist in the codebase. Use the one that matches the test project folder path.

## Global Usings

Both test projects have a global using for NUnit.Framework in .csproj:

```xml
<Using Include="NUnit.Framework" />
```

This means **do NOT add `using NUnit.Framework;`** at the top of test files — it's already available globally. You still need explicit usings for:

```csharp
using FluentAssertions;
using FluentAssertions.Execution;  // only if using AssertionScope
using NSubstitute;                  // only if mocking
```

Plus the `using` for the namespace of the class under test.

## Nullable Annotations

Both test projects enable nullable annotations:

```xml
<Nullable>annotations</Nullable>
```

Use `null!` for late-initialized fields in test fixtures:

```csharp
private IMyService _sut = null!;
private IDependency _dependency = null!;
```

## NUnit Attributes

### Common Attributes

```csharp
[TestFixture]       // Required on every test class
[SetUp]             // Runs before each test — use for mock + SUT creation
[TearDown]          // Runs after each test — use for cleanup/dispose
[OneTimeSetUp]      // Runs once before all tests in fixture
[Test]              // Marks a test method
[TestCase(...)]     // Parameterized test — inline data
[TestCaseSource()]  // Parameterized test — data from method/property
```

### WPF-Specific Attributes

Only add these when the class under test involves WPF UI components (controls, view models that touch the dispatcher, XAML resources):

```csharp
[Apartment(ApartmentState.STA)]   // Required for WPF tests — STA thread
[NonParallelizable]                // Often paired with STA apartment
```

If the test creates or accesses `Application.Current`, add a `[OneTimeSetUp]`:

```csharp
[OneTimeSetUp]
public void OneTimeSetUp()
{
    if (Application.Current == null) { new Application(); }
}
```

## NSubstitute Patterns

### Creating Mocks

```csharp
_logger = Substitute.For<ILogger<MyClass>>();
_service = Substitute.For<IMyService>();
```

### Configuring Returns

```csharp
// Simple return
_service.GetValue().Returns("result");

// Return for any arguments
_service.Process(Arg.Any<string>()).Returns(true);

// Conditional/callback return
_service.GetItems().Returns(x => new List<Item> { new("test") });

// Return with out parameter
_service.TryGet(out Arg.Any<string>()).Returns(x =>
{
    x[0] = "value";
    return true;
});
```

### Verifying Calls

```csharp
// Verify method was called
_service.Received().DoSomething();

// Verify with specific arguments
_service.Received().Process(Arg.Is<string>(s => s.Contains("test")));

// Verify call count
_service.Received(2).DoSomething();

// Verify NOT called
_service.DidNotReceive().DoSomething();
```

## FluentAssertions Patterns

### Common Assertions

```csharp
result.Should().Be(expected);
result.Should().NotBe(unexpected);
result.Should().BeNull();
result.Should().NotBeNull();
result.Should().BeTrue();
result.Should().BeFalse();
result.Should().BeOfType<string>();
result.Should().BeApproximately(3.14, 1e-10);
```

### Collection Assertions

```csharp
list.Should().BeEmpty();
list.Should().NotBeEmpty();
list.Should().ContainSingle(x => x.Name == "test");
list.Should().HaveCount(5);
list.Should().NotContain(x => x.Name == "removed");
list.Should().Contain(x => x.Name == "added");
```

### Exception Assertions

```csharp
Action act = () => _sut.Method(null!);
act.Should().Throw<ArgumentNullException>()
    .WithParameterName("paramName");

// For async methods
Func<Task> act = () => _sut.MethodAsync(null!);
await act.Should().ThrowAsync<ArgumentNullException>();
```

### AssertionScope (Multiple Assertions)

Use `AssertionScope` to group multiple assertions so all are evaluated even if one fails:

```csharp
using FluentAssertions.Execution;

using (new AssertionScope())
{
    result.Name.Should().Be("expected");
    result.Value.Should().Be(42);
    result.IsActive.Should().BeTrue();
}
```

### WPF Binding Assertions

```csharp
result.Should().Be(System.Windows.Data.Binding.DoNothing);
```

## Test Cleanup Patterns

For tests that create temp files or external resources, always clean up:

```csharp
[Test]
public async Task MyTest_CreatesFile_CleansUp()
{
    var tempPath = Path.GetTempFileName();
    try
    {
        // Arrange & Act
        await _sut.ProcessFile(tempPath);

        // Assert
        result.Should().BeTrue();
    }
    finally
    {
        if (File.Exists(tempPath))
            File.Delete(tempPath);
    }
}
```

For services implementing `IDisposable`, use `[TearDown]`:

```csharp
[TearDown]
public void TearDown()
{
    _sut.Dispose();
}
```

## Test Helpers & Mocks

The `Metso.HSC.SimUI.Windows.Tests/Mocks/` folder contains reusable test helpers:

- `ConfigurationMock` — provides `IConfiguration` with in-memory settings
- `MessengerMock` — custom `IMessenger` implementation tracking sent messages
- `DispatcherMock` — mock WPF dispatcher for testing
- `TestServicesConfiguration` — DI container setup for integration-style tests
- `TestGlobalSetup` — NUnit global setup (assembly-level)

Use these when available. For simpler cases, `Substitute.For<T>()` is preferred.
