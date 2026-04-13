# Python Unit Test Examples — pytest + unittest.mock

This file contains Python-specific code patterns and examples for the unit-test-generator skill. The project-specific settings (pytest version, fixture conventions, conftest.py patterns) live in `project-patterns.md` — read that file alongside this one.

## File Structure

```python
# tests/services/test_user_service.py

import pytest
from unittest.mock import MagicMock, patch, call

from myapp.services.user_service import UserService
from myapp.repositories.user_repository import UserRepository
from myapp.models import User


@pytest.fixture
def user_repository():
    return MagicMock(spec=UserRepository)


@pytest.fixture
def sut(user_repository):
    return UserService(user_repository)


class TestGetUserById:

    def test_with_valid_id_returns_user(self, sut, user_repository):
        ...

    def test_when_user_not_found_raises_not_found_error(self, sut, user_repository):
        ...


class TestSaveUser:

    def test_with_valid_user_persists_and_returns(self, sut, user_repository):
        ...
```

Key rules:

- Test files are named `test_<module>.py` or `<module>_test.py` (pytest discovers both)
- Test files mirror the source structure under a `tests/` directory
- Test functions and methods are prefixed with `test_`
- Use `class Test[MethodName]` to group tests; class names must start with `Test`
- Use `pytest.fixture` to create the SUT and mocks; pass them as function parameters
- Use `MagicMock(spec=ClassName)` to create mocks that enforce the interface shape

## Naming Convention

Pattern: `test_[scenario]_[expected_outcome]`

```
test_with_valid_id_returns_user
test_with_negative_id_raises_value_error
test_when_user_not_found_raises_not_found_error
test_with_null_input_raises_type_error
test_empty_list_returns_zero
test_boundary_max_value_returns_max_result
test_repository_called_once_with_correct_id
```

Inside a class, the method name already has context from the class:

```python
class TestGetUserById:
    def test_valid_id_returns_user(self, sut): ...
    def test_negative_id_raises_value_error(self, sut): ...

class TestSaveUser:
    def test_valid_user_persists_and_returns(self, sut): ...
```

## AAA Pattern

```python
def test_with_valid_id_returns_user(self, sut, user_repository):
    # Arrange
    user_id = 42
    expected = User(id=user_id, name="Alice")
    user_repository.find_by_id.return_value = expected

    # Act
    result = sut.get_user_by_id(user_id)

    # Assert
    assert result == expected
```

For trivial cases, combined labels are acceptable:

```python
def test_empty_string_returns_false(self, sut):
    # Act & Assert
    assert sut.is_valid("") is False
```

## Parameterized Tests

Use `@pytest.mark.parametrize`:

```python
@pytest.mark.parametrize("input_value", ["", "  ", "\t", None])
def test_is_valid_blank_or_none_returns_false(self, sut, input_value):
    assert sut.is_valid(input_value) is False
```

Multiple parameters with IDs for clear test names:

```python
@pytest.mark.parametrize("a, b, expected", [
    (1, 1, 2),
    (5, 3, 8),
    (-1, 1, 0),
    (0, 0, 0),
], ids=["ones", "positive", "mixed_sign", "zeros"])
def test_add_various_inputs_returns_sum(self, sut, a, b, expected):
    assert sut.add(a, b) == expected
```

For complex scenarios with named tuples or dataclasses as input:

```python
INVALID_USERS = [
    pytest.param(User(id=None, name="Alice"), id="missing_id"),
    pytest.param(User(id=1, name=""), id="empty_name"),
    pytest.param(User(id=1, name=None), id="null_name"),
]

@pytest.mark.parametrize("invalid_user", INVALID_USERS)
def test_save_user_invalid_user_raises_validation_error(self, sut, invalid_user):
    with pytest.raises(ValidationError):
        sut.save_user(invalid_user)
```

## Fixtures

Declare fixtures close to where they're used (module level or in `conftest.py` for shared ones):

```python
@pytest.fixture
def email_service():
    return MagicMock(spec=EmailService)

@pytest.fixture
def user_repository():
    return MagicMock(spec=UserRepository)

@pytest.fixture
def sut(user_repository, email_service):
    return UserService(user_repository, email_service)
```

For fixtures that need cleanup:

```python
@pytest.fixture
def temp_file(tmp_path):
    file = tmp_path / "data.json"
    file.write_text('{"key": "value"}')
    yield file
    # cleanup happens automatically since tmp_path is managed by pytest
```

