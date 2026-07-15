---
layer: agentic
artifact_type: agent-function
function_id: ci-cd-patterns
scope: ops
status: active
---

# ci-cd-patterns

## Preconditions

The delivery contract, repository workflow state, and protected remote-action boundary must be known before selecting a pipeline pattern.

## Inputs

- Approved delivery contract and current workflow files.
- Required checks, permissions, trigger conditions, and failure policy.

## Procedure

1. Map changed surfaces to deterministic local and CI gates, reusing existing jobs before adding new workflow structure.
2. Select least-privilege permissions, immutable action references, bounded matrices, and secret-safe output for each job.
3. Validate trigger/base-SHA behavior and record which deployment or remote gates remain outside local evidence.

## Outputs

- A pipeline pattern with ordered checks, permissions, evidence, and rollback behavior.

## Gates

- Workflow permissions are least privilege.
- Every check is reproducible or explicitly classified as CI-only.

## Failure Handling

Stop when credentials, remote rulesets, or promotion authority are required; produce a scoped follow-up rather than weakening the gate.

## Related Documents

- [CI/CD engineer](../agents/ci-cd-engineer.md)
- [GitHub governance](../../rules/github-governance.md)
- [Task checklists](../../rules/task-checklists.md)
