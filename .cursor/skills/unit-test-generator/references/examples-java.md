# Java Unit Test Examples — JUnit 5 + Mockito + AssertJ

This file contains Java-specific code patterns and examples for the unit-test-generator skill. The project-specific settings (dependency versions, package conventions, build tool) live in `project-patterns.md` — read that file alongside this one.

## File Structure

```java
package com.example.myapp.services;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.Mockito.*;

import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.*;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private EmailService emailService;

    @InjectMocks
    private UserService sut;

    @Nested
    class GetUserById {

        @Test
        void withValidId_returnsUser() {
            // ...
        }

        @Test
        void whenUserNotFound_throwsNotFoundException() {
            // ...
        }
    }

    @Nested
    class SaveUser {

        @Test
        void withValidUser_persistsAndReturns() {
            // ...
        }
    }
}
```

Key rules:
- Test class names end in `Test` (not `Tests`) by Maven Surefire convention
- Class and method visibility is package-private (no `public`) — JUnit 5 does not require it
- Use `@ExtendWith(MockitoExtension.class)` on the class; declare mocks with `@Mock` and inject with `@InjectMocks`
- Source lives in `src/main/java/`; tests mirror to `src/test/java/` with the same package
- Test file location mirrors source: if source is `src/main/java/com/example/services/UserService.java`, test is `src/test/java/com/example/services/UserServiceTest.java`

## Naming Convention

Pattern: `[scenario]_[expectedOutcome]` inside a `@Nested` class named after the method under test.

```
class GetUserById {
    withValidId_returnsUser
    withNegativeId_throwsIllegalArgumentException
    whenUserNotFound_returnsEmpty
}

class SaveUser {
    withValidData_persistsUser
    withNullUser_throwsNullPointerException
    whenRepositoryFails_propagatesException
}
```

Alternatively, the flat naming pattern `[methodUnderTest]_[scenario]_[expectedOutcome]` is also acceptable:

```
getUserById_withValidId_returnsUser
getUserById_withNegativeId_throwsIllegalArgumentException
saveUser_withNullUser_throwsNullPointerException
```

## AAA Pattern

```java
@Test
void withValidId_returnsUser() {
    // Arrange
    var userId = 42L;
    var expected = new User(userId, "Alice");
    when(userRepository.findById(userId)).thenReturn(Optional.of(expected));

    // Act
    var result = sut.getUserById(userId);

    // Assert
    assertThat(result).isEqualTo(expected);
}
```

## Parameterized Tests

Use `@ParameterizedTest` with a source annotation:

```java
// Simple single-value cases
@ParameterizedTest
@ValueSource(strings = {"", "  ", "\t"})
void isValid_blankInput_returnsFalse(String input) {
    assertThat(sut.isValid(input)).isFalse();
}

// Null input (NullSource or NullAndEmptySource)
@ParameterizedTest
@NullAndEmptySource
void isValid_nullOrEmpty_returnsFalse(String input) {
    assertThat(sut.isValid(input)).isFalse();
}

// Multiple columns
@ParameterizedTest
@CsvSource({
    "1, 1, 2",
    "5, 3, 8",
    "-1, 1, 0",
    "0, 0, 0"
})
void add_variousInputs_returnsSum(int a, int b, int expected) {
    assertThat(sut.add(a, b)).isEqualTo(expected);
}

// Complex objects via method source
@ParameterizedTest
@MethodSource("invalidUserProvider")
void saveUser_invalidUser_throwsValidationException(User invalidUser) {
    assertThatThrownBy(() -> sut.saveUser(invalidUser))
        .isInstanceOf(ValidationException.class);
}

private static Stream<Arguments> invalidUserProvider() {
    return Stream.of(
        Arguments.of(new User(null, "Alice")),
        Arguments.of(new User(1L, "")),
        Arguments.of(new User(1L, null))
    );
}
```

## Setup — Mockito

