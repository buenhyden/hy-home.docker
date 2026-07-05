---
name: deployment-pipeline-design
description: >
  CI/CD pipeline design reference for hy-home.docker. Designs and audits GitHub Actions workflows
  and gate placement for Docker Compose delivery, aligned with the ci-cd-patterns function.
  Use for 'CI/CD', 'pipeline', 'GitHub Actions', 'deployment gate', 'workflow design'.
  Backs the ci-cd-engineer agent.
---

# Deployment Pipeline Design — hy-home.docker

## When to Use

Use when designing or auditing this repository's CI/CD pipelines.

## Procedure

1. Map the change to affected workflows under `.github/workflows/` (e.g. `ci-quality.yml`).
2. Place security/quality gates using the `ci-cd-patterns` function (pre-commit, PR, build).
3. Enforce anti-duplication: do not run the same heavy job in both local pre-commit and CI
   (per `rules/github-governance.md`).
4. Validate workflow YAML and capture the design/audit in `_workspace/repo-support/pipeline_design_<date>.md`.

## Rules

- Pin third-party actions; never use floating tags (repository governance).
- Keep gates measurable against workspace DORA targets.

## Related Documents

- `docs/00.agent-governance/agents/functions/deployment-pipeline-design.md`
- `docs/00.agent-governance/agents/functions/ci-cd-patterns.md`
- `docs/00.agent-governance/rules/github-governance.md`
