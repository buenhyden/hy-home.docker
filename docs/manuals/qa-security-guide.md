# QA & Security Guide

*Target Directory: `docs/manuals/qa-security-guide.md`*
*Description: This document defines the team's quantitative and qualitative standards for testing, code quality, and application security.*

## 1. Quality & Test Checklist

| Category | Check Question | Priority | Notes / Agreements |
| --- | --- | --- | --- |
| **Test Strategy** | Are the test levels (Unit/Integration/E2E/Load) and boundaries defined? | **Mandatory** | |
| **Test Tools** | Are the test framework (e.g., Pytest/Jest), runner, and mock strategies agreed upon? | **Mandatory** | |
| **Coverage Policy** | Is the code coverage target (e.g., total 80%, new lines 100%) numerically defined? | **Mandatory** | |
| **Coverage Gate** | Is the CI/PR failure criteria clear if coverage falls below the target? | **Mandatory** | |
| **Static Analysis (Lint)** | Which Linter, rule set, and auto-format tools are being used? | **Mandatory** | |
| **Style Guide** | Are code style conventions (naming, folder structure, module splitting) documented? | *Optional* | |
| **Code Complexity** | Is there an agreed-upon limit for cyclomatic complexity or file size? | *Optional* | |

## 2. Security & Data Checklist

| Category | Check Question | Priority | Notes / Agreements |
| --- | --- | --- | --- |
| **Security Baseline** | Are minimum checks (secret detection, dependencies, SAST) defined in CI? | **Mandatory** | |
| **AuthN & AuthZ** | Is the Authentication and Authorization architecture (Token, OAuth, RBAC) fully designed? | **Mandatory** | |
| **Data Protection** | Are sensitive data encryption, masking, and access permission policies established? | **Mandatory** | |
| **Security Review** | Is there a mandatory security review process for major features/releases? | *Optional* | |

## 3. Custom QA / Security Rules

[List any project-specific security rules, additional compliance mandates, or custom linters here.]
