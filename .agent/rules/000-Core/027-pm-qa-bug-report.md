---
trigger: when reporting bugs or issues
glob: "BUG_REPORT.md, issues/*.md"
description: Standardized QA Bug Reporting template and guidelines.
---

# QA Bug Report Standards

## 1. The Golden Rule

**"Can a developer reproduce this without asking me any questions?"**

## 2. Required Fields

- **Title**: [Context] Concise summary (e.g., "[Checkout] Submit button unresponsive on iOS").
- **Environment**: OS, Browser Version, App Version, Device.
- **Severity**: Critical (Crash/Blocker) > High (Major Feature) > Medium (Annoyance) > Low (Cosmetic).
- **Steps to Reproduce**: Numbered, exact steps.
  1. Login as User A.
  2. Click 'Settings'.
  3. ...
- **Expected vs Actual**: Clear contrast.

## 3. Evidence

- **Screenshots**: Annotated if possible.
- **Logs**: Console errors, Network tab (500s), Server logs.
- **Video**: For complex interaction bugs.

## 4. Markdown Template

```markdown
# Bug: [Title]

## Summary
[Brief description]

## Severity
[Critical/High/Medium/Low]

## Environment
- OS: Windows 11
- Browser: Chrome 120
- Version: 1.0.5

## Steps to Reproduce
1.
2.
3.

## Expected Behavior
[...]

## Actual Behavior
[...]

## Logs/Screenshots
![Evidence](...)
```
