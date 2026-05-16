# Project-Specific Test Patterns — Python Template

> **How to use this file:** Copy this template to `project-patterns.md` in your `ut-analyst/references/` directory and fill in the values for your actual project. Delete any sections that don't apply. The Analyst reads this file to detect the null-exception convention for the language (e.g., `TypeError` vs `ValueError`) and to infer the expected test file path.

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

## Test Class Naming

| Source module     | Test class        |
| ----------------- | ----------------- |
| `user_service.py` | `TestUserService` |
| `string_utils.py` | `TestStringUtils` |

## Null-Guard Exception Convention

When a required parameter is passed as `None`, the class or function under test should raise:

- **`TypeError`** — Python's default for incorrect argument types (including missing/None values)
- **`ValueError`** — use when the project validates argument values explicitly

_Document which is preferred in this project, or any explicit guard pattern:_

```python
# Example explicit guard
if repository is None:
    raise TypeError("repository cannot be None")
```

## Notes and Exceptions

_Record any project-specific rules that affect Analyst output:_

- _e.g., "All services raise `ValueError` for `None` constructor arguments"_
- _e.g., "`asyncio_mode = strict` — async tests require `@pytest.mark.asyncio` explicitly"_
