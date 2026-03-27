<!-- Target: docs/08.operations/04-data/nosql/cassandra.md -->

# Apache Cassandra Operations Policy

> NoSQL 데이터 인프라(Cassandra) 운영 정책 및 통제 기준.

---

## Overview (KR)

이 문서는 Apache Cassandra 서비스의 영속성 관리, 보안 통제 및 성능 기준을 정의한다. 단일 노드 운영 환경에서 데이터의 안정성과 가용성을 유지하기 위한 관리 지침을 포함한다.

## Policy Scope

Cassandra 5.0 서비스의 데이터 백업, 리소스 할당, 보안 인증 및 모니터링 주기를 규정한다.

## Applies To

- **Systems**: `cassandra-node1`, `cassandra-exporter`
- **Agents**: Data SRE Agents, Backend Agents
- **Environments**: Production, Staging

## Controls

- **Required**:
  - `cassandra_password` Docker Secret을 통한 인증 필수.
  - `${DEFAULT_DATA_DIR}/cassandra` 호스트 볼륨 백업 필수.
  - 힙 상태 모니터링 및 80% 임계치 알림 설정 필수.
- **Allowed**:
  - 특정 워크로드(AI/ML)를 위한 SAI 및 Vector Search 기능 활성화.
  - 성능 분석을 위한 임시 JMX 덤프 수집.
- **Disallowed**:
  - 루트 계정 없이 `cqlsh` 직접 접속 차단.
  - 승인되지 않은 외부 네트워크 포트(9042, 7000) 노출 금지.

## Exceptions

- 데이터 대량 적재(Batch Load) 또는 마이그레이션 시, 성능 최적화를 위해 일시적으로 `CommitLog` 동기화 방식을 변경할 수 있으나, 작업 완료 후 표준 정책으로 복귀해야 한다 (Data Lead 승인 필요).

## Verification

- **Compliance**: 매일 정기 백업 스냅샷 생성 여부를 크론 로그를 통해 확인한다.
- **Health**: `nodetool status` 및 Prometheus 메트릭을 통해 가동 시간을 체크한다.

## Review Cadence

- Quarterly (분기별 데이터 증가율 및 성능 튜닝 내역 검토)

## AI Agent Policy Section (If Applicable)

- **Model Change Process**: 데이터 스키마 또는 컴팩션 전략 변경 시에는 `docs/04.specs`의 스펙 문서를 먼저 갱신하고 검증해야 한다.
- **Log Retention**: Cassandra System Logs 및 Audit Logs는 최소 30일간 보관한다.

## Related Documents

- **ARD**: [04-data Architecture](../../../docs/02.ard/0004-data-architecture.md)
- **Runbook**: [Cassandra Recovery Runbook](../../../docs/09.runbooks/04-data/nosql/cassandra.md)
- **Guide**: [Cassandra System Guide](../../../docs/07.guides/04-data/nosql/cassandra.md)
