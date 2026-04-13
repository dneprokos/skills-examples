# TypeScript Unit Test Examples — Vitest + React Testing Library

This file contains TypeScript-specific code patterns and examples for the unit-test-generator skill. The project-specific settings (framework versions, config paths, provider wrappers) live in `project-patterns.md` — read that file alongside this one.

The primary framework assumed here is **Vitest**. Where Jest differs, notes are provided. For **React component testing**, see the dedicated section at the bottom.

---

## File Structure

```
src/
  services/
    userService.ts
  utils/
    validator.ts
  models/
    ShoppingCart.ts
  components/
    UserList.tsx

tests/                         # or __tests__/ adjacent to source
  services/
    userService.test.ts
  utils/
    validator.test.ts
  models/
    ShoppingCart.test.ts
  components/
    UserList.test.tsx
```

```typescript
// tests/services/userService.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { UserService } from '../../src/services/userService';
import type { UserRepository } from '../../src/repositories/userRepository';

describe('UserService', () => {
  let userRepository: UserRepository;
  let sut: UserService;

  beforeEach(() => {
    userRepository = {
      findById: vi.fn(),
      save: vi.fn(),
    } as unknown as UserRepository;

    sut = new UserService(userRepository);
  });

  describe('getUserById', () => {
    it('should return user for valid id', async () => { ... });
    it('should throw NotFoundError when user does not exist', async () => { ... });
  });

  describe('saveUser', () => {
    it('should persist user and return saved entity', async () => { ... });
  });
});
```

## Naming Convention

Use descriptive `describe`/`it` strings. The pattern is: `it('should [expected outcome] when [scenario]')` or `it('should [expected outcome] for [input description]')`.

```
should return user for valid id
should throw NotFoundError when user does not exist
should return false for empty string
should return false for null input
should call repository save with correct arguments
should not call email service when user is inactive
should increment count to 3 after three clicks
```

Grouping with nested `describe`:

```typescript
describe('UserService', () => {
  describe('getUserById', () => {
    it('should return user for valid id', ...);
    it('should throw when id is negative', ...);
  });

  describe('saveUser', () => {
    it('should persist and return the user', ...);
    it('should throw ValidationError for invalid email', ...);
  });
});
```

## AAA Pattern

```typescript
it("should return user for valid id", async () => {
  // Arrange
  const userId = 42;
  const expected = { id: userId, name: "Alice" };
  vi.mocked(userRepository.findById).mockResolvedValue(expected);

  // Act
  const result = await sut.getUserById(userId);

  // Assert
  expect(result).toEqual(expected);
});
```

Combined labels for trivial setup:

```typescript
it("should return false for empty string", () => {
  // Act & Assert
  expect(sut.isValid("")).toBe(false);
});
```

## Parameterized Tests

Use `it.each` (table-driven) or `it.each` with template literals:

```typescript
// Array of [input, expected] tuples
it.each([
  ["valid@example.com", true],
  ["user@domain.co.uk", true],
  ["", false],
  ["not-an-email", false],
  ["missing@", false],
  [null, false],
])("should return %s for isValid(%s)", (input, expected) => {
  expect(sut.isValid(input as string)).toBe(expected);
});

// Named cases — more readable in test output
it.each([
  { input: "valid@example.com", expected: true, label: "valid email" },
  { input: "", expected: false, label: "empty string" },
  { input: null, expected: false, label: "null input" },
])("should return $expected for $label", ({ input, expected }) => {
  expect(sut.isValid(input as string)).toBe(expected);
});
```

For `describe.each` when the whole describe block parameterizes:

```typescript
describe.each([
  { currency: "USD", symbol: "$" },
  { currency: "EUR", symbol: "€" },
])("with $currency currency", ({ currency, symbol }) => {
  it("should format amount with correct symbol", () => {
    expect(formatter.format(100, currency)).toContain(symbol);
  });
});
```

## Mocking

### Inline object mock (for interfaces / simple objects)

```typescript
const userRepository = {
  findById: vi.fn(),
  save: vi.fn(),
  delete: vi.fn(),
} as jest.Mocked<UserRepository>; // or as vi.Mocked<UserRepository>
```

### vi.fn() for callbacks and simple dependencies

```typescript
const onSubmit = vi.fn();
const logger = { log: vi.fn(), error: vi.fn() };
```

### vi.mock() for module-level mocking

