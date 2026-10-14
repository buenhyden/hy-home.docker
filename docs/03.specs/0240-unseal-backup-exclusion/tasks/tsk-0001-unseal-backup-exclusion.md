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

The exclusion is delivered by a second pull request from branch
`claude/unseal-exclusion-apply` (rules review R2): the first pull request
carries the text, so step 5 is attested against the revised procedure on
`main`, and the exclusion merges only after that. The evidence below was
taken at commit `27d84d9ab`, which held both.

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
  names the host Restic copy (BKP-002) and the R2 copy (BKP-003), says each
  key with its repository meets the threshold, that copies last until the
  owner deletes them, and records the 2026-10-14 decisions without closing
  the exception.
- ADR-0042 (0.2.3): the context adds the R2 copy, the same exposure and the
  decisions; the decision itself is unchanged.
- RUN-0085 (0.9.0): the custody procedure keeps BKP-003 apart from Cloudflare
  account access as well (review N1), defines a place as a separately
  credentialed or physically held unit (N2), says copy throughout (L1), adds
  a Cloudflare account row to the confirmation table, states the merge gate
  for the exclusion, and plans W1b unseal rekey right after W1 with
  hidden-prompt input, `-verify`, a cancel path, no `-backup`, and new shares
  never written to the host; W1b is BLOCKED until a reviewed protected output
  path exists.

### Review Round 1

On 2026-10-14 the independent `iac-reviewer` passed the exclusion and the
`security-auditor` returned FAIL; both found that a rekey does not stop a
pre-rekey Raft snapshot from opening with the old shares, and that the
protected Raft snapshot `secrets/backup/openbao/pre-change.snap` sits beside
the share file in the same host set. The text now moves the rekey to W1b,
before W2 and W3 take new snapshots, states that the exposure ends only when
pre-exclusion host snapshots are deleted from the local and R2 repositories,
corrects the retention wording (30-day bucket lock; 12 months is the
owner-run `forget-prune` policy), keeps the host file and those snapshots
until W1 or a restore proves the off-host shares, names the local repository
with BKP-002, adds Cloudflare account access to step 5, and points RUN-0021's
host restore to off-host custody for the share file.

The `rules-engineer` review of `27d84d9ab` returned FAIL on two items: the
runbook still said the host set had no exclusion (R1, fixed above), and the
merge gate held the revised procedure back until after the attestation that
depends on it (R2). The delivery is split as W1 records. Its advisories are
applied: ADR-0042 traceability links SPEC-0240, and the restore and set
descriptions that change with the exclusion travel in the second pull
request.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Exclusion test | 1 | W1 | Compose baseline tests with the new test (112, 30 skipped) | Branch on `c96d46112` | PASS | W1 Host Exclusion | - |
| Dry run | 1 | W1 | Pinned Restic image `--dry-run` on a synthetic tree, with and without the exclude file | Branch on `c96d46112` | PASS | W1 Host Exclusion | - |
| IaC review | 3 | W3 | Independent `iac-reviewer` review of `27d84d9ab`: exclusion PASS, document notes | `27d84d9ab` | PASS | Review Round 1 | - |
| Security review | 3 | W3 | Independent `security-auditor` review of `27d84d9ab`: rekey semantics and retention wording wrong | `27d84d9ab` | FAIL | Review Round 1 | - |
| Rules review | 3 | W3 | Independent `rules-engineer` review of `27d84d9ab`: stale runbook sentence; merge gate holds the procedure back | `27d84d9ab` | FAIL | Review Round 1 | - |
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
