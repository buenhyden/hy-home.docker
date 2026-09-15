---
title: "Stage 98 보존 class와 route 처분"
version: "0.3.1"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "@buenhyden"
updated: "2026-09-15"
layer: "architecture"
artifact_id: "ADR-0035"
parent_ids:
- "AD-0030"
created: "2026-09-15"
---

# ADR-0035: Stage 98 보존 class와 route 처분

## Context

Stage 98은 지금 `completed/`, `superseded/`, `retired/` 세 보존 본문 경로와
`migrations/`, `tombstones/` 두 결정 기록 경로를 가집니다. 이 구조는 두 가지
면에서 현재 필요와 맞지 않습니다.

첫째, 인용 가능성이 이름에서 도출되지 않고 따로 규정되어 있습니다. link
validator(`scripts/lib/document_governance/links.py`)는 archive 밖에서
`completed/`만 허용하는데, Stage 98 README는 같은 문서 안에서 `superseded/`
보존본도 직접 링크할 수 있다고 적습니다. 규칙이 이름과 분리되어 있으니 두
서술이 서로 다른 답을 가지게 되었습니다.

둘째, Tombstone과 Migration이 복구 원장을 이중으로 운반합니다. Tombstone은
`Recovery Commit`을, Migration은 `Recovery`와 source/target mapping을 필수로
가지며, validator는 `retired/` 보존본마다 짝이 되는 Tombstone을 요구합니다.
frozen 본문의 복구 경로는 이미 Git history가 제공하므로, 기록마다 commit과
경로를 다시 적는 것은 같은 사실을 두 곳에서 유지하는 일입니다.

또 종료된 Incident와 게시된 Postmortem을 보존할 경로가 없습니다. Stage 98
README는 `resolved/`가 필요하면 별도 계약 변경으로 검토한다고만 적고 있습니다.

## Decision Drivers

- 인용 가능 여부는 각 처분이 무엇을 이름으로 가지는지에서 도출되어야 하며,
  별도 허용 목록과 서술이 갈라질 수 없어야 합니다.
- 보존본이 현재 권위로 다시 읽히는 경로를 막아야 합니다. 대체된 규칙을
  인용하는 것이 그 규칙이 되살아나는 방식입니다.
- frozen 본문의 복구는 Git history 하나가 담당하고, Stage 98 기록이 두 번째
  복구 원장이 되지 않아야 합니다.
- 이미 봉인된 기록은 새 계약에 맞추기 위해 다시 쓰지 않아야 합니다.
- 규칙 변경과 validator 이전이 중간 권위 상태 없이 순서대로 이루어져야 합니다.

## Options Considered

1. **현재 구조 유지.** 세 보존 경로와 두 결정 기록을 그대로 두고 README의
   `superseded/` 링크 서술만 고칩니다. 기각: 인용 규칙이 이름과 계속
   분리되고, `resolved/`가 없으며, 이중 복구 원장이 남습니다.
2. **모든 archive 경로 인용 허용과 경고 표기.** 링크 제한을 없애고 보존본에
   "현재 권위 아님" 표기를 요구합니다. 기각: frozen 본문에 표기를 추가하려면
   보존본을 다시 써야 하고, 표기는 대체된 규칙이 인용으로 되살아나는 것을
   막지 못합니다.
3. **여섯 처분을 두 종류로 나누고 인용 가능성을 이름에서 도출.** 본문을
   보존하는 retention class 네 개와 본문 없이 외부 route를 기록하는 route
   disposition 두 개로 나눕니다. 채택 제안.

## Decision

세 번째 방안을 채택합니다.

1. Stage 98은 여섯 처분을 가지며, 각 처분의 디렉터리는 그 처분을 처음 쓰는
   변경이 만듭니다. 기록이 아직 없는 처분에는 디렉터리가 없습니다.
2. retention class는 한때 현재였던 전체 본문을 당시 profile 그대로
   보존합니다. `completed/`는 완료되어 반영된 작업과 그것이 승격한 대상을,
   `superseded/`는 새 현재 권위가 대체한 내용과 그 대체 문서를,
   `retired/`는 후속 없이 철회된 규칙이나 범위와 철회 사유를, `resolved/`는
   종료된 Incident bundle과 게시된 Postmortem, 그리고 종료 근거와 현재 교정
   작업 owner를 이름으로 가집니다. 보존은 profile을 따릅니다. frozen 본문은
   불변이고, Git-history-only 처분은 profile이 그렇게 등록할 때 호환 사본 없이
   복구 가능한 출처를 유지합니다. 지금 그렇게 등록한 profile은 없습니다. 처분에는
   별도 승인이 필요합니다.
3. route disposition은 본문을 담지 않습니다. `tombstones/`는 저장소 밖
   consumer를 위한 은퇴 route, 그 후속 또는 부재, 사유를 이름으로 가지고,
   `migrations/`는 이동한 범위와 현재 owner를 `MIG-####`로 가집니다.
4. retention class는 자신의 본문이 여전히 독자를 현재 권위로 이끌 때만
   인용할 수 있습니다. `completed/`는 Promotion 선언을 통해, `resolved/`는
   교정 작업 owner를 통해 인용할 수 있습니다. `superseded/`는 후속을,
   `retired/`는 현재 route를 대신 인용하며, route disposition은 인용하지
   않습니다. frozen 기록을 이름으로 가리켜야 할 때는 식별자로 부르고 Stage 98
   index를 통해 찾습니다. 예외는 `operation/incident` 기록과 그
   `operation/postmortem`뿐이며, 그런 기록이 근거로 삼는 증거가 보존본
   자체인 경우가 많기 때문입니다.
