---
title: "Lakehouse Operations Policy"
version: "2.0.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "operations"
artifact_id: "POL-0094"
parent_ids:
- "AD-0004"
created: "2026-09-23"
next_review_at: "2027-05-13"
---

# Lakehouse Operations Policy

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the policy payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Purpose and Scope

##### Objective

Iceberg 테이블은 내장 REST 카탈로그 뒤의 SeaweedFS 테이블 버킷 하나에 있다.
접근 범위, 파괴적 유지보수, 테스트 데이터의 분리가 통제 대상이다.

###### Authority
<!-- core-payload-level:4 -->

- [SeaweedFS policy](../05.databases-and-storage/0024-seaweedfs.md)
- SPEC-0262 Analytics labs migration
- [Lakehouse LAB Compose source](../../../../labs/lakehouse/docker-compose.yml)

##### Applies To

카탈로그 노출, 엔진 identity, namespace, 테이블 유지보수, 이미지 및 제거.

###### Exclusions
<!-- core-payload-level:4 -->

root `lakehouse` profile은 HOME SeaweedFS만 선택하므로 이 정책의 LAB 엔진 범위에 포함되지 않는다.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0094-R1 | 항상 | 필수: 엔진은 독립 LAB `labs/lakehouse/docker-compose.yml`의 `lab-lakehouse` profile로만 선택한다 | none | none |
| POL-0094-R2 | 항상 | 금지: root include, HOME network 합류, HOME 이름 선택 추가 | none | none |
| POL-0094-R3 | 항상 | 필수: root `lakehouse` profile은 HOME SeaweedFS만 선택한다 | none | none |
| POL-0094-R4 | HOME 서비스 탐색 시 | 필수: `LAB_LAKEHOUSE_S3_ENDPOINT`/`LAB_LAKEHOUSE_CATALOG_URI` 필수 입력(Kafka bootstrap endpoint 포함)으로만 찾는다 | none | none |
| POL-0094-R5 | 소유자가 LAB에서 도달 가능한 endpoint를 승인하기 전 | 필수: LAB은 렌더링 전용으로 둔다 | 수동 | none |
| POL-0094-R6 | 소유자가 endpoint를 승인하기 전 | 금지: HOME 카탈로그나 S3를 LAB network/host port/route에 임의로 게시 | 수동 | none |
| POL-0094-R7 | 항상 | 필수: HOME 카탈로그는 `object_net`에서만 접근 가능해야 한다 | none | none |
| POL-0094-R8 | 항상 | 금지: HOME 카탈로그의 route와 host port | none | none |
| POL-0094-R9 | 별도 구현 수정 전 | 금지: all-interface S3 listener 상태(`POL-0024` 미준수)를 compliant로 인정 | none | none |
| POL-0094-R10 | 항상 | 필수: 엔진은 `lakehouse` identity로 서명한다 | none | none |
| POL-0094-R11 | 항상 | 필수: 이 identity의 S3 액션과 테이블 버킷 정책은 lakehouse 버킷만 다룬다 | 격리된 실행(범위가 한정된 identity의 테이블 생성/쓰기/compact/삭제 가능과 다른 버킷 읽기 불가 증명) | none |
| POL-0094-R12 | 항상 | 필수: 정책은 열 개의 namespace 및 테이블 액션을 나열하고 정책 변경과 버킷 삭제는 제외한다 | none | none |
| POL-0094-R13 | 새 엔진 추가 시 | 필수: 이 identity를 재사용하거나 자체 범위의 identity를 받는다 | none | none |
| POL-0094-R14 | 항상 | 금지: 엔진의 admin identity 사용 | none | none |
| POL-0094-R15 | 항상 | 필수: `dev`와 `test`는 개발용/테스트용 테이블만 보관한다 | none | none |
| POL-0094-R16 | 운영과 유사한 데이터 보관 시 | 필수: 별도로 승인된 namespace를 쓴다 | 수동 | none |
| POL-0094-R17 | TLS와 인증기를 추가하는 검토된 변경이 있기 전 | 필수: Trino는 loopback host 포트만 열고 route를 두지 않는다 | none | none |
| POL-0094-R18 | 항상 | 필수: Flink REST API와 UI는 loopback host 포트만 열고 route를 두지 않는다 | none | none |
| POL-0094-R19 | 항상 | 필수: `web.submit.enable=false`로 JAR 업로드를 막는다 | none | none |
| POL-0094-R20 | Flink job 실행 시 | 필수: job은 JobManager 컨테이너 내부의 SQL client에서 실행한다 | none | none |
| POL-0094-R21 | 스트리밍 `INSERT` 실행 시 | 필수: job ID와 대상 테이블을 기록한다 | 수동 | none |
| POL-0094-R22 | 항상 | 필수: Great Expectations suite는 읽기 전용 검사만 허용한다 | none | none |
| POL-0094-R23 | 항상 | 필수: suite는 읽기 전용으로 마운트된 추적 파일이고 context는 ephemeral이며 `GX_ANALYTICS_ENABLED=false`로 둔다 | none | none |
| POL-0094-R24 | suite 실패 시 | 필수: 테이블 소유자에게 전달할 발견 사항으로 취급한다 | none | none |
| POL-0094-R25 | suite 실패 시 | 금지: 실패를 이유로 suite 변경 | none | none |
| POL-0094-R26 | 항상 | 필수: Spark의 기본 command는 읽기만 한다 | none | none |
| POL-0094-R27 | `expire_snapshots`/`remove_orphan_files`/`DROP … PURGE`(Trino의 `DROP TABLE`과 그 프로시저 포함) 실행 시 | 필수: 명시된 테이블과 기록된 이유를 갖춘다 | 수동 | none |
| POL-0094-R28 | 항상 | 필수: 불변 build input과 호환성 검토를 요구한다 | none | none |
| POL-0094-R29 | 항상 | 필수: Flink/Spark Iceberg를 함께 검토하고 Trino는 자체 내장 connector version과 상호 읽기/쓰기를 검증한다 | none | none |
| POL-0094-R30 | Flink Hadoop 3.5.0 사용 시 | 필수: Iceberg 1.11 baseline 3.4.3과 달라 통합 검증을 한다 | none | none |
| POL-0094-R31 | 항상 | 필수: 문서의 정적 검증과 runtime 운영 승인을 분리한다 | none | none |
| POL-0094-R32 | 항상 | 필수: `@buenhyden`이 named consumer/target/중단 영향/보존 기간/예외를 소유한다 | none | none |
| POL-0094-R33 | service image/profile/port/secret/mount, DDL/init, capacity 또는 backup 범위 변경 시 | 필수: 이 Policy와 linked Guide/Runbook을 함께 검토한다 | 수동 | none |
| POL-0094-R34 | engine secret/certificate 적용 시 | 필수: 이 subject의 credential 계약을 따른다 | none | none |
| POL-0094-R35 | 앱 인증 연동 시 | 필수: 적용되는 `POL-0079` 통제를 따른다 | none | none |
| POL-0094-R36 | source 반영/재기동 시 | 필수: `POL-0006`의 적용 통제를 따른다 | none | none |
| POL-0094-R37 | 보존/삭제 시 | 필수: `POL-0021`의 적용 통제를 따른다 | none | none |
| POL-0094-R38 | exporter/stateless job 적용 시 | 필수: database restore가 없더라도 설정/credential과 그 작업이 변경하는 upstream state를 통제 범위에 포함한다 | none | none |
| POL-0094-R39 | 소유 artifact/복구 지점/expiry가 불명확할 때 | 금지: 삭제/재생성 | none | none |
| POL-0094-R40 | 항상 | 금지: 기존 Exceptions 외의 새 예외를 승인된 것으로 간주 | none | none |

