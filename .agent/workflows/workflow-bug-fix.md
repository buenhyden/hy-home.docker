---
description: Standard workflow for fixing bugs
---

# Bug Fix Workflow

Based on `016-core-bug-fix-workflow-specific.md`.

1. **Reproduction**
   - Create a minimal reproduction case (script or test).
   - Document steps in the issue.

2. **Test-Driven Fix**
   - Write a FAILING test case that asserts the correct behavior.
   - Run the test to confirm failure.

   ```bash
   # Example
   pytest tests/test_bug_repro.py
   ```

3. **Implementation**
   - Modify code to fix the bug.
   - Run the test again to confirm PASSS.

4. **Regression Testing**
   - Run the full test suite for the affected module.

5. **Submission**
   - Commit with format: `fix: description (#issue)`
   - Link the issue in PR.
