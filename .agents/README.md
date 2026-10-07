---
title: "AI Agent Governance"
version: "1.4.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-07"
layer: "agent-governance"
---

# Agent Governance

## Overview

`.agents/`는 공유 agent governance, role, 재사용 가능한 절차를 위한 저장소 소유의
canonical home입니다. Claude와 Codex는 native adapter를 통해 이 source를
소비합니다. canonical home은 authored content이며 renderer output이 아닙니다.

## Scope

- `governance/`는 approval, security, quality, Git, documentation, workflow,
  bootstrap, SDLC 동작을 소유합니다.
- `roles/`는 안정적인 identity, 책임, permission, handoff를 소유합니다.
- `skills/<skill_id>/SKILL.md`는 호출 가능한 절차를 소유합니다. skill-local
  `agents/openai.yaml`은 명시적 invocation을 요구합니다. skill은 자신만 실행하는
  executable code를 위한 `scripts/`, 본문에 inline하기엔 긴 detail을 위한
  `references/`, output이 사용하는 template을 위한 `assets/`도 소유할 수
  있습니다. 이 세 이름이 허용의 전부입니다. 그 내용은 해당 skill 고유의 것이라
  registry row가 필요 없고 skill 최상위에는 그 외 어떤 것도 존재할 수 없습니다.
  resource는 `SKILL.md` 절차 본문에서 직접 또는 전이적으로 도달해야 합니다.
  절차 본문과 도달한 `references/`의 Markdown link 및 명시적 local token만
  graph edge가 됩니다. `scripts/`는 bounded UTF-8 terminal이고 `assets/`는
  읽지 않는 binary terminal이므로 그 내용을 dependency 문법으로 해석하지 않습니다.
  validator는 symlink와 비정규 node를 따르지 않으며 skill마다 4,096개 entry,
  64단계 directory, 16 MiB text로 순회를 제한합니다. Markdown graph output은
  parse 전에 여는 대괄호 16,384개로 제한합니다. 실행 bit는 도달 가능한 `scripts/`
  file에만 허용됩니다.
- `knowledge/`는 저장소 surface에서 canonical owner로의 검증된 routing과 저장소
  vocabulary, verification coverage를 소유합니다.
- `prompts/`는 반복 작업을 위한 재사용 가능한 input/output contract를
  소유합니다.
- `evaluations/`는 같은 작업의 Skill 없는 출력과 명시적 Skill 호출 출력을
  비교하는 평가 증거 영역입니다. 실제 작업·출력·채점·집계만 보존하며 runtime과
  구성원 authority가 아닙니다. 현재는 역할 안내만 있고 새 증거 분류·등록은 별도
  평가 계약에서 수행합니다. 자동 로드되지 않으며 quality policy가 필수 QA를 소유합니다.
- `governance/providers/registry.yaml`은 provider identity, model/permission
  translation, projection route, hook fact를 소유합니다.
- [Claude](../.claude/provider.md)와 [Codex](../.codex/provider.md)는 각자의
  native loading과 syntax 차이를 소유합니다. 이들의 생성된 README는 output입니다.

Stage 99(`docs/99.templates/README.md`)는 document profile, path, identifier,
lifecycle 값, template을 소유합니다. 등록된 script는 executable check를
소유합니다. 현재 Spec Package Task는 실행 evidence를 소유하며 보존된 Stage 98
record와 Git history가 완료된 evidence를 보관합니다.
README 탐색과 디렉터리 목적 설명은 허용하지만, docs 밖의 현재 지침은 개별 stage
문서에 의존하지 않습니다. 현재 agent 규칙은 해당 governance owner에 두며,
승인된 Spec/Task 읽기와 필요한 registry/schema/template 입력은
`governance/documentation-protocol.md`의 문서 경계 규칙에 따릅니다. 과거 결정의 출처 표시는 현재 실행 권한을 부여하지 않습니다.

## Structure

### Documents

| Path | Purpose |
| --- | --- |
| [governance/](governance/) | 공유 정책과 Provider Registry |
| [roles/](roles/) | 역할 identity와 permission |
| [skills/](skills/) | 명시적으로 호출하는 절차 |
| [knowledge/](knowledge/) | 소유 표면과 검증 경로 |
| [prompts/](prompts/) | 재사용하는 입력과 출력 계약 |
| [evaluations/](evaluations/) | Skill 비교 평가 증거와 작성·보존 안내 |

```text
.agents/
├── README.md
├── evaluations/ # paired Skill evaluation evidence; current README only
├── governance/  # policy, SDLC, hooks, provider registry
├── knowledge/   # 검증된 routing과 vocabulary
├── prompts/     # 재사용 가능한 input/output contract
├── roles/       # 안정적인 identity와 permission
└── skills/      # skill id별 호출 가능한 절차
```

위에서 이름 붙인 세 개의 skill 소유 디렉터리를 제외하면 등록된 canonical
entry만 허용됩니다. 알 수 없는 entry는 보존되며 검토용으로 보고됩니다.
`knowledge/`와 `prompts/`는 canonical owner로 route하며 contract를 선언합니다.
둘 다 obligation을 명시하거나 절차 본문을 담거나 실행 상태를 소유하지
않습니다. 여기에는 공통 runtime, progress ledger, installer, 생성된 role
surface가 도입되지 않습니다.

## Usage

1. 루트 `AGENTS.md` 또는 `CLAUDE.md`로 진입하여 `governance/bootstrap.md`
   (Bootstrap)를 따릅니다.
2. 필요한 policy, role, 명시적으로 선택한 skill, native adapter, 해당 Spec
   Package Task를 읽습니다. Discovery는 permission을 넓히지 않습니다.
3. 승인된 canonical source를 변경하고 Task에 집중된 evidence를 기록합니다.
4. 승인된 projection-input 변경 후에는 등록된 provider renderer의 `--write`와
   `--check` route를 사용합니다. 보고되면 `governance/providers/README.md`의
   정확한 quarantine 절차를 따릅니다. canonical source byte가 보존되고 native
   drift가 0인지 확인합니다.
5. 공유 quality matrix(`governance/quality-standards.md#5-change-type-verification-matrix`)를
   통해 완료 점검을 선택합니다.

## Related Documents

- `governance/sdlc.md` (SDLC)
- `governance/bootstrap.md` (Bootstrap)
- `governance/providers/registry.yaml` (Provider registry)
- Canonical-home decision (`docs/02.architecture/decisions/0032-canonical-agent-governance-home.md`)
- [Documentation index](../docs/README.md)
