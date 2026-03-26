# ADR: Choice of Spilo/Patroni for PostgreSQL HA (0004-data)

## Status

- **Proposed**: 2026-03-26
- **Status**: Decided

## Overview (KR)

`hy-home.docker`의 데이터 무결성과 가동률을 보장하기 위해, 단일 PostgreSQL 인스턴스 대신 Patroni 및 Etcd 기반의 고가용성(HA) 클러스터 솔루션을 채택한다.

## Context

- 데이터 티어의 싱글 포인트 장애(SPOF) 방지 필요.
- 자동 장애 조치(Failover) 및 복제 모니터링 자동화.
- 컨테이너 환경에서의 유연한 클러스터 구성.

## Decision

**Spilo (Zalando's PostgreSQL + Patroni)**를 핵심 데이터베이스 엔진으로 선정한다.

### Rationale

- **Patroni**: Etcd와 연동하여 안정적인 리더 선출 및 자동 장애 복구를 제공.
- **Spilo Image**: Zalando에서 유지보수하는 검증된 PostgreSQL HA 이미지로, Patroni가 사전 탑재되어 설정이 간편함.
- **Etcd**: 이미 플랫폼 내 다른 서비스(Gateway 등)에서 서비스 디스커버리에 사용될 수 있는 강력한 일관성 저장소.

## Alternatives Considered

1. **Vanilla PostgreSQL with Replication**: 수동 Failover가 필요하며 복제 지연 모니터링이 어려움.
2. **Postgres Operator (K8s)**: 현재 환경이 Docker Compose 기반이므로 오버헤드가 큼.

## Consequences

- 3개의 PostgreSQL 노드와 3개의 Etcd 노드가 필요하여 리소스 사용량이 증가.
- HAProxy(pg-router)를 통한 라우팅 설정이 복잡해짐.
- 장애 복구 시 데이터 일관성 보장이 강화됨.

## Related Documents

- **PRD**: [2026-03-26-04-data.md](../01.prd/2026-03-26-04-data.md)
- **ARD**: [0004-data-architecture.md](../02.ard/0004-data-architecture.md)
- **Spec**: [04-data/spec.md](../04.specs/04-data/spec.md)
- **Plan**: [2026-03-26-04-data-standardization.md](../05.plans/2026-03-26-04-data-standardization.md)
