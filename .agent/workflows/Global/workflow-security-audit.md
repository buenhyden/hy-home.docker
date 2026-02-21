---
description: AI Security/QA Agent logic for periodic vulnerability scanning and compliance checks.
---

# Workflow: Security & Quality Audit

This workflow defines the execution loop for the **Security/QA Agent** when triggered on a schedule (e.g., weekly) or prior to a major release.

## 1. Static Analysis (SAST) & Linter Checks

1. Run all project linters (`eslint`, `ruff`, `flake8`, etc.) to enforce the rules in `0140-engineering-excellence-standard.md`.
2. Run Static Application Security Testing (SAST) tools like `Bandit` (Python), `SonarQube`, or `CodeQL`.
3. Analyze the results. If critical or high-severity (e.g., SQLi, XSS) issues are found, explicitly halt the audit and fail the CI pipeline.

## 2. Dependency & Secret Scanning

1. Check dependencies against a known CVE database (e.g., `npm audit`, `pip-audit`, or Dependabot).
2. Scan the repository for accidentally committed secrets using tools like `Gitleaks` or `TruffleHog` to enforce `2211-auth-protocol.md`.
3. Verify that new dependencies conform to the open-source license policy of the organization.

## 3. Dynamic Analysis (DAST) & OWASP Top 10

1. If available in the environment, initiate a Dynamic Application Security Testing (DAST) suite (e.g., OWASP ZAP) against the staging deployment.
2. Cross-reference the application's configuration against `2204-security-owasp.md` manually (e.g., checking HTTP security headers: CSP, HSTS).

## 4. Audit Report Generation

1. Consolidate all findings from SAST, DAST, and dependency scans.
2. Format the findings against the security checklist defined in `2207-security-checklist.md`.
3. Create a Jira issue or GitHub Issue for every high/critical finding.
4. Notify the human engineering team with the final audit report, linking to the generated issues.
