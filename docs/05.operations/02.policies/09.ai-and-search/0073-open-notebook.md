---
title: "Open Notebook Operations Policy"
version: "2.0.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "operations"
artifact_id: "POL-0073"
parent_ids:
- "AD-0011"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Open Notebook Operations Policy

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

Open Notebook은 OPTIONAL 지식/모델 워크스페이스다. 콘텐츠, 데이터베이스,
provider 자격 증명, 암호화 키가 하나의 복구 경계를 이룬다.

###### Authority
<!-- core-payload-level:4 -->

- [Laboratory 아키텍처](../../../02.architecture/01.descriptions/0011-laboratory-architecture.md)

- [Open Notebook Compose 소스](../../../../infra/08-ai/open-notebook/docker-compose.yml)

##### Applies To

활성화, UI/API 노출, 앱/데이터베이스 인증, provider/모델 접근, 콘텐츠 보존,
백업/복구, floating 이미지 업그레이드, 제거.

###### Exclusions
<!-- core-payload-level:4 -->

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0073-R1 | 항상 | 필수: `notebook` profile로만 선택한다 | 수동 | none |
| POL-0073-R2 | 항상 | 금지: `admin`이 이를 선택 | 수동 | none |
| POL-0073-R3 | 항상 | 필수: HOME 밖에 유지한다 | none | none |
| POL-0073-R4 | upstream이 v3를 명시 지원·검증하기 전 | 금지: SurrealDB v3 이상으로의 업그레이드 | 수동 | none |
| POL-0073-R5 | 항상 | 필수: CIDR allowlist를 보존한다 | none | none |
| POL-0073-R6 | 항상 | 필수: API 호스트 포트를 loopback에 바인딩된 상태로 유지한다 | Mechanisms의 API 경계 검증 | none |
| POL-0073-R7 | 항상 | 필수: 애플리케이션 비밀번호와 SurrealDB 인증을 유지한다 | Mechanisms의 UI/앱 인증 검증 | none |
| POL-0073-R8 | SSO 재도입 | 필수: 소유자 결정으로만 한다 | 수동 | none |
| POL-0073-R9 | 항상 | 필수: provider 키는 앱의 암호화된 저장소에 보관한다 | none | none |
| POL-0073-R10 | 항상 | 필수: `open_notebook_encryption_key`는 별도로 보호한다 | none | none |
| POL-0073-R11 | 승인된 재암호화/내보내기 계획 없음 | 금지: `open_notebook_encryption_key` 회전 또는 분실 | 수동 | none |
| POL-0073-R12 | 항상 | 필수: 노트북, 소스 문서, 임베딩, 채팅, provider 설정을 민감 정보로 취급한다 | none | none |
| POL-0073-R13 | 사용 전 | 필수: 보존과 내보내기 소유권을 정의한다 | none | none |
| POL-0073-R14 | 백업 | 필수: SurrealDB를 논리적으로 백업한다 | none | none |
| POL-0073-R15 | 백업 | 필수: `/app/data`, 소스 커밋, 보호된 키/자격 증명 보관을 함께 백업한다 | none | none |
| POL-0073-R16 | 리허설 | 필수: provider egress를 비활성화한 상태로 리허설한다 | none | none |
| POL-0073-R17 | floating 이미지 승격 | 필수: 릴리스/보안 노트를 검토한다 | 수동 | none |
| POL-0073-R18 | floating 이미지 승격 | 필수: 승격 전에 마이그레이션과 자격 증명 복호화를 테스트한다 | none | none |
| POL-0073-R19 | 제거 전 | 필수: 콘텐츠/provider 자격 증명을 내보내거나 명시적으로 폐기한다 | none | none |
| POL-0073-R20 | 제거 시 | 필수: 데이터베이스와 앱 볼륨 삭제를 별개의 파괴적 작업으로 다룬다 | none | none |
| POL-0073-R21 | Ollama-mediated cloud와 direct cloud 도입 | 필수: 별도 credential, 허용 목적, network 및 비용 계약을 갖춘다 | 수동 | none |
| POL-0073-R22 | 항상 | 금지: Ollama-mediated cloud/direct cloud를 자동 fallback이나 동일 instance의 `OLLAMA_NO_CLOUD=1` 예외로 도입 | 수동 | none |
| POL-0073-R23 | 저장된 모델 등록 | 필수: 지원되는 product UI/API를 사용한다 | Mechanisms의 저장된 연결·terminal embedding job·재시작 후 보존 검증 | none |
| POL-0073-R24 | 저장된 모델·provider·embedding 기능 수용 | 금지: 환경 fallback, healthcheck, DB online 또는 디렉터리 존재를 근거로 수용 | Mechanisms의 저장된 연결·terminal embedding job·재시작 후 보존 검증 | none |
| POL-0073-R25 | 다른 credential과 충돌하는 동명 등록 | 필수: 등록을 보존하고 거부한다 | none | none |

- `notebook`만 사용한다. `admin`은 이를 선택해서는 안 된다. HOME 밖에 유지한다.
- Open Notebook upstream은 SurrealDB v2를 요구한다. upstream Open Notebook이
  v3를 명시적으로 지원하고 검증하기 전까지는 SurrealDB v3 이상으로의
  업그레이드가 금지된다.
