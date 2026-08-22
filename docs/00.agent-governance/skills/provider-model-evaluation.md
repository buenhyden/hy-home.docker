---
profile_id: governance-skill
layer: agentic
function_id: provider-model-evaluation
scope: qa
status: active
owner_agent: eval-engineer
---

# provider-model-evaluation

## Preconditions

The provider/model question, official source boundary, repository work profile,
and synthetic comparison fixture must be explicit before evaluation begins.

## Inputs

- Current [provider registry](../providers/registry.yaml) status axes and work-profile selection.
- Dated official provider sources and provider-native schema evidence.
- Deterministic synthetic regression results; no live provider response is
  required or implied.

## Procedure

1. Separate provider lifecycle, repository disposition, runtime acceptance,
   entitlement, repository-default eligibility, and runtime activation.
2. Compare the proposed model/profile decision with dated official sources,
   native schema evidence, and the registered synthetic regression fixture.
3. Return a sourced disposition and acceptance boundary without promoting
   catalog presence, configured defaults, or synthetic scores into a live-model
   claim.

## Outputs

- `sourced-model-disposition`
- `native-acceptance-verdict`
- `regression-comparison`

## Gates

- Every fast-moving fact retains its official source and retrieval date.
- Runtime acceptance and entitlement remain `needs_revalidation` unless the
  separately approved runtime boundary supplies direct evidence.
- Comparisons are deterministic, value-free, and do not call a provider.

## Failure Handling

Return an unverified disposition and stop when a source, native-schema fact,
fixture result, or approval boundary is missing. Do not infer runtime
acceptance, entitlement, quality, cost, or latency.

## Related Documents

- [Evaluation engineer role](../roles/eval-engineer.md)
- [Provider model contract](../providers/registry.yaml)
- [Agent output evaluation fixtures](../../../90.references/data/governance/ref-0064-agent-output-eval-fixtures.md)
- [Spec 134](../../../03.specs/spec-0134-agent-governance-canonical-convergence/spec.md)
