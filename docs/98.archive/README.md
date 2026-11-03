---
title: "98.archive"
version: "3.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-03"
layer: "archive"
---

# 98.archive

## Overview

Stage 98은 활성 스테이지를 떠난 문서의 처분 체계를 정의합니다. 현재 이 스테이지는
보존 기록을 담지 않으며, 이 `README.md`만 남아 있습니다.

활성 스테이지에서 문서를 없앨 때는 그 내용을 Stage 01 요구사항과 Stage 02 아키텍처
문서의 Traceability에 요약하고 원본을 삭제합니다. 삭제된 본문의 기록은 Git 이력이며,
폐기된 번호는 [Stage 99 Registry](../99.templates/registry.json)의
`identity_spaces.*.reserved_history`가 보관해 다시 쓰이지 않게 합니다.

처분 정책은 [문서 보존 및 은퇴 정책](../../.agents/governance/documentation-protocol.md)이
소유합니다. 이 README는 탐색과 체계 설명만 맡습니다.

## Scope

- 소유: Stage 98의 처분 분류와 폴더 체계 설명
- 비소유: 처분 정책, 경로와 profile 계약, 폐기 번호 목록
- 어떤 gate도 Stage 98을 검증하지 않으며, 이 README는 다른 README와 같은 문서 검사를
  받습니다.

### Audience

운영자, 리뷰어, AI agent가 "이 문서는 왜 사라졌는가"를 조회할 때 사용합니다. 답은
요약을 받은 Stage 01·02 문서의 Traceability와 Git 이력에 있습니다.

## Structure

### Documents

| Path | Purpose |
| --- | --- |
| `README.md` | 처분 체계 설명 |

처분 분류는 다음과 같습니다. 기록이 없으므로 각 폴더는 지금 존재하지 않습니다.

| 분류 | 뜻 |
| --- | --- |
| `completed/` | 끝나서 반영된 작업 |
| `superseded/` | 새 현재 권위가 대체한 내용 |
| `retired/` | 후속 없이 철회된 규칙이나 범위 |
| `resolved/` | 종료된 Incident와 게시된 Postmortem |
| `tombstones/` | 은퇴한 route의 기록 |
| `migrations/` | 대규모 이동의 기록 |

```text
98.archive/
└── README.md
```

## Usage

1. 문서를 없애는 변경은 먼저 그 내용을 Stage 01·02 문서에 요약합니다.
2. 원본 문서는 삭제합니다. 이 스테이지로 옮겨 보존하지 않습니다.
3. 폐기된 artifact 번호는 Registry의 `reserved_history`에 추가합니다.
4. 삭제된 본문이 필요하면 Git 이력에서 복구합니다.

## Related Documents

- [문서 보존 및 은퇴 정책](../../.agents/governance/documentation-protocol.md)
- [REQ-0026 문서 보존 및 은퇴](../01.requirements/0026-document-retention-and-retirement.md)
- [AD-0030 문서 Lifecycle 거버넌스](../02.architecture/descriptions/0030-document-lifecycle-governance.md)
