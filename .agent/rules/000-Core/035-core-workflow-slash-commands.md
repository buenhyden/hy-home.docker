---
trigger: always_on
glob: "**/*"
description: "Workflow Slash Commands: Standardized commands for common dev tasks."
---
# Workflow Slash Commands

## 1. Commit Commands

- **/commit-fast**: Automates committing with AI-generated messages.
  - Generates 3 options based on diff.
  - Selects best fit automatically.
  - Commits without user confirmation (use with caution).

## 2. Fix Commands

- **/bug-fix**: Streamlines bug fixing workflow.
  - Creates feature branch `fix/<issue>`.
  - Requires failing test case.
  - Commits with `fix: description (#issue)`.

### Example: Usage

#### Good

```bash
# In chat:
/bug-fix "Login button not responsive"
```
