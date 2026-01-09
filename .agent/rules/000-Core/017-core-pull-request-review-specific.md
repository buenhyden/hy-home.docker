---
trigger: always_on
glob: "**/*"
description: "Pull Request Review agent instructions: Scoring, labeling, and integration."
---
# Pull Request Review Standards (Agent)

## 1. Review Objectives

1. **Requirements (50%)**: Does code meet issue requirements/AC?
2. **Standards (30%)**: Code style, security, specific stack patterns (Drupal/Vue/React).
3. **Security (20%)**: SQLi, XSS, Inputs, CSRF.
4. **Ops**: Labeling & Freshdesk updates.

## 2. Security Assessment

- **SQL**: Parametrized queries ONLY.
- **XSS**: Sanitization (`Html::escape`, `{{ }}`).
- **Permissions**: Proper access control checks.
- **Secrets**: No hardcoded keys.

## 3. Labeling Logic

- **Scores**:
  - ≥ 80%: `code-review-approved` (Green)
  - < 80%: `code-review-changes` (Orange)
  - Security Issues: `code-review-security` (Red)
- **Status**: `requirements-met` vs `requirements-gap`.
- **Tech**: `php-upgrade`, `performance-impact`.

## 4. Output

- **Line Comments**: Use GitHub Review API for specific feedback.
- **Freshdesk**: Update ticket with structured HTML summary (Score, findings, status).
