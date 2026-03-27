<!-- Target: docs/03.adr/0004-postgresql-ha-patroni.md -->

# ADR-0004: Choice of Spilo/Patroni for PostgreSQL HA

## Overview (KR)

이 문서는 `hy-home.docker`의 데이터 무결성과 가동률을 보장하기 위해, 단일 PostgreSQL 인스턴스 대신 Patroni 및 Etcd 기반의 고가용성(HA) 클러스터 솔루션을 채택하는 아키텍처 결정 기록이다.

## Context

- 데이터 티어의 싱글 포인트 장애(SPOF) 방지 필요.
- 자동 장애 조치(Failover) 및 복제 모니터링 자동화 요구.
- 컨테이너 환경에서의 유연한 클러스터 구성 및 운영 편의성.

## Decision

**Spilo (Zalando's PostgreSQL + Patroni)**를 핵심 데이터베이스 엔진으로 선정한다.

- **Patroni**: Etcd와 연동하여 안정적인 리더 선출 및 자동 장애 복구를 제공.
- **Spilo Image**: Zalando에서 유지보수하는 검증된 PostgreSQL HA 이미지 사용.
- **Etcd**: 강력한 일관성 저장소로서 클러스터 상태 관리.

## Explicit Non-goals

- 데이터베이스 샤딩 (본 ADR 범위 밖).
- 애플리케이션 레벨의 데이터 마이그레이션 전략.

## Consequences

- **Positive**: 장애 발생 시 데이터 손실 최소화 및 가동 시간 증대, 자동화된 장애 복구.
- **Trade-offs**: 3개의 노드 구성으로 인한 리소스 소모 증가, HAProxy(pg-router)를 통한 복잡한 라우팅 설정 필요.

## Alternatives

### Vanilla PostgreSQL with Replication

- Good: 구성이 단순하고 리소스 소모가 적음.
- Bad: 수동 Failover가 필요하며 복제 지연 모니터링이 어려움.

### Postgres Operator (K8s)

- Good: 쿠버네티스 환경에서 고도로 자동화됨.
- Bad: 현재 환경이 Docker Compose 기반이므로 도입 오버헤드가 큼.

## Related Documents

- **PRD**: `[../01.prd/2026-03-26-04-data.md]`
- **ARD**: `[../02.ard/0004-data-architecture.md]`
- **Spec**: `[../04.specs/04-data/spec.md]`
- **Plan**: `[../05.plans/2026-03-26-04-data-standardization.md]`
