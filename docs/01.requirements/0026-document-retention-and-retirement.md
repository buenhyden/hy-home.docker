---
title: "문서 보존 및 은퇴 요구사항"
version: "1.6.1"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-09-16"
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
  문서 자신이 `docs/98.archive/retired/` 아래에 원문 그대로 보존되고, 그 보존
  단위가 철회 기록 정확히 하나를 가집니다. 철회 기록은 그 보존본과 짝을 이루는
  봉인 Tombstone이거나 Stage 98 index의 Retention Catalog 행입니다. 어느 한쪽만
  으로는 은퇴의 근거가 되지 않습니다.
- **REQ-0026-FR-0003**: 등록된 check는 철회 기록이 없는 package 제거를
  거부합니다. 해당 package를 가리키는 link의 존재 여부와 무관합니다.
- **REQ-0026-FR-0004**: 아직 현재 의미를 갖는 obligation, decision, structure,
  procedure는 그것을 담고 있던 문서가 은퇴하기 전에 canonical 공통 Agent 거버넌스, 01,
  02, 05 owner로 이동합니다.
- **REQ-0026-FR-0005**: 이 workspace에 구현된 모든 capability는 Stage 01
  Requirement owner 하나와 Stage 02 Description 또는 ADR owner 하나를 가지며,
  Stage 03 package의 은퇴가 그 coverage를 제거하지 않습니다.
- **REQ-0026-FR-0008**: Tombstone은 은퇴한 route의 stage namespace를 그대로
  반영하는 경로에 놓이며, 그 stage의 첫 Tombstone을 쓰는 변경이 namespace를
  만듭니다. namespace가 없다는 사실이 은퇴를 막거나 철회 기록 없는 제거를
  정당화하지 않습니다.
- **REQ-0026-FR-0009**: 활성 스테이지에는 terminal status 문서가 남지
  않습니다. 판정 단위는 Stage 03에서 package이고 다른 활성 스테이지에서는
  문서입니다. Spec이 terminal이 아닌 package 안의 `completed` Task는 허용되며 그
  Task는 처분을 승인하지 않습니다. package는 여전히 Spec의 terminal 전환과 함께
  전체가 이동하고, terminal Spec 또는 Plan과 `cancelled` Task는 결함으로 남습니다.
  `completed`, `superseded`, `retired` 문서는 처분에 대응하는
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

- **REQ-0026-FR-0012**: 보존 기록은 수정하지 않습니다. Retention Catalog 행이 있는
  단위는 그 행의 `Source` 객체와 구성원 경로, Git 파일 mode, frontmatter 이후 본문
  바이트가 같아야 하며, frontmatter는 등록된 lifecycle 필드만 값이 달라지고
  `superseded_by`만 추가될 수 있습니다. 그 비교가 생기기 전에 쓰인 행은 주장이 아니라
  검증 한계로 남습니다. 철회의 처분과 사유는 `retired/` 경로와 그
  단위의 철회 기록이 담고, 완료와 대체의 처분은 각각 `status`와
  `superseded_by`가 자기 서술합니다. 현재 계약에 맞추기 위한 편집은 보존 대상을 훼손하므로
  보존 기록은 frontmatter와 section 계약의 적용 대상이 아닙니다.
- **REQ-0026-FR-0013**: Stage 98은 여섯 처분을 두 종류로 가집니다. 본문을
  보존하는 retention class는 `completed/`, `superseded/`, `retired/`,
  `resolved/`이고, 본문 없이 저장소 밖 consumer의 route를 기록하는 route
  disposition은 `tombstones/`와 `migrations/`입니다. 각 처분은 자신이 이름으로
  가져야 하는 대상을 가지며, 디렉터리는 그 처분을 처음 쓰는 변경이 만듭니다.
  처분에는 별도 승인이 필요합니다.
- **REQ-0026-FR-0014**: 활성 문서가 archive 경로를 인용할 수 있는지는 처분이
  이름으로 가지는 대상에서 도출됩니다. index, `completed/`, `resolved/`만 인용할
  수 있고, `superseded/` 대신 후속을, `retired/`, Tombstone, Migration 대신 현재
  route를 인용합니다. 보존본을 직접 인용할 수 있는 것은 `operation/incident`와 그
  `operation/postmortem`뿐이며, route 기록은 본문을 담지 않아 그 예외가 닿을 대상이
  없으므로 출발 profile과 무관하게 인용할 수 없습니다.
- **REQ-0026-FR-0015**: 어떤 Stage 98 기록도 redirect, path ledger, 자체 설계한
  본문 digest, branch SHA, recovery commit 같은 두 번째 복구 원장을 담지
  않습니다. source Git object는 Retention Envelope가 한 번 이름으로 가지며,
  frozen 내용의 복구는 Git history가 담당합니다.
