---
title: "Request Baseline and Reconciliation Plan"
version: "1.29.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-PLAN-0001"
parent_ids:
- "SPEC-0212"
created: "2026-10-07"
---

# Request Baseline and Reconciliation Plan

## Overview

The current 11–30 request preserves completed P00 Tasks. SEC01 delivers first,
SMTP01 owns the source transition second, and CLN01 deletes the old file third.

R10 adds W16–W23 in TSK-0007 from the 2026-10-15 source baseline. Existing
W1–W15 and completed bodies retain their earlier scope and evidence. The direct user request authorizes this bounded local contract and Plan;
that authority is not inferred from historical acceptance and does not approve
a shared edition or remote action.

## Scope

W9–W15 reconcile the request baseline, owner routes, shared-file leases
and SEC01 → SMTP01 → CLN01 handoffs; W1–W8 retain their historical receipts.
R10 W16–W23 add the current authority, document, lifecycle, retention,
hook/release, memory and OpenBao source corrections in TSK-0007 without
reopening completed Tasks or assigning new downstream acceptance owners.
R13 adds W25 in TSK-0009 for one current-source follow-up. It began separately
from W24's independent infrastructure work and now preserves the published
W24/criterion 19 allocation alongside W25/criterion 20. W26 in TSK-0010
classifies the links behind the standing `historical-links-unrecorded` warning
as a read-only, documentation-only follow-up. W27 in TSK-0011 records a
read-only per-unit Stage 98 disposition dry-run; it removes nothing. W28 in
TSK-0012 applies the owner-approved history-only removal of its candidates.
W29 in TSK-0013 records the follow-up review of the remaining request areas.
W30 in TSK-0014 removes a repeated history scan from the archive check.
W31 in TSK-0015 applies the owner-approved blocked items from TSK-0013.
W32 in TSK-0016 records the owner's choices for the remaining TSK-0013 items.
W33 in TSK-0017 re-reviews the deferred and not-run items from TSK-0016.
W34 in TSK-0018 applies the owner's choices on the items TSK-0017 left open.
W35 in TSK-0019 applies the owner's choices on two gaps from a request re-read.
W36 in TSK-0020 adds a quality characteristic and measure to the NFR template line.
W37 in TSK-0021 scopes the worktree rule to branch worktrees.
W38 in TSK-0022 records a read-only runtime snapshot and a skill bundle audit.
W39 in TSK-0023 records the owner's correction of the exporter drift.
W40 in TSK-0024 corrects stale paths named in agent and provider surfaces.
W41 in TSK-0025 removes a dead CI routing prefix.
W42 in TSK-0026 records the re-run of the full request against the baseline.
W43 in TSK-0027 reads the archive policy against its code.
W44 in TSK-0028 reads the SDLC and CI/QA policy and renames the release workflow.
W45 in TSK-0029 audits the meaning of every request line.
W46 in TSK-0030 judges every pair of the 148 requirements.
W47 in TSK-0031 adds the five missing governance rules.
W48 in TSK-0032 makes governance and provider guidance English.
W49 in TSK-0033 adds a Verification section to every skill.
W50 in TSK-0034 moves the Migration 0003 proof into its own module.
W51 in TSK-0035 writes the rule text behind the partly met lines.

