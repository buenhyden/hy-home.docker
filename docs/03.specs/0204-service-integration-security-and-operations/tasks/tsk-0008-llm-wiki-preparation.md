---
title: "LLM Wiki Preparation Task"
version: "0.1.0"
type: "sdlc/task"
status: "ready"
owner: "@buenhyden"
updated: "2026-10-10"
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
release or runtime write. Before main integration, the recovery action is a
logical revert of these three issuance documents. A PR receipt, required
latest-head checks and coordinator-directed merge remain pending.

The preparation input records future source allowlists for `blog-data/dev`,
`Project-Template/dev`, `hy-home.docker/main` and `hy-home.k8s/main`. A future
application bootstrap must use a verified Project-Template `main` release;
that release and its license are currently unknown. The shared brief was
reachable by title only; its body was not read. Neither gap permits inference.

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

Ready contract issuance: the issuance branch contains no accepted P09
implementation. That observation is separate from unaccepted worker-owned
local material.

### W25 Issuance and Boundaries

The remote baseline `a03c8930a5a15a82f4176bbcfe457bc2ce09db4b` contains Tasks
0001 through 0006 and no issued Task 0008. A previous proposal of Task 0009
was never issued. Task 0008 is allocated after that scan. Pending CLN01 Task
0007 is preserved outside this Task. A separate P09 worktree now has an
in-progress, uncommitted Task 0008 plus helper, fixture and test material.
This issuance formalizes the same identifier but does not accept, copy, test,
or classify that worker-local material. Preserve its work log for later
integration and reconcile it against W25/criterion 13 after a reported handoff.
The earlier SEC-before-P09 issuance convention is withdrawn: W25 may start its
independent preparation files now, while coordinator-owned shared files
integrate serially.

The eventual owner may create only the following new P09 surface:

- `infra/09-platform-ops/project-registration/wiki-preparation/` with Korean
  README navigation, preparation contracts, `schemas/` and `fixtures/`;
- four schemas for future consumer manifests, source/artifact provenance,
  job/outbox/handoff state, and blog-data handoff; valid/invalid synthetic
  fixtures for each;
- `scripts/lib/ops/wiki_preparation.py`, a pure offline helper that accepts
  parsed contracts and caller-provided synthetic bytes only; and
- `tests/lib/ops/test_wiki_preparation.py` and
  `tests/validation/test_wiki_preparation_contracts.py`.

Every new preparation folder, including `schemas/` and `fixtures/`, needs its
own README. A newly needed parent-family README is a coordinator-owned shared
integration change, not a worker-side shortcut.

The helper has no filesystem, network, environment, subprocess or external
write access. It checks cross-field project namespaces, selected candidate and
exact write sets, content hashes and idempotency. Hash format or fixture
equality is not source authenticity, license, ACL or runtime proof.

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

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Task issuance and allocation scan | 13 | W25 | Existing Task and worktree inventory; no Task 0009 issuance | `a03c8930a5a15a82f4176bbcfe457bc2ce09db4b` | PASS | This Task | pending |
| Issuance contract review | 13 | W25 | Independent rules review | Corrected three-document issuance contract | PASS | This Task | pending |
| Issuance static checks | 13 | W25 | Metadata, corpus, links and diff checks; pre-final-prose input | Base SHA and three issuance paths; initial link-scan Task hash above | PASS | This Task | pending |
| Preparation schemas, fixtures and helper | 13 | W25 | Future RED/GREEN unit and contract validation | New P09 artifacts | NOT_RUN | Planned P09 surface | pending |
| Generic registration regression | 13 | W25 | Existing project-registration validation | Current main and future changed input | NOT_RUN | `tests/validation/test_project_registration.py` | pending |
| Independent review and delivery | 13 | W25 | Latest-head review, required CI and owning-Spec PR | Future P09 branch and PR | NOT_RUN | Future delivery receipt | pending |
| HOME, migration, rotation and recovery | 13 | W25 | No operational action is authorized by preparation | No concrete operational target | NOT_RUN | Future exact Task | pending |

## Review and Completion

Before implementation, add meaningful RED cases for rejected namespaces,
selected-write-set overreach, required fields and stale/revoked artifact
handling; turn them GREEN with the narrow helper. Maintain at least 80 percent
coverage for that helper, not as a claim about the future Wiki. Run the new
unit and contract tests, the existing registration regression, changed document
metadata/link checks, manifest/workflow checks when registered, `git diff
--check`, and the registered changed gate. Record command, input SHA, exit code
and failures in this Task. Do not add tests solely for this documentation-only
issuance.

Use logical Conventional Commits, an owning SPEC-0204 PR, latest-head required
CI and independent contract/code/security review before coordinator-directed
merge. Review records must separate SOURCE, UNIT, STATIC and ISOLATED evidence
from HOME, MIGRATION, ROTATION, RECOVERY and DELIVERY. No latter category is
complete from preparation evidence.

## Related Documents

- [SPEC-0204](../spec.md)
- [SPEC-0204 Plan](../plan.md)
- [REQ-0027](../../../01.requirements/0027-home-development-host.md)
- [AD-0031](../../../02.architecture/descriptions/0031-home-development-host.md)
- [ADR-0046](../../../02.architecture/decisions/0046-capability-tiers-and-quality-boundary.md)
- [Project registration](../../../../infra/09-platform-ops/project-registration/README.md)
