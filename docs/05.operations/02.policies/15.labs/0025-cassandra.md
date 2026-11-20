---
title: "Cassandra Operations Policy"
version: "3.0.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "operations"
artifact_id: "POL-0025"
parent_ids:
- "AD-0004"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Cassandra Operations Policy

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

독립 Cassandra LAB의 단일 노드·데이터 보존·인증 경계를 정의한다. HOME 소비자와 공유하지 않는다.

###### Authority
<!-- core-payload-level:4 -->

- Declared parent: [AD-0004](../../../02.architecture/01.descriptions/0004-data-architecture.md)
- [LAB Compose](../../../../labs/cassandra/docker-compose.yml)

##### Applies To

`labs/cassandra/docker-compose.yml`의 `cassandra-node1`, `cassandra-node1-data`, `lab_cassandra_core_net`와 연결 문서에 적용한다.

###### Exclusions
<!-- core-payload-level:4 -->

exporter와 Cassandra password secret은 현재 구현에 없다.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0025-R1 | 항상 | 필수: 공식 Compose에 선언된 공식 Cassandra 이미지의 `/var/lib/cassandra`를 named volume `cassandra-node1-data`에 영속한다 | none | none |
| POL-0025-R2 | 항상 | 금지: 기존 HOME/과거 anonymous volume의 자동 재사용·삭제 | none | none |
| POL-0025-R3 | 항상 | 필수: `AllowAllAuthenticator`/`AllowAllAuthorizer` 기본 상태를 무인증으로 취급한다 | none | none |
| POL-0025-R4 | 항상 | 필수: 내부 네트워크만 사용한다 | none | none |
| POL-0025-R5 | 항상 | 금지: host port·gateway route·실제 업무 소비자 추가 | none | none |
| POL-0025-R6 | 실제 인증·권한이 필요할 때 | 필수: 이미지 지원 설정과 무인증·오인증 거부를 격리 검증한 뒤 별도 승인된 소스 변경으로 적용한다 | 수동 | none |
| POL-0025-R7 | 백업 시 | 필수: release/schema/keyspace/replication/topology와 snapshot tag 및 모든 SSTable을 묶는다 | none | none |
| POL-0025-R8 | restore 검증 시 | 필수: 새 빈 격리 대상에서만 검증한다 | none | none |
| POL-0025-R9 | 운영 승인 시 | 필수: 용량·업그레이드·복구·보존 기간과 소비자 영향을 확인한 뒤 승인한다 | 수동 | none |
| POL-0025-R10 | 항상 | 필수: volume 삭제와 secret 변경은 별도 범위로 다룬다 | none | none |
| POL-0025-R11 | 정적 확인 시 | 허용: 정적 Compose 렌더와 승인된 read-only 건강 확인 | none | none |
| POL-0025-R12 | 항상 | 금지: 단일 노드를 HA로 주장 | none | none |
| POL-0025-R13 | 항상 | 금지: `nodetool` 건강을 복구 증거로 사용 | none | none |
| POL-0025-R14 | LAB 기동·중단·복구·정리 시 | 필수: `@buenhyden`이 승인하고 기존 상태 소유권을 확인한다 | 수동 | none |
| POL-0025-R15 | 항상 | 필수: `POL-0006`과 `POL-0021`을 따른다 | none | none |

- **Required:** 공식 Compose에 선언된 공식 Cassandra 이미지의 실제 `/var/lib/cassandra`를 named volume `cassandra-node1-data`(bind 대상 `${LAB_DATA_DIR}/cassandra/node1`)에 영속한다. 기존 HOME/과거 anonymous volume은 자동 재사용·삭제하지 않는다.
- **Required:** `AllowAllAuthenticator`/`AllowAllAuthorizer` 기본 상태를 무인증으로 취급한다. 내부 네트워크만 사용하며 host port·gateway route와 실제 업무 소비자를 추가하지 않는다.
- **Required:** 실제 인증·권한이 필요하면 이미지 지원 설정과 무인증·오인증 거부를 격리 검증한 뒤 별도 승인된 소스 변경으로 적용한다.
- **Required:** 백업은 release/schema/keyspace/replication/topology와 snapshot tag 및 모든 SSTable을 묶는다. restore는 새 빈 격리 대상에서만 검증한다.
- **Required:** 용량·업그레이드·복구·보존 기간과 소비자 영향을 확인한 뒤 운영을 승인한다. volume 삭제와 secret 변경은 별도 범위다.
- **Allowed:** 정적 Compose 렌더와 승인된 read-only 건강 확인.
- **Disallowed:** 단일 노드를 HA로 주장하거나 `nodetool` 건강을 복구 증거로 사용하지 않는다.

###### Accountable lifecycle boundary
<!-- core-payload-level:4 -->

@buenhyden이 LAB 기동·중단·복구·정리 승인과 기존 상태 소유권을 확인한다. [POL-0006](../01.common/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)과 [POL-0021](../10.platform-and-backup/0021-backup-and-restore.md)을 따른다.

##### Exceptions

###### Exception Conditions
<!-- core-payload-level:4 -->

승인된 예외 없음.

###### Approval and Review
<!-- core-payload-level:4 -->

이미지·profile·mount·접속·인증 계약 변경 시 검토한다.

#### Enforcement

##### Mechanisms

`LAB_DATA_DIR=/tmp/hy-home-lab-cassandra-static docker compose --env-file labs/.env.example -f labs/cassandra/docker-compose.yml --profile cassandra config --quiet`와 문서 링크 검사를 수행한다. 실제 CQL·복원은 `NOT_RUN`으로 기록한다.

##### Limits

다음 규칙은 정책이 이름 있는 자동 검사를 연결하지 않았다.

- 이름 있는 검사 없음(volume): `POL-0025-R1`, `POL-0025-R2`
- 이름 있는 검사 없음(접근): `POL-0025-R3`, `POL-0025-R4`, `POL-0025-R5`
- 이름 있는 검사 없음(백업): `POL-0025-R7`, `POL-0025-R8`
- 이름 있는 검사 없음(운영): `POL-0025-R10`
- 이름 있는 검사 없음(정적 확인): `POL-0025-R11`
- 이름 있는 검사 없음(금지): `POL-0025-R12`, `POL-0025-R13`
- 이름 있는 검사 없음(lifecycle): `POL-0025-R15`
- 수동 검토·승인에 의존(인증): `POL-0025-R6`
- 수동 검토·승인에 의존(운영): `POL-0025-R9`
- 수동 검토·승인에 의존(lifecycle): `POL-0025-R14`
- 정책이 스스로 밝힌 한계: 정적 Compose 렌더와 문서 링크 검사는 Mechanisms에 있으나 어느 규칙에 대응하는지 정책이 연결하지 않았다.
- 실제 CQL과 복원은 `NOT_RUN`으로 기록되며 실행 증거가 없다.

#### Ownership

##### Owner

이 정책의 소유자는 frontmatter의 `owner`인 `@buenhyden`이다.

##### Review Triggers

- Subject peers: [GDE-0025](../../01.guides/15.labs/0025-cassandra.md), [RUN-0025](../../03.runbooks/15.labs/0025-cassandra.md)
- [LAB 설명](../../../../labs/cassandra/README.md)
- [Cassandra backup](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/backups.html)

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