W24 adds the independent `INFRA-P0` routing snapshot for requirements 11–32.
It freezes common boundaries before `INFRA-P1` data/secret/recovery work or any
variable implementation; it does not reopen r10 criteria 11–18.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Historical local/remote and Project-Template baseline read; retained evidence only | None | TSK-0001 | Preserved Task evidence |
| W2 | 2 | Historical fifteen-item ownership; superseded for current routing | W1 | TSK-0001 | Preserved Task evidence |
| W3 | 3, 4 | Historical root/LAB inventory and profile probes; LAB excluded from current execution | W1 | TSK-0001 | Preserved Task evidence |
| W4 | 5 | Historical conflict map and ADR-0047 | W2, W3 | TSK-0001 | Preserved Task evidence |
| W5 | 6 | Historical QA/protection read and validation | W4 | TSK-0001 | Preserved Task evidence |
| W6 | 1, 2 | Historical twenty-item main/template baseline | W5 | TSK-0002 | Preserved Task evidence |
| W7 | 3 | Historical inventory comparison; no fresh LAB run | W6 | TSK-0002 | Preserved Task evidence |
| W8 | 7 | Historical open-Spec disposition | W6 | TSK-0002 | Preserved Task evidence |
| W9 | 1 | Compare local/origin/remote main, dirty state and named baseline; parse root service keys and current inventory only | None | TSK-0003 | Value-free baseline and source-set evidence |
| W10 | 2, 3, 6, 7 | Read open Spec/Plan/Task frontmatter, latest tracked source and PR state; classify residuals and exclusions | W9 | TSK-0003 | Requirement table and owning evidence paths |
| W11 | 2, 4 | Observe contract RED; update SPEC-0212 Spec/Plan and SPEC-0204 Spec/Plan current routing | W10 | TSK-0003 | Contract GREEN; current authority checker |
| W12 | 4, 5 | Record writers/order/rollback, validate final documents, independent review, logical commits and protected PR delivery | W11 | TSK-0003 | Document checks; staged checks; actual hosted observations |
| W13 | 8 | Record current routing and SEC01 → SMTP01 → CLN01 ordering | W12 | TSK-0005 | Value-free contract probe; Stage 99 checks |
| W14 | 10 | Bind current main, supplied COORD input, observed worktree/PR state and active-package inventory; retain PR #457's merged receipt as input only | None | TSK-0006 | Value-free Git/source and lifecycle audit |
| W15 | 9 | Map requirements 11–30, reconcile active routing conflicts, record writer locks/recovery boundaries, run Stage99 selectors and hand off exact current inputs | W14 | TSK-0006 | Cross-package source, Task and document audit |
| W16 | 11 | P01 source/permission/delta baseline, attachment identity and classified finding map | None | TSK-0007 | Read-only Git and canonical-owner audit |
| W17 | 12 | P02 role, language, section and link correction; coupled Stage99 target amendment design | W16 | TSK-0007 | Changed metadata/links and affected contract regressions |
| W18 | 13 | P03 distinguish existing approval, Task state, acceptance, integration and observations | W16 | TSK-0007 | Generation-6 reader and exact lifecycle/acceptance evidence |
| W19 | 14 | P04 consumer/assurance/hold assessment and authorized retention or retirement | W16 | TSK-0007 | Direct consumer trace and applicable archive integrity checks |
| W20 | 15 | P05 hook/CI call graph and reproduced push-stage or duplicate assurance correction | W16 | TSK-0007 | Focused hook/routing tests and isolated installed-stage probe |
| W21 | 16 | P06 branch/release/CHANGELOG/rollback producer audit and concrete source corrections | W16 | TSK-0007 | Current producer/config trace and scoped contracts |
| W22 | 17 | P07 shared-memory/native-off/Restic reuse and justified missing assurance design or implementation | W16 | TSK-0007 | Existing receipts plus synthetic memory/backup regressions |
| W23 | 18 | P08 OpenBao optional-skip and CA-overlay discrepancies, operations promotion and quality limits | W16 | TSK-0007 | Focused OpenBao synthetic tests and changed document checks |
| W24 | 19 | INFRA-P0 inventory scope, owner routes, QA/CI mapping, writer leases, evidence ladder, and P1–P9 handoffs for requirements 11–32 and distinct F01–F29 findings | None | TSK-0008 | Value-free source/static evidence; no native/HOME/recovery claim |
| W25 | 20 | Classify r13 P01-P08 follow-up findings; remove one reproduced link-graph duplicate, bind repository-file provenance to its declared revision, and retain one shared memory store through sanitized CLI common-directory identity | W16 | TSK-0009 | Focused link and memory regressions, changed-path CI selection, and changed document checks |
| W26 | 21 | Classify the links counted by `historical-links-unrecorded` against each record's pre-archive Git origin and record the residual set and its proven cause | W25 | TSK-0010 | Read-only Git object resolution; changed document metadata and link checks |
| W27 | 22 | Per-unit Stage 98 retention-payload dry-run: consumers, capture, hold, isolated restore, and candidate or blocked disposition; no removal | W26 | TSK-0011 | Read-only checker-library reuse and `git archive` restore; changed document metadata and link checks |
| W28 | 23 | Owner-approved history-only removal of the TSK-0011 candidates: capture rows for pre-catalog units, assessment rows, whole-payload removal | W27 | TSK-0012 | Corpus lifecycle, link alignment, and changed document checks after removal |
| W29 | 24 | Review of the remaining request areas: apply verified small corrections; defer or block the rest with owner and reason | W28 | TSK-0013 | Renderer drift, metadata contracts and changed checks, affected unit tests |
| W30 | 25 | Measure and remove the repeated history scan in the archive assessment snapshot check | W29 | TSK-0014 | Archive regressions and timed corpus check |
| W31 | 26 | Remove git-cliff configuration, add template subtopics, and repair the index-membership regression | W30 | TSK-0015 | Metadata contracts, template and gate tests, full unit suite |
| W32 | 27 | Classify repository-path absence tests, list `_workspace` writers, and keep external acceptance not run | W31 | TSK-0016 | Absence-test scan, metadata contracts, workspace contract tests |
| W33 | 28 | Replace past-removal absence checks with current-rule checks and read remote and cross-repository state without writing | W32 | TSK-0017 | Tier and routing tests, manifest negative check, read-only API and repository reads |
| W34 | 29 | Narrow merge methods, diagnose pre-existing unit failures, run static Compose validation, and hand off cross-repository gaps | W33 | TSK-0018 | Merge-method read-back, isolated-venv test run, Compose validation in a clean worktree |
| W35 | 30 | Delete the stale `main-current` tag and add the worktree location rule | W34 | TSK-0019 | Remote tag read-back, governance contract, provider render |
| W36 | 31 | Add a quality characteristic and measure to the requirement template's NFR line | W35 | TSK-0020 | Requirement parser and template tests |
| W37 | 32 | Scope the worktree location rule to branch worktrees | W36 | TSK-0021 | Governance contract, provider render |
| W38 | 33 | Read running container health and audit skill bundles | W37 | TSK-0022 | Read-only `docker ps`/`inspect`, skill inventory |
| W39 | 34 | Record the owner's recreation of `airflow-statsd-exporter` and its health | W38 | TSK-0023 | Read-only `docker inspect` and project health count |
| W40 | 35 | Correct repository paths in agent and provider surfaces that no longer exist | W39 | TSK-0024 | Path existence scan, governance contract |
| W41 | 36 | Remove routing and references to files that do not exist in active surfaces | W40 | TSK-0025 | Path existence scan, workflow-contract and gate tests |
| W42 | 37 | Re-run the request against the baseline, close TSK-0008, and record the unperformed specification audits | W41 | TSK-0026 | Baseline readback, metadata contracts |
| W43 | 38 | Read the archive policy text against its code and checks, and correct mismatches | W42 | TSK-0027 | Archive corpus check, metadata contracts, routing tests |
| W44 | 39 | Read SDLC and CI/QA policy against code and rename the release workflow | W43 | TSK-0028 | Workflow contract, gate and release tests, metadata contracts |
| W45 | 40 | Audit the meaning of each non-blank request line against the repository | W44 | TSK-0029 | Line coverage, metadata contracts, agent governance |
| W46 | 41 | Judge every pair of the 148 requirements for duplication and conflict | W45 | TSK-0030 | Pair coverage, attribute coverage, metadata contracts |
| W47 | 42 | Add the missing rules for lines L047, L171, L175, L292, and L369 | W46 | TSK-0031 | Agent governance, provider projections, routing tests, metadata contracts |
| W48 | 43 | Make governance and provider guidance English and enforce it | W47 | TSK-0032 | Language check, language and registry tests, agent governance, metadata contracts |
| W49 | 44 | Add a required Verification section to every skill | W48 | TSK-0033 | Section coverage, metadata contracts, registry and heading tests |
| W50 | 45 | Move the Migration 0003 cutover proof into its own module | W49 | TSK-0034 | Archive behavior parity, document governance suite, script manifest |
| W51 | 46 | Write the rule text behind the partly met request lines | W50 | TSK-0035 | Agent governance, language check, routing tests, metadata contracts |

