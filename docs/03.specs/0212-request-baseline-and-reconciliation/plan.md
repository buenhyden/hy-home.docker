---
title: "Request Baseline and Reconciliation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-07"
layer: "specs"
artifact_id: "SPEC-0212-PLAN-0001"
parent_ids:
- "SPEC-0212"
created: "2026-10-07"
---

# Request Baseline and Reconciliation Plan

## Overview

Record the baseline and inventory from read-only observation, publish the
selection decision, then hand off to the follow-on packages in dependency
order. This package changes documents and the Registry only.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Read local/remote main, Project-Template main and the pack baseline | None | TSK-0001 | Task evidence |
| W2 | 2 | Assign each request item a disposition and owning prompt | W1 | TSK-0001 | Task evidence |
| W3 | 3, 4 | Render root and LAB models and probe profile selection | W1 | TSK-0001 | Task evidence |
| W4 | 5 | Map conflicting rules to follow-on owners and publish ADR-0047 | W2, W3 | TSK-0001 | Task evidence |
| W5 | 6 | Record QA selection and remote protection, then validate this change | W4 | TSK-0001 | Task evidence |

## Verification Plan

Run the registered changed-profile local gate on the final diff, first with
`--explain` to record the selection and then without it. Re-render the root
and LAB models with the recorded commands for any recheck. Remote PR
`candidate-quality` owns candidate acceptance. No container, image build,
data operation or secret read is part of this package.

Follow-on order is prompt 12, then 01 and 03, then 02, 04 and 05, then 06 and
07, then 08. Prompts 09 and 10 are independent discovery work. Prompt 11
applies at each package's merge. Shared writers: the Registry, the Stage 03
README and `.github/workflow-contract.yml` take one writer at a time, and
`infra/common-optimizations*` belongs to prompt 05 alone.

## Risks and Rollback

The inventory is a source model rendered from the public example. HOME may
differ, so runtime facts stay `NOT_RUN` until they are observed. Revert the
logical commit to withdraw this package. The Registry numbers it issued stay
issued and are not reused.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-request-baseline-and-inventory.md)