- **REQ-0026-FR-0016**: 종료된 Incident는 종료 시점을 자기 frontmatter로
  말합니다. status가 `resolved`인 `operation/incident`는 비어 있지 않은
  `resolved_at`을 가집니다. `resolved/`가 이름으로 가져야 하는 것이 종료 근거이므로,
  그 근거가 문서 밖 서술에만 있으면 보존본이 자기 처분을 자기 서술하지 못합니다.

## Non-functional Requirements

- **REQ-0026-NFR-0006**: 은퇴 check는 현재 tree와 Stage 98에서 판정을
  도출합니다. 고정된 count, digest, expected commit chain은 판정에 참여하지
  않습니다.
- **REQ-0026-NFR-0007**: 철회 기록 하나가 은퇴한 보존 단위 하나를 기록하며
  member 단위로 생성하지 않습니다. archive는 파일 수가 아니라 은퇴 횟수에
  비례해 증가합니다.

## Constraints

- Stage 98의 처분별 하위 트리는 은퇴·완료·대체 당시 보존 대상으로 선택된
  본문을 frozen copy로 보존하며, 그 동일성은 REQ-0026-FR-0012가 정의합니다.
  완료 package의 보존 대상은
  outcome을 write back한 Spec, 그 Plan, 그리고 모든 Task입니다. Retention
  Catalog가 한 번 이름으로 가지는 source Git object는 보존본의 원본 동일성을
  증명하며 redirect 권위를 만들지 않고, 보존해야 할 본문을 Git-only 상태로
  남기는 대안이 되지 않습니다.
  ADR-0031이 accepted였던 기간에 Spec만 보존된 package의 당시 범위는 역사적
  사실로 유지하며 누락된 member를 소급 생성하지 않습니다.
- 변경의 비교 base는 그 변경의 분기 지점이므로, base에서 terminal이 아닌
  status는 그 문서를 은퇴시키는 동일한 변경이 terminal로 관측할 수 없습니다.
  따라서 terminal-status 의무는 base 대비 강제가 아니라 철회 기록에 기록됩니다.
- Git-history-only 처분은 profile이 그렇게 등록할 때만 적용되며 현재 그런
  profile은 없으므로, 보존 대상 본문을 Git-only로 남기지 않는다는 위 첫
  Constraint가 모든 처분에 그대로 적용됩니다. 이미 봉인된 Tombstone과 Migration은
  기록 당시 형태를 유지하며 새 계약에 맞추어 다시 쓰지 않습니다.

## Acceptance Criteria

- 철회 기록 없이 제거된 package는 등록된 check에서 실패합니다.
- 철회 기록과 함께 제거된 package는 대응하는 `retired/` frozen copy가 있고, 그
  단위의 철회 기록이 정확히 하나이며, 봉인 Tombstone의 recovery commit 또는
  Retention Catalog 행의 source Git object가 원래 경로에서 해석될 때만
  통과합니다.
- 보존 규칙은 Spec Package를 적재하지 않고 `.agents/`에서 읽을 수 있습니다.
- ADR-0033 수락 이후 `completed`로 처분된 Spec Package는 Spec, Plan, 모든
  Task 본문을 같은 보존 경로에 함께 보유합니다.
- terminal 전환, archive 이동, current consumer cutover는 하나의 결과 tree에
  적용됩니다. active Stage 03의 점유는 REQ-0026-FR-0009에 따라 package 단위로
  판정되므로, Spec이 terminal이면 어떤 구성원도 남지 않고 그 전까지 남을 수
  있는 terminal 구성원은 `completed` Task뿐입니다.
- Tombstone이 존재하는 모든 stage namespace는 그 stage에서 실제로 route 은퇴가
  일어났음을 뜻합니다. 철회를 Retention Catalog 행이 기록한 은퇴는 Tombstone
  namespace를 만들지 않습니다.
- archive 밖 문서에서 `superseded/`와 `retired/`로 가는 링크는
  `operation/incident`와 `operation/postmortem`이 아니면 등록된 check에서
  실패하고, `tombstones/`와 `migrations/`로 가는 링크는 그 둘을 포함한 모든 출발
  profile에서 실패합니다.

## Traceability

- [문서 보존 및 은퇴 정책](../../.agents/governance/documentation-protocol.md)
- [문서 lifecycle 거버넌스 아키텍처](../02.architecture/descriptions/0030-document-lifecycle-governance.md)
- ADR-0033 Spec Package 전체 본문 보존 (superseded)
- ADR-0031 보존 기록으로서의 아카이브 (superseded)
- ADR-0035 Stage 98 보존 class와 route 처분 (superseded)
- [ADR-0036 보존 대기 package, route 기록 인용, frozen 동일성](../02.architecture/decisions/0036-archive-occupancy-citation-and-frozen-identity.md)

## Related Documents

- [Stage authoring matrix](../../.agents/governance/stage-authoring-matrix.md)
- [Stage 99 registry](../99.templates/registry.json)
