---
title: "98.archive"
version: "2.5.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-28"
layer: "archive"
---

# 98.archive

## Overview

Stage 98은 활성 스테이지가 더 이상 담지 않는 것을 여섯 처분으로 보존합니다.
각 처분은 자기 디렉터리를 가지며, 그 디렉터리는 해당 처분을 처음 쓰는 변경이
만듭니다. 기록이 아직 없는 처분에는 디렉터리가 없습니다. 처분은 두 종류로
나뉘고, 종류가 디렉터리에 담기는 것과 현재 문서가 그것을 인용할 수 있는지를
정합니다.

이 README는 archive 탐색과 작업 안내만 소유합니다. 보존 정책은
[.agents](../../.agents/governance/documentation-protocol.md#stage-98-dispositions)가,
경로와 profile 계약은 [Stage 99 Registry](../99.templates/registry.json)가,
선택의 근거는 [ADR-0037](../02.architecture/decisions/0037-package-disposition-wait-and-task-cancellation.md)이
소유합니다. 여기 보존된 어떤 기록도 `.agents/`와 Stage 01·02·03·05의 현재
규칙을 덮어쓰지 않습니다.

## Scope

**Retention class**는 한때 현재였던 전체 본문을 당시 profile 그대로 보존합니다.
더 이상 현재가 아닌 governed 문서는 Stage 01, 02, 03, 05, 90, 99를 떠나 자신에게
일어난 일에 맞는 class에 보존됩니다. 보존은 profile을 따릅니다. frozen 본문은
불변이고, Git-history-only 처분은 호환 사본 없이 복구 가능한 출처를 유지합니다.
처분에는 별도 승인이 필요합니다.

| Class | 담는 것 | 이름으로 가져야 하는 것 | 활성 스테이지에서 인용 |
| --- | --- | --- | --- |
| `completed/` | 끝나서 반영된 작업 | 그것이 승격한 대상 | 가능 |
| `superseded/` | 새 현재 권위가 대체한 내용 | 그것을 대체한 문서 | 불가, 후속을 인용 |
| `retired/` | 후속 없이 철회된 규칙이나 범위 | 철회 사유 | 불가 |
| `resolved/` | 종료된 Incident bundle과 게시된 Postmortem | 종료 근거와 현재 교정 작업 owner | 역사적 증거로 가능 |

**Route disposition**은 본문을 담지 않습니다. 저장소 밖 consumer를 위한 route를
이름으로 가지므로, 현재 문서는 그 기록이 아니라 현재 route를 인용합니다.

| Family | 담는 것 | 이름으로 가져야 하는 것 | 활성 스테이지에서 인용 |
| --- | --- | --- | --- |
| `tombstones/` | 없음 | 은퇴한 route, 그 후속 또는 부재, 사유 | 불가 |
| `migrations/` | 없음 | 이동한 범위와 현재 owner, `MIG-####` | 불가 |

인용 가능성은 이 저장소의 보존·인용 정책과 등록된 검증 판정을 따릅니다.
retention class는 자기 본문이 여전히 독자를 현재 권위로 이끌 때만 인용할 수
있다는 정책상의 구분입니다. `completed`는
Promotion 선언을 통해, `resolved`는 교정 작업 owner를 통해 그렇게 합니다.
`superseded` 본문은 자신을 대체한 문서를 이름으로 가지므로 인용은 그 후속에
둡니다. 대체된 규칙을 인용하는 것이 그 규칙이 되살아나는 방식이기 때문입니다.
`retired`는 가리키는 대상이 없으므로 인용하면 독자가 철회된 규칙에 머뭅니다.

기존 Task 본문에 이미 있던 Commit Ledger와 검증 revision은 원래 실행 증거이므로
그대로 보존합니다. 아래의 두 번째 복구 원장 금지는 그 증거를 삭제하라는 뜻이
아닙니다.

어느 family의 Stage 98 기록도 두 번째 복구 원장을 담지 않습니다. redirect, path
ledger, 자체 설계한 본문 digest, branch SHA, recovery commit이 그것입니다.
[Retention Catalog](retention-catalog.md)의 Retention Envelope가 source Git
object를 한 번 이름으로 가지며, frozen 내용의 복구는 일반 Git history가
담당합니다.

이 스테이지에서 현재 유효한 문서는 이 `README.md`와
[`retention-catalog.md`](retention-catalog.md) 둘뿐이며, 둘 다 보존 기록이
아닙니다. README는 탐색만 맡고, 보존 단위의 행은 Retention Catalog 기록이
소유합니다.

### 외부 참조 경계

`docs/` 안의 문서 간 링크는 기존 계약을 유지하며, 프로그램이 여는 machine
reference는 링크가 아닙니다. 문서는 이 index와, 자기 본문이 여전히 독자를 현재
권위로 이끄는 retention class를 넘어 `docs/98.archive/`로 링크하지 않습니다. 그
class는 Promotion 선언을 통한 `completed/`와, 교정 작업 owner를 통해 역사적
증거가 되는 `resolved/`입니다. `superseded/` 본문 대신 후속을, `retired/` 본문,
Tombstone, Migration 대신 현재 route를 인용합니다. 여전히 이름을 불러야 하는
frozen 기록은 식별자로 부르고 이 index를 통해 찾습니다.

보존본을 직접 인용할 수 있는 것은 `operation/incident` 기록과 그
`operation/postmortem`뿐입니다. 그런 기록이 근거로 삼는 증거는 보존된 기록 자체인
경우가 많기 때문입니다. 다만 route 기록은 본문을 담지 않아 그 예외가 닿을 대상이
없으므로, `tombstones/`와 `migrations/`는 출발 profile과 무관하게 인용할 수
없습니다.

현재 강제는 `check-document-links.py --mode alignment`의
`active-archive-link` 판정이 담당하며 `--mode all`에도 포함됩니다.
허용된 보존본 링크는 당시의 실행·사건 증거를 찾는 경로이며 현재 규칙이나 실행
승인을 대신하지 않습니다. 현재 평가의 withdrawn·invalidated와 이력 전용 이용 가능성은 Incident 예외보다
먼저 차단합니다. 보존 원문의 링크는 원래 commit/path에서 검사합니다. 기존 세대의
역사 링크 오류·출처 부재는 명시적인 관찰이며, 새 정확 포착의 오류는 실패입니다.

### Git-history-only 처분

`common.archive_retention`은 보존 단위의 이용 가능성 `retained`와
`git-history-only`를 등록합니다. 실제 재평가는 기존 카탈로그의 선택 영역
`Current Assessments`에만 기록하며, 행이 없으면 `unreviewed`/`retained`입니다.
현재 평가는 포착 당시의 status와 별개이며 옛 원문을 다시 쓰지 않습니다.

이력 전용 전환에는 단위·행위·시점을 특정한 별도 승인, hold 부재, 원본 객체의
복구 가능성, 현재 소비자 정리와 전체 단위 부재가 모두 필요합니다. 결정은 당시
Task revision의 승인 상태·범위·본문 증거로 검증합니다. 포착 행과 평가 행은
제거 후에도 남으며, 본문 대신 카탈로그를 안내합니다. `purged`는 지원하지 않습니다.
이 README와 일반 표준 채택은 어떤 실제 제거도 승인하지 않습니다.

새 기록은 등록된 template과 check를 만족합니다. 이미 봉인된 Tombstone과 Migration은
기록 당시 형태를 역사로 유지하며, 새 계약에 맞추려고 다시 쓰지 않습니다.

## Structure

```text
98.archive/
├── README.md
├── retention-catalog.md
├── completed/
│   └── <original-stage>/<원래 경로 그대로>
├── superseded/
│   └── <original-stage>/<원래 경로 그대로>
├── retired/
│   └── <original-stage>/<원래 경로 그대로>
├── tombstones/
│   └── <original-stage>/
│       └── 0001-<slug>.md
└── migrations/
    └── 0001-<slug>.md
```

`resolved/`는 첫 종료 Incident를 보존하는 변경이 만들기 전까지 존재하지
않습니다. 보존 기록의 경로는 원래 경로에서 선행 루트만 바꾼 것이며, 그 매핑은
`preserved_origin_path()`가 소유합니다. `docs/` 재편 이전에 철회된 문서는 당시
루트(`archive/`)를 경로에 그대로 유지합니다.

## Audience

운영자, 리뷰어, AI agent가 "이 문서는 왜 사라졌는가"와 "그 문서는 무엇이라
말했는가"를 조회할 때 사용합니다.

## How to Work in This Area

1. **처분은 경로가 결정합니다.** 보존 기록의 `status`는 이동 당시 값 그대로이며
   처분을 뜻하지 않습니다. 어떤 기록이 철회된 것인지는 `retired/` 아래에 있다는
   사실이 결정하며, frontmatter가 결정하지 않습니다.
2. **보존 기록은 수정하지 않습니다.** catalog 행이 있는 단위는 그 행의 `Source`
   객체와 구성원 경로, Git 파일 mode, 전체 blob 바이트가 같아야 합니다.
   Registry에 고정된 기존 포착 세대와 ADR-0036 최초 전환에만 종전의 제한된
   lifecycle 필드 비교를 유지합니다. Git 객체·index와 checkout 개행 표현을
   구분하며 외부 filter나 renormalize로 원문을 맞추지 않습니다.
   현재 계약에 맞추기 위한 편집은 보존하려던 대상을 훼손합니다. 그래서 이
   기록들은 frontmatter가 관리되지 않는 보존 프로파일로 등록됩니다. 자동
   포맷터도 예외가 아닙니다. `.markdownlint-cli2.yaml`은 `fix: true`로 동작하므로
   `completed/`, `superseded/`, `retired/` 세 하위 트리를 ignore에 두어야 하며,
   `resolved/`도 그것을 만드는 변경이 ignore에 추가합니다. 저작 기록인
   `migrations/`와 `tombstones/`는 계속 lint 대상입니다. 다만 Registry가 frozen
   legacy status로 등록한 다음 세 migration은 보존된 예외이며 lint에서
   제외합니다: `migrations/0001-sdlc-taxonomy-convergence.md`,
   `migrations/0002-operations-catalog-convergence.md`,
   `migrations/0003-workspace-governance-simplification.md`.
3. **처분에는 별도 승인이 필요합니다.** 완료, 대체, 철회, 종료 어느 것도 다른
   작업의 부수효과로 일어나지 않습니다.
4. 철회를 기록하는 변경은 `retired/` 보존본 하나와 그 단위의 철회 기록 하나를
   함께 만듭니다. 새 철회의 기록은 Retention Catalog 행이며, 봉인된 Tombstone과
   짝을 이루는 기존 보존본은 그 짝을 철회 기록으로 유지합니다. corpus check는
   Tombstone의 `Retired Path`와 보존본의 원래 경로가 일치하는지로 그 짝을
   확인합니다.
5. 과거의 대규모 이동은 해당 Migration의 source/target mapping으로 찾습니다.
   Migration은 인용 대상이 아니므로 이 index에서 식별자로 찾습니다.
6. `python3 scripts/validation/check-document-corpus-lifecycle.py`로 migration,
   tombstone, frozen preserved body, decision link, recovery blob을 한 번에
   검증합니다. 이 CLI는 별도 `--mode`를 제공하지 않습니다.

> Historical evidence (not current authority; source: Git history):
> ADR-0031 채택 시 보존된 철회 문서 104건 중 49건은 `status: active`,
> 83건은 `type` 없이 남아 있었습니다. 이는 당시 원문을 보존한 결과이며
> 현재 인벤토리 수나 작성 기준이 아닙니다.

## Related Documents

- [문서 보존 및 은퇴 정책](../../.agents/governance/documentation-protocol.md)
- [REQ-0026 문서 보존 및 은퇴](../01.requirements/0026-document-retention-and-retirement.md)
- [AD-0030 문서 Lifecycle 거버넌스](../02.architecture/descriptions/0030-document-lifecycle-governance.md)
- [ADR-0037 Package Waiting, Cancellation and Archive Reassessment](../02.architecture/decisions/0037-package-disposition-wait-and-task-cancellation.md)
- ADR-0035 Stage 98 보존 class와 route 처분 (superseded)
