---
title: 문서 보존 및 은퇴 요구사항
type: sdlc/requirement
layer: requirements
status: active
owner: "@buenhyden"
artifact_id: REQ-0026
parent_ids: []
created: 2026-09-01
updated: 2026-09-01
---

# 문서 보존 및 은퇴 요구사항

## Problem and Goals

거버넌스 문서가 축적되는 동안 문서가 얼마나 오래 유지되는지에 대한 규칙이
없었습니다. 은퇴는 변경마다 개별적으로 판단되었고, 그 판단 근거는 은퇴를
수행한 일회성 packet 안에만 존재했습니다. 그 packet이 종료되면 규칙과 무엇이
삭제되었는지에 대한 기록이 함께 사라져, 삭제된 내용이 Git에서 복구는
가능하지만 **발견은 불가능한** 상태가 되었습니다.

목표는 그 규칙을 적용한 변경보다 오래 살아남는 보존 규칙입니다. 문서는 현재
의미를 소유하는 동안 유지되고, 제거될 때는 항상 추적 가능한 pointer를
남깁니다.

## Stakeholders and User Needs

- Repository 관리자는 문서를 만든 packet을 읽지 않고도 그 문서가 왜 존재하며
  언제 사라져도 되는지 알아야 합니다.
- Agent는 기계적으로 검사 가능한 은퇴 조건이 필요합니다. 무관한 작업의
  부수효과로 링크 없는 문서가 삭제되어서는 안 됩니다.
- 감사자는 무엇이 제거되었고, 왜 제거되었으며, 그 내용이 어디로 갔는지 찾을
  수 있어야 합니다.

## Functional Requirements

- **REQ-0026-FR-0001**: 보존 판단은 lifecycle status와 소유권을 입력으로
  사용합니다. 문서의 나이와 corpus 크기는 보존 판단의 입력이 될 수 없습니다.
- **REQ-0026-FR-0002**: package 또는 단독 문서의 은퇴는 Stage 98 Tombstone을
  정확히 하나 생성합니다. Tombstone은 retired path, replacement 또는 `none`,
  reason, recovery commit을 담습니다.
- **REQ-0026-FR-0003**: 등록된 check는 Tombstone이 없는 package 제거를
  거부합니다. 해당 package를 가리키는 link의 존재 여부와 무관합니다.
- **REQ-0026-FR-0004**: 아직 현재 의미를 갖는 obligation, decision, structure,
  procedure는 그것을 담고 있던 문서가 은퇴하기 전에 canonical Stage 00, 01,
  02, 05 owner로 이동합니다.
- **REQ-0026-FR-0005**: 이 workspace에 구현된 모든 capability는 Stage 01
  Requirement owner 하나와 Stage 02 Description 또는 ADR owner 하나를 가지며,
  Stage 03 package의 은퇴가 그 coverage를 제거하지 않습니다.

## Non-functional Requirements

- **REQ-0026-NFR-0006**: 은퇴 check는 현재 tree와 Stage 98에서 판정을
  도출합니다. 고정된 count, digest, expected commit chain은 판정에 참여하지
  않습니다.
- **REQ-0026-NFR-0007**: Tombstone 하나가 은퇴한 package 하나를 기록하며 member
  단위로 생성하지 않습니다. archive는 파일 수가 아니라 은퇴 횟수에 비례해
  증가합니다.

## Constraints

- Git이 내용 복구 경계로 남습니다. Stage 98은 pointer만 저장하며 은퇴한 본문의
  복제본이나 redirect 문서를 저장하지 않습니다.
- 변경의 비교 base는 그 변경의 분기 지점이므로, base에서 terminal이 아닌
  status는 그 문서를 은퇴시키는 동일한 변경이 terminal로 관측할 수 없습니다.
  따라서 terminal-status 의무는 base 대비 강제가 아니라 Tombstone에 기록됩니다.

## Acceptance Criteria

- Tombstone 없이 제거된 package는 등록된 check에서 실패합니다.
- Tombstone과 함께 제거된 package는 통과하며, 그 Tombstone은 retired path와
  정규 Git blob으로 해석됩니다.
- 보존 규칙은 Spec Package를 적재하지 않고 Stage 00에서 읽을 수 있습니다.

## Traceability

- [문서 보존 및 은퇴 정책](../00.agent-governance/policies/documentation-protocol.md)
- [문서 lifecycle 거버넌스 아키텍처](../02.architecture/descriptions/0030-document-lifecycle-governance.md)
- [ADR-0030 은퇴 기록으로서의 Tombstone](../02.architecture/decisions/0030-tombstone-retirement-record.md)

## Related Documents

- [Stage authoring matrix](../00.agent-governance/policies/stage-authoring-matrix.md)
- [Stage 99 registry](../99.templates/registry.json)
