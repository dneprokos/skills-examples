# Project-Specific Test Patterns — TypeScript / React Template

> **How to use this file:** Copy this template to `project-patterns.md` in your skill directory and fill in the values for your actual project. Delete any sections that don't apply. This file is loaded alongside `examples-typescript.md` when generating tests.

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
  setup.ts         # Vitest setup file (runs before each test file)
  AllProviders.tsx  # Provider wrapper for component tests
  utils.tsx        # shared render helpers
```

_Alternatively, tests may live adjacent to source as `*.test.ts` files — update as needed._

## Test Configuration

_Paste your relevant `vitest.config.ts` section:_

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true, // allows describe/it/expect without imports
    environment: "jsdom", // required for React Testing Library
    setupFiles: ["./tests/setup.ts"], // runs before each test file
    clearMocks: true, // automatically clears mocks between tests
  },
});
```

_If using Jest, provide your `jest.config.ts` instead._

## Setup File

_Paste or describe what `tests/setup.ts` contains:_

```typescript
// tests/setup.ts
import "@testing-library/jest-dom"; // extends expect() with custom DOM matchers
```

## Import Conventions

_Describe how imports work — path aliases, barrel files, etc.:_

```typescript
// If the project uses path aliases (e.g., @/ → src/)
import { UserService } from "@/services/userService";
import type { User } from "@/models/User";

// Or relative imports
import { UserService } from "../../src/services/userService";
```

## Global vs. Explicit Imports

If `globals: true` is set in `vitest.config.ts`, you do not need to import `describe`, `it`, `expect`, `vi`, or `beforeEach`:

```typescript
// globals: true — no imports needed
describe("MyService", () => {
  it("should work", () => {
    expect(true).toBe(true);
  });
});

// globals: false — explicit imports required
import { describe, it, expect, vi, beforeEach } from "vitest";
```

_State which mode this project uses._

## Mock Configuration

```typescript
// In vitest.config.ts — set clearMocks/resetMocks/restoreMocks globally
clearMocks: true,    // clears mock.calls and mock.results before each test
resetMocks: false,   // resets mock implementation/return values
restoreMocks: false, // restores vi.spyOn() mocks to original implementation
```

_If not using global mock clearing, note that tests must call `vi.clearAllMocks()` in `beforeEach`._

## Provider Wrapper

_Describe and show your `AllProviders` component or individual provider setup:_

```typescript
// tests/AllProviders.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router-dom';

interface Props {
  children: React.ReactNode;
}

export function AllProviders({ children }: Props) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false, staleTime: Infinity },
    },
  });

  return (
    <QueryClientProvider client={queryClient}>
      <MemoryRouter>
        {children}
      </MemoryRouter>
    </QueryClientProvider>
  );
}
```

Usage: `render(<MyComponent />, { wrapper: AllProviders });`

_If the project uses Redux, add `<Provider store={testStore}>` to AllProviders._

## Test File Naming

| Source file                   | Test file                            |
| ----------------------------- | ------------------------------------ |
| `src/services/userService.ts` | `tests/services/userService.test.ts` |
| `src/components/UserList.tsx` | `tests/components/UserList.test.tsx` |
| `src/utils/validator.ts`      | `tests/utils/validator.test.ts`      |

## TypeScript Configuration for Tests

_If `tsconfig.json` has paths or strict settings relevant to tests, note them:_

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"]
    },
    "types": ["vitest/globals", "@testing-library/jest-dom"]
  }
}
```

## React Query / API Mocking

_Describe how API calls are mocked in this project:_

```typescript
// Option A: vi.mock the fetch/axios module
vi.mock("@/lib/apiClient", () => ({
  get: vi.fn(),
  post: vi.fn(),
}));

// Option B: MSW (Mock Service Worker) handlers
// server is set up in tests/setup.ts via setupServer(...)
import { server } from "../mocks/server";
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

## Notes and Exceptions

_Record any project-specific rules that override the defaults in `examples-typescript.md`:_

- _e.g., "Use `screen.getByTestId('...')` only in the components/ module — the design system does not expose ARIA roles on all leaf elements"_
- _e.g., "The Auth context must always be wrapped with `<AuthProvider isAuthenticated={true}>` in tests"_
- _e.g., "Vitest globals are disabled — always import `{ describe, it, expect, vi }` explicitly"_
- _e.g., "MSW is used for all API mocking — do not use `vi.mock` for HTTP calls"_
