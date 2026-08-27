---
profile_id: readme
status: active
layer: archive
---

# 98.archive

## Overview

Stage 98은 폐기된 안정 경로와 대규모 권위 이동을 찾기 위한 최소 역사
인덱스입니다. 전체 과거 본문은 Git history가 보관하며, 이 Stage는 현재 SDLC
규칙이나 구현 지침을 소유하지 않습니다.

## Scope

- `migrations/`: 승인된 대규모 경로·권위 이동의 매핑
- `tombstones/`: 삭제된 안정 경로의 최소 복구 포인터
- `README.md`: 조회 절차와 권위 경계

Stage 98은 `docs/00.agent-governance/`, `docs/01.requirements/`,
`docs/02.architecture/`, `docs/03.specs/`, `docs/05.operations/`의 현재 규칙을
덮어쓰지 않습니다. Superseded ADR은 Stage 02 decision log에 남으며
Tombstone으로 이동하지 않습니다.

## Structure

```text
98.archive/
├── README.md
├── migrations/
│   └── 0001-<slug>.md
└── tombstones/
    └── <original-stage>/
        └── 0001-<slug>.md
```

경로의 유형 접두사는 제거하지만 `mig-####`, `tombstone-####` 안정 ID는
frontmatter에 유지합니다. 날짜는 파일명에 넣지 않습니다.

## How to Work in This Area

1. 대규모 이동은 해당 [Migration](migrations/0003-workspace-governance-simplification.md)의
   source/target mapping으로 찾습니다.
2. Tombstone은 `Retired Path`, `Replacement` 또는 `none`, `Reason`, `status`,
   `Recovery Commit`만을 복구 근거로 사용합니다.
3. 완료된 change packet 본문은 이 디렉터리에 복제하지 않습니다. Task 10
   검증기는 삭제 전 frontmatter에 있던 recovery tuple을
   `f259c139fb7da166609029cdd3657de87e639f6b:<former-stage-98-path>`에서 읽습니다.
   기존 tuple이 없었던 controller-reviewed 항목만 같은 commit과 해당 former
   path를 직접 사용합니다.
4. `python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-recovery`
   로 모든 `commit:path`가 regular Git blob인지 다시 증명합니다.

Active 문서는 개별 Tombstone을 직접 링크하지 않고 이 README 또는 관련
Migration을 통해 과거 이동을 조회합니다. Tombstone에는 삭제된 본문,
line-number SHA, blob digest, archive snapshot 또는 snapshot count를 넣지
않습니다. 별도의 감사·법적 보존 요구가 승인되지 않으면 본문 복사본을
추가하지 않습니다.

Migration 0003은 승인된 실행 ledger이므로 Task 10에서 byte-identical하게
유지합니다. 실행형 ledger의 압축은 Task 13만 수행합니다.

## Related Documents

- [Workspace governance simplification Migration](migrations/0003-workspace-governance-simplification.md)
- [Stage 99 document registry](../99.templates/registry.json)
- [Task 10 evidence](../03.specs/0153-workspace-governance-simplification/tasks/tsk-0010-archive.md)
