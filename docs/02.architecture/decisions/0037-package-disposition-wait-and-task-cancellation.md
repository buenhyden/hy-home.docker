---
title: "완료 package의 처분 대기와 Task 취소"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "@buenhyden"
updated: "2026-09-17"
layer: "architecture"
artifact_id: "ADR-0037"
parent_ids:
- "AD-0030"
created: "2026-09-17"
---

# ADR-0037: 완료 package의 처분 대기와 Task 취소

## Context

[ADR-0036](./0036-archive-occupancy-citation-and-frozen-identity.md) Decision 1은
활성 Stage 03의 occupancy를 package 단위로 판정하면서 두 가지를 계속 거부합니다.
Spec이 terminal이 아닌 package 안의 `cancelled` Task, 그리고 활성 Stage 03에 남은
terminal Spec 또는 terminal Plan입니다. 2026-09-17 `main@2edac5bd6` 기준으로
`scripts/lib/document_governance/archive.py`의 `validate_active_stage_occupancy`가
이 두 거부를 집행하고, REQ-0026-FR-0009와 정책의 Retention by status 절이 같은
규칙을 서술합니다.

이 두 거부는 각각 다른 비용을 만듭니다.

첫째, Task 하나를 취소하는 정당한 변경이 package의 처분 판단 없이는 통합되지
않습니다. ADR-0036은 이를 의도된 결과로 기록했지만, 그 결과 취소된 작업은
`in-progress`나 `blocked`로 남거나 삭제되는 두 선택만 가집니다. 전자는 status가
사실과 다르고, 후자는 실행 증거를 잃습니다. 취소 사유와 그 Task가 맡던 수용
기준의 행방은 어디에도 기계적으로 기록되지 않습니다.

둘째, 완료와 처분이 같은 commit에 묶입니다. ADR-0036 Options Considered의 Frozen
동일성 2번 방안(준비 commit 뒤 순수 rename commit)은 "준비 commit에서 terminal
문서가 활성 스테이지에 남아 occupancy 검사를 위반한다"는 이유로 기각되었습니다.
그래서 완료 commit은 lifecycle 필드와 이동을 함께 담고, 보존본의 `Source`는 이동
직전의 완성된 원본이 아니라 그보다 앞선 commit이 됩니다. 두 객체의 차이는
Registry `common.frozen_transition_fields`가 허용하는 lifecycle 필드 변환으로만
설명됩니다. 또한 `spec_packages.py`의 `_validate_completion_evidence`는 Spec이
`completed`가 되기 전에는 실행되지 않으므로, 완료 영수증의 결함은 이동하는 그
commit에서야 드러납니다(SPEC-0178 Failure Modes 마지막 행).

마지막으로, terminal status 집합이 Registry `lifecycles.<id>.terminal_statuses`에서
읽히지 않고 `archive.py`의 `TERMINAL_DOCUMENT_STATUSES`와 `spec_packages.py`의
`_TERMINAL_STATUSES`에 각각 하드코딩되어 있습니다. 완료 검증은 이미 Registry 값을
읽으므로 같은 의미를 세 곳이 따로 가집니다.

## Decision Drivers

- lifecycle status는 기록된 사실과 일치해야 하며, 검사를 통과하려고 거짓 status를
  유지하거나 실행 증거를 지우는 경로가 없어야 합니다.
- 완료와 처분 승인은 서로 다른 사건입니다. 완료를 기록했다는 사실이 처분을
  승인하지 않고, 처분을 기다린다는 사실이 새 실행을 허용하지 않아야 합니다.
- 취소는 사유, 승인, 그 Task가 맡던 수용 기준의 행방을 기계적으로 확인할 수
  있어야 하며, 수용 기준이 어느 Task에도 도착하지 않는 경로가 없어야 합니다.
- 처분 대기를 표현하려고 실제 작업 상태가 아닌 lifecycle 값을 만들지 않습니다
  (ADR-0036 Occupancy 2번 방안의 기각 사유 유지).
