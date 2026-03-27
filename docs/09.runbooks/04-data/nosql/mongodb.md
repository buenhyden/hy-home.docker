<!-- Target: docs/09.runbooks/04-data/nosql/mongodb.md -->

# MongoDB Recovery Runbook

> Emergency recovery procedures for MongoDB Replica Set and failover incidents.

---

## Overview (KR)

이 문서는 MongoDB 레플리카 셋의 Primary 부재, 과도한 데이터 지연(Lag), 또는 Arbiter 장애 발생 시의 신속한 복구 절차를 설명한다.

## Runbook Type

`disaster-recovery`

## Target Audience

- On-call Engineer
- SRE
- DBA

## Purpose

레플리카 셋의 Primary를 재선출하고, Secondary 노드를 최신 상태로 재동기화하며, 클러스터의 정족수를 보호하여 쓰기 가용성을 확보한다.

## Pre-remediation Checklist

- [ ] `rs.status()` 명령으로 멤버 상태 확인 (`PRIMARY` 유무 확인)
- [ ] `docker logs`를 통해 Election 로그 분석
- [ ] 네트워크 분리(Split-brain) 가능성 검토
- [ ] Oplog window 내 최신 데이터 존재 여부 확인

## Remediation Steps

### Scenario 1: No Primary Elected

정족수 부족으로 Primary가 선출되지 않는 경우.

1. 죽은 노드(Secondary 또는 Arbiter) 우선 복구:
   ```bash
   docker-compose restart mongodb-rep2
   ```
2. 최소 2개 노드가 살아나면 자동으로 Election이 시작됨.
3. 강제 선출 (긴급 상황):
   Primary로 만들고자 하는 노드에서 `rs.stepDown()` 또는 Priority 조정을 통해 선출 유도.

### Scenario 2: Stale Secondary (Re-sync required)

Secondary 노드 데이터가 너무 오래되어 Oplog로 추적이 불가능한 경우.

1. Secondary 노드 중지 및 데이터 초기화:
   ```bash
   docker-compose stop mongodb-rep2
   rm -rf ${DEFAULT_DATA_DIR}/mongodb/data2/*
   ```
2. 컨테이너 시작:
   ```bash
   docker-compose start mongodb-rep2
   ```
3. Initial Sync 시작 확인:
   ```bash
   rs.status() # stateStr: 'STARTUP2' 확인
   ```

## Verification Steps

1. 클러스터 멤버십 확인:
   ```bash
   rs.conf()
   ```
2. 쓰기 테스트:
   ```bash
   db.test.insertOne({status: "recovered", date: new Date()})
   ```

## Post-remediation Tasks

- Oplog 사이즈 증설 필요성 검토
- Arbiter 배치 위치 물리적 격리 확인
- 펜싱(Fencing) 로직 및 타이머 값(ElectionTimeout) 조정 검토

## Related Documents

- **Guide**: [MongoDB Replica Set Guide](../../../07.guides/04-data/nosql/mongodb.md)
- **Operation**: [MongoDB Operation Policy](../../../08.operations/04-data/nosql/mongodb.md)
