---
trigger: always_on
glob: "**/*.{test,spec}.{js,ts,jsx,tsx}"
description: "Jest: Mocking, Assertions, Async testing, and Setup/Teardown."
---
# Jest Standards

## 1. Mocking Strategies

- **External Systems**: Always mock Network requests (Axios/Fetch) and Databases. Unit tests must be offline.
- **Spies**: Use `jest.spyOn()` to observe behavior without overwriting it, or to mock implementation temporarily.
- **Restoration**: Use `afterEach(() => jest.clearAllMocks())` to prevent leakage between tests.

### Example: Spies

**Good**

```javascript
const logSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
// test...
logSpy.mockRestore(); // Cleanup
```

**Bad**

```javascript
console.error = jest.fn(); // Permanently corrupts console.error
```

## 2. Async Testing

- **Await**: Always `await` promises. Do not rely on `done` callbacks (legacy).
- **Reject**: Test error paths using `.rejects.toThrow()`.

### Example: Async

**Good**

```javascript
await expect(api.getUser(1)).resolves.toEqual({ id: 1 });
await expect(api.getBadUser()).rejects.toThrow('Not Found');
```

## 3. Structure & Hygiene

- **Describe Blocks**: specific functionality (`describe('getUser')`) -> specific scenarios (`it('returns user if found')`).
- **Snapshots**: Use small, inline snapshots (`toMatchInlineSnapshot`) for small UI/JSON. Avoid massive external snapshot files.
- **Setup**: Use `beforeAll` for heavy setup (Database connection) and `afterAll` for cleanup.
