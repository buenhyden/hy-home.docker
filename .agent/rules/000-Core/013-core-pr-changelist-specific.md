---
trigger: always_on
glob: "*.md"
description: "PR Changelist: Formatting standards for pull request descriptions."
---
# PR Changelist Standards

## 1. Format

- **Output**: request "raw markdown code block" to avoid rendering.
- **Structure**: Start with `# Summary of Changes`, then use `## Categories`.
- **Items**: Past tense verbs (`Added`, `Fixed`), backticks for code (`variable`).

## 2. Compliance

- **Validation**: Ensure output starts with ` ```markdown ` and `# Summary`.

### Example: Changelist

#### Good

```markdown
# Summary of Changes

## Auth
- Added `login` function.
- Fixed token expiration bug.
```
