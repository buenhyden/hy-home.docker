---
title: "Single-Administrator OpenBao Custody Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-14"
layer: "specs"
artifact_id: "SPEC-0242-TSK-0001"
parent_ids:
- "SPEC-0242-PLAN-0001"
created: "2026-10-14"
---

# Single-Administrator OpenBao Custody Task

## Objective

Keep OpenBao custody on the host for a single administrator, with only the
backup and R2 keys off the host, as SPEC-0242 states.

## Inputs and Authorization

- **Request:** on 2026-10-14 the owner asked to review the maintenance window
  and the step 5 custody table, then answered "secrets/security/ 폴더내 배치"
  and, in AskUserQuestion, chose "host에 두는 정책 원함", "host + key만 외부",
  "W1b 빼기", and for the password manager account BKP-003, the R2
  credentials, BKP-002 and Cloudflare account access, adding that a backup
  copy goes to `/home/hyunyoun/data/hy-home.secrets`.
- **Baseline:** `main` `f0984f3c0`, with PR #476 underneath.
- **Not done:** no HOME change, no secret or second-copy read. Only the
  directory's metadata was read: root-owned, mode 0700, on the same system
  disk as the repository.

## Work Log

### W1 Runbook

RUN-0085 (0.11.0) replaces the off-host separation procedure with a
single-administrator custody section: a layout table, the accepted exposure,
a four-step procedure and a value-free step 5 table whose verdict is `PASS`
with a Check starting "owner-attested". Step 5 in the HOME order and the
window precondition point to it. The W1b rekey section and its table row are
replaced by a statement that this window does not rekey. W3b refers to the
step 5 record. W0's image check now greps `^hy-home/openbao`, which the
Compose pin uses; the old pattern matched nothing, so W0 always failed. A
missing image is re-imported from the reviewed OCI archive, since it cannot
be pulled.

### W2 Policy and Decision Record

POL-0085 (0.7.0) records the reversal and the accepted exposure and keeps the
exception open. ADR-0042 (0.2.4) updates its context and links this Spec.
SPEC-0240's Task records the withdrawal; its disposition is left to the
owner.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Runbook checks | 1 | W1 | Changed metadata (9 documents) 0 violations; links `--mode all` PASS; markdownlint 0; operations catalog tests OK | Branch | PASS | W1 Runbook | - |
| Record checks | 2 | W2 | Same checks over POL-0085, ADR-0042 and the SPEC-0240 and TSK-0006 records | Branch | PASS | W2 Policy and Decision Record | - |
| Step 5 record | 4 | W4 | Owner step 5 statement in TSK-0006 | - | NOT_RUN | Work Log | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 1 | pending | - | - |
| 2 | pending | - | - |
| 3 | pending | - | - |
| 4 | pending | - | - |

## Review and Completion

No criterion is accepted until the owner accepts it.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
