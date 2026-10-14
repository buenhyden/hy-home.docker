---
title: "Unseal Share File Out of Host Backups Task"
version: "0.2.4"
type: "sdlc/task"
status: "superseded"
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
  Later that day the owner stated that one administrator holds every place,
  asked to change POL-0085 and RUN-0085 to fit, and chose "3곳, 조건부".
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

On that branch, `infra/09-platform-ops/restic/sets/host-exclude.txt` excludes
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
  never written to the host; W1b was BLOCKED until a reviewed protected output
  path existed. RUN-0085 0.10.3 (PR #472) now gates W1b on PGP preparation
  instead; contract 4 still holds.

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
with BKP-002, adds Cloudflare account access to step 5, and, on the exclusion
branch, points RUN-0021's host restore to off-host custody for the share file.

The `rules-engineer` review of `27d84d9ab` returned FAIL on two items: the
runbook still said the host set had no exclusion (R1, fixed above), and the
merge gate held the revised procedure back until after the attestation that
depends on it (R2). The delivery is split as W1 records. Its advisories are
applied: ADR-0042 traceability links SPEC-0240, and the restore and set
descriptions that change with the exclusion travel in the second pull
request.

### W5 Single-Administrator Places

The four-place layout (three shares and a share-free place for BKP-003) was
written for separation between places, not people, and the owner is the only
administrator. The owner chose three places with a condition. RUN-0085
(0.10.0) now says that the unit is a place, not a person, so three places,
one share each, are the minimum; BKP-003 stays apart from the R2 credentials
and Cloudflare account access and normally from every share, and may join one
share only after a new host snapshot confirms the exclusion (criterion 4) and
listings of both repositories show no pre-exclusion host snapshot. Until
then the first storage still needs a fourth, share-free place. A place's opening means
(master password, media passphrase, key location) may not be stored in
another place. The step 5 table and verdict accept the conditional placement
only with those two records. POL-0085 (0.6.0) records the decision and keeps
the exception open.

### W5 Review Round 1

Independent reviews of `f9b04c1ac` on 2026-10-14 both returned FAIL.

- `rules-engineer`: the share rows of the step 5 table could not answer
  "offsite key와 장소가 다른가" for the share beside BKP-003, so the verdict
  failed the layout it was meant to allow; the W1 and W1b approvers still read
  "share 보유자 2명"; criterion 5 asked POL-0085 to state the rule it only
  records; the Plan still said two pull requests; this Evidence lacked a
  commit and review rows. All fixed; a moved BKP-003 now requires step 5
  again.
- `security-auditor`: the daily `restic copy` re-uploads any pre-exclusion
  snapshot still in the local host repository, so an R2-only deletion is
  undone the next day; a deletion record proves an action, not the state;
  `prune` keeps some unused space by default; no tracked tool deletes
  selected snapshots. Condition (2) now requires that neither repository
  holds a pre-exclusion host snapshot, proved by value-free listings taken
  after a later daily copy, with `prune --max-unused 0`, and says that this
  needs new reviewed tooling or the retention period. Notes applied: the
  table asks whether a place's opening means is stored elsewhere, a
  reappearing file sends BKP-003 back to a share-free place, "with R2 read
  access" is stated, and "SPEC-0240 기준 4" replaces the ambiguous "W4".

### W5 Review Round 2

Re-reviews of `fc2a62155` on 2026-10-14: `security-auditor` PASS with notes
and `rules-engineer` PASS with notes; every Round 1 finding was confirmed
fixed. Notes applied: RUN-0085 no longer says the old snapshots can be deleted
right after the lock period, it points to condition (2); the TSK-0006 entry
moved into date order. Left as a recommendation: a reviewed deletion tool
could also confirm with `restic check` that no pre-exclusion data remains.

### Review Round 2

Re-reviews on 2026-10-14 of the current `main` text and branch
`claude/unseal-exclusion-apply-v2` (`8a693bf4d`): `security-auditor` PASS with
notes and `rules-engineer` PASS with notes; every Round 1 finding is fixed.
Notes applied: the main Task no longer states branch content as current;
this summary of W1b follows RUN-0085 0.10.3; RUN-0021 and
`hyhome-backup.sh` name the shares an older Raft snapshot opens with, and
RUN-0085 requires the third share's off-host copy to be proven before any
deletion, since W1 and `-verify` each use two shares (both in their branches).
The criterion 2 document checks ran on `main` `fae77e14d`: changed metadata
for POL-0085, ADR-0042 and RUN-0085 with 0 violations, links `--mode all`
PASS and markdownlint 0.

### Owner Withdrawal — 2026-10-14

After reviewing the step 5 custody table, the owner, the only administrator,
chose (AskUserQuestion) to keep the shares and the CA key on the host and in
the host backup, to keep only BKP-003, the R2 credentials, BKP-002 and
Cloudflare account access off the host, and to drop the W1b rekey. SPEC-0242
carries that. This package's exclusion (W1, branch
`claude/unseal-exclusion-apply-v2`), its merge gate and criterion 4 are
therefore withdrawn and will not merge; the W5 place rule is replaced. The
same day the owner chose `superseded` by SPEC-0242 for this package, to take
effect once SPEC-0242 is merged and approved, when the package leaves Stage
03; the exclusion branches are deleted.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0240 | draft | superseded | #owner-withdrawal--2026-10-14 |
| SPEC-0240-PLAN-0001 | draft | superseded | #owner-withdrawal--2026-10-14 |
| SPEC-0240-TSK-0001 | draft | superseded | #owner-withdrawal--2026-10-14 |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Exclusion test | 1 | W1 | Compose baseline tests with the new test (112, 30 skipped) | Branch on `c96d46112` | PASS | W1 Host Exclusion | - |
| Dry run | 1 | W1 | Pinned Restic image `--dry-run` on a synthetic tree, with and without the exclude file | Branch on `c96d46112` | PASS | W1 Host Exclusion | - |
| IaC review | 3 | W3 | Independent `iac-reviewer` review of `27d84d9ab`: exclusion PASS, document notes | `27d84d9ab` | PASS | Review Round 1 | - |
| Security review | 3 | W3 | Independent `security-auditor` review of `27d84d9ab`: rekey semantics and retention wording wrong | `27d84d9ab` | FAIL | Review Round 1 | - |
| Rules review | 3 | W3 | Independent `rules-engineer` review of `27d84d9ab`: stale runbook sentence; merge gate holds the procedure back | `27d84d9ab` | FAIL | Review Round 1 | - |
| Place rule text | 5 | W5 | Changed metadata, markdownlint and links for RUN-0085, POL-0085 and this package | `f9b04c1ac` | PASS | W5 Single-Administrator Places | - |
| Rules review W5 | 5 | W5 | Independent `rules-engineer` review: table rejects the allowed layout; stale approver wording; criterion wording | `f9b04c1ac` | FAIL | W5 Review Round 1 | - |
| Security review W5 | 5 | W5 | Independent `security-auditor` review: daily copy re-uploads deleted R2 snapshots; deletion record is not state proof | `f9b04c1ac` | FAIL | W5 Review Round 1 | - |
| Security re-review W5 | 5 | W5 | Independent `security-auditor` re-review: PASS with notes, notes applied | `fc2a62155` | PASS | W5 Review Round 2 | Security review W5 |
| Rules re-review W5 | 5 | W5 | Independent `rules-engineer` re-review: PASS with notes, notes applied | `fc2a62155` | PASS | W5 Review Round 2 | Rules review W5 |
| Place rule checks | 5 | W5 | Changed metadata, markdownlint and links on the final text | Branch after `fc2a62155` | PASS | W5 Review Round 2 | - |
| Text checks | 2 | W2 | Changed metadata for POL-0085, ADR-0042 and RUN-0085 (0 violations); links `--mode all` PASS; markdownlint 0 | `fae77e14d` | PASS | Review Round 2 | - |
| Security re-review | 3 | W3 | Independent `security-auditor` re-review of the Round 1 fixes: PASS with notes, notes applied | `main` and `8a693bf4d` | PASS | Review Round 2 | Security review |
| Rules re-review | 3 | W3 | Independent `rules-engineer` re-review of the Round 1 fixes: PASS with notes, notes applied | `main` and `8a693bf4d` | PASS | Review Round 2 | Rules review |
| Merge gate | 4 | W4 | RUN-0085 step 5 `owner-attested` before merge | - | NOT_RUN | Work Log | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 1 | accepted | Exclusion test, Dry run | Owner accepted 2026-10-14 |
| 2 | accepted | Text checks | Owner accepted 2026-10-14 |
| 3 | accepted | IaC review, Security re-review, Rules re-review | Owner accepted 2026-10-14 |
| 4 | pending | - | - |
| 5 | accepted | Place rule text, Security re-review W5, Rules re-review W5, Place rule checks | Owner accepted 2026-10-14 |

## Review and Completion

Withdrawn 2026-10-14, see Owner Withdrawal: the exclusion will not merge. Before that, on 2026-10-14 the owner, answering the review question (AskUserQuestion), accepted criteria 1 and 5. After the Round 2
re-reviews the owner accepted criteria 2 and 3 the same day. Criterion 4 can no
longer be met; its disposition goes with the package's.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
