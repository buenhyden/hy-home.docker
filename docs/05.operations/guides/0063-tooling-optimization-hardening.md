---
title: "Platform Operations and Quality Optimization Hardening Usage Guide"
version: "1.0.3"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0063"
parent_ids:
- "POL-0063"
created: "2026-05-17"
---

# Platform Operations and Quality Optimization Hardening Usage Guide

## Usage

### Overview

이 문서는 `09-platform-ops`·`11-quality`의 최적화/하드닝 변경을 운영자와 개발자가 재현 가능하게 적용하기 위한 가이드다. 공개 경계 보안, 네트워크 경계 표준화, 테스트 도구 안정성 계약, 검증 절차를 제공한다.

### Usage Type

`system-guide | how-to`

### Target Audience

- SRE / Platform Operator
- DevOps Engineer
- Platform Product Owner

### Purpose

- SonarQube/Terrakube 경로를 gateway+SSO 정책에 정렬한다.
- tooling compose 네트워크 경계를 일관화한다.
- root k6와 독립 Locust LAB 테스트 런타임 계약을 안정화한다.
- tooling 하드닝 회귀를 script/CI로 조기 차단한다.
- 카탈로그 확장 항목을 운영 실행 가능한 로드맵으로 반영한다.

### Prerequisites

- Docker / Docker Compose 실행 환경
- `infra/09-platform-ops` 및 `infra/11-quality` 수정 권한
- Traefik middleware(`gateway-standard-chain`, `sso-errors`, `sso-auth`) 준비

### Step-by-step Instructions

실행 순서와 실패·복구 판단은 [런북](../runbooks/0063-tooling-optimization-hardening.md)의 `검토된 하드닝 변경 순서` 절차를 따른다. 데이터와 권한 경계는 해당 정책을 유지한다.

### Common Pitfalls

- 공개 라우터에 SSO 체인을 누락하는 실수
- service-local compose 단독 config 실패를 root compose context와 구분하지 못하는 실수
- 독립 LAB Locust worker health 상태를 root profile 검사로 오인하는 실수
- k6 leaf에 존재하지 않는 worker 또는 Traefik route를 문서화하는 실수

## Common Checks

- `bash scripts/hardening/check-all-hardening.sh 09-platform-ops 11-quality`
- `bash scripts/validation/check-template-security-baseline.sh`
- `python3 scripts/validation/check-document-links.py --mode traceability`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0063-tooling-optimization-hardening.md)을 따른다.

## Traceability

- 상위 문서: [Platform Operations and Quality Optimization Hardening Operations Policy](../policies/0063-tooling-optimization-hardening.md) (`POL-0063`)
- 설계 근거: [Platform Operations·Quality 아키텍처](../../02.architecture/descriptions/0009-tooling-architecture.md) (`AD-0009`)
- 동일 주제 문서: [Policy](../policies/0063-tooling-optimization-hardening.md) (`POL-0063`), [Runbook](../runbooks/0063-tooling-optimization-hardening.md) (`RUN-0063`)

현재 IaC helper는 OpenTofu다. 기존 Terraform workspace는 [migration handoff](0068-terraform.md)를 따른다. Syncthing runtime은 제거되었으며 현재 하드닝 기동 대상에 포함하지 않는다.

## Related Documents

- 실행 버전의 원본은 Compose/Dockerfile 선언이며, [파생 버전 목록](../../../infra/tech-stack.versions.json)은 변경 누락 검증에 사용한다.

- [Operations index](../README.md)
- [Operations policy](../policies/0063-tooling-optimization-hardening.md)
- [Recovery runbook](../runbooks/0063-tooling-optimization-hardening.md)
