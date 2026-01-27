# 📐 Architecture Patterns

이 문서는 프로젝트 전반에 적용된 핵심 아키텍처 패턴과 설계 철학을 설명합니다.

## 1. Directional Dependency (단방향 의존성)

시스템은 명확한 계층 구조를 가지며, 의존성은 항상 상위에서 하위로만 흐릅니다.

- **Presentation (Ingress/UI)** -> **Domain (App Logic)** -> **Data (DB/Cache)** -> **Infrastructure (Network/OS)**
- 상위 레이어는 하위 레이어를 알 수 있지만, 하위 레이어는 상위 레이어에 의존해서는 안 됩니다.

## 2. Modular Micro-Services

모든 서비스는 독립적으로 배포 및 확장 가능해야 합니다.

- **Independent Config**: 각 서비스는 자체 `docker-compose.yml`과 설정 파일을 가집니다.
- **Service Isolation**: 한 서비스의 장애가 전체 시스템으로 전파되지 않도록 설계합니다 (Retry, Timeout 설정).
- **Include-based Orchestration**: 메인 오케스트레이터가 필요한 서비스만 발췌하여 구성하는 유연성을 제공합니다.

## 3. Network Topology & Isolation

보안과 성능을 위해 네트워크 계층을 분리합니다.

- **`infra_net`**: 핵심 인프라 서비스(Gateway, DB, Monitoring) 간의 전용 통신망.
- **`project_net`**: 실제 비즈니스 애플리케이션과 인프라 서비스를 연결하는 가교 네트워크.
- **Static IP Strategy**: 핵심 인프라 서비스에는 고정 IP를 부여하여 DNS 장애 시에도 안정적인 내부 통신을 보장합니다.

## 4. Sidecar Pattern

핵심 비즈니스 로직 외의 부가 기능(로그 수집, 지표 전송, 환경 변수 주입)은 사이드카 컨테이너를 통해 처리합니다.

- 예: PostgreSQL 컨테이너 옆에 붙는 `postgres-exporter`.
- 예: 각 서비스 로그를 수집하는 `Alloy` 에이전트.

## 5. Security-by-Design

- **Internal-only**: DB, 내부 API 등은 직접 외부에 노출하지 않고 `Traefik`을 경유하도록 합니다.
- **SSO First**: 모든 관리 도구(Grafana, n8n 등)는 `Keycloak` 중앙 인증을 거치도록 강제합니다.
- **Least Privilege**: 컨테이너는 필요한 최소한의 볼륨 권한(`ro` vs `rw`)과 리소스를 할당받습니다.
