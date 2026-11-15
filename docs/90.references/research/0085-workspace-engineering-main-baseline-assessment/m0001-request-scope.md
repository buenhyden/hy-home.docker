---
title: "Workspace Engineering Main Baseline Request Scope"
version: "0.4.1"
type: "reference/research"
status: "in-review"
owner: "@buenhyden"
updated: "2026-11-16"
layer: "references"
artifact_id: "RES-0085-m0001"
parent_ids:
- "RES-0085"
created: "2026-09-04"
observed_at: "2026-09-05"
---

# Workspace Engineering Main Baseline Request Scope

## Overview

This member preserves the binding repository target, comparison baseline,
evidence boundaries, and recovered request identity for the dated RES-0085
assessment. Historical workspace-baseline conclusions are consolidated into
RES-0002-m0020; GitHub Actions platform findings remain in RES-0084.

## Scope and Method

### Boundaries

#### Research Questions

- Which repository revision is the baseline for this dated assessment?
- Which evidence classes may support repository, Hosted, runtime, provider, and
  remote-control-plane claims?
- Which observations remain outside the approved or accessible boundary?

#### Purpose

Prevent the original request, historical observations, or configuration-only
evidence from being mistaken for the current `main` implementation or live
runtime state, while keeping the exact recovery provenance available.

#### Repository Role

RES-0085 owns the dated request and recovery evidence. RES-0002-m0020 holds the
historical baseline synthesis. RES-0002 holds cross-domain research and RES-0084
holds GitHub Actions platform research. Canonical agent governance owns policy.
The relevant tracked source establishes the current implementation, and the
authorized Task records new execution evidence.

#### In Scope

- Repository: `buenhyden/hy-home.docker`
- Target and comparison branch: `main`
- Baseline commit: `4c6d211129615eab372d720ebd209b6c27618c86`
- Repository and external observation date: 2026-09-05
- Integration method: feature branch
- Direct writes to `main`: prohibited

#### Out of Scope

- Secret values, credentials, certificates, authentication files, shell
  history, raw log databases, and user-global Claude or Codex settings.
- New deployment, release, tag, provider, or remote-control-plane mutation.
- Runtime acceptance for an unnamed service target.

#### Definitions / Facts

- **Repository evidence** is tracked content or a deterministic local validator
  result tied to the baseline.
- **Hosted evidence** is a dated GitHub Actions run tied to an exact revision.
- **Runtime evidence** requires observation of the named service or provider
  behavior and is not implied by configuration.
- **Remote evidence** requires authenticated read-back from the remote control
  plane and remains point-in-time.

### Reproducible Method

The 2026-09-05 observation ran these checks against the baseline:

- `python3 -m unittest tests.lib.document_governance.test_references`
- `python3 scripts/validation/check-document-links.py --mode traceability`
- `python3 scripts/knowledge/generate-llm-wiki.py --check`
- `python3 scripts/validation/run-ci-gate.py --profile full`

Revalidated 2026-11-06: `scripts/knowledge/generate-llm-wiki.py` no longer
exists; `scripts/knowledge/` holds only `report-graphify-health.sh`. The
LLM Wiki generator retired on 2026-09-10. The other three commands remain
present (`tests/lib/document_governance/test_references.py`,
`scripts/validation/check-document-links.py:108`,
`scripts/validation/run-ci-gate.py`).

## Findings

### Dated Observations

#### Dated Repository State

All harness engineering, loop engineering, Claude Code and Codex governance,
spec-driven development, Docker Compose, infrastructure, SDLC, operations,
documentation, architecture, CI/CD, QA, security, verification and validation,
agent organization, memory, cost control, editor integration, context sharing,
and README analyses in the recovered request were assessed against
`main@4c6d211129615eab372d720ebd209b6c27618c86`.

Generic guidance is informative only. Repository-local instructions,
architecture decisions, policies, security controls, and verification evidence
have precedence.

#### Evidence and Adoption Matrix

| Capability | Repository implementation | Evidence depth | Gap | Verification route |
| --- | --- | --- | --- | --- |
| Baseline identity | Exact `main` SHA recorded by RES-0085 | Defined, Local-executed | Later commits require a new observation | `git rev-parse main` |
| Research ownership | The consolidation assigned workspace-baseline interpretation to RES-0002-m0020 and GitHub mechanics to RES-0084 | Repository-enforced | Any later RES-0085 lifecycle transition requires separate approval | reference contract, lifecycle, and link checks |
| Hosted CI | Exact aggregate job runs recorded by SPEC-0172 | Hosted-executed | Future runs are mutable | completed Spec plus GitHub run |
| Main protection | Exact approved read-back recorded by SPEC-0172 | Remote-verified on 2026-09-05 | Later drift is possible | authenticated full read-back |
| Deployment and release | No named target or current event | Unverified / not adopted | Acceptance and rollback target absent | separate approved Requirement-to-Task chain |

- The requested comparison target is `main` at
  `4c6d211129615eab372d720ebd209b6c27618c86`, observed 2026-09-05.
- RES-0002 and RES-0084 hold topical research. RES-0002-m0020 holds the
  consolidated historical repository-local baseline conclusions.
- RES-0085 records the dated assessment boundary and exact recovered request.
- Local, hosted, provider, runtime, and remote evidence are separate. The
  approved 2026-09-05 read-back in SPEC-0172 records remote protection for this
  assessment. Live deployment, tag, and release remain outside its scope.
- The recorded integration scope used a feature branch and prohibited direct
  writes to `main`.

### Interpretation

#### Gaps and Risks

- This evidence is intentionally fixed to the named baseline and must not be
  presented as current after later `main` revisions.
- Local validation cannot prove Hosted runner, provider entitlement, deployed
  service, or remote GitHub state.
- Copying current or topical findings into this member would recreate the
  authority duplication removed by consolidation.

#### Recommendations

- Use the relevant tracked source and an authorized Task for a new baseline
  assessment. Preserve the original observations in this member.
- Keep mutable Hosted, provider, runtime, and remote claims dated and tied to
  their owning evidence.
- Route implementation work through Research → Requirement → Architecture/ADR
  → Spec → Plan → Task → Verification → Independent Review.

#### Scope Implications

The original assessment covered the named repository revision and dated
external research. Policy and any new implementation or operational action
require their own authority through the repository SDLC chain.

## Limitations

### Unobserved Facts

- Secret values, credentials, user-global provider settings, raw logs, and
  shell history were not read.
- No deployment, release, tag, provider call, or remote mutation was observed.

### Interpretation Limits

- Hosted, provider, runtime, and remote evidence is point-in-time for
  2026-09-04 and 2026-09-05 and is not a permanent guarantee.
- SPEC-0172 and SPEC-0173 have since retired from the tree; their outcomes are
  recoverable from Git history only.

## Sources

- Repository baseline `main@4c6d211129615eab372d720ebd209b6c27618c86`,
  observed 2026-09-05.
- [Canonical agent governance](../../../../.agents/README.md).
- [Registry](../../../99.templates/registry.json) and the
  [research member template](../../../99.templates/templates/references/research.template.md).
- Completed SPEC-0172 outcome.

## Related Documents

- [Dated baseline assessment package](README.md)
- [Historical workspace baseline synthesis](../0002-agentic-engineering-research-pack/m0020-workspace-baseline.md)
- [Agentic engineering research](../0002-agentic-engineering-research-pack/README.md)
- [GitHub Actions platform research](../0084-github-actions-platform/README.md)
