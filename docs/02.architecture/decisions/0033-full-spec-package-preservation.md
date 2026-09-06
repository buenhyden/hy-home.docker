---
title: "Spec Package 전체 본문 보존"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "@buenhyden"
updated: "2026-09-06"
layer: "architecture"
artifact_id: "ADR-0033"
parent_ids:
- "AD-0030"
created: "2026-09-06"
---

# ADR-0033: Spec Package 전체 본문 보존

## Context

현재 문서 보존 정책과 Spec Package validator는 Stage 03을 떠나는 완료 package가
Spec, Plan, 모든 Task를 보존하도록 요구합니다. Git object는 보존본의 출처와
복구 가능성을 증명하지만, 저장소에서 직접 발견하고 읽을 수 있는 본문을
대체하지 않습니다.

accepted 상태인 ADR-0031은 완료 package의 영구 보존 단위를 Spec으로 한정하고
Plan과 Task를 transient 운반체로 규정했습니다. 그 본문을 현재 계약에 맞게
고치면 채택된 결정을 사후에 바꾸게 됩니다. 반대로 그 결정을 그대로 현재
권위로 두면 정책, 실행 가능한 guard, Requirement와 Architecture Description이
서로 다른 보존 단위를 소유하게 됩니다.

이 결정은 현재 보존 보장을 바꾸지 않고 그 보장의 durable decision owner를
정합화하기 위한 제안입니다. 기존 frozen record의 범위나 내용을 소급해
바꾸거나 SPEC-0173을 완료시키지 않습니다.

## Decision Drivers

- Spec, Plan, Task의 원문 실행 맥락을 Git 명령 없이 발견하고 검토할 수 있어야
  합니다.
- lifecycle status, 보존할 본문, 처분을 설명하는 기록은 서로 다른 사실로
  유지되어야 합니다.
- accepted decision과 frozen record의 본문은 나중 계약에 맞추기 위해
  다시 쓰지 않아야 합니다.
- 현재 의미의 owner 이전, terminal status 전환, archive 이동은 중간 권위
  상태를 만들지 않아야 합니다.
- 일반 package 처분과 승인된 divergent-branch handoff의 증거 계약을 섞지
  않아야 합니다.

## Options Considered

1. **ADR-0031의 Spec-only 보존과 Git 기반 Plan/Task 복구를 유지.** 기존 결정을
   그대로 둡니다. 기각: Plan과 Task 본문을 저장소에서 직접 보존해야 한다는
   현재 정책 및 실행 가능한 package guard와 충돌합니다.
2. **accepted ADR-0031의 본문을 현재 의미로 수정.** 현재 문서 수를 늘리지
   않습니다. 기각: 실제로 채택되었던 Spec-only 결정을 지우고 명시적
   supersession 및 보존 lifecycle을 우회합니다.
3. **ADR-0031의 본문을 보존하고 검토된 successor로 전체 package 보존을
   소유.** 기존 결정과 현재 결정을 모두 추적할 수 있고 현재 정책 및 guard와
   한 보존 단위로 수렴합니다. 채택 제안.

## Decision

이 문서는 세 번째 방안을 제안합니다. 검토 후 수락되면 Stage 03 package의
완료, 대체 또는 철회는 다음 규칙을 따릅니다.

1. 현재 의미를 갖는 obligation, decision, structure, procedure와 current
   consumer가 요구하는 증거를 terminal 전환 전에 canonical Agent governance,
   Stage 01, Stage 02 또는 Stage 05 owner로 이전하고, inbound consumer를 같은
   논리 변경에서 새 owner로 전환합니다.
2. package의 Spec, Plan, 모든 Task는 등록된 lifecycle에 따른 status와 실제
   completion evidence를 먼저 갖춥니다. 미완료이거나 차단된 package는 active
   Stage 03에 남습니다.
3. terminal 전환과 처분은 하나의 결과 tree에서 원자적으로 이루어집니다.
   Spec, Plan, 모든 Task의 전체 본문은 함께 해당
   `docs/98.archive/<disposition>/03.specs/` 경로로 이동하며, 이동된 본문은
   frozen evidence가 됩니다. outcome을 Spec이나 다른 current owner에 write
   back했다는 사실은 Plan 또는 Task 본문을 삭제할 근거가 아닙니다.
4. status는 member의 lifecycle 상태를, frozen body는 당시 내용을, archive
   경로와 처분 기록은 이동 이유를 각각 표현합니다. 완료와 대체는 terminal
   status 및 supersession lineage로 처분을 설명하므로 Tombstone을 만들지
   않습니다. 철회는 전체 package 보존본과 package당 Tombstone 하나를 함께
   요구합니다. Tombstone은 본문을 흡수하지 않습니다.
