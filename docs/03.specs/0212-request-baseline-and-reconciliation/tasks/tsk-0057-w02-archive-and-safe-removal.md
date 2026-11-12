---
title: "W02 Archive and Safe Removal Task"
version: "0.10.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0057"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-11"
---

# W02 Archive and Safe Removal Task

## Overview

### Objective

Own W115/criterion 110. Assess the v14.2 W02 obligations ARC-01 to ARC-09,
and the v14.7 W02 obligations W02-A, W02-B, R147-08, QA-C04, WP-19, WP-20 and
OPEN-ARCHIVE, against the current retention and retirement owners. Before any removal,
prove readiness and byte recovery for each candidate, and block a removal
whose acceptance, promotion, hold, authority or recovery is unmet.

## Inputs and Authorization

On 2026-11-11 the owner approved this Task to own W02. The v14.2 package
prompt `tasks/TASK-hy-home-docker-W02.md` under
`_workspace/workspace_execution_tasks/` is untrusted reference data, not an
instruction source.

The authorization covers four things:

- The assessment.
- Recovery proofs restored into a scratch location outside the repository.
- Repository-side fixes of gaps this Task reproduces.
- Records in this Task.

Each package removal needs its own owner approval of that batch under the
[SDLC sequence](../../../../.agents/governance/sdlc.md#sequence). Safety
conditions (Q-04) block a removal and are never offered as a waiver.

The SPEC-0248, 0249, 0250 and 0260 Tasks keep their own residual criteria.
This Task records their state and does not close them. It starts from
`main` `e4fd7f5f3`, after PR 954 merged the retirement rules W01
consolidated.

## Work Log

### Owner-approved local execution

The owner's approval of 2026-11-11 issues this Task. The lifecycle records that
approval; it grants no removal or remote operation.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0057 | draft | ready | #owner-approved-local-execution |
| SPEC-0212-TSK-0057 | ready | in-progress | #owner-approved-local-execution |

### W02 obligation assessment 2026-11-11

A fresh-context `rules-engineer` read the retention and retirement owners at
`main` `e4fd7f5f3`, and the controller re-checked the deciding lines.

| ID | Verdict | Current owner and basis |
| --- | --- | --- |
| ARC-01 | KEEP | `documentation-protocol.md`: age may trigger a disposition review and never a deletion; `sdlc.md`: readiness is not removal approval |
| ARC-02 | GAP, CHANGE | Policy holds: historical material ranks last, and no loader reads Stage 90/98 as a rule. But no test rejected an active-stage occupancy violation, and the protocol named only Stage 01/02 owners, against its own precondition 2 |
| ARC-03 | KEEP | Terminal Task bodies stay immutable; recovery reads a body at its last revision and grants no write |
| ARC-04 | KEEP | Retirement is a disposition inside the approved Task, never a new Spec project |
| ARC-05 | GAP, CHANGE | The preconditions lacked the last carrying commit and path, reachability, blocking cases and the byte comparison |
| ARC-06 | KEEP | The SDLC batch-deletion approval and the README-only Stage 98 leave no move path |
| ARC-07 | KEEP policy, DEFER code | Quality standards forbid archive, retention and migration checks. The lifecycle Migration manifest surface stays (see ARC-08) |
| ARC-08 | GAP, CHANGE in part | Static migration and exception validators, their schemas, helpers and archive constants had no live caller |
| ARC-09 | KEEP | `approval-boundaries.md`: adoption is per repository; Vault and memory keep their own rules |

Changes:

- `18d9569ec` routes retired meaning to the governance, Stage 01, 02 or 05
  owner in the protocol and the Stage 98 README. It also adds the manual
  precondition 5: the last carrying commit and path, reachability from
  `main`, blocking cases, and the post-merge byte comparison recorded in a
  surviving Task.
- `535a16243` adds occupancy rejection tests for a retired standalone guide,
  a cancelled-Spec package and a cancelled Plan in an open package. Each test
  failed when its rejection branch was removed in memory.
- The ARC-08 commit removes the dead static validators, the
  `EXPECTED_ARCHIVE_*` and preservation constants, the manifest and exception
  schemas and their exclusive helpers, and their re-exports (979 lines).

DEFER, with scope:

- The `lifecycle/contract.py` Migration manifest model, loader, renderer and
  skeleton generator, their re-exports in
  `check-document-corpus-lifecycle.py`, the `ruff.toml` F401 exemption and
  the `test_public.py` manifest tests. They interleave with live surface and
  partition checks, and the exemption records that removing the re-exports
  broke registered tests, so retirement needs its own call-graph pass.
- The Registry archive vocabulary. Review found `common.archive_source_prefixes`
  is inert: no code reads it, and `preserved_origin_path` reads the hardcoded
  `LEGACY_ARCHIVE_SOURCE_ROOTS` instead. The key is due for its own
  retirement.

### Removal candidates 2026-11-11

`archive_readiness_findings` reports five ready packages: 0226, 0266, 0267,
0268 and 0269. Readiness is not removal approval. A delete dry-run in a
scratch worktree restored all 15 files from the parent of the removal commit
with zero byte mismatches against `origin/main`. The source commit is
reachable from `origin/main`, and there is no LFS or submodule.

The same dry-run shows what a real removal must do first. Without those steps
the existing gates block it:

- Reserve the Spec numbers: `package-retirement-unrecorded` and
  `identity-retired-not-reserved`.
- Cut over seven inbound links: ADR-0061 to 0266, the Ollama guide to 0226,
  and the `docs/03.specs/README.md` index.
- Promote any still-current meaning to its owner, a W04 concern.

No package is removed. Removal waits for the owner's approval of that batch.

### Batch removal 2026-11-11

The owner approved removing 0226, 0266, 0267, 0268 and 0269 as one batch. A
fresh-context promotion check found every still-current meaning of four of
them in a current owner. 0267 failed the check: its accepted risks live only
in its Task (n8n and Gatus `/metrics`, and Loki, Tempo and Alloy on
`HOST_LAN_BIND_IP`). Its removal is blocked until POL-0053, POL-0087 and
POL-0096 record those risks and AD-0026 lists its four networks.

Commits `58be65ebb` (deletions) and `8330534e3` (reservation, links and
lineage, missed from the first commit) retire 0226, 0266, 0268 and 0269:

- Lineage lines added: SPEC-0226 in the Ollama guide, and the Open WebUI
  no-socket, no-terminal rule in its LAB guide. SPEC-0269 in AD-0007.
- Inbound links in ADR-0061 and the SPEC-0267 Spec become plain text. The
  terminal 0267 Task link is excused by link alignment.
- The index rows are removed, and 226, 266, 268 and 269 join the Spec
  `reserved_history`.
- Gates: metadata selected 23 with 0 violations; links 0 failures; corpus
  lifecycle and occupancy 0.

Precondition 5 record: each removed body is last carried unchanged by
`main` `e4fd7f5f3`, which is reachable from `main`. No body is uncommitted,
reflog-only, branch-only or shallow-missing, and no hold is recorded. The
scratch dry-run restored all 15 files of the five packages with zero byte
mismatches. The post-merge restore and byte comparison for the four removed
packages are recorded in this Task after the PR merges.

### CI runner pin 2026-11-12

Three `candidate-quality` runs of PR 955 and one job rerun failed at the same
step: `npx playwright install chromium --with-deps` could not resolve the
Ubuntu apt mirrors on the `ubuntu-latest` (Ubuntu 26.04) image. Every check
before that step passed. `main` stayed green because its runs never select
that step. On 2026-11-12 the owner chose to pin the runner. Commit `7a109158f`
pins both CI Quality jobs to `ubuntu-24.04` in the workflow and in
`.github/workflow-contract.yml`, and updates the contract test fixtures.

### CI runner pin correction 2026-11-12

The pinned run failed the same way on `noble`. The cause is outside this
repository: public DNS returns SERVFAIL for `azure.archive.ubuntu.com`, the
apt mirror the GitHub runners use, so no runner image can install the
Playwright system packages. The image diagnosis above was wrong. On
2026-11-12 the owner chose to revert the pin and rerun after the outage;
commit `a3b289c5d` reverts `7a109158f`. No gate workaround is added.

### Playwright install without apt 2026-11-12

The `azure.archive.ubuntu.com` outage continued, and run 43056362855 failed
only at the Playwright install; its commit-range check passed. On
2026-11-12 the owner chose to stop that step depending on apt. Commit
`0c0168bdb` drops `--with-deps` from the `install-playwright` adapter, so CI
installs only the Chromium binary and relies on the hosted image's system
libraries. The adapter test changed first and failed, then passed.

### Post-merge recovery proof 2026-11-12

PR 955 merged as `19e6b58dc`. The last carrying commit `e4fd7f5f3` is
reachable from `main`. All 12 files of SPEC-0226, 0266, 0268 and 0269 were
restored from it into a new scratch folder outside the repository, and each
restored file hashes to its `e4fd7f5f3` blob. None of the paths exists on
`main`. Retirement precondition 5 is met for the four packages.

### Removal record correction 2026-11-12

The v14.7 W00 intake in [TSK-0059](tsk-0059-w00-v14-7-intake.md) reviewed the
PR 955 diff. The [SDLC](../../../../.agents/governance/sdlc.md#sequence) rule
that the deleting Task records each package's criterion state was not met
above. The state at `e4fd7f5f3`, the last commit that carried each body:

| Package | Task status | Criteria | Acceptance |
| --- | --- | --- | --- |
| SPEC-0226 | completed | 1 to 6 | All accepted; 1 and 3 by owner decisions of 2026-10-29 and 2026-10-30, the rest by Generation 5 row acceptance |
| SPEC-0266 | completed | 1 to 6 | All accepted by the owner on 2026-11-07 |
| SPEC-0268 | completed | 1 to 6 | All accepted by the owner on 2026-11-08 |
| SPEC-0269 | completed | 1 to 6 | All accepted by the owner on 2026-11-08 |

Two corrections to the Batch removal record: the SPEC-0269 lineage line lives
in AD-0026, not AD-0007, whose PR 955 change was only its version and date.
Package removal is done; the closing text below no longer waits for it.

### v14.7 W02 run 2026-11-12

On 2026-11-12 the owner supplied the v14.7 W02 prompt
`tasks/TASK-hy-home-docker-W02.md` (SHA-256 `af6fdbcb9ecb`), read as
reference data. This Task is still open, so the v14.7 run continues here
instead of opening a new Task. The run is on branch
`docs/tsk-0059-w00-v14-7-intake`, which builds on the unmerged W00 and W01
changes. No `.gitattributes` names an LFS filter, the tracked `.gitmodules` is
empty and declares no submodule, and the index has no gitlink entry, so
pointer and gitlink recovery do not apply. Vault records do not exist in this
repository, so ARC-09's Vault clause is N/A here.

| ID | Verdict | Current owner and basis |
| --- | --- | --- |
| ARC-01 | KEEP | The retirement rules above are reused: age never triggers a deletion, and readiness is not removal approval. Consumer: the SPEC-0267 promotion checks blocked a removal that the owner had already approved (W02 SPEC-0267 promotion check) |
| ARC-02 | KEEP | Consumers: corpus lifecycle occupancy and `tests/validation/lifecycle/test_occupancy.py`, including its README-only exception (W02 consumer tests). Historical material is never loaded as an instruction (bootstrap precedence) |
| ARC-03, QA-C04 | KEEP | Consumer: `spec_packages.py` rejects a changed terminal Task body or identity, exercised by `test_spec_packages` (W02 consumer tests). No terminal body is edited in this run, and nothing is removed without approval and recovery |
| ARC-04 | KEEP (process) | Disposition stays inside this Task; no Spec or ledger is added for it |
| ARC-05 | CHANGE | Precondition 5 now recovers a Git LFS or submodule body as its payload or submodule commit, and an unrecoverable one blocks the removal. The blocking-case scenarios are NOT_RUN (W02 blocking-case scenarios) |
| ARC-06 | KEEP | Stage 98 is README-only and there is no move path. Consumer: the occupancy run and tests (W02 consumer tests) |
| ARC-07 | KEEP (process) | No archive, retention-catalog or migration gate is reintroduced; precondition 5 stays a manual record |
| ARC-08 | CHANGE, handed off | A dead subgraph of about 1,500 lines in `lifecycle/contract.py` has no production caller; the removal goes to W05 (H-W02-1) |
| ARC-09 | CHANGE | The protocol now says the retirement rules govern development documents only. Operational data and backups keep their Stage 05 owners, and shared agent memory keeps the environment constraints. Correction: the 2026-11-11 basis cited `approval-boundaries.md` for Vault and memory, but that file has no such text |
| Self-removing Task (prompt section 3 item 4) | KEEP | Retention by status requires final evidence while the package is still editable, which freezes decisions, promotion and authorization first. Precondition 5 records the post-merge recovery in a Task that survives the removal, so a removed Task never has to store its own final hash |
| Delete dry-run (prompt section 7 item 5) | KEEP (process) | The standing impact test is the registered gates: `package-retirement-unrecorded`, `identity-retired-not-reserved` and link alignment, which blocked the 2026-11-11 dry-run until reservation and link cutover. The scratch recovery dry-run is this Task's practice, not a rule (W02 removal dry-run, W02 SPEC-0267 recovery dry-run) |
| Registry retention and archive vocabulary (prompt section 3 item 1) | GAP, handed off | `archive_source_prefixes` is inert. The archive frontmatter fields (`archived_from`, `archived_at`, `archive_reason`, `archive_disposition`, `archived_commit`, `archived_blob`, `archive_authorizations`) remain in the Registry, the frontmatter schema and `metadata/profile.py`, although Stage 98 holds no bodies. `archive_retention.disposition_entry_statuses` stays in use: `lifecycle/occupancy.py`, `spec_packages.py` and `registry.py` read it. W03 assesses each field's consumers (H-W02-2) |
| W02-A, R147-08, WP-20 | PARTIAL | SPEC-0267 is removed after promotion, approval and a recovery dry-run (SPEC-0267 removal). The post-merge byte comparison is pending |
| W02-B, WP-19 | KEEP | The manual precondition 5 record and `archive_readiness_findings` stay separate. The latter is an on-read library function, reached only by `test_generation6.py`, with no CLI or gate. The user's Git-only goal and tool archive defaults are separate decisions: the protocol's Document Retention and Retirement summarizes and deletes, keeps version history as the record and leaves Stage 98 without bodies |
| OPEN-ARCHIVE | No conflict | SPEC-0267 was held under Q-04 until its promotion passed, then removed in `06bf2e201`. No retention exception or authority conflict remains open |

The SPEC-0248, 0249, 0250 and 0260 Tasks are merged and each has four
criteria pending owner acceptance. They are not reimplemented. Their packages
stay until their Tasks are terminal.

### SPEC-0267 retirement map 2026-11-12

The owner approved removing SPEC-0267 in the 2026-11-11 batch, so only its
safety conditions remain.

1. Commit `1cd6301b5` closed the two gaps named in the Batch removal record:
   the four networks in AD-0026, and the three accepted risks in POL-0053,
   POL-0087 and POL-0096.
2. A fresh-context `rules-engineer` promotion check returned BLOCKED. Some
   still-current meanings had no owner, and some owners contradicted the
   build:
   - the Pyroscope metastore;
   - the ComfyUI remount;
   - the Keycloak, OAuth2 Proxy and SeaweedFS binds;
   - the Keycloak recreate lesson;
   - the bound-listener exception;
   - the full n8n peer list;
   - the lineage lines.
3. Commit `b5fda3ffc` corrected those Stage 02 and 05 owners.
4. Commit `8757f25ca` added REQ-0023-FR-0004 as the Stage 01 owner, approved
   by the owner on 2026-11-12.
5. The re-check returned BLOCKED again on three items:
   - FR-0004 claimed more than Compose delivers;
   - POL-0024 omitted Alloy;
   - RUN-0014 had a duplicate line.
6. Commit `8659f05a6` fixed all three. FR-0004 keeps a general rule with
   recorded exceptions, as the owner chose on 2026-11-12: the Registry debug
   listener `:5001` and the SeaweedFS master, volume and filer metrics.

The n8n broker HOME apply follow-up is closed: TSK-0042 recorded "P03 Runner
HOME apply" (W68) as PASS. The ComfyUI egress follow-up is settled by
SPEC-0268, under which egress exists only while the maintenance overlay is
attached, with approval each time. That is neither of the two options SPEC-0267
named, and egress is unrestricted while the overlay is attached.

Recovery dry-run: no file of the package differs between `main` `4cd25b95b`
and this branch. The last commit that changed it is `8330534e3`, reachable
from `main`. Three files restored from `4cd25b95b` into a scratch folder
outside the repository hash to their blobs, with 0 mismatches. The only
inbound link is the `docs/03.specs/README.md` index row. The removal also
adds 267 to the Spec `reserved_history`.

### SPEC-0267 removal 2026-11-12

The final promotion re-check returned READY. Commit `06bf2e201` deletes the
three files of SPEC-0267, removes its `docs/03.specs/README.md` index row (the
only inbound link) and adds 267 to the Spec `reserved_history`. Gates at that
commit: metadata selected 52 with 0 violations, link alignment 0 failures,
corpus lifecycle occupancy 0, operations catalog PASS. The same commit rewords the FR-0004
exception reason from "consumers cannot all be named" to "not yet bound to a
consumer-only address". The re-check had found the old reason inaccurate; the
owner meaning it approved (a general rule with the two recorded exceptions) is
unchanged.

Criterion state at `4cd25b95b`, the last commit that carried the bodies:

| Package | Task status | Criteria | Acceptance |
| --- | --- | --- | --- |
| SPEC-0267 | completed | 1 to 7 | All accepted by the owner on 2026-11-08; E11 stays NOT_RUN by the owner's decision to accept a dry-run rollback rehearsal |

Precondition 5 record: `main` `4cd25b95b` carries each removed body unchanged
at `docs/03.specs/0267-secondary-listener-hardening/spec.md`, `plan.md` and
`tasks/tsk-0001-secondary-listener-hardening.md`. The last commit that changed
them is `8330534e3`, reachable from `main`. No body is uncommitted, reflog-only, branch-only or shallow-missing,
and no hold is recorded. After merge, this Task restores the three bodies from
`4cd25b95b` and compares their bytes.

The re-check noted, without blocking:

- Loki gRPC `9096` and Tempo gRPC `9095` listen unauthenticated on all
  interfaces. They are component RPC, outside FR-0004's four kinds.
- Each consumer-only network also lets the listener's service reach the
  consumer.

Both are recorded for the owner.

### v14.7 handoffs

| ID | Writer | Difference |
| --- | --- | --- |
| H-W02-1 | W05 | Remove the uncalled subgraph in `lifecycle/contract.py`. Its roots are `_repo_manifest_matches`, `_canonical_replacement_findings`, `_baseline_merge_owner_findings`, `_held_result_snapshot`, `_surface_replacement_findings`, `_surface_partition_plan_findings`, `_surface_result_state_findings`, `_partition_plan_findings`, `_profile_required_fields`, `_blob_at_commit_path`, `_surface_rollback_valid`, `_changed_record_paths`, `_load_repo_migration_manifest`, `_safe_archive_value`, `_git_object_type` and `load_migration_contract`. Delete transitively: helpers such as `_baseline_regular_blob`, `_changed_path_sets`, `_verified_commit` and `_safe_path_text` become dead with the subgraph. Remove with it the Migration manifest types, loaders, renderer and skeleton generator, their re-exports and the `test_public.py` manifest tests. Narrow the corpus-lifecycle F401 entry in `ruff.toml` if any re-export remains; do not drop it. First confirm that the generation 7 proof reader uses none of them |
| H-W02-2 | W03 | Assess the Registry archive vocabulary: the inert `common.archive_source_prefixes` and the archive frontmatter fields in the Registry, `document-frontmatter.schema.json` and `metadata/profile.py`. Retire each field with no remaining consumer; keep `archive_retention.disposition_entry_statuses` |
| H-W02-3 | Owner | Done 2026-11-12: REQ-0023-FR-0004 with recorded exceptions |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W02 obligation assessment | 110 | W115 | archive-owner-assessment | ARC-01 to ARC-09 at main `e4fd7f5f3` | NOT_RUN | Assessment not yet run | required | - |
| W02 obligation assessment result | 110 | W115 | archive-owner-assessment | ARC-01 to ARC-09 at main `e4fd7f5f3` | PASS | Per-ID table above: five KEEP; ARC-02, 05 and 08 GAP changed; ARC-07 code and ARC-08 manifest surface DEFER with scope | required | W02 obligation assessment |
| W02 removal dry-run | 110 | W115 | removal-recovery-dry-run | Five ready packages at `e4fd7f5f3` in a scratch worktree | PASS | 15 files restored with zero byte mismatches; gates block the removal until reservation and seven link cutovers | optional | - |
| W02 batch removal | 110 | W115 | package-retirement | Commit `58be65ebb` removing 0226, 0266, 0268, 0269; 0267 held | PASS | Promotion verified for four; reserved_history and link cutover done; metadata 0, links 0, lifecycle 0; post-merge byte comparison pending | required | - |
| W02 post-merge recovery | 110 | W115 | removal-recovery-proof | `e4fd7f5f3` reachable from `main` `19e6b58dc`; 12 files of 0226, 0266, 0268, 0269 | PASS | 12 files restored outside the repository, 0 byte mismatches against their blobs; no path present on `main` | required | - |
| W02 code review | 110 | W115 | independent-source-review | Fresh-context code-reviewer of `682393d7c` | PASS | APPROVED: no removed name has a code, workflow, manifest or dynamic consumer; `manifest_schema_v2` has no reader; corrected the archive-vocabulary note | required | - |
| W02 governance suite | 110 | W115 | document-governance-unit-suite | `tests/lib/document_governance` discover while `58be65ebb` and `8330534e3` were being written | FAIL | FAILED (errors=2); test names not captured; the corpus changed during the run | optional | - |
| W02 governance suite rerun | 110 | W115 | document-governance-unit-suite | `tests/lib/document_governance` discover at `56d32c32f`, clean tree | PASS | Ran 765 tests, OK, exit 0 | optional | W02 governance suite |
| W02 remote candidate | 110 | W115 | remote-candidate-quality | PR 955 runs on `ubuntu-latest` through `0ec2f14cb` | FAIL | Playwright `--with-deps` apt install could not resolve Ubuntu mirrors; earlier stages passed | required | - |
| W02 runner pin checks | 110 | W115 | workflow-contract | Commit `7a109158f` | PASS | GitHub workflow contract PASS (workflows 5, jobs 7); test_github_workflow_contract 48 OK | required | - |
| W02 remote candidate on 24.04 | 110 | W115 | remote-candidate-quality | PR 955 run 43049853619 at `fe54ee0f9` on `ubuntu-24.04` | FAIL | Same apt step failed: `azure.archive.ubuntu.com` unresolvable; public DNS SERVFAIL confirmed; pin reverted in `a3b289c5d` | required | - |
| W02 remote candidate after message fix | 110 | W115 | remote-candidate-quality | PR 955 run 43056362855 at `6980e3bdd` | FAIL | Commit range passed; Playwright apt install failed on the mirror DNS outage | required | - |
| W02 remote candidate final | 110 | W115 | remote-candidate-quality | PR 955 head `28b4be123`, hosted run 43060150134 | PASS | `candidate-quality` SUCCESS on the merged head; read from the PR check rollup on 2026-11-12, job log not re-read | required | W02 remote candidate, W02 remote candidate on 24.04, W02 remote candidate after message fix |
| W02 adapter without apt | 110 | W115 | red-green-proof | Commit `0c0168bdb` | PASS | Adapter test failed with the old vector, then test_ci_gate_adapters OK; ruff clean | required | - |
| W02 v14.7 assessment | 110 | W115 | archive-owner-assessment | v14.7 W02 prompt sha256 af6fdbcb, assessed at `3c8b5932b` | PASS | v14.7 per-ID table above | required | - |
| W02 SPEC-0267 recovery dry-run | 110 | W115 | removal-recovery-dry-run | SPEC-0267 at `main` `4cd25b95b`, last change `8330534e3` | PASS | 3 files restored outside the repository, 0 byte mismatches | optional | - |
| W02 SPEC-0267 promotion check | 110 | W115 | promotion-check | SPEC-0267 against its owners after `1cd6301b5` | FAIL | rules-engineer BLOCKED: unowned or contradicted meanings listed in the retirement map | required | - |
| W02 blocking-case scenarios | 110 | W115 | removal-blocking-scenarios | Uncommitted, squash-dropped, reflog-only, shallow, recorded-hold and missing-historical-consumer cases in a scratch repository | NOT_RUN | The scratch command was denied at the permission prompt on 2026-11-12 | required | - |
| W02 SPEC-0267 promotion re-check | 110 | W115 | promotion-check | SPEC-0267 against its owners at `8757f25ca` | FAIL | rules-engineer BLOCKED: FR-0004 broader than Compose, POL-0024 member list, RUN-0014 duplicate line; fixed in `8659f05a6` | required | - |
| W02 v14.7 review | 110 | W115 | independent-review | Commits `3c8b5932b` and `357590856` | FAIL | code-reviewer CHANGES_REQUIRED: `.gitmodules` claim, narrow H-W02-1, KEEPs without consumer evidence, no check rows, Registry archive vocabulary without a verdict, and seven minor items; fixed in this revision | required | - |
| W02 SPEC-0267 promotion final | 110 | W115 | promotion-check | SPEC-0267 against its owners at `8659f05a6` | PASS | rules-engineer READY: B1 to B3 and both recommended items fixed; no further listener in FR-0004's kinds | required | W02 SPEC-0267 promotion check, W02 SPEC-0267 promotion re-check |
| W02 SPEC-0267 removal | 110 | W115 | package-retirement | Commit `06bf2e201` | PASS | Package deleted, index row removed, 267 reserved; metadata 0, links 0, occupancy 0, operations catalog PASS; post-merge byte comparison pending | required | - |
| W02 consumer tests | 110 | W115 | consumer-unittest | `tests.validation.lifecycle.test_occupancy`, `tests.lib.document_governance.test_spec_packages` and `test_operations_catalog`, plus corpus lifecycle, in a worktree pinned at `8659f05a6` | PASS | 236 tests OK in 1038 s; occupancy 0 violations | required | - |
| W02 v14.7 review result | 110 | W115 | independent-review | Commits `5a5fa122d`, `82275d313` and `4b7021386` | PASS | code-reviewer re-reviews: I1 to I5, M1 to M7, N1 to N3 and R1 to R3 resolved; final verdict PASS | required | W02 v14.7 review |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 110 | pending | - | - | SPEC-0212 TSK-0057 |

## Review and Completion

In progress. The assessment, the dry-run, the reproduced-gap changes and the
removal of 0226, 0266, 0268 and 0269 are recorded, with their criterion state
and post-merge recovery. Criterion 110 waits for the owner.

v14.7: SPEC-0267 is removed in `06bf2e201`; its post-merge byte comparison is
pending. The blocking-case scenarios are NOT_RUN. H-W02-1 and H-W02-2 are open.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [W01 Task](tsk-0056-w01-governance-standardization.md)
