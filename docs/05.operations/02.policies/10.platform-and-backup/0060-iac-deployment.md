---
title: "IaC Deployment Policy"
version: "2.0.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "operations"
artifact_id: "POL-0060"
parent_ids:
- "AD-0009"
created: "2026-03-25"
next_review_at: "2027-05-13"
---

# IaC Deployment Policy

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

이 정책은 `09-platform-ops`의 OpenTofu CLI helper와 Terrakube API/UI/executor를 이용한 IaC 변경의 승인, state, secret, evidence 기준을 정의한다.

###### Authority
<!-- core-payload-level:4 -->

- 상위 문서: [Platform Operations·Quality 아키텍처](../../../02.architecture/01.descriptions/0009-tooling-architecture.md) (`AD-0009`)

- 실행 버전의 원본은 Compose/Dockerfile 선언이며, [파생 버전 목록](../../../../infra/tech-stack.versions.json)은 변경 누락 검증에 사용한다.

##### Applies To

- **Systems**: `infra/09-platform-ops/opentofu/docker-compose.yml`, `infra/09-platform-ops/terrakube/docker-compose.yml`
- **Environments**: 단일 HOME/DEV 호스트의 `iac` profile(온디맨드 DEV)

Terraform Compose runtime은 제거되었다. 기존 workspace 이관은 [Terraform 이관](../../01.guides/10.platform-and-backup/0082-opentofu.md#terraform-이관)을 따른다.

###### Exclusions
<!-- core-payload-level:4 -->

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0060-R1 | IaC 변경 시 | 필수: PR review, plan evidence, apply approval, state backend boundary 기록을 거친다 | 수동 | none |
| POL-0060-R2 | 항상 | 필수: OpenTofu helper는 `$HOME/.aws`, `$HOME/.azure` read-only mount와 `workspace/` scope 안에 머문다 | 수동 | none |
| POL-0060-R3 | 항상 | 필수: Terrakube secret material은 Docker Secret names만 문서화한다 | 수동 | none |
| POL-0060-R4 | 항상 | 금지: Terrakube secret 값 노출 | 수동 | none |
| POL-0060-R5 | 항상 | 허용: 문서/검증 절차의 in-place 보강, state/backend 정책의 보수적 강화, approval gate 추가 | none | none |
| POL-0060-R6 | 항상 | 금지: 승인 없는 apply | 수동 | none |
| POL-0060-R7 | 항상 | 금지: Docker socket 권한 확대 | none | none |
| POL-0060-R8 | 항상 | 금지: 정책과 절차의 중복 SSoT 생성 | 수동 | none |
| POL-0060-R9 | Terrakube 실행 경로 제한이 해소되기 전 | 금지: 브라우저 로그인이나 정적 검증으로 IaC 실행이 가능하다고 승인 | none | none |

- **Required**: IaC 변경은 PR review, plan evidence, apply approval, state backend boundary 기록을 거친다.
- **Required**: OpenTofu helper는 `$HOME/.aws`, `$HOME/.azure` read-only mount와 `workspace/` scope를 벗어나지 않는다.
- **Required**: Terrakube secret material은 Docker Secret names만 문서화하고 값은 노출하지 않는다.
- **Allowed**: 문서/검증 절차의 in-place 보강, state/backend 정책의 보수적 강화, approval gate 추가.
- **Disallowed**: secret 값 노출, 승인 없는 apply, Docker socket 권한 확대, 정책과 절차의 중복 SSoT 생성.

###### 책임과 구현 제한
<!-- core-payload-level:4 -->

승인·예외 및 복구 판단 책임자는 `@buenhyden`이다. Terrakube executor의 Docker
socket 권한과 외부 도구 선택은 OpenTofu의 읽기 전용 cloud credential mount와
다르다. [Terrakube 정책](0069-terrakube.md)의 실행 경로 제한을 해소하기 전에는
브라우저 로그인이나 정적 검증으로 IaC 실행이 가능하다고 승인하지 않는다.

##### Exceptions

###### Exception Conditions
<!-- core-payload-level:4 -->

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

###### Approval and Review
<!-- core-payload-level:4 -->

- 서비스 구성 변경 시 검토
- 문서 템플릿 변경 시 검토
- 주요 운영 정책 변경 시 검토

#### Enforcement

##### Mechanisms

- `bash scripts/hardening/check-all-hardening.sh 09-platform-ops`
- 원격 PR public `changed` 검사 ([quality policy](../../../00.workspace/04.quality/quality-standards.md#canonical-delivery-phase-matrix))
- OpenTofu/Terrakube guide/runbook과 compose service names가 일치하는지 검토한다.

##### Limits

아래 규칙은 지정된 검사 없이 승인과 수동 검토에 의존한다.

- 변경 절차: 수동 검토/승인에 의존: `POL-0060-R1`, `POL-0060-R6` / 지정된 검사 없음: `POL-0060-R9`
- 마운트와 secret: 수동 검토/승인에 의존: `POL-0060-R2`, `POL-0060-R3`, `POL-0060-R4`, `POL-0060-R8` / 지정된 검사 없음: `POL-0060-R7`
- 허용 작업: 지정된 검사 없음: `POL-0060-R5`
- 정책이 지정한 hardening 검사와 원격 PR `changed` 검사를 특정 규칙에 연결하는 문장은 없다.
- guide/runbook과 compose service names 일치는 검토로만 확인한다.

#### Ownership

##### Owner

책임 소유자는 frontmatter `owner`인 **@buenhyden**이다.

##### Review Triggers

- 동일 주제 문서: 없음 — `0060`은 독립 정책이며 같은 번호의 Guide/Runbook은 없다.

- [Operations index](../../README.md)
- [OpenTofu guide](../../01.guides/10.platform-and-backup/0082-opentofu.md)
- [Terrakube guide](../../01.guides/10.platform-and-backup/0069-terrakube.md)
- [OpenTofu runbook](../../03.runbooks/10.platform-and-backup/0082-opentofu.md)
- [Terrakube runbook](../../03.runbooks/10.platform-and-backup/0069-terrakube.md)

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
