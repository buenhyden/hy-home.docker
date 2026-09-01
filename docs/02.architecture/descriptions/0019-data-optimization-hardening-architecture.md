---
profile_id: architecture-description
status: active
artifact_id: AD-0019
artifact_type: architecture-description
parent_ids:
  - REQ-0016
created: 2026-03-28
updated: 2026-09-01
---
# Data Optimization and Hardening Architecture

## Context and Stakeholders

이 문서는 `infra/04-data/`의 관계형, NoSQL, cache, object storage, analytics,
graph/vector 서비스 구조를 설명한다. Maintainer와 operator는 공통 Compose
계약과 engine별 lifecycle·recovery 절차를 분리해 관리한다.

## System Boundaries

- `infra/04-data/**`는 data service Compose topology와 engine별 configuration을
  소유한다.
- Stage 03 capability Spec은 구현 경계를, Stage 05 subject는 운영 절차를
  소유한다.
- Gateway routing, Stage 03 security secret 공급, Stage 06 telemetry 수집은
  각각의 계층에서 제공된다.
- 제품 business schema·query와 cloud migration은 이 아키텍처 밖이다.

## Components

- Analytics: InfluxDB, ksqlDB, OpenSearch, warehouse services
- Cache and KV: Valkey cluster
- Object storage: MinIO, SeaweedFS
- NoSQL: Cassandra, CouchDB, MongoDB
- Operational platforms: management database, Supabase
- Relational: PostgreSQL cluster
- Specialized: Neo4j, Qdrant

각 component는 독립 configuration과 volume을 유지하며 common optimization,
secret, healthcheck, network contract를 Compose에서 조합한다.

## Data Flow

서비스는 SQL, Redis/Valkey, S3-compatible, search, vector, graph protocol을
통해 명시적으로 연결된다. Persistent state는 `${DEFAULT_DATA_DIR}` 아래의
서비스별 volume 경계를 유지하고 credential은 Compose secret 계약으로
주입된다.

## Deployment View

현재 구현은 `infra/common-optimizations.yml`과 각 engine Compose 파일을
조합한다. Hardening 및 Compose validators가 secret, label, expose,
healthcheck 정합성을 검사한다. 추가 HA, lifecycle automation, failover drill은
현재 모든 engine에 구현된 것으로 간주하지 않으며 별도 승인된 current
Requirement와 ADR을 통해 도입한다.

## Quality Attributes

- **Security**: credential 주입을 일관되게 유지하고 불필요한 노출을 줄인다.
- **Reliability**: healthcheck와 engine별 recovery procedure를 사용한다.
- **Scalability**: 승인된 engine별 확장을 공통 Compose 경계를 깨지 않고
  도입할 수 있어야 한다.
- **Operability**: static Gate, capability Spec, Operations subject가 같은
  topology와 failure boundary를 설명해야 한다.

## Traceability

- [REQ-0016](../../01.requirements/0016-data-optimization-hardening.md)
- [ADR-0019](../decisions/0019-data-hardening-and-ha-expansion-strategy.md)
- [SPEC-0004](../../03.specs/0004-data/spec.md)
- [Data hardening guide](../../05.operations/catalog/04-data/0030-optimization-hardening/guide.md)
- [Data hardening policy](../../05.operations/catalog/04-data/0030-optimization-hardening/policy.md)
- [Data hardening runbook](../../05.operations/catalog/04-data/0030-optimization-hardening/runbook.md)
