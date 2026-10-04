---
title: "Secret Layout and Environment Parity Task"
version: "1.0.4"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-05"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0004"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-03"
---

# Secret Layout and Environment Parity Task

## Objective

Reconcile the entire secret tree and its source consumers under the user's
2026-10-03 explicit request. Consolidate common/communication and
surreal_db/surrealdb duplicates, group credentials by service and DB instance,
and preserve actual values and issued IDs. This is a source and value-preserving
path operation; HOME recreation, credential rotation and deletion remain
separate.

## Inputs

Main baseline `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`, integrated
secret-layout commit `8df1e89fce0b3bea1f5f3241b95af5c8fefb8fd3`, public
registry, literal Compose/entrypoint consumers and key-only env comparison.
Private values are consumed only by approved local execution tools, never
printed, searched, included in fixtures or copied to this receipt.

## Work Log

The user authorized the entire auth, automation, backup, certs, common,
communication, data, db, labs, observability, security, storage and tools tree.
Exact source writers are `docker-compose.yml`, `.gitignore`,
`secrets/README.md`, `secrets/SENSITIVE_ENV_VARS.md.example`, empty tracked
secret directory markers, path literals and metadata-only public-source
selection in `scripts/operations/gen-secrets.sh`, and
`tests/validation/test_secret_metadata_sync.py`. Closure also touched the
existing SPEC identity high-water pair in `docs/99.templates/registry.json`,
the existing test-owner lists in `.github/workflow-contract.yml`, fixed-selector
regression `tests/lib/gate/test_github_workflow_contract.py`, selected public
operations documents and exact renamed path consumers. Root/LAB actual env and
private registry are ignored execution inputs; public examples own their key
sets. Any key rename must update both examples, actual assignments and all
source consumers atomically without guessing a value.

Every old/new pair is checked for regular-file identity and metadata before
value-preserving relocation. Legacy paths remain compatibility hardlinks while
main consumers still name them. Removing an alias is a separate post-cutover
operation; no currently mounted inode is destroyed. Backup/snapshot/custody and
certificate artifacts are distinct from generated Docker secrets and are not
removed as registry orphans. DB directories follow actual endpoint consumers;
IDs retain their semantic meaning. The combined creation/update column records
the current metadata review date for a moved path; it does not assert that the
unchanged credential bytes were newly issued.

On 2026-10-03 a read-only child improperly included private registry value
cells for AI-003 and COMM-001/002/003/004/006 in its tool output. The child
context was quarantined; root received only sanitized IDs and command scope.
Independent security review found no evidence of Git, document or runtime
propagation. The user subsequently approved resuming value-preserving path
moves and metadata sync while reserving rotation for a separate plan. No
exposed values or original output are stored in this package.

## Verification Evidence

Root key comparison: 212 actual/example keys, no missing/extra/duplicate keys.
LAB comparison: 48 keys, no missing/extra/duplicate keys. Empty LAB data,
cluster-ID, certificate and Locust paths retain their unapproved-runtime status;
no fabricated value is supplied. `_PIP_ADDITIONAL_REQUIREMENTS` is intentionally
empty.

### Closure source evidence imported during 2026-10-04 integration

Closure commit `451b1ec7e4c5509e088a17c9c0f33e3dab93ddd7` preserved the
following historical source evidence. PR359 carries the source side, current
static QA and the protected parity receipt below.

| Evidence | Result | Limit |
| --- | --- | --- |
| Path-only verification | HISTORICAL PASS | 90 identity pairs and 84 new canonical hardlinks verified without reading secret values; OpenBao custody added one non-registry service-sidecar pair. |
| Compatibility aliases | HISTORICAL PASS | Previous paths remain compatibility aliases until current main consumers are switched. Removing aliases remains separate. |
| Metadata tool value preservation | HISTORICAL PASS | Direct precheck exited 1 for one drifted file; sync and final prune-check exited 0, `files_changed=0`, values preserved. |
| Protected backup comparison | HISTORICAL PASS | 138 private value cells and 212 shared root env assignments unchanged. Values were not printed in this Task. |
| Canonical registered files | HISTORICAL PASS | 105 canonical registered files exist as regular files and are Git-ignored. Root/LAB key sets remain 212/48 with no missing, extra or duplicate keys. |
| Focused secret tests | HISTORICAL PASS, 43/43 | Synthetic/source tests only; no HOME recreation, rotation or service restart. |
| First integrated changed gate | HISTORICAL PARTIAL | First exited 1 for SPEC high-water mismatch, then passed 629 document regressions and 239 integrated tests after ledger reconciliation. Later found two temporary checkout permissions, normalized to 0755 while preserving contents/Git mode. |
| Registered-plan tail | HISTORICAL PASS | Missing test owners and stale required selector were corrected without weakening profiles, skip scope or validator strength. Final tail from `leaf.workflow-contract-regressions` exited 0, including 175 repository-integrity tests. |
| Complete changed command | HISTORICAL NONZERO | The full changed command itself did not return 0; previous successful stages plus corrected tail formed the bounded final source evidence. |
| Runtime skips | NOT_RUN | HOME recreation, credential rotation/reissue, service restart, irreversible alias deletion and live secret/log inspection remain excluded. |

