---
status: archived
artifact_id: ref-0086
artifact_type: archive
parent_ids: []
archived_from: docs/05.operations/guides/03-security/01.setup.md
archived_at: '2026-06-05'
archive_reason: Duplicate setup guide retained service-local compose startup, direct
  container runtime commands, and generic template residue that conflict with the
  current Vault operations guide.
archive_disposition: duplicate
archived_commit: b9a96ac0995fd665f6b121d69483a5c83300823e
archived_blob: 1e6d8bf109e421dab99cf1b37a0e5a01da1371fe
preservation_class: git-history
current_replacement: docs/05.operations/03-security/ops-0016-vault/guide.md
---

# Archive Tombstone: 03-Security Setup Guide

## Overview

이 문서는 active chain에서 제거한 `03-security` setup guide의 tombstone입니다.
원문 본문은 현재 root compose 검증 경계와 충돌하므로 재노출하지 않습니다.

## Archive Metadata

| Field | Value |
| --- | --- |
| Archived from | `docs/05.operations/guides/03-security/01.setup.md` |
| Archived on | `2026-06-05` |
| Archive reason | Duplicate setup guide retained service-local compose startup, direct container runtime commands, and generic template residue that conflict with the current Vault operations guide. |
| Current replacement | `docs/05.operations/guides/03-security/vault.md` |

## Current Replacement

현재 Vault 사용, AppRole bootstrap, static validation, runtime evidence 기준은
[Vault guide](../../../05.operations/03-security/ops-0016-vault/guide.md)를 사용합니다.

## Archive Ledger

- Original path: `docs/05.operations/guides/03-security/01.setup.md`
- Disposition: archived tombstone
- Body policy: stale original body removed

## Related Documents

- [docs archive index](../../README.md)
- [Vault guide](../../../05.operations/03-security/ops-0016-vault/guide.md)