5. Git history와 regular blob은 원본 동일성 및 복구 경로를 증명합니다. 현재
   처분에서 보존해야 할 Spec, Plan 또는 Task 본문을 Git-only 상태로 남기는
   대안이 되지 않습니다.

이미 frozen 상태인 기록은 이 결정에 맞추기 위해 확장, 재구성 또는 수정하지
않습니다. 과거의 Spec-only 보존 package에 누락된 Plan/Task를 소급 생성하지
않으며, 그 기록의 당시 범위 자체를 역사적 사실로 유지합니다. 이 규칙은 이
결정의 수락 이후 current package가 terminal 처분을 시작할 때 적용됩니다.

승인된 divergent-branch package handoff는 별도 예외 계약을 그대로 유지합니다.
그 흐름은 source packet의 status와 전체 파일 집합 및 bytes를 변경 없이
`superseded/`에 보존하고, distinct active target Task가 exact commit, path,
identity와 integration receipt를 운반합니다. target이 나중에 완료되면 그
target의 Spec, Plan, 모든 Task 역시 위의 일반 원자적 보존 규칙을 따릅니다.

## Consequences

- 완료 package의 상세 실행 근거를 Spec 요약과 분리된 원래 Plan/Task 형태로
  계속 검토할 수 있습니다.
- 보존 파일 수와 저장소 크기는 Spec-only 방식보다 증가합니다. 새로운 archive
  경로, 서비스, 보존 기간 또는 runtime 권한은 추가되지 않습니다.
- active Stage 03은 현재 작업만 담고, preserved Task는 새 증거를 받지 않는
  frozen record가 됩니다.
- completion, supersession, withdrawal의 처분 의미와 Tombstone 요구가 분리되어
  완료나 대체를 철회로 잘못 기록하지 않습니다.
- ADR-0031의 accepted 본문과 기존 archive body는 그대로 남으므로 과거 결정과
  실행 기록의 정확한 역사를 추적할 수 있습니다.
- 현재 정책 및 validator의 전체 package 보장은 유지됩니다. 이 결정은 gate,
  lifecycle edge, permission, model, hook, server 또는 runtime을 추가하지
  않습니다.

## Traceability

- [REQ-0026 문서 보존 및 은퇴](../../01.requirements/0026-document-retention-and-retirement.md)
- [AD-0030 문서 Lifecycle 거버넌스](../descriptions/0030-document-lifecycle-governance.md)
- [ADR-0031 보존 기록으로서의 아카이브](0031-preserved-archive-record.md)
- [SPEC-0173 Governance and QA Surface Convergence](../../03.specs/0173-governance-qa-surface-convergence/spec.md)
- [SPEC-0173 implementation plan](../../03.specs/0173-governance-qa-surface-convergence/plan.md)
- [SPEC-0173 Task 0006](../../03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0006-generated-evidence-and-final-verification.md)

ADR-0031은 이 제안이 바꾸려는 accepted predecessor입니다. 제안 상태에서는
`supersedes` 관계를 선언하지 않습니다. 실제 수락 시에만 ADR-0033을 accepted
successor로 전환하고, ADR-0031의 reciprocal supersession metadata와 frozen
preservation을 같은 lifecycle 변경에서 적용합니다.

## Compliance

기존 metadata, architecture lifecycle, link, corpus lifecycle 및 Spec Package
guard가 각각 제안의 profile, reciprocal supersession, current consumer,
처분과 전체 Spec/Plan/Task membership을 검사합니다. 수락 변경에서는 ADR-0031의
본문과 새 frozen body를 별도로 비교하고 그 실제 결과를 SPEC-0173 Task 0006에
기록해야 합니다. 이 proposed 문서 자체나 일부 문서 check는 전체 repository,
runtime, Hosted CI 또는 SPEC-0173 completion의 PASS를 뜻하지 않습니다.

## Follow-up

독립 검토가 이 제안을 수락할 근거를 확인한 뒤에만 ADR-0033의 initial
`proposed` lifecycle을 `accepted`로 전환합니다. 같은 원자적 변경에서
ADR-0031을 reciprocal successor metadata와 함께 `superseded/`에 보존하고,
REQ-0026과 AD-0030 및 current consumer를 이 결정에 맞춥니다. 실제 승인 근거,
본문 비교, lifecycle transition, 검증 결과와 미해결 blocker는 SPEC-0173 Task
0006이 기록합니다.
