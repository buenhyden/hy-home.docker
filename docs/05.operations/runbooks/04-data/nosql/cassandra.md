---
status: active
---
<!-- Target: docs/05.operations/runbooks/04-data/nosql/cassandra.md -->

# Cassandra Health and Recovery Triage Runbook

## Cassandra Health and Recovery Triage Procedure

> Scope: Triage Cassandra single-node runtime health, collect evidence, and perform only verified non-destructive recovery steps.

### Overview

이 런북은 `cassandra-node1` 또는 `cassandra-exporter` 상태 이상이 발생했을 때 현재 compose에 맞는 점검 순서와 안전한 재시작 경계를 제공한다. 데이터 복원, snapshot 교체, 볼륨 이동은 이 문서에서 검증된 절차가 아니므로 에스컬레이션 대상으로 분리한다.

### Purpose

Cassandra 단일 노드 선택 서비스의 장애 증거를 빠르게 수집하고, compose가 보장하는 범위 안에서만 서비스를 재기동하거나 확인한다.

### Canonical References

- **Spec**: N/A — no upstream source
- **Policy**: [Cassandra operations policy](../../../policies/04-data/nosql/cassandra.md)
- **Guide**: [Cassandra usage guide](../../../guides/04-data/nosql/cassandra.md)

## When to Use

- `cassandra-node1`가 unhealthy, stopped, or missing 상태일 때
- `nodetool status`가 expected `UN` 상태를 반환하지 않을 때
- `cassandra-exporter`가 Cassandra health 이후에도 metrics endpoint를 제공하지 않을 때
- NoSQL operations 문서와 현재 compose evidence를 함께 갱신해야 할 때

## Procedure

### Checklist

- [ ] 루트 compose에서 Cassandra include가 선택적으로 주석 처리되어 있는지, 이번 런타임에서 의도적으로 활성화했는지 확인한다.
- [ ] secret 값을 출력하지 않는 명령만 사용한다.
- [ ] 데이터 복원, snapshot 교체, 볼륨 이동, credential rotation이 필요한 경우 이 런북을 중단하고 에스컬레이션한다.
- [ ] 모든 명령 출력은 요약으로 기록하고 secret 값은 기록하지 않는다.

### Steps

1. compose 렌더링을 확인한다.

   ```bash
   docker compose -f docker-compose.yml -f infra/04-data/nosql/cassandra/docker-compose.yml --profile data --profile obs config
   ```

2. 컨테이너 상태를 확인한다.

   ```bash
   docker compose ps cassandra-node1 cassandra-exporter
   ```

3. Cassandra 로그에서 시작/health 관련 오류를 확인한다.

   ```bash
   docker compose logs --tail=120 cassandra-node1
   ```

4. 노드 상태를 확인한다.

   ```bash
   docker exec cassandra-node1 nodetool status
   ```

5. 컨테이너가 stopped 상태이고 데이터 복구 작업이 필요하지 않은 경우 compose로 재기동한다.

   ```bash
   docker compose -f docker-compose.yml -f infra/04-data/nosql/cassandra/docker-compose.yml --profile data --profile obs up -d cassandra-node1 cassandra-exporter
   ```

6. read-only CQL 확인을 수행한다.

   ```bash
   docker exec cassandra-node1 sh -lc 'cqlsh -u "$CASSANDRA_USER" -p "$(cat /run/secrets/cassandra_password)" -e "SELECT cluster_name, release_version FROM system.local;"'
   ```

### Verification Steps

- `docker compose ps cassandra-node1 cassandra-exporter`에서 `cassandra-node1`가 healthy 또는 running 상태인지 확인한다.
- `docker exec cassandra-node1 nodetool status`에서 node state가 `UN`인지 확인한다.
- read-only CQL query가 secret 값을 출력하지 않고 정상 종료되는지 확인한다.

### Observability and Evidence Sources

- **Logs**: `docker compose logs --tail=120 cassandra-node1`, `docker compose logs --tail=120 cassandra-exporter`
- **Metrics**: `cassandra-exporter` exposed ports `${CASSANDRA_EXPORTER_PORT:-8080}` and `${CASSANDRA_EXPORTER_LISTEN_PORT:-8081}`
- **Config**: `docker compose ... config` rendered output without secret values

### Safe Rollback or Recovery Procedure

1. Documentation-only changes can be reverted by the current git diff or the logical commit that introduced them.
2. Runtime recovery in this runbook is limited to compose `up -d` for the declared services after evidence capture.
3. N/A — no verified data restore, snapshot replacement, or volume rollback procedure is documented yet.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: Stop file or log inspection if secret material appears in output.
- **Eval Re-run**: Re-run `bash scripts/validation/check-repo-contracts.sh` and `bash scripts/validation/check-doc-implementation-alignment.sh` after documentation changes.

## Evidence

- Capture command names, pass/fail status, service states, image tags, and sanitized log summaries.
- Do not capture secret values or full secret-backed command output.
- Record whether Cassandra was optional/commented in root compose or explicitly included for the runtime session.

## Rollback or Recovery

N/A — no verified rollback or recovery procedure is documented beyond non-destructive compose restart and status verification. If data corruption, snapshot restore, volume mutation, or credential rotation is suspected, preserve evidence and escalate.

## Escalation

Escalate to the owning operator when `nodetool status` does not return `UN`, logs show storage corruption, a restore is required, secret exposure risk appears, or the observed service set differs from `cassandra-node1` plus `cassandra-exporter`. Include sanitized logs, rendered compose evidence, service states, and attempted steps.

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/nosql/cassandra.md)
- [Operations policy](../../../policies/04-data/nosql/cassandra.md)
- [Infra README](../../../../../infra/04-data/nosql/cassandra/README.md)
