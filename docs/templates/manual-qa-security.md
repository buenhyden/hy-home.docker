---
title: 'QA & Security Manual'
status: 'Active | Draft'
version: 'v1.0.0'
date: 'YYYY-MM-DD'
owner: 'buenhyden'
layer: 'common'
tags: ['manual', 'qa', 'security']
---

# QA & Security Manual

> **Status**: [Active | Draft]
> **Version**: v1.0.0
> **Date**: YYYY-MM-DD
> **Layer**: common
> **Review Cycle**: Quarterly

**Overview (KR):** [팀의 코드 품질 기준, 테스트 피라미드 전략, 그리고 애플리케이션 보안 체크리스트에 대한 약속을 한국어로 1-2문장 요약하세요.]

---

## 1. Test Strategy (The Pyramid)

| Level | Coverage Target | Tools |
| ----- | --------------- | ----- |
| **Unit** | > 80% | Jest / Vitest |
| **Integration** | Critical Paths | Supertest / Playwright |
| **E2E** | Key User Flows | Playwright |

---

## 2. Security Baseline

### 2.1. Static Analysis (SAST)

* Tool: [e.g., SonarQube / GitHub CodeQL]
* Frequency: Every PR

### 2.2. Dependency Audit

* Tool: [e.g., Snyk / npm audit]
* Policy: No Zero-day criticals allowed in `main`.

---

## 3. Data Privacy & Compliance

* **PII Handling**: [e.g., Scrubbing logs, encryption at rest]
* **Auth Standards**: [e.g., OAuth2 / OIDC]

---

## 4. Quality Gates

* **PR Gate**:
  * Lint checks must pass.
  * Build must be successful.
  * No regression in coverage.

---

## 5. Incident & Vulnerability Handling

* **SLA**: Critical fixed in 24h, High in 1 week.
* **Reporting**: [Where to report security issues]