### Current v30 continuation and delivery

The direct 2026-10-26 request extends W24's previous 11–31 routing scope to
R32 without a new Task, criterion, inventory authority, or duplicate prompt
package. TSK-0008 records the current source survey, package provenance,
four-axis owner map and exact writer leases. TSK-0006/0009/0010 and other
completed records remain historical evidence. Reuse the existing v30 bundle's
five standalone prompts and its single dependencies folder; preserve missing
historical references as unavailable rather than recreating their contents.

The survey classifies the whole tracked-path set and the relevant current
Task/consumer/source scopes; it does not claim semantic review of every byte.
After the coordinator reconciles the read-only findings, exact safe source
units proceed through their own prerequisites and independent prechange
review. A missing runtime/private/owner decision does not block unrelated
reversible source fixes. TSK-0008 names the current scopes; old writer names
below are historical assignments and confer no present lease.

The Quality cancellation correction belongs to SPEC-0214's current C10/W11
continuation, preserving completed criterion 7. Service selection, network and
optional ACL changes retain SPEC-0204 P02/P03/P05 and SPEC-0218 ownership.
Root Compose and environment edits require the coordinator's explicit release
to the single service writer after review; no current parallel writer owns
those files. The coordinator integrates only reviewed exact inputs.

This execution delivers local logical commits and per-Spec PR drafts only.
Earlier prospective push/PR/remote-merge directions below are superseded for
this request until separate direct authorization. No integration target is
inferred from being on main; an unidentified local target blocks integration
alone. Runtime, credential, deletion, host and external-cluster actions retain
their exact target, approval and recovery gates. Independent review and final
verification precede local delivery; no future result is recorded as PASS.

