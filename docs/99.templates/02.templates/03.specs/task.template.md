---
title: '{{TITLE}}'
version: 0.1.0
type: sdlc/task
status: draft
owner: '{{OWNER}}'
document_scope:
  subject: '{{DOCUMENT_SUBJECT}}'
  layer: workspace
document_lifecycle: draft
updated: '{{UPDATED}}'
layer: specs
artifact_id: '{{ARTIFACT_ID}}'
parent_ids:
- '{{PARENT_ID}}'
created: '{{CREATED}}'
---

# {{TITLE}}

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: 이 문서로 해결할 정보 필요와 실제 독자를 밝힌다. 본문 정책을 중복 복사하지 않는다. -->

Readers use the task payload below for this document's information and judgments.

### 책임과 적용 범위

<!-- 작성 규칙: 유지할 대상·적용과 제외 범위·책임자를 밝힌다. 메타데이터 자체가 실행 승인이나 인수 권한을 부여하지 않는다. -->

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: 실제로 존재하거나 명시적으로 생성할 입력, 제약, 전제를 구분한다. 확인한 사실과 가정을 혼동하지 않는다. -->

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

<!-- 작성 규칙: 해당 kind의 payload와 조건·표·필드 의미를 소유한다. 관련 없는 문서 역할과 Release 책임을 모든 문서에 복제하지 않는다. -->

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->
<!-- Author prompt: Write body prose in English; keep headings, paths, identifiers, and commands unchanged. -->
<!-- Author prompt: Before setting status to cancelled, supply cancellation frontmatter with a nonempty reason, an actual authorization_ref, and criteria_disposition entries containing an integer criterion plus exactly one successor Task identity or approved withdrawal_ref. A successor is another non-cancelled Task in the same package. authorization_ref and withdrawal_ref use unambiguous same-Task heading anchors to actual structural evidence; those records do not authenticate or grant approval. An empty criteria_disposition list states that this Task held no criterion; it does not close any Spec criterion. Never seed or infer cancellation approval. -->
<!-- Author prompt: Keep the Evidence header, separator, and every data row in one contiguous pipe-table block. Narrative may appear before or after that block; put other pipe tables outside the Results subsection. -->
<!-- Author prompt: Evidence records observations only. Evidence ID names the row uniquely. Method is automated, review or observation. Input names the revision or candidate examined; Tool and Config the tool, version and configuration, or `-`. Command is the command run or the observation method, or `-`; Exit is the command's exit code, or `-` when nothing ran, never 0 for a check that did not run. Result is PASS, FAIL, ERROR, NOT_RUN, CANCELLED or NOT_APPLICABLE. Required is true or false and is not an approval; every required non-PASS observation remains open until an equivalent PASS explicitly resolves it. In Resolves, write `-` or the IDs of earlier non-PASS rows with the same Command and Work Unit in this Task that this PASS row resolves for a shared criterion. A checker's own regression test and a document or contract check are different Commands. -->
<!-- Author prompt: The Criterion Decisions table holds one row for each Spec criterion this Task owns. A criterion the Plan assigns to a current, non-cancelled Task has exactly one row, in one such Task; a criterion whose assigned Tasks are all historical or cancelled has none. Intent is accept, reject, not-required or undecided. Acceptance is pending, accepted, rejected or not-required; accepted needs a PASS for every criterion/Work Unit pair the Plan assigns to a current, non-cancelled Task, cites at least one PASS row for that criterion, cites a non-PASS row only when a later row resolves it, and leaves no unresolved required observation; not-required and rejected need a Decision. Accepted By names who actually judged, or `-`; the name does not authenticate anyone. Current Owner names the durable owner or a reasoned N/A disposition, and Reassigned To the permitted new owner of the obligation, or `-`. The Evidence cell is `-` or Evidence IDs of this Task. Put no other pipe table in the Criterion Decisions subsection. -->

#### Scope

##### Objective and Parent

{{OBJECTIVE_AND_PARENT_PLAN_AND_WORK_UNITS}}

##### Inputs and Authority

<!-- Author prompt: Name the Spec criteria, Plan work units, request identity and revision supplied by the trusted origin or unknown, authorization source, exact scope and current applicability. Record a changed, expired or withdrawn binding before resuming affected work. Naming an authorization here only records it. -->

{{INPUTS_AND_AUTHORITY}}

#### Execution Log

##### Work Performed