## Exception Assertions

```python
def test_divide_by_zero_raises_zero_division_error(self, sut):
    with pytest.raises(ZeroDivisionError):
        sut.divide(10, 0)

# Check message
def test_add_item_none_raises_value_error_with_message(self, sut):
    with pytest.raises(ValueError, match="item cannot be None"):
        sut.add_item(None)

# Capture exception for further inspection
def test_process_invalid_input_raises_with_details(self, sut):
    with pytest.raises(ProcessingError) as exc_info:
        sut.process("invalid")
    assert "invalid" in str(exc_info.value)
    assert exc_info.value.code == 400
```

## Mocking Patterns

### MagicMock with spec

```python
mock_repo = MagicMock(spec=UserRepository)
mock_repo.find_by_id.return_value = User(id=1, name="Alice")
```

### patch decorator

Use when the code imports and calls the dependency directly (not injected):

```python
@patch("myapp.services.email_sender.send_email")
def test_registers_user_sends_confirmation_email(self, mock_send, sut):
    # Arrange
    sut.register(email="alice@example.com")

    # Assert
    mock_send.assert_called_once_with(
        to="alice@example.com",
        subject="Welcome!"
    )
```

### patch as context manager

```python
def test_load_config_file_not_found_raises_config_error(self, sut):
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(ConfigError):
            sut.load_config("missing.json")
```

### Verify interactions

```python
mock_repo.save.assert_called_once_with(expected_user)
mock_repo.find_by_id.assert_called_once_with(42)
mock_email.send.assert_not_called()

# More flexible — argument matching
mock_repo.save.assert_called_once()
actual_arg = mock_repo.save.call_args[0][0]
assert actual_arg.name == "Alice"
```

## Async Test Pattern

Use `pytest-asyncio` with `@pytest.mark.asyncio`:

```python
import pytest
import pytest_asyncio


@pytest.mark.asyncio
async def test_fetch_user_valid_id_returns_user(self, sut, user_repository):
    # Arrange
    user_id = 42
    expected = User(id=user_id, name="Alice")
    user_repository.find_by_id_async = AsyncMock(return_value=expected)

    # Act
    result = await sut.fetch_user_async(user_id)

    # Assert
    assert result == expected

@pytest.mark.asyncio
async def test_fetch_user_not_found_raises(self, sut, user_repository):
    # Arrange
    user_repository.find_by_id_async = AsyncMock(side_effect=NotFoundError("User not found"))

    # Act & Assert
    with pytest.raises(NotFoundError):
        await sut.fetch_user_async(99)
```

## Grouping with Classes

Use a class per method under test. Shared fixtures can be defined at module level or in `conftest.py`:

```python
class TestDeposit:

    def test_positive_amount_increases_balance(self, sut):
        sut.deposit(100)
        assert sut.balance == 100

    def test_zero_amount_raises_value_error(self, sut):
        with pytest.raises(ValueError):
            sut.deposit(0)

    def test_negative_amount_raises_value_error(self, sut):
        with pytest.raises(ValueError):
            sut.deposit(-50)


class TestWithdraw:

    def test_sufficient_balance_decreases_balance(self, sut):
        sut.deposit(200)
        sut.withdraw(50)
        assert sut.balance == 150

    def test_insufficient_balance_raises_insufficient_funds(self, sut):
        sut.deposit(10)
        with pytest.raises(InsufficientFundsError):
            sut.withdraw(100)
```

## Python-Specific Anti-Patterns

- **Don't use** `unittest.TestCase` subclasses when using pytest — prefer plain functions and classes with `test_` prefix; `TestCase` loses access to pytest fixtures
- **Don't use** `assert mock.called` — prefer `mock.assert_called_once()` or `mock.assert_called_once_with(...)` for clearer failure messages
- **Don't patch** at the wrong import path — always patch where the name is looked up, not where it's defined (e.g., `patch("myapp.services.SomeClass")` not `patch("myapp.utils.SomeClass")`)
- **Don't use** `MagicMock()` without `spec=` for important dependencies — without spec, accessing non-existent attributes silently succeeds, hiding bugs
- **Don't forget** `pytest.ini` / `pyproject.toml` configuration for `asyncio_mode` when using `pytest-asyncio` (check `project-patterns.md`)
- **Don't share** mutable state between tests — always create fresh instances in fixtures, never at module level without `autouse` fixture cleanup
