---
layer: agentic
artifact_type: agent-function
function_id: workspace-audit-revalidation
scope: agentic
status: active
---

# workspace-audit-revalidation

## Preconditions

A canonical audit, criterion definitions, current repository baseline, and representative evidence boundary must be fixed before scoring.

## Inputs

- Canonical audit and current repository evidence.
- Criterion IDs, scorers, thresholds, source cutoff, and known forward dependencies.

## Procedure

1. Reproduce each criterion against current tracked source and generated freshness, treating advisory graphs and provider claims as non-authoritative.
2. Apply the defined scorer and threshold to representative evidence, separating repository adoption from runtime acceptance or entitlement.
3. Record changed statuses, unchanged gaps, confidence, and exact validation evidence without backdating or promoting unobserved claims.

## Outputs

- A calibrated revalidation with criterion-level evidence and explicit uncertainty.

## Gates

- Evidence is representative, source-bounded, and reproducible.
- No criterion receives a pass from absent runtime or provider observation.

## Failure Handling

Return `needs_revalidation` when evidence, entitlement, cutoff, or calibration is insufficient; never infer completion from policy text alone.

## Related Documents

- [Evaluation engineer](../agents/eval-engineer.md)
- [Agent catalog contract](../../contracts/agent-catalog.yaml)
- [Agentic scope](../../scopes/agentic.md)
