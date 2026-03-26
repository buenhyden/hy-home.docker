# Keycloak Operations Policy

> Operational and security policies for the central identity and access management system (02-auth).

---

## Overview (KR)

이 문서는 Keycloak IAM 서버의 운영 정책을 정의한다. 사용자 계정 관리, 렐름(Realm) 및 클라이언트 설정의 변경 통제, 그리고 보안 감사(Audit Logging) 기준을 규정하여 인증 시스템의 무결성을 보장한다.

## Policy Type

`security-policy | operational-standard`

## Target Audience

- Security Administrators
- SRE / Platform Engineers
- Compliance Auditors

## Service SLOs

- **Availability**: 99.9% (LDAP/AD 연동 시 의존성 포함)
- **Token Validity**: Access Token(1H), Refresh Token(30D)
- **Audit Retention**: 90 Days (JSON Structured Logs)

## Operational Procedures

### 1. User & Group Management
- **Provisioning**: 정규 사용자 계정은 관리자에 의해 생성되어야 하며, `hy-home` 렐름의 표준 그룹 구조(`/admins`, `/operators`, `/users`)를 따라야 함.
- **Self-service**: 유저는 본인의 계정 정보만 수정 가능하며, 비밀번호 찾기(Forgot Password) 기능은 SMTP 서버 연동 후 활성화됨.

### 2. Realm & Client Controls
- **Change Management**: 렐름 설정 및 클라이언트 등록은 사전에 스테이징 환경에서 검증되어야 함.
- **Secret Management**: `confidential` 클라이언트의 Secret은 `/run/secrets` 경로에 안전하게 보관되며, 정기적으로 갱신되어야 함.

### 3. Identity Provider Trust
- **External IdP**: Google OAuth2 등 외부 IdP 연동 시 `first broker login` 플로우를 통해 플랫폼 계정과의 정합성을 유지함.
- **Security Check**: 외부 IdP의 클라이언트 ID/Secret은 유출 즉시 폐기하고 재발급 절차를 밟아야 함.

## Security Controls

- **Encryption**: 모든 토큰 서명(Signing)은 RS256 알고리즘을 사용하며, 키 회전(Key Rotation) 정책을 적용함.
- **Audit**: 모든 성공/실패 로그인 시도 및 설정 변경은 `/opt/keycloak/data/log` 또는 Graylog/Loki로 전송되어 상시 모니터링됨.

## Related Documents

- **Guide**: `[../../07.guides/02-auth/keycloak.md]`
- **Runbook**: `[../../09.runbooks/02-auth/keycloak.md]`
- **Spec**: `[../../04.specs/02-auth/keycloak.md]`
