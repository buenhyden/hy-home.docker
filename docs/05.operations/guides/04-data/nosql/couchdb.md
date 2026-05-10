<!-- Target: docs/05.operations/guides/04-data/nosql/couchdb.md -->

# CouchDB Operation Policy

> Operational standards for managing a 3-node CouchDB cluster with replication focus.

---

## Overview (KR)

이 문서는 CouchDB 클러스터의 데이터 정합성 유지, 디스크 최적화(Compaction), 그리고 멀티 마스터 복제 환경에서의 운영 정책을 정의한다.

## Policy Type

`operational-standard`

## Target Audience

- Operator
- SRE
- Developer

## Purpose

클러스터 내 데이터 불일치를 방지하고, 지속적인 서비스 가용성을 보장하며, 리소스 효율적인 안정 운영을 목표로 한다.

## Service Level Objectives (SLO)

- **Availability**: 99.9% (Cluster consensus maintained)
- **Data Integrity**: Zero loss during node rotation
- **API Response**: 99th percentile < 500ms for standard requests

## Operational Procedures

### 1. Monitoring & Health Check

- **Endpoint**: `https://couchdb.${DEFAULT_URL}/_membership` 호출을 통해 모든 노드가 클러스터에 참여 중인지 확인한다.
- **Alerts**: 특정 노드의 `_up` 상태가 1분 이상 지속되지 않을 경우 경고 발생.

### 2. Disk Management (Compaction)

CouchDB는 Append-only 데이터베이스이므로 정기적인 압축 작업이 필수적이다.

- **Auto-compaction**: 배포 시 설정된 자동 압축 정책(Fragmentation threshold 30%)이 정상 작동하는지 모니터링한다.
- **Manual Trigger**: 디스크 부족 경고 시 `/database/_compact` API를 통해 강제 압축을 수행한다.

### 3. Backup & DR

- **CouchDB Replication**: 중요한 데이터베이스는 별도의 오프사이트(Off-site) CouchDB 인스턴스로 실시간 또는 정기 복제를 설정한다.
- **Metadata Backup**: `_users`, `_replicator` 시스템 데이터베이스를 정기적으로 백업한다.

## Common Pitfalls

- **Revision Sprawl**: 너무 잦은 업데이트는 `_rev` 기록을 방대하게 만들어 뷰 인덱싱 성능을 저하시킨다. 정기적인 리비전 제한 수(`revs_limit`) 설정을 검토한다.
- **Shared Secret Conflict**: 클러스터 노드 간 `COUCHDB_SECRET`이 일치하지 않으면 노드 간 통신 및 복제가 실패한다.

## Related Documents

- **Infrastructure**: [CouchDB Infrastructure](../../../../../infra/04-data/nosql/couchdb/README.md)
- **Usage**: [CouchDB Cluster Usage](./couchdb.md)
- **Procedure**: [CouchDB Recovery Procedure](./couchdb.md)

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

> Migrated from `docs/05.operations/04-data/nosql/couchdb.md` during the 2026-05-10 operations taxonomy consolidation.

### CouchDB Cluster Usage

> Document-oriented NoSQL database optimized for multi-master replication and synchronization.

---

#### Overview (KR)

이 문서는 CouchDB 3-노드 클러스터의 아키텍처, 데이터 동기화 메커니즘 및 `hy-home.docker` 환경에서의 사용 가이드를 제공한다. CouchDB의 HTTP 기반 API와 강력한 복제 기능을 활용하는 방법을 설명한다.

#### Usage Type

`system-guide`

#### Target Audience

- Developer
- Operator
- Agent-tuner

#### Purpose

애플리케이션 개발자가 CouchDB의 오프라인 우선(Offline-first) 데이터 동기화 기능을 이해하고, 클러스터 환경에서 가용성 높은 서비스를 구축할 수 있도록 돕는다.

#### Prerequisites

- `infra/04-data/nosql/couchdb` 클러스터 배포 환경
- HTTP REST API 및 JSON 데이터 형식에 대한 기본 지식
- PouchDB 또는 CouchDB 클라이언트 라이브러리에 대한 이해

#### Step-by-step Instructions

##### 1. 클러스터 상태 확인

CouchDB 전체 노드가 정상적으로 연결되어 있는지 상태를 확인한다.

```bash
### 특정 노드 상태 확인
curl -u ${COUCHDB_USER}:${COUCHDB_PASSWORD} https://couchdb.${DEFAULT_URL}/_up
```

##### 2. 데이터베이스 및 문서 생성

CouchDB는 모든 작업을 HTTP API를 통해 수행한다.

