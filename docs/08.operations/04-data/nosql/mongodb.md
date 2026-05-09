<!-- Target: docs/08.operations/04-data/nosql/mongodb.md -->

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

- **Infrastructure**: [MongoDB Infrastructure](../../../../infra/04-data/nosql/mongodb/README.md)
- **Guide**: [MongoDB Replica Set Guide](../../../07.guides/04-data/nosql/mongodb.md)
- **Runbook**: [MongoDB Recovery Runbook](../../../09.runbooks/04-data/nosql/mongodb.md)

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
