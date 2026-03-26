# Keycloak Operations Policy

> Identity & Access Management Governance (02-auth)

---

## Overview (KR)

이 문서는 `hy-home.docker` 플랫폼의 중앙 인증 시스템인 Keycloak의 운영 정책을 정의한다. 아이덴티티 관리의 일관성, 보안 통제 기준, 그리고 운영 규준을 명시한다.

## Policy Scope

- Keycloak 서비스 인스턴스 (Quarkus distribution)
- 렐름(Realm) 구성 및 관리 권한
- 클라이언트(Client) 등록 및 시크릿 관리 정책
- 사용자 데이터 및 감사 로그(Audit Log) 보존

## Applies To

- **Systems**: Keycloak Container, PostgreSQL (Auth Data)
- **Agents**: Identity-aware agents, Audit agents
- **Environments**: Production, Staging, Local Development

## Controls

- **Required**:
  - 모든 외부 접속은 Traefik을 통한 HTTPS(TLS 1.2+) 필수.
  - 관리자 접근은 전용 관리 네트워크 또는 지정된 IP에서만 허용 (권장).
  - 렐름당 최소 1회 이상의 정기 설정 백업 (JSON export).
- **Allowed**:
  - `hy-home.realm` 내의 신규 클라이언트 생성 (운영팀 승인 시).
  - 커스텀 테마를 통한 브랜드 아이덴티티 적용.
- **Disallowed**:
  - `master` 렐름에 직접적인 서비스 클라이언트 등록 금지.
  - 컨테이너 내 root 권한으로 프로세스 실행 금지.

## Exceptions

- 로컬 개발 환경에서는 HTTP 접속 허용.
- 응급 복구 시 `bootstrap-admin`을 통한 임시 계정 생성 허용.

## Verification

- `keycloak/health/live` 및 `keycloak/health/ready` 엔드포인트 상시 모니터링.
- 월간 감사 로그 검토 (비정상 로그인 시도 확인).

## Review Cadence

- Quarterly (분기별 정책 및 권한 검토)

## Related Documents

- **ARD**: `[../../docs/02.ard/02-auth-architecture.md]`
- **Runbook**: `[../../docs/09.runbooks/02-auth/keycloak.md]`
- **Postmortem**: `[../../docs/11.postmortems/README.md]`
