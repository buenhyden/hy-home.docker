---
title: "Data Packages"
version: "2.0.1"
type: "reference/category-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
layer: "references"
created: "2026-07-02"
---

# Data Packages

## Overview

저장소 인벤토리, 생성된 navigation 산출물, 구조화된 데이터셋, 용어집,
안정적인 참고 사실입니다.

Stage 90 authority boundary와 package lifecycle 규칙은
[References index](../README.md)와 Stage 99 Registry가 정의합니다.

현재 tree가 package 집합을 정의합니다: package는 README가 존재하고 자신의
Stage 99 profile을 만족할 때 존재합니다. 필요한 의미를 canonical owner로
옮기고 모든 inbound consumer를 갱신하고 아래 표의 행을 제거하고
Tombstone을 기록하는 같은 변경에서 제거되어 은퇴합니다. 은퇴한
`DATA-` 번호는 다시 발급하지 않습니다.

## Packages

이 범주는 package를 보유하지 않습니다.

열세 개 package가 2026-09-10에 은퇴했습니다. SPEC-0173은 이 범주가 따르는
규칙을 명시합니다: Stage 90 데이터는 "현재 consumer가 존재하는 동안만
현재성을 유지한다." 이 package들을 살아 있게 만들던 모든 consumer,
곧 등록된 generator, freshness gate, 해당 경로를 적어 두던 metadata
allow-list가 같은 변경에서 제거되어 더 이상 읽는 이가 남지 않았습니다.
보존된 각 본문은 `docs/98.archive/retired/90.references/data/` 아래에
있으며 tombstone으로 기록됩니다.

DATA-0067은 남은 consumer가 독자가 아니었던 유일한 package였습니다:
lifecycle gate가 그 `data.yaml`을 Migration 0003 복구 blob과 byte 단위로
비교합니다. 같은 승인 아래 Migration 행이 보존된 경로를 다시 가리키도록
바뀌었고, payload는 byte 그대로 보존되었으므로 비교는 같은 byte에 대해
같은 동등성을 증명합니다.

이곳의 새 package는 만들기 전에 현재 consumer가 먼저 지정되어야 하며,
만든 뒤에 지정해서는 안 됩니다.

## Authoring

package는 `data/####-<slug>/` 아래에만 만들고, 대응하는 Stage 99
템플릿을 사용합니다. 관찰 날짜, 인용, provenance, 활성 owner
Traceability를 보존합니다.

## Related Documents

- [References index](../README.md)
- [Stage 99 Registry](../../99.templates/registry.json)
