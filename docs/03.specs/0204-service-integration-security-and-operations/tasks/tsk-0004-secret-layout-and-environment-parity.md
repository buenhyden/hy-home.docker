---
title: "Secret Layout and Environment Parity Task"
version: "0.1.4"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-04"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0004"
parent_ids:
- "SPEC-0204"
- "SPEC-0204-PLAN-0001"
created: "2026-10-03"
---

# Secret Layout and Environment Parity Task

## Objective

Reconcile the entire secret tree and its source consumers under the user's
2026-10-03 explicit request. Consolidate common/communication and
surreal_db/surrealdb duplicates, group credentials by service and DB instance,
and preserve actual values and issued IDs. This is a source and value-preserving
path operation; HOME recreation, credential rotation and deletion remain separate.

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
secret directory markers, the existing SPEC identity high-water pair in
`docs/99.templates/registry.json`, the existing test-owner lists in
`.github/workflow-contract.yml` and its fixed-selector regression
`tests/lib/gate/test_github_workflow_contract.py`, path literals and metadata-only public-source selection in
`scripts/operations/gen-secrets.sh`,
and `tests/validation/test_secret_metadata_sync.py`. Public operations path
consumers are amended only for the exact renamed path: ADR-0042, GDE-0021,
GDE-0045, GDE-0096, POL-0085, RUN-0014, RUN-0021, RUN-0034, RUN-0050,
RUN-0057, RUN-0085, RUN-0089, RUN-0090, RUN-0091, RUN-0096, RUN-0097,
RUN-0098, the Crawl4AI/MLflow/dbt/JupyterLab READMEs, the Renovate systemd
unit source, and the existing Compose validation synthetic path. Root/LAB actual env and
private registry are ignored execution inputs; public examples own their key
sets. Any key rename must update both examples, actual assignments and all
source consumers atomically without guessing a value.

Every old/new pair is checked for regular-file identity and metadata before
value-preserving relocation. Legacy paths remain compatibility hardlinks while
main consumers still name them. Removing an alias is a separate post-cutover
operation; no currently mounted inode is destroyed. Backup/snapshot/custody and
certificate artifacts are distinct from generated Docker secrets and are not
removed as registry orphans. DB directories follow actual endpoint consumers;
IDs retain their semantic meaning. The combined creation/update column
records the current metadata review date for a moved path; it does not assert
that the unchanged credential bytes were newly issued.

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
empty. Actual path-only verification established 90 identity pairs and 84 new
canonical hardlinks without reading secret values; OpenBao custody added one
non-registry service-sidecar pair. All previous paths remain compatibility
aliases until current main consumers are switched. The automatic approval
review rejected copying private registry/env inputs to a temporary worktree
because that duplicated real secret values. That approach was abandoned.
The metadata tool instead consumes only public sources from the reviewed
worktree while keeping every private input/output in the owner checkout.
The owner direct precheck exited 1 for one drifted file; sync and final
prune-check exited 0, ending with files_changed=0 and values preserved.
A protected-backup comparison proved all 138 private value cells and all
212 shared root env assignments unchanged. The 105 canonical registered
files exist as regular files and are Git-ignored. Root/LAB key sets remain
212/48 with no missing, extra or duplicate keys. Focused secret tests passed
43/43; independent security review found no Critical/High/Important issue.
The public-source root remains an owner-approved immutable input; the tool
does not attest repository identity or defend concurrent same-user mutation.
The first integrated changed gate exited 1: its 629-test document
regression suite found that repository history already contains SPEC-0206
but the identity high-water was 205. The two existing ledger fields were
reconciled to 206/207; no new Spec or operations ID was issued and no
SPEC-0206 implementation was merged. The retry passed the 629 document
regressions and 239 integrated tests, then found two temporary checkout
files with group-write permission; their contents and Git 100755 modes
were preserved while checkout permissions were normalized to 0755. A
registered-plan tail retry then found eight unregistered regression
modules. They were assigned once to the existing Compose/service and
repository-integrity owners, retaining the current path-aware profiles.
Archive recovery separately reports
0 violations; this does not replace delivery or vulnerability gates.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1, 4, 8 | W1/W5 | PASS: approved source, value-preserving path/metadata and key parity scope; HOME recreation and rotation excluded | [Secret ownership and consumer contract](../../../../secrets/README.md) |

Final verification on 2026-10-04 preserved each failed gate result.
`python3 scripts/validation/run-ci-gate.py --profile changed` first exited
1 for the identity ledger, then 1 for two checkout permissions after the
629-test document and 239-test integrated suites passed. Static Compose
render passed all 67 selections. Existing `execute_execution_plan` resumed
the same registered plan at `leaf.compose-baseline-regressions`; its next
failures identified eight missing test owners and the stale required-selector
expectation. Each was corrected without changing profiles, skip scope or
validator strength. The final registered tail from
`leaf.workflow-contract-regressions`, invoked by
`python3 /tmp/hyhome-resume-gates.py`, exited 0, including 175 final
repository-integrity tests. The complete changed command did not return 0;
previous successful stages plus corrected tail provide the bounded final
source evidence. Runtime skips remain NOT_RUN. All public changes were
reviewed independently; no open implementation finding remains.

## Review Evidence

Independent incident review is recorded above. Independent public-source security review approved owner direct sync; it
reran 43 secret regressions, shell syntax and diff hygiene, all exit 0.
No private value was read by that reviewer. Two minor source-root trust/
TOCTOU limits are recorded in the verification receipt. On 2026-10-03
the independent security reviewer also reran 32 quality/object regressions,
`py_compile` and diff hygiene (all exit 0) after rejecting ambient AWS CLI
resolution, weak credential permissions and partial restore publication.
The two Medium findings were resolved; actual SeaweedFS execution remains
NOT_RUN. These synthetic checks do not inspect private values or rotate them.

## Commit Ledger

Baseline and predecessor integration are named above; the final source commit
will record the exact changed set. Remote publication and merge are not implied.

## Rulings

No key/token/password regeneration, HOME start/restart, private-log inspection,
secret rotation or irreversible alias/backup deletion. Synthetic tests only.

The failed registered selector regression was corrected by adding the same
seven mandatory module names to the existing expectation; independent review
reran reachability/skip-boundary tests (2/2, exit 0) and approved the minimal
workflow registration change.

## Deferred Items

Rotate/reissue SurrealDB administrator, SMTP app password, Supabase SMTP
password, Slack webhook and Stalwart administrator credentials through a
separately approved provider/server-first plan. COMM-001 is an account identity;
its replacement depends on the selected provider procedure. Each rotation needs
selected consumers, rollback window and verification before revoking the old
credential. No current rotation or HOME execution is authorized.
