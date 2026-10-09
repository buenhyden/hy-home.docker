---
title: "Administration and Experimentation Hardening Usage Guide"
version: "1.0.2"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "GDE-0074"
parent_ids:
- "POL-0074"
created: "2026-05-17"
---

# Administration and Experimentation Hardening Usage Guide

## Overview

이 가이드는 Data·Observability·AI·Analytics tier에 흩어진 관리·실험 기능(dozzle, redisinsight,
open-notebook, mlflow, jupyterlab)의 최적화·하드닝 변경을 재현 가능하게 적용하는 기준이다.
관리 UI 보안 경계, 네트워크 표준화, 최소권한 적용, 기준선 검증 절차를 다룬다.
`system-guide | how-to` 유형이다.

## Audience and Goal

대상 독자는 Platform SRE, DevOps Engineer, Security Reviewer다. 목표는 다음과 같다.

- 관리 UI를 서비스별 gateway·allowlist·인증 경계로 정렬한다.
- 제거된 dashboard의 직접 노출을 다시 만들지 않는다. 현재 서비스의 승인된 loopback 경계는 개별 정책을 따른다.
- Dozzle의 socket read-only 마운트를 유지하되 Docker API 권한 통제로 보지 않는다.
- open-notebook UI route를 승인된 allowlist+large-body+앱 비밀번호 경계로 보호하고 secret-file 주입을 유지한다.
- 하드닝 회귀를 script와 CI로 일찍 막는다.

## Usage

### 사전 조건

- Docker와 Docker Compose 실행 환경
- 변경 대상 Data·Observability·AI·Analytics 패키지의 수정 권한
- Traefik middleware(`gateway-standard-chain`, `sso-errors`, `sso-auth`) 준비

실행 순서와 실패·복구 판단은 [런북](../runbooks/0074-laboratory-optimization-hardening.md)의 `검토된 하드닝 변경 순서` 절차를 따른다. 데이터와 권한 경계는 해당 정책을 유지한다.

### 흔한 실수

- allowlist CIDR 설정을 빠뜨려 운영자 접근이 막힌다.
- dashboard direct 포트 노출을 되돌려 우회 경로를 만든다.
- dozzle socket 권한을 read-write로 둔다.
- 문서 링크와 README 인덱스 동기화를 빠뜨린다.
- service-local standalone compose render를 root readiness 증거로 오해한다.

### Common Checks

- `bash scripts/hardening/check-all-hardening.sh 04-data 06-observability 08-ai 12-analytics`
- `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/validation/check-template-security-baseline.sh`
- `python3 scripts/validation/check-document-links.py --mode traceability`

### Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0074-laboratory-optimization-hardening.md)을 따른다.

### Traceability

- 상위 문서: [Administration and Experimentation Hardening Operations Policy](../policies/0074-laboratory-optimization-hardening.md) (`POL-0074`)
- 설계 근거: [Administration and Experimentation Architecture Description](../../02.architecture/descriptions/0011-laboratory-architecture.md) (`AD-0011`)
- 동일 주제 문서: [Policy](../policies/0074-laboratory-optimization-hardening.md) (`POL-0074`), [Runbook](../runbooks/0074-laboratory-optimization-hardening.md) (`RUN-0074`)

## Related Documents

- 실행 버전의 원본은 Compose/Dockerfile 선언이며, [파생 버전 목록](../../../infra/tech-stack.versions.json)은 변경 누락 검증에 사용한다.

- [Operations index](../README.md)
- [Operations policy](../policies/0074-laboratory-optimization-hardening.md)
- [Recovery runbook](../runbooks/0074-laboratory-optimization-hardening.md)
