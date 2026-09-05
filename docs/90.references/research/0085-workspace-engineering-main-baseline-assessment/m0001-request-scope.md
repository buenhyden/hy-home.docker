---
title: "Workspace Engineering Main Baseline Request Scope"
version: "0.3.0"
type: "reference/research"
status: "review"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "references"
artifact_id: "RES-0085-m0001"
parent_ids:
- "RES-0085"
created: "2026-09-04"
observed_at: "2026-09-05"
identity_recovery:
  source_commit: "db21aebf079fcc4e867779861b49c2283b7f8f01"
  source_path: "docs/90.references/research/0085-workspace-engineering-main-baseline-assessment/REQUEST-SCOPE.md"
  source_artifact_id: "RES-0085-SCOPE"
  decision_path: "docs/03.specs/0172-document-contract-convergence/tasks/tsk-0001-document-contract-convergence.md"
  decision_artifact_id: "SPEC-0172-TSK-0001"
  disposition: "consolidated"
---

# Workspace Engineering Main Baseline Request Scope

## Overview

This member preserves the binding repository target, comparison baseline,
evidence boundaries, and recovered request identity for the dated RES-0085
assessment. Current workspace-baseline conclusions are consolidated into
RES-0002-m0020; GitHub Actions platform findings remain in RES-0084.

## Research Questions

- Which repository revision is the baseline for the current assessment?
- Which evidence classes may support repository, Hosted, runtime, provider, and
  remote-control-plane claims?
- Which observations remain outside the approved or accessible boundary?

## Purpose

Prevent the original request, historical observations, or configuration-only
evidence from being mistaken for the current `main` implementation or live
runtime state, while keeping the exact recovery provenance available.

## Repository Role

RES-0085 owns the dated request and recovery evidence. RES-0002-m0020 owns
current baseline interpretation, RES-0002 owns cross-domain research, RES-0084
owns GitHub Actions platform mechanics, Stage 00 owns policy, and the current
Task owns execution evidence.

## Scope

### In Scope

- Repository: `buenhyden/hy-home.docker`
- Target and comparison branch: `main`
- Baseline commit: `4c6d211129615eab372d720ebd209b6c27618c86`
- Repository and external observation date: 2026-09-05
- Integration method: feature branch
- Direct writes to `main`: prohibited

### Out of Scope

- Secret values, credentials, certificates, authentication files, shell
  history, raw log databases, and user-global Claude or Codex settings.
- New deployment, release, tag, provider, or remote-control-plane mutation.
- Runtime acceptance for an unnamed service target.

## Definitions / Facts

- **Repository evidence** is tracked content or a deterministic local validator
  result tied to the baseline.
- **Hosted evidence** is a dated GitHub Actions run tied to an exact revision.
- **Runtime evidence** requires observation of the named service or provider
  behavior and is not implied by configuration.
- **Remote evidence** requires authenticated read-back from the remote control
  plane and remains point-in-time.

## Dated Repository State

All harness engineering, loop engineering, Claude Code and Codex governance,
spec-driven development, Docker Compose, infrastructure, SDLC, operations,
documentation, architecture, CI/CD, QA, security, verification and validation,
agent organization, memory, cost control, editor integration, context sharing,
and README analyses in the recovered request were assessed against
`main@4c6d211129615eab372d720ebd209b6c27618c86`.

Generic guidance is informative only. Repository-local instructions,
architecture decisions, policies, security controls, and verification evidence
have precedence.

## Detailed Findings

- The requested comparison target is `main` at
  `4c6d211129615eab372d720ebd209b6c27618c86`, observed 2026-09-05.
- RES-0002 and RES-0084 remain topical research owners; RES-0002-m0020 now owns
  current repository-local baseline conclusions.
- RES-0085 records the dated assessment boundary and exact recovered request;
  it does not compete with the current baseline owner.
- Local, hosted, provider, runtime, and remote evidence are separate. The
  latest remote protection evidence is the approved 2026-09-05 read-back in
  SPEC-0172; live deployment, tag, and release remain outside this observation.
- This renewal uses a feature branch and does not write directly to `main`.

## Evidence and Adoption Matrix

| Capability | Repository implementation | Evidence depth | Gap | Verification route |
| --- | --- | --- | --- | --- |
| Baseline identity | Exact `main` SHA recorded by RES-0085 | Defined, Local-executed | Later commits require a new observation | `git rev-parse main` |
| Research ownership | RES-0002-m0020 owns the current baseline; RES-0084 owns GitHub mechanics | Repository-enforced | Any later RES-0085 lifecycle transition requires separate approval | reference contract, lifecycle, and link checks |
| Hosted CI | Exact aggregate job runs recorded by SPEC-0172 | Hosted-executed | Future runs are mutable | owning Task plus GitHub run |
| Main protection | Exact approved read-back recorded by SPEC-0172 | Remote-verified on 2026-09-05 | Later drift is possible | authenticated full read-back |
| Deployment and release | No named target or current event | Unverified / not adopted | Acceptance and rollback target absent | separate approved Requirement-to-Task chain |

## Gaps and Risks

- This evidence is intentionally fixed to the named baseline and must not be
  presented as current after later `main` revisions.
- Local validation cannot prove Hosted runner, provider entitlement, deployed
  service, or remote GitHub state.
- Copying current or topical findings into this member would recreate the
  authority duplication removed by consolidation.

## Recommendations

- Re-observe current repository state in RES-0002-m0020 when `main` changes
  materially; do not refresh this dated scope carrier in place.
- Keep mutable Hosted, provider, runtime, and remote claims dated and tied to
  their owning evidence.
- Route implementation work through Research → Requirement → Architecture/ADR
  → Spec → Plan → Task → Verification → Independent Review.

## Verification

- `python3 -m unittest tests.lib.document_governance.test_references`
- `python3 scripts/validation/check-document-links.py --mode traceability`
- `python3 scripts/knowledge/generate-llm-wiki.py --check`
- `python3 scripts/validation/run-ci-gate.py --profile full`

## Sources

- Repository baseline `main@4c6d211129615eab372d720ebd209b6c27618c86`,
  observed 2026-09-05.
- [Stage 00 governance](../../../00.agent-governance/README.md).
- [Registry](../../../99.templates/registry.json) and the
  [research member template](../../../99.templates/templates/references/research.template.md).
- [SPEC-0172 Task evidence](../../../03.specs/0172-document-contract-convergence/tasks/tsk-0001-document-contract-convergence.md).

## Scope Implications

This scope permits current repository and dated external research. It does not
authorize policy creation in Stage 90, deployment, release, secret inspection,
or a new remote mutation. Any new implementation recommendation needs a
separate owner and the repository SDLC chain.

## Related Documents

- [Dated baseline assessment package](README.md)
- [Current workspace baseline](../0002-agentic-engineering-research-pack/m0020-workspace-baseline.md)
- [Agentic engineering research](../0002-agentic-engineering-research-pack/README.md)
- [GitHub Actions platform research](../0084-github-actions-platform/README.md)
- [SPEC-0172 execution evidence](../../../03.specs/0172-document-contract-convergence/tasks/tsk-0001-document-contract-convergence.md)
