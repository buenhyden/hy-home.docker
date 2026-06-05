---
status: active
---
<!-- Target: docs/05.operations/runbooks/11-laboratory/portainer.md -->

# Portainer Recovery Runbook

## Portainer Recovery Procedure

> Scope: optional Portainer route hardening, Docker socket boundary, and access evidence.

### Overview (KR)

이 런북은 optional Portainer UI 접속 실패, route hardening drift, Docker socket 연결 문제를 진단하는 절차를 정의한다. 관리자 비밀번호 초기화나 데이터 삭제는 이 런북의 검증된 자동 복구 범위가 아니다.

### Purpose

Portainer의 optional root include 상태와 write-capable Docker socket 위험을 명확히 기록하고, 비파괴적 evidence를 확보한 뒤 필요한 경우 승인 절차로 에스컬레이션한다.

### Canonical References

- **Spec**: [Laboratory spec](../../../03.specs/11-laboratory/spec.md)
- **Policy**: [Portainer policy](../../policies/11-laboratory/portainer.md)
- **Guide**: [Portainer guide](../../guides/11-laboratory/portainer.md)

## When to Use

- `portainer.${DEFAULT_URL}` UI 접속이 실패할 때.
- hardening check에서 Portainer route, image, static IP, healthcheck drift가 감지될 때.
- Portainer가 local Docker endpoint를 표시하지 못할 때.

## Procedure

### Checklist

- [ ] Portainer root include가 optional/commented인지 또는 승인되어 활성화됐는지 기록한다.
- [ ] Docker socket mount와 Portainer data path 변경 내역을 기록한다.
- [ ] 관리자 계정 reset, data restore, endpoint 등록 변경은 승인 필요 작업으로 분리한다.

### Steps

1. static hardening을 확인한다: `bash scripts/hardening/check-all-hardening.sh 11-laboratory`.
2. optional service가 실행 중이면 상태와 로그를 기록한다: `docker ps --format '{{.Names}}\t{{.Status}}'`, `docker logs --tail 100 portainer`.
3. Docker socket 존재 여부를 확인한다: `test -S /var/run/docker.sock`.
4. route drift가 있으면 `gateway-standard-chain@file,portainer-admin-ip@docker,sso-errors@file,sso-auth@file`로 복구한다.
5. 관리자 비밀번호 reset, helper container 실행, data volume restore/delete가 필요하면 중단하고 `## Escalation`으로 이동한다.

### Verification Steps

- `bash scripts/hardening/check-all-hardening.sh 11-laboratory`
- optional include가 활성화된 runtime에서 `portainer.${DEFAULT_URL}` 접속과 local endpoint evidence를 기록한다.

### Observability and Evidence Sources

- **Logs**: `docker logs --tail 100 portainer`
- **Static config**: [Portainer compose](../../../../infra/11-laboratory/portainer/docker-compose.yml)

### Safe Rollback or Recovery Procedure

N/A — no verified password reset, helper-container, data restore, or data deletion procedure is documented for autonomous execution.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: stop if secret, token, or temporary password output may be exposed.
- **Eval Re-run**: hardening, doc traceability.

## Evidence

- Record hardening output, optional include state, container status/log tail, and whether escalation was required.

## Rollback or Recovery

If password reset, endpoint mutation, Docker socket permission expansion, volume restore, or data deletion is required, stop and escalate.

## Escalation

Escalate to the owning operator for password reset, helper container execution, endpoint authorization, data restore/delete, or any runtime mutation outside static boundary correction.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/11-laboratory/portainer.md)
- [Operations policy](../../policies/11-laboratory/portainer.md)
