<!-- Target: docs/05.operations/04-data/nosql/mongodb.md -->

# MongoDB Operation Policy

> Operational standards for MongoDB Replica Set (3.2 GA) high availability and security.

---

## Overview (KR)

이 문서는 MongoDB 레플리카 셋의 안정적인 복제 상태 유지, 백업 절차, 보안 패치 및 모니터링 운영 정책을 정의한다.

## Policy Type

`operational-standard`

## Target Audience

- Operator
- SRE
- DBA

## Purpose

레플리카 셋의 정족수(Quorum)를 안정적으로 유지하고, 장애 발생 시 자동 페일오버 프로세스를 보장하며, 데이터 유출 방지를 위한 보안 준수 사항을 관리한다.

## Service Level Objectives (SLO)

- **Availability**: 99.95% (Replica Set failover capability)
- **Replication Lag**: Primary/Secondary 간 지연 < 10 seconds
- **Data Durability**: W:MAJORITY 설정 준수 시 손실 방지

## Operational Procedures

### 1. Monitoring & Alerting

- **Replication Health**: `rs.status()`의 `optimeDate` 차이를 주기적으로 감시하여 지연(Lag)을 추적한다.
- **Disk Pressure**: 데이터 볼륨(`mongodb_data1`, `data2`) 사용량이 85%를 초과할 경우 디스크 확장을 계획한다.

### 2. Backup & Restoration

- **Oplog Tail**: `mongodb-exporter`를 통해 Oplog 사이즈와 가용 시간을 모니터링하여 갑작스러운 데이터 증가에 대비한다.
- **Consistent Backups**: `mongodump` 수행 시 `--oplog` 옵션을 사용하여 백업 시점의 일치성을 보장한다.

### 3. Security Maintenance

- **Auth Audit**: 모든 접속은 RBAC(Role-Based Access Control)를 거쳐야 하며, 주기적으로 미사용 계정을 정리한다.
- **Key Rotation**: 클러스터 내부 인증용 `mongo-keyfile`을 정기적으로 교체할 수 있는 프로세스를 수립한다.

## Common Pitfalls

- **Arbiter Risk**: Arbiter 노드가 다운되면 3노드 클러스터에서 2노드만 남게 되어 데이터 노드 하나만 더 장애가 나도 Primary 선출이 불가능해진다. Arbiter 가용성 역시 중요하다.
- **Oplog Window**: Oplog가 너무 작으면 보관 주기가 짧아져 Secondary 노드 재동기화(Initial Sync)가 불가능해질 수 있다.

## Related Documents

- **Infrastructure**: [MongoDB Infrastructure](../../../../../infra/04-data/nosql/mongodb/README.md)
- **Usage**: [MongoDB Replica Set Usage](./mongodb.md)
- **Procedure**: [MongoDB Recovery Procedure](./mongodb.md)

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

## Usage

> Migrated from `docs/05.operations/04-data/nosql/mongodb.md` during the 2026-05-10 operations taxonomy consolidation.

### MongoDB Replica Set Usage

> Document-oriented NoSQL database with flexible schemas and high availability via Replica Sets.

---

#### Overview (KR)

이 문서는 MongoDB 8.2 Replica Set의 아키텍처, 데이터 모델링 원칙 및 `hy-home.docker` 환경에서의 연결 및 운영 가이드를 제공한다.

#### Usage Type

`system-guide`

#### Target Audience

- Developer
- Operator
- Agent-tuner

#### Purpose

개발자가 MongoDB의 문서 기반 데이터 모델을 효율적으로 설계하고, 운영자가 레플리카 셋의 고가용성 메커니즘을 이해하여 안정적인 데이터 서비스를 제공할 수 있도록 돕는다.

#### Prerequisites

- `infra/04-data/nosql/mongodb` 레플리카 셋 배포 환경
- MongoDB 셸 (`mongosh`) 또는 GUI 클라이언트 (Compass) 사용법
- JSON/BSON 데이터 구조에 대한 기초 지식

#### Step-by-step Instructions

##### 1. 레플리카 셋 상태 진단

클러스터의 멤버십과 상태를 확인한다.

```bash
docker exec -it mongodb-rep1 mongosh -u ${MONGODB_ROOT_USERNAME} --eval "rs.status()"
```

- **PRIMARY**: 모든 읽기/쓰기 작업이 수행되는 메인 노드.
- **SECONDARY**: Primary로부터 데이터를 복제하며 장애 시 새로운 Primary로 승격 가능.
- **ARBITER**: 데이터를 저장하지 않으며 투표에만 참여하여 정족수를 유지.

##### 2. 애플리케이션 연결

고가용성을 위해 모든 노드를 포함한 연결 문자열을 사용한다.

```text
mongodb://${USER}:${PASS}@mongodb-rep1:27017,mongodb-rep2:27017/?replicaSet=MyReplicaSet&authSource=admin
```

##### 3. 관리 UI 접근

**Mongo Express**를 통해 웹 기반으로 데이터를 관리할 수 있다.

