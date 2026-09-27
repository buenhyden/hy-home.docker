---
title: "Agent Prompts"
version: "0.2.0"
type: "governance/prompt-index"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2026-09-06"
---

# Agent Prompts

## Overview

`.agents/prompts/`는 반복되는 agent 작업을 위한 재사용 가능한 prompt
contract를 보관합니다. prompt는 무엇이 필요한지, 무엇을 산출해야 하는지,
무엇을 해서는 안 되는지, 진행할 수 없을 때 무엇을 해야 하는지를 선언합니다.
작업 자체가 아니라 작업을 감싸는 envelope입니다.

두 provider 모두 같은 canonical path에서 이 파일을 읽으므로, prompt는
session 경계와 provider 전환을 넘어 유지됩니다.

## Scope

- 포함: 목적, 필수 input, output contract, prohibition, failure handling,
  적용 가능한 role, skill, 평가 기준.
- 제외: `skills/`에 속하는 순서화된 절차 단계, `governance/`에 속하는
  obligation, 현재 Spec Package Task에 속하는 실행 상태와 결과.

prompt를 읽는 것은 어떤 role도 선택하지 않으며 어떤 permission도 부여하지
않습니다. 이미 선택된 role의 permission profile과 승인된 Task scope가 계속
적용됩니다.

## Structure

```text
.agents/prompts/
├── README.md
├── commit-message.md
├── diff-review.md
├── handoff.md
└── test-design.md
```

| Prompt | Answers |
| --- | --- |
| [handoff](handoff.md) | 다음 session은 파일과 Git 상태만으로 어떻게 재개하는가? |
| [diff-review](diff-review.md) | 정확한 diff는 작성자와 무관하게 어떻게 검토되는가? |
| [commit-message](commit-message.md) | commit message는 staged diff로부터 어떻게 작성되는가? |
| [test-design](test-design.md) | test는 requirement와 그 failure condition으로부터 어떻게 도출되는가? |

Prompt slug는 skill id와 구분되게 유지되어 하나의 이름이 두 가지 다른
것으로 resolve되지 않습니다.

## How to Work in This Area

1. 필요한 것이 절차가 아니라 input/output contract인지 확인합니다. 절차는
   skill에 속합니다.
2. `docs/99.templates/templates/governance/prompt.template.md`를 복사하고
   등록된 섹션을 순서대로 유지합니다.
3. 소유 skill과 role의 이름을 명시하고 둘 중 하나를 다시 서술하지
   않습니다.
4. prohibition을 구체적인 거부로 작성하여 독자가 특정 output이 그것을
   위반하는지 판단할 수 있게 합니다.
5. Provider Registry의 `canonical_sources`에 파일을 등록한 뒤 document
   metadata와 agent governance contract 점검을 실행합니다.

### Applying a Prompt

prompt를 불러오고 모든 필수 input을 제공하며 선언된 output을 정확히
산출합니다. input을 사용할 수 없다면 근사치로 대체하지 말고 prompt의
failure handling을 따릅니다. prompt가 어디에 적용되었는지는 현재 Task에
기록합니다. prompt 자체는 아무것도 기록하지 않습니다.

## Related Documents

- [Agent governance index](../README.md)
- [Knowledge index](../knowledge/README.md)
- [Agentic policy](../governance/agentic.md)
- Canonical knowledge and prompt surfaces decision (`docs/02.architecture/decisions/0034-canonical-knowledge-and-prompt-surfaces.md`)
- [Documentation index](../../docs/README.md)
