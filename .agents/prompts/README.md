---
title: "Agent Prompts"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: Agent Prompts
  layer: agent
updated: "2026-11-20"
created: "2026-09-06"
---

# Agent Prompts

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

#### Responsibility

##### Purpose

###### Purpose and Readers
<!-- core-payload-level:4 -->

`.agents/prompts/`는 반복되는 agent 작업을 위한 재사용 가능한 prompt
contract를 보관합니다. prompt는 무엇이 필요한지, 무엇을 산출해야 하는지,
무엇을 해서는 안 되는지, 진행할 수 없을 때 무엇을 해야 하는지를 선언합니다.
작업 자체가 아니라 작업을 감싸는 envelope입니다.

두 provider 모두 같은 canonical path에서 이 파일을 읽으므로, prompt는
session 경계와 provider 전환을 넘어 유지됩니다.

###### Inputs and Outputs
<!-- core-payload-level:4 -->

- 포함: 목적, 필수 input, output contract, prohibition, failure handling,
  적용 가능한 role, skill, 평가 기준.

prompt를 읽는 것은 어떤 role도 선택하지 않으며 어떤 permission도 부여하지
않습니다. 이미 선택된 role의 permission profile과 승인된 Task scope가 계속
적용됩니다.

##### Excluded Responsibilities

- 제외: `skills/`에 속하는 순서화된 절차 단계, `governance/`에 속하는
  obligation, 현재 Spec Package Task에 속하는 실행 상태와 결과.

#### Current Contents

##### Paths

###### Current Items
<!-- core-payload-level:4 -->

```text
.agents/prompts/
├── README.md
├── commit-message.md
├── diff-review.md
├── handoff.md
└── test-design.md
```

| Path | Purpose |
| --- | --- |
| [handoff.md](handoff.md) | Next-session handoff contract |
| [diff-review.md](diff-review.md) | Independent diff-review contract |
| [commit-message.md](commit-message.md) | Staged-diff commit-message contract |
| [test-design.md](test-design.md) | Requirement-driven test-design contract |

Prompt slug는 skill id와 구분되게 유지되어 하나의 이름이 두 가지 다른
것으로 resolve되지 않습니다.

###### Classification
<!-- core-payload-level:4 -->

prompt는 작업 자체가 아니라 작업을 감싸는 envelope입니다. `skills/`의 절차 단계와 `governance/`의 obligation을 대체하지 않으며, 네 prompt는 모두 같은 형식의 재사용 계약입니다.

##### Owners

이 README의 소유자는 frontmatter `owner`의 `@buenhyden`입니다. 목록에 있는 각 항목의 소유자는 이 README가 따로 기록하지 않습니다.

#### Usage

##### Entry Points

###### Upstream and Downstream
<!-- core-payload-level:4 -->

- [Knowledge index](../knowledge/README.md)
- Canonical knowledge and prompt surfaces decision (`docs/00.workspace/02.architecture/02.decisions/0034-canonical-knowledge-and-prompt-surfaces.md`)
- [Documentation index](../../docs/README.md)

###### Policy and Templates
<!-- core-payload-level:4 -->

- [Agent governance index](../README.md)
- [Agentic policy](../governance/agentic.md)
- [문서 작성 계약](../../docs/00.workspace/03.process/documentation-protocol.md#readme-and-agentsmd): README와 AGENTS.md의 역할 구분
- README 템플릿 `docs/99.templates/02.templates/91.agent-governance/prompt-index.template.md`: 이 README의 양식 원본이며 형식은 Stage 99 Registry의 profile이 소유합니다.

##### Checks

###### Create and Review
<!-- core-payload-level:4 -->

1. 필요한 것이 절차가 아니라 input/output contract인지 확인합니다. 절차는
   skill에 속합니다.
2. `docs/99.templates/02.templates/91.agent-governance/prompt.template.md`를 복사하고
   등록된 섹션을 순서대로 유지합니다.
3. 소유 skill과 role의 이름을 명시하고 둘 중 하나를 다시 서술하지
   않습니다.
4. prohibition을 구체적인 거부로 작성하여 독자가 특정 output이 그것을
   위반하는지 판단할 수 있게 합니다.
5. Provider Registry의 `canonical_sources`에 파일을 등록한 뒤 document
   metadata와 agent governance contract 점검을 실행합니다.

###### Applying a Prompt
<!-- core-payload-level:4 -->

prompt를 불러오고 모든 필수 input을 제공하며 선언된 output을 정확히
산출합니다. input을 사용할 수 없다면 근사치로 대체하지 말고 prompt의
failure handling을 따릅니다. prompt가 어디에 적용되었는지는 현재 Task에
기록합니다. prompt 자체는 아무것도 기록하지 않습니다.

###### Transition and Exit
<!-- core-payload-level:4 -->

이 README는 `navigation` 수명주기의 `active` 상태만 가지며 다른 상태로 전이하지 않습니다. 목록 항목을 추가·이동·삭제할 때 이 문서를 함께 갱신하고, 삭제한 항목의 이력은 Git이 기록합니다.

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
