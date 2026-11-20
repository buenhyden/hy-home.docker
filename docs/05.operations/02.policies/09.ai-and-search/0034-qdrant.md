---
title: "Qdrant Operations Policy"
version: "2.0.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "operations"
artifact_id: "POL-0034"
parent_ids:
- "AD-0004"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Qdrant Operations Policy

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

이 정책은 root-active `HOME` Qdrant 운영 기준을 정의한다. 기준은 [Qdrant Compose 구현](../../../../infra/04-data/qdrant/docker-compose.yml)의 단일 service, exact `ai`/`ai-llm`/`qdrant` profiles, `ai_net`, API key secret, SSO 뒤의 REST route와 `/readyz` healthcheck다.

###### Authority
<!-- core-payload-level:4 -->

- Declared parent: [Data Tier (04-data) Architecture Description](../../../02.architecture/01.descriptions/0004-data-architecture.md) (`AD-0004`)

- [Infra README](../../../../infra/04-data/qdrant/README.md)

##### Applies To

- `infra/04-data/qdrant/docker-compose.yml`
- `qdrant` service와 `qdrant-data` volume
- SSO(`sso-auth@file`)와 API key 뒤에 있는 REST route `qdrant.${DEFAULT_URL}`; gRPC route는 없음
- `qdrant_api_key`(AI-008)에서 나온 API key; health endpoint만 이 키 없이 응답한다
- `qdrant_read_only_api_key`(AI-009)에서 나온 read-only API key로, Prometheus가 보유하는 유일한 키다; full key와 달라야 한다
- `QDRANT__STORAGE__SNAPSHOTS_PATH=/qdrant/storage/snapshots`
- `docs/05.operations` 아래에 연결된 guide와 runbook

###### Exclusions
<!-- core-payload-level:4 -->

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0034-R1 | 항상 | 필수: 문서는 Qdrant를 cluster가 아니라 단일 unprivileged service로 설명한다 | none | none |
| POL-0034-R2 | 모든 Qdrant client | 필수: key를 secret file에서 읽는다 | 수동 | none |
| POL-0034-R3 | 모든 Qdrant client | 금지: key를 Compose environment 값, logs, evidence에 노출 | 수동 | none |
| POL-0034-R4 | 외부 접근 가이드 | 필수: 선언된 SSO REST route 안에 머문다 | none | none |
| POL-0034-R5 | 외부 접근 가이드 | 금지: host port publishing이나 gRPC route를 암시 | none | none |
| POL-0034-R6 | persistence와 snapshot-path 표현 | 필수: `qdrant-data:/qdrant/storage:rw`와 `/qdrant/storage/snapshots`와 일치시킨다 | 문서 비교 / `docker compose --profile qdrant config --quiet` | none |
| POL-0034-R7 | 백업 inventory | 필수: collection이나 full-storage snapshot identifier, engine minor version, aliases, vector counts/config, checksum, retention, restore evidence를 기록한다 | 수동 | none |
| POL-0034-R8 | 항상 | 필수: snapshot file을 디스크에서 보호한다 | 수동 | none |
| POL-0034-R9 | restore rehearsal | 필수: 동일 minor 또는 다음 minor compatibility를 가진 새로운 isolated target을 사용한다 | 수동 | none |
| POL-0034-R10 | restore rehearsal | 필수: 명시적으로 검토된 force action이 아니면 target collection이 없어야 한다 | 수동 | none |
| POL-0034-R11 | restore rehearsal | 필수: snapshot 크기의 약 2배에 해당하는 여유 디스크를 둔다 | 수동 | none |
| POL-0034-R12 | promotion 전 | 필수: aliases, collection config/status, point counts, representative searches를 검증한다 | 수동 | none |
| POL-0034-R13 | upgrade/removal | 필수: restore-tested snapshot과 capacity review를 갖춘다 | 수동 | none |
| POL-0034-R14 | 읽기 전용 점검 | 허용: read-only `/readyz`, `/collections`(secret file의 key 사용), compose config rendering, service logs, evidence 수집용 `docker compose ps` | none | none |
| POL-0034-R15 | 문서 전용 수정 | 허용: image tag, profile, route, healthcheck, volume 설명을 compose와 일치시키는 수정 | 문서 비교 / `docker compose --profile qdrant config --quiet` / `check-document-links.py --mode all` | 검사 결과 |
| POL-0034-R16 | 항상 | 금지: 별도 owner 승인과 검증된 runbook evidence 없이 collection delete, snapshot restore, volume replacement, cluster repair, data mutation 단계를 승인된 정책으로 제시 | 수동 | none |
| POL-0034-R17 | 항상 | 금지: API key를 제거하거나 key 없이 Qdrant를 호출하는 client 추가 | 수동 | none |
| POL-0034-R18 | 항상 | 필수: 문서의 정적 검증과 runtime 운영 승인을 분리한다 | none | none |
| POL-0034-R19 | service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 | 필수: 이 Policy와 linked Guide/Runbook을 함께 검토한다 | none | none |
| POL-0034-R20 | 항상 | 필수: engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 `POL-0079`를, source 반영·재기동은 `POL-0006`을, 보존·삭제는 `POL-0021`의 적용 통제를 따른다 | none | none |
| POL-0034-R21 | 소유 artifact·복구 지점·expiry가 불명확할 때 | 필수: 삭제/재생성을 중단한다 | none | none |
| POL-0034-R22 | 항상 | 금지: 기존 Exceptions 외의 새 예외를 승인된 것으로 간주 | none | none |

