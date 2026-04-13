# Project-Specific Test Patterns — Java Template

> **How to use this file:** Copy this template to `project-patterns.md` in your skill directory and fill in the values for your actual project. Delete any sections that don't apply. This file is loaded alongside `examples-java.md` when generating tests.

## Frameworks & Versions

| Library        | Version | Purpose                                   |
| -------------- | ------- | ----------------------------------------- |
| JUnit          | 5.x     | Test framework                            |
| Mockito        | 5.x     | Mocking                                   |
| AssertJ        | 3.x     | Assertion library                         |
| Java           | 17 / 21 | Runtime                                   |
| Build tool     | Maven / Gradle | Build and test runner              |

_Replace with your actual versions._

## Project Structure

Tests live under `src/test/java/` and mirror the source package structure under `src/main/java/`.

| Source                                               | Test                                                  |
| ---------------------------------------------------- | ----------------------------------------------------- |
| `src/main/java/com/example/services/UserService.java`| `src/test/java/com/example/services/UserServiceTest.java` |
| `src/main/java/com/example/utils/StringUtils.java`   | `src/test/java/com/example/utils/StringUtilsTest.java`|

_Adjust the base package `com.example` to your actual root package._

## Package Conventions

Test classes live in the **same package** as the class under test:

```java
// Source
package com.example.services;

// Test
package com.example.services;
```

This gives tests access to package-private members without breaking encapsulation.

## Test Class Naming

| Source class  | Test class       |
| ------------- | ---------------- |
| `UserService` | `UserServiceTest` |
| `StringUtils` | `StringUtilsTest` |

_Both `Test` suffix and `Test` prefix are common; pick one and be consistent._

## Common Annotations

```java
@ExtendWith(MockitoExtension.class)   // required for @Mock / @InjectMocks
@DisplayName("UserService Tests")     // optional — adds readable name in IDE/CI
```

Add project-specific annotations if you have custom test extensions:

```java
// Example: custom extension for database rollback
@ExtendWith(DatabaseRollbackExtension.class)
```

## Mock Setup Pattern

```java
@Mock
private UserRepository userRepository;

@InjectMocks
private UserService sut;
```

Or manual wiring (use when `@InjectMocks` is unreliable due to ambiguous constructors):

```java
@BeforeEach
void setUp() {
    userRepository = mock(UserRepository.class);
    sut = new UserService(userRepository);
}
```

## Assertion Style

This project uses **AssertJ** exclusively. Do not mix with Hamcrest or plain JUnit `assertEquals`.

```java
assertThat(result).isEqualTo(expected);
assertThat(list).hasSize(3).containsExactly("a", "b", "c");
assertThatThrownBy(() -> sut.method(null)).isInstanceOf(NullPointerException.class);
```

## Test Discovery Configuration

For Maven, Surefire runs classes matching `**/*Test.java` and `**/*Tests.java` by default. If your project customises this in `pom.xml` or `build.gradle`:

```xml
<!-- pom.xml example -->
<plugin>
  <artifactId>maven-surefire-plugin</artifactId>
  <configuration>
    <includes>
      <include>**/*Test.java</include>
    </includes>
  </configuration>
</plugin>
```

_Add your actual configuration here._

## Integration vs. Unit Test Separation

_Describe how this project distinguishes unit tests from integration tests. For example:_

- Unit tests: no `@SpringBootTest`, no DB, mocks only — tagged with `@Tag("unit")`
- Integration tests: `@SpringBootTest`, real DB via Testcontainers — tagged with `@Tag("integration")`, run in a separate CI step

## Project-Specific Test Helpers

_List any shared utilities, base classes, or custom matchers used in tests:_

```java
// Example: custom base class for repository tests
abstract class RepositoryTestBase {
    @BeforeEach
    void truncateTables() { ... }
}
```

## Notes and Exceptions

_Record any project-specific rules that override the defaults in `examples-java.md`:_

- _e.g., "Use `@DisplayName` for all test classes in the `api` module"_
- _e.g., "The `LegacyPaymentProcessor` class is not injectable — use `ReflectionTestUtils`"_
