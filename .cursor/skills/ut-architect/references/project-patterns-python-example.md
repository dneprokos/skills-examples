# Project-Specific Test Patterns — Python Template

> **How to use this file:** Copy this template to `project-patterns.md` in your `ut-architect/references/` directory and fill in the values for your actual project. Delete any sections that don't apply. The Architect reads this file to determine assertion style, test file location, and the null-guard exception type for constructor parameters.

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

## Null-Guard Exception Convention

Constructor null-guard tests expect:

- **`TypeError`** — Python's default for None passed where an object is required

_If the project raises `ValueError` for missing required arguments instead, document it here._

## Assertion Style

Plain `assert` statements with pytest's detailed failure output. No third-party assertion library (unless documented here).

```python
assert result == expected
with pytest.raises(TypeError):
    MyService(repository=None)
```

## Mock Library

`unittest.mock.MagicMock(spec=ClassName)` to create mocks that enforce interface shape.

_If `pytest-mock` `mocker` fixture is used, document its pattern here._

## Notes and Exceptions

_Record any project-specific rules that affect Architect strategy:_

- _e.g., "All services raise `ValueError` (not `TypeError`) for None constructor arguments"_
- _e.g., "Use `AsyncMock` for any dependency whose methods are coroutines"_