- 엔진은 독립 LAB `labs/lakehouse/docker-compose.yml`의 `lab-lakehouse` profile로만 선택한다(SPEC-0262). root
  include, HOME network 합류, HOME 이름 선택 추가를 금지한다. root `lakehouse` profile은 HOME
  SeaweedFS만 선택한다.
- LAB은 HOME 서비스를 `LAB_LAKEHOUSE_S3_ENDPOINT`·`LAB_LAKEHOUSE_CATALOG_URI` 필수 입력으로만
  찾는다. 소유자가 LAB에서 도달 가능한 endpoint를 승인하기 전까지 LAB은 렌더링 전용이며, 이를
  위해 HOME 카탈로그나 S3를 LAB network·host port·route에 임의로 게시하지 않는다(미결정, 별도
  승인). Kafka bootstrap endpoint도 같다.
- HOME 카탈로그는 `object_net`에서만 접근 가능해야 하고 라우트/host port를 금지한다. 현재 all-interface S3 listener는 edge_net/seaweed_internal에도 8181을 열어 이 통제가 미준수다(POL-0024). route/host port 부재와 authenticated catalog 동작은 더 좁은 통제이며 network 격리를 대신하지 않는다. 별도 구현 수정 전 compliant로 인정하지 않는다. 엔진은
  `lakehouse` identity로 서명하며, 이 identity의 S3 액션과 테이블 버킷
  정책은 lakehouse 버킷만 다룬다. 정책은 열 개의 namespace 및 테이블 액션을
  나열하며 정책 변경과 버킷 삭제는 제외한다. 새 엔진은 이 identity를 재사용
  하거나 자체 범위의 identity를 받는다. 어떤 엔진도 admin identity를 쓰지
  않는다.