### W25 file map and checks

The link slice owns `scripts/lib/document_governance/links.py`,
`scripts/validation/check-document-links.py`, and
`tests/lib/document_governance/test_links.py`. Its regression proves one
same-input parse reaches the graph once and retains the CLI's existing modes.
The memory slice owns `scripts/lib/ops/memory_sources.py`,
`scripts/operations/agent_memory.py`, and `tests/lib/hooks/test_agent_memory.py`;
it adds a bogus-revision rejection and makes the CLI's own/caller
common-directory identity use the sanitized Git runner, without weakening the
digest, tracked-file, or no-symlink checks. This source-only regression does not
read a memory store.
`tests/validation/test_agent_governance_ci_routing.py` verifies that a memory
helper change selects the focused agent-governance route. The W25 memory writer
also owns the one-line `.github/workflow-contract.yml` changed-path map and its
direct gate-contract tests; it maps the helper and its regressions to the
focused route without changing unrelated workflow selection.
The metadata QA slice owns
`scripts/lib/document_governance/metadata/reference.py` and
`tests/lib/document_governance/metadata/test_reference.py`. It transports the
already-computed immutable legacy-archive binding into changed-record validation;
it does not alter an archive, add a predicate or constant, or redefine the
immutable-binding rule.

W25's doc-writer exception owns only
`.agents/governance/environment-constraints.md` and
`docs/05.operations/runbooks/10-platform-and-backup/0021-backup-and-restore.md`.
After an actual required-check readback and scoped review, it also owns only
`.github/rulesets/main-protection.md` for that canonical observation. These
exceptions clarify the full-commit/current-byte source-pin contract and the
observed protection state; they do not change a policy schema, runtime
procedure, or historical record.

### Exact writer map

The historical P00 doc-writer owned this Spec, this Plan and TSK-0003 for the
first reviewable current-contract unit. The current COORD writer owns only this
Spec, this Plan and TSK-0006. TSK-0001, TSK-0002, TSK-0003 and TSK-0005 are
completed historical bodies and remain immutable. Existing operations bodies,
inventory, Registry, runtime and governance sources are read-only here.
No new Spec number is issued. Independent reviewers do not edit the patch. A delivery-receipt unit after
actual P00 merge may reconcile the frontmatter of TSK-0001/TSK-0002 from their
already accepted historical criteria, preserving both bodies byte-for-byte.
The current Task records their lifecycle edges and actual delivery separately;
this is no fresh execution or downstream native acceptance.

For downstream work, each acceptance owner assigns one implementation writer
before touching a shared path. P01 owns secret classification/prerequisites;
P02 owns metadata/path mappings; P03 owns root gateway, endpoint and port
contracts; P04 owns Airflow source/native integration; P05 owns n8n source/native
integration; P06 owns per-image consumption; P07 owns root-leaf controls and
exact exceptions. SEC01 owns P09 preparation documents, schemas, synthetic
fixtures and future acceptance contracts. It creates no external workspace,
Wiki engine, native application or production consumer. SMTP01 provides only
the canonical secret/consumer/catalog interface and reviews related P09
contracts; it does not duplicate P09 files. P10 owns a named input-to-recovery
consumer. These stage labels allocate no new Spec IDs or unnamed live targets.

