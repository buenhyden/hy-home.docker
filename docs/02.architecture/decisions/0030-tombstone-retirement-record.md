---
title: 은퇴 기록으로서의 Tombstone
version: 1.0.0
type: sdlc/architecture-decision
layer: architecture
status: active
owner: "@buenhyden"
artifact_id: ADR-0030
parent_ids:
  - AD-0030
created: 2026-09-01
updated: 2026-09-01
---

# ADR-0030: 은퇴 기록으로서의 Tombstone

## Context

거버넌스 문서를 은퇴시키면 문서는 tree에서 사라지고 그 근거는 은퇴를 수행한
packet 안에 남았습니다. 그 packet 자체가 종료 대상이므로, 무엇이 제거되었는지에
대한 기록도 함께 사라졌습니다. Git은 내용을 보관하지만 복구하려면 삭제된
경로를 이미 알고 있어야 했고, 결과적으로 은퇴한 작업은 **복구 가능하면서 동시에
발견 불가능한** 상태였습니다.

2026-09-01에 구체적 사례를 측정했습니다. 한 branch에서 40개 package가 추적
pointer 없이 은퇴했고, 유지된 Stage 03 package 4개는 어떤 종류의 inbound
참조도 없어 이후 변경이 등록된 check 하나도 실패시키지 않고 그것들을 제거할 수
있는 상태였습니다.

또한 저장소는 이전 Stage 03 은퇴에 대해 이미 Tombstone 32개를 유지하고 있었던
반면, 진행 중이던 convergence packet은 모든 Tombstone을 삭제하도록 규정하고
있었습니다. 두 개의 은퇴 관례가 동시에 유효한 상태였습니다.

## Decision Drivers

- 은퇴 기록은 그것을 수행한 packet이 종료된 뒤에도 발견 가능해야 합니다.
- inbound link의 부재가 삭제 허가로 읽혀서는 안 됩니다.
- archive가 은퇴한 내용의 두 번째 복제본이 되어서는 안 됩니다.
- 그 기록은 검토가 아니라 validator로 검사 가능해야 합니다.

## Options Considered

1. **추적 기록 없이 Git에 의존.** 가장 저렴하고 파일이 늘지 않습니다. 기각:
   복구에 경로를 미리 알아야 하고, 검토된 은퇴와 사고성 삭제를 validator가
   구분할 수 없습니다.
2. **모든 은퇴를 담는 단일 ledger table.** 파일 하나로 훑기 쉽습니다. 기각:
   모든 제거가 편집해야 하는 직렬화된 authority가 되며, 이는 같은 convergence
   에서 `docs/98.archive/migrations/`로부터 제거한 바로 그 결합입니다.
3. **은퇴 경로에 redirect 문서 배치.** link가 계속 해석됩니다. 기각: redirect는
   은퇴 경로에 놓인 본문이므로 corpus가 실제로 줄지 않고, 현재 stage가 archive를
   계속 가리키게 됩니다.
4. **은퇴한 package당 Tombstone 하나.** 채택.

## Decision

Stage 98 Tombstone 하나가 은퇴한 package 하나 또는 은퇴한 단독 문서 하나를
기록합니다. Tombstone은 retired path, replacement 또는 `none`, reason,
recovery commit을 담으며 본문은 저장하지 않습니다.

`validate_spec_package_lifecycle`은 `_recorded_retirements`를 통해 Tombstone
집합을 읽고, Tombstone이 없는 package 전체 제거에 대해
`package-retirement-unrecorded`를 보고합니다. 따라서 Tombstone은 Stage 00의
terminal-status, 의미 이관, consumer 갱신 의무가 충족되었다는 강제 가능한
증거입니다. 변경의 비교 base는 그 변경의 분기 지점이므로 동일한 변경이 설정한
status를 base가 보여줄 수 없기 때문입니다.

Tombstone은 저장소의 수명 동안 유지됩니다. 보존은 live navigation consumer로
측정하지 않습니다. inbound link가 없는 Tombstone도 여전히 그 은퇴 경로를
발견 가능하게 만드는 pointer입니다.

## Consequences

긍정적: 은퇴한 package가 계속 발견 가능하고, link 없는 package를 조용히 삭제할
수 없으며, archive가 파일 수가 아니라 은퇴 횟수에 비례해 증가하고, 기록이 그것을
만든 packet보다 오래 남습니다.

부정적: 모든 은퇴에 추적 파일 하나의 비용이 들고 Stage 99가 tombstone identity를
할당해야 합니다. Stage 98은 단조 증가하므로 은퇴 목록을 훑을 수 있는 곳은 그
index뿐입니다.

폐기: SPEC-0158의 ruling 5와 6. 모든 Tombstone 삭제와 live recovery-navigation
consumer 기준 archive 보존을 요구했습니다.

## Compliance

- `tests/lib/document_governance/test_spec_packages.py`가 기록되지 않은 은퇴는
  실패하고 기록된 은퇴는 통과함을 증명합니다.
- `python3 scripts/validation/check-document-metadata.py --mode check-contracts`가
  Tombstone이 존재하는 상태에서 violation 0을 보고합니다.

## Traceability

- [REQ-0026 문서 보존 및 은퇴](../../01.requirements/0026-document-retention-and-retirement.md)
- [AD-0030 문서 lifecycle 거버넌스 아키텍처](../descriptions/0030-document-lifecycle-governance.md)
- [문서 보존 및 은퇴 정책](../../00.agent-governance/policies/documentation-protocol.md)

## Related Documents

- [ADR-0029 Workspace governance authority](0029-workspace-governance-authority.md)
