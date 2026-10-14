---
title: "Single-Administrator OpenBao Custody Task"
version: "0.1.1"
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
- **Baseline:** `main` `4421d30f1` (the PR #476 merge).
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

### W3 Review Round 1

Independent reviews of `3eb6d360f` on 2026-10-14:

- `security-auditor` PASS with notes. Applied: the R2 account ID and bucket
  name join account A, since `.env` is inside the R2 copy; step 3 checks the
  account A values with a read-only R2 snapshot listing from hidden input,
  because step 6 uses the host's copies; the exposure adds what the account's
  Cloudflare access and writable R2 tokens can destroy; "recover everything
  from R2" is stated as intended, not proven; the account's recovery means and
  second factor stay offline and off the host; RUN-0021 no longer asks for
  BKP-001 in offline custody; ADR-0042 names Cloudflare access and the open
  exception.
- `rules-engineer` FAIL on R1: RUN-0085's window and P06 lines, POL-0085's P06
  gate and RUN-0098 still required "independent custody", which the new
  section no longer defines. They now point to the step 5 record. Notes
  applied: SPEC-0240's Task no longer reads as live merge instructions, its
  README row says it was withdrawn, TSK-0006 keeps its old custody row as
  history, this Task names its baseline and commits, and the Spec scope lists
  these consumers.

### W3 Review Round 2

The `rules-engineer` re-review of `31c218d71` passed with notes: every gate
that named independent custody now points to the step 5 record. Notes
applied: contracts 2 to 4 now own what step 5 contains (the R2 identifiers,
the listing with the account's values, the destructive exposure, recovery as
intended), and POL-0085 names the non-secret R2 identifiers.

### W4 Step 5 Record

On 2026-10-14 the owner returned the step 5 table and clarified that the
backup and R2 values are on a separate desktop rather than in the password
manager account, which holds Cloudflare access. Contract 2, RUN-0085 (0.12.2)
and POL-0085 (0.7.1) now name the off-host place as a password manager
account or the owner's separate desktop. Every answer was yes, so SPEC-0204
TSK-0006 records step 5 as `PASS`, owner-attested.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Runbook checks | 1 | W1 | Changed metadata (9 documents) 0 violations; links `--mode all` PASS; markdownlint 0; operations catalog tests OK | `3eb6d360f` | PASS | W1 Runbook | - |
| Record checks | 2 | W2 | Same checks over POL-0085, ADR-0042 and the SPEC-0240 and TSK-0006 records | `3eb6d360f` | PASS | W2 Policy and Decision Record | - |
| Security review | 3 | W3 | Independent `security-auditor`: PASS with notes, notes applied | `3eb6d360f` | PASS | W3 Review Round 1 | - |
| Rules review | 3 | W3 | Independent `rules-engineer`: undefined "independent custody" gates | `3eb6d360f` | FAIL | W3 Review Round 1 | - |
| Rules re-review | 3 | W3 | Independent `rules-engineer` re-review: PASS with notes, notes applied | `31c218d71` | PASS | W3 Review Round 2 | Rules review |
| Round 2 checks | 1 | W1 | Changed metadata (11 documents) 0 violations; links `--mode all` PASS; markdownlint 0 | Branch after `31c218d71` | PASS | W3 Review Round 2 | - |
| Step 5 record | 4 | W4 | owner-attested step 5 table recorded in TSK-0006: every answer yes, R2 listing with the off-host values passed | Owner statement 2026-10-14 | PASS | W4 Step 5 Record | - |

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