Only one writer at a time may own `docker-compose.yml`, public environment
contracts, `.github/workflow-contract.yml`, `scripts/manifest.yaml`, the
Stage 99 Registry, document indexes, shared Alloy/gateway/backup configuration,
and both `infra/common-optimizations.yml` and
`infra/common-optimizations.exceptions.json`. P00 owns none of their implementation.
P07 reuses SPEC-0218 v2; no full common-file rewrite follows from this Plan.

For W24, the coordinator exclusively writes this Spec, this Plan, and
TSK-0008. The bounded matrix at `m0021-local-docker-service-consolidation.md`
is an input projection, not a second inventory authority. Later writers are:
P01/P06/P07 for data, secret, backup and root-control work; SEC01 plus each
affected leaf owner for images, Dockerfiles, OCI evidence and update records;
P03 for connection and port contracts; P04/P05/P10 for the vertical flow;
the QA/CI owner for workflow contracts, gate scripts and tests; and P08/
SPEC-0227 plus the image owner for Stage 05 and requirement-31 documents.
Root Compose, `.env.example`, catalogs/exceptions, Stage 99 Registry, Stage 05
indexes, shared scripts, and CI contracts require a named single-writer lease.
Unknown task-level token, time, and rate limits do not release that lease.

For W14–W15, the coordinator writes only this package's Spec, Plan and
TSK-0006. Existing worktrees are evidence of possible concurrent ownership, not
permission to edit their paths. The lock map is: SEC01 image/digest/build;
P01 OpenBao TLS/custody; P02 catalog; SMTP01 canonical SMTP/alias; CLN01 exact
retirement; P03 common connection/port contracts; P04 SQL/DAG; P05 workflow and
SMTP node; P06 migration; P07 measurements/root leaves; P08 Stage05 moves; P10
acceptance fixtures; SPEC01 active-contract documents. The coordinator may
propose a shared-file change, but the lease holder integrates it after the
preceding source identity and review are fixed.

### Dependency and P08 integration order

1. P00 fixes baseline, ownership and exclusions first. Applied work stays
   NO_CHANGE and genuine gaps keep their existing acceptance owner.
2. P01 classification precedes P02 mappings and P06 actual secret consumption.
   P03 endpoint/port contracts precede their P04/P05 consumers; P09 references
   these contracts only for preparation. P07 uses
   observed demand and consumer prerequisites, with no invented optimal limits.
3. P04 and P05 native runs require actual connection/secret/recovery targets.
   Wiki preparation has no external workspace, native/app or production-consumer
   assignment. A future canonical SMTP interface may later name a consumer; P10
   consumes only verified interfaces and its named recovery fixture.
4. P08 selects exact current common/domain document destinations through the
   Registry. Finish a feature writer's edits and evidence before moving those
   paths; then one P08 writer moves documents and updates all references,
   indexes and applicable checks. Re-read SHA and hand the new paths back to
   the feature owner before any further edit. Do not edit old/new paths in
   parallel. P08 may move LAB documents to typed `labs/` destinations; LAB code,
   config, secrets and runtime are not moved.
5. Each feature owner completes its Task, independent review and per-Spec PR.
   P00's inventory or merge receipt cannot complete a downstream native run.
6. W24 records its reviewed P0 route before P1 or any variable source change;
   criterion acceptance remains pending while its evidence rows stay open. P1 establishes
   non-destructive restore prerequisites before live or irreversible image,
   connection, leaf, workflow, or retirement work; it does not block unrelated
   reversible source, test, CI, or P9 documentation work. Every logical change
   maps changed files to a regression, selector/gate, rollback, and operating
   documentation owner; requirement 31 is completed in the same unit as its
   actual ROOT-image change.

### R10 ownership and integration

The coordinator assigns one writer per slice. The documentation writer owns
this Spec, Plan and TSK-0007. Hook/CI implementation, Stage 99 and governance
contracts, and OpenBao source each have a distinct writer; the controller
integrates shared files and releases their lease before another writer edits.
No worktree path alone proves a lease released. Do not rewrite earlier Tasks.

