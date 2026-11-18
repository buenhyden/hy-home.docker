---
name: "ci-cd-patterns"
description: "Use when delivery workflows need deterministic local and CI gates, least-privilege jobs, and explicit remote promotion boundaries."
metadata:
  title: "ci-cd-patterns"
  version: "1.3.1"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-11-18"
  function_id: "ci-cd-patterns"
  scope: "ops"
  owner_agent: "ci-cd-engineer"
---

# ci-cd-patterns

## Trigger

### When to Use

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

The delivery contract, repository workflow state, and protected remote-action boundary must be known before selecting a pipeline pattern.

### When Not to Use

None: this skill states no exclusion.

## Procedure

### Steps

1. Map changed surfaces to deterministic local and CI gates, reusing existing jobs before adding new workflow structure.
2. Select least-privilege permissions, immutable action references, bounded matrices, and secret-safe output for each job.
3. Validate trigger/base-SHA behavior and record which deployment or remote gates remain outside local evidence.

#### Gates

- Workflow permissions are least privilege.
- Every check is reproducible or explicitly classified as CI-only.

#### Inputs

- Approved delivery contract and current workflow files.
- Required checks, permissions, trigger conditions, and failure policy.

### Failure Handling

Stop when credentials, remote rulesets, or promotion authority are required; produce a scoped follow-up rather than weakening the gate.

## Outputs

### Artifacts

- A pipeline pattern with ordered checks, permissions, evidence, and rollback behavior.

### Handoff

Owning role, policies and related documents:

- [CI/CD engineer](../../roles/ci-cd-engineer.md)
- [GitHub governance](../../../docs/00.workspace/02.process/github-governance.md)
- [Task checklists](../../../docs/00.workspace/03.quality/task-checklists.md)

## Verification

### Checks

- `scripts/validation/check-github-workflow-contract.py` passes for any changed workflow.
- Every job declares explicit least-privilege `permissions` and pins each action to a full commit SHA.
- Each check is marked reproducible locally or CI-only, and the remote gates left unobserved are listed.

### Limits

A remote gate the run does not observe stays unproven; the skill lists it
rather than counting it as passed.