```typescript
vi.mock("../../src/services/emailService", () => ({
  sendEmail: vi.fn(),
}));

import { sendEmail } from "../../src/services/emailService";
// sendEmail is now a vi.Mock
```

### vi.spyOn() for partial mocks

```typescript
const spy = vi.spyOn(console, "error").mockImplementation(() => {});
// ... run test
spy.mockRestore();
```

### Configure return values

```typescript
vi.mocked(userRepository.findById).mockResolvedValue({ id: 1, name: "Alice" });
vi.mocked(userRepository.findById).mockRejectedValue(new Error("DB error"));
vi.mocked(userRepository.save).mockResolvedValueOnce({ id: 1, name: "Alice" });
```

### Verify interactions

```typescript
expect(userRepository.save).toHaveBeenCalledOnce();
expect(userRepository.save).toHaveBeenCalledWith(
  expect.objectContaining({ name: "Alice" }),
);
expect(emailService.send).not.toHaveBeenCalled();
```

## Exception Assertions

```typescript
// Synchronous throw
expect(() => sut.divide(10, 0)).toThrow("Division by zero");
expect(() => sut.process(null)).toThrow(TypeError);

// Async throw
await expect(sut.fetchUser(999)).rejects.toThrow("User not found: 999");
await expect(sut.fetchUser(999)).rejects.toBeInstanceOf(NotFoundError);
```

## Async Test Pattern

```typescript
it("should fetch user successfully", async () => {
  // Arrange
  const mockUser = { id: "123", name: "John" };
  vi.mocked(userRepository.findById).mockResolvedValue(mockUser);

  // Act
  const user = await sut.getUserById("123");

  // Assert
  expect(user).toEqual(mockUser);
  expect(userRepository.findById).toHaveBeenCalledWith("123");
});

it("should throw NetworkError when request fails", async () => {
  // Arrange
  vi.mocked(userRepository.findById).mockRejectedValue(
    new Error("Network error"),
  );

  // Act & Assert
  await expect(sut.getUserById("123")).rejects.toThrow("Network error");
});
```

---

## React Component Testing (Testing Library + Vitest)

Use **React Testing Library** with **Vitest** (or Jest). Test from the user's perspective: query by accessible roles, labels, and text — not by CSS classes or component internals.

### File Structure

```typescript
// tests/components/SearchBox.test.tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { SearchBox } from "../../src/components/SearchBox";
```

### Provider Wrapper Pattern

When a component needs context providers (Router, QueryClient, Redux store), wrap it with an `AllProviders` helper rather than repeating setup in every test:

```typescript
// tests/AllProviders.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router-dom';

export function AllProviders({ children }: { children: React.ReactNode }) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return (
    <QueryClientProvider client={queryClient}>
      <MemoryRouter>{children}</MemoryRouter>
    </QueryClientProvider>
  );
}

// Usage in tests
render(<MyComponent />, { wrapper: AllProviders });
```

### renderComponent Helper Pattern

For complex components, extract a `renderComponent` factory function that returns query helpers and action functions. This keeps tests readable and avoids repetitive setup:

```typescript
describe('SearchBox', () => {
  const renderComponent = () => {
    const onChange = vi.fn();
    render(<SearchBox onChange={onChange} />);

    return {
      input: screen.getByPlaceholderText(/search/i),
      user: userEvent.setup(),
      onChange,
    };
  };

  it('should render an input field', () => {
    const { input } = renderComponent();
    expect(input).toBeInTheDocument();
  });

  it('should call onChange when Enter is pressed', async () => {
    const { input, onChange, user } = renderComponent();
    await user.type(input, 'hello{enter}');
    expect(onChange).toHaveBeenCalledWith('hello');
  });

  it('should not call onChange when input is empty', async () => {
    const { input, onChange, user } = renderComponent();
    await user.type(input, '{enter}');
    expect(onChange).not.toHaveBeenCalled();
  });
});
```

For components with complex async loading, expose `waitForFormToLoad` or similar async helpers:

```typescript
const renderComponent = () => {
  const onSubmit = vi.fn();
  render(<ProductForm onSubmit={onSubmit} />, { wrapper: AllProviders });

  return {
    onSubmit,
    waitForFormToLoad: async () => {
      await screen.findByRole('form');                      // wait for load
      return {
        nameInput: screen.getByPlaceholderText(/name/i),
        submitButton: screen.getByRole('button', { name: /save/i }),
      };
    },
  };
};
```

