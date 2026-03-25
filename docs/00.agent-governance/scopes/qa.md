---
title: 'Quality Assurance Scope'
layer: qa
---

# Quality Assurance Scope

Standards for testing, automation, and reliability engineering.

## 1. Context & Objective
- **Goal**: Zero-regression delivery and high confidence releases.

## 2. Requirements & Constraints
- **Target**: 100% pass rate for E2E tests before merge.

## 3. Implementation Flow
1. Write test plan in `05.plans`.
2. Implement unit tests (Red-Green-Refactor).
3. Run `npx playwright test`.

## 4. Operational Procedures
- Nightly regression suite runs.

## 5. Maintenance & Safety
- Flaky tests must be quarantined or fixed immediately.

