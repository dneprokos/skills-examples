# Project-Specific Test Patterns — TypeScript / React Template

> **How to use this file:** Copy this template to `project-patterns.md` in your `ut-architect/references/` directory and fill in the values for your actual project. Delete any sections that don't apply. The Architect reads this file to determine assertion style, test file location, and the null-guard exception type for constructor parameters.

## Frameworks & Versions

| Library                     | Version | Purpose                     |
| --------------------------- | ------- | --------------------------- |
| Vitest (or Jest)            | 2.x     | Test framework and runner   |
| @testing-library/react      | 16.x    | React component testing     |
| @testing-library/user-event | 14.x    | User interaction simulation |
| @testing-library/jest-dom   | 6.x     | Custom DOM matchers         |
| React                       | 18 / 19 | UI library                  |
| TypeScript                  | 5.x     | Language                    |

_Replace with your actual versions from `package.json`._

## Project Structure

```
src/
  components/
  services/
  utils/

tests/             # mirrors src/
  components/
  services/
  utils/
```

## Test File Naming

| Source file                   | Test file                            |
| ----------------------------- | ------------------------------------ |
| `src/services/userService.ts` | `tests/services/userService.test.ts` |
| `src/components/UserList.tsx` | `tests/components/UserList.test.tsx` |

## Null-Guard Exception Convention

Constructor null-guard tests expect:

- **`TypeError`** — TypeScript/JavaScript default for null/undefined violations

_If the project uses explicit guard throws with a custom message, document the pattern:_

```typescript
if (!repository) throw new TypeError("repository is required");
```

## Assertion Style

**Vitest `expect`** (or Jest `expect`) with `@testing-library/jest-dom` custom matchers for DOM assertions.

```typescript
expect(result).toEqual(expected);
expect(() => new MyService(null)).toThrow(TypeError);
```

## Mock Library

**`vi.fn()`** for function mocks; object mocks via partial object literal cast with `as unknown as MyInterface`.

_If using Jest, replace `vi` with `jest`._

## Notes and Exceptions

_Record any project-specific rules that affect Architect strategy:_

- _e.g., "`globals: false` in vitest.config.ts — always import `{ describe, it, expect, vi }` explicitly"_
- _e.g., "React components require `AllProviders` wrapper — never render without context"_
- _e.g., "Use `msw` for all HTTP dependency mocking — never mock `fetch` directly"_
