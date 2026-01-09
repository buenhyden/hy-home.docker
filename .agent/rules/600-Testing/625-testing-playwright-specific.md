---
trigger: always_on
glob: "**/*.spec.ts"
description: "Playwright: Reliable Locators, Visual Testing, and Parallel Execution."
---
# Playwright Standards

## 1. Locators & Selectors

- **User-Facing**: `page.getByRole()`, `page.getByLabel()`, `page.getByText()`.
- **Resilience**: Avoid CSS/XPath selectors coupled to implementation details.
- **TestID**: Use `page.getByTestId()` as a last resort.

## 2. Execution & Context

- **Parallelism**: Enable `fullyParallel: true`. Tests MUST be isolated.
- **Context**: Rely on `browserContext` setup in `test-worker`.
- **Authentication**: Use `globalSetup` or `storageState.json` for session reuse.

## 3. Visual Comparison (Snapshot Testing)

- **Screenshots**: Use `expect(page).toHaveScreenshot()` for visual regression.
- **Thresholds**: Configure `maxDiffPixels` or `maxDiffPixelRatio` for tolerance.

### Example: Visual

**Good**

```ts
await expect(page).toHaveScreenshot('landing.png', { maxDiffPixelRatio: 0.01 });
```

**Bad**

```ts
// No visual tests, relying on manual visual QA for every release
```

## 4. Network & Mocking

- **Route**: `page.route('**/api/data', route => route.fulfill(...))`.

## 5. Debugging

- **Trace Viewer**: Enable `trace: 'retain-on-failure'`. Best debugging tool.
