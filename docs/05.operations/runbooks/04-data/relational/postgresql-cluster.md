---
status: active
---
<!-- Target: docs/05.operations/runbooks/04-data/relational/postgresql-cluster.md -->

# postgresql-cluster Runbook

## Overview (KR)

이 런북은 `docs/05.operations/runbooks/04-data/relational/postgresql-cluster.md` 주제의 실행 절차를 정의한다. 기존 절차를 유지하면서 검증, evidence, rollback 기준을 명확히 한다.

## postgresql-cluster Procedure

> Scope: PostgreSQL Cluster High-Availability Recovery

> Patroni 및 etcd 기반 PostgreSQL 클러스터 장애 복구 및 유지보수 실행 지침
> Operational Procedures for Fault Recovery and Maintenance of Patroni and etcd-based PostgreSQL Clusters

---

### Overview (KR/EN)

#### KR

이 런북은 `postgresql-cluster` 장애 시 신속한 복구 및 유지보수 작업을 위한 실행 절차를 정의한다. 운영자가 즉시 따라 할 수 있는 단계와 검증 기준을 제공하여 서비스 중단을 최소화하는 것을 목적으로 한다.

#### EN

This runbook defines operational procedures for rapid recovery and maintenance in the event of a `postgresql-cluster` failure. It provides step-by-step instructions and verification criteria that operators can follow immediately to minimize service disruption.

### Purpose

- etcd 쿼럼 소실 시 클러스터 복구
- PostgreSQL 마스터 장애 시 수동 페일오버 및 상태 복구
- `pg-cluster-init`을 이용한 데이터베이스 초기화 재수행

### Canonical References

- **ARD**: `docs/02.architecture/requirements/0004-data-architecture.md`
- **Spec**: `docs/03.specs/04-data/spec.md`
- **Operation**: `docs/05.operations/runbooks/04-data/relational/postgresql-cluster.md`

## When to Use

- `patronictl list` 결과에서 리더가 없거나 쿼럼이 깨진 경우
- 계획된 점검을 위해 리더 노드를 변경(Switchover)해야 하는 경우
- `pg-router`를 통한 DB 접속이 불가능한 경우

## Procedure

### Checklist

- [ ] `docker compose ps`로 etcd 및 pg 노드 컨테이너 생존 확인
- [ ] `docker compose logs`로 에러 메시지 확인
- [ ] 데이터 볼륨(`DEFAULT_DATA_DIR`)의 디스크 여유 공간 확인

### Steps

#### 1. 클러스터 수동 리더 변경 (Switchover)

```bash
docker exec -it pg-0 patronictl -c /home/postgres/postgres.yml switchover
```

##### 2. etcd 쿼럼 복구 (전체 장애 시)

1. 모든 PostgreSQL 노드 정지: `docker compose stop pg-0 pg-1 pg-2`
2. etcd 데이터 초기화 (필요시): `rm -rf ${DEFAULT_DATA_DIR}/etcd/*`
3. etcd 서비스 재시작: `docker compose up -d etcd-1 etcd-2 etcd-3`
4. PostgreSQL 노드 순차 가동: `docker compose up -d pg-0` (이후 순차)

##### 3. 초기화 작업(pg-cluster-init) 재실행

```bash
docker compose rm -f pg-cluster-init
docker compose up pg-cluster-init
```

### Verification Steps

- [ ] `docker exec -it pg-0 patronictl -c /home/postgres/postgres.yml list` 실행 후 `Leader` 존재 확인
- [ ] `pg_isready -h localhost -p 15432 -U postgres` 명령으로 쓰기 포트 가용성 확인

### Observability and Evidence Sources

- **Signals**: Grafana PostgreSQL Dashboard, `pg-router` HAProxy Stats
- **Evidence to Capture**: `patronictl list` 출력 결과, `docker compose logs`

### Safe Rollback or Recovery Procedure

- [ ] 기존 클러스터 상태 보존을 위한 볼륨 백업 권장
- [ ] etcd 강제 무력화 전 반드시 데이터 무결성 검토

### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Evidence

- Capture command output, timestamps, and operator/agent actions for any execution of this runbook.

## Rollback or Recovery

- Use only recovery or rollback steps already documented in this runbook, including any `Safe Rollback or Recovery Procedure` subsection above.
- N/A for additional verified recovery steps: this file does not validate a broader service-specific rollback beyond the documented procedure.
- If the observed failure does not match the documented steps, stop changes, preserve evidence, and escalate under `## Escalation`.

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state.

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/relational/postgresql-cluster.md)
- [Operations policy](../../../policies/04-data/relational/postgresql-cluster.md)
- [Operations template](../../../../99.templates/operation.template.md)
