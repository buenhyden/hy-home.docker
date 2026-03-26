# OAuth2 Proxy Operations

> Operational policies and security controls for the OAuth2 Proxy authentication layer.

---

## Overview (KR)

이 문서는 OAuth2 Proxy의 운영 정책과 보안 관리 지침을 제공한다. 세션 관리, 화이트리스트 정책, 그리고 업스트림 보안 설정을 포함한다.

## Policy Type

`security-policy | operational-standard`

## Target Audience

- Operator
- Security-auditor
- Agent-tuner

## Service SLOs

- **Availability**: 99.9% (ForwardAuth 경로의 가용성 보장)
- **Latency**: `< 50ms` (인증 체크 오버헤드 최소화)

## Operational Procedures

### 1. Session Management

- **Storage**: Sessions are stored in Valkey Cluster (`infra/04-data/valkey`).
- **Timeout**:
  - `cookie_expire`: 168h (7 days)
  - `cookie_refresh`: 1h
- **Security**: `cookie_httponly`, `cookie_secure` 옵션은 반드시 `true`로 설정되어야 함.

### 2. Whitelist & Access Control

- **Allowed Domains**: 프로젝트의 메인 도메인 및 하위 도메인으로 제한.
- **Authenticated Emails**: 특정 도메인(예: `hy-home.com`) 이외의 이메일은 기본적으로 거부함 (`--email-domain` 설정).

### 3. Upstream Security

- **Trust**: 백엔드 서비스로 전달되는 `X-Auth-Request-User`, `X-Auth-Request-Email` 헤더의 신뢰성을 보장하기 위해 Traefik 미들웨어에서 헤더 주입을 엄격히 통제함.

## Security Controls

- **Secret Rotation**: `cookie_secret` 및 `client_secret`은 주기적으로 교체되어야 하며, Docker Secrets를 통해 관리됨.
- **Audit Logging**: 모든 인증 요청 및 콜백 로그는 표준 출력으로 기록되어 fluent-bit을 통해 수집됨.

## Related Documents

- **Guide**: `[../../07.guides/02-auth/oauth2-proxy.md]`
- **Runbook**: `[../../09.runbooks/02-auth/oauth2-proxy.md]`
- **Spec**: `[../../04.specs/02-auth/oauth2-proxy.md]`
