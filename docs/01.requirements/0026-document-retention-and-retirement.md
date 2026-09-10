---
title: "문서 보존 및 은퇴 요구사항"
version: "1.3.0"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-09-07"
layer: "requirements"
artifact_id: "REQ-0026"
parent_ids: []
created: "2026-09-01"
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
- **REQ-0026-FR-0002**: package 또는 단독 문서의 은퇴는 두 기록을 남깁니다.
  Stage 98 Tombstone 정확히 하나가 retired path, replacement 또는 `none`,
  reason, recovery commit을 담고, 문서 자신은 `docs/98.archive/retired/` 아래에
  원문 그대로 보존됩니다. 어느 한쪽만으로는 은퇴의 근거가 되지 않습니다.
- **REQ-0026-FR-0003**: 등록된 check는 Tombstone이 없는 package 제거를
  거부합니다. 해당 package를 가리키는 link의 존재 여부와 무관합니다.
- **REQ-0026-FR-0004**: 아직 현재 의미를 갖는 obligation, decision, structure,
  procedure는 그것을 담고 있던 문서가 은퇴하기 전에 canonical 공통 Agent 거버넌스, 01,
  02, 05 owner로 이동합니다.
- **REQ-0026-FR-0005**: 이 workspace에 구현된 모든 capability는 Stage 01
  Requirement owner 하나와 Stage 02 Description 또는 ADR owner 하나를 가지며,
  Stage 03 package의 은퇴가 그 coverage를 제거하지 않습니다.
- **REQ-0026-FR-0008**: Tombstone은 은퇴한 문서의 stage namespace를 그대로
  반영하는 경로에 놓입니다. 문서를 은퇴시킬 수 있는 모든 stage는 namespace를
  가지며, namespace가 없다는 사실이 은퇴를 막거나 Tombstone 없는 제거를
  정당화하지 않습니다.
- **REQ-0026-FR-0009**: 활성 스테이지에는 terminal status 문서가 남지
  않습니다. `completed`, `superseded`, `retired` 문서는 처분에 대응하는
  `docs/98.archive/` 하위 트리로 보존 이동합니다. 보존은 이동이므로 status
  표시와 이동을 한 변경 안에서 함께 수행합니다. 두 단계로 나누는 규칙은
  member를 삭제하던 이전 모델의 제약이었고, 실행 증거 삭제 check는 문서가
  다른 경로에 계속 존재하는 이동에는 적용되지 않습니다. Stage 03 완료 시
  영구 outcome은 completed Spec에 먼저 write back하고, 그 package의 Spec,
  Plan, 모든 Task 본문을 함께 `completed/`에 보존합니다. current consumer가
  있는 의미와 증거는 terminal 전환 전에 현재 정본으로 이전하며, outcome을
  write back했다는 사실은 Plan 또는 Task 본문을 제거할 근거가 되지 않습니다.
- **REQ-0026-FR-0010**: Stage 03 package는 경계가 있는 변경 계약입니다.
  정상상태를 서술하는 package는 그 상태를 소유하는 Stage 02 Description과
  Stage 05 subject로 내용을 옮긴 뒤 은퇴합니다.
- **REQ-0026-FR-0011**: Stage 01부터 05까지의 문서 레이어는 상호 참조 링크로
  양방향 추적성을 유지합니다. 이 의무는 문서 거버넌스에 속하므로 개별 도메인
  요구사항이 각자 다시 선언하지 않습니다.

- **REQ-0026-FR-0012**: 보존 기록은 수정하지 않습니다. 이동 또는 삭제 당시
  본문과 byte-identical해야 합니다. 철회의 처분과 사유는 `retired/` 경로와
  Tombstone이 담고, 완료와 대체의 처분은 각각 `status`와 `superseded_by`가
  자기 서술합니다. 현재 계약에 맞추기 위한 편집은 보존 대상을 훼손하므로
  보존 기록은 frontmatter와 section 계약의 적용 대상이 아닙니다.

## Non-functional Requirements

- **REQ-0026-NFR-0006**: 은퇴 check는 현재 tree와 Stage 98에서 판정을
  도출합니다. 고정된 count, digest, expected commit chain은 판정에 참여하지
  않습니다.
- **REQ-0026-NFR-0007**: Tombstone 하나가 은퇴한 package 하나를 기록하며 member
  단위로 생성하지 않습니다. archive는 파일 수가 아니라 은퇴 횟수에 비례해
  증가합니다.

## Constraints

- Stage 98의 처분별 하위 트리는 은퇴·완료·대체 당시 보존 대상으로 선택된
  본문을 byte-identical frozen copy로 보존합니다. 완료 package의 보존 대상은
  outcome을 write back한 Spec, 그 Plan, 그리고 모든 Task입니다. Git object와
  recovery commit은 보존본의 원본 동일성을 증명하며 redirect 권위를 만들지
  않고, 보존해야 할 본문을 Git-only 상태로 남기는 대안이 되지 않습니다.
  ADR-0031이 accepted였던 기간에 Spec만 보존된 package의 당시 범위는 역사적
  사실로 유지하며 누락된 member를 소급 생성하지 않습니다.
- 변경의 비교 base는 그 변경의 분기 지점이므로, base에서 terminal이 아닌
  status는 그 문서를 은퇴시키는 동일한 변경이 terminal로 관측할 수 없습니다.
  따라서 terminal-status 의무는 base 대비 강제가 아니라 Tombstone에 기록됩니다.

## Acceptance Criteria

- Tombstone 없이 제거된 package는 등록된 check에서 실패합니다.
- Tombstone과 함께 제거된 package는 대응하는 `retired/` frozen copy가 있고,
  Tombstone의 recovery commit이 정규 Git blob으로 해석되며, 두 기록의 원래
  경로가 일치할 때만 통과합니다.
- 보존 규칙은 Spec Package를 적재하지 않고 `.agents/`에서 읽을 수 있습니다.
- ADR-0033 수락 이후 `completed`로 처분된 Spec Package는 Spec, Plan, 모든
  Task 본문을 같은 보존 경로에 함께 보유합니다.
- terminal 전환, archive 이동, current consumer cutover가 하나의 결과 tree에
  적용되어 active Stage 03에 terminal 중간 상태가 남지 않습니다.
- Tombstone이 존재하는 모든 stage namespace는 그 stage에서 실제로 은퇴가
  일어났음을 뜻하며, 은퇴가 일어난 stage에 namespace가 없는 경우는 없습니다.

## Traceability

- [문서 보존 및 은퇴 정책](../../.agents/governance/documentation-protocol.md)
- [문서 lifecycle 거버넌스 아키텍처](../02.architecture/descriptions/0030-document-lifecycle-governance.md)
- [ADR-0033 Spec Package 전체 본문 보존](../02.architecture/decisions/0033-full-spec-package-preservation.md)
- ADR-0031 보존 기록으로서의 아카이브 (superseded)

## Related Documents

- [Stage authoring matrix](../../.agents/governance/stage-authoring-matrix.md)
- [Stage 99 registry](../99.templates/registry.json)
