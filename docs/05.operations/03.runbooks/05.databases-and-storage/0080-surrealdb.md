---
title: "SurrealDB Runbook"
version: "1.0.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "operations"
artifact_id: "RUN-0080"
parent_ids:
- "POL-0080"
created: "2026-09-19"
next_review_at: "2027-05-13"
---

# SurrealDB Runbook

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

이 런북은 `surrealdb`(`surrealdb`/`notebook` profile, `ai_net`, host port 없음)의 헬스 트리아지와 계획된 격리 export/import 리허설을 제공한다. 안전한 증거를 수집하고, namespace, database, auth scope, 스키마와 데이터를 보존하는 반복 가능한 복구 테스트를 정의한다.

- `surrealdb`가 없거나, 비정상이거나, 접근 불가한 경우.
- 인증, namespace/database 선택, 영속성이 의심되는 경우.
- 승인된 backup, upgrade, 또는 격리 restore 리허설을 계획 중인 경우.

##### Targets

- 선언된 parent: [SurrealDB Policy](../../02.policies/05.databases-and-storage/0080-surrealdb.md) (`POL-0080`)
- 관장 architecture: [AD-0011](../../../02.architecture/01.descriptions/0011-laboratory-architecture.md)
- 대상 peer 문서: [Guide](../../01.guides/05.databases-and-storage/0080-surrealdb.md), [Policy](../../02.policies/05.databases-and-storage/0080-surrealdb.md)

