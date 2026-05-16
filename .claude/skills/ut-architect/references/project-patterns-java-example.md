# Project-Specific Test Patterns — Java Template

> **How to use this file:** Copy this template to `project-patterns.md` in your `ut-architect/references/` directory and fill in the values for your actual project. Delete any sections that don't apply. The Architect reads this file to determine assertion style, test file location, and the null-guard exception type for constructor parameters.

## Frameworks & Versions

| Library    | Version        | Purpose               |
| ---------- | -------------- | --------------------- |
| JUnit      | 5.x            | Test framework        |
| Mockito    | 5.x            | Mocking               |
| AssertJ    | 3.x            | Assertion library     |
| Java       | 17 / 21        | Runtime               |
| Build tool | Maven / Gradle | Build and test runner |

_Replace with your actual versions._

## Project Structure

Tests live under `src/test/java/` and mirror the source package structure under `src/main/java/`.

| Source                                                | Test                                                      |
| ----------------------------------------------------- | --------------------------------------------------------- |
| `src/main/java/com/example/services/UserService.java` | `src/test/java/com/example/services/UserServiceTest.java` |
| `src/main/java/com/example/utils/StringUtils.java`    | `src/test/java/com/example/utils/StringUtilsTest.java`    |

_Adjust the base package `com.example` to your actual root package._

## Test Class Naming

| Source class  | Test class        |
| ------------- | ----------------- |
| `UserService` | `UserServiceTest` |
| `StringUtils` | `StringUtilsTest` |

## Null-Guard Exception Convention

Constructor null-guard tests expect:

- **`NullPointerException`** (default Java convention, thrown by `Objects.requireNonNull`)

_If the project uses `IllegalArgumentException` or another type, document it here._

## Assertion Style

This project uses **AssertJ** exclusively. Do not mix with Hamcrest or plain JUnit `assertEquals`.

```java
assertThat(result).isEqualTo(expected);
assertThatThrownBy(() -> sut.method(null)).isInstanceOf(NullPointerException.class);
```

## Mock Library

**Mockito** via `@ExtendWith(MockitoExtension.class)`. Use `@Mock` + `@InjectMocks` or manual wiring in `@BeforeEach`.

## Notes and Exceptions

_Record any project-specific rules that affect Architect strategy:_

- _e.g., "Always use manual `@BeforeEach` wiring — `@InjectMocks` is banned due to ambiguous constructors"_
- _e.g., "Repository interfaces are always mocked; never use an in-memory implementation in unit tests"_
