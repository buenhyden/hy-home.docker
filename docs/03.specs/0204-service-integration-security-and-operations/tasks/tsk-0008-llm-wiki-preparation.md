---
title: "LLM Wiki Preparation Task"
version: "0.2.5"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-11"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0008"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-10"
---

# LLM Wiki Preparation Task

## Objective

Issue the P09 implementation boundary for an unimplemented LLM Wiki. The
eventual implementer prepares contracts, schemas, synthetic fixtures and
acceptance criteria so a later task can build the product without guessing its
authority or resource boundaries. This Task does not implement the Wiki.

## Inputs and Authorization

The direct 2026-10-10 P09 request authorizes this Task, its future owned
source/docs/tests, logical commits, PR, review and merge after checks. It
supersedes older SPEC-0212 wording where it conflicts; shared SPEC-0212
reconciliation remains a coordinator-owned documentation dependency, not an
application or runtime prerequisite.

The approval source is the direct user request for
`buenhyden/hy-home.docker`; this issuance branch is
`codex/p09-task-issuance` from pre-change main
`a03c8930a5a15a82f4176bbcfe457bc2ce09db4b`. It authorizes no settings,
release or runtime write. Before main integration, the recovery action was a
logical revert of these three issuance documents. The issuance PR #414 was
merged at `cac9e10fa584754706598d624654e07e8d6531f4`. Required latest-head
checks, PR review and delivery remain pending only for the later P09 source
integration.

The preparation input records future source allowlists for `blog-data/dev`,
`Project-Template/dev`, `hy-home.docker/main` and `hy-home.k8s/main`. A future
application bootstrap must use a verified Project-Template `main` release.
Read-only intake observed Project-Template main
`6b1c7394f1e08c0ce566f76b4644c2cad9c89891` (unprotected) and README blob
`0c9c037a98b220b1c5443468a3ddcdb68b0589bd`; `/releases/latest` returned
HTTP 404 (exit 1), so a verified main release is `BLOCKED_FACTS`. SPDX license
was null, rights remain UNKNOWN, and the observed Python/Shell languages are
automation rather than an app-stack decision. Its README requires product and
stack intake before Stage01 and review of `bash scripts/ws.sh bootstrap --dry-run`
before bootstrap; neither bootstrap nor an external workspace was created.
The shared brief was reachable by title only; its body was not read. Neither
gap permits inference.

No project ID, endpoint, OIDC client, database/role, collection, bucket,
credential, external workspace, real data, or HOME target is approved. Do not
read secret values, private environment/authentication files, raw HOME logs or
user data. Learning applications and LAB runtime changes are excluded. P08,
not this Task, owns any later Stage 05 LAB documentation move.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0204-TSK-0008 | draft | ready | #inputs-and-authorization |
| SPEC-0204-TSK-0008 | ready | in-progress | #w25-received-execution-handoff |
| SPEC-0204 | blocked | in-progress | #w25-received-execution-handoff |
| SPEC-0204-PLAN-0001 | blocked | in-progress | #w25-received-execution-handoff |

### Lifecycle Event Reconciliation

| Artifact | From | To | Canonical carrier | Canonical source commit | Canonical integration commit | Duplicate source commit | Duplicate integration commit | Disposition | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SPEC-0204 | blocked | in-progress | SPEC-0204-TSK-0009 | a27163a4f8efcea005d931b7f92e4f616132d8f3 | 80c31405df7983dc4b7d8ad8823f73323247d264 | 9666aa6b610f1f524893e10095ddd253a381fddc | abe2b8b19a2fe17cd08f06681f338a0e07a4c3f9 | concurrent-duplicate-observation | #w25-concurrent-lifecycle-reconciliation |
| SPEC-0204-PLAN-0001 | blocked | in-progress | SPEC-0204-TSK-0009 | a27163a4f8efcea005d931b7f92e4f616132d8f3 | 80c31405df7983dc4b7d8ad8823f73323247d264 | 9666aa6b610f1f524893e10095ddd253a381fddc | abe2b8b19a2fe17cd08f06681f338a0e07a4c3f9 | concurrent-duplicate-observation | #w25-concurrent-lifecycle-reconciliation |

