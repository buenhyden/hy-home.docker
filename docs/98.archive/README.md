---
title: "98.archive"
version: "1.2.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "archive"
---

# 98.archive

## Overview

Stage 98은 활성 스테이지를 떠난 durable outcome, 대체 문서, 철회 문서를
보관합니다. 보존 대상으로 선택된 기록은 파일로 존재하므로 읽고 검증할 수
있습니다. Stage 03의 Plan과 Task는 outcome이 completed Spec 또는 다른 current
owner로 이전되고 current consumer가 없으면 exact Git regular blob으로 복구하는
transient 실행 운반체이며, 별도 보존본을 만들지 않습니다.

Stage 98은 현재 규칙이나 구현 지침을 소유하지 않습니다. 여기 있는 어떤
문서도 `docs/00.agent-governance/`, `docs/01.requirements/`,
`docs/02.architecture/`, `docs/03.specs/`, `docs/05.operations/`의 현재 규칙을
덮어쓰지 않습니다.

## Scope

Stage 98에는 두 종류가 있고, 이 둘을 섞지 않는 것이 이 스테이지의 유일한
구조 규칙입니다.

**결정의 기록** — 무슨 일이 왜 일어났는지를 담고, 본문은 담지 않습니다.

| 폴더 | 기록하는 사건 | 담는 것 | 담지 않는 것 |
| --- | --- | --- | --- |
| `migrations/` | 승인된 대규모 경로·권한 이동 | source/target 매핑, `MIG-####` | 이동된 문서의 본문 |
| `tombstones/` | 문서의 **철회** | 철회 사유, 대체 대상 또는 `none`, 검증 커밋, `tomb-<id>` | 본문, blob digest, line-number SHA, snapshot |

**보존된 본문** — 문서가 무엇이라 말했는지를 담고, 처분 사유는 담지 않습니다.

| 폴더 | 보존 사유 | 짝이 되는 결정 기록 |
| --- | --- | --- |
| `completed/` | 변경 패키지의 Spec outcome이 완료됨 | 없음 — `status: completed`가 자기 서술 |
| `superseded/` | 더 새로운 문서로 대체됨 | 없음 — `superseded_by`가 자기 서술 |
| `retired/` | 철회됨 | `tombstones/`의 해당 Tombstone |

철회만 결정 기록을 따로 요구합니다. 문서는 자신이 왜 철회되었는지 말하지
않으므로 그 사실은 어디에도 남지 않습니다. 완료와 대체는 문서 자신의
frontmatter가 이미 말합니다.

`README.md`는 이 스테이지에서 유일하게 현재 유효한 문서이며 보존 기록이
아닙니다.

## Structure

```text
98.archive/
├── README.md
├── migrations/
│   └── 0001-<slug>.md
├── tombstones/
│   └── <original-stage>/
│       └── 0001-<slug>.md
├── completed/
│   └── <original-stage>/<원래 경로 그대로>
├── superseded/
│   └── <original-stage>/<원래 경로 그대로>
└── retired/
    └── <original-stage>/<원래 경로 그대로>
```

보존 기록의 경로는 원래 경로에서 선행 루트만 바꾼 것이며, 그 매핑은
`preserved_origin_path()`가 소유합니다. `docs/` 재편 이전에 철회된 문서는
당시 루트(`archive/`)를 경로에 그대로 유지합니다.

## Audience

운영자, 리뷰어, AI agent가 "이 문서는 왜 사라졌는가"와 "그 문서는 무엇이라
말했는가"를 조회할 때 사용합니다.

## How to Work in This Area

1. **처분은 경로가 결정합니다.** 보존 기록의 `status`는 삭제 당시 값 그대로이며
   처분을 뜻하지 않습니다. 현재 `retired/` 104건 중 49건이 `status: active`를
   담고 있습니다. 어떤 기록이 철회된 것인지는 `retired/` 아래에 있다는 사실과
   해당 Tombstone이 결정하며, frontmatter가 결정하지 않습니다.
2. **보존 기록은 수정하지 않습니다.** 삭제 또는 이동 당시 본문과
   byte-identical해야 하고, 현재 계약에 맞추기 위한 편집은 보존하려던 대상을
   훼손합니다. 그래서 이 기록들은 frontmatter가 관리되지 않는 프로파일로
   등록되며, 104건 중 83건은 타입 분류 체계 이전 문서라 `type`이 없습니다.
   자동 포맷터도 예외가 아닙니다. `.markdownlint-cli2.yaml`은 `fix: true`로
   동작하므로 `completed/`, `superseded/`, `retired/` 세 하위 트리를 ignore에
   두어야 하며, 그러지 않으면 all-files 실행이 보존 본문을 조용히 다시
   씁니다. 저작 기록인 `migrations/`와 `tombstones/`는 계속 lint 대상입니다.
3. **철회는 두 기록이 짝을 이룹니다.** Tombstone 하나와 보존본 하나가 서로를
   가리키며, 한쪽만으로는 근거가 되지 않습니다. 짝은 Tombstone의
   `Retired Path`와 보존본의 원래 경로가 일치하는지로 확인합니다.
4. 대규모 이동은 해당
   [Migration](migrations/0003-workspace-governance-simplification.md)의
   source/target mapping으로 찾습니다.
5. `python3 scripts/validation/check-document-corpus-lifecycle.py`로 migration,
   tombstone, frozen preserved body, decision link, recovery blob을 한 번에
   검증합니다. 이 CLI는 별도 `--mode`를 제공하지 않습니다.
6. **Stage 03 completion은 Spec outcome을 보존합니다.** Plan/Task를 제거하기
   전에 current consumer cutover와 exact Git regular-blob recovery를 증명합니다.
   기존 `completed/` 아래의 Plan/Task는 이미 frozen인 legacy evidence이므로
   수정하거나 일괄 정리하지 않습니다.

활성 문서는 `completed/`와 `superseded/` 보존본을 역사적 증거로 직접 링크할
수 있습니다. 이때 같은 문맥에서 현재 권위를 소유하는 Stage 00/01/02/05
문서를 함께 연결해야 합니다. `retired/` 보존본, Tombstone, Migration은 현재
권위의 의존성이 아니며 이 README 또는 관련 Migration을 통해 탐색합니다.

## Related Documents

- [문서 보존 및 은퇴 정책](../00.agent-governance/policies/documentation-protocol.md)
- [REQ-0026 문서 보존 및 은퇴](../01.requirements/0026-document-retention-and-retirement.md)
- [AD-0030 문서 Lifecycle 거버넌스](../02.architecture/descriptions/0030-document-lifecycle-governance.md)
