---
status: archived
artifact_id: ref-0093
artifact_type: archive
parent_ids: []
archived_from: docs/05.operations/policies/07-workflow/airbyte.md
archived_at: '2026-06-02'
archive_reason: Airbyte has no tracked infra implementation under infra/07-workflow/airbyte
  and must not remain an active operations policy.
archive_disposition: duplicate
archived_commit: 681add36981133abda1a380c52234e55a93ecf54
archived_blob: 0154169fd95d7e8e365008315bca4ee8308d6d44
preservation_class: git-history
current_replacement: docs/03.specs/spec-0008-workflow/spec.md
---

# Archive Tombstone: Airbyte Operations Policy

## Overview

이 문서는 현재 구현과 상충해 active operations chain에서 제거된 Airbyte policy tombstone입니다.
원문 운영 정책은 stale current-truth로 재노출하지 않습니다.

## Archive Metadata

| Field | Value |
| --- | --- |
| Archived from | `docs/05.operations/policies/07-workflow/airbyte.md` |
| Archived on | `2026-06-02` |
| Archive reason | Airbyte has no tracked implementation under `infra/07-workflow/airbyte`. |
| Current replacement | [Workflow spec](../../../03.specs/spec-0008-workflow/spec.md) |

## Current Replacement

현재 workflow tier는 Airflow와 n8n 구현을 기준으로 해석합니다. Airbyte 정책은
새 infra 구현이 추가되고 Stage 01-04 chain이 다시 승인될 때 새로 작성해야 합니다.

## Archive Ledger

- Original path: `docs/05.operations/policies/07-workflow/airbyte.md`
- Disposition: archived tombstone
- Body policy: stale original body removed

## Related Documents

- [Archive index](../../README.md)
