---
title: "Single-Administrator OpenBao Custody Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-14"
layer: "specs"
artifact_id: "SPEC-0242-PLAN-0001"
parent_ids:
- "SPEC-0242"
created: "2026-10-14"
---

# Single-Administrator OpenBao Custody Plan

## Overview

Rewrite the custody text in one pull request, review it, then record the
owner's step 5 statement.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | RUN-0085 custody section, step 5 record and window lines | None | TSK-0001 | Task evidence |
| W2 | 2 | POL-0085 exception and ADR-0042 context | None | TSK-0001 | Task evidence |
| W3 | 3 | Independent security and rules reviews; document checks | W1, W2 | TSK-0001 | Task evidence |
| W4 | 4 | Record the owner's step 5 statement in TSK-0006 | W3 | TSK-0001 | Task evidence |

## Verification Plan

Run changed metadata, links `--mode all`, markdownlint and the operations
catalog tests; obtain independent `security-auditor` and `rules-engineer`
reviews of the branch.

## Risks and Rollback

- **One account holds every key.** A compromise of the password manager
  account exposes the R2 copy, every secret and every share. Accepted by the
  owner; the account's recovery means stay out of it and off the host.
- **Host loss.** Recovery needs that account and R2 access; the host second
  copy does not help.
- **Rollback.** Revert the text; SPEC-0240's separated layout and exclusion
  branch remain available.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-single-admin-openbao-custody.md)
