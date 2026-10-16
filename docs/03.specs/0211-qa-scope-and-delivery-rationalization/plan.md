---
title: "QA Scope and Delivery Rationalization Plan"
version: "0.4.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0211-PLAN-0001"
parent_ids:
- "SPEC-0211"
created: "2026-10-07"
---

# QA Scope and Delivery Rationalization Plan

## Overview

Publish the initial draft contract, then implement the approved scope in
independent writer slices with a shared registration owner and read-only review.

## Scope

W1–W7 classify and retire obsolete QA, narrow changed-path selection,
restore remote candidate ownership, consolidate commit/changelog/SemVer
producers and align governance with Issue/Project navigation. Continuing
assurances keep their consumers, while historical refs, frozen evidence and
runtime authorization remain preserved.

W71–W73 support the existing criteria after W70 integrates: capture exact
selected toolchain/dependency and secure artifact identity, extend the existing
runner's per-gate evidence, and reconcile ROOT release obligations plus actual
QA04 execution. The CI audit implementer owns source/Plan writing; the root
agent integrates. The document writer owns the bounded RUN-0009 edit after this
Plan assignment. Task0001 retains sole Criterion Acceptance decisions.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 5 | Publish the initial draft package and issue identity | None | TSK-0001 | Task evidence |
| W2 | 1 | Classify and retire obsolete QA with continuing owners and bounded historical-link recovery | W1 | TSK-0001 | Task evidence |
| W3 | 2 | Narrow selection and preserve unique execution/failure boundaries | W2 | TSK-0001 | Task evidence |
| W4 | 3 | Restore optimized remote PR candidate QA and phase ownership | W3 | TSK-0001 | Task evidence |
| W5 | 4 | Consolidate commit, changelog and SemVer release production | W2 | TSK-0001 | Task evidence |
| W6 | 5 | Align current governance and Issue/Project views | W4, W5 | TSK-0001 | Task evidence |
| W7 | 1, 2, 3, 4, 5 | Validate final input, review and record residual owners | W6 | TSK-0001 | Task evidence |
| W70 | 2, 3, 5 | Support the existing criteria by promoting deterministic contract regressions to hosted changed selection and restoring tier 13 hardening coverage | W7 | TSK-0002 | RED/GREEN path selection, failure propagation and hardening behavior |
| W71 | 2, 3, 5 | Bind actual toolchain and dependency identity to the existing runner and define secure bounded artifact custody | W70 | TSK-0003 | Focused identity drift and artifact-boundary RED/GREEN |
| W72 | 2, 3, 5 | Record per-gate identity, selection, timing and terminal state in the existing runner for authenticated PR and explicitly evidenced clean-HEAD local runs; persist early remaining NOT_RUN evidence | W71 | TSK-0003 | Success, failure, timeout, cancellation, local identity and incomplete-receipt RED/GREEN |
| W73 | 2, 3, 4, 5 | Add ROOT promotion evidence to RUN-0009 and record service/path joins, actual QA04 changed/FULL/requirements and current-head remote proof or owned blockers | W72 | TSK-0003 | Actual final-input execution, exact-head observations, scoped docs and independent review |
| W74 | 1, 2 | Remove unit tests that repeat a real-tree check the full profile already runs as a gate, or that depend on local Git refs, and replace each with a fixture-bound check of the same rule | W72 | TSK-0003 | Per-test timing before and after; focused RED/GREEN for each replacement; no lost rule coverage |

## Verification Plan

Use focused RED/GREEN only for changed behavior and scoped registered style
checks. Derive final changed selection from the machine contract. The remote
PR run owns candidate validation excluding typed local-only leaves while
admitting the closed deterministic CI gate-contract, Compose-baseline and
repository-integrity regression set. The shared runner selects the hosted set
in the normal local changed plan and the changed candidate plan; all other units,
implementation fixtures and links remain in the local-only lane before
submission. Capture the immutable event, merge SHA, ordered raw parents and
absolute system Git path and configured Python interpreter before dependency
installation through the fixed system Bash path; require exact
agreement before contract loading, prerequisite selection and changed-path
execution. Poisoned custom event, SHA and PATH inputs must fail closed. Local
development does not repeat the remote bundle or full
profile. Separate Conftest unit verify from actual corpus commands while preserving
one invocation per registered gate ID/mode and Docker prerequisite ownership.
Retire completed cutover, fixed corpus and test-only helper units only after
current semantic owners are verified. Record each actual input, result and
review separately in the Task. W2 retires remaining historical source-census
and retired-file expectations with continuing owners. W3 removes the manifest's
path-only mirror requirement, closes direct unittest admission to LOCAL, and
corrects per-file shell syntax validation. Scoped lint-only corrections retain
Conftest mode and command behavior and use registered one-file lint/syntax checks.
W4 connects isolated local-staged lint/format immediately before commit and
exact authenticated pr-merge server checks before selected builds, sharing
candidate tool pins. W6 reconciles policy, authoring prompts and hook-warning
consumers without installing or replacing user-global hooks. Future deployment
promotion is a policy boundary only, not a new deployment workflow. W6 aligns full-audit and review-delta
policy. W7 validates only affected cases, manifest and read-only static/document
checks; it does not replay unchanged metadata/library aggregates or full QA.
Initial draft publication and final evidence-only records use document-minimum
checks. Generic preserved-source compatibility remains separate from historical
cutover completion evidence.

For the user's execution prompt04 on 2026-10-16 only, W73 runs an actual
changed-profile audit, explicit FULL-profile audit and requirements paths on
the final integrated input. This request-specific full-audit scope overrides
the ordinary no-full-repeat default for this execution; it does not make FULL
mandatory for every future commit, Release or unchanged input. Keep the
existing one-invocation and input/mode/trust reuse contracts, and never label
model/explain output as an actual run. W71 binds actual executable/dependency
identity and secure artifact custody; W72 records each selected node before
execution and preserves remaining NOT_RUN nodes on early stop. Current remote
PR/check issuer and merged-main security observations remain distinct from
local results. The configured strict App-bound required check and empty
effective rules are dated observations, not workflow-source immutability. No
protection PATCH, operational credential use, real data, HOME action or release
publication is authorized. RUN-0009 remains the release procedure owner;
source-only additions create no deployment workflow or scanner.

## Risks and Recovery

### Risks and Rollback

Recover retired source through the logical Git commit. Preserve frozen records
and existing tag refs. Reject scope drift, missing continuing owners, duplicate
execution, failed required validation or important review findings. Missing
remote authorization blocks that operation only. No release, deployment, secret
or remote-protection mutation is implied by source validation.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-qa-scope-and-delivery-rationalization.md)
- [Hosted contract and tier 13 hardening task](tasks/tsk-0002-hosted-contract-and-tier13-hardening.md)

- [QA04 execution evidence and ROOT release support](tasks/tsk-0003-qa04-execution-evidence-and-root-release-support.md)