### W25 Concurrent Lifecycle Reconciliation

Task 0009's source commit and PR #418 first integrated the two package lifecycle
transitions. Task 0008's divergent source commit independently recorded the
same observations before PR #417 integrated later. The registered receipt above
preserves both append-only Task histories and names Task 0009 as the canonical
carrier; it does not authorize generic deduplication or alter either package
state. Validation binds the blocked common-base Spec and Plan, exact Task
identities at source and integration trees, absence of each edge on its main
parent, one edge after each merge, and the ordered PR #418 then PR #417
introductions on current main's first-parent history. A side-merge-only reach,
reused Task path, pre-existing edge, or mismatched pre/post state invalidates
the receipt rather than creating a lifecycle override.

Ready contract issuance: the issuance branch contains no accepted P09
implementation. That observation is separate from unaccepted worker-owned
local material.

### W25 Issuance and Boundaries

The remote baseline `a03c8930a5a15a82f4176bbcfe457bc2ce09db4b` contains Tasks
0001 through 0006 and no issued Task 0008. A previous proposal of Task 0009
was never issued. Task 0008 is allocated after that scan. Pending CLN01 Task
0007 is preserved outside this Task. At issuance, a separate P09 worktree had
an in-progress, uncommitted Task 0008 plus helper, fixture and test material.
This issuance formalized the same identifier without accepting, copying,
testing or classifying that worker-local material. Its work log is retained as
historical handoff input and reconciled against W25/criterion 13 after the
reported handoff.
The earlier SEC-before-P09 issuance convention is withdrawn: W25 may start its
independent preparation files now, while coordinator-owned shared files
integrate serially.

The eventual owner may create only the following new P09 surface:

- `infra/09-platform-ops/project-registration/wiki-preparation/` with Korean
  README navigation, preparation contracts, `schemas/` and `fixtures/`;
- four schemas for future consumer manifests, source/artifact provenance,
  job/outbox/handoff state, and blog-data handoff; valid/invalid synthetic
  fixtures for each;
- `scripts/lib/ops/wiki_preparation.py`, the sole public pure offline helper
  API, plus its private `scripts/lib/ops/wiki_preparation_semantics.py`
  implementation module; both accept parsed contracts and caller-provided
  synthetic bytes only; and
- `tests/lib/ops/test_wiki_preparation.py` and
  `tests/validation/test_wiki_preparation_contracts.py`.

Every new preparation folder, including `schemas/` and `fixtures/`, needs its
own README. A newly needed parent-family README is a coordinator-owned shared
integration change, not a worker-side shortcut.

The public helper re-exports `PreparationError` and keeps the only public API;
the private semantics module has no filesystem, network, environment,
subprocess or external-write access. Both modules remain under 800 lines and
split validators remain at most 50 lines. They check cross-field project
namespaces, selected candidate and exact write sets, content hashes and
idempotency. Hash format or fixture equality is not source authenticity,
license, ACL or runtime proof.

Reuse `infra/09-platform-ops/project-registration/`'s generic registration
schema and validator; do not weaken or duplicate them. The future consumer
manifest records project ID, source repository/ref allowlist, data
classification; issuer and audience; planned DEV database
and role names; Valkey command and prefix; Qdrant collection and RBAC; S3
prefix; egress allowlist; metrics labels and cardinality; retention; backup
RPO/RTO; and disabled/by-design flags. The new contracts reject other projects,
path escape, wildcard/admin grants and empty required values. They define source
revision/content hash/path/retrieval/effective times, license/rights/ACL/delete/revoke
events, idempotency key, parser/chunker/embedding versions, index generation
and generation provenance. The job/outbox contract defines exact
`pending`, `running`, `partial`, `succeeded`, `failed` and `cancelled` states,
at-least-once delivery, dedup/dead/backfill/timeouts, a public generation
pointer, non-atomic PG/object/Qdrant reconciliation, recovery reconciliation
and deletion priority. A future deletion or revocation must immediately
invalidate or remove search, point queries, citations, downloads, cache and
previous generations.

