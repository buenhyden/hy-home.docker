---
description: Workflow for generating high-quality Bug Reports
---

# Bug Reporting Workflow

1. **Isolate**
    - Confirm the bug is reproducible.
    - Determine minimum steps to trigger it.
    - Verify if it happens in Incognito/Private mode (Rule out cache/extensions).

2. **Gather Evidence**
    - Take Screenshot of the UI state.
    - Copy text of Error Messages.
    - Open DevTools Console -> Copy Stack Trace.
    - Open Network Tab -> Identify failing request (500/400).

3. **Draft Report**
    - **Title**: `[Component] Brief description`
    - **Env**: Browser/OS.
    - **Steps**: 1, 2, 3...
    - **Expected**: "Form submits"
    - **Actual**: "Nothing happens, Console error 400"

4. **Submit**
    - Post to Tracking System (Jira/GitHub Issues).
    - Label with Severity.
    - Tag relevant Developer (if known).
