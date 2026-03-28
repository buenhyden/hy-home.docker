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

- **Plan**: [../../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md](../../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md)
- **Task**: [../../06.tasks/2026-03-28-02-auth-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-02-auth-optimization-hardening-tasks.md)
- **Spec**: [../../04.specs/02-auth/spec.md](../../04.specs/02-auth/spec.md)
- **Runbook**: [../../09.runbooks/02-auth/keycloak.md](../../09.runbooks/02-auth/keycloak.md)
- **Guide**: [../../07.guides/02-auth/keycloak.md](../../07.guides/02-auth/keycloak.md)