<!-- Author prompt: Record what was done in order, with the commits or artifacts it produced. Keep each `#### Execution Items`, `#### Lifecycle Events`, `#### Lifecycle Event Reconciliation` and `#### Contract Migration` table under Work Performed as its own `####` heading, and anything a reader links to as a heading of that level or deeper. A section with nothing to record says why in one sentence instead of staying empty. -->

{{WORK_PERFORMED}}

###### Execution Items
<!-- core-payload-level:4 -->

<!-- Author prompt: Keep this table only for several independently tracked items, with at least two rows, and then remove the frontmatter `status`; each row owns its status, each Work Unit belongs to one item, and a blocked or cancelled item names its Blocker. A Task with one status removes this heading and table. -->

| Item | Work Unit | Owner | Status | Blocker |
| --- | --- | --- | --- | --- |
| {{ITEM}} | {{ITEM_WORK_UNIT}} | {{ITEM_OWNER}} | {{ITEM_STATUS}} | {{BLOCKER}} |

###### Lifecycle Events
<!-- core-payload-level:4 -->

<!-- Author prompt: Record every frontmatter `status` change as one row, in order from the initial `draft` (`draft` to `ready` to `in-progress`, then `completed`, `blocked` or `cancelled`); the metadata gate refuses a status that no row reaches. Each Evidence cell is one unique heading anchor of this Task that shows why the step happened. `completed` also needs PASS evidence and an accepted decision for every assigned criterion. A Task still in `draft` removes this heading and table. -->

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| {{ARTIFACT_ID}} | {{FROM_STATUS}} | {{TO_STATUS}} | {{EVIDENCE_ANCHOR}} |

##### Blockers and Decisions

{{BLOCKERS_DEFERRALS_AND_RULINGS}}

#### Verification Evidence

##### Results

| Evidence ID | Criteria | Work Unit | Method | Input | Tool and Config | Command | Exit | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| {{EVIDENCE_ID}} | {{CRITERIA}} | {{WORK_UNIT}} | {{METHOD}} | {{INPUT}} | {{TOOL_AND_CONFIG}} | {{COMMAND}} | {{EXIT}} | {{RESULT}} | {{LOCATION}} | {{REQUIRED}} | {{RESOLVES}} |

##### Resolution Links

{{LINKS_FROM_FAILED_OBSERVATIONS_TO_THEIR_RESOLUTION}}

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Intent | Acceptance | Evidence | Decision | Accepted By | Current Owner | Reassigned To |
| --- | --- | --- | --- | --- | --- | --- | --- |
| {{CRITERION}} | {{INTENT}} | {{ACCEPTANCE}} | {{ACCEPTANCE_EVIDENCE}} | {{DECISION}} | {{ACCEPTED_BY}} | {{CURRENT_OWNER}} | {{REASSIGNED_TO}} |

##### Remaining Conditions

{{REMAINING_CONDITIONS_AND_DEFERRED_ITEMS}}

#### Handoff

##### Promotion Receipt

<!-- Author prompt: For each acceptance criterion, name the Plan work unit, the Task result, the durable document and the commit that changed it, the consumer update and check that show it, the criterion's Criterion Decisions row and any residual with its owner, or why no durable update is needed. -->

{{PROMOTION_TARGET_AND_RECEIPT}}

##### Next Owner

{{NEXT_OWNER_AND_RESUME_CONDITIONS}}

## 적용과 확인

### 적용 방법

<!-- 작성 규칙: 실제 독자가 문서 또는 연결된 native 출력을 사용하는 방법을 설명한다. 필요 없는 운영·승인 단계를 만들지 않는다. -->

Use the procedures or reading order stated in the role payload.

### 확인 기준

<!-- 작성 규칙: 문서 목적에 필요한 확인만 제시한다. 설계·구현·검증·사용자 인수를 구별하고 모든 문서에 코드 시험을 강요하지 않는다. -->

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

<!-- 작성 규칙: 정본 owner와 필요한 의존 관계의 목적을 적는다. 모든 문서의 양방향 링크나 과거 별칭을 강제하지 않는다. -->

The role payload retains the current owner and dependency references.

### 외부 근거

<!-- 작성 규칙: 외부 사실과 현재 설계의 적용·제외 이유를 구분한다. 출처가 실행 권한이나 성공 증거를 대신하지 않는다. -->

External basis and its limits remain those stated in the role payload; a citation grants no authority.
