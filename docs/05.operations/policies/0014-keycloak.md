---
title: "02-Auth Keycloak Operations Policy"
version: "1.0.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "POL-0014"
parent_ids:
- "AD-0002"
created: "2026-05-17"
---

# 02-Auth Keycloak Operations Policy

## Overview

이 문서는 `02-auth` Keycloak 운영 정책을 정의한다. DB/관리자 시크릿 처리, readiness 검증, 변경 통제 기준을 명시한다.

## Policy Scope

- `infra/02-auth/keycloak/docker-compose.yml`
- Keycloak secret injection and healthcheck contract
- Realm/client 운영 변경 승인 정책

- **Systems**: Keycloak (Quarkus)
- **Agents**: Infra/DevOps/Ops agents
- **Environments**: Local, Dev, Stage, Production-like

## Controls

- **Required**:
  - Keycloak은 `template-infra-high`를 사용한다.
  - DB/Admin 비밀은 `/run/secrets` 파일에서 읽어 환경 변수로 주입한다.
  - readiness healthcheck(`/health/ready`)를 유지한다.
  - 시크릿 길이/값 등 민감한 디버그 출력은 금지한다.
- **Allowed**:
  - 기동 안정화를 위한 healthcheck 타이밍 조정
  - 운영 승인 하의 realm/client 설정 변경
- **Disallowed**:
  - 시크릿 평문 하드코딩
  - 인증 우회 목적 설정 변경

### AI Agent Policy

- **Model / Prompt Change Process**: N/A
- **Eval / Guardrail Threshold**: check-all-hardening.sh 02-auth 실패 0건
- **Log / Trace Retention**: 인증 로그 보존 정책은 관측성 기준 준수
- **Safety Incident Thresholds**: readiness 실패 지속, 로그인 실패 급증, realm 설정 오류 시 런북 절차 수행

## Exceptions

- 긴급 장애 대응 시 임시 설정 변경은 가능하나, 동일 작업 윈도우 내 원복 계획과 변경 기록을 남겨야 한다.

## Verification

- `bash scripts/hardening/check-all-hardening.sh 02-auth`
- `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`

### Backup and Upgrade Controls

- `mng-pg`의 Keycloak database를 권위 백업으로 취급한다. realm export만으로
  사용자, 세션, 자격 증명, 실행 중 변경의 완전한 복구를 주장하지 않는다.
- 일관된 export가 필요하면 공식 offline 절차에 따라 모든 Keycloak node를
  중지한다. 실행 중 export를 database backup 대체물로 쓰지 않는다.
- 백업 접근, 관리자 password, database password, client secret은 각 secret
  owner가 보관하며 문서나 증거에 값을 복사하지 않는다.
- upgrade 전에 복구 가능한 database backup을 확인하고 격리 복제본에서 migration과
  대표 OIDC 흐름을 검증한다. rollback에는 이전 image와 이전 database가 함께 필요하다.

## Review Cadence

- 월 1회 정기 점검
- Keycloak 버전/realm 정책 변경 시 수시 점검

## Traceability

- Declared parent: [02-Auth Architecture Description](../../02.architecture/descriptions/0002-auth-architecture.md) (`AD-0002`)
- Subject peers: [Guide](../guides/0014-keycloak.md) (`GDE-0014`), [Runbook](../runbooks/0014-keycloak.md) (`RUN-0014`)

## Related Documents

- [Official upstream operational documentation](https://www.keycloak.org/server/containers)

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../infra/tech-stack.versions.json) provides drift verification.

- [Operations index](../README.md)
- [Usage guide](../guides/0014-keycloak.md)
- [Recovery runbook](../runbooks/0014-keycloak.md)