The blog-data handoff contract records selected candidate IDs, base SHA, target
path allowlist, expected content hash, exact write set, approval, conflict
policy, receipt and idempotency. It forbids one approved candidate from writing
all detected candidates. Raw output may become Literature candidates only;
Permanent notes, Maps and publishing remain subject to their existing separate
review. P09 does not perform a handoff or write blog-data.

The product intake identifies target users, goals, non-goals, staged MVP,
resource/call/rights constraints, operational owners, risks and open decisions;
unknown product targets do not become production endpoints. Source Git remains
the code/document authority, blog-data remains the reviewed Literature,
Permanent, Maps, draft and published-content authority, and hy-home.docker
owns shared engine/auth/ingress/observability/backup. A future Core records
ingestion status, source/revision, search index, job, candidate, learning and
handoff state; it must not rewrite sources or blog-data without review or
create a second permanent knowledge canon. This record model does not authorize
a learning application.

The preparation package must include that intake, the four contracts, future
login-to-permitted-source-registration, sync-state, evidence/freshness search,
candidate review, selected handoff, retry and recovery flows. E2E acceptance
must cover empty, delayed, permission-denied, partial-failure and recovery
screens without building them. Its readiness matrix separates reusable engines,
facts requiring verification, future app work and scope-out. P04/P05's
independent manifest validation/publish/notification batch is a future
connection-test asset, not Wiki completion evidence; a generic consumer
provision blueprint remains unexecuted. It must not create Wiki Core/API/UI,
search/embedding, crawler, app DB/role, Qdrant collection, object bucket,
production client, n8n Wiki schedule, external workspace, blog-data write or
any runtime resource.

The coordinator exclusively integrates `spec.md`, `plan.md`, SPEC-0212
routing, parent READMEs, `scripts/manifest.yaml`, workflow registration and
common test README changes. Do not edit those files without an assigned
integration window. SEC01/SMTP01/CLN01 operational completion is not required
to draft W25's new files; their final service, secret and recovery contracts
remain readiness conditions rather than invented values.

The separate P09 worker session exclusively owns P09 helper, schema, fixture,
test and Task implementation/validation. SEC01 stops editing that P09 surface
and continues only its image/security code and independent tests. The
coordinator owns contract changes during issuance and integrates the worker's
reported execution log later. The coordinator has no cross-chat stop/send
mechanism; user reports are the sole handoff for actual session-stop status and
are distinct from this worktree's observations.

### W25 Received Execution Handoff

The received worker record is the immutable Git tree
`aa110d58e8de2b8b37eb3c5ad4f4de854ee86299` at this Task path. Its Task draft
used stale W24 and criteria 4/5/8 mappings, so it is evidence input rather than
a replacement authority. This issued Task preserves its Task identity, created
date, criterion 13 and W25 mapping while receiving the worker's source and QA
history. The 29-file P09 payload was received as uncommitted worker handoff
input; no operational resource was created by that presence. The coordinator's
33-file integration payload, including three parent READMEs and the private
semantics module, is the current source delivery candidate (40 changed paths
overall) and remains pending its own PR QA and delivery receipt.

Worker-owned RED evidence remains recorded as failures: policy admission first
accepted coherent project/path changes, then unconstrained resource and receipt
authority, exhausted job retry, unsafe candidate paths, and unapproved
registration references. The worker corrected those cases in the pure helper;
the original failures are not recast as PASS. The received final source inputs
matched the imported pre-finding tree at handoff: helper SHA-256
`51044ec43592c8eccf40774d821016784e562bb0d30a59bd66d38685b3ecc0af`,
with received test and contract input hashes `48e1c…` and `0748ca…`.