- CIDR allowlist를 보존하고 API 호스트 포트를 loopback에 바인딩된 상태로
  유지한다. 공유 SSO가 없는 한 애플리케이션 비밀번호가 유일한 신원 통제이므로
  이 비밀번호와 SurrealDB 인증은 계속 필수다. SSO 재도입은 별도의 소유자 결정이다.
- provider 키는 앱의 암호화된 저장소에 보관하고 `open_notebook_encryption_key`는
  별도로 보호한다. 승인된 재암호화/내보내기 계획 없이는 절대로 회전하거나
  분실하지 않는다.
- 노트북, 소스 문서, 임베딩, 채팅, provider 설정을 민감 정보로 취급한다.
  사용 전에 보존과 내보내기 소유권을 정의한다.
- SurrealDB를 논리적으로 백업하고 `/app/data`, 소스 커밋, 보호된 키/자격 증명
  보관을 함께 백업한다. provider egress를 비활성화한 상태로 리허설한다.
- 추적 중인 이미지가 의도적으로 floating이므로 릴리스/보안 노트를 검토한다.
  승격 전에 마이그레이션과 자격 증명 복호화를 테스트한다.
- 제거 전에 콘텐츠/provider 자격 증명을 내보내거나 명시적으로 폐기한다.
  데이터베이스와 앱 볼륨 삭제는 별개의 파괴적 작업이다.
- 현재 기본 provider 경로는 local-only Ollama다. Ollama-mediated cloud와 direct
  cloud는 별도 credential, 허용 목적, network 및 비용 계약을 요구하며 자동 fallback
  이나 동일 instance의 `OLLAMA_NO_CLOUD=1` 예외로 도입하지 않는다.
- 저장된 모델 등록은 지원되는 product UI/API를 사용한다. 환경 fallback, healthcheck,
  DB online 또는 디렉터리 존재로 저장된 모델·provider·embedding 기능을 수용하지
  않는다. 다른 credential과 충돌하는 동명 등록은 보존하고 거부한다.

##### Exceptions

###### Exception Conditions
<!-- core-payload-level:4 -->

공유 SSO 제거는 소유자 커밋 `b90b74837`, 포괄 admin 선택 제거는 `d5912ab03`의
승인된 경계다. 변경 가능한 이미지 예외는 저장소의 image-tag 예외 원본에 따라
Laboratory Operator가 매월 검토하고 사용할 rollback 이미지 식별자를 보존한다.
책임자 `@buenhyden`의 별도 검토 없이 이 예외를 인증 생략·API 확대·v3 전환으로
확장하지 않는다. 암호화 키 손실은 DB 복원만으로 복구되지 않는다.

API를 광범위하게 노출하거나, 키를 소스에 저장하거나, 대응하는 암호화 키와
격리된 검증 없이 데이터를 복구하는 예외는 없다.

###### Approval and Review
<!-- core-payload-level:4 -->

릴리스, provider/모델, API 경로, DB 스키마, 키, 보존 정책 변경 시
검토한다.

#### Enforcement

##### Mechanisms

UI/앱 인증, API 경계, DB 준비 상태, 키 복호화, 하나의 합성 노트북을
검증하며, provider 접근은 별도로 승인된 경우에만 검증한다. 모델 기능은 저장된
연결, terminal embedding job, 입력/응답 및 재시작 후 보존을 별도로 검증한다.

##### Limits

정책은 검증 대상을 나열하지만 전용 검사 이름과 실행 증거를 지정하지 않으며 아래 항목은 수동 검토나 별도 승인에 의존한다.

- profile과 SurrealDB(POL-0073): R1-R2, R4은 수동 검토나 승인에 의존한다; R3에는 정책이 지정한 검사가 없다.
- 접근 통제(POL-0073): R8은 수동 검토나 승인에 의존한다; R5에는 정책이 지정한 검사가 없다.
- 키와 데이터 취급(POL-0073): R11은 수동 검토나 승인에 의존한다; R9-R10, R12-R13에는 정책이 지정한 검사가 없다.
- 백업과 복구(POL-0073): R14-R16에는 정책이 지정한 검사가 없다.
- 승격과 제거(POL-0073): R17은 수동 검토나 승인에 의존한다; R18-R20에는 정책이 지정한 검사가 없다.
- provider 경로(POL-0073): R21-R22은 수동 검토나 승인에 의존한다.
- 모델 등록(POL-0073): R25에는 정책이 지정한 검사가 없다.
- Mechanisms는 UI/앱 인증, API 경계, DB 준비, 키 복호화, 합성 노트북 검증을 요구하나 명령이나 스크립트를 지정하지 않는다.
- 백업/복구 리허설, 암호화 키 보호, 마이그레이션·자격 증명 복호화 테스트는 수행 기록 없이는 입증되지 않는다.
- provider 접근은 별도 승인된 경우에만 검증되며, 모델 기능(저장 연결, embedding job, 재시작 후 보존)은 별도 검증이 필요하다.

#### Ownership

##### Owner

책임 소유자는 frontmatter `owner`인 **@buenhyden**이다.

##### Review Triggers

- [가이드](../../01.guides/09.ai-and-search/0073-open-notebook.md) (`GDE-0073`)
- [런북](../../03.runbooks/09.ai-and-search/0073-open-notebook.md) (`RUN-0073`)

- [Open Notebook 보안](https://github.com/lfnovo/open-notebook/blob/main/docs/5-CONFIGURATION/security.md)
- [SurrealDB 백업 및 복구](https://surrealdb.com/docs/manage/self-hosted/backups-and-recovery)

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
