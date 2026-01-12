---
trigger: always_on
glob: "**/*"
description: "Bug Fix Workflow: Standardized process from reproduction to verification."
---
# Bug Fix Workflow

## 1. Reproduction (The "Repro")

- **Requirement**: A bug MUST be reproducible before fixing.
- **Step**: Create a minimal reproduction case (test case or script) that fails.
- **Documentation**: Document the reproduction steps in the issue.

## 2. Test-Driven Fix

1. **Fail**: Write a test that asserts the correct behavior (it should fail now).
2. **Fix**: Modify the code to pass the test.
3. **Pass**: Verify the test passes.

## 3. Regression Testing

- Ensure the fix does not break existing functionality. Run the full test suite for the affected module.

## 4. Submission

- **Commit**: `fix: description (#issue)`
- **PR**: Link the issue (`Fixes #123`).
- **Description**: Explain the root cause and the fix logic.


## See Also

- [010-core-git-specific.md](./010-core-git-specific.md) - Git commit standards for fixes
- [050-core-debugging-specific.md](./050-core-debugging-specific.md) - Debugging strategies