The automatic approval review rejected copying private registry/env inputs to a
temporary worktree because that duplicated real secret values. That approach was
abandoned. The metadata tool instead consumes only public sources from the
reviewed worktree while keeping every private input/output in the owner checkout.
The public-source root remains an owner-approved immutable input; the tool does
not attest repository identity or defend concurrent same-user mutation.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1, 4, 8 | W1/W5 | PASS: approved source, value-preserving path/metadata and protected parity evidence recorded; HOME recreation and rotation excluded | [Secret ownership and consumer contract](../../../../secrets/README.md) |

## Review Evidence

Independent incident review is recorded above. Closure-side independent
public-source security review approved owner direct sync; it reran 43 secret
regressions, shell syntax and diff hygiene, all exit 0. No private value was
read by that reviewer. Two minor source-root trust/TOCTOU limits are recorded in
the verification receipt. On 2026-10-03 the independent security reviewer also
reran 32 quality/object regressions, `py_compile` and diff hygiene after
rejecting ambient AWS CLI resolution, weak credential permissions and partial
restore publication. The two Medium findings were resolved; actual SeaweedFS
execution remains NOT_RUN. Independent current integration review returned PASS.

## Commit Ledger

Baseline `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`; predecessor
secret-layout integration `8df1e89fce0b3bea1f5f3241b95af5c8fefb8fd3`;
closure `451b1ec7e4c5509e088a17c9c0f33e3dab93ddd7`; PR359 delivery `467bd644b071f9dfa02ca1af2d622502c3445d28`; CI `required CI run37180461557 PASS`. Remote publication and merge are recorded only by the protected delivery receipt.

## Rulings

No key/token/password regeneration, HOME start/restart, private-log inspection,
secret rotation or irreversible alias/backup deletion. Synthetic tests only.
The failed registered selector regression was corrected by adding the same seven
mandatory module names to the existing expectation; independent review reran
reachability/skip-boundary tests, 2/2 exit 0, and approved the minimal workflow
registration change.

## Deferred Items

Rotate/reissue SurrealDB administrator, SMTP app password, Supabase SMTP
password, Slack webhook and Stalwart administrator credentials through a
separately approved provider/server-first plan. COMM-001 is an account identity;
its replacement depends on the selected provider procedure. Each rotation needs
selected consumers, rollback window and verification before revoking the old
credential. No current rotation or HOME execution is authorized.

### Owner-checkout candidate parity preflight

The existing owner approval for value-preserving metadata synchronization is
retained. A read-only `gen-secrets.sh --sync-metadata-prune-check` invocation
from the owner checkout consumes its private registry/root/LAB env only inside
the approved tool; `--metadata-source-root` selects this reviewed source tree's
three public examples. Output is changed-file counters only; no values, file
contents, credentials, runtime or writes are authorized by this check.
Candidate-source parity was not used as protected-main proof. Rotation remains separate.

Candidate preflight on 2026-10-04: from the owner checkout,
`bash /tmp/hyhome-0204-source-integration/scripts/operations/gen-secrets.sh
--sync-metadata-prune-check --metadata-source-root /tmp/hyhome-0204-source-integration`
exited0, `files_changed=0`, values preserved and secret files untouched. This
proved candidate public/private metadata and env exact-set parity only; no
new credential validity, file move or service recreation was claimed from it.

### Protected completion receipt — 2026-10-04

After PR359 reached protected main as `467bd644b071f9dfa02ca1af2d622502c3445d28`, the owner-checkout
`bash scripts/operations/gen-secrets.sh --sync-metadata-prune-check
--metadata-source-root /home/hyunyoun/data/hy-home.docker`
rerun recorded `exit0, files_changed=0, values=preserved, secret_files=untouched`. Combined with the Task1 source QA packet and
workflow/secret/gate tests, this completes the source/public metadata and
approved private parity contract without printing or reading secret values
outside the approved tool. HOME recreation, service restart, credential
rotation/reissue, irreversible alias deletion, private-log inspection and
credential validity remain `NOT_RUN`.
