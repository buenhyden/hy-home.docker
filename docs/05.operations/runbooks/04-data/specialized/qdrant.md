---
status: active
---
<!-- Target: docs/05.operations/runbooks/04-data/specialized/qdrant.md -->

# Qdrant Health and Recovery Triage Runbook

## Qdrant Health and Recovery Triage Procedure

> Scope: Triage root-active Qdrant service health, REST/gRPC route assumptions, persistence path, and evidence capture without destructive data actions.

### Overview

이 런북은 `qdrant` 서비스가 unhealthy, stopped, route failure, or readiness failure 상태일 때 현재 compose에 맞는 점검 순서와 안전한 재시작 경계를 제공한다. collection delete, snapshot recovery, volume replacement, cluster repair는 이 문서에서 검증된 복구 절차가 아니므로 에스컬레이션 대상으로 분리한다.

### Purpose

Qdrant single unprivileged service의 상태, `/readyz` healthcheck, REST/gRPC Traefik route, snapshot path evidence를 수집하고 compose가 보장하는 범위 안에서만 비파괴 조치를 수행한다.

### Canonical References

- **Spec**: N/A — no upstream source
- **Policy**: [Qdrant operations policy](../../../policies/04-data/specialized/qdrant.md)
- **Guide**: [Qdrant usage guide](../../../guides/04-data/specialized/qdrant.md)

## When to Use

- `qdrant`가 unhealthy, stopped, or missing 상태일 때
- `/readyz`가 200 응답을 반환하지 않을 때
- REST route `qdrant.${DEFAULT_URL}` 또는 gRPC route `qdrant-grpc.${DEFAULT_URL}` 경계를 확인해야 할 때
- Qdrant operations 문서와 현재 compose evidence를 함께 갱신해야 할 때

## Procedure

### Checklist

- [ ] 루트 compose에서 `infra/04-data/specialized/qdrant/docker-compose.yml`가 active include인지 확인한다.
- [ ] 현재 compose에는 Qdrant secret이 선언되어 있지 않음을 확인한다.
- [ ] collection delete, snapshot recovery, volume replacement, cluster repair가 필요한 경우 이 런북을 중단하고 에스컬레이션한다.
- [ ] 모든 명령 출력은 요약으로 기록하고 application data payload는 기록하지 않는다.

### Steps

1. compose 렌더링을 확인한다.

   ```bash
   docker compose --profile data --profile ai config qdrant
   ```

2. 서비스 상태를 확인한다.

   ```bash
   docker compose ps qdrant
   ```

3. 최근 로그를 확인한다.

   ```bash
   docker compose logs --tail=120 qdrant
   ```

4. REST readiness를 확인한다.

   ```bash
   curl -fsS "https://qdrant.${DEFAULT_URL}/readyz"
   ```

5. read-only collection inventory를 확인한다.

   ```bash
   curl -fsS "https://qdrant.${DEFAULT_URL}/collections"
   ```

6. 컨테이너가 stopped 상태이고 데이터 작업이 필요하지 않은 경우 compose로 재기동한다.

   ```bash
   docker compose --profile data --profile ai up -d qdrant
   ```

### Verification Steps

- `docker compose ps qdrant`에서 `qdrant`가 running 또는 healthy 상태인지 확인한다.
- `/readyz`가 200 response evidence를 제공하는지 확인한다.
- `docker compose --profile data --profile ai config qdrant`에서 `qdrant-data:/qdrant/storage:rw`와 `/qdrant/storage/snapshots`가 유지되는지 확인한다.

### Observability and Evidence Sources

- **Logs**: `docker compose logs --tail=120 qdrant`
- **Health**: `/readyz` and compose healthcheck
- **Route**: Traefik HTTP labels on `qdrant` and TCP labels on `qdrant-grpc`
- **Config**: `docker compose --profile data --profile ai config qdrant`

### Safe Rollback or Recovery Procedure

1. Documentation-only changes can be reverted by the current git diff or the logical commit that introduced them.
2. Runtime recovery in this runbook is limited to compose `up -d qdrant` after evidence capture.
3. N/A — no verified snapshot recovery, collection restore, volume replacement, or cluster rollback procedure is documented yet.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: Stop file or log inspection if application data or credentials appear in output.
- **Eval Re-run**: Re-run `bash scripts/validation/check-repo-contracts.sh` and `bash scripts/validation/check-doc-implementation-alignment.sh` after documentation changes.

## Evidence

- Capture command names, pass/fail status, service state, image tag, sanitized logs, route labels, and readiness summary.
- Do not capture vector payloads, collection data, credentials, or mutation API bodies.
- Record whether the issue involves container health, REST route, gRPC route, persistence, or snapshot-path symptoms.

## Rollback or Recovery

N/A — no verified rollback or recovery procedure is documented beyond non-destructive compose restart and status verification. If collection mutation, snapshot restore, volume replacement, or cluster repair is required, preserve evidence and escalate.

## Escalation

Escalate to the owning operator when `/readyz` fails after restart, logs show storage corruption, route labels differ from expected compose, a Qdrant secret/API-key requirement appears without compose support, or any data operation is required. Include sanitized logs, rendered compose evidence, service states, and attempted steps.

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/specialized/qdrant.md)
- [Operations policy](../../../policies/04-data/specialized/qdrant.md)
- [Infra README](../../../../../infra/04-data/specialized/qdrant/README.md)
