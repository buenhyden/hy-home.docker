---
title: "Stage 99 Document Contracts and Templates"
version: "2.5.4"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "templates"
---

# Stage 99 Document Contracts and Templates

## Stage Responsibility

### Purpose and Readers

Stage 99는 문서 경로, profile, identifier, section, lifecycle 상태와 전이,
traceability 형태, 복사용 template의 유일한 권위입니다. machine authority는
[`registry.json`](./registry.json)이며, `contracts/` 아래 두 schema가
registry와 문서 frontmatter를 검증합니다. 사람과 AI agent를 위한 정책은
공통 Agent 거버넌스에 남고, 실행 가능한 gate 동작은 등록된 `scripts/`
모듈에 남습니다.

이전 계약은 Git history로 복구할 수 있으나, 현재 작성이나 검증 입력이
아닙니다.

### Inputs and Outputs

Stage 99가 소유하는 것:

- the Requirement Package and Architecture Description profiles;
- the Guide, Policy, Runbook, Incident, and Postmortem profiles;
- the Research, Audit, Data publication roles;
- canonical path와 안정 ID 패턴;
- profile별 frontmatter와 section 계약;
- lifecycle 상태와 허용된 직접 transition;
- Requirement child space를 포함한 단조 증가 identity 발급 상태;
- template 역할-profile 등록;
- 재사용 가능한 Markdown과 실행 가능한 interface-contract template;
- 정확한 Stage 03 package-index와 contract-payload 파일명 및 media type;
- 네 자리 Operations subject route 형태.

Stage 99는 agent 행동, 제품 사실, 아키텍처 결정, 구현 증거, 운영 정책,
reference finding을 소유하지 않습니다.

## Contents

### Current Items

| Path | Purpose |
| --- | --- |
| [registry.json](registry.json) | 문서 profile과 lifecycle machine 권위 |
| [contracts/](contracts/) | Registry와 frontmatter 값 schema |
| [templates/](templates/) | 등록된 복사용 작성 source |

```text
docs/99.templates/
├── README.md
├── registry.json
├── contracts/
│   ├── document-frontmatter.schema.json
│   └── document-profile.schema.json
└── templates/
    ├── governance/
    ├── runtime/
    ├── requirements/
    ├── architecture/
    ├── specs/
    │   └── contracts/
    ├── operations/
    ├── references/
    └── common/
```

### Classification

#### Authority Model

| Surface | Authority | Purpose |
| :--- | :--- | :--- |
| [`registry.json`](./registry.json) | machine | profiles, paths, identities, lifecycle, traceability, template registration |
| [`contracts/document-profile.schema.json`](./contracts/document-profile.schema.json) | machine | registry shape |
| [`contracts/document-frontmatter.schema.json`](./contracts/document-frontmatter.schema.json) | machine | typed frontmatter value shape |
| [`templates/`](./templates/) | copy source | profile-referenced authoring forms |

Consumer는 `scripts.lib.document_governance.registry`를 통해 Registry를
로드해야 합니다. README 본문이나 template 본문을 machine policy로
재해석해서는 안 됩니다.

모든 profile은 하나의 `frontmatter_policy`를 선언합니다. `required`는
canonical Markdown artifact의 `type`이 해당 Registry-classified profile type과
같아야 함을 뜻하며 전용 복사 template이 없는 package,
domain, subject, stage, governance, generated, repository-support
Markdown에도 적용됩니다. `absent`는 Markdown frontmatter를 쓰지 않는
실행 가능한 machine contract 전용입니다. `unmanaged`는 지원되지 않는
fallback을 뜻하며 현재 작성 대상이 아닙니다. Stage 01~03 lifecycle은
`deprecated`, `superseded`, `retired`, `archived` 상태를 두지 않습니다.
대체되거나 철회된 문서는 현재 owner에 요약한 뒤 삭제하고 번호를 예약합니다.

#### Common Role Forms

