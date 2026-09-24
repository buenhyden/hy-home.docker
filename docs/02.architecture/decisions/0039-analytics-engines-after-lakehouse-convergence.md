---
title: "Analytics Engines after Lakehouse Convergence"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "@buenhyden"
updated: "2026-09-24"
layer: "architecture"
artifact_id: "ADR-0039"
parent_ids:
- "AD-0012"
created: "2026-09-24"
---

# ADR-0039: Analytics Engines after Lakehouse Convergence

## Context

ADR-0015는 `04-data/analytics`에서 InfluxDB(시계열), ksqlDB(스트림 처리),
OpenSearch(로그·검색), StarRocks(OLAP)를 각각 전용 엔진으로 채택했다.
SPEC-0180은 Iceberg table을 SeaweedFS에 두는 lakehouse를 도입했고, 그 엔진인
Flink와 Trino가 ksqlDB·StarRocks와 같은 역할을 맡는다. 같은 역할의 엔진을 둘씩
유지하면 이미지, 설정, 보안 검토, 운영 문서가 두 배가 되지만 얻는 기능은 없다.

S01 ruling은 Flink live acceptance 뒤에 ksqlDB를, Trino live acceptance 뒤에
StarRocks를 제거하기로 했다. 두 acceptance는 2026-09-24에 통과했다. Flink가 batch
INSERT와 checkpoint를 거치는 streaming INSERT로 table을 썼고, Trino가 같은 행을
읽었으며, Great Expectations suite가 Trino를 통해 통과했다. ksqlDB와 StarRocks는
배포된 적이 없고 host data나 volume도 없었다.

## Decision

수락되면 이 ADR은 ADR-0015를 supersede한다.

- **시계열**: InfluxDB 3 Core 단일 deployment를 유지한다(ADR-0015와 같다).
- **로그·검색**: OpenSearch 3.x를 유지한다(ADR-0015와 같다).
- **스트림 처리**: Flink가 Kafka topic과 Iceberg table 사이의 SQL 스트림 처리를
  맡는다. `lakehouse` profile의 JobManager와 TaskManager이며, checkpoint는 host
  directory에 둔다.
- **OLAP·SQL 조회**: Trino가 SeaweedFS의 Iceberg table에 대한 SQL 조회를 맡는다.
  별도 저장소를 가진 warehouse를 두지 않는다.
- ksqlDB와 StarRocks는 채택하지 않는다. 같은 역할의 엔진을 더하려면 이 ADR을
  대체하는 결정이 필요하다.

Runtime image tag는 tracked Compose 파일이 고정하고, 현재 image 목록은
`infra/tech-stack.versions.json`이 가진다.

## Consequences

- **Positive**:
  - 스트림 처리와 OLAP이 한 table format(Iceberg)과 한 object store를 공유하므로
    엔진 사이 복사나 동기화가 없다.
  - 엔진 수가 줄어 image, 보안 검토, 운영 문서가 줄어든다.
- **Trade-offs**:
  - Trino는 저장 계층이 없는 query engine이므로 성능은 Iceberg table 설계와
    SeaweedFS에 좌우된다.
  - Flink SQL은 ksqlDB의 pull query 같은 serving 기능이 없다. 필요하면 별도 결정이
    필요하다.
  - Flink와 Trino는 인증이 없는 API를 loopback host port로만 연다(POL-0094).

### Explicit Non-goals

- InfluxDB나 OpenSearch를 lakehouse로 옮기는 것.
- 핵심 트랜잭션 데이터를 분석 엔진에 직접 저장하는 것.

## Options Considered

### Alternative 01: ksqlDB와 StarRocks를 Flink·Trino와 함께 유지

- **Good**: 기존 결정을 바꾸지 않는다.
- **Bad**: 같은 역할의 엔진을 두 벌 운영하고, 배포된 적 없는 엔진의 문서와
  검증을 계속 유지해야 한다.

### Alternative 02: Spark만으로 스트림과 OLAP을 처리

- **Good**: 엔진이 하나로 준다.
- **Bad**: 대화형 SQL 조회에 Trino보다 무겁고, S12 Spark는 table 유지보수와 batch
  용도로 둔다.

## Traceability

근거는 SPEC-0180 Task 0008의 S01 ruling, S12–S15 source 단계, 2026-09-24 live
acceptance 기록과 현재 저장소 구성이다. 기록되지 않은 런타임 상태는 주장하지
않는다.

## Related Documents

- **Superseded on acceptance**: [ADR-0015](0015-analytics-engine-selection.md)
- **Architecture Description**: [0012-data-analytics-architecture.md](../descriptions/0012-data-analytics-architecture.md)
- **Requirements**: [0005-data-analytics.md](../../01.requirements/0005-data-analytics.md)
- **Lakehouse policy**: [POL-0094](../../05.operations/catalog/04-data/0094-lakehouse/policy.md)
