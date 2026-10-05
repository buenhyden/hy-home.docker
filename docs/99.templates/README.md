---
title: "Stage 99 Document Contracts and Templates"
version: "2.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-04"
layer: "templates"
---

# Stage 99 Document Contracts and Templates

## Overview

Stage 99는 문서 경로, profile, identifier, section, lifecycle 상태와 전이,
traceability 형태, 복사용 template의 유일한 권위입니다. machine authority는
[`registry.json`](./registry.json)이며, `contracts/` 아래 두 schema가
registry와 문서 frontmatter를 검증합니다. 사람과 AI agent를 위한 정책은
공통 Agent 거버넌스에 남고, 실행 가능한 gate 동작은 등록된 `scripts/`
모듈에 남습니다.

이전 계약은 Git history로 복구할 수 있으나, 현재 작성이나 검증 입력이
아닙니다.

## Scope

Stage 99가 소유하는 것:

- the Requirement Package and Architecture Description profiles;
- the Guide, Policy, Runbook, Incident, and Postmortem profiles;
- the Research, Audit, Data publication roles and archive route records;
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

## Structure

### Documents

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
    ├── archive/
    └── common/
```

## Usage

1. 등록된 profile과 template 역할을 선택합니다.
2. 선언된 `type` 계약을 바꾸지 않고 등록된 source를 복사합니다.
3. 저장된 high-water mark보다 높은 ID를 발급합니다.
4. placeholder를 바꾸고 전체 traceability ID를 추가합니다.
5. 문서 계약 validator와 owning stage gate를 실행합니다.
6. 계약 자체가 바뀔 때는 Registry, schema, template, consumer, test를 하나의
   검토된 논리적 단위에서 함께 바꿉니다.

### Authority Model

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
fallback과 등록된 frozen archive payload를 포괄하며, 둘 다 현재 작성
대상이 아닙니다.

### Identity and Lifecycle Rules

#### Stage 03 Evidence

Task 상태는 frontmatter에만 둡니다. `Evidence`의 각 행은 기존 criterion과
Plan work unit, 실제 check와 input, result, location, acceptance를 기록하며 Status
열을 두지 않습니다. 필수 criterion의 완료에는 `PASS`와 `accepted`가 모두
필요합니다. Plan의 `Work Breakdown`은 여섯 열이고 Task의 `Evidence`는 여덟
열입니다. 정확한 열 순서와 vocabulary는 Registry가 소유합니다.
Lifecycle Events는 실제 직접 전이와 같은 Task의 evidence anchor만 기록하며
승인 source를 인증하지 않습니다. 승인·검토·실행의 의미는
[SDLC](../../.agents/governance/sdlc.md)가 소유합니다.

#### Registered Identity Shapes

`registry.json`은 profile별 identity 형태를 `artifact_id_pattern`에,
소유 container를 `identity_relation`에 명시합니다. 이 절은 그 필드들이
표현하는 규칙을 설명할 뿐, 필드 자체를 다시 정의하지 않습니다.

#### Required Frontmatter Envelope

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
- Tombstone은 `identity_relation: inherited`를 사용합니다: `artifact_id`는
  `tomb-{retired_artifact_id}`이며,
  `scripts/lib/document_governance/archive.py`가 이를 도출합니다. 네 자리
  파일명은 Registry의 `tombstone` space에서 별도의 단조 증가 발급을
  사용하며 상속된 artifact identity가 있어도 그 `high_water`나 `next_number`
  검사는 그대로 적용됩니다.
- Incident 번호는 연도 partition마다 다시 시작하므로, 연도는 경로뿐
  아니라 identity에도 속합니다.
- 안정적인 package ID는 등록된 접두사와 대소문자를 유지합니다.
- Requirement 자식은 owner를 완전히 포함한 ID를 사용합니다:
  `REQ-####-FR-####`, `REQ-####-NFR-####`, `REQ-####-IF-####`.
- FR, NFR, IF 카운터는 package가 소유합니다. Registry 발급 key는 전체
  owner를 포함하므로(예: `REQ-0001.FR`), 같은 자식 번호가 서로 다른 두
  Requirement Package에서 독립적으로 발급될 수 있습니다.
- 발급된 번호는 다시 사용하지 않습니다. `high_water`는 절대 감소하지
  않고 `next_number`는 항상 `high_water`보다 큽니다.
