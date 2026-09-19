---
title: "Neo4j Health and Recovery Triage Runbook"
version: "1.1.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "RUN-0033"
parent_ids:
- "GDE-0033"
created: "2026-05-17"
---

# Neo4j Health and Recovery Triage Runbook

## Overview

> Scope: Triage root-active Neo4j service health, route assumptions, secret-backed authentication, and evidence capture without destructive data actions.

이 런북은 health triage와 별도 승인 후 수행할 Community offline dump의 격리 복원 rehearsal 계약을 제공한다. 이번 변경에서 dump/load나 database stop은 실행하지 않았다.

### Purpose

Neo4j single Community service의 상태, secret-aware entrypoint, healthcheck, Traefik Browser route evidence를 수집하고 compose가 보장하는 범위 안에서만 비파괴 조치를 수행한다.

## When to Use

- `neo4j`가 unhealthy, stopped, or missing 상태일 때
- `cypher-shell RETURN 1` healthcheck가 실패할 때
- Browser route `https://neo4j.${DEFAULT_URL}`가 응답하지 않을 때
- Neo4j operations 문서와 현재 compose evidence를 함께 갱신해야 할 때

## Procedure

### Checklist

- [ ] 루트 compose에서 `infra/04-data/specialized/neo4j/docker-compose.yml`가 active include인지 확인한다.
- [ ] secret 값을 출력하지 않는 명령만 사용한다.
- [ ] offline dump/load, password rotation, data volume replacement가 필요한 경우 이 런북을 중단하고 에스컬레이션한다.
- [ ] 모든 명령 출력은 요약으로 기록하고 secret 값은 기록하지 않는다.

### Steps

1. compose 렌더링을 확인한다.

   ```bash
   docker compose --profile graph config --quiet
   ```

2. 서비스 상태를 확인한다.

   ```bash
   docker compose ps neo4j
   ```

3. 최근 로그를 확인한다.

   ```bash
   docker compose logs --tail=120 neo4j
   ```

4. container-local secret mount로 Cypher health를 확인한다.

   ```bash
   docker exec neo4j sh -lc 'cypher-shell -a bolt://localhost:7687 -u neo4j -p "$(tr -d "\n" < /run/secrets/neo4j_password)" "RETURN 1;"'
   ```

5. 컨테이너가 stopped 상태이고 데이터 작업이 필요하지 않은 경우 compose로 재기동한다.

   ```bash
   docker compose --profile graph up -d neo4j
   ```

6. Browser route는 HTTP status만 확인한다.

   ```bash
   curl -fsSI "https://neo4j.${DEFAULT_URL}"
   ```

### Verification Steps

- `docker compose ps neo4j`에서 `neo4j`가 running 또는 healthy 상태인지 확인한다.
- `cypher-shell ... RETURN 1` 명령이 secret 값을 출력하지 않고 정상 종료되는지 확인한다.
- `curl -fsSI "https://neo4j.${DEFAULT_URL}"`가 gateway/TLS route evidence를 제공하는지 확인한다.

### Observability and Evidence Sources

- **Logs**: `docker compose logs --tail=120 neo4j`
- **Health**: compose healthcheck and container-local `cypher-shell RETURN 1`
- **Route**: Traefik labels on `neo4j`
- **Config**: `docker compose --profile graph config --quiet`

### Safe Rollback or Recovery Procedure

1. Documentation-only changes can be reverted by the current git diff or the logical commit that introduced them.
2. Runtime recovery in this runbook is limited to compose `up -d neo4j` after evidence capture.
3. 실패한 isolated target과 전용 volume을 폐기한다. source volume과 dump는 변경하지 않는다.

### Planned Isolated Restore Rehearsal

1. 사전 승인과 downtime window를 확보하고 database name, Community engine version, store format, schema/index/constraint inventory, label/relationship/count invariants, free space를 기록한다. password는 기록하지 않는다.
2. source database를 정상 offline 상태로 전환한 뒤 해당 Community version의 `neo4j-admin database dump`로 named database dump를 생성하고 checksum/manifest와 함께 보호한다. online Enterprise backup 명령을 사용하거나 live store files를 복사하지 않는다.
3. production network/volume을 공유하지 않는 fresh compatible Community target과 별도 test password를 준비한다.
4. target database가 없는 상태에서 `neo4j-admin database load`로 dump를 적재하고 target만 시작한다. partial/failed load target은 재사용하지 않는다.
5. database online state, constraints/indexes, label/relationship/count invariants, representative read-only Cypher, Browser/Bolt health를 검증한다.
6. 실패하면 target을 승격하지 않고 폐기한다. production cutover와 password rotation은 별도 승인 사항이다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: Stop file or log inspection if secret material appears in output.
- **Eval Re-run**: Re-run `python3 scripts/validation/check-document-links.py --mode all` after documentation changes.

## Evidence

- Capture command names, pass/fail status, service state, image tag, sanitized logs, and route status.
- Do not capture secret values or full credential-backed command output.
- Record whether the issue involves container health, Browser route, secret mount, or persistence symptoms.

## Rollback or Recovery

데이터 복구는 위 planned isolated rehearsal로만 검증한다. 이번 변경에서는 dump/load, password rotation, data mutation과 volume replacement를 실행하지 않았다.

## Escalation

Escalate to the owning operator when `cypher-shell RETURN 1` fails after restart, logs show data corruption, the secret-aware entrypoint cannot read `/run/secrets/neo4j_password`, route labels differ from expected compose, secret exposure risk appears, or any data operation is required. Include sanitized logs, rendered compose evidence, service states, and attempted steps.

## Traceability

- Declared parent: [Neo4j Usage Guide](guide.md) (`GDE-0033`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](guide.md) (`GDE-0033`), [Policy](policy.md) (`POL-0033`)

## Related Documents

- [Compose implementation: infra/04-data/specialized/neo4j/docker-compose.yml](../../../../../infra/04-data/specialized/neo4j/docker-compose.yml)

- [Neo4j backup and restore](https://neo4j.com/docs/operations-manual/current/backup-restore/)
- [Neo4j backup planning and edition scope](https://neo4j.com/docs/operations-manual/current/backup-restore/planning/)
- [Neo4j open-source licensing](https://neo4j.com/open-source-project/)

- [Operations index](../../../README.md)
- [Usage guide](guide.md)
- [Operations policy](policy.md)
- [Infra README](../../../../../infra/04-data/specialized/neo4j/README.md)
