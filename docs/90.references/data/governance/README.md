---
status: active
---

<!-- Target: docs/90.references/data/governance/README.md -->

# Governance Reference Data

> Stage routing, governance inventory, and validation-reference data

## Overview

`docs/90.references/data/governance` stores stable governance reference data
that supports Stage 00 rules and repository validation without becoming active
policy itself.

이 폴더의 reference는 Stage 00 governance 원문을 대체하지 않습니다. 최신
정책과 routing rule은 `docs/00.agent-governance/`가 담당합니다.

## Category Role

이 category는 governance 규칙을 반복해서 해석해야 하는 audit, review,
validation 작업을 보조합니다. 실행 절차나 policy 변경은 canonical Stage 00
또는 Stage 04 문서에서 처리합니다.

## Audience

이 README의 주요 독자:

- Documentation Writers
- QA Engineers
- AI Agents
- Repository Maintainers

## Scope

### In Scope

- Stable routing-reference data derived from Stage 00 governance rules
- Advisory validation and recommendation tool references
- Agent-output eval fixture and local advisory runner references for recurring task surfaces
- Generated provider hook parity and behavioral reminder references
- Generated audit implementation matrix references for Stage 90 audit maintenance
- Reviewed corpus lifecycle manifests and generator-owned safe summaries
- Governance inventory context used by audit reports

### Out of Scope

- Active policy body
- Provider runtime configuration
- Model policy changes
- Secret values, credentials, tokens, private keys, shell history, or raw logs

## Structure

```text
governance/
├── README.md                          # This file
├── agent-output-eval-fixtures.md      # Agent-output eval fixture catalog
├── audit-implementation-matrix.md     # Generated audit implementation matrix snapshot
├── document-corpus-lifecycle/         # Reviewed manifests and generated safe summaries
├── gap-to-stage-routing.md            # Gap-to-stage routing advisory reference
└── provider-hook-parity-matrix.md     # Generated provider hook parity matrix
```

## Current References

- [agent-output-eval-fixtures.md](./agent-output-eval-fixtures.md) - agent-output eval fixture catalog and local advisory runner contract for documentation, provider, and infrastructure tasks
- [audit-implementation-matrix.md](./audit-implementation-matrix.md) - generated audit implementation matrix snapshot for report coverage, overview categories, candidate closure, generated evidence surfaces, and residual gap signals
- [document-corpus-lifecycle/README.md](./document-corpus-lifecycle/README.md) - corpus lifecycle manifest and generated-summary routing
- [document-corpus-lifecycle/foundation.yaml](./document-corpus-lifecycle/foundation.yaml) - reviewed blocking Foundation migration manifest
- [document-corpus-lifecycle/foundation-summary.md](./document-corpus-lifecycle/foundation-summary.md) - generator-owned safe Foundation summary
- [gap-to-stage-routing.md](./gap-to-stage-routing.md) - Stage 00 gap-to-stage routing table and recommender contract
- [provider-hook-parity-matrix.md](./provider-hook-parity-matrix.md) - generated Claude/Codex/Gemini hook parity matrix and Gemini behavioral reminder checklist

## How to Work in This Area

1. Verify that a new document is reference data, not active policy.
2. Link every governance fact back to Stage 00 source documents.
3. Keep non-README reference documents English-only.
4. Validate lifecycle manifest and summary changes through their canonical lifecycle checker modes.
5. Run `bash scripts/validation/check-repo-contracts.sh` after changing this category.

## Related Documents

- [reference data](../README.md)
- [90.references](../../README.md)
- [documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md)
- [gap routing recommender](../../../../scripts/validation/recommend-gap-routing.sh)
