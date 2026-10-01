---
title: "CI Delivery Gate Optimization"
version: "0.1.4"
type: "sdlc/spec"
status: "active"
owner: "@buenhyden"
updated: "2026-10-02"
layer: "specs"
artifact_id: "SPEC-0199"
parent_ids:
- "REQ-0024"
- "REQ-0027"
- "AD-0027"
created: "2026-10-01"
---

# CI Delivery Gate Optimization

## Overview

Assign each repository-owned QA predicate to the earliest useful delivery
boundary, and repeat it only when a different revision or environment gives a
distinct result. Keep pull-request protection, explicit full-audit capability,
and merged-revision security evidence while removing routine full-suite work
from commit, push, and post-merge paths. A successful main push advances a
mutable `main-current` channel tag to the verified main commit. Existing
release tags remain separate and unchanged.

The user requested a review of local, remote, and GitHub Actions verification;
evidence-based removal of one-off, legacy, deprecated, duplicate,
contradictory, and excessive scripts and tests; and a tag that follows main.
The user selected `main-current` and approved this architectural design on
2026-10-01. The user approved the written Spec on 2026-10-01 and requested
an implementation Plan; the written Plan was approved on 2026-10-02 with
same-session implementation and an independent final review.

## Boundaries and Inputs

The tracked inputs are `.github/workflows/`, `.github/workflow-contract.yml`,
`.pre-commit-config.yaml`, `.codex/hooks.json`, `.claude/settings.json`,
`scripts/hooks/agent-event-hook.sh`, `scripts/validation/`,
`scripts/lib/gate/`, `scripts/manifest.yaml`, `tests/`, and their canonical
governance and operations owners. Inspect actual local `core.hooksPath`,
protected-branch required contexts, active remote workflows, and hosted run
evidence before claiming an execution boundary. A repository hook declaration
does not prove it is the installed local hook.

The 2026-10-01 baseline has a required PR `validation-changed` context and a
main-push/manual `validation-full` job. The latter repeats much of the same
six-suite repository QA after the PR gate. The declared pre-commit and pre-push
hooks also invoke `changed` and `full`, respectively, while the agent Stop
hook invokes `changed` with a 540-second budget. The observed local Git hook
path is `/home/hyunyoun/.codex/git-hooks`, outside this repository; changing
`.pre-commit-config.yaml` alone does not replace it. The public gate already
deduplicates exact invocations within one plan, so the target is phase-level
duplication rather than another gate-DAG framework.

In scope: quality workflow triggers/jobs, public gate routing, repository-owned
hook bindings, static workflow contract, tests and script inventory, `.github`
supporting definitions, canonical quality/GitHub/Git policies, and affected
operator navigation. Preserve the required context name unless a separately
reviewed protection migration is unavoidable. Document the two disabled remote
workflow registrations that have no tracked workflow file; they are remote
state, not currently executing scripts.

Out of scope: changing global Git hooks or credentials, creating a PAT,
weakening main protection, rewriting release tags, changing service runtime,
deleting frozen historical records, and claiming external CodeQL or GitGuardian
runs were eliminated. A remote workflow registration may be removed only
through its own reviewed remote-state action.

## Behavior Contract

| Boundary | Required behavior | Evidence owner |
| --- | --- | --- |
| Commit | Cheap touched-file format, lint, secret, and commit-message checks only; no public `changed` or `full` suite | Installed-hook observation and local command result |
| Feature-branch push | No automatic full repository QA; an explicit local focused check remains available | Local Task evidence |
| Pull request to main | One required `validation-changed` run for each relevant candidate revision, with existing changed-path selection and fail-closed fallback | GitHub check on exact PR candidate SHA |
| Main push after merge | Only checks whose merged SHA, hosted security context, or SARIF publication produces distinct evidence; no repeated full QA suite | GitHub main-push run on exact SHA |
| Manual dispatch | The existing `full` profile remains available for intentional corpus-wide audit | Dispatch run and selected ref |

Keep the PR workflow eligible for every PR to main, including documentation
changes. Do not apply workflow-level path filters that leave the required check
pending when GitHub skips a workflow. Preserve cancellation of stale runs, but
do not cancel a newer candidate's check in favor of an older one. A PR title
edit reruns the required changed profile, including git-flow validation.
This repetition is necessary because an edited run can cancel an in-progress
synchronize run under the workflow's concurrency group. A git-flow-only
success under the same required job name would otherwise allow the candidate
SHA to appear green without a completed changed-profile result.

The post-merge path must have an explicit narrow profile or equivalent
registered route in the existing gate system. Define its allowed gate leaves
and context in the workflow contract, prove it has no routine QA leaf already
owned by the PR path, and retain any genuinely distinct merged-SHA security
check with its reason. CodeQL default setup and external security integrations
remain separate observations; repository-owned scheduling must not silently
disable them. A failed post-merge check remains a visible failure, not a
retroactive claim that PR protection passed for the merged SHA.

After the main-push post-merge job succeeds, a dependent tag job advances
`refs/tags/main-current` to that exact main SHA only if remote `main` still
points to the same SHA. If the tag is already there, it succeeds without a
write. The tag job alone gets `contents: write`; quality jobs keep read-only
content permission and only the additional security permission needed for
SARIF. Record the old and new SHA in the run. A stale run, failed check,
missing permission, or rejected tag update leaves the tag unchanged and the
job failed, with a documented retry path. Do not target `0.0.1`, `v*.*.*`, or
other release tags. `main-current` is a channel pointer, not a release or a
version source for running services.

## Technical Approach

