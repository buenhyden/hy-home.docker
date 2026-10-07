---
title: "QA Scope and Delivery Rationalization Plan"
version: "0.2.0"
type: "sdlc/plan"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-07"
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

## Verification Plan

Use focused RED/GREEN only for changed behavior and scoped registered style
checks. Derive final changed selection from the machine contract. The remote
PR run owns candidate validation excluding typed local-only leaves. The shared
runner selects necessary units, implementation fixtures and links once in its
local-only lane before submission; local development does not repeat the remote bundle or full
profile. Separate Conftest unit verify from actual corpus commands while preserving
one invocation per registered gate ID/mode and Docker prerequisite ownership.
Retire completed cutover, fixed corpus and test-only helper units only after
current semantic owners are verified. Record each actual input, result and
review separately in the Task. W2 retires remaining historical source-census
and retired-file expectations with continuing owners. W3 removes the manifest's
path-only mirror requirement, closes direct unittest admission to LOCAL, and
corrects per-file shell syntax validation. Scoped lint-only corrections retain
Conftest mode and command behavior and use registered one-file lint/syntax checks. W6 aligns full-audit and review-delta
policy. W7 validates only affected cases, manifest and read-only static/document
checks; it does not replay unchanged metadata/library aggregates or full QA.
Initial draft publication and final evidence-only records use document-minimum
checks. Generic preserved-source compatibility remains separate from historical
cutover completion evidence.

## Risks and Rollback

Recover retired source through the logical Git commit. Preserve frozen records
and existing tag refs. Reject scope drift, missing continuing owners, duplicate
execution, failed required validation or important review findings. Missing
remote authorization blocks that operation only. No release, deployment, secret
or remote-protection mutation is implied by source validation.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-qa-scope-and-delivery-rationalization.md)
