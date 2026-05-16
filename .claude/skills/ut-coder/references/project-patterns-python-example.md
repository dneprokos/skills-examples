# Project-Specific Test Patterns — Python Template

> **How to use this file:** Copy this template to `project-patterns.md` in your skill directory and fill in the values for your actual project. Delete any sections that don't apply. This file is loaded alongside `examples-python.md` when generating tests.

## Frameworks & Versions

| Library        | Version | Purpose                                 |
| -------------- | ------- | --------------------------------------- |
| pytest         | 8.x     | Test framework and runner               |
| pytest-asyncio | 0.23+   | Async test support                      |
| pytest-mock    | 3.x     | MagicMock / `mocker` fixture (optional) |
| Python         | 3.11+   | Runtime                                 |

_Replace with your actual versions from `requirements-dev.txt` or `pyproject.toml`._

## Project Structure

Tests live under `tests/` and mirror the source structure.

| Source                               | Test                                  |
| ------------------------------------ | ------------------------------------- |
| `src/myapp/services/user_service.py` | `tests/services/test_user_service.py` |
| `src/myapp/utils/string_utils.py`    | `tests/utils/test_string_utils.py`    |

_If your project uses `__tests__/` directories adjacent to source files instead, update accordingly._

## pytest Configuration

_Paste your `pytest.ini` or relevant `[tool.pytest.ini_options]` section from `pyproject.toml`:_

```toml
# pyproject.toml example
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"          # or "strict" — set to "auto" to avoid @pytest.mark.asyncio on every async test
addopts = "--strict-markers -q"
```

```ini
# pytest.ini example
[pytest]
testpaths = tests
asyncio_mode = auto
```

## Test Discovery

Pytest discovers files matching `test_*.py` or `*_test.py` and functions/methods prefixed with `test_` inside classes starting with `Test`.

_Note any custom collectors or markers registered in this project:_

```toml
# Example custom markers
markers = [
    "unit: fast unit tests with no I/O",
    "integration: tests that require a real DB or external service",
    "slow: tests expected to take more than 5 seconds",
]
```

## Mocking Approach

This project uses `unittest.mock` (stdlib). The `pytest-mock` `mocker` fixture is / is not available _(choose one)_.

Primary pattern:

```python
from unittest.mock import MagicMock, AsyncMock, patch

@pytest.fixture
def user_repository():
    return MagicMock(spec=UserRepository)
```

_If the project uses `pytest-mock`, fixtures look like:_

```python
def test_calls_repo(sut, mocker):
    mock_repo = mocker.MagicMock(spec=UserRepository)
    mocker.patch.object(sut, '_repository', mock_repo)
    ...
```

## Fixture Conventions

- Project-wide shared fixtures live in `tests/conftest.py`
- Module-level fixtures live at the top of the test file
- Use `scope="module"` or `scope="session"` only for expensive setup (DB connections, Docker containers)

_List any important shared fixtures here:_

```python
# From tests/conftest.py
@pytest.fixture(scope="session")
def db_engine():
    """Real SQLAlchemy engine connected to test database."""
    ...

@pytest.fixture
def db_session(db_engine):
    """Rolls back each test in a transaction."""
    ...
```

## Assertion Style

Plain `assert` statements with pytest's detailed failure output. No third-party assertion library.

```python
assert result == expected
assert result is None
assert "error" in str(exc_info.value).lower()
assert mock_repo.save.call_count == 1
```

_If this project uses a library like `assertpy` or `hamcrest`, note it here._

## Async Support

`asyncio_mode = auto` means all `async def test_*` functions run as coroutines without needing `@pytest.mark.asyncio`. _(Update if your project uses `strict` mode.)_

```python
async def test_fetch_user_returns_user(sut):
    result = await sut.fetch_user(42)
    assert result.name == "Alice"
```

## Import Conventions

Source root is on `PYTHONPATH` via `pyproject.toml` or `conftest.py`. Imports use the full package path:

```python
from myapp.services.user_service import UserService
from myapp.models import User
```

_If the project uses relative imports or a `src/` layout, note the import style here._

## Notes and Exceptions

_Record any project-specific rules that override the defaults in `examples-python.md`:_

- _e.g., "All service tests inherit from `BaseServiceTest` which provides a pre-configured `db_session` fixture"_
- _e.g., "Use `freezegun` for any test that touches `datetime.now()`"_
- _e.g., "`asyncio_mode = strict` — always add `@pytest.mark.asyncio` explicitly"_
