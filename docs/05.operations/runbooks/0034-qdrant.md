---
title: "Qdrant Health and Recovery Triage Runbook"
version: "1.3.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-25"
layer: "operations"
artifact_id: "RUN-0034"
parent_ids:
- "GDE-0034"
created: "2026-05-17"
---

# Qdrant Health and Recovery Triage Runbook

## Overview

> Scope: Triage root-active Qdrant service health, REST route (SSO) assumptions, persistence path, and evidence capture without destructive data actions.

이 런북은 health triage와 별도 승인 후 수행할 Qdrant snapshot의 격리 복원 rehearsal 계약을 제공한다. 이번 변경에서 snapshot create/recover API나 storage mutation은 실행하지 않았다.

### Purpose

Qdrant single unprivileged service의 상태, `/readyz` healthcheck, SSO 뒤의 REST Traefik route, snapshot path evidence를 수집하고 compose가 보장하는 범위 안에서만 비파괴 조치를 수행한다.

## When to Use

- `qdrant`가 unhealthy, stopped, or missing 상태일 때
- `/readyz`가 200 응답을 반환하지 않을 때
- REST route `qdrant.${DEFAULT_URL}`(SSO 뒤) 경계를 확인해야 할 때
- Qdrant operations 문서와 현재 compose evidence를 함께 갱신해야 할 때

## Procedure

### Checklist

- [ ] 루트 compose에서 `infra/04-data/specialized/qdrant/docker-compose.yml`가 active include인지 확인한다.
- [ ] `secrets/data/qdrant_api_key.txt`와 `secrets/data/qdrant_read_only_api_key.txt`가 있고 비어 있지 않은지 값을 읽지 않고 확인한다(`test -s`).
- [ ] collection delete, snapshot recovery, volume replacement, cluster repair가 필요한 경우 이 런북을 중단하고 에스컬레이션한다.
- [ ] 모든 명령 출력은 요약으로 기록하고 application data payload는 기록하지 않는다.

### Steps

1. compose 렌더링을 확인한다.

   ```bash
   docker compose --profile qdrant config --quiet
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
   # 6333 is the default QDRANT_PORT; substitute it if changed.
   docker compose exec qdrant bash -c 'exec 3<>/dev/tcp/127.0.0.1/6333; printf "GET /readyz HTTP/1.0\r\n\r\n" >&3; cat <&3'
   ```

5. read-only collection inventory를 확인한다.

   ```bash
   docker compose exec qdrant bash -c 'exec 3<>/dev/tcp/127.0.0.1/6333; printf "GET /collections HTTP/1.0\r\napi-key: %s\r\n\r\n" "$(tr -d "\r\n" </run/secrets/qdrant_api_key)" >&3; cat <&3'
   ```

6. 컨테이너가 stopped 상태이고 데이터 작업이 필요하지 않은 경우 compose로 재기동한다.

   ```bash
   docker compose --profile qdrant up -d qdrant
   ```

### Verification Steps

- `docker compose ps qdrant`에서 `qdrant`가 running 또는 healthy 상태인지 확인한다.
- `/readyz`가 200 response evidence를 제공하는지 확인한다.
- `docker compose --profile qdrant config --quiet`가 통과하는지 확인하고, source Compose에서 `qdrant-data:/qdrant/storage:rw`와 `/qdrant/storage/snapshots`가 유지되는지 비교한다.

### Observability and Evidence Sources

- **Logs**: `docker compose logs --tail=120 qdrant`
- **Health**: `/readyz` and compose healthcheck
- **Route**: Traefik HTTP labels on `qdrant` with SSO; no gRPC route
- **Config**: `docker compose --profile qdrant config --quiet`

### Safe Rollback or Recovery Procedure

1. Documentation-only changes can be reverted by the current git diff or the logical commit that introduced them.
2. Runtime recovery in this runbook is limited to compose `up -d qdrant` after evidence capture.
3. 실패한 isolated target과 전용 volume을 폐기한다. source service, snapshot과 tracked volume은 변경하지 않는다.

### Planned Isolated Restore Rehearsal

1. 사전 승인 후 source engine minor version, collection list/config/status, aliases, point-count invariants, snapshot scope/identifier와 free disk를 기록한다. API key가 켜져 있는지도 기록한다.
2. approved collection or full-storage snapshot을 생성하고 `/qdrant/storage/snapshots`에서 manifest/checksum과 함께 보호한다. snapshot API response나 vector payload를 evidence에 복사하지 않는다.
3. production network/route/volume을 공유하지 않는 fresh target을 same minor 또는 upstream이 허용하는 next minor로 준비한다. snapshot 크기의 약 2배 free disk와 absent target collection을 확인한다.
4. collection snapshot recovery API 또는 full-storage startup recovery 중 snapshot type에 맞는 upstream procedure 하나만 사용한다. `force`는 target collision이 명시적으로 검토된 경우에만 별도 승인한다.
5. `/readyz`, collection status/config, aliases, point counts와 representative search invariants를 검증한다. version, checksum 또는 count mismatch면 승격하지 않는다.
6. 실패하면 target을 폐기한다. production route switch, API key 교체, collection deletion과 volume replacement는 별도 승인 사항이다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: Stop file or log inspection if application data or credentials appear in output.
- **Eval Re-run**: Re-run `python3 scripts/validation/check-document-links.py --mode all` after documentation changes.

## Evidence

- Capture command names, pass/fail status, service state, image tag, sanitized logs, route labels, and readiness summary.
- Do not capture vector payloads, collection data, credentials, or mutation API bodies.
- Record whether the issue involves container health, REST route, in-network gRPC, persistence, or snapshot-path symptoms.

## Rollback or Recovery

데이터 복구는 위 planned isolated rehearsal로만 검증한다. 이번 변경에서는 snapshot mutation, collection restore/delete, volume replacement와 route change를 실행하지 않았다.

## Escalation

Escalate to the owning operator when `/readyz` fails after restart, logs show storage corruption, route labels differ from expected compose, a client gets 401 because it lacks the API key, or any data operation is required. Include sanitized logs, rendered compose evidence, service states, and attempted steps.

## Traceability

- Declared parent: [Qdrant Usage Guide](../guides/0034-qdrant.md) (`GDE-0034`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](../guides/0034-qdrant.md) (`GDE-0034`), [Policy](../policies/0034-qdrant.md) (`POL-0034`)

## Related Documents

- [Compose implementation: infra/04-data/specialized/qdrant/docker-compose.yml](../../../infra/04-data/specialized/qdrant/docker-compose.yml)

- [Qdrant snapshots](https://qdrant.tech/documentation/operations/snapshots/)
- [Qdrant migration and recovery](https://qdrant.tech/documentation/migration-recovery-options/)

- [Operations index](../README.md)
- [Usage guide](../guides/0034-qdrant.md)
- [Operations policy](../policies/0034-qdrant.md)
- [Infra README](../../../infra/04-data/specialized/qdrant/README.md)
