---
title: "98.archive"
version: "2.4.3"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
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
선택의 근거는 [ADR-0036](../02.architecture/decisions/0036-archive-occupancy-citation-and-frozen-identity.md)이
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

인용 가능성은 이름에서 도출되며 따로 규정되지 않습니다. retention class는 자기
본문이 여전히 독자를 현재 권위로 이끌 때만 인용할 수 있습니다. `completed`는
Promotion 선언을 통해, `resolved`는 교정 작업 owner를 통해 그렇게 합니다.
`superseded` 본문은 자신을 대체한 문서를 이름으로 가지므로 인용은 그 후속에
둡니다. 대체된 규칙을 인용하는 것이 그 규칙이 되살아나는 방식이기 때문입니다.
`retired`는 가리키는 대상이 없으므로 인용하면 독자가 철회된 규칙에 머뭅니다.

어느 family의 Stage 98 기록도 두 번째 복구 원장을 담지 않습니다. redirect, path
ledger, 자체 설계한 본문 digest, branch SHA, recovery commit이 그것입니다.
catalog의 Retention Envelope가 source Git object를 한 번 이름으로 가지며, frozen
내용의 복구는 일반 Git history가 담당합니다.

`README.md`는 이 스테이지에서 유일하게 현재 유효한 문서이며 보존 기록이
아닙니다.

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

현재 강제는 `check-document-links.py`의 `active-archive-link`가 담당합니다.
Stage 98 문서끼리의 상호 참조는 이 규칙의 대상이 아닙니다.

### Git-history-only 처분

Git-history-only로 등록된 profile은 없습니다. 그런 profile이 등록되기 전까지 모든
처분은 frozen 본문을 유지하며, 보존해야 할 본문을 Git-only 상태로 남기는 것은
보존의 대안이 되지 않습니다.

새 기록은 등록된 template과 check를 만족합니다. 이미 봉인된 Tombstone과 Migration은
기록 당시 형태를 역사로 유지하며, 새 계약에 맞추려고 다시 쓰지 않습니다.

## Retention Catalog

보존 단위 하나가 한 행입니다. 단위는 Spec package 디렉터리, Incident bundle
디렉터리, 또는 단독 문서입니다. `Record`는 `docs/98.archive/` 아래 단위 경로이며
package와 bundle은 `/`로 끝납니다. `Class`는 처분 디렉터리이고, `Names`는 그
class가 이름으로 가져야 하는 값이며, `Source`는 이 모델이 허용하는 유일한 source
Git object입니다. 이동하는 변경은 자기 commit을 이름으로 가질 수 없으므로 source가
존재하던 base commit을 적습니다.

| Record | Class | Names | Source |
| --- | --- | --- | --- |
| `superseded/02.architecture/decisions/0033-full-spec-package-preservation.md` | superseded | ADR-0035 | `677a6e5135de8af1faa9110f912f2452972abf22:docs/02.architecture/decisions/0033-full-spec-package-preservation.md` |
| `completed/03.specs/0177-archive-disposition-enforcement/` | completed | ADR-0035 | `9e120c6fc22d6ddb0ff33e878341b8fdcfa73bd0:docs/03.specs/0177-archive-disposition-enforcement` |
| `superseded/02.architecture/decisions/0035-stage-98-retention-classes-and-route-dispositions.md` | superseded | ADR-0036 | `ea8623eaf04efa5b4f32d538cb3dc0e5235831e0:docs/02.architecture/decisions/0035-stage-98-retention-classes-and-route-dispositions.md` |
| `completed/03.specs/0178-archive-occupancy-citation-and-frozen-identity/` | completed | ADR-0036 | `3c5db48cbae8edfccfa1b0a56ad9421e6b1ccafd:docs/03.specs/0178-archive-occupancy-citation-and-frozen-identity` |
| `superseded/90.references/research/0081-roadmap/README.md` | superseded | RES-0002 | `bb43abb5e0894f45d1179a60770d489a0da41e7c:docs/90.references/research/0081-roadmap/README.md` |
| `retired/05.operations/catalog/09-tooling/0067-syncthing/guide.md` | retired | Syncthing was removed from the active service inventory; no successor exists. | `d1e6ded52808b02392c52472d5416518a3b959d6:docs/05.operations/catalog/09-tooling/0067-syncthing/guide.md` |
| `retired/05.operations/catalog/09-tooling/0067-syncthing/policy.md` | retired | Syncthing was removed from the active service inventory; no successor exists. | `d1e6ded52808b02392c52472d5416518a3b959d6:docs/05.operations/catalog/09-tooling/0067-syncthing/policy.md` |
| `retired/05.operations/catalog/09-tooling/0067-syncthing/runbook.md` | retired | Syncthing was removed from the active service inventory; no successor exists. | `d1e6ded52808b02392c52472d5416518a3b959d6:docs/05.operations/catalog/09-tooling/0067-syncthing/runbook.md` |
| `superseded/05.operations/catalog/04-data/0023-minio/guide.md` | superseded | GDE-0024 | `988059fe898fe739a2eb420f5370eba346568295:docs/05.operations/catalog/04-data/0023-minio/guide.md` |
| `superseded/05.operations/catalog/04-data/0023-minio/policy.md` | superseded | POL-0024 | `988059fe898fe739a2eb420f5370eba346568295:docs/05.operations/catalog/04-data/0023-minio/policy.md` |
| `superseded/05.operations/catalog/04-data/0023-minio/runbook.md` | superseded | RUN-0024 | `988059fe898fe739a2eb420f5370eba346568295:docs/05.operations/catalog/04-data/0023-minio/runbook.md` |
| `superseded/05.operations/catalog/03-security/0016-vault/guide.md` | superseded | GDE-0085 | `a797331dce2f4da089f50e8a73eea525b1445955:docs/05.operations/catalog/03-security/0016-vault/guide.md` |
| `superseded/05.operations/catalog/03-security/0016-vault/policy.md` | superseded | POL-0085 | `a797331dce2f4da089f50e8a73eea525b1445955:docs/05.operations/catalog/03-security/0016-vault/policy.md` |
| `superseded/05.operations/catalog/03-security/0016-vault/runbook.md` | superseded | RUN-0085 | `a797331dce2f4da089f50e8a73eea525b1445955:docs/05.operations/catalog/03-security/0016-vault/runbook.md` |

이 catalog가 생기기 전에 보존된 기록은 당시 계약이 요구한 철회 기록을 그대로
유지합니다. 소급 적재는 하지 않습니다.

## Structure

```text
98.archive/
├── README.md
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
   객체와 구성원 경로, Git 파일 mode, frontmatter 이후 본문 바이트가 같아야 하며,
   frontmatter는 Registry의 `common.frozen_transition_fields`가 나열한 필드만 값이
   달라지고 `superseded_by`만 추가될 수 있습니다.
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
- [ADR-0036 보존 대기 package, route 기록 인용, frozen 동일성](../02.architecture/decisions/0036-archive-occupancy-citation-and-frozen-identity.md)
- ADR-0035 Stage 98 보존 class와 route 처분 (superseded)