- 허용 status 집합은 Registry 한 곳에서 읽습니다.
- 이미 frozen 상태인 기록은 소급해 수정하지 않습니다.

## Options Considered

### 완료 package의 처분 대기

1. **현행 유지: terminal Spec과 Plan은 활성 Stage 03에서 항상 거부.** 기각: 완료와
   처분이 같은 commit에 묶이고, 완료 영수증 결함이 이동 commit에서야 드러나며,
   이동 직전 원본을 `Source`로 둘 수 없습니다.
2. **처분 대기를 뜻하는 marker나 새 status 도입.** 기각: ADR-0036이 기각한 것과 같은
   비작업 상태를 만들고, marker와 실제 구성원 상태가 어긋날 수 있습니다.
3. **구조 판정: Spec이 `completed`이고 모든 구성원이 terminal이면 처분 대기로 허용.**
   채택 제안. 대기 여부는 이미 있는 status 값에서 도출되고, nonterminal 구성원이
   하나라도 있으면 거부하므로 대기 중 새 실행이 생기지 않습니다.
4. **Task 본문의 승인 영수증을 추가로 요구.** 기각: 영수증 section parser 계약이
   하나 더 생기며, 처분 승인은 이미 이동하는 변경의 승인 경계가 소유합니다.

### Task 취소

1. **현행 유지: 활성 package의 `cancelled` Task는 항상 거부.** 기각: 위 Context의
   첫째 비용.
2. **사유 문자열 하나만 조건부 필수.** 기각: 수용 기준의 재할당을 기계적으로
   확인할 수 없습니다.
3. **cancelled Task 전용 필수 section.** 기각: section별 조건 필수와 표 parser를
   새로 만들어야 합니다.
4. **구조화된 `cancellation` frontmatter를 `cancelled` 조건부 필수로 등록.** 채택
   제안. Registry의 기존 `required_frontmatter_by_status` 계약을 재사용하고, 값의
   구조와 참조 무결성만 확인하는 판정 하나를 package 검증에 둡니다.

## Decision

1. 활성 Stage 03의 occupancy는 계속 package 단위로 판정합니다. Spec이 `completed`인
   package는 Plan이 `completed`이고 모든 Task가 `completed` 또는 유효한 취소 근거를
   가진 `cancelled`일 때 처분 대기로 활성 Stage 03에 남을 수 있습니다. 그 package에
   terminal이 아닌 구성원이 하나라도 있으면 결함입니다. Spec이 `cancelled` 또는
   `superseded`인 package는 이 결정의 대기 대상이 아니며 계속 결함입니다.
2. 처분 대기는 처분 승인이 아닙니다. package는 여전히 Spec, Plan, 모든 Task가 함께
   한 번에 이동하며, 이동에는 별도 승인이 필요합니다. 대기 중인 package에서 새
   작업을 하려면 새 package에서 시작하고, terminal 구성원을 nonterminal로 되돌리지
   않습니다.
3. Spec이 terminal이 아닌 package 안의 `cancelled` Task는 유효한 `cancellation`을
   가지면 허용하고, 없거나 무효하면 결함입니다. terminal Plan은 Spec이 `completed`인
   경우에만 허용합니다.
4. `task` profile은 `cancellation`을 `cancelled` 조건부 필수 frontmatter로 등록합니다.
   값은 비어 있지 않은 `reason`, `approved_by`, `approved_at`(날짜)과 `criteria`
   목록을 가집니다. `criteria`의 각 항목은 Spec의 Acceptance Contract 번호 목록에
   실재하는 `criterion`과, `reassigned_to` 또는 `withdrawn` 가운데 정확히 하나를
   가집니다. `reassigned_to`는 같은 package에 실재하고 자신이 아니며 `cancelled`가
   아닌 Task의 식별자입니다. `withdrawn`은 사유이며 완료 영수증의 criterion 커버리지
   의무를 면제하지 않습니다. 수용 기준 자체를 철회하려면 Spec을 개정합니다.
   template은 `cancellation`을 seed하지 않습니다.
