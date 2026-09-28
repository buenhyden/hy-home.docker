---
title: "Dozzle Recovery Runbook"
version: "1.1.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0072"
parent_ids:
- "GDE-0072"
created: "2026-05-17"
---

# Dozzle Recovery Runbook

## When to Use

OIDC/CIDR denial, missing log stream, socket error, settings loss, suspected
compromise, 또는 승인된 upgrade에 사용한다.

## Procedure

1. 루트에서 validate하고 점검한다.

   ```bash
   docker compose --profile admin-logs config --quiet
   docker compose --profile admin-logs ps dozzle
   docker compose --profile admin-logs logs --tail=200 dozzle
   ```

2. OIDC issuer/client/secret/CA, CIDR, Docker socket, target container, Docker
   log-driver 증상을 구분한다. 기본적으로 raw application log는 캡처하지 않는다.
3. auth bypass나 socket compromise가 의심되면 Dozzle을 중지하고, OIDC client
   secret을 revoke/rotate하고, sanitized audit evidence를 보존한다. `:ro` socket
   flag가 Docker API mutation이 불가능했다는 증거는 아니다.
4. OIDC/CIDR/socket 통제가 검토된 후에만 재시작한다. 허용/거부된 identity/CIDR과
   예상 filtered visibility를 확인한다.

### Settings recovery and upgrade

Dozzle을 중지하고, bind-backed `/data` 전체를 protected storage로 복사하고, 먼저
production socket이 없는 isolated instance로 복원한다. upgrade 시에는 advisory/
release를 검토하고 해당 copy에서 OIDC, roles/filters, streaming,
actions/shell 기본값을 테스트한다. 비호환 시 image와 settings copy를 함께 롤백한다.

## Evidence

exit, source commit, OIDC/CIDR allow/deny boolean, visible container count,
settings checksum, 최종 socket/service 상태를 기록한다. log 내용은 redact한다.

## Rollback or Recovery

settings restore와 upgrade rehearsal은 **계획되었으나 미실행** 상태이다. Docker
로그는 별도의 logging backend recovery가 필요하며 Dozzle은 이를 복원할 수 없다.

## Escalation

socket compromise 의심, auth/CIDR bypass, secret exposure, log authority 누락,
settings 비호환이 있으면 중단한다.

## Traceability

- [Guide](../guides/0072-dozzle.md) (`GDE-0072`)
- [Policy](../policies/0072-dozzle.md) (`POL-0072`)
- [Dozzle Compose](../../../infra/11-laboratory/dozzle/docker-compose.yml)

## Related Documents

- [Dozzle authentication](https://dozzle.dev/guide/authentication)
