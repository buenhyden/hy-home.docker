---
title: 보존 기록으로서의 아카이브
version: 1.0.0
type: sdlc/architecture-decision
layer: architecture
status: active
owner: "@buenhyden"
artifact_id: ADR-0031
parent_ids:
  - AD-0030
created: 2026-09-04
updated: 2026-09-04
supersedes:
  - ADR-0030
---

# ADR-0031: 보존 기록으로서의 아카이브

## Context

ADR-0030은 은퇴를 삭제로 정의하고 Tombstone을 그 복구 포인터로 두었습니다.
채택 근거 중 하나가 "archive가 은퇴한 내용의 두 번째 복제본이 되어서는 안
된다"였고, 본문은 Git history가 보관했습니다.

워크스페이스는 이제 반대 기본값을 요구합니다. 완료된 것, 오래된 것, 폐기된
것은 모두 유지하되 관리 방식을 달리하고, 어느 것도 활성 디렉터리에 남지
않습니다. 이 전제 아래에서 ADR-0030의 결정은 두 가지 결과를 낳습니다. 은퇴
문서 104건은 파일로 존재하지 않아 조회하려면 경로를 미리 알고 Git을 직접
읽어야 했고, 완료 package 21건과 대체 문서 3건은 갈 곳이 없어 활성 스테이지에
남아 있었습니다.

## Decision Drivers

- 보존 여부는 조회 가능성으로 판단합니다. 파일이 아닌 내용은 경로를 아는
  사람만 읽을 수 있습니다.
- 처분 사유와 본문은 서로 다른 사실이며 한쪽이 다른 쪽을 대신하지 못합니다.
- 보존된 기록은 나중 계약에 맞추기 위해 편집되어서는 안 됩니다.
- 활성 스테이지는 현재 작업만 담아야 합니다.

## Options Considered

1. **ADR-0030 유지.** 파일이 늘지 않습니다. 기각: "폐기된 것도 유지"를 만족하지
   못하고, 완료·대체 문서가 활성 스테이지에 남습니다.
2. **본문을 Tombstone에 담기.** 파일 하나로 끝납니다. 기각: Tombstone의 최소
   계약은 본문·blob·snapshot을 금지하며, 그 금지가 Tombstone을 검사 가능한
   고정 형태로 유지합니다.
3. **보존 기록이 처분 사유까지 흡수.** 기록이 자기 서술적이 됩니다. 기각:
   frontmatter를 덧붙이면 삭제 당시 문서와 byte-identical하지 않게 되어 복구
   커밋 대조가 성립하지 않습니다.
4. **처분별 하위 트리에 본문을 보존하고 Tombstone은 철회 기록으로 유지.**
   채택.

## Decision

`docs/98.archive/`는 두 종류를 담습니다. `migrations/`와 `tombstones/`는
결정의 기록이며 본문을 담지 않습니다. `completed/`, `superseded/`,
`retired/`는 문서 본문을 원문 그대로 담으며 처분 사유를 담지 않습니다.

보존 기록의 경로는 원래 경로에서 선행 루트만 바꾼 것이며 `docs/` 재편 이전에
철회된 문서는 당시 루트를 유지합니다. 처분은 경로가 결정하고 보존본의
`status`가 결정하지 않습니다.

철회만 두 기록을 요구합니다. 문서는 자신이 왜 철회되었는지 말하지 않으므로
Tombstone이 그 사실을 담고, 보존본이 문서가 무엇이라 말했는지를 담습니다.
완료와 대체는 `status`와 `superseded_by`가 이미 말하므로 Tombstone을 만들지
않습니다. Tombstone의 `Recovery Commit`은 이제 복구 경로가 아니라 보존본이
제거 당시 문서와 동일함을 증명하는 검증 앵커입니다.

보존 기록은 작성 대상이 아닙니다. frontmatter와 section 계약, 그리고 나가는
link의 해석 가능성은 보존 기록에 적용되지 않습니다. 들어오는 link는 계속
검사됩니다.

## Consequences

- 은퇴 문서 104건이 파일로 복원되었고 각각 기록된 커밋의 blob과
  byte-identical합니다. 그 결과 archive는 이질적입니다. 104건 중 49건이
  `status: active`를, 83건이 `type` 없음을 담고 있으며 이는 제거 당시의
  사실입니다.
- 완료 package 21건과 대체 문서 3건이 활성 스테이지를 떠났습니다.
- `validate_spec_package_lifecycle`은 `preserved_paths`를 함께 받아 완료에
  의한 이탈과 철회에 의한 이탈을 구분합니다. 완료에 Tombstone을 요구하면
  일어나지 않은 철회를 기록하게 됩니다.
- 활성 문서는 보존 기록을 직접 link할 수 있습니다. 그 대상은 실재하는
  파일이기 때문입니다. Tombstone 직접 link는 계속 금지됩니다.
- ADR-0030이 금지했던 "두 번째 복제본"은 이제 의도된 결과입니다. 중복은
  Tombstone의 `Retired Path` 하나이며 그것은 두 기록을 잇는 조인 키입니다.

## Compliance

`python3 scripts/validation/run-ci-gate.py --profile full`이 이 결정을
집행하는 check를 포함합니다.

## Traceability

- [AD-0030 문서 Lifecycle 거버넌스](../descriptions/0030-document-lifecycle-governance.md)
- [REQ-0026 문서 보존 및 은퇴](../../01.requirements/0026-document-retention-and-retirement.md)
- [Stage 98 아카이브](../../98.archive/README.md)

## Related Documents

- [문서 보존 및 은퇴 정책](../../00.agent-governance/policies/documentation-protocol.md)