- Operations subject와 role artifact는 독립적인 안정 ID를 가집니다.
  Registry는 네 자리 subject route와 각 role ID 형태를 검증하지만 그
  번호를 서로 동일시하지 않습니다. 현재 catalog 디렉터리 포함 관계가
  role-subject 소속을 소유합니다.
- Incident 연도 디렉터리만 날짜-경로 예외입니다.
- lifecycle 전이는 그 profile의 lifecycle에 등록된 경우에만 유효합니다.
  terminal 상태에는 나가는 전이가 없습니다.

의미적 흐름은 profile마다 다릅니다: Requirement는 검토 후 승인하고, ADR은
수락하거나 거부하며, Spec과 Plan은 승인 후 진행·차단·완료될 수 있고, Task는
준비 상태를 거쳐 진행 중이 됩니다. Guide·Policy·Runbook과 common rule·Skill은
검토 후 active가 되며, Postmortem과 reference는 게시되고, Navigation README와
current archive catalog는 active로 유지되며 Migration과 Tombstone 기록은
draft 또는 sealed입니다. `registry.json`이 모든 진입 상태, edge, terminal
상태의 정확한 권위로 남습니다.
전체 Git history 발급 검증은 전체 문서 계약 profile이 소유합니다. 변경
검증은 저장된 Registry 발급 상태를 사용합니다.

#### Cancellation and Archive Assessments

`cancelled` Task에는 `cancellation`이 필요합니다. 실제 `reason`과 `authorization_ref`,
`criteria_disposition`을 작성합니다. 각 `criterion`에는 `successor` 또는 승인된
범위 철회 참조 `withdrawal_ref` 중 하나만 둡니다. 재배정 대상은 같은 package의
자신이 아닌 유효한 Task여야 합니다. 취소는 완료 영수증의 PASS 의무를 면제하지
않으며 template은 승인값을 미리 채우지 않습니다.

보존 단위의 실제 재평가만 기존 카탈로그의 `Current Assessments`에 기록합니다.
필드와 판정 순서는 `common.archive_retention`이 소유합니다. 평가·제거 결정은
당시 Task revision의 `archive_authorizations`와 해당 본문의 실제 승인 인용을
연결합니다. 빈 승인값, proposed ADR, 이 일반 계약 채택 승인은 개별 제거 증거가
아닙니다. 포착 행과 기존 원문은 재평가 때 수정하지 않습니다.
승인 항목의 `evidence`는 같은 Task의 `#heading-anchor`이며 해당 절의 실제
승인 인용은 `> @owner approved action for unit on YYYY-MM-DD.` 형식으로
단위·행위·일자·권한자를 명시합니다. 코드 fence의 예제나 부정문은 증거가
아닙니다. 실제 승인 없이 이 문장을 채우지 않습니다.

#### Pinned Requirement Allocation Recovery

일반적인 신뢰 baseline loader는 여전히 엄격합니다. 현재 metadata gate는
추적되는 현재 Task의 `requirement_allocation_recovery_decisions` 필드를
통해서만 기록된 REQ-0012.FR 안정 identity 복원을 복구할 수 있으며, 그
정확한 값 문법은 frontmatter schema에 있습니다. 이 decision은 요청된 비교
base, 결함 commit, 그 유효한 parent, 이전/손상/복구된 발급 집합, 복구된
Requirement 콘텐츠 hash를 고정합니다. 복구는 이들의 Git ancestry, 정규
bounded source, 변하지 않은 defect-to-base Requirement 콘텐츠, 정확히
선언에만 그치는 복구를 검증합니다. 영향받지 않은 모든 발급은 여전히
일반적인 엄격한 loader를 통과합니다. 과거 발급은 `[1, 2, 3, 4]`로
유지되며, 현재 전이는 철회된 번호 3을 예약하고 안정 번호 4를 유지합니다.

누락, 중복, 추적되지 않음, 형식 오류, 오래되거나 불일치하는 증거는
fail-closed로 처리됩니다. 대체 base 검색, history 재작성, 일반 waiver,
identity 재사용은 암묵적으로 허용하지 않습니다. 복구된 commit이 비교
base가 되면, 엄격한 loading은 복구 증거를 참조하지 않고도 성공합니다.

### Template Rules

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

## Related Documents

- [Template catalog](./templates/README.md)
- [Canonical agent governance home ADR](../02.architecture/decisions/0032-canonical-agent-governance-home.md)
