<!-- Target: docs/09.runbooks/04-data/nosql/cassandra.md -->

# Cassandra Recovery Runbook

> Emergency recovery procedures for Apache Cassandra single-node instance.

---

## Overview (KR)

이 문서는 Cassandra 서비스 중단, 데이터 오염 또는 노드 장애 시 신속하게 서비스를 정상화하기 위한 긴급 대응 절차를 설명한다.

## Runbook Type

`disaster-recovery`

## Target Audience

- On-call Engineer
- SRE
- AI-Operator

## Purpose

Cassandra 서비스 장애 발생 시 다운타임을 최소화하고, 데이터 손실 없이 최단 시간 내에 서비스를 복구하는 것을 목표로 한다.

## Pre-remediation Checklist

- [ ] `docker ps`를 통해 컨테이너 상태 확인
- [ ] `docker logs cassandra-node1`에서 "Error" 키워드 검색
- [ ] `${DEFAULT_DATA_DIR}/cassandra` 볼륨 접근 가능 여부 확인
- [ ] 사용 가능한 최근 백업본(Snapshot) 존재 여부 확인

## Remediation Steps

### Scenario 1: Service Down (Container Crash)

컨테이너가 비정상 종료된 경우 재시작을 시도한다.

1. 컨테이너 재시작:
   ```bash
   cd infra/04-data/nosql/cassandra
   docker-compose up -d
   ```
2. 시작 로그 확인 (Status 'Ready' 확인):
   ```bash
   docker logs -f cassandra-node1
   ```

### Scenario 2: Data Corruption (Restore from Snapshot)

데이터 오염 시 스냅샷을 기반으로 복원한다.

1. 서비스 중지:
   ```bash
   docker-compose stop cassandra-node1
   ```
2. 기존 데이터 백업 (안전을 위해):
   ```bash
   mv ${DEFAULT_DATA_DIR}/cassandra/data ${DEFAULT_DATA_DIR}/cassandra/data_broken
   ```
3. 스냅샷 복사:
   (백업 스토리지에서 최근 스냅샷을 `${DEFAULT_DATA_DIR}/cassandra/data` 위치로 복구)
4. 권한 확인 및 시작:
   ```bash
   chown -R 999:999 ${DEFAULT_DATA_DIR}/cassandra/data
   docker-compose start cassandra-node1
   ```

## Verification Steps

1. 노드 상태 확인:
   ```bash
   docker exec -it cassandra-node1 nodetool status
   ```
   (상태가 `UN`이어야 함)
2. 데이터 샘플 쿼리:
   ```bash
   docker exec -it cassandra-node1 cqlsh -u ${CASSANDRA_USER} -p ${CASSANDRA_PASSWORD} -e "SELECT * FROM system.local;"
   ```

## Post-remediation Tasks

- 장애 원인 분석 (Post-mortem) 작성 및 공유
- 모니터링 임계값 조정 필요성 검토
- 백업 무결성 추가 점검

## Related Documents

- **Guide**: [Cassandra System Guide](../../../docs/07.guides/04-data/nosql/cassandra.md)
- **Operation**: [Cassandra Operation Policy](../../../docs/08.operations/04-data/nosql/cassandra.md)
