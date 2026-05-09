<!-- Target: docs/08.operations/04-data/nosql/cassandra.md -->

# Cassandra Operation Policy

> Operational standards for maintaining a high-throughput Apache Cassandra single-node instance.

---

## Overview (KR)

이 문서는 `hy-home.docker` 환경에서 Apache Cassandra의 안정적인 운영을 위한 백업, 성능 모니터링, 리소스 관리 정책을 정의한다.

## Policy Type

`operational-standard`

## Target Audience

- Operator
- SRE
- AI-Operator

## Purpose

운영자가 Cassandra의 데이터 정합성을 유지하고, 성능 병목 현상을 사전에 방지하며, 효과적인 백업 및 복구 체계를 구축할 수 있도록 한다.

## Service Level Objectives (SLO)

- **Availability**: 99.9% (Single node limitation acknowledged)
- **Read Latency**: 95th percentile < 100ms
- **Write Latency**: 95th percentile < 50ms

## Operational Procedures

### 1. Monitoring & Alerting

- **Key Metrics**:
  - `ReadLatency`, `WriteLatency`: 요청 처리 속도 감시
  - `PendingTasks`: 시스템 부하 및 스케줄링 지연 확인
  - `DiskUsage`: `/var/lib/cassandra` 볼륨 잔여 용량 체크
- **Thresholds**: Disk 사용량 80% 초과 시 경고 발생.

### 2. Backup Strategy

- **Manual Snapshots**: 주요 업그레이드 또는 데이터 이관 전 `nodetool snapshot`을 수행한다.
- **Automated Backup**: `${DEFAULT_DATA_DIR}/cassandra` 볼륨의 일일 증분 백업을 수행한다. (External Storage 연동)
- **Recovery**: [Cassandra Recovery Runbook](../../../09.runbooks/04-data/nosql/cassandra.md)을 참조하여 복권 수행.

### 3. Resource Management

- **JVM Heap**: 컨테이너 메모리의 50%(최대 8GB)를 힙 메모리로 할당한다.
- **Compaction**: 가급적 부하가 적은 시간에 `SizeTieredCompactionStrategy`를 통해 수행되도록 설정한다.

## Common Pitfalls

- **Disk Space during Compaction**: 컴팩션 작업 중에는 일시적으로 데이터 파일 크기가 2배까지 늘어날 수 있으므로 충분한 여유 공간(최소 50%)이 필요하다.
- **Garbage Collection**: JVM GC 포즈로 인한 응답 지연 발생 시 GC 로그를 분석하여 힙 크기를 재조정한다.

## Related Documents

- **Infrastructure**: [Cassandra Infrastructure](../../../../infra/04-data/nosql/cassandra/README.md)
- **Guide**: [Cassandra System Guide](../../../07.guides/04-data/nosql/cassandra.md)
- **Runbook**: [Cassandra Recovery Runbook](../../../09.runbooks/04-data/nosql/cassandra.md)

---

## Policy Scope

이 정책은 관련 서비스의 운영 기준, 변경 통제, 검증 방법을 다룬다.

## Applies To

- **Systems**: 관련 Docker Compose 서비스와 문서화된 운영 자산
- **Agents**: repo-local governance를 따르는 AI agents
- **Environments**: local, development, homelab operations

## Controls

- **Required**: 변경 전 관련 README, guide, runbook 확인
- **Allowed**: 문서와 검증 절차의 in-place 보강
- **Disallowed**: secret 값 노출, 승인 없는 runtime 변경, 정책과 절차의 중복 SSoT 생성

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## Verification

- 관련 repository validation script와 문서 heading audit로 준수 여부를 확인한다.

## Review Cadence

- 서비스 구성 변경 시 검토
- 문서 템플릿 변경 시 검토
- 주요 운영 정책 변경 시 검토

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.
