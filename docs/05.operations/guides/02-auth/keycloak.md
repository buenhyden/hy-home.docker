# 02-Auth Keycloak Operations Policy

## Overview (KR)

이 문서는 `02-auth` Keycloak 운영 정책을 정의한다. DB/관리자 시크릿 처리, readiness 검증, 변경 통제 기준을 명시한다.

## Policy Scope

- `infra/02-auth/keycloak/docker-compose.yml`
- Keycloak secret injection and healthcheck contract
- Realm/client 운영 변경 승인 정책

## Applies To

- **Systems**: Keycloak (Quarkus)
- **Agents**: Infra/DevOps/Ops agents
- **Environments**: Local, Dev, Stage, Production-like

## Controls

- **Required**:
  - Keycloak은 `template-infra-med`를 사용한다.
  - DB/Admin 비밀은 `/run/secrets` 파일에서 읽어 환경 변수로 주입한다.
  - readiness healthcheck(`/health/ready`)를 유지한다.
  - 시크릿 길이/값 등 민감한 디버그 출력은 금지한다.
- **Allowed**:
  - 기동 안정화를 위한 healthcheck 타이밍 조정
  - 운영 승인 하의 realm/client 설정 변경
- **Disallowed**:
  - 시크릿 평문 하드코딩
  - 인증 우회 목적 설정 변경

## Exceptions

- 긴급 장애 대응 시 임시 설정 변경은 가능하나, 동일 작업 윈도우 내 원복 계획과 변경 기록을 남겨야 한다.

## Verification

- `bash scripts/check-auth-hardening.sh`
- `docker compose -f infra/02-auth/keycloak/docker-compose.yml config`

## Review Cadence

- 월 1회 정기 점검
- Keycloak 버전/realm 정책 변경 시 수시 점검

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: N/A
- **Eval / Guardrail Threshold**: auth-hardening 스크립트 실패 0건
- **Log / Trace Retention**: 인증 로그 보존 정책은 관측성 기준 준수
- **Safety Incident Thresholds**: readiness 실패 지속, 로그인 실패 급증, realm 설정 오류 시 런북 절차 수행

## Related Documents

- **Plan**: [../../04.execution/plans/2026-03-28-02-auth-optimization-hardening-plan.md](../../../04.execution/plans/2026-03-28-02-auth-optimization-hardening-plan.md)
- **Task**: [../../04.execution/tasks/2026-03-28-02-auth-optimization-hardening-tasks.md](../../../04.execution/tasks/2026-03-28-02-auth-optimization-hardening-tasks.md)
- **Spec**: [../../03.specs/02-auth/spec.md](../../../03.specs/02-auth/spec.md)
- **Procedure**: [../../05.operations/02-auth/keycloak.md](./keycloak.md)
- **Usage**: [../../05.operations/02-auth/keycloak.md](./keycloak.md)

## Usage

> Migrated from `docs/05.operations/02-auth/keycloak.md` during the 2026-05-10 operations taxonomy consolidation.

### 02-Auth Keycloak Usage

#### Overview (KR)

이 문서는 `02-auth`의 Keycloak 운영 구성 방법을 설명한다. DB/관리자 시크릿 주입 방식, 헬스체크 점검, OIDC 클라이언트 정합 확인 절차를 중심으로 다룬다.

#### Usage Type

`system-guide | how-to`

#### Target Audience

- Infra/DevOps Engineers
- Operators
- Contributors

#### Purpose

- Keycloak의 시크릿/헬스체크 계약을 안정적으로 유지한다.
- OAuth2 Proxy 연동을 위한 OIDC issuer/redirect 정합성을 보장한다.

#### Prerequisites

- Docker/Docker Compose 사용 가능
- `infra/02-auth/keycloak/docker-compose.yml` 접근 가능
- `mng-pg` 서비스 준비됨

#### Step-by-step Instructions

1. Compose 설정 확인
   - `service: template-infra-med` 적용 여부 확인
   - `KC_DB_PASSWORD_FILE`, `keycloak_db_password`, `keycloak_admin_password` 연결 확인
2. 헬스체크 계약 확인
   - 관리 포트 readiness 체크(`/health/ready`) 설정 확인
3. OIDC 발급자 URL 확인
   - Realm issuer와 OAuth2 Proxy `OAUTH2_PROXY_OIDC_ISSUER_URL`가 동일한 도메인 규칙을 따르는지 확인