Start with the Stage 99 stale authority prose and empty REQ-0024/AD-0030
scaffolding. Align new common-guidance language at its policy owner. Reproduce
pre-push multiple-ref/deletion behavior in an isolated repository. Independently
fix the OpenBao optional-skip contract and SPEC-0243 CA-overlay source wording.
The controller sequences any table/lifecycle/memory amendment after its exact
consumer impact and compatibility are reviewable; unimplemented targets stay
pending in TSK-0007 rather than being treated as completed by this Plan.

## Verification Plan

Run a value-free source-set audit, actual frontmatter parse and read-only PR
metadata before authoring. Observe the requirement-coverage/exclusion contract
probe fail on the baseline, then pass after the active-contract edits. Its
input SHA and result are recorded in the Task; no persistent snapshot test or
new service-count constant is added for this documentation change.

On the final source run document metadata/relationship/lifecycle checks,
local document links and `git diff --check`; select through the current changed
profile with `--explain`, without substituting a local aggregate candidate
run for the hosted PR. Run the existing agent-authority checker to establish
whether SPEC-0221 already meets the request. No public full/private env render,
LAB check, container run or secret read is part of P00.

W14–W15 add no live validation. They use tracked source and public Git metadata
only. HOME, migration, rotation, deletion, native workflow execution and empty
target restoration remain NOT_RUN until their owning Task identifies the exact
resource, approved operator/window, backup set and recovery boundary. A P08
document move waits for the feature-owner path freeze and a single move writer;
the confirmed duplicate README headings and stale domain wording are source
findings, not permission to move LAB runtime assets.

W24 records only tracked, value-free source and authenticated public Git
observations. `SOURCE_APPLIED`, `STATIC_PASS`, `ISOLATED_PASS`, `NATIVE_PASS`,
`HOME_PASS`, and `RECOVERY_PASS` are ordered domains; no lower domain implies a
higher one. A local changed no-op or `full --explain` selection is not hosted
required-check coverage. Missing live targets remain `BLOCKED` or `NOT_RUN`.

After independent review, validate the Conventional Commit message and run
`scripts/validation/run-ci-precommit.sh --mode local-staged` on the exact
staged set. Read actual branch protection and PR checks. Push this request's
branch, create its PR and attach it; merge only when its current review/check
conditions are satisfied. Record hosted results separately from local results.

For r10, select the smallest checks that establish each changed guarantee.
Content-only edits use changed metadata, relationships, links and diff checks;
Registry/parser/permission/workflow changes add their directly affected
regressions. Use synthetic repositories and DBs for failure probes. Record
actual commands, revisions, result and elapsed observations once. Hosted CI,
real provider effectiveness, HOME backup/restore and remote main protection
remain separate observations. Never create credentials or change managed
settings to make a source check pass.

## Risks and Recovery

### Risks and Rollback

Revert only the logical W13 documentation commit through a protected PR to
restore the prior active contract; preserve historical Tasks and issued IDs.
No service, credential, data, volume or host state changes, so no runtime/data
rollback is claimed. Equal baseline, merged draft and historical runtime PASS
must not be promoted to fresh validation. A concurrent shared-writer/path
change invalidates affected inputs and requires a fresh scoped check.

Revert W24 as its isolated documentation unit through the protected PR path;
do not revert an independent owner’s implementation with it. Before a secret
rotation, data migration, retirement, or live upgrade, the owner records the
concrete target, backup identity, restore boundary, compatibility result,
operator/window, stop condition, and rollback. Missing prerequisites block
only that dependent operation.

## Related Documents

- [Spec](spec.md)
- [R10 reconciliation Task](tasks/tsk-0007-r10-reconciliation.md)
- [Infrastructure audit execution Task](tasks/tsk-0008-infra-audit-execution.md)
- [Historical link classification Task](tasks/tsk-0010-historical-link-classification.md)
- [SMTP01 request contract Task](tasks/tsk-0005-smtp01-request-contract.md)
- [Current coordination audit Task](tasks/tsk-0006-current-coordination-audit.md)
- [Completed P00 Task](tasks/tsk-0003-active-contract-and-exclusions.md)
- [Historical baseline Task](tasks/tsk-0001-request-baseline-and-inventory.md)
- [Historical twenty-item Task](tasks/tsk-0002-twenty-item-reconciliation.md)
- [Integration plan](../0204-service-integration-security-and-operations/plan.md)
