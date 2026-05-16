# Project-Specific Test Patterns — TypeScript / React Template

> **How to use this file:** Copy this template to `project-patterns.md` in your `ut-analyst/references/` directory and fill in the values for your actual project. Delete any sections that don't apply. The Analyst reads this file to detect the null-exception convention for the language (e.g., `TypeError`) and to infer the expected test file path.

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
  models/

tests/             # top-level test directory (mirrors src/)
  components/
  services/
  utils/
```

_Alternatively, tests may live adjacent to source as `*.test.ts` files — update as needed._

## Test File Naming

| Source file                   | Test file                            |
| ----------------------------- | ------------------------------------ |
| `src/services/userService.ts` | `tests/services/userService.test.ts` |
| `src/components/UserList.tsx` | `tests/components/UserList.test.tsx` |
| `src/utils/validator.ts`      | `tests/utils/validator.test.ts`      |

## Null-Guard Exception Convention

When a required parameter is passed as `null` or `undefined`, the class or function under test should throw:

- **`TypeError`** — TypeScript/JavaScript default for null/undefined access violations

_If the project uses explicit guard throws, document the pattern:_

```typescript
// Example explicit guard
if (!repository) {
  throw new TypeError("repository is required");
}
```

## Notes and Exceptions

_Record any project-specific rules that affect Analyst output:_

- _e.g., "Services use Zod for input validation and throw `ZodError` instead of `TypeError`"_
- _e.g., "React components are tested via Testing Library, not unit-style class instantiation"_
