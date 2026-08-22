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
- Value-free agent-role and provider-model retirement provenance
- Dated, non-authoritative GitHub Actions control-plane observations
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
├── agent-governance-retirement-ledger.yaml # Role/model retirement provenance
├── agent-output-eval-fixtures.md      # Agent-output eval fixture catalog
├── audit-implementation-matrix.md     # Generated audit implementation matrix snapshot
├── document-corpus-lifecycle/         # Reviewed manifests and generated safe summaries
├── gap-to-stage-routing.md            # Gap-to-stage routing advisory reference
├── github-actions-control-plane-observation.yaml # Dated public remote observation
├── provider-hook-parity-matrix.md     # Generated provider hook parity matrix
├── target-surface-delta-manifest.yaml # Reviewed Spec 135 successor delta
└── target-surface-delta-summary.md    # Generated value-free delta summary
```

## Current References

- [agent-governance-retirement-ledger.yaml](ref-0063-agent-governance-retirement-ledger.yaml) - historical role and model replacements with immutable baseline commit/blob provenance
- [agent-output-eval-fixtures.md](ref-0064-agent-output-eval-fixtures.md) - agent-output eval fixture catalog and local advisory runner contract for documentation, provider, and infrastructure tasks
- [audit-implementation-matrix.md](ref-0065-audit-implementation-matrix.md) - generated audit implementation matrix snapshot for report coverage, overview categories, candidate closure, generated evidence surfaces, and residual gap signals
- [document-corpus-lifecycle/README.md](./document-corpus-lifecycle/README.md) - corpus lifecycle manifest and generated-summary routing
- [document-corpus-lifecycle/foundation.yaml](document-corpus-lifecycle/ref-0067-foundation.yaml) - reviewed blocking Foundation migration manifest
- [document-corpus-lifecycle/foundation-summary.md](document-corpus-lifecycle/ref-0066-foundation-summary.md) - generator-owned safe Foundation summary
- [gap-to-stage-routing.md](ref-0070-gap-to-stage-routing.md) - Stage 00 gap-to-stage routing table and recommender contract
- [github-actions-control-plane-observation.yaml](ref-0071-github-actions-control-plane-observation.yaml) - dated public GitHub Actions inventory with explicit unverified control-plane and root-cause boundaries
- [provider-hook-parity-matrix.md](ref-0072-provider-hook-parity-matrix.md) - generated Claude/Codex/Gemini hook parity matrix and Gemini behavioral reminder checklist
- [target-surface-delta-manifest.yaml](ref-0073-target-surface-delta-manifest.yaml) - advisory successor manifest classifying every target path changed since the immutable Spec 133 closure
- [target-surface-delta-summary.md](ref-0074-target-surface-delta-summary.md) - generator-owned, value-free successor-delta and current-inventory summary

## How to Work in This Area

1. Verify that a new document is reference data, not active policy.
2. Link every governance fact back to Stage 00 source documents.
3. Keep non-README reference documents English-only.
4. Keep retirement records value-free and bind each source to an exact Git commit, path, and blob.
5. Validate lifecycle manifest and summary changes through their canonical lifecycle checker modes.
6. Keep remote observations source-linked, dated, non-authoritative, and explicit about every unverified field.
7. Refresh the target-surface delta summary only through
   `python3 scripts/validation/check-target-surface-delta-contract.py --write-summary`.
8. Run `bash scripts/validation/check-repo-contracts.sh` after changing this category.

## Related Documents

- [reference data](../README.md)
- [90.references](../../README.md)
- [documentation protocol](../../../00.agent-governance/policies/documentation-protocol.md)
- [gap routing recommender](../../../../scripts/validation/recommend-gap-routing.sh)
