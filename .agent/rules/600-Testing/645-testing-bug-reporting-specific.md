---
trigger: always_on
glob: "**/*"
description: "QA: Structured bug reporting standards with severity levels and reproduction steps."
---
# Bug Reporting Standards

## 1. Structure

All bug reports must follow this standard structure:

- **Title**: Concise summary.
- **Severity**: Level 1-5 (Criticial to Cosmetic).
- **Environment**: OS, Browser, App Version.
- **Steps to Reproduce**: Numbered list.
- **Expected vs. Actual**: Clear contrast.

## 2. Severity Levels

- **S1 (Critical)**: Data loss, system crash, security breach.
- **S2 (Major)**: Core feature broken, no workaround.
- **S3 (Medium)**: Feature broken, workaround exists.
- **S4 (Minor)**: UI/UX annoyance, typo.
- **S5 (Trivial)**: Suggestion, minor polish.

## 3. Best Practices

- **One Bug Per Report**: Do not bundle issues.
- **Objective**: "Button fails to click" vs. "Broken UI".
- **Evidence**: Attach logs, screenshots, or videos.

### Example: Bug Report

#### Good

```markdown
**Title**: Checkout fails with 500 Error when cart > 10 items

**Severity**: S2 (Major)

**Steps to Reproduce**:
1. Add 11 items to cart.
2. Click "Checkout".
3. Observe error page.

**Expected**: Proceed to payment.
**Actual**: 500 Internal Server Error.
```

## 4. Defect Lifecycle

- **Status Flow**: New -> Confirmed -> In Progress -> Fixed -> Verified -> Closed.
- **Proof**: Attach screenshots or error logs for every fix before closing.
