---
status: archived
layer: archive
---

<!-- Target: docs/98.archive/05.operations/guides/05-messaging/ksql-streaming.md -->

# Archive Tombstone: ksqlDB Streaming Operations

## Overview

이 문서는 현재 구현과 상충하거나 active chain에서 제거된 문서의 tombstone입니다.
원문 본문은 stale current-truth로 재노출하지 않습니다.

## Archive Metadata

| Field | Value |
| --- | --- |
| Archived from | `docs/05.operations/guides/05-messaging/ksql-streaming.md` |
| Archived on | `2026-06-04` |
| Archive reason | ksqlDB는 현재 `05-messaging` 구현이 아니라 `infra/04-data/analytics/ksql` 및 `04-data/analytics` operations 문서가 소유한다. |
| Current replacement | `docs/05.operations/guides/04-data/analytics/ksqldb.md` |

## Current Replacement

현재 ksqlDB 사용, policy, runbook 기준은 `04-data/analytics`의 ksqlDB 문서를 따른다.
Kafka dependency와 Schema Registry dependency는 replacement 문서의 current compose boundary에서 확인한다.

## Archive Ledger

- Original path: `docs/05.operations/guides/05-messaging/ksql-streaming.md`
- Disposition: archived tombstone
- Body policy: stale original body removed

## Related Documents

- [docs archive index](../../../README.md)
- [Current ksqlDB guide](../../../../05.operations/guides/04-data/analytics/ksqldb.md)
