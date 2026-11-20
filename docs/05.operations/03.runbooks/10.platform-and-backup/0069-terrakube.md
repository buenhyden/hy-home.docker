---
title: "Terrakube Recovery Runbook"
version: "2.0.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "operations"
artifact_id: "RUN-0069"
parent_ids:
- "GDE-0069"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Terrakube Recovery Runbook

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

Terrakube(`terrakube-api`, `terrakube-ui`, `terrakube-executor`)의 장애 진단, 조정된 백업·격리 복원,
업그레이드 절차다.

API/UI/executor failure, stuck run, OIDC failure, missing state/output, 또는
승인된 backup/restore/upgrade에 사용한다.

##### Targets

- [Guide](../../01.guides/10.platform-and-backup/0069-terrakube.md) (`GDE-0069`)
- [Policy](../../02.policies/10.platform-and-backup/0069-terrakube.md) (`POL-0069`)
- [Terrakube Compose](../../../../infra/09-platform-ops/terrakube/docker-compose.yml)

- [Terrakube documentation](https://docs.terrakube.io/)
- [Operations index](../../README.md)

#### Preflight

##### Authority

저장소 루트에서 작업한다.

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
| 1 | 새 Terrakube run을 동결하고 workspace/run ID, VCS ref, state key, component status, apply 진행 여부를 기록한다 | 문서에 기록 없음 | remote effect와 recovery owner를 파악하기 전에는 active apply를 중지하지 않고 중단 조건이면 @buenhyden에게 escalation |
| 2 | `iac` profile을 validate하고 `terrakube-api/ui/executor`의 상태와 로그를 점검한다 | `ps` 상태가 확인되고 `docker compose --profile iac config --quiet`가 통과한다 | 실패 시 Stop Conditions에 따라 중단하고 @buenhyden에게 escalation |
| 3 | 재시작 전에 UI, API DB, state/output, stuck execution 증상을 분류한다 | 문서에 기록 없음 | migration을 반복 재시도하거나 state를 로그로 다운로드하지 않고 취소/replay 전에 remote provider action을 확인한다 |
| 4 | dependency와 active-run check 후 실패한 component만 재시작한다 | 문서에 기록 없음 | job이나 apply replay는 별도 authorization 없이 하지 않는다 |
| 5 | Coordinated backup and isolated restore: scheduling을 차단하고 active run을 해결한 뒤 API/UI와 executor를 중지한다 | 문서에 기록 없음 | active/unknown apply가 있으면 중단한다 |
| 6 | Coordinated backup and isolated restore: DB, SeaweedFS `tfstate`, Keycloak 설정, Compose, secret 메타데이터의 복구 세트를 캡처하고 recovery-point receipt를 기록한다 | DB backup ID, object inventory, source commit, Keycloak/client configuration을 연결한 receipt 하나가 기록된다 | DB-object 불일치나 backup 불가면 중단한다 |
| 7 | Coordinated backup and isolated restore: 두 store를 isolated target으로 복원하고 provider, VCS webhook, executor egress를 비활성화한다 | 문서에 기록 없음 | 실패 시 Stop Conditions에 따라 중단하고 @buenhyden에게 escalation |
| 8 | Coordinated backup and isolated restore: 격리 store에서만 component set을 시작하고 organization/workspace/run count, state/output key, OIDC role mapping, non-applying plan을 확인한다 | count, 참조된 state/output key, OIDC role mapping, non-applying plan이 확인된다 | 복원된 executor를 live account로 향하게 하지 않고 중단한다 |
| 9 | Coordinated backup and isolated restore: 검토 후에만 승격하고 아니면 원본을 유지하며 격리 사본을 진단용으로 보존한다 | 문서에 기록 없음 | 사본 삭제는 보존 의무와 승인 확인 뒤 따로 처리한다 |

1. 새 Terrakube run을 동결한다. workspace/run ID, VCS ref, state key, component
   status, apply 진행 여부를 기록한다. remote effect와 recovery owner를 파악하기
   전에는 active apply를 중지하지 않는다.
2. bounded state를 validate하고 점검한다.

   ```bash
   docker compose --profile iac config --quiet
   docker compose --profile iac ps terrakube-api terrakube-ui terrakube-executor
   docker compose --profile iac logs --tail=200 terrakube-api terrakube-ui terrakube-executor
   ```

3. 재시작 전에 분류한다.
   - UI만: gateway와 OIDC redirect/claim을 점검한다.
   - API DB error: `mng-pg`를 점검한다. migration을 반복적으로 재시도하지 않는다.
   - missing state/output: state를 로그로 다운로드하지 않고 SeaweedFS bucket/key와
     DB reference를 점검한다.
   - stuck execution: Valkey coordination과 executor/Docker access를 점검하고,
     취소나 replay 전에 remote provider action을 확인한다.
4. dependency와 active-run check 후 실패한 component만 재시작한다. job이나 apply를
   replay하려면 별도 authorization이 필요하다.

###### Coordinated backup and isolated restore
<!-- core-payload-level:4 -->

1. scheduling을 차단하고, active run을 대기하거나 안전하게 해결한 뒤, Terrakube
   writer가 남지 않도록 API/UI와 executor를 중지한다.
2. 복구 세트는 Terrakube PostgreSQL 데이터베이스, SeaweedFS `tfstate` object/버전, 관련
   Keycloak client/role 설정, 추적되는 Compose, secret 메타데이터/보관 정보다. Valkey는 조정
   상태이므로 정지된 제어 플레인과 일관되면 된다. PostgreSQL에는 owner의 online
   logical/physical backup 절차를, `tfstate`에는
   [일일 백업](../05.databases-and-storage/0024-seaweedfs.md)에 포함되는 SeaweedFS 세트를 사용한다.
   일일 스케줄 자체가 DB와 object의 같은 복구 시점을 보장하지 않으므로 작성자 정지
   구간과 두 캡처의 일관성을 별도로 확인한다. DB backup ID, object
   snapshot/version inventory, source commit, Keycloak/client configuration을
   연결하는 recovery-point receipt 하나를 기록한다. secret/state 내용은 캡처하지 않는다.
3. 두 store를 모두 isolated target으로 복원한다. replacement secret을 사용하고
   provider, VCS webhook, executor egress를 비활성화한다.
4. isolated store에 대해서만 복원된 component set을 시작한다. organization/
   workspace/run count, 참조된 state/output key, OIDC role mapping, non-applying
   plan을 확인한다. 복원된 executor를 live account로 향하게 하지 않는다.
5. 검토 후에만 승격한다. 그렇지 않으면 원본을 그대로 두고 격리된 사본을 진단용으로
   보존한다. 사본 삭제는 보존 의무와 승인 여부를 확인한 뒤 따로 처리한다.

###### Upgrade
<!-- core-payload-level:4 -->

coordinated backup을 완료하고 모든 migration/release note를 검토하고 복원된
store에서 새 API/UI/executor를 테스트한 뒤, 호환되는 set을 upgrade한다. 실패
시에는 새 set을 중지하고 DB와 object를 이전 image로 함께 복원한다. migration 이후
DB/state 롤백 없이 image만 되돌리는 것은 안전하지 않다. SeaweedFS 사본 하나나 DB 덤프
하나만으로 복구 가능성을 추정하지 않는다.

###### 현재 실행 경로의 제한
<!-- core-payload-level:4 -->

인증 오류를 우회하거나 실제 plan/apply를 재시도하지 말고 `@buenhyden`에게 보고한다. 제한의 배경은 [Guide](../../01.guides/10.platform-and-backup/0069-terrakube.md#현재-실행-경로의-제한)를 따른다.

##### Stop Conditions

active/unknown apply, DB-object 불일치, Docker-socket 예기치 않은 access, auth
모호성, backup 불가, destructive migration이 있으면 중단한다.

#### Verification

##### Expected Results

###### Service Checks
<!-- core-payload-level:4 -->

`terrakube-api`, `terrakube-ui`, `terrakube-executor`의 `ps` 상태와 `docker compose --profile iac config --quiet` 통과를 확인한다.

###### Evidence
<!-- core-payload-level:4 -->

정제된 컴포넌트 health·run/workspace 개수·백업 ID/checksum·state-key 개수·
release/source 커밋·비적용 plan 결과와 최종 상태를 기록한다.

##### Unverified Conditions

이 런북이 아직 관찰하지 못한 항목은 다음과 같다. 이 문서에는 아래 항목의 실행 결과가 기록되어 있지 않다.

- Coordinated backup and isolated restore 전체(작성자 정지, 두 store 복원, 격리 component 시작): recovery-point receipt와 복원 뒤 organization/workspace/run count, state/output key, OIDC role mapping, non-applying plan 관찰이 필요하다.
- 실패한 component 재시작과 job/apply replay(별도 authorization 필요): 승인 기록과 재시작 뒤 `ps` 상태가 필요하다.
- Upgrade: 복원된 store에서 새 API/UI/executor를 테스트한 결과와 DB/object 동시 복원 가능성의 관찰이 필요하다.
- 현재 실행 경로의 제한(인증 오류 우회 금지): 문서는 인증 오류가 있는 상태를 @buenhyden에게 보고하라고만 기록하며, 해소 여부의 관찰 결과는 없다.

#### Escalation

##### Next Owner

책임자는 `@buenhyden`이다. 위 Stop Conditions의 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

##### Recovery or Forward Repair

이 coordinated backup/restore와 upgrade 단계는 **계획되었으나 미실행** 상태이다.
component restart나 단일 store snapshot으로 recovery했다고 주장하지 않는다.

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