```bash
### 데이터베이스 생성
curl -X PUT -u ${COUCHDB_USER}:${COUCHDB_PASSWORD} https://couchdb.${DEFAULT_URL}/my_database

### 문서 생성
curl -X POST -H "Content-Type: application/json" \
     -u ${COUCHDB_USER}:${COUCHDB_PASSWORD} \
     https://couchdb.${DEFAULT_URL}/my_database \
     -d '{"name": "hy-home", "type": "NoSQL"}'
```

##### 3. 데이터 동기화 (Replication)

CouchDB의 핵심은 원격 데이터베이스 간의 동기화이다.

- **Check-pointer**: 복제 진행 상황을 추적하여 중단 시 재개 가능하게 한다.
- **Conflicts**: 동일 문서 동기화 시 발생하는 충돌을 리비전(`_rev`) 기반으로 해결한다.

##### 4. 뷰와 쿼리 (Views & Mango)

- **Design Documents**: Map-Reduce 뷰를 정의하여 인덱싱된 조회를 수행한다.
- **Mango Queries**: MongoDB와 유사한 JSON 스타일의 선언적 쿼리를 사용한다.

#### Common Pitfalls

- **Sticky Session**: Traefik 설정에서 Sticky Cookie가 비활성화되면 노드 간 리비전 불일치로 인해 예상치 못한 충돌이 발생할 수 있다.
- **Compaction**: CouchDB는 문서를 업데이트할 때마다 새 리비전을 생성하므로, 주기적인 컴팩션(Compaction) 작업이 없으면 디스크 사용량이 급격히 증가한다.
- **Admin Party**: 기본 인증이 설정되지 않은 경우 누구나 접근 가능한 위험이 있으므로 항상 Secrets 기반 인증을 확인한다.

#### Related Documents

- **Infrastructure**: [CouchDB Infrastructure](../../../../../infra/04-data/nosql/couchdb/README.md)
- **Operation**: [CouchDB Operations Policy](./couchdb.md)
- **Procedure**: [CouchDB Recovery Procedure](./couchdb.md)

## Procedure

> Migrated from `docs/05.operations/04-data/nosql/couchdb.md` during the 2026-05-10 operations taxonomy consolidation.

### CouchDB Recovery Procedure

> Emergency recovery procedures for CouchDB Cluster and node synchronization issues.

---

#### Overview (KR)

이 문서는 CouchDB 클러스터 정족수 상실, 노드 간 복제 중단, 또는 데이터 정합성 이슈 발생 시의 복구 절차를 정의한다.

#### Procedure Type

`incident-response`

#### Target Audience

- On-call Engineer
- SRE
- AI-Agent

#### Purpose

CouchDB 클러스터의 고가용성 상태를 복구하고, 노드 간 데이터 불일치를 해결하여 안정적인 문서 동기화 환경을 재구축한다.

#### Pre-remediation Checklist

- [ ] `https://couchdb.${DEFAULT_URL}/_membership` 결과 분석
- [ ] 노드 간 HTTP 통신(Port 5984) 및 Cluster 통신(Port 4369, 5986) 확인
- [ ] `couchdb_secret`이 모든 노드에서 동일한지 확인

#### Remediation Steps

##### Scenario 1: Node Out-of-Sync (Re-joining Cluster)

클러스터에서 이탈한 노드를 다시 조인시킨다.

1. 로그 확인: `docker logs couchdb-node1`
2. 노드 재시작:

   ```bash
   docker-compose restart couchdb-node1
   ```

3. 클러스터 수동 조인 (필요 시):
   (Setup API를 통해 이탈한 노드의 IP/Port를 다시 추가)

##### Scenario 2: High Fragmentation (Manual Compaction)

디스크 부족으로 인한 쓰기 거부 시 압축을 수행한다.

1. 모든 데이터베이스 목록 확인:

   ```bash
   curl -u ${USER}:${PASS} https://couchdb.${DEFAULT_URL}/_all_dbs
   ```

2. 특정 DB 압축 실행:

   ```bash
   curl -H "Content-Type: application/json" -X POST -u ${USER}:${PASS} \
        https://couchdb.${DEFAULT_URL}/<db_name>/_compact
   ```

#### Verification Steps

1. 클러스터 동기화 지연 확인:

   ```bash
   curl -u ${USER}:${PASS} https://couchdb.${DEFAULT_URL}/_scheduler/docs
   ```

2. 특정 문서 리비전 일치 여부 확인 (각 노드별 직접 쿼리).

#### Post-remediation Tasks

- `revs_limit` 정책 적정성 검토
- 디스크 자동 확장 트리거 점검
- 공유 시크릿(Secret) 관리 상태 재확인

#### Related Documents

- **Usage**: [CouchDB Cluster Usage](./couchdb.md)
- **Operation**: [CouchDB Operation Policy](./couchdb.md)

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
