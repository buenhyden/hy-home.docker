# Traefik Operations Policy

> Governance and control rules for the Traefik Edge Router.

---

### Policy Enforcement

- HTTPS is enforced globally; HTTP is redirected to HTTPS at the Traefik entrypoint level.
- Basic Authentication is required for accessing the Traefik Dashboard.
- All internal services must be protected by SSO (`sso-auth@file`) unless explicitly excluded in the service labels.

## Overview (KR)

이 문서는 Traefik 운영 정책을 정의한다. 클러스터 진입점의 보안 통제, TLS 인증서 관리 표준, 그리고 동적 라우팅 구성 변경에 대한 승인 절차를 규정한다.

## Policy Scope

이 정책은 모든 트라이픽(Traefik) 구성 파일(`traefik.yml`, `middleware.yml`, `tls.yaml`)과 Docker 라벨을 통한 라우팅 정의를 통제한다.

## Applies To

- **Systems**: Traefik, Docker Engine, Cert-Manager (if applicable).
- **Agents**: Gateway Maintenance Agents.
- **Environments**: All environments (Production, Staging, Dev).

## Controls

### 1. Security & Compliance
- **Required**: 모든 공개 경로는 HTTPS(TLS)를 필수로 사용해야 하며, 포트 80은 HTTPS로의 리다이렉션만 허용한다.
- **Required**: Traefik 대시보드는 반드시 `dashboard-auth` (Basic Auth) 미들웨어로 보호되어야 한다.
- **Disallowed**: 비밀번호나 민감한 정보는 `middleware.yml`에 평문으로 작성할 수 없으며, 반드시 Docker Secrets를 사용해야 한다.

### 2. Configuration Management
- **Required**: 정적 설정(`traefik.yml`)의 변경은 인프라 배포 마일스톤(Plan)을 통해 검토되어야 한다.
- **Allowed**: 새로운 서비스 추가 시의 라벨 추가는 각 프로젝트의 태스크(Task) 단위로 자유롭게 수행 가능하다.

### AI Agent Operation Policy

- **Standard Operating Procedure**: AI agents are permitted to update dynamic configurations (`dynamic/*.yml`) to add or refine middlewares.
- **Constraints**: Changes to the static configuration (`traefik.yml`) or global entrypoints require formal architectural review (ARD update).

## Exceptions
- 로컬 개발 환경(`dev` 프로필)에서는 TLS 없이 HTTP만 사용하는 것을 허용한다.
- 비상 장애 복구 상황에서는 사후 보고를 전제로 수동으로 구성을 변경할 수 있다.

## Verification
- **Automated**: `traefik healthcheck` 명령을 통한 주기적 상태 모니터링.
- **Manual**: 매월 1회 SSL 인증서 만료일 및 TLS 버전 준수 현황 점검.

## Review Cadence

- Quarterly (분기별 1회 점검 및 업데이트)

## Related Documents

- **ARD**: `[../../02.ard/README.md]`
- **Runbook**: `[../../09.runbooks/01-gateway/traefik.md]`
- **Postmortem**: `[../../11.postmortems/README.md]`
