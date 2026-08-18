---
status: active
---

# Document Corpus Lifecycle Reference Data

> 검토된 migration manifest와 deterministic summary를 제공하는 Stage 90 data route

## Overview

`docs/90.references/data/governance/document-corpus-lifecycle`는 문서 corpus
lifecycle migration의 검토 가능한 manifest와 generator-owned summary를
보관합니다. 이 namespace는 Stage 99 machine contract와 Stage 04 evidence를
보조하며, 정책·승인·runtime truth를 대체하지 않습니다.

## Category Role

이 category는 reviewed blocking Foundation 및 target-surface decision을 각
manifest와 safe summary로 제시해 source selection과 검토
상태를 재현할 수 있게 합니다. lifecycle 규칙과 승인 기준은 Stage 99 contract
및 Stage 04 evidence가 소유하며, 이 경로는 그 판단 근거를 참조 가능한 data로만
제공합니다.

## Audience

이 README의 주요 독자:

- Documentation Writers
- QA Engineers
- AI Agents
- Repository Maintainers

## Scope

### In Scope

- 승인된 wave source selection을 분류한 reviewed manifest
- manifest에서 결정론적으로 생성한 safe summary
- Stage 99 contract, validator, Stage 04 Task로 향하는 routing

### Out of Scope

- corpus 문서의 본문 또는 frontmatter 일괄 이관
- archive ledger, immutable snapshot manifest, tombstone payload
- runtime, Compose, infrastructure, deployment, secret, provider state
- review verdict 또는 blocking enforcement의 자체 승인

## Structure

```text
document-corpus-lifecycle/
├── README.md                               # This routing index
├── ref-0066-foundation-summary.md                 # Generator-owned Foundation summary
├── ref-0067-foundation.yaml                       # Reviewed blocking v1 manifest
├── ref-0068-target-surface-convergence-summary.md # Generator-owned target summary
└── ref-0069-target-surface-convergence.yaml       # Reviewed blocking v2 classification
```

## How to Work in This Area

1. `ref-0067-foundation.yaml`은 [corpus migration contract](../../../../99.templates/support/corpus-migration-contract.md)와 machine registry를 따라 검토합니다.
2. `ref-0066-foundation-summary.md`는 lifecycle validator의 `generate-summary` mode로만 갱신하고 hand edit하지 않습니다.
3. `ref-0069-target-surface-convergence.yaml`은 고정 baseline의 eight source roots와 exact direct source paths를 schema v2로 분류하며, 승인된 whole-branch review와 controlled-wrapper evidence에 따라 blocking/pass 상태를 유지합니다.
4. `ref-0068-target-surface-convergence-summary.md`도 lifecycle validator의 `generate-summary` mode로만 갱신합니다.
5. manifest와 summary는 Stage 04 Task evidence 및 independent review와 함께 해석합니다.
6. Foundation에서는 archive ledger나 snapshot manifest를 publish하지 않습니다. 해당 산출물은 Wave D의 별도 승인 범위입니다.
7. 변경 후 wave별 `check-manifest`, `check-summary`, generated owner check mode, repository contracts를 실행합니다.

## Related Documents

- [governance reference data](../README.md)
- [reference data](../../README.md)
- [Foundation Spec](../../../../03.specs/spec-0131-document-corpus-lifecycle-migration-foundation/spec.md)
- Foundation Plan
- Foundation Task
- [Target Surface Spec](../../../../03.specs/spec-0133-target-surface-contract-convergence/spec.md)
- Target Surface Plan
- Target Surface Task
- [corpus migration contract](../../../../99.templates/support/corpus-migration-contract.md)
- [machine migration registry](../../../../99.templates/support/document-corpus-migration-contract.yaml)
