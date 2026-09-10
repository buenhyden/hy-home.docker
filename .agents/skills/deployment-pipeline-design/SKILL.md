---
name: "deployment-pipeline-design"
description: "Use when release requirements need a pipeline design with immutable artifacts, approval gates, rollout observations, and concrete rollback."
metadata:
  title: "deployment-pipeline-design"
  version: "1.1.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-09-06"
  function_id: "deployment-pipeline-design"
  scope: "ops"
  owner_agent: "ci-cd-engineer"
---

# deployment-pipeline-design

## Preconditions

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

Release policy, deployment constraints, environments, approval authority, and rollback target must be explicit.

## Inputs

- Approved release policy and deployment constraints.
- Artifact identity, validation gates, environment boundaries, and recovery requirements.

## Procedure

1. Separate build, verify, approve, promote, observe, and rollback stages with immutable artifact handoff.
2. Place security, QA, and manual approval gates according to blast radius and environment authority.
3. Define rollout observations, stop conditions, and the exact artifact/configuration rollback path.

## Outputs

- A deployment pipeline design with stages, authorities, evidence, and rollback semantics.

## Gates

- Promotion cannot cross an approval boundary implicitly.
- Rollback is concrete, versioned, and testable before release.

## Failure Handling

Defer implementation when environment credentials, promotion authority, or rollback artifacts are absent; never substitute local success for deployment proof.

## Related Documents

- [CI/CD engineer](../../roles/ci-cd-engineer.md)
- [CI/CD patterns](../ci-cd-patterns/SKILL.md)
- [Approval boundaries](../../governance/approval-boundaries.md)
