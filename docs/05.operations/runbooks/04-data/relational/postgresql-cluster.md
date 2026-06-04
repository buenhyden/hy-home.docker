---
status: active
---
<!-- Target: docs/05.operations/runbooks/04-data/relational/postgresql-cluster.md -->

# PostgreSQL Cluster Health and Recovery Triage Runbook

## PostgreSQL Cluster Health and Recovery Triage Procedure

> Scope: Triage optional PostgreSQL HA cluster health, etcd quorum symptoms, HAProxy routing, Patroni leadership, init job state, and exporter readiness without destructive data actions.

### Overview (KR)

이 런북은 `postgresql-cluster` 선택 스택의 etcd, Patroni/Spilo, HAProxy, init job, exporter 상태 이상을 현재 compose 기준으로 점검하는 절차다. DCS destructive recovery, forced cluster bootstrap, leadership mutation, backup restore, volume replacement는 이 문서에서 검증된 복구 절차가 아니므로 에스컬레이션 대상으로 분리한다.

### Purpose

PostgreSQL HA cluster의 서비스 상태와 routing/leadership evidence를 수집하고, compose가 보장하는 범위 안에서만 비파괴 재기동과 상태 확인을 수행한다.

### Canonical References

- **Spec**: N/A — no upstream source
- **Policy**: [PostgreSQL cluster operations policy](../../../policies/04-data/relational/postgresql-cluster.md)
- **Guide**: [PostgreSQL cluster usage guide](../../../guides/04-data/relational/postgresql-cluster.md)

## When to Use

- `pg-router` write/read endpoint가 응답하지 않을 때
- `patronictl list`에서 leader/member 상태 확인이 필요할 때
- etcd node, PostgreSQL node, exporter, or `pg-cluster-init` 상태가 unhealthy/stopped일 때
- PostgreSQL cluster operations 문서와 현재 compose evidence를 함께 갱신해야 할 때

## Procedure

### Checklist

- [ ] 루트 compose에서 PostgreSQL cluster include가 선택적으로 주석 처리되어 있는지, 이번 런타임에서 의도적으로 활성화했는지 확인한다.
- [ ] secret 값을 출력하지 않는 명령만 사용한다.
- [ ] DCS data deletion, forced cluster bootstrap, leadership mutation, backup restore, credential rotation, database mutation이 필요한 경우 이 런북을 중단하고 에스컬레이션한다.
- [ ] 모든 명령 출력은 요약으로 기록하고 credential, SQL payload, application data는 기록하지 않는다.

### Steps

1. compose 렌더링을 확인한다.

   ```bash
   docker compose -f docker-compose.yml -f infra/04-data/relational/postgresql-cluster/docker-compose.yml --profile data --profile service config
   ```

2. 전체 서비스 상태를 확인한다.

   ```bash
   docker compose ps etcd-1 etcd-2 etcd-3 pg-router pg-cluster-init pg-0 pg-1 pg-2 pg-0-exporter pg-1-exporter pg-2-exporter
   ```

3. etcd endpoint health를 각 etcd container에서 확인한다.

   ```bash
   docker exec etcd-1 etcdctl endpoint health --endpoints=http://127.0.0.1:${ETCD_CLIENT_PORT:-2379}
   ```

4. Patroni leadership을 확인한다.

   ```bash
   docker exec pg-0 patronictl -c /home/postgres/postgres.yml list
   ```

5. HAProxy와 init job 로그를 확인한다.

   ```bash
   docker compose logs --tail=120 pg-router pg-cluster-init
   ```

6. PostgreSQL node와 exporter 로그를 확인한다.

   ```bash
   docker compose logs --tail=120 pg-0 pg-1 pg-2 pg-0-exporter pg-1-exporter pg-2-exporter
   ```

7. 컨테이너가 stopped 상태이고 데이터 작업이 필요하지 않은 경우 compose로 해당 서비스만 재기동한다. 예시는 `pg-router` 기준이며, 대상 서비스명은 현재 `docker compose ps` 결과에서 확인한 declared service로 제한한다.

   ```bash
   docker compose -f docker-compose.yml -f infra/04-data/relational/postgresql-cluster/docker-compose.yml --profile data --profile service up -d pg-router
   ```

### Verification Steps

- `docker compose ps ...`에서 intended services가 running 또는 healthy 상태인지 확인한다.
- `patronictl list`에서 leader와 members가 표시되는지 확인한다.
- `pg-router` 로그와 HAProxy config validation healthcheck가 정상인지 확인한다.
- exporter logs 또는 `/metrics` checks가 secret 값을 출력하지 않고 정상 evidence를 제공하는지 확인한다.

### Observability and Evidence Sources

- **Logs**: `docker compose logs --tail=120 pg-router pg-cluster-init pg-0 pg-1 pg-2`
- **Cluster state**: `patronictl list`
- **DCS state**: `etcdctl endpoint health`
- **Routing**: HAProxy stats route `pg-haproxy.${DEFAULT_URL}` and HAProxy healthcheck
- **Metrics**: `pg-0-exporter`, `pg-1-exporter`, `pg-2-exporter`

### Safe Rollback or Recovery Procedure

1. Documentation-only changes can be reverted by the current git diff or the logical commit that introduced them.
2. Runtime recovery in this runbook is limited to compose `up -d` for stopped declared services after evidence capture.
3. N/A — no verified DCS reset, forced cluster bootstrap, leadership mutation, backup restore, credential rotation, or volume rollback procedure is documented yet.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: Stop file or log inspection if secret material appears in output.
- **Eval Re-run**: Re-run `bash scripts/validation/check-repo-contracts.sh` and `bash scripts/validation/check-doc-implementation-alignment.sh` after documentation changes.

## Evidence

- Capture command names, pass/fail status, service states, image tags, sanitized logs, and leadership/routing summary.
- Do not capture secret values, SQL payloads, database row contents, or credential-backed connection strings.
- Record whether the cluster was optional/commented in root compose or explicitly included for the runtime session.

## Rollback or Recovery

N/A — no verified rollback or recovery procedure is documented beyond non-destructive compose restart and status verification. If DCS reset, forced cluster bootstrap, leadership mutation, backup restore, credential rotation, or volume replacement is required, preserve evidence and escalate.

## Escalation

Escalate to the owning operator when no leader can be identified, etcd quorum symptoms appear, HAProxy routing diverges from compose, `pg-cluster-init` repeatedly fails, logs show storage corruption, secret exposure risk appears, or any data operation is required. Include sanitized logs, rendered compose evidence, service states, leadership summary, and attempted steps.

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/relational/postgresql-cluster.md)
- [Operations policy](../../../policies/04-data/relational/postgresql-cluster.md)
- [Infra README](../../../../../infra/04-data/relational/postgresql-cluster/README.md)