- **Required**: 문서는 Qdrant를 cluster가 아니라 단일 unprivileged service로 설명해야 한다.
- **Required**: 모든 Qdrant client는 secret file에서 key를 읽어야 하며 key가 Compose environment 값, logs, evidence에 절대 나타나서는 안 된다.
- **Required**: 외부 접근 가이드는 선언된 SSO REST route 안에 머물러야 하며, host port publishing이나 gRPC route를 암시해서는 안 된다.
- **Required**: persistence와 snapshot-path 표현은 `qdrant-data:/qdrant/storage:rw`와 `/qdrant/storage/snapshots`와 일치해야 한다.
- **Required**: 백업 inventory는 collection이나 full-storage snapshot identifier, engine minor version, aliases, vector counts/config, checksum, retention, restore evidence를 기록한다. snapshot file은 디스크에서 보호되며, API key는 그 파일에 대한 API 접근만 보호한다.
- **Required**: Restore rehearsal은 동일 minor 또는 다음 minor compatibility를 가진 새로운 isolated target을 사용하고, 명시적으로 검토된 force action이 아니면 target collection이 없어야 하며, snapshot 크기의 약 2배에 해당하는 여유 디스크가 필요하다.
- **Required**: promotion 전에 aliases, collection config/status, point counts, representative searches를 검증한다. Upgrade/removal에는 restore-tested snapshot과 capacity review가 필요하다.
- **Allowed**: read-only `/readyz`, `/collections`(secret file의 key 사용), compose config rendering, service logs, evidence 수집을 위한 `docker compose ps`.
- **Allowed**: image tag, profile, route, healthcheck, volume 설명을 compose와 일치시키는 문서 전용 수정.
- **Disallowed**: 별도의 owner 승인과 검증된 runbook evidence 없이 승인된 정책으로 제시되는 collection delete, snapshot restore, volume replacement, cluster repair, data mutation 단계.
- **Disallowed**: API key를 제거하거나 key 없이 Qdrant를 호출하는 client를 추가하는 행위.

###### Accountable lifecycle boundary
<!-- core-payload-level:4 -->

적용 identity: `qdrant`. 문서의 정적 검증과 runtime 운영 승인을 분리한다. @buenhyden이 named consumer·target·중단 영향·보존 기간과 예외를 소유한다. service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 이 Policy와 linked Guide/Runbook을 함께 검토한다. engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 적용되는 [POL-0079](../03.identity-and-access/0079-application-auth-integration.md)를, source 반영·재기동은 [POL-0006](../01.common/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary), 보존·삭제는 [POL-0021](../10.platform-and-backup/0021-backup-and-restore.md)의 적용 통제를 따른다. exporter와 stateless job 자체에는 database restore가 없지만 설정·credential와 그 작업이 변경하는 upstream state는 제외되지 않는다. 소유 artifact·복구 지점·expiry가 불명확하면 삭제/재생성을 중단한다. 기존 Exceptions 외의 새 예외는 승인된 것으로 간주하지 않는다.

##### Exceptions

###### Exception Conditions
<!-- core-payload-level:4 -->

N/A - 현재 승인된 예외 없음.

###### Approval and Review
<!-- core-payload-level:4 -->

- Qdrant compose image/profile/secret/route/snapshot-path 변경 시 검토한다.
- Stage 05 운영 문서 audit 주기 동안 검토한다.

#### Enforcement

##### Mechanisms

- compose 변경 후 이 정책을 [Qdrant guide](../../01.guides/09.ai-and-search/0034-qdrant.md), [Qdrant runbook](../../03.runbooks/09.ai-and-search/0034-qdrant.md), [infra README](../../../../infra/04-data/qdrant/README.md)와 비교한다.
- service-name, image, route, secret, healthcheck, volume 문서 갱신을 승인하기 전에 `docker compose --profile qdrant config --quiet`를 실행한다.
- 정책이나 연결된 운영 문서 갱신 후 `python3 scripts/validation/check-document-links.py --mode all`을 실행한다.

##### Limits

이 정책의 이름 붙은 검사는 문서 비교, `docker compose --profile qdrant config --quiet`, `check-document-links.py --mode all` 세 가지이며 모두 정적 문서 검증이라 아래 규칙은 검사 없이 수동 검토나 runbook 증거에 의존한다.

- 서비스 설명과 접근(POL-0034): R1, R4-R5에는 정책이 지정한 검사가 없다.
- key 취급(POL-0034): R2-R3, R17은 수동 검토나 승인에 의존한다.
- 백업과 복구(POL-0034): R7-R13은 수동 검토나 승인에 의존한다.
- 허용 사항(POL-0034): R14에는 정책이 지정한 검사가 없다.
- 승인 없는 변경(POL-0034): R16은 수동 검토나 승인에 의존한다.
- lifecycle 경계(POL-0034): R18-R22에는 정책이 지정한 검사가 없다.
- 세 검사는 runtime 운영 승인이나 실제 backup/restore를 증명하지 않는다.
- secret/key 취급, 백업 inventory, restore rehearsal, promotion 검증, 변경 금지 단계는 수동 검토와 runbook 증거에 의존하며 지정된 검사가 없다.

#### Ownership

##### Owner

이 정책의 소유자는 frontmatter `owner`에 기록된 @buenhyden이다.

##### Review Triggers

- Subject peers: [Guide](../../01.guides/09.ai-and-search/0034-qdrant.md) (`GDE-0034`), [Runbook](../../03.runbooks/09.ai-and-search/0034-qdrant.md) (`RUN-0034`)

- [Qdrant snapshots](https://qdrant.tech/documentation/operations/snapshots/)
- [Qdrant migration and recovery](https://qdrant.tech/documentation/migration-recovery-options/)
- [Operations index](../../README.md)
- [Usage guide](../../01.guides/09.ai-and-search/0034-qdrant.md)
- [Recovery runbook](../../03.runbooks/09.ai-and-search/0034-qdrant.md)

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
