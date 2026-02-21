# QA & Security Guide

*Target Directory: `docs/manuals/qa-security-guide.md`*
*Description: This document defines the team's quantitative and qualitative standards for testing, code quality, and application security, as per the `0700-testing-and-qa-standard.md` and `2200-security-pillar` rules.*

---

## 1. Quality & Test Strategy

Please fill out the following quality agreements before initiating significant development work to ensure adherence to the Testing Pyramid and CI/CD quality gates.

| Category | Check Question | Expected Standard (Rule) | Notes / Agreements |
| --- | --- | --- | --- |
| **Test Strategy** | Are the test levels (Unit/Integration/E2E/Load) and boundaries defined? | **Mandatory** | |
| **Test Tools** | Are the test framework, runner, and mock strategies agreed upon? | **Mandatory** | |
| **Coverage Policy** | Is the code coverage target numerically defined? | **Mandatory (> 80%)** | |
| **Coverage Gate** | Is the CI/PR failure criteria clear if coverage falls below the target? | **Mandatory** | |
| **Test Isolation** | Are setup/teardown mechanisms agreed upon to prevent flaky tests? | **Mandatory** | |
| **Static Analysis** | Which Linter, rule set, and auto-format tools are being used? | **Mandatory** | |
| **Style Guide** | Are code style conventions (naming, folder structure) documented? | *Optional* | |

## 2. Security & Data Baseline

Please fill out the following security agreements to ensure compliance with the Security Master Checklist (`2207-security-checklist.md`).

| Category | Check Question | Expected Standard (Rule) | Notes / Agreements |
| --- | --- | --- | --- |
| **Security Baseline** | Are minimum checks (secret detection, SAST, dependency audit) defined in CI? | **Mandatory** | |
| **AuthN & AuthZ** | Is the Authentication and Authorization architecture (Token, OAuth, RBAC) fully designed? | **Mandatory** | |
| **Input Validation** | Is parameterization enforced for 100% of DB queries and execution sinks? | **Mandatory** | |
| **Data Protection** | Are sensitive data (PII) encryption, masking, and access permission policies established? | **Mandatory** | |
| **AI Safety** | If using LLMs, are prompt delimiting and PII scrubbing rules established? | **Mandatory (If applicable)** | |
| **Security Review** | Is there a mandatory security review process for major features/releases? | *Optional* | |

## 3. Performance & Accessibility Baseline

Please fill out the following performance and accessibility agreements to ensure compliance with the Performance (`1060-performance.md`) and Localization/A11y (`1070-a11y-details.md`) rules.

| Category | Check Question | Expected Standard (Rule) | Notes / Agreements |
| --- | --- | --- | --- |
| **Performance Budgets** | Are Core Web Vitals (LCP, CLS, INP) targets defined for critical paths? | **Mandatory** | |
| **Accessibility (A11y)** | Are WCAG AA requirements (contrast, ARIA) included in the DoD? | **Mandatory** | |
| **A11y Verification** | Which automated QA tools (Axe/Lighthouse) are used in CI? | **Mandatory** | |

## 4. Custom QA / Security Rules

[List any project-specific security rules, additional compliance mandates, or custom linters here.]

- **Dependency Update Policy**: [e.g., Dependabot weekly, auto-merge patch versions]
- **Penetration Testing**: [e.g., Annual external audit]
- **Vulnerability SLA**: [e.g., Critical bugs fixed within 24 hours]