5. occupancy와 package 검증은 terminal status 집합을 Registry
   `lifecycles.<id>.terminal_statuses`에서 읽고, 코드 안의 별도 상수를 두지 않습니다.
6. 완료 대기가 허용되므로 완료 영수증 검증은 이동 전 활성 Stage 03에서 실행됩니다.
   완료 전환과 이동은 서로 다른 통합 상태가 될 수 있고, 각 상태가 이 결정의 판정을
   만족해야 합니다. 이 결정은 보존본과 `Source`의 비교 규칙
   (ADR-0036 Decision 3, `common.frozen_transition_fields`)을 바꾸지 않습니다.
   완료 전환이 앞선 commit으로 분리될 때 그 비교를 exact 동일성으로 좁히는 일은
   후속 결정이 소유합니다.

ADR-0036 Decision 2(route 기록 인용 금지와 incident/postmortem 예외), Decision 3
(`Source` 비교), Decision 4(소급 금지와 객체 부재의 실패 보고), Decision 5
(`resolved` Incident의 `resolved_at`), 그리고 ADR-0036이 ADR-0035에서 다시 적은
유지 규칙은 이 결정이 수락될 때 다시 적어 유지합니다. 바뀌는 것은 위 1, 3, 4,
5, 6뿐입니다.

## Consequences

- Task 하나의 취소가 package의 처분 판단 없이 통합되며, 그 사유와 수용 기준의
  행방이 frontmatter로 남습니다.
- 완료 영수증 결함이 이동 전에 드러나므로, 이동 commit에서 본문을 고쳐야 하는
  경우가 사라집니다.
- 처분 대기 package가 Stage 03에 남을 수 있으므로, Stage 03 index는 진행 중
  package와 처분 대기 package를 구분해 보여야 합니다. index를 현재 작업과 역사
  탐색으로 나누는 일은 이 결정의 범위 밖입니다.
- REQ-0026-FR-0009, 정책의 Retention by status 절, `task-checklists.md`의 완료
  항목이 개정되고, `task` profile과 task template 설명이 `cancellation`을 얻습니다.
- 대기 중인 package가 오래 남을 수 있습니다. 나이는 처분 검토의 계기일 뿐 삭제의
  근거가 아니라는 기존 규칙이 그대로 적용됩니다.
- `cancelled` Spec package의 처분 대기는 여전히 허용되지 않으므로, package 전체의
  취소는 철회 기록과 함께 한 번에 처분합니다.

## Traceability

- [AD-0030 문서 Lifecycle 거버넌스](../descriptions/0030-document-lifecycle-governance.md)
- [REQ-0026 문서 보존 및 은퇴](../../01.requirements/0026-document-retention-and-retirement.md)
- [ADR-0036 보존 대기 package, route 기록 인용, frozen 동일성](./0036-archive-occupancy-citation-and-frozen-identity.md)
- [SPEC-0179 Package Disposition Wait and Task Cancellation](../../03.specs/0179-package-disposition-wait-and-task-cancellation/spec.md)
- [문서 보존 및 은퇴 정책](../../../.agents/governance/documentation-protocol.md#retention-by-status)

## Compliance

규칙 서술은 canonical 정책과 REQ-0026이 소유하고, 이 결정은 선택의 근거를
소유합니다. 이 문서 자체는 어떤 check의 PASS도 뜻하지 않습니다. 수락 변경은
SPEC-0179의 Task에 occupancy, package, metadata 검사의 실제 실행 결과를 기록해야
합니다.

## Follow-up

SPEC-0179가 검사를 옮기고 이 결정의 수락을 소유합니다. supersession 검사는 effective
상태가 아닌 후속 문서의 `supersedes`를 거부하므로, 이 결정의 `supersedes`와
ADR-0036의 `superseded_by`는 수락과 같은 결과 tree에서 함께 추가합니다. 완료 전환을
분리한 원본에 대한 exact 동일성은 별도 결정이 다룹니다.