- [SurrealDB export](https://surrealdb.com/docs/reference/cli/surrealdb-cli/commands/export)
- [SurrealDB import](https://surrealdb.com/docs/reference/cli/surrealdb-cli/commands/import)
- [SurrealDB upgrades and patching](https://surrealdb.com/docs/manage/self-hosted/upgrades-and-patching)
- [SurrealDB authentication](https://surrealdb.com/docs/learn/security/authentication/summary)
- [SurrealDB licensing](https://surrealdb.com/license)
- [운영 인덱스](../../README.md)
- [Infrastructure README](../../../../infra/08-ai/open-notebook/README.md)

#### Preflight

##### Authority

- [ ] 저장소 루트에서 작업하고 선택한 정확한 profile을 기록한다.
- [ ] configuration commit, Dockerfile/[Compose](../../../../infra/08-ai/open-notebook/docker-compose.yml) 버전 권한과 [runtime version projection](../../../../infra/tech-stack.versions.json), 엔진 버전(Open Notebook에는 SurrealDB v2가 필수), namespace, database, 예상 스키마와 record invariant를 기록한다.
- [ ] `surreal_db_password`와 원본 레코드는 증거에서 제외한다.
- [ ] export, import, stop, upgrade, volume 작업 전에 별도 승인을 받는다.

##### Environment

리허설 전에 소스 버전, namespace/database, auth level, table/schema/permission 인벤토리, record-count invariant, export 옵션과 여유 용량을 기록한다(`Planned Isolated Restore Rehearsal` 1번 단계).

#### Procedure

##### Steps

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| 1 | `config --quiet`로 설정 렌더링 | Compose 렌더링과 서비스 상태가 정확한 source/profile과 일치 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 2 | `ps surrealdb`로 상태 확인 | Compose 렌더링과 서비스 상태가 정확한 source/profile과 일치 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 3 | `surreal is-ready`로 접근성 확인 | 문서에 기록 없음 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 4 | `logs --tail=120`으로 정제된 로그 검토 | 문서에 기록 없음 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 5 | Planned Isolated Restore Rehearsal: 승인 후 소스 버전/namespace/database/인벤토리/export 옵션/여유 용량 기록 | 문서에 기록 없음 | 승인 없으면 진행하지 않음, 보호된 credential 입력만 사용 |
| 6 | Planned Isolated Restore Rehearsal: 명시한 namespace/database로 `surreal export` 실행하고 manifest/checksum과 보존 | Export checksum과 선언된 scope가 리허설 입력과 일치 | credential은 export하지 않음 |
| 7 | Planned Isolated Restore Rehearsal: 프로덕션과 공유 없는 새 v2 호환 target과 별도 test credential 준비 | 문서에 기록 없음 | 근거와 별도 승인 전에는 v3를 사용하지 않음 |
| 8 | Planned Isolated Restore Rehearsal: v2 CLI 동작 확인 후 빈 target에 `surreal import` 실행 | 문서에 기록 없음 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 9 | Planned Isolated Restore Rehearsal: readiness/접근/table/스키마/permission/record-count/read-only 쿼리 검증 | 격리 target이 스키마, permission, count, 대표 read 검사를 통과하고 source는 변경되지 않음 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 10 | Planned Isolated Restore Rehearsal: import 오류/불일치 시 target 격리 보존 | 문서에 기록 없음 | 같은 target에서 재시도하지 않고 별도 빈 대상에서 재시도, 기존 volume 삭제는 별도 승인 |

1. 설정 렌더링: `docker compose --profile surrealdb config --quiet`.
2. 상태 확인: `docker compose --profile surrealdb ps surrealdb`.
3. 접근성 확인: `docker compose --profile surrealdb exec -T surrealdb /usr/local/bin/surreal is-ready --endpoint http://127.0.0.1:8000`.
4. 정제된 로그 검토: `docker compose --profile surrealdb logs --tail=120 surrealdb`.

###### Planned Isolated Restore Rehearsal
<!-- core-payload-level:4 -->

1. 승인을 받아 소스 버전, namespace/database, auth level, table/schema/permission 인벤토리, record-count invariant, export 옵션과 여유 용량을 기록한다. 보호된 credential 입력을 사용한다.
2. 명시적으로 지정한 namespace와 database에 대해 업스트림 `surreal export` 워크플로를 실행한다. manifest, checksum, 버전, scope, 캡처 시각, 보존 기간, 만료 시점과 함께 export를 보존한다. credential은 아티팩트에 export하지 않는다.
3. 프로덕션 port, network, volume, secret을 전혀 공유하지 않고 현재 배포의 v2 유지 정책에 맞는 새 호환 target을 준비한다. import에 필요한 auth scope로 별도 테스트 credential을 생성한다. 선택한 Open Notebook 이미지와의 v3 호환성을 단정하지 않으며, 정확한 이미지 조합의 근거와 별도 승인 전에는 v3를 사용하지 않는다.
4. 선택한 v2 CLI의 옵션·인증 및 import 처리 동작을 확인하고, 비어 있는 target과 명시적 namespace/database에 대해 업스트림 `surreal import` 워크플로를 실행한다.
5. readiness, 인증된 namespace/database 접근, table, 스키마 정의, permission, record-count invariant, 대표 read-only 쿼리를 검증한다. 증거를 정제한다.
6. import가 오류나 invariant 불일치를 보고하면 target을 부분 변경된 것으로 간주하고 격리 보존한다. 재시도는 별도의 빈 대상으로 하며 기존 volume 삭제는 진단·보존 종료 후 따로 승인받는다. 같은 target에서는 절대 재시도하지 않는다.

##### Stop Conditions

mount, 버전, namespace/database, 또는 인증이 선언된 상태와 다르면 증거 수집 후 중단한다.

#### Verification

##### Expected Results

###### Service Checks
<!-- core-payload-level:4 -->

- Compose 렌더링과 서비스 상태가 정확한 source/profile과 일치한다.
- Export checksum과 선언된 scope가 리허설 입력과 일치한다.
- 격리된 target이 스키마, permission, count, 대표 read 검사를 통과한다.
- source volume, route, credential, runtime이 전혀 변경되지 않았다.

###### Evidence
<!-- core-payload-level:4 -->

날짜, configuration commit, 서비스/profile, source와 target 버전, namespace/database 식별자, backup checksum, exit status, 정제된 invariant, 그리고 명시적 미실행/실행 상태를 기록한다. secret 값이나 원본 database 콘텐츠는 절대 기록하지 않는다.

##### Unverified Conditions

이 runbook은 아래 항목을 아직 관측하지 않았다.

- Planned Isolated Restore Rehearsal: 계획이며 이 문서에는 실행 결과가 기록되어 있지 않다. 격리 target의 import 후 스키마, permission, record-count, read-only 쿼리 통과가 있으면 검증된다.
- v3 호환성: 선택한 Open Notebook 이미지와의 v3 호환성은 단정하지 않으며 정확한 이미지 조합의 근거가 없다.
- Compose 렌더링, `is-ready`, 로그 확인: 관측 결과가 기록되어 있지 않다. 문서는 명시적 미실행/실행 상태를 evidence에 기록하라고 한다.

#### Escalation

##### Next Owner

credential, 버전/스토리지 형식 호환성, namespace/database scope, 부분 import, 파괴적 스토리지 변경, 또는 backup 부재로 안전한 진행이 불가능하면 중단하고 `@buenhyden`에게 연락한다.

##### Recovery or Forward Repair

restore 증거는 위의 계획된 격리 리허설로만 확보한다. 프로덕션 cutover, route 변경, secret rotation, upgrade, 스토리지 교체는 별도 승인이 필요하며 이 Runbook 범위에서 실행하지 않는다.

문서 변경은 범위가 한정된 diff로 되돌린다. 리허설이 실패하면 target과 전용 volume을 격리 보존하고 추가 쓰기를 중지한다. 삭제는 별도의 승인된 정리이며 자동 롤백이 아니다. source와 보호된 export는 그대로 둔다.

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