The worker reported dedicated synthetic suites: 21 tests PASS and helper branch
coverage 99 percent. Coordinator replay on the root-matched payload observed
29 tests (21 P09 and 8 existing registration tests) PASS, and Ruff check and
format for the three P09 Python files PASS. Those receipts apply to the
pre-finding worker source and are historical SOURCE/UNIT evidence only. Final
coverage must measure both the public helper and private semantics module.
At handoff, the worker also reported unresolved integration facts:
unregistered script-manifest entry, coordinator-owned workflow/changed-gate
registration, metadata/lifecycle reconciliation, and staged Gitleaks false
positives for synthetic checksums. Those historical FAIL, BLOCKED and NOT_RUN
states were resolved in later source work; their original receipts remain below.

### W25 Security Finding and Correction History

Independent security review found that the trusted policy did not bound job
`max_attempts` or timeout: synthetic input admitted `max_attempts=1000000000`
and `timeout=2147483647`. The root-assigned fix subsequently changed only the
helper, its unit tests and the job schema, followed by re-review. At that time,
the prior 21-test/99-percent receipts did not prove the final source. A further
review found unbound nested `backup_restore` data and a deletion watermark
above its sequence with pending generation `None`; the same root TDD fix and
re-review resolved those findings. The approved coordinator-owned
Gitleaks change uses exact AND/target-rule/path/hash checks for independently
recomputed public synthetic checksums; its negative-boundary checks passed in
commit `fcd738f65`, and the common manifest/workflow and parent-README
registration integration is complete as source work. Replacement frozen QA
later passed; candidate CI and source delivery remain pending. SPEC-0212 PR #412 must reconcile its stale P09
ownership in a separate global-contract change; this Task does not edit
SPEC-0212.

P2 review also found stale source/job receipts could block later legal source
progress or allow old source state after revoke/delete history. The scoped
state-revision correction was then implemented and confirmed by helper/schema/
test: source uses `{generation, evaluated_sequence}` and job uses
`{generation, transition_count, outbox_sequence}`, while raw content hash and
dedup key remain unchanged. It retains the full canonical request SHA and
rejects a different payload at the same state revision. This is semantic
fixture evidence only, not an actual delete or restore proof.

Gitleaks v8.30 static replay then passed for the approved narrow public-checksum
rule: the previous eight findings became zero; either checksum outside its
allowed path, or a changed checksum inside either fixture class, remains
detected with exit 23; a second custom rule with the exact digest at an allowed
path also remains detected with exit 23, proving the target-rule boundary. The
source and blog digests were independently recomputed public hashes, not
secrets. Common-file delivery is complete as source work; candidate CI, final
review and delivery remain pending.

Malformed trusted-policy collections were an additional P2 finding resolved by
the same root TDD fix and re-review; they were not accepted merely because the
collection had a valid outer document shape.

### W25 Frozen Fix Receipt

The frozen helper SHA-256 is
`836a1de27cb5f82c2fcb589797caadb2a11943d88020a565755d3ecc8621febb`;
unit, contract and job-schema inputs are respectively
`6934bd9190bb97fc625f3ebdf0c3e1142001dff18e16baeb1bdb9526699c416d`,
`e7b253639b8b5fd0e4256cd2d9a3007bd1bf08ff7f9997fe9cefa8252b3a4737`,
and `7257ad1bc76027560e873608e07c56b0f0ddd2d68bfba27352ae9c4e46d79053`.
RED retained three groups: eight failures for backup owner/bounds/document
policy/watermark, two idempotency-conflict errors in progress tests, and five
trusted-policy expansion failures. Six focused GREEN cases then passed; the
frozen suite passed 24 tests with 99 percent branch coverage (200 statements,
two misses, 28 branches, no partial branches), and Ruff passed. Independent
security review passed its 24 tests; package/helper/test Gitleaks scans found
zero findings. These are first-round SOURCE/UNIT/STATIC receipts only, not
final source acceptance or evidence of source authenticity, rights/licenses,
live ACL/query/cache propagation, deletion, restore or delivery.

Second-round review reopened P2: versioned `state_revision` keys could bypass
immutable admission comparison across revisions, allowing a source rights-basis
change on revoke or a job backfill change while progress passed. QA then defined
a stable immutable admission anchor and persisted digest alongside the versioned
state receipt (or an equivalent trusted exact immutable-field binding). The
staged helper `836a…` and its controller receipt predate that correction; do
not treat either as final acceptance. The required contract-model update
replaced the earlier frozen README content.

