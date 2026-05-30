---
status: active
---
<!-- Target: docs/05.operations/runbooks/04-data/specialized/neo4j.md -->

# Neo4j Runbook

## Overview (KR)

이 런북은 Neo4j 데이터베이스의 백업 추출, 복구 및 관리자 패스워드 재설정 절차를 정의한다. 장애 발생 시 운영자가 즉시 실행할 수 있는 명령어를 제공한다.

## Neo4j Recovery Procedure

> Scope: Neo4j Graph Database

> Procedure for database backup/restore and password management for Neo4j within the `04-data/specialized` tier.

### Purpose

데이터 유실 방지를 위한 백업 수행 및 서비스 중단 시 빠른 데이터 복구를 지원한다.

### Canonical References

- [Data architecture ARD](../../../../02.architecture/requirements/0004-data-architecture.md)
- [Neo4j operations policy](../../../policies/04-data/specialized/neo4j.md)
- [Neo4j infra README](../../../../../infra/04-data/specialized/neo4j/README.md)

## When to Use

- 정기적인 데이터 백업(Dump)이 필요할 때.
- 기존 백업 수단으로부터 데이터를 복구해야 할 때.
- 관리자 패스워드 분실 또는 유출로 인한 재설정이 필요할 때.

## Procedure

### 1. Database Dump (Backup)

Neo4j Community Edition은 인스턴스를 중지한 후 오프라인 덤프를 수행해야 한다.

1. 인스턴스 중지: `docker compose stop neo4j`
2. 덤프 생성:

   ```bash
   docker run --rm \
     --volumes-from neo4j \
     -v $(pwd)/backups:/backups \
     neo4j:5.26.23-community \
     neo4j-admin database dump neo4j --to-path=/backups
   ```

3. 인스턴스 시작: `docker compose start neo4j`

#### 2. Database Load (Restore)

1. 인스턴스 중지: `docker compose stop neo4j`
2. 데이터 복구:

   ```bash
   docker run --rm \
     --volumes-from neo4j \
     -v $(pwd)/backups:/backups \
     neo4j:5.26.23-community \
     neo4j-admin database load neo4j --from-path=/backups --overwrite-destination=true
   ```

3. 인스턴스 시작: `docker compose start neo4j`

#### 3. Password Rotation

1. 승인된 secret rotation 절차로 Docker Secret `neo4j_password`를 갱신한다. 값은 문서나 로그에 남기지 않는다.
2. 서비스 재시작: `docker compose up -d --force-recreate neo4j`

### Verification Steps

- [ ] `docker compose ps` 결과 `neo4j` 상태가 `Up (healthy)`인지 확인.
- [ ] 아래 방식으로 secret 값을 history에 남기지 않고 연결 확인.

  ```bash
  read -rsp "Neo4j password: " NEO4J_PASSWORD; echo
  cypher-shell -u neo4j -p "$NEO4J_PASSWORD" "RETURN 1;"
  unset NEO4J_PASSWORD
  ```

### Observability and Evidence Sources

- **Signals**: Docker logs (`docker compose logs -f neo4j`), `/data/logs/neo4j.log`.
- **Evidence to Capture**: 덤프 파일 파일명 및 크기, 복구 로그 텍스트.

### Safe Rollback or Recovery Procedure

- 복구 실패 시, 기존 `neo4j-data` 볼륨의 백업 디렉토리를 보존하고 이전 시점의 덤프 파일을 사용하여 재시도한다.

---

### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Evidence

- Capture command output, timestamps, and operator or agent actions for any execution of this runbook.
- Record failed checks, observed symptoms, and the final recovery or escalation state in the related task or incident evidence.

## Rollback or Recovery

- Use only recovery or rollback steps already documented in this runbook, including any `Safe Rollback or Recovery Procedure` subsection above.
- N/A for additional verified recovery steps: this file does not validate a broader service-specific rollback beyond the documented procedure.
- If the observed failure does not match the documented steps, stop changes, preserve evidence, and escalate under `## Escalation`.

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state.

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/specialized/neo4j.md)
- [Operations policy](../../../policies/04-data/specialized/neo4j.md)
