---
title: "보존 대기 package, route 기록 인용, frozen 동일성"
version: "0.2.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "@buenhyden"
updated: "2026-09-16"
layer: "architecture"
artifact_id: "ADR-0036"
parent_ids:
- "AD-0030"
created: "2026-09-15"
---

# ADR-0036: 보존 대기 package, route 기록 인용, frozen 동일성

## Context

2026-09-15 `main@e233d2a19`의 archive 정합성 조사
([RES-0096](../../90.references/research/0096-archive-disposition-consistency/README.md))는
ADR-0035가 수락되어도 남는 세 가지 불일치를 확인했습니다.

첫째, 활성 Stage 03의 occupancy는 문서 단위로 판정됩니다.
`validate_active_stage_occupancy`는 terminal status 문서가 활성 스테이지에 있으면
거부하므로, 정책은 끝난 Task도 package가 함께 이동할 때까지 `in-progress`를
유지하라고 규정합니다. lifecycle은 `in-progress`에서 `completed`로의 전이를 허용하고
`_validate_execution_states`도 `in-progress`와 `blocked` Task만 제약하므로, 막는 것은
이 한 검사뿐입니다. 그 결과 status 필드는 기록된 사실과 다르고, 독자는 본문
증거를 읽어야 완료 여부를 압니다.

둘째, ADR-0035 Decision 4는 `operation/incident`와 `operation/postmortem`이 archive
경로를 직접 인용할 수 있는 이유를 "근거가 보존본 자체인 경우가 많다"로 설명합니다.
그런데 link validator의 예외는 목적지를 가리지 않아, 본문이 없는 Tombstone과
Migration까지 허용합니다. 예외의 근거가 적용되지 않는 대상에도 예외가 열려 있습니다.

셋째, REQ-0026-FR-0012는 보존본이 이동 당시 본문과 byte-identical하다고 요구합니다.
SPEC-0173과 SPEC-0176의 완료 commit은 이동과 같은 commit에서 `version`, `status`,
그리고 Task의 증거 문단과 표 행을 바꾸었습니다. 이동 직전 바이트를 담은 Git 객체가
없으므로 그 동일성은 어떤 객체로도 검증되지 않습니다. ADR-0035의 Retention Catalog
`Source`는 경로, 조상 여부, 객체 유형만 확인합니다.

## Decision Drivers

- lifecycle status는 기록된 사실과 일치해야 하며, 검사를 통과하려고 거짓 status를
  유지하는 규칙이 없어야 합니다.
- package의 terminal 전환과 처분은 계속 하나의 결과 tree에서 원자적으로
  이루어져야 합니다(ADR-0033 Decision 3).
- 인용 예외는 그 근거가 적용되는 대상에만 열려야 합니다.
- "동일하다"는 보장은 Git 객체로 기계 검증할 수 있어야 하며, 저장된 digest나 두 번째
  복구 원장을 만들지 않아야 합니다(REQ-0026-NFR-0006, REQ-0026-FR-0015).
- 이미 frozen 상태인 기록은 소급해 수정하지 않습니다.

## Options Considered

### Occupancy

1. **문서 단위 판정과 `in-progress` 우회 유지.** 기각: status가 사실과 다른 상태가
   제도화됩니다.
2. **처분 대기를 뜻하는 새 Task 상태 추가.** 기각: 처분 대기를 표현하려고 lifecycle에
   실제 작업 상태가 아닌 값을 넣습니다.
3. **package 단위 판정, 비terminal package 안의 `completed` Task만 허용.** 채택 제안.
   `cancelled` Task는 허용하지 않으므로, Task 하나를 취소하는 변경은 그 처분 판단 없이
   통합되지 않습니다.

### Incident 인용 예외

1. **현행 유지.** 기각: 근거가 적용되지 않는 route 기록까지 예외가 열립니다.
2. **예외 폐지.** 기각: 사고 재구성에 필요한 보존 본문 인용까지 막습니다.
3. **예외를 retention class 본문으로 한정하고, route 기록은 모든 출발 문서에서 index
   경유.** 채택 제안.

### Frozen 동일성

1. **현행: 이동 commit에서 자유롭게 편집하고 동일성은 Task 서술로만 기록.** 기각:
   요구와 실제가 다르고 기계 검증이 없습니다.
2. **준비 commit 뒤 순수 rename commit.** 기각: 준비 commit에서 terminal 문서가 활성
   스테이지에 남아 occupancy 검사와 commit마다 실행되는 changed gate를 위반하고,
   REQ-0026-FR-0009와 ADR-0033 Decision 3의 원자성을 깨며, 직접 push하는 통합에서는
   그 중간 상태가 기준 branch에 남습니다.
3. **한 commit을 유지하고 등록된 lifecycle frontmatter 필드만 달라지도록 허용,
   catalog `Source`와 frozen 객체를 기계 비교.** 채택 제안.

## Decision

세 영역 모두 세 번째 방안을 채택합니다.

1. 활성 Stage 03의 occupancy는 package 단위로 판정합니다. package의 terminal 여부는
   Spec의 status가 정합니다. terminal Spec 또는 terminal Plan이 활성 Stage 03에
   있으면 거부합니다. Spec이 terminal이 아닌 package 안에서는 `completed` Task를
   허용하고, `cancelled` Task는 계속 거부합니다. `completed` Task는 처분 승인이 아니며,
   package는 여전히 Spec의 terminal 전환과 함께 전체가 한 번에 이동합니다. Spec이
   terminal인 package는 활성 Stage 03에 어떤 구성원도 남길 수 없습니다. Stage 01,
   02, 05, 90의 단독 문서는 문서 단위 판정을 유지합니다.
