---
title: "Single-Administrator OpenBao Custody"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-14"
layer: "specs"
artifact_id: "SPEC-0242"
parent_ids:
- "REQ-0003"
- "AD-0004"
- "ADR-0041"
- "ADR-0042"
created: "2026-10-14"
---

# Single-Administrator OpenBao Custody

## Overview

The owner is the only administrator. On 2026-10-14, after reviewing the
off-host custody step, the owner chose (AskUserQuestion) to keep the OpenBao
unseal shares and the CA key on the host, in `secrets/` and an owner-made
root-only second copy at `/home/hyunyoun/data/hy-home.secrets`, and in the
host Restic backup, and to keep only BKP-003, the R2 credentials, BKP-002 and
Cloudflare account access off the host, in one password manager account. The
owner also chose to drop the W1b unseal rekey. This withdraws SPEC-0240's
backup exclusion, rekey and place separation.

## Scope

In scope: RUN-0085's custody section, its step 5 record and verdict, the
maintenance window's W1b and the W0 and W3b lines that depend on custody or
the image pin, POL-0085's exception text and ADR-0042's context, the consumers that
named independent custody as a gate (RUN-0021, RUN-0098, POL-0085's P06 line),
and the withdrawal and pointer records in SPEC-0240's Task and SPEC-0204
TSK-0006. Out of scope:
any HOME change, credential handling, reading the second copy, the rest of the
window's readiness, and SPEC-0240's lifecycle disposition.

## Contracts

1. The shares and the CA key stay on the host and in the host backup, local
   and R2. The host second copy is on the same system disk and is not
   off-host storage.
2. BKP-003, the R2 credentials, BKP-002 and Cloudflare account access are kept
   off the host in one password manager account, whose recovery means are
   kept neither in that account nor on the host.
3. The accepted exposure is stated: that one account opens the R2 copy with
   every secret and share, and one reader of the host meets the threshold.
   The POL-0085 exception stays open.
4. Step 5 is a value-free owner record of those four keys, the second copy and
   the account's recovery means, recorded as `PASS` with a Check that starts
   "owner-attested"; an empty cell is `NOT_RUN` and any "아니오" is `FAIL`.
5. The window has no W1b rekey; W3b refers to the step 5 record; the W0 image
   check matches the Compose pin and a missing image is re-imported, not
   pulled.

## Acceptance Criteria

1. RUN-0085 states contracts 1, 2, 4 and 5 and the exposure of contract 3.
2. POL-0085 and ADR-0042 record the decision and keep the exception open.
3. Independent security and rules reviews find nothing blocking, and the
   document checks pass.
4. The owner's step 5 record is in SPEC-0204 TSK-0006 as `PASS`.

## Related Documents

- [REQ-0003](../../01.requirements/0003-security.md)
- [AD-0004](../../02.architecture/descriptions/0004-data-architecture.md)
- [ADR-0041](../../02.architecture/decisions/0041-offsite-backup-target.md)
- [ADR-0042](../../02.architecture/decisions/0042-openbao-unseal-method.md)
- [SPEC-0240](../0240-unseal-backup-exclusion/spec.md)
- [Plan](plan.md)
