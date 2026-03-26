# Task: Security Documentation Standardization

## Overview (KR)

이 문서는 Security 티어(`03-security`)의 문서 체계를 표준화하는 작업의 구현·검증 작업 목록이다. Vault 서버 및 에이전트 구성을 포함한 PRD, ARD, ADR, Spec, Plan의 생성 및 리팩토링 작업을 추적 가능하게 기록한다.

## Inputs

- **Parent Spec**: `[../04.specs/03-security/spec.md]`
- **Parent Plan**: `[../05.plans/2026-03-26-03-security-standardization.md]`

## Working Rules

- 모든 문서는 `docs/99.templates/`의 표준 템플릿을 준수해야 한다.
- 모든 문서 작업 후에는 상대 경로 링크의 무결성을 검증한다.
- 레이어별 `README.md`는 `readme.template.md`를 기반으로 리팩토링한다.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| T-001 | Security PRD 생성 및 레벨 README 리팩토링 | doc | §1 | Phase 1 | `ls docs/01.prd/` | Done |
| T-002 | Security ARD 생성 및 레벨 README 리팩토링 | doc | §1 | Phase 1 | `ls docs/02.ard/` | Done |
| T-003 | Security ADR 생성 및 레벨 README 리팩토링 | doc | §1 | Phase 1 | `ls docs/03.adr/` | Done |
| T-004 | Security Spec 생성 및 레벨 README 리팩토링 | doc | §1 | Phase 2 | `ls docs/04.specs/03-security/` | Done |
| T-005 | Security Plan 생성 및 레벨 README 리팩토링 | doc | §1 | Phase 2 | `ls docs/05.plans/` | Done |
| T-006 | Security Task 문서 생성 및 레벨 README 리팩토링 | doc | §1 | Phase 3 | `ls docs/06.tasks/` | In Progress |

## Verification Summary

- **Test Commands**: `ls -R docs/`, `grep` for Mandatory Sections.
- **Evidence Location**: `docs/01.prd/`, `docs/02.ard/`, `docs/03.adr/`, `docs/04.specs/03-security/`, `docs/05.plans/`, `docs/06.tasks/`.
