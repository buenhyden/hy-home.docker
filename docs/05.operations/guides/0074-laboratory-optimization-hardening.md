---
title: "Administration and Experimentation Hardening Usage Guide"
version: "1.0.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0074"
parent_ids:
- "POL-0074"
created: "2026-05-17"
---

# Administration and Experimentation Hardening Usage Guide

## Usage

### Overview

이 문서는 여러 tier의 관리·실험 기능 최적화/하드닝 변경을 운영자와 개발자가 재현 가능하게 적용하기 위한 가이드다. 관리 UI 보안 경계, 네트워크 표준화, 최소권한 적용, 기준선 검증 절차를 제공한다.

### Usage Type

`system-guide | how-to`

### Target Audience

- Platform SRE
- DevOps Engineer
- Security Reviewer

### Purpose

- 관리 UI를 서비스별 gateway·allowlist·인증 경계로 정렬한다.
- 제거된 dashboard의 직접 노출을 재도입하지 않는다. 현재 서비스의 승인된 loopback 경계는 개별 정책을 따른다.
- Dozzle의 socket read-only 마운트를 유지하되 Docker API 권한 통제로 간주하지 않는다.
- open-notebook UI route를 승인된 allowlist+large-body+앱 비밀번호 경계로 보호하고 secret-file 주입을 유지한다.
- laboratory 하드닝 회귀를 script/CI로 조기 차단한다.

### Prerequisites

- Docker / Docker Compose 실행 환경
- 변경 대상 Data·Observability·AI·Analytics 패키지의 수정 권한
- Traefik middleware(`gateway-standard-chain`, `sso-errors`, `sso-auth`) 준비

### Step-by-step Instructions

실행 순서와 실패·복구 판단은 [런북](../runbooks/0074-laboratory-optimization-hardening.md)의 `검토된 하드닝 변경 순서` 절차를 따른다. 데이터와 권한 경계는 해당 정책을 유지한다.

### Common Pitfalls

- allowlist CIDR 설정 누락으로 운영자 접근이 차단되는 실수
- dashboard direct 포트 노출을 되돌려 우회 경로를 만드는 실수
- dozzle socket 권한을 read-write로 유지하는 실수
- 문서 링크/README 인덱스 동기화를 누락하는 실수
- service-local standalone compose render를 root readiness evidence로 오해하는 실수

## Common Checks

- `bash scripts/hardening/check-all-hardening.sh 04-data 06-observability 08-ai 12-analytics`
- `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/validation/check-template-security-baseline.sh`
- `python3 scripts/validation/check-document-links.py --mode traceability`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0074-laboratory-optimization-hardening.md)을 따른다.

## Traceability

- 상위 문서: [Administration and Experimentation Hardening Operations Policy](../policies/0074-laboratory-optimization-hardening.md) (`POL-0074`)
- 설계 근거: [Administration and Experimentation Architecture Description](../../02.architecture/descriptions/0011-laboratory-architecture.md) (`AD-0011`)
- 동일 주제 문서: [Policy](../policies/0074-laboratory-optimization-hardening.md) (`POL-0074`), [Runbook](../runbooks/0074-laboratory-optimization-hardening.md) (`RUN-0074`)

## Related Documents

- 실행 버전의 원본은 Compose/Dockerfile 선언이며, [파생 버전 목록](../../../infra/tech-stack.versions.json)은 변경 누락 검증에 사용한다.

- [Operations index](../README.md)
- [Operations policy](../policies/0074-laboratory-optimization-hardening.md)
- [Recovery runbook](../runbooks/0074-laboratory-optimization-hardening.md)