공통 역할 16개를 공통 절 계약 `COMMON-DOC-FORM-1` 1.0.0으로 옮기는 규칙은
[문서 프로토콜](../../.agents/governance/documentation-protocol.md#role-specific-authoring)이
정한다. 옮기는 단위, 구 양식과 빈 절의 거부, 아직 옮기지 않은 역할의 양식,
예외 조건이 모두 그곳에 있다. 역할별 절 이름은 Registry가 선언하며, 진행
상황은 SPEC-0212 TSK-0059가 기록한다. 이 표기는 네 저장소 공동 채택을 뜻하지
않는다.

## Workflow

### Create and Review

1. 등록된 profile과 template 역할을 선택합니다.
2. 선언된 `type` 계약을 바꾸지 않고 등록된 source를 복사합니다.
3. 저장된 high-water mark보다 높은 ID를 발급합니다.
4. placeholder를 바꾸고 전체 traceability ID를 추가합니다.
5. 문서 계약 validator와 owning stage gate를 실행합니다.
6. 계약 자체가 바뀔 때는 Registry, schema, template, consumer, test를 하나의
   검토된 논리적 단위에서 함께 바꿉니다.

#### Template Rules

- `template_id`/template 역할이 등록한 source를 복사합니다.
- Markdown template frontmatter는 profile의 `type`을 선언하며 구체적인
  대상 경로를 담지 않습니다.
- Markdown placeholder는 `{{UPPER_SNAKE_CASE}}`를 사용합니다. template
  전용 작성 안내는 HTML comment로 나타날 수 있으나 승격 후까지 남아서는
  안 됩니다. native machine contract template은 대신 `__UPPER_SNAKE__`
  token을 사용합니다.
- 공유되는 stage README 형태는 의도적인 destination-bound 예외입니다:
  그 `layer` placeholder는 정확한 Registry `frontmatter_routes` 항목에서
  해석됩니다. 여러 stage가 공유하는 source는 하나의 stage 리터럴을 쓸 수
  없으며, 대상 문서는 등록된 리터럴을 사용해야 하고 stage를 임의로 만들
  수 없습니다.
- 대상 문서로 승격하기 전에 모든 placeholder를 바꿉니다.
- 실행 가능한 OpenAPI, GraphQL, Proto 계약은 이를 소유하는 Stage 03 Spec
  package에 속합니다. 그 결정적 파일명과 media type은 Registry profile이며,
  Stage 01은 구현과 무관한 interface 필요를 유지합니다.
- `DESIGN.md`는 root UI/design-system 권위로 남으며 Stage 03 design
  artifact가 아닙니다.

### Transition and Exit

#### Identity and Lifecycle Rules

##### Stage 03 Evidence

Task 상태는 frontmatter 하나에 둡니다. 여러 항목을 따로 추적하는 Task는
Execution Log의 Work Performed 아래 `Execution Items` 표의 각 행이 상태를
가지며 frontmatter `status`를 쓰지 않습니다. `Evidence`의 각 행은 기존 criterion과 Plan work
unit, 실제 check와 input, result, location, 그리고 같은 Task에서 criterion을
공유하고 Check·Work Unit이 같은 앞선 non-PASS 관측을 해소하는 `Resolves`를
기록합니다. 수용 판정은 criterion마다 한 번, Task의
`Criterion Acceptance` 표에 둡니다. Plan의 `Work Breakdown`은 여섯 열이고
새 Task의 `Evidence`는 필수성을 포함한 아홉 열이고 수용 표에는 현재 owner를
기록합니다. 이전 판본의 보존 기록은 당시 표로 읽습니다. 정확한 열 순서와 vocabulary는 Registry가
소유합니다. Registry `common`의 절 이름 값(`plan_section` 등)은 이전 H2 이름을
가리키는 논리 이름입니다. 공통 양식으로 옮긴 문서에서는 같은 절이 새 H2 아래
H3로 있으며(예: `Implementation Strategy` 아래 `Work Breakdown`), 검사기는 두
형식 중 정확히 하나만 받아들입니다. Task에서는 `Evidence`가 `Verification
Evidence` 아래 `Results`, `Criterion Acceptance`가 `Acceptance Decision` 아래
`Criterion Decisions`, `Work Log`가 `Execution Log` 아래 `Work Performed`를
가리킵니다.
Lifecycle Events는 실제 직접 전이와 같은 Task의 evidence anchor만 기록하며
승인 source를 인증하지 않습니다. 승인·검토·실행의 의미는
[SDLC](../../.agents/governance/sdlc.md)가 소유합니다.

##### Registered Identity Shapes

`registry.json`은 profile별 identity 형태를 `artifact_id_pattern`에,
소유 container를 `identity_relation`에 명시합니다. 이 절은 그 필드들이
표현하는 규칙을 설명할 뿐, 필드 자체를 다시 정의하지 않습니다.

##### Required Frontmatter Envelope

profile의 `required_frontmatter`와 `optional_frontmatter`는 문서가
선언해야 하는 key를, `common.frontmatter_order`는 순서를,
`frontmatter_values`는 profile별 literal 제약을,
[`contracts/document-frontmatter.schema.json`](./contracts/document-frontmatter.schema.json)은
각 값의 형태를 명시합니다. 작성 행동, 콘텐츠 버전, envelope의 의미는
공통 Agent 거버넌스
[문서화 정책](../../.agents/governance/documentation-protocol.md#authoring-rules)이
소유합니다.

Canonical skill은 최상위에 정확히 `name`, `description`, `metadata`만 갖는
`.agents/skills/{slug}/SKILL.md`를 사용합니다. 등록된
`native-skill-envelope` 예외는 중첩된 metadata를 일반 governance skill
profile과 공통 값 schema를 통해 투영합니다. 이름, 폴더, `function_id`는
서로 일치해야 합니다. 이 직렬화 계약은 runtime 권한을 부여하지 않습니다.
다른 작성 문서는 공통 frontmatter envelope를 유지합니다.

`parent_ids`는 Registry가 선언한 구조적 관계를 담습니다. Plan은 정확히 하나의
Spec parent를, Task는 정확히 하나의 Plan parent를 둡니다. 더 넓은 증거와
consumer 관계는 `Traceability`나 `Related Documents`에 둡니다. 소유권은
`.github/CODEOWNERS` 또는 해당 canonical role에서 옵니다. 짧은 Registry
profile `id`는 하나의 고유한 `type`에 명시적으로 매핑되며, 추가 작성용
분류자가 아닙니다.

- 독립 package 경로는 네 자리 숫자를 쓰고 의미 접두사를 생략합니다.
- 구성원 identity는 자신을 담는 container의 identity에 그 container 자체의
  내부 순번을 더한 것이므로, 같은 구성원 번호가 서로 다른 두 container
  아래에서 반복될 수 있습니다.
- Stage 90 package 구성원은 `m####-<slug>.md`로 이름 붙이며, Registry
  profile 경로가 그 규칙을 소유하고
  `scripts/lib/document_governance/references.py`가 그 분류를 실행합니다.
- 폐기된 번호는 각 top-level identity space의 `reserved_history`에 정렬된
  목록으로 둡니다. 예약된 번호는 다시 발급하지 않으며, Stage 01 번호 공백과
  Stage 03 package 삭제는 그 번호가 예약되어 있을 때만 정당합니다.
- Incident 번호는 연도 partition마다 다시 시작하므로, 연도는 경로뿐
  아니라 identity에도 속합니다.
- 안정적인 package ID는 등록된 접두사와 대소문자를 유지합니다.
- Requirement 자식은 owner를 완전히 포함한 ID를 사용합니다:
  `REQ-####-FR-####`, `REQ-####-NFR-####`. `IF` 자식은 더 발급하지 않으며,
  기존 `REQ-####.IF` 공간은 예약 이력을 보존하는 append-only 기록으로만 남습니다.
- FR, NFR, IF 카운터는 package가 소유합니다. Registry 발급 key는 전체
  owner를 포함하므로(예: `REQ-0001.FR`), 같은 자식 번호가 서로 다른 두
  Requirement Package에서 독립적으로 발급될 수 있습니다.
- 발급된 번호는 다시 사용하지 않습니다. `high_water`는 절대 감소하지
  않고 `next_number`는 항상 `high_water`보다 큽니다.
- 재사용 검사의 이력 범위는 HEAD에서 도달 가능한 commit입니다. 병합되지
  않은 다른 branch가 같은 번호를 발급하면 Registry `high_water` 줄의 병합
  충돌로 드러나며, 그 branch가 이 checkout의 검사 결과를 바꾸지 않습니다.
- Operations subject와 role artifact는 독립적인 안정 ID를 가집니다.
  Registry는 네 자리 subject route와 각 role ID 형태를 검증하지만 그
  번호를 서로 동일시하지 않습니다. 현재 catalog 디렉터리 포함 관계가
  role-subject 소속을 소유합니다.
- Incident 연도 디렉터리만 날짜-경로 예외입니다.
- lifecycle 전이는 그 profile의 lifecycle에 등록된 경우에만 유효합니다.
  terminal 상태에는 나가는 전이가 없습니다.

의미적 흐름은 profile마다 다릅니다: Requirement는 검토 후 승인하고, ADR은
수락하거나 거부합니다. Spec과 Plan은 계약·계획의 승인 권한만 나타내며,
진행·차단·완료는 Task 또는 Execution Item이 소유합니다.
Task는 준비 상태를 거쳐 진행 중이 됩니다. Guide·Policy·Runbook과 common rule·Skill은
검토 후 active가 되며, Postmortem과 reference는 게시되고, Navigation README는
active로 유지됩니다. `registry.json`이 모든 진입 상태, edge, terminal
상태의 정확한 권위로 남습니다.
전체 Git history 발급 검증은 전체 문서 계약 profile이 소유합니다. 변경
검증은 저장된 Registry 발급 상태를 사용합니다.

##### Cancellation

`cancelled` Task에는 `cancellation`이 필요합니다. 실제 `reason`과 `authorization_ref`,
`criteria_disposition`을 작성합니다. 각 `criterion`에는 `successor` 또는 승인된
범위 철회 참조 `withdrawal_ref` 중 하나만 둡니다. 재배정 대상은 같은 package의
자신이 아닌 유효한 Task여야 합니다. 취소는 완료 영수증의 PASS 의무를 면제하지
않으며 template은 승인값을 미리 채우지 않습니다.

문서를 은퇴시킬 때는 남아야 할 내용을 01·02 문서의 Traceability에 요약하고 원본을
삭제한 뒤, 그 번호를 `reserved_history`에 추가합니다. Stage 98은 기록을 담지
않습니다.

## Related Documents

### Upstream and Downstream

[docs 색인](../README.md)이 stage 전체의 진입점이며, Stage 99는 다른 stage 문서의 profile, 경로, 식별자, template을 등록합니다.

### Policy and Templates

- [에이전트 작업 규칙](AGENTS.md)
- [Template catalog](./templates/README.md)
- [Canonical agent governance home ADR](../02.architecture/decisions/0032-canonical-agent-governance-home.md)
- [문서 작성 계약](../../.agents/governance/documentation-protocol.md#readme-and-agentsmd): README 형식과 언어 규칙의 정본
- [README 템플릿](templates/common/readme-stage.template.md): 이 README의 양식 원본
