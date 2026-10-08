---
title: "Compose Container and Host Naming Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-08"
layer: "specs"
artifact_id: "SPEC-0216-PLAN-0001"
parent_ids:
- "SPEC-0216"
created: "2026-10-08"
---

# Compose Container and Host Naming Plan

## Overview

Land the rule, its exceptions and its test with the Compose edits in one
commit, update the documents that name containers, then recreate the affected
HOME containers after the merge.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1, 3 | Add the rule, exception entries, test and Compose edits | None | TSK-0001 | Task evidence |
| W2 | 2 | Update operations documents and READMEs to current container names | W1 | TSK-0001 | Task evidence |
| W3 | 4 | Recreate affected HOME containers from the merged source | W1, W2 | TSK-0001 | Task evidence |

## Verification Plan

Run the regression test against the previous Compose files (RED) and the
edited ones (GREEN), the full Compose validation, the changed-profile local
gate and the staged lint. Remote PR `candidate-quality` owns candidate
acceptance. HOME recreation keeps named volumes and checks health and
Prometheus targets afterwards.

## Risks and Rollback

Renaming a container drops the old name from Docker DNS. A search found the
old names only in Compose files, documents and READMEs, not in configuration
or scripts. Revert the commits and recreate the services to restore the old
names; volumes are untouched either way.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-compose-container-and-host-naming.md)