### Querying Elements

Prefer role-based queries — they reflect accessibility and match how users interact with the UI:

```typescript
// Preferred
screen.getByRole("button", { name: /submit/i });
screen.getByRole("textbox", { name: /email/i });
screen.getByRole("img", { name: /avatar/i });
screen.getByRole("heading", { name: /cart/i });

// Text content
screen.getByText(/welcome/i);

// Placeholder / label (when no semantic role is available)
screen.getByPlaceholderText(/search/i);
screen.getByLabelText(/password/i);
```

Use `findBy*` for elements that appear asynchronously, `queryBy*` to assert absence:

```typescript
// Async — waits up to timeout
const heading = await screen.findByRole("heading", { name: /products/i });

// Assert element is NOT present
expect(screen.queryByRole("alert")).not.toBeInTheDocument();
```

### User Interactions

Always use `userEvent` (not `fireEvent`) for user interactions — it simulates realistic browser behaviour:

```typescript
const user = userEvent.setup();

await user.type(input, "hello");
await user.click(button);
await user.selectOptions(select, ["option1"]);
await user.keyboard("{Enter}");
await user.tab();
await user.clear(input);
```

### Component Test Examples

```typescript
// Simple rendering
it('should render a list of images', () => {
  const imageUrls = ['url1', 'url2'];
  render(<ProductImageGallery imageUrls={imageUrls} />);
  const images = screen.getAllByRole('img');
  expect(images).toHaveLength(2);
  imageUrls.forEach((url, index) => {
    expect(images[index]).toHaveAttribute('src', url);
  });
});

// Interaction test
it('should increment count on button click', async () => {
  render(<Counter />);
  const user = userEvent.setup();
  const button = screen.getByRole('button', { name: /increment/i });

  await user.click(button);

  expect(screen.getByText('Count: 1')).toBeInTheDocument();
});

// Async data loading
it('should display users after loading', async () => {
  render(<UserList />, { wrapper: AllProviders });
  expect(await screen.findByText('Alice')).toBeInTheDocument();
});

// Validation errors
it.each([
  { scenario: 'missing', name: undefined, error: /required/i },
  { scenario: 'too long', name: 'a'.repeat(256), error: /255/i },
])('should show error when name is $scenario', async ({ name, error }) => {
  const { waitForFormToLoad } = renderComponent();
  const { nameInput, submitButton } = await waitForFormToLoad();
  const user = userEvent.setup();

  if (name) await user.type(nameInput, name);
  await user.click(submitButton);

  expect(screen.getByRole('alert')).toHaveTextContent(error);
});

// Callback props
it('should call onSubmit with correct data', async () => {
  const { onSubmit, waitForFormToLoad } = renderComponent();
  const { nameInput, submitButton } = await waitForFormToLoad();
  const user = userEvent.setup();

  await user.type(nameInput, 'Widget');
  await user.click(submitButton);

  expect(onSubmit).toHaveBeenCalledWith({ name: 'Widget' });
});
```

### React-Specific Anti-Patterns

- **Don't** query by CSS class or `data-testid` when a semantic role or accessible name exists — it makes tests brittle and doesn't test accessibility
- **Don't use** `fireEvent.click()` for user interactions — use `userEvent.click()` which simulates the full event chain
- **Don't** `await` synchronous queries (`getBy*`) — only `findBy*` should be awaited
- **Don't wrap** every render in a `waitFor` — if more than a few tests need it, the component may need a loading indicator or the test setup is wrong
- **Don't** test component internals (state values, refs, private methods) — test what the user sees and does
- **Don't forget** to call `userEvent.setup()` — calling `userEvent.click(el)` without setup skips pointer events

---

## TypeScript-Specific Anti-Patterns

- **Don't use** `as any` to bypass type errors in test files — use proper type assertions or `as unknown as T` only when necessary
- **Don't write** `expect(mock).toBeCalled()` without importing the correct mock — if the module is not mocked, the assertion will always pass vacuously
- **Don't skip** `vi.clearAllMocks()` in `beforeEach` when mocks accumulate state across tests — or configure `clearMocks: true` in `vitest.config.ts`
- **Don't use** Jest globals (`jest.fn()`, `jest.mock()`) in a Vitest project — import from `vitest` instead