Use the existing `.github/workflow-contract.yml` gate registry and
`run-ci-gate.py` runner. Keep one static command per quality job and adapt the
focused workflow checker and tests to the new event/profile mapping. Remove
expensive automatic repository-owned local hook routes only after tracing every
caller and retaining their unique cheap predicates. In particular, reconcile
`run-ci-precommit.sh`'s recursion-safe skip list with any removed public hook
IDs, and align both provider Stop bindings with the canonical quality policy.
Do not change a user's global hook installation as a side effect.

Inventory every proposed script or test deletion using its manifest entry,
callers, workflow/hook consumers, assertions, and replacement owner. Delete a
file only when it has no live consumer or its behavior is covered by one
current canonical owner and the relevant regression gate still passes. A
historical name, large file, or negative assertion against a retired path is
not proof of dead code. The current audit found no evidence-backed file
deletion candidate; this Spec does not require a deletion quota. Remove a
duplicate invocation at its owner even when its underlying test must remain.

Update `.agents/governance/quality-standards.md`,
`.agents/governance/github-governance.md`, applicable Git/release policy,
and `.agents/knowledge/verification-surface-map.md` alongside the
executable workflow contract. Update `.github` navigation and
Stage 05 runbooks only where operator actions or recovery actually change.
Write Spec, Plan, and Task prose in English; README and Stage 05 explanatory
prose follow their registered Korean language rule. Avoid a parallel CI
governance document or second verification matrix.

## Interfaces and Data

The public CLI keeps `changed` and `full`; a narrow post-merge profile, if
introduced, is a registered static profile rather than a caller-controlled
arbitrary gate list. The PR required check remains `validation-changed`.
GitHub workflow environment supplies trusted event/SHA fields, never
interpolated untrusted PR text into shell. The tag job uses only the
repository-scoped `GITHUB_TOKEN`; no new credential or secret is stored.
Protected-branch settings and remote disabled-workflow registrations are
observed and reported separately from tracked YAML.

## Failure Modes and Guardrails

- If a required PR check is skipped, absent, cancelled, or red, the PR is not
  merge-ready. Workflow syntax and contract tests must catch trigger/filter
  regressions before delivery.
- If a gate leaf would disappear from all normal and manual routes, restore an
  owner before removing its old invocation. Environment-specific checks remain
  in the environment where they are meaningful.
- If the merged commit differs from the PR head, report the revision boundary.
  The post-merge result does not replace PR required-check evidence.
- If main advances while a run is executing, reject the stale tag update.
  Avoid force-updating any release tag. A retry rechecks main and resumes from
  current state rather than assuming the old SHA is still current.
- If the installed local hook differs from the tracked declaration, report the
  observed boundary and do not claim local hook optimization is deployed.
- If removal evidence is ambiguous, retain the script/test and record why.
  Do not delete preservation fixtures or suppress tests merely to reduce time.

## Acceptance Contract

1. A reviewed execution matrix identifies every repository-owned heavy QA
   command across commit, push, PR, main push, manual dispatch, and agent Stop;
   each retained repeated invocation has a distinct revision/environment
   reason. The installed local Git hook boundary is reported separately.
2. Routine commit and feature-branch push do not automatically invoke the
   public `changed` or `full` gate. Cheap unique local checks remain, and the
   agent Stop path no longer performs a second mandatory `changed` run.
3. `validation-changed` remains the required PR context for all PRs to main.
   Changed-path, title-edit, stale-run, and failed/skipped-check scenarios are
   covered by focused tests and static contract verification.
4. A main push runs only registered merged-revision or hosted-security checks;
   it does not run the six-suite `full` QA profile. Manual dispatch still runs
   `full`, and no existing required gate leaf becomes unreachable.
5. The tag job moves only `main-current` after successful main-push checks,
   confirms the run SHA is still main HEAD, is idempotent, uses minimum token
   permission, and reports failure without moving a release tag. Tests cover
   success, already-current, stale-main, and failed-check cases; hosted evidence
   proves the first real update only after the workflow is delivered.
6. Every removed script/test/hook invocation has a recorded consumer and
   replacement analysis. Active regression tests and scripts stay in place
   when no evidence-backed deletion exists. The manifest and workflow contract
   have no dangling references.
7. Canonical policies, the active verification knowledge map, `.github`
   definitions/navigation, and affected runbooks describe the same phase
   ownership and tag recovery behavior. Focused gate,
   workflow, hook, and documentation checks pass on the exact candidate; actual
   hosted PR and main-push results are recorded separately from local results.

## Traceability

- [REQ-0024 agent governance](../../01.requirements/0024-agent-governance-standardization.md): REQ-0024-FR-0007, REQ-0024-FR-0008, REQ-0024-NFR-0011, REQ-0024-NFR-0012, and REQ-0024-NFR-0013.
- [AD-0027 canonical adapter](../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md): one policy owner and provider-specific hook bindings.
- [REQ-0027 host verifiability](../../01.requirements/0027-home-development-host.md): REQ-0027-NFR-0004 requires actual revision-scoped evidence; this Spec is context, not an unverified result claim.
- [GitHub workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax): required-check and permission boundaries.
- [GitHub `GITHUB_TOKEN`](https://docs.github.com/en/actions/concepts/security/github_token): token-created tag pushes do not recursively run normal push workflows.
- [CodeQL setup types](https://docs.github.com/en/code-security/concepts/code-scanning/setup-types): default setup owns PR and branch scanning outside this repository workflow.
- [GitHub immutable releases](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases): release identity remains distinct from the mutable channel tag.

## Open Questions

None at this design stage. The Plan must verify the exact current remote
protection, hook, and workflow observations before editing or delivery.

## Operational Impact

Expected developer wait is lower because commit and feature push no longer run
full repository QA, and main push no longer repeats all PR-owned suites. PR
protection remains the merge gate. Security checks on the merged SHA and
`main-current` movement remain visible GitHub jobs. A failed post-merge job
requires repair and rerun; it must not be hidden by moving the tag manually.
