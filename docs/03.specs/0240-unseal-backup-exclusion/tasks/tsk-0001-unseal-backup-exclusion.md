---
title: "Unseal Share File Out of Host Backups Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-14"
layer: "specs"
artifact_id: "SPEC-0240-TSK-0001"
parent_ids:
- "SPEC-0240-PLAN-0001"
created: "2026-10-14"
---

# Unseal Share File Out of Host Backups Task

## Objective

Keep the OpenBao unseal share file out of the host backup and its R2 copy,
and correct the text that called it the only copy, as SPEC-0240 states.

## Inputs and Authorization

- **Request:** on 2026-10-14 the owner asked to review and proceed with the
  security finding (H1) from the PR #461 review, then chose in
  AskUserQuestion "백업 제외 + rekey" and, for POL-0085, "사실대로 정정".
- **Baseline:** `main` `c96d46112`.
- **Not done:** no rekey, no deletion of the host file or of any snapshot, no
  HOME backup run, no secret read. The synthetic dry run used invented files.

## Work Log

### W1 Host Exclusion

`infra/09-platform-ops/restic/sets/host-exclude.txt` now excludes
`/src/host/secrets/security/openbao/openbao_unseal_keys.txt`, the path the
Restic job mounts `secrets/` under, and keeps its comment explaining why. A
new test in `tests/validation/test_compose_baseline_gates.py` pins the
exclusion list to that one path.

A dry run of the pinned `restic/restic:0.19.1` image on a synthetic tree
(invented `openbao_unseal_keys.txt`, a sibling `other.txt` and
`backup/x.txt`, network none, a throwaway repository) with the tracked
exclude file listed only `other.txt` and `x.txt` as new; without it, all
three. A first attempt mounted the tree one level too deep and proved
nothing; it is not counted.

### W2 Policy, Decision and Runbook Text

- POL-0085 (0.5.6): the exception no longer calls the file the only copy. It
  names the host Restic copy (BKP-002) and the R2 copy (BKP-003, bucket lock,
  up to 12 months), says BKP-003 with R2 read access meets the threshold, and
  records the 2026-10-14 decisions without closing the exception.
- ADR-0042 (0.2.3): the context adds the R2 copy, the same exposure and the
  decisions; the decision itself is unchanged.
- RUN-0085 (0.9.0): the custody procedure keeps BKP-003 apart from Cloudflare
  account access as well (review N1), defines a place as a separately
  credentialed or physically held unit (N2), says copy throughout (L1), adds
  a Cloudflare account row to the confirmation table, states the merge gate
  for the exclusion, and plans W9 unseal rekey in a separate window with
  hidden-prompt input, verification before the new shares apply, and new
  shares never written to the host; W9 is BLOCKED until a reviewed protected
  output path exists.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Exclusion test | 1 | W1 | Compose baseline tests with the new test (112, 30 skipped) | Branch on `c96d46112` | PASS | W1 Host Exclusion | - |
| Dry run | 1 | W1 | Pinned Restic image `--dry-run` on a synthetic tree, with and without the exclude file | Branch on `c96d46112` | PASS | W1 Host Exclusion | - |
| Merge gate | 4 | W4 | RUN-0085 step 5 `owner-attested` before merge | - | NOT_RUN | Work Log | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 1 | pending | - | - |
| 2 | pending | - | - |
| 3 | pending | - | - |
| 4 | pending | - | - |

## Review and Completion

Do not merge before RUN-0085 step 5 is `owner-attested`. No criterion is
accepted until the owner accepts it.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