- `dev`와 `test`는 개발용 테이블과 테스트용 테이블을 보관한다. 운영과
  유사한 데이터는 별도로 승인된 namespace가 필요하다.
- Trino의 HTTP API는 인증이 없다. TLS와 인증기를 추가하는 검토된 변경이
  있기 전까지는 loopback host 포트만 열고 라우트는 없다. 기본 engine command는 SQL 쓰기를 하지 않지만 dependency provisioning은 정책·namespace를 변경할 수 있다.
- Flink의 REST API와 UI도 인증이 없다. loopback host 포트만 열고 라우트는
  없으며, `web.submit.enable=false`로 설정해 이를 통한 JAR 업로드를 막는다.
  job은 JobManager 컨테이너 내부의 SQL client에서 온다. 스트리밍 `INSERT`는
  취소될 때까지 계속 쓴다. job ID와 대상 테이블을 기록한다.
- Great Expectations suite는 읽기 전용 검사만 허용한다. 현재 Trino username은 인증/authorization 경계가 아니므로 SQL 권한 강제는 미구현이다. suite는 읽기 전용으로 마운트된 추적
  파일이고, context는 ephemeral이며 `GX_ANALYTICS_ENABLED=false`다. 실패한
  suite는 테이블 소유자에게 전달할 발견 사항이지 suite를 바꿀 이유가 아니다.
- Spark의 기본 command는 읽기만 한다. `expire_snapshots`,
  `remove_orphan_files`, `DROP … PURGE`는 파일을 삭제하므로 명시된 테이블과
  기록된 이유가 필요하다. Trino의 `DROP TABLE`과 그 `expire_snapshots`/
  `remove_orphan_files` 테이블 프로시저도 동일하다.
- 불변 build input과 호환성 검토를 요구한다. 현재 checksum은 Flink 5개/Spark 2개 JAR ADD만 고정하며 base image tag·OS/Python 의존성은 불변 lock이 아니다. Flink/Spark Iceberg를 함께 검토하고 Trino는 자체 내장 connector version과 상호 읽기/쓰기를 검증한다. 현 Flink Hadoop 3.5.0은 Iceberg 1.11 baseline 3.4.3과 달라 통합 검증이 필요하다.

###### Accountable lifecycle boundary
<!-- core-payload-level:4 -->