QA then reported a second-round GREEN frontier model with an immutable admission
digest, explicit prior states, versioned receipts and persisted digest. That
intermediate report preceded the replacement frozen full-suite/style proof and
independent review; the later replacement receipt is the accepted source QA.

Security review then refined source identity: source admission is path-wide
`H(project, contract, repository, ref, path)`, with revision/content/timestamp
and processing versions outside its admission digest. The caller-owned typed
`versions` allowlist contains exact `{parser, chunker, embedding}` mappings;
the selected mapping is preserved with source revision and content hash in the
generation artifact. An artifact is immutable within a generation and can
change only at a higher generation under an updated caller policy. The
revoked/deleted terminal frontier remains preserved. The canonical contract and
source input documentation now match that model. Replacement frozen QA and
review later passed; source authenticity, store completeness and runtime remain
`NOT_RUN`.

### W25 Revoked Frozen Source QA Receipt

The pre-replacement frozen source input passed 34 tests in 4.670 seconds. Its
public helper SHA-256 is
`52d6b056dc5f7ca21cbe52222af75da15f7c64bc5084929a1c351b5f62df9cdc`, its
private semantics SHA-256 is
`00420ffed04d45d2cb2293420bc2a84fb57863d3dd81de64e386359ec772e8d6`, and
the unit, contract and job schema inputs are respectively
`af2ff71c0196cb4f47074cb19b0150e15697731e9d03a3d58e8718505fca7deb`,
`9e410ba523b8172e7670d5cf60c6bcfdc507658e680af8cd28ca540493f9280f` and
`7257ad1bc76027560e873608e07c56b0f0ddd2d68bfba27352ae9c4e46d79053`.
All functions are under 50 lines; public/private source sizes are 373/531
lines. Frozen Ruff, JSON and diff checks passed. The coverage receipt was 99
percent (291 statements and 44 branches). QA subsequently found a Qdrant
role-order extraction parity regression and revoked this freeze. These hashes,
34-test result and coverage are historical only; the replacement frozen QA and
coverage receipt below supersede them. This source QA does not prove source
authenticity, store completeness, runtime, HOME, migration, rotation, recovery
or delivery.

### W25 Replacement Frozen Source QA Receipt

The Qdrant role-order parity RED case exited 1 with an error; the replacement
GREEN validates exact map keys/collection and a typed duplicate-free role set.
The replacement frozen source input passed 35 tests in 11.490 seconds (exit 0)
with 99 percent coverage (exit 0; 292 statements, two misses, 44 branches and
zero partial branches). Its public helper SHA-256 remains
`52d6b056dc5f7ca21cbe52222af75da15f7c64bc5084929a1c351b5f62df9cdc`; its
private semantics SHA-256 is
`67ee2c09ca74d1231690c2bcb5c1bc96cf342ee26f46f1a2ef097f0d6335e56e`; and
the unit and contract inputs are respectively
`af2ff71c0196cb4f47074cb19b0150e15697731e9d03a3d58e8718505fca7deb` and
`72b45ab9c9b2736198a382392a2b08aee1b0a375e30bba9175b3bbab974cd175`.
Ruff check, Ruff format, diff checks and independent code review passed with no
Critical or Important finding. Maximum function length is 46 lines in the
public module and 37 in the private module. This confirms frozen SOURCE/UNIT/
STATIC input only; runtime, source authenticity, store completeness,
HOME, migration, rotation, recovery and DELIVERY remain `NOT_RUN` or pending.
Independent security review passed with no open Critical, High or Medium
finding; the narrow Gitleaks exceptions passed. Authoritative prior-store
authentication/atomic persistence/completeness, real Git bytes/license/ACL and
live query/cache/index revocation, DB/Qdrant/S3/outbox/credentials,
backup/restore/HOME and delivery remain `NOT_RUN`.

