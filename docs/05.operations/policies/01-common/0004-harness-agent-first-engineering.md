---
title: "Harness / Agent-first Engineering Operations Policy"
version: "1.4.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0004"
parent_ids:
- "REQ-0024"
created: "2026-06-04"
next_review_at: "2027-05-13"
---

# Harness / Agent-first Engineering Operations Policy

## Purpose and Scope

### Objective

이 운영 정책은 `hy-home.docker`의 하네스 엔지니어링과 Agent-first Engineering 계약을 유지하기 위한 통제 기준을 정의한다.

canonical agent governance는 `.agents/`에 있다: governance policy가 규칙을 소유하고,
Provider Registry가 provider identity, model, permission translation을 소유하며,
role이 각자의 tier와 work profile을 소유한다. 이 문서는 운영 측면만 소유한다 —
하네스 실행·검증의 승인 경계와 실패 보고 기준이다. 실제 순서는 Runbook이 소유한다.

아래 표는 canonical 규칙의 소유자로 연결한다. 모델·permission·scope를 이 문서에
별도 값으로 복제하지 않는다.

#### Authority

- 과거 구현 출처: Harness and Agent-first Engineering Outcome (`SPEC-0094`)

### Applies To

이 정책은 다음 대상에 적용한다.

- Agent entry shim.
- Governance policy, role, skill, provider registry.
- Claude·Codex native adapter와 hook surface.
- Stage documentation과 validator.
- `AGENTS.md`, `CLAUDE.md`
- `.claude/**`
- `.codex/**`
- `.agents/**`
- `docs/03.specs/**`
- `docs/03.specs/[0-9][0-9][0-9][0-9]-*/plan.md`
- `docs/03.specs/[0-9][0-9][0-9][0-9]-*/tasks/tsk-[0-9][0-9][0-9][0-9]-*.md`
- `docs/05.operations/guides/*/[0-9][0-9][0-9][0-9]-*.md`
- `docs/05.operations/policies/*/[0-9][0-9][0-9][0-9]-*.md`
- `docs/05.operations/runbooks/*/[0-9][0-9][0-9][0-9]-*.md`
- `scripts/validation/check-*.sh`, `scripts/hardening/check-all-hardening.sh`, `scripts/validation/validate-docker-compose.sh`

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0004-R1 | Root 파일 | 필수: 상세 policy를 `.agents/`와 runtime overlay에 위임한다 | none | none |
| POL-0004-R2 | Native role adapter와 thin Claude skill pointer | 필수: authored `.agents` source와 동기화 상태를 유지한다 | none | none |
| POL-0004-R3 | canonical 파일 | 금지: renderer output으로 만든다 | none | none |
| POL-0004-R4 | 모델 선택 | 필수: role의 `work_profile`과 Provider Registry의 provider mapping을 따른다 | none | none |
| POL-0004-R5 | 항상 | 금지: 현재 모델/계층/개수를 이 문서에서 별도로 선언한다 | none | none |
| POL-0004-R6 | 각 runtime agent | 필수: 정확히 하나의 primary scope를 import한다 | none | none |
| POL-0004-R7 | Runtime hook | 필수: shell command substitution 부작용 없이 실제 payload shape를 파싱한다 | none | none |
| POL-0004-R8 | Codex surface | 필수: Provider Registry가 native agent pattern을 선언하고 renderer가 role당 하나의 adapter를 hook configuration 옆에 작성한다 | none | none |
| POL-0004-R9 | Codex surface 내용 결정 | 필수: 이 문서가 아니라 registry가 결정한다 | none | none |
| POL-0004-R10 | 새 stage 문서 | 필수: `docs/99.templates/`를 사용한다 | none | none |
| POL-0004-R11 | 새 stage 문서 | 필수: parent README 파일을 갱신한다 | none | none |
| POL-0004-R12 | Active runtime/governance 파일 | 금지: 외부 harness source label 참조 | none | none |
| POL-0004-R13 | Graphify 사용 시 | 필수: health가 clean할 때만 navigation aid로 쓴다 | none | none |
| POL-0004-R14 | contaminated output | 필수: advisory로 두고 tracked source 및 canonical 문서와 대조 검증한다 | none | `status=advisory` 보고 |
| POL-0004-R15 | 적용 gate 실행 시 | 필수: 현재 선택 범위를 기록한다 | none | none |
| POL-0004-R16 | 범위 밖 remediation | 필수: 별도 승인을 받는다 | 수동 | none |
| POL-0004-R17 | AI Agent 한도 | 필수: [Agentic Engineering Policy](../../../../.agents/governance/agentic.md#execution-rules)(Graphify는 [Environment Constraints](../../../../.agents/governance/environment-constraints.md#4-graphify))를 따른다 | none | none |
| POL-0004-R18 | native 호출/복구 결과 기록 시 | 금지: 정적 source나 수동 비교를 native 호출/복구 성공으로 기록한다 | none | none |
| POL-0004-R19 | Docker/실제 환경 접근 | 필수: 해당 Task의 승인 범위에서 실행한다 | none | none |
| POL-0004-R20 | 미실행 항목 | 금지: 미실행을 성공으로 취급한다 | none | none |

| 통제 | 요구사항 |
| --- | --- |
| Thin root shims | Root 파일은 상세 policy를 `.agents/`와 runtime overlay에 위임한다. |
| Runtime mirror parity | Native role adapter와 thin Claude skill pointer는 authored `.agents` source와 동기화 상태를 유지한다; canonical 파일은 renderer output이 되지 않는다. |
| Runtime parity scope | Repository check는 catalog, model, scope import, protocol-reference parity를 증명한다; 모든 runtime 문서의 semantic parity를 증명하지는 않는다. |
| Model selection | role의 `work_profile`과 Provider Registry의 provider mapping을 따른다. 현재 모델·계층·개수를 별도로 선언하지 않는다. |
| Scope imports | 각 runtime agent는 정확히 하나의 primary scope를 import한다. |
| Hook safety | Runtime hook은 shell command substitution 부작용 없이 실제 payload shape를 파싱해야 한다. |
| Codex boundary | Governance는 Codex catalog를 채택했다: Provider Registry가 native agent pattern을 선언하고 renderer가 role당 하나의 adapter를 hook configuration 옆에 작성한다. Codex surface가 무엇을 담는지는 이 문서가 아니라 registry가 결정한다. |
| Template-first docs | 새 stage 문서는 `docs/99.templates/`를 사용하고 parent README 파일을 갱신한다. |
| Source-label prevention | Active runtime/governance 파일은 외부 harness source label을 참조하지 않아야 한다. |
| Graph context health | Graphify는 health가 clean할 때만 navigation aid가 된다; contaminated output은 advisory로 남으며 tracked source 및 canonical 문서와 대조 검증해야 한다. |
| Infra validation scope | 적용 gate의 현재 선택 범위를 기록한다. Compose validator와 baseline script의 기본 범위가 다르며 범위 밖 remediation은 별도 승인한다. |
| AI Agent limits | [Agentic Engineering Policy](../../../../.agents/governance/agentic.md#execution-rules)가 소유하며, Graphify의 경우 [Environment Constraints](../../../../.agents/governance/environment-constraints.md#4-graphify)가 소유한다. |

자동 답변 점수 QA와 완료 사건의 전용 증명은 현재 delivery gate가 아니다.
현재 문서·Docker 계약과 이를 지원하는 회귀의 허용 범위, 폐기 순서, 단계별 실행은
[quality policy](../../../../.agents/governance/quality-standards.md)가 소유한다.
정적 source나 수동 비교를 native 호출·복구 성공으로 기록하지 않는다.
Docker·실제 환경 접근은 해당 Task의 승인 범위에서 실행하며 미실행은 성공이 아니다.

### Exceptions

#### Exception Conditions

- 과거 Stage 90 또는 Stage 98 evidence는 명확히 non-authoritative일 때 이전 source label을 언급할 수 있다.
- `bash scripts/knowledge/report-graphify-health.sh`는 `status=advisory`를 보고할 수 있다; 이는 repository validation 실패가 아니라 신뢰도 하향 evidence다.
- CLI를 사용할 수 없을 때 `graphify` refresh를 건너뛸 수 있지만 건너뛴 사실은 보고해야 한다.
- `rtk`는 active shell에서 사용할 수 없을 때 우회할 수 있다.
- 승인되지 않은 Compose/include/IP remediation은 이 하네스 점검의 실행 범위가 아니다.

#### Approval and Review

- 현재 owner나 계약이 바뀌면 영향받는 소비자와 필요한 회귀를 검토한다.
- 완료 여부는 현재 Task의 실제 필수 증거와 독립 검토로 판정하며 같은 입력의 aggregate QA를 반복하지 않는다.
- `.claude`, `.codex`, 또는 canonical agent governance role/skill catalog가 바뀌면 이 policy를 검토한다.
- scope 밖 infra profile 실패는 HAFE acceptance criteria를 조용히 확장하는 대신 별도로 기록한다.

## Enforcement

### Mechanisms

변경 영향에 맞춰 quality policy와 canonical public plan이 선택한 검사만 수행한다.
[Runbook](../../runbooks/01-common/0004-harness-agent-first-engineering.md#steps)은 승인된
관측의 실행 경로를 안내하며 모든 변경에 전체 hook/runtime bundle을 요구하지 않는다.

### Limits

이 정책은 아래 규칙에 대해 명명된 자동 검사를 연결하지 않거나 수동 검토에 맡긴다.

- Root shim/미러: 명명된 검사 없음 R1~R3 (`POL-0004-` 접두)
- 모델/scope: 명명된 검사 없음 R4~R6 (`POL-0004-` 접두)
- Hook/Codex: 명명된 검사 없음 R7~R9 (`POL-0004-` 접두)
- 문서/source label: 명명된 검사 없음 R10~R12 (`POL-0004-` 접두)
- Graphify/gate 범위: 명명된 검사 없음 R13~R15, R17; 수동 검토 R16 (`POL-0004-` 접두)
- 증거 기록: 명명된 검사 없음 R18~R20 (`POL-0004-` 접두)
- repository check는 catalog/model/scope import/protocol-reference parity만 증명하며 모든 runtime 문서의 semantic parity는 증명하지 않는다(83행).
- 자동 답변 점수 QA와 완료 사건의 전용 증명은 현재 delivery gate가 아니다(94행).
- `bash scripts/knowledge/report-graphify-health.sh`의 `status=advisory`는 신뢰도 하향 evidence이며 repository validation 실패가 아니다(105행).

## Ownership

### Owner

정책 소유자는 @buenhyden이다.

### Review Triggers

- 같은 주제: [Guide](../../guides/01-common/0004-harness-agent-first-engineering.md) (`GDE-0004`), [Runbook](../../runbooks/01-common/0004-harness-agent-first-engineering.md) (`RUN-0004`)

- [Operations index](../../README.md)
