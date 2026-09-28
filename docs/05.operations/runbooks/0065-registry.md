---
title: "Docker Registry Runbook"
version: "1.1.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0065"
parent_ids:
- "GDE-0065"
created: "2026-05-17"
---

# Docker Registry Runbook

## When to Use

`/v2/` failure, push/pull 또는 digest mismatch, storage exhaustion, consistent
backup/restore, upgrade, 또는 별도로 승인된 garbage collection에 사용한다.

## Procedure

1. 저장소 루트에서 validate하고 bounded status를 캡처한다.

   ```bash
   docker compose --profile registry config --quiet
   docker compose --profile registry ps registry
   docker compose --profile registry logs --tail=200 registry
   ```

2. `${DEFAULT_REGISTRY_DIR}`가 존재하고, 예상 filesystem에 있으며, private artifact
   내용을 나열하지 않고도 충분한 여유 공간이 있는지 확인한다. client가 의도한 trusted
   endpoint에 도달하는지 확인하되, firewall/client trust를 넓히지 않는다.
3. digest mismatch가 발생하면 promotion을 중지하고, 예상/관찰된 digest를 기록하고,
   알려진 source에서 pull한다. evidence 위에 retag하거나 blob을 삭제하지 않는다.
4. storage와 network 점검 후 `registry`만 재시작한다. `/v2/`를 확인한 뒤 non-sensitive
   canary 하나를 push/pull하고 digest를 비교한다.

### Consistent backup and restore

1. tracked config에 read-only maintenance mode가 없으므로 push/pull을 차단하고
   `registry`를 중지한다.
2. `${DEFAULT_REGISTRY_DIR}` filesystem 전체를 protected storage로 snapshot하거나
   복사한다. source commit, filesystem snapshot/checksum, repository/tag/digest
   inventory를 기록한다. snapshot 완료 후에만 source를 다시 시작한다.
3. untrusted network route가 없는 isolated Registry로 복원한다. API, catalog/tag
   count를 확인하고 대표 집합을 digest로 pull한다.
4. digest 검증과 명시적 data replacement 승인 후에만 복원된 store를 promote한다.

### Garbage collection and upgrade

- GC는 destructive하다: backup을 확보/검증하고, registry를 중지 상태로 유지하거나
  검토된 read-only mode를 설정하고, 지원되면 dry-run을 실행하고, mark set을 검토한
  뒤 명시적 승인 하에서만 실행한다. 필요한 digest pull을 확인한다.
- upgrade 시에는 새 image를 isolated restored copy에 먼저 테스트한다. canary
  push/pull과 digest 동등성을 확인하며, format이나 동작이 호환되지 않으면 image와
  storage snapshot을 함께 되돌린다.

## Evidence

exit, endpoint boundary, source commit, snapshot ID/checksum, count, 선택된
digest, 최종 service state를 기록한다. credential이나 layer는 캡처하지 않는다.

## Rollback or Recovery

backup/restore, GC, upgrade rehearsal은 이 문서에서 **계획되었으나 미실행** 상태이다.
Registry storage에 대한 복구 단계로 `rm`을 절대 사용하지 않는다.

## Escalation

untrusted exposure, 알 수 없는 artifact provenance, backup 누락, digest mismatch,
filesystem corruption, 승인 없는 deletion/GC 요청이 있으면 중단한다.

## Traceability

- [Guide](../guides/0065-registry.md) (`GDE-0065`)
- [Policy](../policies/0065-registry.md) (`POL-0065`)
- [Registry Compose](../../../infra/09-tooling/registry/docker-compose.yml)

## Related Documents

- [Registry deployment](https://distribution.github.io/distribution/about/deploying/)
- [Garbage collection](https://distribution.github.io/distribution/about/garbage-collection/)