2. archive 밖 문서에서 `tombstones/`와 `migrations/`로 가는 링크는 출발 profile과
   무관하게 거부합니다. `operation/incident`와 `operation/postmortem`은 네 retention
   class의 본문을 직접 인용할 수 있습니다. `superseded/`나 `retired/` 본문을 인용할 때
   그것이 역사 증거이며 현재 권위가 무엇인지 적는 일은 의미 검토 항목이고 기계 검사
   대상이 아닙니다.
3. Retention Catalog에 행이 있는 보존 단위는 그 행의 `Source` 객체와 구성원 경로 집합,
   Git 파일 mode, 본문 바이트(개행 포함)가 같아야 합니다. frontmatter는 Registry가
   등록한 lifecycle 필드의 값만 달라질 수 있고, `superseded_by`는 추가될 수 있습니다.
   그 밖의 키 추가, 삭제, 순서 변경은 허용하지 않습니다. frontmatter가 없는 파일은 전체
   바이트가 같아야 합니다. 따라서 완료 증거는 이동 전 commit에 쓰고, 완료 commit은
   lifecycle 필드, 이동, Stage 03 index 행과 Retention Catalog 행, 다른 문서의
   consumer cutover만 담습니다.
4. 이 결정은 catalog 행이 없는 기존 보존본에 소급하지 않으며, 그 기록의 원본 동일성은
   검증 한계로 남깁니다. 필요한 Git 객체가 없으면 통과가 아니라 실패로 보고합니다.
5. 종료된 Incident는 종료 시점을 자기 frontmatter로 말합니다. status가 `resolved`인
   `operation/incident`는 비어 있지 않은 `resolved_at`을 가집니다. `resolved/`
   retention class가 이름으로 가져야 하는 것이 종료 근거이므로, 그 근거가 문서 밖
   서술에만 있으면 보존본이 자기 처분을 자기 서술하지 못합니다. Registry는 이미
   `postmortem`의 `published`에 `reviewed_at`을 요구하는 status-conditional 계약을
   가지므로 이 규칙은 등록 항목 하나로 강제되고 새 check를 만들지 않습니다. 이
   규칙의 Stage 01 owner는 `REQ-0026`의 새 functional requirement이며, SPEC-0178이
   수락과 같은 결과 tree에서 그것을 개정합니다.

## Consequences

- 끝난 Task가 자기 status로 완료를 말하므로, 정책의 `in-progress` 우회 문단과
  REQ-0026-FR-0009가 개정됩니다.
- 종료 시점이 없는 Incident는 `resolved`가 될 수 없습니다. `resolved/`로의 이동을
  수행하는 규칙은 이 결정의 범위가 아닙니다. REQ-0026은 이 의무를 소유하는
  functional requirement를 얻으며, 그 requirement 없이는 이 결정의 규칙 서술이
  Stage 01 owner를 갖지 못합니다.
- Task 하나의 취소는 여전히 처분 판단을 요구합니다.
- 현재 추적되는 incident와 postmortem 문서가 없으므로, 좁혀진 예외가 거부하는 현재
  링크는 없습니다. REQ-0026-FR-0014와 그 Acceptance Criteria가 개정됩니다.
- REQ-0026-FR-0012의 "byte-identical"은 "`Source` 객체와 동일하며 등록된 lifecycle
  필드만 예외"라는 검증 가능한 불변식으로 바뀌고, 완료 절차는 증거 기록을 이동 전
  commit으로 옮깁니다.
- 이 결정은 ADR-0035를 대체하게 되므로, 수락 시점에 ADR-0035와 그것이 다시 적은
  ADR-0033 규칙 가운데 유지되는 것을 다시 적어야 합니다.

## Traceability

- [AD-0030 문서 Lifecycle 거버넌스](../descriptions/0030-document-lifecycle-governance.md)
- [REQ-0026 문서 보존 및 은퇴](../../01.requirements/0026-document-retention-and-retirement.md)
- [ADR-0035 Stage 98 보존 class와 route 처분](0035-stage-98-retention-classes-and-route-dispositions.md)
- ADR-0033 Spec Package 전체 본문 보존 (superseded)
- [SPEC-0178 Archive Occupancy, Route Citation, and Frozen Identity](../../03.specs/0178-archive-occupancy-citation-and-frozen-identity/spec.md)
- [RES-0096 Archive Disposition Consistency Assessment](../../90.references/research/0096-archive-disposition-consistency/README.md)
- [문서 보존 및 은퇴 정책](../../../.agents/governance/documentation-protocol.md#document-retention-and-retirement)

## Compliance

규칙 서술은 canonical 정책과 REQ-0026이 소유하고, 이 결정은 선택의 근거를 소유합니다.
이 proposed 문서는 어떤 check의 동작도 바꾸지 않으며 PASS를 뜻하지 않습니다. 수락
변경은 SPEC-0178의 Task에 occupancy, link, catalog 검사의 실제 실행 결과를 기록해야
합니다.

## Follow-up

SPEC-0178이 검사를 옮기고 이 결정을 `accepted`로 전환합니다. SPEC-0178은 SPEC-0177이
ADR-0035를 수락하고 완료된 뒤에만 활성화합니다. 이 결정은 수락과 함께 ADR-0035를
supersede합니다. supersession 검사는 effective 상태가 아닌 후속 문서의 `supersedes`를
거부하므로, 그 frontmatter와 ADR-0035의 `superseded_by`는 수락 결과 tree에서 함께
추가하고, 그때 ADR-0035 본문을 기준으로 유지되는 규칙을 이 결정에 다시 적습니다.
