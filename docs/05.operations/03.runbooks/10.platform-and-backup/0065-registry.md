---
title: "Docker Registry Runbook"
version: "2.0.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "operations"
artifact_id: "RUN-0065"
parent_ids:
- "GDE-0065"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Docker Registry Runbook

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the runbook payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Trigger and Scope

##### Trigger

Registry(`registry` service)의 장애 진단, 일관된 백업·복원, 업그레이드, 별도로 승인된
garbage collection 절차다.

`/v2/` failure, push/pull 또는 digest mismatch, storage exhaustion, consistent
backup/restore, upgrade, 또는 별도로 승인된 garbage collection에 사용한다.

##### Targets

- [Guide](../../01.guides/10.platform-and-backup/0065-registry.md) (`GDE-0065`)
- [Policy](../../02.policies/10.platform-and-backup/0065-registry.md) (`POL-0065`)
- [Registry Compose](../../../../infra/09-platform-ops/registry/docker-compose.yml)

- [Registry deployment](https://distribution.github.io/distribution/about/deploying/)
- [Garbage collection](https://distribution.github.io/distribution/about/garbage-collection/)

#### Preflight

##### Authority

작업 전에 승인자를 기록한다. 복원된 store 승격(data replacement)과 garbage collection은 명시적 승인이 있어야 하며, 책임자는 `@buenhyden`이다.

##### Environment

작업 전 점검은 아래 항목에 따른다.

###### 작업 선택과 복구 전제
<!-- core-payload-level:4 -->

변경 전에 정확한 서비스·데이터 경로·승인자·중단 영향을 기록하고 [공통 복구 전제](0021-backup-and-restore.md)를
적용한다. 격리 대상, 복구본 식별자·무결성, 여유 공간, 비밀 보관, 작성자 정지와
승격 승인 중 하나라도 불명확하면 중단한다. config·secret 교체는
[공통 수명주기 정책](../../02.policies/01.common/0006-infrastructure-optimization-governance.md)의
단일 파일 bind 재생성과 비밀 비노출 확인을 따른다. 재시작은 데이터 복원이나 자격 증명
폐기 검증을 대신하지 않는다.

#### Procedure

##### Steps

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| 1 | 저장소 루트에서 `registry` profile을 validate하고 bounded status를 캡처한다 | 문서에 기록 없음 | 실패 시 Stop Conditions에 따라 중단하고 @buenhyden에게 escalation |
| 2 | `${DEFAULT_REGISTRY_DIR}`의 존재, filesystem, 여유 공간과 client의 trusted endpoint 도달을 확인한다 | 문서에 기록 없음 | firewall/client trust를 넓히지 않고 중단한다 |
| 3 | digest mismatch가 발생하면 promotion을 중지하고 예상/관찰 digest를 기록한 뒤 알려진 source에서 pull한다 | 문서에 기록 없음 | evidence 위에 retag하거나 blob을 삭제하지 않고 중단한다 |
| 4 | storage와 network 점검 후 `registry`만 재시작하고 `/v2/` 응답과 canary push/pull digest를 비교한다 | `registry`가 정상이고 `/v2/`가 응답하며 canary digest가 동일하다 | 실패 시 Stop Conditions에 따라 중단하고 @buenhyden에게 escalation |
| 5 | Consistent backup and restore: push/pull을 차단하고 `registry`를 중지한다 | 문서에 기록 없음 | 실패 시 Stop Conditions에 따라 중단하고 @buenhyden에게 escalation |
| 6 | Consistent backup and restore: `${DEFAULT_REGISTRY_DIR}` 전체를 snapshot/복사하고 checksum과 inventory를 기록한 뒤 source를 다시 시작한다 | source commit, snapshot/checksum, repository/tag/digest inventory가 기록된다 | backup 누락이면 중단한다 |
| 7 | Consistent backup and restore: untrusted route가 없는 isolated Registry로 복원하고 API, catalog/tag count, 대표 digest pull을 확인한다 | API, catalog/tag count, 대표 집합의 digest pull이 확인된다 | 실패 시 Stop Conditions에 따라 중단하고 @buenhyden에게 escalation |
| 8 | Consistent backup and restore: digest 검증과 명시적 data replacement 승인 후에만 복원된 store를 promote한다 | 문서에 기록 없음 | 승인 없는 deletion/replacement 요청이면 중단한다 |
| 9 | 로컬 이미지 이관과 제거: 이미지를 `localhost:${REGISTRY_PORT:-5000}/<repository>:<tag>`로 태그하고 push한다 | 문서에 기록 없음 | 실패 시 Stop Conditions에 따라 중단하고 @buenhyden에게 escalation |
| 10 | 로컬 이미지 이관과 제거: push된 참조를 digest로 pull하여 push 출력의 digest와 비교하고 Task에 기록한다 | repository, tag, digest, 출처 Dockerfile이 Task에 기록된다 | digest가 다르면 로컬 태그를 제거하지 않는다 |
| 11 | 로컬 이미지 이관과 제거: 2단계 성공 후에만 로컬 태그를 제거한다 | 문서에 기록 없음 | 컨테이너가 사용하는 이미지는 제거하지 않는다 |
| 12 | 로컬 이미지 이관과 제거: 다시 사용하려면 Registry 참조를 pull하여 재태깅하거나 Dockerfile에서 재빌드한다 | 문서에 기록 없음 | 실패 시 Stop Conditions에 따라 중단하고 @buenhyden에게 escalation |

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

###### Consistent backup and restore
<!-- core-payload-level:4 -->

1. tracked config에 read-only maintenance mode가 없으므로 push/pull을 차단하고
   `registry`를 중지한다.
2. `${DEFAULT_REGISTRY_DIR}` filesystem 전체를 protected storage로 snapshot하거나
   복사한다. source commit, filesystem snapshot/checksum, repository/tag/digest
   inventory를 기록한다. snapshot 완료 후에만 source를 다시 시작한다. HOME 야간 Restic
   백업(RUN-0021)은 registry를 복사하지 않으므로 이 snapshot이 유일한 백업이다.
3. untrusted network route가 없는 isolated Registry로 복원한다. API, catalog/tag
   count를 확인하고 대표 집합을 digest로 pull한다.
4. digest 검증과 명시적 data replacement 승인 후에만 복원된 store를 promote한다.

###### Garbage collection and upgrade
<!-- core-payload-level:4 -->

- GC는 destructive하다: backup을 확보/검증하고, registry를 중지 상태로 유지하거나
  검토된 read-only mode를 설정하고, 지원되면 dry-run을 실행하고, mark set을 검토한
  뒤 명시적 승인 하에서만 실행한다. 추적되는 설정은 삭제를 활성화하지 않는다. 필요한 digest pull을 확인한다.
- upgrade 시에는 일관된 백업을 먼저 확보하고 Distribution release/스토리지 변경 사항을 검토한 뒤 새 image를 isolated restored copy에 먼저 테스트한다. canary
  push/pull과 digest 동등성을 확인하며, format이나 동작이 호환되지 않으면 image와
  storage snapshot을 함께 되돌린다.

###### 로컬 이미지 이관과 제거
<!-- core-payload-level:4 -->

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

##### Stop Conditions

untrusted exposure, 알 수 없는 artifact provenance, backup 누락, digest mismatch,
filesystem corruption, 승인 없는 deletion/GC 요청이 있으면 중단한다.

#### Verification

##### Expected Results

###### Service Checks
<!-- core-payload-level:4 -->

`docker compose --profile registry ps registry`가 정상이고 `/v2/`가 응답해야 한다. non-sensitive canary 하나를 push/pull한 뒤 digest를 비교한다.

###### Evidence
<!-- core-payload-level:4 -->

exit, endpoint boundary, source commit, snapshot ID/checksum, count, 선택된
digest, 최종 service state를 기록한다. credential이나 layer는 캡처하지 않는다.

##### Unverified Conditions

이 런북이 아직 관찰하지 못한 항목은 다음과 같다. 이 문서에는 아래 단계의 실행 결과가 기록되어 있지 않다.

- Consistent backup and restore(push/pull 차단과 `registry` 중지 포함): snapshot ID/checksum, catalog/tag count, 격리 복원 뒤 대표 digest pull 결과가 필요하다.
- 복원된 store의 promote(명시적 data replacement 승인 필요): 승인 기록과 digest 검증 결과가 필요하다.
- Garbage collection과 upgrade(destructive, 승인 필요): 백업 확보, dry-run, mark set 검토, 격리 복사본에서의 canary push/pull과 digest 동등성 관찰이 필요하다.
- 로컬 이미지 이관과 제거: push된 digest와 pull한 digest의 비교 결과, 로컬 태그 제거 기록이 필요하다.
- 재시작 후 `/v2/`와 canary push/pull digest 비교: 실행 결과가 필요하다.

#### Escalation

##### Next Owner

책임자는 `@buenhyden`이다. 위 Stop Conditions의 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

##### Recovery or Forward Repair

backup/restore, GC, upgrade rehearsal은 이 문서에서 **계획되었으나 미실행** 상태이다.
Registry storage에 대한 복구 단계로 `rm`을 절대 사용하지 않는다.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