The P09 issuance PR #414 was already merged at
`cac9e10fa584754706598d624654e07e8d6531f4`; its prior receipt does not prove
this source payload's future PR QA or delivery. A later native corpus run
exited 3 because the Evidence Result `BLOCKED` is outside the registered
result domain. The row below now records `NOT_RUN` while preserving the
coordinator-pending integration condition; final corpus/metadata and full-index
QA remain to be run on the final staged input.

A later changed-metadata run against base `cac9e10fa584754706598d624654e07e8d6531f4`
selected 16 documents and exited 1 with two `task-lifecycle-events-invalid`
violations: the SPEC and Plan frontmatter transitions lacked registered
evidence. The parent `blocked` to `in-progress` lifecycle rows above correct
that exact omission; no transition override or validator change is used.

### Issuance Verification

Independent rules review found no remaining P1 or P2 contract finding. An
initial metadata check returned exit 1 because W25's Dependencies cell had an
unregistered prose value, and the corpus check returned exit 3. The dependency
was corrected to `None` and the non-existent CLN criterion placeholder was
removed; archive-profile diagnostics in that initial metadata run were outside
these three files.

The corrected issuance input passed: metadata check-changed (base
`a03c8930a5a15a82f4176bbcfe457bc2ce09db4b`, the three issuance paths) exited
0 with three selected documents and zero violations; corpus exited 0; document
links exited 0 for 1,170 documents and 11,455 links, with one warning that
2,870 legacy links have no capture source; their historical resolution remains
unverified; and `git diff --check` exited 0. The initial link-scan input Task SHA-256 was
`ac280709c59e8a6bf0f081a1736aabad69fd01361dea250fc7545b50014a2e7f`;
metadata/corpus receipts name the base SHA and selected three paths. These prior
checks predate final Task prose and readiness. Coordinator PR and delivery
evidence are still `NOT_RUN`; final-head PR QA revalidates this source.

The first final corpus run rejected the Markdown lifecycle evidence link; it
now uses the registered bare anchor. The first local-staged controller run
reported MD029 because an auto-formatter rewrote criterion 13 to 12. The narrow
MD029 guard around criterion 13 preserves the issued CLN criterion 12 and P09
criterion 13; final verification remains with the coordinator.

The issuance command recipe is the changed-document metadata check with the
recorded base and three issuance paths, the corpus lifecycle check, document
links with `--root . --mode all`, and `git diff --check`. Re-run those commands
on the final staged input before delivery; no implementation or runtime command
is implied by this documentation issuance.

### Historical Delivery Status and Superseding Local Integration