- **URL**: `https://mongo-express.${DEFAULT_URL}`
- **Auth**: 배포 시 설정된 Basic Auth 정보를 확인한다.

##### 4. 인덱스 최적화 및 쿼리 프로파일링

- `db.collection.explain()` 명령을 통해 쿼리 실행 계획을 수집한다.
- 쿼리 패턴에 맞는 적절한 인덱스(Compound, TTL, Text 등)를 생성하여 성능을 최적화한다.

#### Common Pitfalls

- **Election Delay**: 노드 장애 시 새로운 Primary가 선정되는 동안(보통 수 초 내외) 일시적인 쓰기 거부가 발생할 수 있다. 애플리케이션 레벨의 재시도 로직이 필요하다.
- **Read Preference**: 기본값은 `primary`이나, 읽기 부하 분산을 위해 `secondaryPreferred` 설정을 고려할 수 있다. 단, 최신 데이터 정합성 이슈에 유의해야 한다.
- **WiredTiger Cache**: MongoDB는 시스템 메모리의 상당 부분을 캐시로 사용하므로 Docker 리소스 제한 시 `cacheSizeGB` 설정을 신중히 확인해야 한다.

#### Related Documents

- **Infrastructure**: [MongoDB Infrastructure](../../../../../infra/04-data/nosql/mongodb/README.md)
- **Operation**: [MongoDB Operations Policy](./mongodb.md)
- **Procedure**: [MongoDB Recovery Procedure](./mongodb.md)

## Procedure

> Migrated from `docs/05.operations/04-data/nosql/mongodb.md` during the 2026-05-10 operations taxonomy consolidation.

### MongoDB Recovery Procedure

> Emergency recovery procedures for MongoDB Replica Set and failover incidents.

---

#### Overview (KR)

이 문서는 MongoDB 레플리카 셋의 Primary 부재, 과도한 데이터 지연(Lag), 또는 Arbiter 장애 발생 시의 신속한 복구 절차를 설명한다.

#### Procedure Type

`disaster-recovery`

#### Target Audience

- On-call Engineer
- SRE
- DBA

#### Purpose

레플리카 셋의 Primary를 재선출하고, Secondary 노드를 최신 상태로 재동기화하며, 클러스터의 정족수를 보호하여 쓰기 가용성을 확보한다.

#### Pre-remediation Checklist

- [ ] `rs.status()` 명령으로 멤버 상태 확인 (`PRIMARY` 유무 확인)
- [ ] `docker logs`를 통해 Election 로그 분석
- [ ] 네트워크 분리(Split-brain) 가능성 검토
- [ ] Oplog window 내 최신 데이터 존재 여부 확인

#### Remediation Steps

##### Scenario 1: No Primary Elected

정족수 부족으로 Primary가 선출되지 않는 경우.

1. 죽은 노드(Secondary 또는 Arbiter) 우선 복구:

   ```bash
   docker-compose restart mongodb-rep2
   ```

2. 최소 2개 노드가 살아나면 자동으로 Election이 시작됨.
3. 강제 선출 (긴급 상황):
   Primary로 만들고자 하는 노드에서 `rs.stepDown()` 또는 Priority 조정을 통해 선출 유도.

##### Scenario 2: Stale Secondary (Re-sync required)

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

#### Verification Steps

1. 클러스터 멤버십 확인:

   ```bash
   rs.conf()
   ```

2. 쓰기 테스트:

   ```bash
   db.test.insertOne({status: "recovered", date: new Date()})
   ```

#### Post-remediation Tasks

- Oplog 사이즈 증설 필요성 검토
- Arbiter 배치 위치 물리적 격리 확인
- 펜싱(Fencing) 로직 및 타이머 값(ElectionTimeout) 조정 검토

#### Related Documents

- **Usage**: [MongoDB Replica Set Usage](./mongodb.md)
- **Operation**: [MongoDB Operation Policy](./mongodb.md)

---

#### Canonical References

- [../README.md](../README.md)
- [../../05.operations/README.md](../../../README.md)
- [../../05.operations/README.md](../../../README.md)

#### When to Use

- 관련 서비스 점검, 재시작, 검증, 문서 보강이 필요할 때
- 운영 절차와 evidence capture가 필요한 변경을 수행할 때

#### Procedure or Checklist

##### Checklist

- [ ] 관련 operation policy를 확인한다.
- [ ] 현재 compose/config/docs 상태를 확인한다.
- [ ] 필요한 절차를 수행한다.
- [ ] 검증 결과와 evidence를 기록한다.

##### Procedure

1. 관련 README와 operation 문서를 확인한다.
2. 작업 전 현재 상태를 기록한다.
3. 절차를 최소 변경으로 수행한다.
4. 검증 명령 또는 수동 확인을 실행한다.

#### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

#### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

#### Related Operational Documents

- [../README.md](../README.md)
- [../../05.operations/README.md](../../../README.md)
- [../../05.operations/incidents/README.md](../../../incidents/README.md)
