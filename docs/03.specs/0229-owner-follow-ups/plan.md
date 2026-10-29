---
title: "Owner Follow-ups Plan"
version: "0.2.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0229-PLAN-0001"
parent_ids:
- "SPEC-0229"
created: "2026-10-10"
---

# Owner Follow-ups Plan

## Overview

Diagnose, fix or document each item, record the results and validate.

## Scope

W1 diagnoses Storybook MCP refresh errors and documents reauthentication;
W2 adjusts the Grype seed cap and scans the two pinned AI images offline;
W3 documents stdin-only snapshot-token issuance in RUN-0021. W4 validates
these owner follow-ups without changing image pins, global Codex settings
or holding the OpenBao admin token.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Keycloak event analysis and GDE-0101 note | None | TSK-0001 | Task evidence |
| W2 | 2 | Grype cap, database download and offline scans | None | TSK-0001 | Task evidence |
| W3 | 3 | RUN-0021 snapshot-token commands | None | TSK-0001 | Task evidence |
| W4 | 4 | Changed gate, staged style check, candidate quality, merge | W1, W2, W3 | TSK-0001 | Task evidence |

## Verification Plan

Keycloak event counts by type, client, reason and source; the seed tests; the
offline scans; a shell syntax check of the RUN-0021 block; the document
checks, the gate and the remote candidate.

## Risks and Recovery

### Risks and Rollback

- The scan findings stay open until the owner decides on newer images.
- The token commands run only with the owner's admin token; a failed proof
  leaves the new token in a side file and the backup unchanged.
- Rollback: revert the commits.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-owner-follow-ups.md)
