---
title: "Docker Registry Runbook"
version: "1.1.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
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

### 작업 선택과 복구 전제

변경 전에 정확한 서비스·데이터 경로·승인자·중단 영향을 기록하고 [공통 복구 전제](0021-backup-and-restore.md)를
적용한다. 격리 대상, 복구본 식별자·무결성, 여유 공간, 비밀 보관, 작성자 정지와
승격 승인 중 하나라도 불명확하면 중단한다. config·secret 교체는
[공통 수명주기 정책](../policies/0006-infrastructure-optimization-governance.md)의
단일 파일 bind 재생성과 비밀 비노출 확인을 따른다. 재시작은 데이터 복원이나 자격 증명
폐기 검증을 대신하지 않는다.

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

### 계획된 저장소 유지보수

추적되는 설정에는 읽기 전용 유지보수 모드가 없다. 일관된 파일시스템 백업을 위해
클라이언트를 차단하고 Registry를 중지한 다음, 전체 bind 디렉터리를 스냅샷/복사하고
카탈로그/태그/digest 인벤토리를 기록한다. 격리된 Registry로 복원하고, 승격 전에
`/v2/`, 카탈로그/태그, 선택된 digest의 pull을 검증한다. garbage collection을
하려면 Registry가 읽기 전용이거나 중지된 상태여야 하고 파괴적 데이터 작업에 대한 별도
승인도 받아야 한다. 업그레이드 전에는 일관된 백업을 확보하고 Distribution의 release/스토리지
변경 사항을 검토하고 복원된 사본으로 새 이미지를 테스트하고 push/pull/digest를
검증한다. 이 문서 작업에서는 백업, 복원, GC, 업그레이드를 실행하지 않았다.

### 로컬 이미지 이관과 제거

실행 중이 아닌 로컬 빌드 이미지는 Registry에 보관해 두고 `/`의 Docker 이미지 저장소에서는
빼 둘 수 있다. `${DEFAULT_REGISTRY_DIR}`는 데이터 디스크에
있다.

1. 이미지를 `localhost:${REGISTRY_PORT:-5000}/<repository>:<tag>`로 태그하고
   push한다.
2. push된 참조를 digest로 pull하고 push 출력의 digest와 비교한다. repository,
   tag, digest, 출처 Dockerfile을 Task에 기록한다.
3. 2단계가 성공한 후에만 로컬 태그를 제거한다. 실행 중이든 중지되었든 컨테이너가
   여전히 사용하는 이미지는 절대 제거하지 않는다.
4. 다시 사용하려면 Registry 참조를 pull하여 Compose 파일이 기대하는 이름으로
   재태깅하거나, 추적되는 Dockerfile에서 재빌드한다.

## Evidence

exit, endpoint boundary, source commit, snapshot ID/checksum, count, 선택된
digest, 최종 service state를 기록한다. credential이나 layer는 캡처하지 않는다.

## Rollback or Recovery

backup/restore, GC, upgrade rehearsal은 이 문서에서 **계획되었으나 미실행** 상태이다.
Registry storage에 대한 복구 단계로 `rm`을 절대 사용하지 않는다.

## Escalation

책임자는 `@buenhyden`이다. 아래 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

untrusted exposure, 알 수 없는 artifact provenance, backup 누락, digest mismatch,
filesystem corruption, 승인 없는 deletion/GC 요청이 있으면 중단한다.

## Traceability

- [Guide](../guides/0065-registry.md) (`GDE-0065`)
- [Policy](../policies/0065-registry.md) (`POL-0065`)
- [Registry Compose](../../../infra/09-platform-ops/registry/docker-compose.yml)

## Related Documents

- [Registry deployment](https://distribution.github.io/distribution/about/deploying/)
- [Garbage collection](https://distribution.github.io/distribution/about/garbage-collection/)
