---
status: active
---
<!-- Target: docs/05.operations/runbooks/11-laboratory/dozzle.md -->

# Dozzle Recovery Runbook

## Dozzle Recovery Procedure

> Scope: Dozzle route hardening, Docker socket read-only access, and log-stream evidence.

### Overview

이 런북은 Dozzle UI 접속 실패, 로그 스트림 중단, Docker socket 접근 오류가 발생했을 때 비파괴적으로 상태를 확인하고 복구 범위를 판단하는 절차를 정의한다.

### Purpose

Dozzle의 read-only Docker socket 경계와 SSO/allowlist route 경계를 유지하면서 로그 기반 트러블슈팅 evidence를 확보한다.

### Canonical References

- **Spec**: [Laboratory spec](../../../03.specs/11-laboratory/spec.md)
- **Policy**: [Dozzle policy](../../policies/11-laboratory/dozzle.md)
- **Guide**: [Dozzle guide](../../guides/11-laboratory/dozzle.md)

## When to Use

- `dozzle.${DEFAULT_URL}` UI가 응답하지 않을 때.
- 특정 컨테이너 로그가 보이지 않거나 실시간 업데이트가 멈출 때.
- `/var/run/docker.sock` permission 오류가 보일 때.

## Procedure

### Checklist

- [ ] Dozzle 컨테이너 상태와 최근 compose/socket 변경 내역을 기록한다.
- [ ] Docker socket mount가 `:ro`인지 확인한다.
- [ ] route middleware chain과 allowlist 변경 여부를 확인한다.

### Steps

1. static hardening을 확인한다: `bash scripts/hardening/check-all-hardening.sh 11-laboratory`.
2. root-active admin profile을 확인한다: `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh`.
3. 실행 중이면 상태와 로그를 기록한다: `docker ps --format '{{.Names}}\t{{.Status}}'`, `docker logs --tail 100 dozzle`.
4. socket drift가 있으면 `/var/run/docker.sock:/var/run/docker.sock:ro`로 복구한다.
5. route drift가 있으면 `gateway-standard-chain@file,dozzle-admin-ip@docker,sso-errors@file,sso-auth@file`로 복구한다.
6. runtime restart가 필요하면 영향 범위와 승인자를 기록한 뒤 Dozzle 단위로만 수행한다.

### Verification Steps

- `bash scripts/hardening/check-all-hardening.sh 11-laboratory`
- `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh`
- 활성화된 runtime에서 `dozzle.${DEFAULT_URL}` 접속과 log stream evidence를 기록한다.

### Observability and Evidence Sources

- **Logs**: `docker logs --tail 100 dozzle`
- **Static config**: [Dozzle compose](../../../../infra/11-laboratory/dozzle/docker-compose.yml)

### Safe Rollback or Recovery Procedure

N/A — no verified image rollback or data restore procedure is documented. Static boundary correction and approved single-service restart are the verified recovery boundaries.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: N/A
- **Eval Re-run**: hardening, root profile validation, doc traceability.

## Evidence

- Record hardening output, container status, relevant log tail, and any approved runtime action.

## Rollback or Recovery

If the observed failure requires changing Docker socket permissions beyond read-only, broad service restarts, or image rollback, stop and escalate.

## Escalation

Escalate to the owning operator when socket permission changes, auth/allowlist changes, destructive actions, or runtime restarts outside Dozzle scope are required.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/11-laboratory/dozzle.md)
- [Operations policy](../../policies/11-laboratory/dozzle.md)
