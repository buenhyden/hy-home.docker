---
status: active
---
<!-- Target: docs/05.operations/runbooks/11-laboratory/dashboard.md -->

# Laboratory Dashboard Recovery Runbook

## Laboratory Dashboard Recovery Procedure

> Scope: Homer dashboard static config, route hardening, and optional runtime evidence.

### Overview

이 런북은 optional Homer dashboard의 설정 오류, route hardening drift, UI 렌더링 실패를 진단하고 증거를 남기는 절차를 정의한다.

### Purpose

Homer 설정을 검증하고, direct host port 재노출이나 SSO/allowlist 누락을 빠르게 확인하며, runtime 변경이 필요하면 승인된 범위로 분리한다.

### Canonical References

- **Spec**: [Laboratory spec](../../../03.specs/11-laboratory/spec.md)
- **Policy**: [Dashboard policy](../../policies/11-laboratory/dashboard.md)
- **Guide**: [Dashboard guide](../../guides/11-laboratory/dashboard.md)

## When to Use

- `homer.${DEFAULT_URL}` 접속이 실패하거나 빈 화면이 표시될 때.
- `infra/11-laboratory/dashboard/config/config.yml` 변경 후 링크/아이콘이 깨질 때.
- hardening check에서 Homer route, direct port, static IP, healthcheck drift가 감지될 때.

## Procedure

### Checklist

- [ ] Dashboard root include가 optional/commented인지 또는 승인되어 활성화됐는지 기록한다.
- [ ] 최근 `config/config.yml`, compose label, `LAB_ALLOWED_CIDRS` 변경 내역을 기록한다.
- [ ] runtime restart가 필요한지와 승인 범위를 먼저 확인한다.

### Steps

1. YAML 구문을 확인한다: `yq eval . infra/11-laboratory/dashboard/config/config.yml`.
2. tier hardening을 확인한다: `bash scripts/hardening/check-all-hardening.sh 11-laboratory`.
3. 실행 중이면 상태와 로그를 기록한다: `docker ps --format '{{.Names}}\t{{.Status}}'`, `docker logs --tail 100 homer`.
4. route drift가 있으면 compose label을 current policy chain으로 복구한다.
5. config 수정이 필요하면 최소 diff로 수정하고 구문 검증을 다시 수행한다.

### Verification Steps

- `bash scripts/hardening/check-all-hardening.sh 11-laboratory`
- `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh`
- 활성화된 runtime에서 `homer.${DEFAULT_URL}` 접속 evidence를 기록한다.

### Observability and Evidence Sources

- **Logs**: `docker logs --tail 100 homer`
- **Static config**: [dashboard compose](../../../../infra/11-laboratory/dashboard/docker-compose.yml), [Homer config](../../../../infra/11-laboratory/dashboard/config/config.yml)

### Safe Rollback or Recovery Procedure

N/A — no verified broad runtime rollback is documented. Config correction, route hardening restoration, and approved service restart are the verified recovery boundaries.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: N/A
- **Eval Re-run**: hardening, root profile validation, doc traceability.

## Evidence

- Record command output, config validation result, route/hardening result, and any approved runtime action.

## Rollback or Recovery

If the observed failure requires deleting dashboard data, changing auth, or restarting services outside the approved scope, stop and escalate.

## Escalation

Escalate to the owning operator when verification fails, direct exposure appears, auth/allowlist changes are needed, or runtime restart/data mutation requires approval.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/11-laboratory/dashboard.md)
- [Operations policy](../../policies/11-laboratory/dashboard.md)
