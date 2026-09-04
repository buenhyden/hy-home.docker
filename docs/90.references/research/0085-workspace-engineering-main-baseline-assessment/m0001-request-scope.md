---
title: "Workspace Engineering Main Baseline Request Scope"
version: "0.1.0"
type: "reference/research"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-04"
layer: "references"
artifact_id: "RES-0085-m0001"
parent_ids:
- "RES-0085"
created: "2026-09-04"
identity_recovery:
  source_commit: "db21aebf079fcc4e867779861b49c2283b7f8f01"
  source_path: "docs/90.references/research/0085-workspace-engineering-main-baseline-assessment/REQUEST-SCOPE.md"
  source_artifact_id: "RES-0085-SCOPE"
  decision_path: "docs/03.specs/0172-document-contract-convergence/tasks/tsk-0001-document-contract-convergence.md"
  decision_artifact_id: "SPEC-0172-TSK-0001"
  disposition: "consolidated"
---

# Workspace Engineering Main Baseline Request Scope

## Binding Target

- Repository: `buenhyden/hy-home.docker`
- Target and comparison branch: `main`
- Integration method: feature branch and pull request
- Direct writes to `main`: prohibited

All harness engineering, loop engineering, Claude Code and Codex governance,
spec-driven development, Docker Compose, infrastructure, SDLC, operations,
documentation, architecture, CI/CD, QA, security, verification and validation,
agent organization, memory, cost control, editor integration, context sharing,
and README analyses in this research request must be interpreted against the
actual files and executable behavior of this repository's `main` branch.

Generic guidance is informative only. Repository-local instructions,
architecture decisions, policies, security controls, and verification evidence
have precedence.

## Related Documents

- [Baseline assessment](README.md)