4. 정적 검증
   - `docker compose -f infra/02-auth/keycloak/docker-compose.yml config`
   - `bash scripts/check-auth-hardening.sh`

#### Common Pitfalls

- Keycloak realm URL과 OAuth2 Proxy issuer URL 불일치
- DB 시크릿 파일 경로 오타
- 초기 기동 시간보다 짧은 헬스체크 판단으로 인한 오탐

#### Related Documents

- **Spec**: [../../03.specs/02-auth/spec.md](../../../03.specs/02-auth/spec.md)
- **Operation**: [../../05.operations/02-auth/keycloak.md](./keycloak.md)
- **Procedure**: [../../05.operations/02-auth/keycloak.md](./keycloak.md)
- **Plan**: [../../04.execution/plans/2026-03-28-02-auth-optimization-hardening-plan.md](../../../04.execution/plans/2026-03-28-02-auth-optimization-hardening-plan.md)

## Procedure

> Migrated from `docs/05.operations/02-auth/keycloak.md` during the 2026-05-10 operations taxonomy consolidation.

### 02-Auth Keycloak Procedure

: Keycloak Runtime Recovery

#### Overview (KR)

이 런북은 Keycloak readiness 실패, DB 연결 오류, 시크릿 회전 후 인증 장애 상황의 복구 절차를 정의한다.

#### Purpose

- Keycloak 가용성을 빠르게 복구한다.
- 시크릿/설정 회귀 시 안전하게 롤백한다.

#### Canonical References

- [Operations Policy](./keycloak.md)
- [Plan](../../../04.execution/plans/2026-03-28-02-auth-optimization-hardening-plan.md)
- [Tasks](../../../04.execution/tasks/2026-03-28-02-auth-optimization-hardening-tasks.md)

#### When to Use

- `/health/ready` 실패 지속
- DB 인증 오류 또는 연결 오류
- 관리자/DB 비밀 회전 직후 로그인 실패

#### Procedure or Checklist

##### Checklist

- [ ] `docker compose -f infra/02-auth/keycloak/docker-compose.yml config` 성공
- [ ] `bash scripts/check-auth-hardening.sh` 결과 확인
- [ ] `docker compose ps`에서 `keycloak`, `mng-pg` 상태 확인

##### Procedure

1. 설정/로그 확인
   - `docker logs keycloak --tail=200`
   - `docker compose -f infra/02-auth/keycloak/docker-compose.yml config`
2. readiness 실패 대응
   - DB 연결 상태 확인(`mng-pg` 로그/상태)
   - Keycloak 재기동: `docker compose -f infra/02-auth/keycloak/docker-compose.yml up -d keycloak`
3. 시크릿 회전 장애 대응
   - `/run/secrets/keycloak_admin_password`, `/run/secrets/keycloak_db_password` 파일 존재와 mount 상태 확인
   - secret 값은 출력하지 않고 환경 변수/secret 파일 매핑 오타, rotation timestamp, 관련 서비스 재시작 여부 점검
4. 사후 검증
   - readiness 재확인
   - OAuth2 Proxy 연동 로그인 테스트

#### Verification Steps

- [ ] `bash scripts/check-auth-hardening.sh` 통과
- [ ] `docker exec keycloak sh -c 'exec 3<>/dev/tcp/127.0.0.1/9000; printf \"GET /health/ready HTTP/1.1\\r\\nHost: localhost\\r\\nConnection: close\\r\\n\\r\\n\" >&3; cat <&3'`에서 `\"status\":\"UP\"` 확인

#### Observability and Evidence Sources

- **Signals**: readiness 상태, Keycloak 로그의 DB/OIDC 오류
- **Evidence to Capture**:
  - `docker logs keycloak --tail=200`
  - `check-auth-hardening.sh` 실행 결과

#### Safe Rollback or Recovery Procedure

- [ ] 직전 정상 커밋으로 `infra/02-auth/keycloak/docker-compose.yml` 복원
- [ ] `docker compose -f infra/02-auth/keycloak/docker-compose.yml up -d keycloak`
- [ ] readiness 및 로그인 플로우 재검증

#### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: N/A
- **Eval Re-run**: `bash scripts/check-auth-hardening.sh`
- **Trace Capture**: Keycloak 로그 + CI job 로그

#### Related Operational Documents

- **Usage**: [../../05.operations/02-auth/keycloak.md](./keycloak.md)
- **OAuth2 Proxy Procedure**: [./oauth2-proxy.md](./oauth2-proxy.md)
