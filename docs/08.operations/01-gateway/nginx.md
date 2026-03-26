# Nginx Operations Policy

> Governance and control rules for the Nginx Proxy.

---

## Overview (KR)

이 문서는 Nginx 프록시 운영 정책을 정의한다. 경로 기반 라우팅 규칙의 중앙 집중 관리, SSO 인증 연동 표준, 그리고 대용량 트래픽 처리를 위한 프록시 최적화 기준을 규정한다.

## Policy Scope

이 정책은 Nginx의 주 설정 파일(`nginx.conf`)과 이를 통한 업스트림(Upstream) 서비스 물리 보안 및 라우팅 제어를 대상으로 한다.

## Applies To

- **Systems**: Nginx, OAuth2 Proxy, Backend Services (MinIO, Keycloak 등).
- **Agents**: Gateway Maintenance Agents.
- **Environments**: All environments.

## Controls

### 1. Routing & Security
- **Required**: 모든 `/app/` 하위 경로는 반드시 SSO(`auth_request`)를 통한 인증을 거쳐야 한다.
- **Required**: 서비스 노출 시 불필요한 헤더 노출을 방지하기 위해 `server_tokens off;` 설정을 유지한다.
- **Allowed**: 정적인 자산(Static Assets) 서빙 시 Nginx 캐싱 설정을 적용하여 백엔드 부하를 줄이는 것을 권장한다.

### 2. Configuration Standards
- **Required**: 새로운 업스트림 추가 시 명확한 서비스 이름 정의와 `keepalive` 설정을 포함해야 한다.
- **Required**: 업로드 기능이 있는 서비스(예: MinIO)의 경우 `client_max_body_size`를 명시적으로 제어해야 한다.

## Exceptions

- `ping` 엔드포인트와 같이 상태 확인을 위한 경로는 인증 예외를 적용한다.
- 외부망과 단절된 내부 전용 관리 서비스는 조직 내 합의에 따라 SSO를 생략할 수 있다.

## Verification

- **Compliance Check**: `nginx -t` 명령을 통한 구문 무결성 검사.
- **Audit**: 분기별로 사용되지 않는 업스트림 및 유효하지 않은 경로 규칙 제거.

## Review Cadence

- Quarterly (분기별 1회 점검)

## Related Documents

- **ARD**: `[../../02.ard/README.md]`
- **Runbook**: `[../../09.runbooks/01-gateway/nginx.md]`
- **Postmortem**: `[../../11.postmortems/README.md]`
