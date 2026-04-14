# Project-Specific Test Patterns — Java Template

> **How to use this file:** Copy this template to `project-patterns.md` in your `ut-analyst/references/` directory and fill in the values for your actual project. Delete any sections that don't apply. The Analyst reads this file to detect the null-exception convention for the language (e.g., `NullPointerException`) and to infer the expected test file path.

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

When a constructor parameter is `null`, the class under test should throw:

- **`NullPointerException`** (default Java convention)

_If the project uses a different convention (e.g., `IllegalArgumentException`, or `Objects.requireNonNull` with a custom message), document it here._

## Notes and Exceptions

_Record any project-specific rules that affect Analyst output:_

- _e.g., "All services validate constructor parameters with `Objects.requireNonNull` and throw `NullPointerException`"_
- _e.g., "The `LegacyPaymentProcessor` is a concrete class instantiated directly — it has no interface"_