`@Mock` + `@InjectMocks` with `@ExtendWith(MockitoExtension.class)` is the preferred approach:

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    private ProductRepository productRepository;

    @Mock
    private PaymentGateway paymentGateway;

    @InjectMocks
    private OrderService sut;

    @BeforeEach
    void setUp() {
        // Additional setup beyond mock injection goes here
    }
}
```

Configure return values:

```java
when(productRepository.findById(productId)).thenReturn(Optional.of(product));
when(paymentGateway.charge(any())).thenReturn(PaymentResult.success());
```

Configure thrown exceptions:

```java
when(productRepository.findById(anyLong()))
    .thenThrow(new DatabaseException("Connection lost"));
```

Verify interactions:

```java
verify(paymentGateway, times(1)).charge(any(ChargeRequest.class));
verify(emailService, never()).sendConfirmation(anyString());
verify(productRepository).save(argThat(p -> p.getName().equals("Widget")));
```

## Exception Assertions (AssertJ)

```java
// Basic exception type
assertThatThrownBy(() -> sut.process(null))
    .isInstanceOf(NullPointerException.class);

// Message check
assertThatThrownBy(() -> sut.divide(10, 0))
    .isInstanceOf(ArithmeticException.class)
    .hasMessageContaining("zero");

// Caused by
assertThatThrownBy(() -> sut.loadConfig("missing.json"))
    .isInstanceOf(ConfigException.class)
    .hasCauseInstanceOf(IOException.class);

// assertThatExceptionOfType (more readable for known types)
assertThatExceptionOfType(IllegalArgumentException.class)
    .isThrownBy(() -> sut.setAge(-1))
    .withMessage("Age must be non-negative");
```

## Async / CompletableFuture

```java
@Test
void fetchData_validUrl_returnsContent() throws Exception {
    // Arrange
    when(httpClient.getAsync("https://api.example.com/data"))
        .thenReturn(CompletableFuture.completedFuture("response body"));

    // Act
    var result = sut.fetchData("https://api.example.com/data").get();

    // Assert
    assertThat(result).isEqualTo("response body");
}

@Test
void fetchData_serverError_completesExceptionally() {
    // Arrange
    when(httpClient.getAsync(anyString()))
        .thenReturn(CompletableFuture.failedFuture(new IOException("503")));

    // Act & Assert
    var future = sut.fetchData("https://api.example.com/data");
    assertThatThrownBy(future::get)
        .hasCauseInstanceOf(IOException.class);
}
```

## Grouping with @Nested

Use `@Nested` to organise tests by the method under test. Each inner class gets a descriptive name:

```java
@Nested
class Deposit {

    @Test
    void withPositiveAmount_increasesBalance() { ... }

    @Test
    void withZeroAmount_throwsIllegalArgumentException() { ... }

    @Test
    void withNegativeAmount_throwsIllegalArgumentException() { ... }
}

@Nested
class Withdraw {

    @Test
    void withSufficientBalance_decreasesBalance() { ... }

    @Test
    void withInsufficientBalance_throwsInsufficientFundsException() { ... }
}
```

For a class with only one or two public methods, skip `@Nested` and put the test methods directly in the outer class.

## Java-Specific Anti-Patterns

- **Don't use** JUnit 4 annotations (`@org.junit.Test`, `@Before`, `@RunWith`) — use JUnit 5 (`@Test`, `@BeforeEach`, `@ExtendWith`)
- **Don't add** `public` to test classes or test methods — JUnit 5 doesn't require it and it's noisy
- **Don't use** Hamcrest matchers (`assertThat(..., is(...))`) when the project uses AssertJ — pick one assertion library and be consistent
- **Don't mock** `final` classes without enabling the Mockito inline mock maker; prefer injecting via interface instead
- **Don't use** `@InjectMocks` when the constructor has ambiguous injection — prefer constructor injection or `@Spy` + manual wiring
- **Don't call** `verifyNoMoreInteractions(mock)` at the end of every test — it creates brittle tests; only verify interactions that are actually part of the tested behaviour
