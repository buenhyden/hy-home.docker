---
status: active
---
<!-- Target: docs/05.operations/runbooks/04-data/specialized/neo4j.md -->

# Neo4j Health and Recovery Triage Runbook

## Neo4j Health and Recovery Triage Procedure

> Scope: Triage root-active Neo4j service health, route assumptions, secret-backed authentication, and evidence capture without destructive data actions.

### Overview

이 런북은 `neo4j` 서비스가 unhealthy, stopped, route failure, or authentication failure 상태일 때 현재 compose에 맞는 점검 순서와 안전한 재시작 경계를 제공한다. offline dump/load, password rotation, data volume replacement는 이 문서에서 검증된 복구 절차가 아니므로 에스컬레이션 대상으로 분리한다.

### Purpose

Neo4j single Community service의 상태, secret-aware entrypoint, healthcheck, Traefik Browser route evidence를 수집하고 compose가 보장하는 범위 안에서만 비파괴 조치를 수행한다.

### Canonical References

- **Spec**: N/A — no upstream source
- **Policy**: [Neo4j operations policy](../../../policies/04-data/specialized/neo4j.md)
- **Guide**: [Neo4j usage guide](../../../guides/04-data/specialized/neo4j.md)

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
   docker compose --profile data --profile graph config neo4j
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
   docker compose --profile data --profile graph up -d neo4j
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
- **Config**: `docker compose --profile data --profile graph config neo4j`

### Safe Rollback or Recovery Procedure

1. Documentation-only changes can be reverted by the current git diff or the logical commit that introduced them.
2. Runtime recovery in this runbook is limited to compose `up -d neo4j` after evidence capture.
3. N/A — no verified offline dump/load, password rotation, data restore, or volume rollback procedure is documented yet.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: Stop file or log inspection if secret material appears in output.
- **Eval Re-run**: Re-run `bash scripts/validation/check-repo-contracts.sh` and `bash scripts/validation/check-doc-implementation-alignment.sh` after documentation changes.

## Evidence

- Capture command names, pass/fail status, service state, image tag, sanitized logs, and route status.
- Do not capture secret values or full credential-backed command output.
- Record whether the issue involves container health, Browser route, secret mount, or persistence symptoms.

## Rollback or Recovery

N/A — no verified rollback or recovery procedure is documented beyond non-destructive compose restart and status verification. If dump/load, password rotation, data mutation, or volume replacement is required, preserve evidence and escalate.

## Escalation

Escalate to the owning operator when `cypher-shell RETURN 1` fails after restart, logs show data corruption, the secret-aware entrypoint cannot read `/run/secrets/neo4j_password`, route labels differ from expected compose, secret exposure risk appears, or any data operation is required. Include sanitized logs, rendered compose evidence, service states, and attempted steps.

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/specialized/neo4j.md)
- [Operations policy](../../../policies/04-data/specialized/neo4j.md)
- [Infra README](../../../../../infra/04-data/specialized/neo4j/README.md)
