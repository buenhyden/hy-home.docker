---
title: "Governance and QA Convergence Specification"
version: "0.2.0"
type: "sdlc/spec"
status: "active"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "specs"
artifact_id: "SPEC-0174"
parent_ids:
- "REQ-0024"
- "AD-0027"
created: "2026-09-05"
---

# Governance and QA Convergence Specification

## Overview

Closeout review checkpoint (2026-09-05): the user approved transferring this
package's retained obligations to SPEC-0173 and preserving this entire packet.
The original implementation narrative below is dated evidence, not a request
to restore retired wrappers or execute remote delivery. Current Stage 00 policy
allows an empty `.agents/` root and retains direct canonical Codex skill reads.
The integrated workflow contract owns executable composition. Independent
provider, gate, Python, and policy integration reviews passed; final aggregate
acceptance remains with SPEC-0173 Task 0006. This is forward review for handoff,
not retrospective completion of this package's original remote scope.

Remove the retired shared runtime directory, converge provider-neutral governance
and provider adapters, and make local and hosted validation follow the same
observable contracts without redundant checks or incompatible Compose selections.

## Boundaries and Inputs

The user authorized repository changes, obsolete-document retirement, fixture and
gate simplification, local and hosted QA, and logical commits against `main`.
Scope includes Stage 00, Stage 99, provider projections, hooks, `.github/`, scripts,
tests, active reference evidence, and the current Spec/Plan/Task corpus.
Deployment, credentials, global provider configuration, branch-protection mutation,
PR merge, and other workers' branches remain outside this change.

## Behavior Contract

- Stage 00 owns common policies, roles, procedures, workflow, and QA semantics.
  Provider registry entries own translation facts; native files never own policy.
- The retired shared runtime directory is absent and cannot be regenerated.
  Claude retains native skill projection. Codex loads canonical Stage 00 skill
  files explicitly; this is not a claim of native skill-picker discovery.
- `changed` and `full` remain the only public validation profiles. The manifest
  owns composition, and a selected atomic leaf executes at most once per run.
- Local and hosted QA share applicable checks. GitHub-only upload permissions
  must not be confused with the ability to run a scanner locally.
- Independent Compose selections retain collision validation. No aggregate
  environment may force mutually exclusive services into one selection.
- Existing reviews, permission bounds, secret safety, timeouts, and failure
  propagation remain mandatory. Skips name an actual scope or environment limit.
- Historical evidence is not current policy. Retired operational prescriptions
  leave active authority, while frozen archive bodies remain recoverable.

## Technical Approach

Remove compatibility projections from the registry, renderer, and typed contract;
remove their tracked generated files and update consumers. Reuse existing canonical
policy owners rather than creating a second rules tree. Correct the executable
QA contract and its regression tests with the same change. Consolidate explanations
and refresh generated catalogs only through their generators.

## Interfaces and Data

- `docs/00.agent-governance/providers/registry.yaml`: provider translation routes.
- `docs/99.templates/registry.json`: document profiles, templates, IDs, lifecycle.
- `.github/workflow-contract.yml`: gate DAG, suite impact, workflow and Action facts.
- `python3 scripts/validation/run-ci-gate.py --profile changed|full`: public QA.
- `bash scripts/operations/sync-provider-surfaces.sh --check`: read-only parity.

## Failure Modes and Guardrails

Reject unregistered projections and retired-directory reintroduction. Preserve
unknown or other-owned files. Never waive a failing collision, security, metadata,
or lifecycle check to produce a green result. An unavailable dependency or remote
review remains unverified; a local result never substitutes for a hosted result.
Do not rewrite active concurrent branches or frozen archive bodies.

## Acceptance Contract

| Requirement | Evidence |
| --- | --- |
| Shared runtime removed | tracked-path census, renderer parity, negative reintroduction test |
| Provider controls preserved | native role controls and canonical skill-route regressions |
| QA composition converged | suite/runner/workflow tests and selected profile output |
| Compose CI selection repaired | workflow override regression and independent selection checks |
| Documentation current | metadata, traceability, lifecycle, retired-reference and freshness checks |
| Reviewable delivery | logical commits, PR scope, exact hosted status and remaining review requirements |

## Traceability

- [REQ-0024](../../01.requirements/0024-agent-governance-standardization.md)
- [AD-0027](../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md)
- [ADR-0029](../../02.architecture/decisions/0029-workspace-governance-authority.md)
- [Plan](plan.md)
- [Task](tasks/tsk-0001-converge-governance-and-qa.md)

## Open Questions

Native Codex skill-picker adoption without the removed directory is not assumed.
Explicit canonical reads are the supported repository route. Independent review
and remote branch-protection administration remain owner decisions.

## Operational Impact

No live service operation, deployment, secret read, or global installation is part
of this change. Existing PRs remain independent until the owner chooses integration.