5. 어떤 Stage 98 기록도 두 번째 복구 원장을 운반하지 않습니다. redirect, path
   ledger, 자체 설계한 본문 digest, branch SHA, recovery commit을 담지 않습니다.
   catalog의 Retention Envelope가 source Git object를 한 번 이름으로 가지며,
   frozen 내용의 복구는 일반 Git history가 담당합니다.
6. 이 결정의 수락과 validator 이전은 SPEC-0177이 소유합니다. 수락 전까지 link
   validator는 `completed/`만 허용하고, 수락 이전의 인용은 열거된 consumer로
   남습니다. 이미 봉인된 Tombstone과 Migration은 기록 당시 형태를 역사로
   유지하며 새 계약에 맞추어 다시 쓰지 않습니다.

이 결정은 수락과 함께 ADR-0033을 대체하므로, ADR-0033이 소유하던 규칙 가운데
계속 유효한 것을 다음과 같이 다시 적습니다. 바뀌는 것은 ADR-0033 Decision 4의
Tombstone 짝 요구뿐입니다.

- 현재 의미를 갖는 obligation, decision, structure, procedure와 current consumer가
  요구하는 증거는 terminal 전환 전에 canonical 거버넌스 또는 Stage 01, 02, 05
  owner로 옮기고, inbound consumer를 같은 논리 변경에서 새 owner로 전환합니다.
- Stage 03 package의 Spec, Plan, 모든 Task는 등록된 lifecycle status와 실제
  completion evidence를 먼저 갖추고, 미완료이거나 차단된 package는 active Stage 03에
  남습니다.
- terminal 전환과 처분은 하나의 결과 tree에서 원자적으로 이루어지며, Spec, Plan,
  모든 Task의 전체 본문은 함께 해당 retention class로 이동해 frozen evidence가
  됩니다.
- profile이 frozen 본문을 보존하는 한, 그 본문을 Git-only 상태로 남기는 것은
  보존의 대안이 아닙니다.
- 승인된 divergent-branch package handoff는 source packet의 status와 전체 파일
  집합 및 bytes를 변경 없이 `superseded/`에 보존하고, distinct active target Task가
  exact commit, path, identity와 integration receipt를 운반하는 예외 계약을
  유지합니다.
- 완료와 대체는 철회로 기록하지 않습니다. 새 모양의 Tombstone은 저장소 밖
  consumer의 route를 기록할 뿐 철회 기록이 아니므로, 어느 retention class의
  route든 이름으로 가질 수 있습니다.
- 이미 frozen 상태인 기록은 이 결정에 맞추기 위해 확장, 재구성 또는 수정하지
  않으며, ADR-0031이 accepted였던 기간에 Spec만 보존된 package의 범위는 역사적
  사실로 둡니다.

## Consequences

- 인용 규칙이 각 처분이 이름으로 가지는 대상에서 도출되므로, README와
  validator가 서로 다른 허용 목록을 가질 수 없게 됩니다.
- 종료된 Incident와 Postmortem이 보존 경로를 얻고, 그 기록만 archive 경로를
  직접 인용할 수 있습니다.
- 새 Tombstone과 Migration은 복구 commit과 경로 원장을 적지 않습니다. 기존 봉인
  기록은 그 필드를 역사로 유지하므로, 수락 이후 한동안 두 형태가 공존합니다.
- `retired/` 보존본과 Tombstone의 짝 요구가 사라지므로, 철회 사유는 Stage 98
  README의 Retention Catalog 행이 담습니다. 그 행은 기록의 경로, class, class가
  이름으로 가져야 하는 값, source Git object를 한 번씩 적습니다.
- 수락 시 ADR-0033의 철회 짝 조항(Decision 4)이 바뀌므로, 이 결정은 ADR-0033의
  전체 package 보존 단위를 다시 적고 수락과 함께 ADR-0033을 supersede합니다.
  ADR-0033 Decision 5의 Git-only 배제는 이 결정이 다시 적어 유지하고,
  SPEC-0177이 Git-history-only profile을 등록하지 않으므로 REQ-0026의 Constraint도
  그대로 유지됩니다.

## Traceability

- [AD-0030 문서 Lifecycle 거버넌스](../descriptions/0030-document-lifecycle-governance.md)
- [REQ-0026 문서 보존 및 은퇴](../../01.requirements/0026-document-retention-and-retirement.md)
- [ADR-0033 Spec Package 전체 본문 보존](0033-full-spec-package-preservation.md)
- [SPEC-0177 Archive Disposition Enforcement](../../03.specs/0177-archive-disposition-enforcement/spec.md)
- [문서 보존 및 은퇴 정책](../../../.agents/governance/documentation-protocol.md#stage-98-dispositions)

## Compliance

규칙 서술은 canonical 정책과 Stage 98 README가 소유하고, 이 결정은 그 선택의
근거를 소유합니다. 수락 전 강제 범위는 현재 link validator와 corpus lifecycle
check가 검사하는 범위이며, 이 proposed 문서 자체는 그 check의 PASS를 뜻하지
않습니다. 수락 변경은 SPEC-0177의 Task에 link validator, Tombstone 계약,
Retention Envelope 검사의 실제 실행 결과를 기록해야 합니다.

## Follow-up

SPEC-0177이 validator와 template을 이전하고, Retention Envelope의 형태를
정하고, 이 결정을 `accepted`로 전환합니다. 새 규칙은 Registry의
`common.archive_disposition_model` 스위치 뒤에서 먼저 병합되고, 그 스위치를
`adopted`로 바꾸는 결과 tree가 이 결정을 수락하고 ADR-0033을 supersede합니다.
