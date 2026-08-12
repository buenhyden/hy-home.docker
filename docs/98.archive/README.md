---
layer: archive
---

# 98.archive

> 승인된 typed Stage 98 기록의 단일 대상이며, current guidance나 일반 본문
> 저장소가 아닙니다.

## Overview

`docs/98.archive/`는 완료된 change evidence, 제거된 문서의 간결한 provenance
tombstone, 그리고 승인된 migration ledger를 stable identity로 보존합니다.
Active 문서는 Stage 98을 현재 지침으로 소비하지 않으며, 현재 판단은 각 active
stage의 canonical artifact를 따릅니다.

## Audience

- Documentation Writers
- AI Agents
- Repository Maintainers

## Scope

### In Scope

- `changes/chg-<id>-<slug>/plan.md`와 `task.md`로 보존하는 완료 change evidence
- `tombstones/<stage>/<stable-id>-<slug>.md`의 concise provenance record
- `migrations/mig-<id>-<slug>.md`의 승인된 source-to-target disposition ledger
- 검증된 Git provenance, preservation metadata, replacement relation

### Out of Scope

- 현재 판단 기준으로 사용하는 requirement, architecture, spec, plan, task, policy
- 제거된 문서의 전체 본문을 tombstone에 복제하는 행위
- source stage 구조를 그대로 복제하는 archive directory
- active 문서의 Related Documents 대상

## Structure

```text
98.archive/
├── changes/
│   └── chg-<id>-<slug>/
│       ├── plan.md
│       └── task.md
├── tombstones/
│   └── <stage>/
│       └── <stable-id>-<slug>.md
├── migrations/
│   └── mig-<id>-<slug>.md
└── README.md
```

## Current Inventory

Task 7 기준 `changes/`에는 146개 change packet과 234개 typed document가
있습니다. 이 가운데 88개 packet은 Plan/Task pair, 14개는 ledger가 승인한
Plan-only disposition, 44개는 ledger가 승인한 Task-only disposition입니다.
`tombstones/`에는 38개 retired-document tombstone이 있습니다: `03.specs/` 28개,
`05.operations/` 10개입니다. 각 기록은 원문 본문 대신 검증된 source path와
Git provenance만 보존합니다. `migrations/`에는 authoritative `mig-0001` ledger
한 건이 있습니다.

각 물리 문서는 다음 profile 중 정확히 하나를 사용합니다.

- `change-plan`: `changes/chg-<id>-<slug>/plan.md`
- `change-task`: `changes/chg-<id>-<slug>/task.md`
- `tombstone`: `tombstones/<stage>/<stable-id>-<slug>.md`
- `migration`: `migrations/mig-<id>-<slug>.md`

정확한 disposition과 source provenance는
[mig-0001](migrations/mig-0001-sdlc-taxonomy-convergence.md)이 소유합니다.
과거의 날짜 기반 실행·archive 경로와 repository-root `archive/` 경로는 routing
target이 아니며 Git history와 migration ledger로만 조회합니다. 새 archive
identity는 `chg-`, `mig-`, 또는 stage-appropriate tombstone identity를 사용하고,
날짜는 `archived_at` 같은 typed provenance key에 둡니다.

## Non-Authoritative Historical Provenance Ledger

This hand-maintained, non-authoritative compatibility section is intentionally
empty after the typed migration and is not routing. Historical source-to-target
facts are owned by `mig-0001`. The retired `docs/98.archive/04.execution/`
location is recorded here only as provenance and is not routing.

### End Non-Authoritative Historical Provenance Ledger

## How to Work in This Area

1. 승인된 migration row와 source Git object를 먼저 검증합니다.
2. Change evidence는 ledger가 지정한 동일 `chg-<id>` packet에 배치합니다.
3. Tombstone에는 retired body를 복제하지 않고 typed provenance만 기록합니다.
4. Active consumer를 canonical active target으로 이동한 뒤 archive record를 만듭니다.
5. Lifecycle, metadata, active-to-archive link gate를 모두 통과시킵니다.

## Related Documents

- [docs index](../README.md)
- [stage authoring matrix](../00.agent-governance/rules/stage-authoring-matrix.md)
- [archive and retention contract](../99.templates/support/archive-retention-contract.md)
- [document corpus migration contract](../99.templates/support/corpus-migration-contract.md)
- [archive template](../99.templates/templates/common/archive.template.md)
