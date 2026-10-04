---
title: "Audit Packages"
version: "2.0.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
layer: "references"
created: "2026-07-02"
---

# Audit Packages

## Overview

특정 시점의 gap, 구현, conformance 평가입니다. Audit package는 증거이며
승인 gate가 아닙니다.

Stage 90 authority boundary와 package lifecycle 규칙은
[References index](../README.md)와 Stage 99 Registry가 정의합니다.

## Scope

이 README는 현재 audit package 경로와 보존된 audit route를 안내합니다. 평가의
finding과 후속 조치는 해당 package 또는 이를 소유하는 Stage 03 Task에 남습니다.

SPEC-0158이 이 범주를 은퇴시켰습니다. 현재 tree가 Stage 90 package 집합을
정의합니다: package는 README가 존재하고 자신의 Stage 99 profile을 만족할 때
존재합니다. package는 필요한 의미를 canonical owner로 옮기고 모든 inbound consumer를
갱신하고 아래 표의 행을 제거하는 같은 변경에서 제거되어 은퇴합니다.
archive ledger가 membership을 결정하지 않으므로 package를 은퇴시키는
작업은 더 이상 Stage 99 개정이 아닙니다.

Stage 99 identity는 여전히 한 번만 소비됩니다. 은퇴한 package의 `AUD-`
번호는 `identity-history-regression`이 재발급을 금지하므로 다시 사용하지
않습니다.

Stage 간 audit은 자신을 관장하는 Spec 아래의 Task에 둡니다. 이때 `task`는
`package-member` profile이므로 전역 identity를 발급하지 않습니다.

## Structure

이 범주는 package를 보유하지 않습니다. SPEC-0158이 선언한 은퇴를
완료한 상태입니다.

열네 개 package가 2026-09-10에 은퇴했습니다. 각 package는 독자가 아니라
등록된 consumer 덕분에 살아 있었습니다: 파일명을 매핑하던 criteria 계약,
그 행을 단정하던 semantic-freshness checker, package 디렉터리를 읽던
matrix generator, 그 경로를 이름 붙이던 metadata profile의 path
allow-list입니다. 이 넷 모두 같은 변경에서 제거되었습니다. 보존된 각 본문은
`docs/98.archive/retired/90.references/audits/` 아래에 있으며
`tomb-AUD-0019`부터 `tomb-AUD-0032`까지의 tombstone으로 기록됩니다.

## Dated Historical Snapshots

은퇴한 audit snapshot은 metadata에 자신의 관찰 날짜를 유지하며 현재
package 경로는 날짜를 포함하지 않습니다.

AUD-0097은 2026-09-09에 은퇴했습니다. 네 결함 가운데 세 개는 tree에서
수정되었지만 그동안 네 개의 운영 guide가 여전히 AUD-0097을 미해결 finding의
owner로 링크하고 있었습니다. 남은 한 결함은 이를 소유하는 subject의
guide로 옮겨졌습니다. 보존된 본문은 `docs/98.archive/retired/` 아래에
있으며 `tomb-AUD-0097`이 그 처분을 기록합니다.

## Supersession Ledgers

Migration 0003이 과거 경로 복구를 기록합니다.

## Usage

package는 `audits/####-<slug>/` 아래에만 만들고 대응하는 Stage 99
템플릿을 사용합니다. 관찰 날짜, 인용, provenance, 활성 owner
Traceability를 보존합니다.

## Related Documents

- [References index](../README.md)
- [Stage 99 Registry](../../99.templates/registry.json)
