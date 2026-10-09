---
title: "Platform Operations and Quality Optimization Hardening Usage Guide"
version: "1.0.4"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "GDE-0063"
parent_ids:
- "POL-0063"
created: "2026-05-17"
---

# Platform Operations and Quality Optimization Hardening Usage Guide

## Overview

이 가이드는 `09-platform-ops`와 `11-quality`의 최적화·하드닝 변경을 재현 가능하게 적용하는 기준이다.
공개 경계 보안, 네트워크 경계 표준화, 테스트 도구 안정성 계약, 검증 절차를 다룬다.
`system-guide | how-to` 유형이다.

## Audience and Goal

대상 독자는 SRE/Platform Operator, DevOps Engineer, Platform Product Owner다.
목표는 다음과 같다.

- SonarQube와 Terrakube 경로를 gateway+SSO 정책에 맞춘다.
- tooling compose의 네트워크 경계를 일관되게 유지한다.
- root `k6`와 독립 Locust LAB의 테스트 런타임 계약을 안정화한다.
- 하드닝 회귀를 script와 CI로 일찍 막는다.
- 카탈로그 확장 항목을 실행 가능한 로드맵으로 반영한다.

## Usage

### 사전 조건

- Docker와 Docker Compose 실행 환경
- `infra/09-platform-ops`와 `infra/11-quality`의 수정 권한
- Traefik middleware(`gateway-standard-chain`, `sso-errors`, `sso-auth`) 준비

실행 순서와 실패·복구 판단은 [런북](../runbooks/0063-tooling-optimization-hardening.md)의 `검토된 하드닝 변경 순서` 절차를 따른다. 데이터와 권한 경계는 해당 정책을 유지한다.

### 흔한 실수

- 공개 라우터에 SSO 체인을 빠뜨린다.
- service-local compose의 단독 config 실패를 root compose context와 구분하지 못한다.
- 독립 LAB Locust worker의 health 상태를 root profile 검사로 오해한다.
- k6 leaf에 없는 worker나 Traefik route를 문서에 적는다.

### Common Checks

- `bash scripts/hardening/check-all-hardening.sh 09-platform-ops 11-quality`
- `bash scripts/validation/check-template-security-baseline.sh`
- `python3 scripts/validation/check-document-links.py --mode traceability`

### Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0063-tooling-optimization-hardening.md)을 따른다.

### Traceability

- 상위 문서: [Platform Operations and Quality Optimization Hardening Operations Policy](../policies/0063-tooling-optimization-hardening.md) (`POL-0063`)
- 설계 근거: [Platform Operations·Quality 아키텍처](../../02.architecture/descriptions/0009-tooling-architecture.md) (`AD-0009`)
- 동일 주제 문서: [Policy](../policies/0063-tooling-optimization-hardening.md) (`POL-0063`), [Runbook](../runbooks/0063-tooling-optimization-hardening.md) (`RUN-0063`)

현재 IaC helper는 OpenTofu다. 기존 Terraform workspace는 [migration handoff](0068-terraform.md)를 따른다. Syncthing runtime은 제거되었으며 현재 하드닝 기동 대상에 포함하지 않는다.

## Related Documents

- 실행 버전의 원본은 Compose/Dockerfile 선언이며, [파생 버전 목록](../../../infra/tech-stack.versions.json)은 변경 누락 검증에 사용한다.

- [Operations index](../README.md)
- [Operations policy](../policies/0063-tooling-optimization-hardening.md)
- [Recovery runbook](../runbooks/0063-tooling-optimization-hardening.md)
