<!-- Target: docs/03.adr/0011-laboratory-services.md -->

# ADR-0011: 11-laboratory 계층 주요 서비스 선정 및 구성

## Context

시스템 운영 효율성을 높이기 위해 컨테이너 관리, 데이터베이스 조회, 서비스 내비게이션 환경을 구축해야 한다. 이를 위해 가볍고 신뢰할 수 있으며, Traefik 및 Keycloak과 원활하게 통합되는 도구들을 선정해야 한다.

## Decision

다음과 같은 서비스 스택을 `11-laboratory`의 표준 도구로 선정한다.

1. **Dashboard**: **Homer**
    * 이유: 매우 가볍고 정적 설정 파일(`config.yml`)만으로 관리가 가능하며, 아이콘 및 그룹화 기능을 통해 직관적인 대시보드 구성을 지원한다.
2. **Container Management**: **Portainer (CE)**
    * 이유: Docker 환경에서 가장 널리 사용되는 관리 GUI이며, 스택 관리 및 로그 조회가 매우 용이하다.
3. **Database Inspection**: **RedisInsight**
    * 이유: Redis/Valkey의 데이터를 트리 구조로 시각화하고, 성능 분석 및 쿼리 작성을 지원하는 공식 도구이다.

## Rationale

* **중앙 집중식 접근**: 모든 도구는 Homer 대시보드를 통해 브라우저 한 곳에서 접근 가능하다.
* **보안 일관성**: 모든 서비스에 Traefik `sso-auth` 미들웨어를 적용하여 별도의 계정 관리 없이 Keycloak 통합 로그인을 보장한다.
* **리소스 최적화**: 운영 서버의 리소스를 최소한으로 사용하도록 최신 경량 이미지를 사용한다.

## Consequences

* **Positive**:
  * CLI에 익숙하지 않은 사용자도 인프라 상태를 쉽게 파악할 수 있다.
  * Redis 데이터 디버깅 및 컨테이너 로그 분석 로그 속도가 비약적으로 향상된다.
* **Negative**:
  * Docker Socket을 Portainer에 노출함에 따른 보안 리스크가 존재하므로, SSO 인증을 통해서만 접근을 허용해야 한다.

## Status: Accepted (2026-03-26)
