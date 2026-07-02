---
status: draft
---

<!-- Target: docs/98.archive/<original-stage>/<original-path>.md -->

# Archive Tombstone: {original document title}

> Rules:
>
> - Target-relative links in `## Related Documents` are calculated from the copied tombstone path, not from `docs/99.templates/`.
> - Replace example links with real target-relative links, or delete unused examples before saving.
> - Do not preserve the original stale body in the archive tombstone.

## Overview

이 문서는 현재 구현과 상충하거나 active chain에서 제거된 문서의 tombstone입니다.
원문 본문은 stale current-truth로 재노출하지 않습니다.

## Archive Metadata

| Field | Value |
| --- | --- |
| Archived from | `<original-path>` |
| Archived on | `YYYY-MM-DD` |
| Archive reason | `<short reason>` |
| Current replacement | `<current active document or N/A>` |

## Current Replacement

현재 판단 기준으로 사용할 문서 또는 구현 경로를 명시합니다.

## Archive Ledger

- Original path: `<original-path>`
- Disposition: archived tombstone
- Body policy: stale original body removed

## Related Documents

- [docs archive index](../98.archive/README.md)