Read-only GitHub API verification confirmed that [PR #417](https://github.com/buenhyden/hy-home.docker/pull/417)
was merged at `abe2b8b19a2fe17cd08f06681f338a0e07a4c3f9` on
2026-10-10T14:51:45Z. Its [hosted candidate run](https://github.com/buenhyden/hy-home.docker/actions/runs/38060606376)
finished with failure at source head
`0e696adc9733b081cc9e47477d8f66eaaa4b3433`. The receiving worker attributed
the lifecycle diagnostic to SEC01 Task 0009; that diagnostic detail is the
worker's report, while the API independently confirms the merge and failed run.
Neither the merge nor later local repairs turn that historical CI result into
PASS. Preserve the coordinator's lifecycle reconciliation above together with
this later received failure evidence; do not replace this Task with the older
foreign working copy.

The current user instruction requires local `main` integration without PRs,
remote push or remote merge and prohibits dev. It supersedes the prospective PR
sequence below for this continuation. Keep reviewed source commits, validate the
current affected documents and registered local gates, and preserve operational
NOT_RUN boundaries. This is preparation only: actual Wiki application and
operational resources remain unimplemented; no external workspace, collection,
credential, runtime client or schedule is created by this receipt.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Task issuance and allocation scan | 13 | W25 | Existing Task and worktree inventory; no Task 0009 issuance | `a03c8930a5a15a82f4176bbcfe457bc2ce09db4b` | PASS | This Task | pending |
| Issuance contract review | 13 | W25 | Independent rules review | Corrected three-document issuance contract | PASS | This Task | pending |
| Issuance static checks | 13 | W25 | Metadata, corpus, links and diff checks; pre-final-prose input | Base SHA and three issuance paths; initial link-scan Task hash above | PASS | This Task | pending |
| Received P09 source and RED/GREEN | 13 | W25 | Immutable worker tree and coordinator root-match comparison | `aa110d58e8de2b8b37eb3c5ad4f4de854ee86299`; received source hashes | PASS | W25 received execution handoff | pending |
| Pre-finding P09 synthetic UNIT and coverage | 13 | W25 | Dedicated suites: 21 tests; 99 percent helper branch coverage | Superseded worker helper `51044ec43592c8eccf40774d821016784e562bb0d30a59bd66d38685b3ecc0af` | PASS | W25 received execution handoff | rejected |
| Trusted-policy job-bound finding | 13 | W25 | `max_attempts=1000000000` and `timeout=2147483647` admitted | Pre-fix integration payload; corrected by replacement QA | FAIL | W25 security finding | rejected |
| Scoped Gitleaks static boundary | 13 | W25 | v8.30 exact public-checksum rule and negative path/hash/target-rule probes | Synthetic source and blog digests | PASS | W25 security finding | pending |
| First-round frozen QA receipt | 13 | W25 | 24 tests, 99 percent coverage, Ruff, independent security 24 tests and Gitleaks scans | Superseded frozen helper/schema/test input in W25 frozen fix receipt | PASS | W25 frozen fix receipt | rejected |
| Revoked frozen source QA | 13 | W25 | 34 tests in 4.670s; functions below 50 lines; Ruff/JSON/diff | Superseded pre-replacement public/private helper and unit/contract/job inputs | PASS | W25 revoked frozen source QA receipt | rejected |
| Replacement frozen source QA | 13 | W25 | Qdrant parity RED/GREEN; 35 tests in 11.490s exit 0; 99-percent coverage exit 0; Ruff/diff | Replacement public/private helper and unit/contract inputs in W25 receipt | PASS | W25 replacement frozen source QA receipt | pending |
| Replacement security review | 13 | W25 | Independent review and narrow Gitleaks exceptions | Replacement frozen source input; runtime and delivery remain NOT_RUN | PASS | W25 replacement frozen source QA receipt | pending |
| Common registration and delivery | 13 | W25 | Historical script registration and owning-Spec delivery; current local continuation is separate | PR #417 merge `abe2b8b19`; hosted candidate run `38060606376` at `0e696adc` failed | FAIL | Historical Delivery Status and Superseding Local Integration | pending |
| HOME, migration, rotation and recovery | 13 | W25 | No operational action is authorized by preparation | No concrete operational target | NOT_RUN | Future exact Task | pending |

## Review and Completion

The replacement implementation met its frozen source-level QA target, but this
Task remains in progress. Run the current 35-test coverage plus the unchanged
eight registration regressions, changed document metadata/link checks,
manifest/workflow checks, `git diff --check` and the registered changed gate on
the final integration input. Record command, input SHA, exit code and failures
here. Candidate CI, independent review and delivery remain required. Do not
substitute synthetic results for application/runtime evidence.

Use logical Conventional Commits, an owning SPEC-0204 PR, latest-head required
CI and independent contract/code/security review before coordinator-directed
merge. Review records must separate SOURCE, UNIT, STATIC and ISOLATED evidence
from HOME, MIGRATION, ROTATION, RECOVERY and DELIVERY. No latter category is
complete from preparation evidence; actual runtime resource changes remain 0.

## Related Documents

- [SPEC-0204](../spec.md)
- [SPEC-0204 Plan](../plan.md)
- [REQ-0027](../../../01.requirements/0027-home-development-host.md)
- [AD-0031](../../../02.architecture/descriptions/0031-home-development-host.md)
- [ADR-0046](../../../02.architecture/decisions/0046-capability-tiers-and-quality-boundary.md)
- [Project registration](../../../../infra/09-platform-ops/project-registration/README.md)
