---
title: "Agent Knowledge"
version: "0.3.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2026-09-06"
---

# Agent Knowledge

## Overview

`.agents/knowledge/`는 독자를 canonical owner로 route하는 검증된 living
knowledge를 보관합니다. agent가 매 session마다 추론하는 대신 등록된 파일을
읽는 것만으로 surface ownership, 저장소 vocabulary, verification coverage를
해결하도록 존재합니다.

Knowledge는 authority가 아닙니다. member는 무엇이 사실이고 누가 그 규칙을
소유하는지를 기술하며 규칙 자체는 그 owner에게 남습니다.

## Scope

- 포함: surface-to-authority routing, 저장소 vocabulary, verification
  coverage map, 그리고 검증되어 재사용되는 domain knowledge.
- 제외: `governance/`에 속하는 obligation과 prohibition, `skills/`에 속하는
  순서화된 절차, Stage 02와 Stage 03에 속하는 상세 설계와 specification,
  Stage 05에 속하는 operator 절차, Stage 90에 속하는 일자 지정 단발성 관찰,
  현재 Spec Package Task에 속하는 실행 상태.

obligation을 명시하는 member는 결함입니다. 그 내용을 `governance/`로
route하고 link를 남깁니다.

## Structure

```text
.agents/knowledge/
├── README.md
├── glossary.md
├── repository-map.md
└── verification-surface-map.md
```

모든 member는 owner, scope, source, `observed_at`, validity, sensitivity,
`review_cycle`, invalidation을 선언하여 staleness가 가정이 아니라 탐지
가능하도록 하며 파생 근거가 된 tracked source를 이름 붙이는 `Provenance`
섹션을 갖습니다. source 변경·삭제·정정 또는 review expiry가 발생하면 다시
읽기 전까지 해당 fact는 invalid입니다.

## Usage

1. 기존 member가 이미 해당 내용을 소유하는지 확인합니다. 두 번째 owner를
   추가하는 대신 기존 member를 확장합니다.
2. `docs/99.templates/templates/governance/knowledge.template.md`를 복사하고
   등록된 섹션을 유지합니다.
3. 모든 claim을 tracked source에서 도출하고 그 source를 관찰 commit과
   날짜와 함께 `Provenance` 아래에 이름 붙입니다.
4. member를 stale하게 만드는 조건을 `Refresh Triggers` 아래에 기술합니다.
5. Provider Registry의 `canonical_sources`에 파일을 등록한 뒤 document
   metadata와 agent governance contract 점검을 실행합니다.

### Curation Lifecycle

| Stage | Condition | Owner |
| --- | --- | --- |
| Create | agent가 같은 routing이나 vocabulary를 반복해서 재구성함 | 승인된 Task 내 `doc-writer` |
| Verify | 모든 claim이 이름 붙은 commit의 tracked source로 추적됨 | 검토 전 작성자 |
| Deduplicate | 기존 governance, skill, stage document, member 중 어느 것도 이를 소유하지 않음 | `rules-engineer` 검토 |
| Promote | 여기서 발견된 obligation은 `governance/`로, durable decision은 ADR로 이동 | 소유 stage |
| Retrieve | bootstrap order 또는 role의 관련 문서에서 진입함 | 모든 role |
| Re-review | refresh trigger가 발동하거나 선언된 review cycle이 경과함 | `doc-writer` |
| Expire | route된 owner가 더 이상 존재하지 않거나 claim이 더 이상 유효하지 않음 | `doc-writer` |
| Archive | member가 `living` lifecycle을 통해 대체되거나 폐기됨 | [documentation protocol](../governance/documentation-protocol.md) |
| Delete | age나 count로는 결코 삭제되지 않으며, 등록된 retirement route를 통해서만 삭제됨 | [documentation protocol](../governance/documentation-protocol.md) |

age와 file count는 retention 기준이 아닙니다. member는 routing이 올바른 동안
유지되며 여전히 유효한 의미가 canonical owner로 이동했을 때 폐기됩니다.

## Related Documents

- [Agent governance index](../README.md)
- [Prompt index](../prompts/README.md)
- [Documentation protocol](../governance/documentation-protocol.md)
- Canonical knowledge and prompt surfaces decision (`docs/02.architecture/decisions/0034-canonical-knowledge-and-prompt-surfaces.md`)
- [Documentation index](../../docs/README.md)
