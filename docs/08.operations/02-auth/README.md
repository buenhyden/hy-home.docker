# Auth Operations Policy (02-auth)

> Identity & Access Management Operations (02-auth)

## Overview

이 문서는 `hy-home.docker` 인증 시스템(02-auth)의 운영 정책과 보안 가이드라인을 정의한다. 사용자 계정 관리, 세션 정책, 시스템 안정성 유지를 위한 규칙을 포함한다.

## Policy Goals

- **Security**: 최소 권한 원칙(LoP)에 따른 접근 제어.
- **Availability**: SSO 서비스의 99.9% 가동률 유지.
- **Compliance**: 개인 정보 및 세션 데이터의 안전한 관리.

## Operational Standards

### 1. 계정 및 권한 관리 (IAM)

- **관리자 계정**: Keycloak `master` 렐름의 관리자 계정은 최소 인원에게만 부여하며, 강력한 비밀번호 정책을 적용한다.
- **서비스 렐름**: 실제 서비스는 전용 렐름(`hy-home.realm`)에서 운영하며, `master` 렐름과 분리한다.
- **클라이언트**: 새로운 서비스 연동 시 전용 Client ID를 발급하고, 필요 최소한의 Scope만 부여한다.

### 2. 세션 및 쿠키 정책 (SSO)

- **OAuth2 Proxy**:

  - `cookie_secure`는 항상 `true`여야 함 (HTTPS 필수).
  - 세션 만료 시간은 기본 12시간, 리프레시 주기는 1시간으로 설정한다.
- **Keycloak**:

  - SSO 및 세션 타임아웃 설정을 통해 유휴 세션을 자동 정리한다.
  - 보안을 위해 `Proxy Headers` 설정을 `xforwarded`로 유지한다.

### 3. 데이터 백업 및 보관

- **Keycloak DB**: PostgreSQL 컨테이너의 정기 백업을 수행하며, 렐름 설정값은 주기적으로 JSON으로 익스포트하여 보관한다.
- **로그**: 모든 로그인 시도 및 관리자 작업은 감사 로그(Audit Log)로 기록하며, 외부 로깅 시스템으로 전송한다.

## Monitoring & Auditing

- **Metrics**: Prometheus를 통해 Keycloak 및 OAuth2 Proxy의 가용성과 응답 시간을 모니터링한다.
- **Audit**: 주기적으로 미사용 계정 및 접근 권한을 검토하고 정리한다.

## Related Documents

- **Setup Guide**: `[../07.guides/02-auth/keycloak.md]`
- **Keycloak Policy**: `[./keycloak.md]`
- **Runbook**: `[../09.runbooks/02-auth/README.md]`