적용 identity: `seaweedfs-table-bucket`, `flink-jobmanager`, `flink-taskmanager`, `great-expectations`, `spark`, `trino`. 문서의 정적 검증과 runtime 운영 승인을 분리한다. @buenhyden이 named consumer·target·중단 영향·보존 기간과 예외를 소유한다. service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 이 Policy와 linked Guide/Runbook을 함께 검토한다. engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 적용되는 [POL-0079](../03.identity-and-access/0079-application-auth-integration.md)를, source 반영·재기동은 [POL-0006](../01.common/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary), 보존·삭제는 [POL-0021](../10.platform-and-backup/0021-backup-and-restore.md)의 적용 통제를 따른다. exporter와 stateless job 자체에는 database restore가 없지만 설정·credential와 그 작업이 변경하는 upstream state는 제외되지 않는다. 소유 artifact·복구 지점·expiry가 불명확하면 삭제/재생성을 중단한다. 기존 Exceptions 외의 새 예외는 승인된 것으로 간주하지 않는다.

##### Exceptions

###### Exception Conditions
<!-- core-payload-level:4 -->

없음. 카탈로그 credential vending이나 라우트를 활성화하려면 검토된 변경이
필요하다.

###### Approval and Review
<!-- core-payload-level:4 -->

SeaweedFS, Iceberg, 엔진 업그레이드 시, 새 엔진 추가 시, 새 namespace가
생길 때마다 검토한다.

#### Enforcement

##### Mechanisms

Compose 렌더링, 카탈로그 확인, 그리고 범위가 한정된 identity가 테이블을
생성·쓰기·compact·삭제할 수 있고 다른 버킷은 읽을 수 없음을 증명하는
격리된 실행.

##### Limits

정책은 Compose 렌더링과 카탈로그 확인을 개별 규칙과 연결하지 않으며, 아래 규칙은 승인/검토에 의존하거나 강제 수단이 없다.

- 격리/endpoint: 수동 검토 `POL-0094-R5`~`R6`; 강제 수단 없음 `POL-0094-R1`~`R4`
- HOME 카탈로그: 강제 수단 없음 `POL-0094-R7`~`R9`
- identity/namespace: 수동 검토 `POL-0094-R16`; 강제 수단 없음 `POL-0094-R10`, `POL-0094-R12`~`R15`
- 엔진 노출/동작: 수동 검토 `POL-0094-R21`, `POL-0094-R27`; 강제 수단 없음 `POL-0094-R17`~`R20`, `POL-0094-R22`~`R26`
- build/호환성: 강제 수단 없음 `POL-0094-R28`~`R30`
- 책임/수명주기 경계: 수동 검토 `POL-0094-R33`; 강제 수단 없음 `POL-0094-R31`~`R32`, `POL-0094-R34`~`R40`
- HOME 카탈로그 `object_net` 격리는 현재 all-interface S3 listener 때문에 미준수(`POL-0024`)이다.
- Trino/Flink API는 인증이 없고 Trino username은 인증/authorization 경계가 아니므로 SQL 권한 강제는 미구현이다.
- LAB 도달 가능한 S3/catalog/Kafka endpoint 승인은 미결정이며 그 전까지 LAB은 렌더링 전용이다.
- build input은 Flink 5개/Spark 2개 JAR checksum만 고정하며 base image tag와 OS/Python 의존성은 불변 lock이 아니다.
- Flink Hadoop 3.5.0과 Iceberg 1.11 baseline 3.4.3의 통합 검증이 필요하다.

#### Ownership

##### Owner

이 정책의 소유자는 frontmatter의 `owner`인 `@buenhyden`이다.

##### Review Triggers

- [가이드](../../01.guides/15.labs/0094-lakehouse.md) (`GDE-0094`)
- [런북](../../03.runbooks/15.labs/0094-lakehouse.md) (`RUN-0094`)
- [LAB 공개 입력 예시](../../../../labs/.env.example)
- [Compose profile vocabulary](../01.common/0078-compose-profile-vocabulary.md)

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
