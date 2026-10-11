---
title: "P08 Operations Document Layout Task"
version: "0.1.1"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-11"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0015"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-11"
---

# P08 Operations Document Layout Task

## Objective

Deliver SPEC-0212 requirement 25 through Plan W56–W62 and Spec criterion 8: one
meaningful location for each current Stage05 Guide, Policy and Runbook, populated
folder READMEs, synchronized path consumers and a verified owner handoff.
Perform actual LAB document moves within the three operations families while
excluding LAB runtime/source/secret/data changes. Reuse completed SPEC-0227 body
refresh and preserve completed P00 Tasks, issued identities and created dates.

## Inputs and Authorization

The coordinator issues SPEC-0204-TSK-0015 through this reviewed documentation
commit after observing maximum issued Task number 14 across Git history and
confirming no issued 15, including the foreign root. No implementation or move
is admitted by the issuance commit.
No new Spec is allocated.
Initial branch `codex/p08-operations-document-layout` and dedicated worktree
`.worktrees/p08-operations-document-layout` start at
`4c83f14b11a77e13e582eb85d0bf256685472a95`. The coordinator's direct remote,
origin/main and local-main observation identified that same revision. Recheck
these refs, HEAD and dirty paths before each implementation unit. Preserve the
foreign root Task4 and all other uncommitted files; do not reset, stash or clean.

The user P08 prompt is execution input; its reference planner is comparison
material, not accepted code or corpus classification. Read the current Spec,
Plan, Registry/templates and actual tracked operations documents. The separate
source integration input `c7d56a383ad8b77dd615327d11605b3e15d2146e` reached
exit 124 at the coordinator's 30-minute aggregate limit. Its public explain
listed ten routes; the actual LOCAL plan contains 33 executable nodes, including
local-only checks. Completed-node evidence is retained; the same runner is
resuming the remaining registered nodes on that fixed input. No original
aggregate PASS or main delivery is claimed. Adopt its reviewed final main SHA
only after actual integration.

This admission proposal owns this Task and additive active SPEC-0204 Spec/Plan
routing only. Completed SPEC-0212/P00 and SPEC-0227 records remain byte-preserved.
After issuance the worker may prepare a new pure helper at
`scripts/lib/document_governance/operations_moves.py` only if an audit finds no
existing owner to reuse; its dedicated unit-test path is
`tests/lib/document_governance/test_operations_moves.py` and public fixtures
belong under `tests/fixtures/document_governance/operations-moves/`. Provide
READMEs for new fixture folders and their relevant parent family. No duplicate
planner, document registry, generated table owner or fixed corpus count is
authorized. Planning helpers must not move files or run services.

Shared changes are coordinator proposals until an exact writer lease transfers:
Registry/schema/discovery/profile/heading, operations catalog and Guide binding,
manifest/workflow/CI registration, documentation indexes and feature-owned
documents. The source coordinator currently owns those common consumers.
No old and new path may have simultaneous independent writers. Independent
reviewers inspect exact changes without editing the implementation.

The exact LAB destinations are `docs/05.operations/guides/labs/`,
`docs/05.operations/policies/labs/` and `docs/05.operations/runbooks/labs/`.
Repository-root `labs/`, LAB services/Compose/images/secrets/data and all native
execution remain OUT_OF_SCOPE. Learning applications are excluded even from
planning; Wiki stays preparation only. This Task creates no application,
workspace, DB, credential, consumer or operational workload.

The latest direct-user delivery lane is local main, without dev or required PR.
Keep logical owning-Spec commits, exact-head checks and independent review.
Do not push or create a PR during issuance. If a later remote route is adopted,
report its actual PR/check/merge evidence separately from local results.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0204-TSK-0015 | draft | ready | #inputs-and-authorization |
| SPEC-0204-TSK-0015 | ready | in-progress | #continuation-baseline-and-w56-reuse-result |

### Admission correction history

The uncommitted SPEC-0212 Task6 proposal failed actual metadata validation,
exit 1: 3 documents selected, 146 violations. Adding work to that completed
package caused invalid-package fallback/cascades; this was not an archive
defect or a PASS. Independent review held the proposal. The coordinator
preserved its exact files and restored only the owned parent edits, removing
the uncommitted draft. Task6 was never formally issued or committed. This
replacement uses active SPEC-0204 criterion 8; no completed-parent lifecycle
transition, archive rewrite or validator exemption is introduced.

### W56 Admission and reuse audit

Record actual main/origin/remote/HEAD/dirty state and owner leases. Reuse current
Registry/profile/catalog/link discovery APIs where suitable. The initial tree
contains operations catalog, taxonomy, Registry and metadata-profile helpers;
no dedicated operations-moves helper was found in the scoped filename search.
This observation is not a completed semantic reuse audit or source test.
The observed flat corpus of 230 documents (79 Guides, 76 Policies, 75 Runbooks)
is a dated planning observation, not a new validator constant or final move map.

### Continuation baseline and W56 reuse result

Fresh coordinator observations place this dedicated P08 worktree, local `main`
and `refs/remotes/origin/main` at
`c26c3b93f4e73034ddad4d08ba9da8eaa9fec0c7`, with this worktree clean. The
remote observation follows a fetch; the coordinator did not push this revision.
The initial `4c83f14b11a77e13e582eb85d0bf256685472a95` baseline remains a dated
issuance receipt. The shared root checkout still has 24 foreign paths, and the
preserved old P05 checkout still has 28 staged foreign paths. Neither set was
staged, changed, reset, stashed or cleaned for P08.

The scoped reuse audit found a real gap for a **pure semantic mapping
preflight**, not a second Registry, parser, discovery service or move executor.
It confirms that `frontmatter_record_from_text`, Registry classification and
path matching, and `taxonomy.validate_stable_identity` are available for their
existing responsibilities. The new pure helper calls `taxonomy.classify_path`,
which delegates to the existing Registry matcher; it does not call a second
classifier. Current flat-path consumers remain coordinator owned: operations
catalog assumptions at lines 1666, 2274 and 2302,
metadata-profile parent matching at line 872, heading handling at line 1103,
and the flat Registry and Script Manifest contracts. Those observations define
future coupled-consumer work; they do not accept nested paths.

One worker may now implement only the new helper and dedicated fixtures/tests
for W56/W57 under its exclusive lease. That helper validates candidate mapping
input and cannot move files, choose a final corpus classification or establish
W58 nested-consumer acceptance. The coordinator remains the single writer for
shared registration and for any separately delegated, exact registration/test
lease; this is not a blanket common-consumer mutation. The full W57 map is being
read and drafted; no exact move map, writer lease or LAB classification is
approved yet. W58–W62 remain NOT_RUN. Actual document renames and LAB runtime
changes remain zero.

The initial semantic review identifies six subject cohorts as candidates only:
0022 Valkey, 0025 Cassandra, 0026 CouchDB, 0027 MongoDB, 0031 PostgreSQL
cluster and 0062 Locust (18 typed files total). Subject 0074 combines laboratory
optimization with management and experiment services, so it is not an automatic
LAB classification. Mixed subjects 0019 OpenSearch and 0036 Kafka remain
review-required. These are body-based review observations, not a move list or
approval to relocate any file.

The independent draft review found four unresolved mapping defects: 51 service
bindings are missing, fenced-code headings need explicit handling, nine targets
have prefixed paths, and generated-source ownership is unproven. Corrections are
closed for that draft only. The historical draft-review FAIL remains recorded;
it is not a move, runtime or consumer-validation result. The latest final map
is NOT_RUN and pending its exact approval.

### Source preparation receipts and final-gate boundary

The pure mapping-preflight helper has 22 scoped tests and 100% scoped coverage.
The coordinator QA receipt reports 134 registry-plus-helper tests and 111
workflow tests, and a six-path common change received independent review with
an ACCEPT result. The indexed manifest/workflow check completed with exit 0.
The QA RED/GREEN correction adds a finite fixture admission in
`metadata/profile.py` with the existing registry test; it is not a W58 path
migration. The rejected intermediate evidence used non-canonical result or
acceptance values and Markdown lifecycle anchors. Those validation failures are
preserved as corrections, without a waiver or override.
These are source-preparation receipts only: the helper validates candidate input
and does not choose a final mapping or accept a nested consumer.

The initial corrected Task-only metadata check exited 0 and selected one path:
this Task. Its target filter excluded three fixture paths, so it is not fixture
README coverage evidence. The scoped staged check exited 0 on the pre-correction
12-byte candidate, and the final lifecycle check exited 0 after the raw-anchor
correction. Final metadata, final staged validation and the registered aggregate
remain NOT_RUN pending the exact final candidate; no PASS is claimed for them.

The received map draft reports the same 230 source paths and hashes with 29
target differences (11 Guide, 9 Policy and 9 Runbook). Those counts are dated
observations, not validator constants. Its external aggregate `015957` and
corrected internal aggregate `a2ec20` are separate artifacts. Exact writer
leases, final mapping approval and all moves remain pending.

### W57 Exact semantic mapping

Enumerate `git ls-files docs/05.operations` and parse each actual frontmatter
type, artifact ID, title, implementation_services, body and links. Review one
old-to-new exact path row per target with reason, subject owner, LAB decision,
anchors, relative command working directory and generated-source owner. Match
by exact path and artifact ID; reject conflicting mappings. Equal numeric IDs
across different document families do not establish equal subject or LAB status.
Unclassified or conflicting subjects remain review-required, with a named next
decision; do not hide them in common. Create only populated meaningful domains.

### W58 Path contract and regression unit

Current blockers include flat Registry paths, direct catalog/Guide-parent
assumptions, immediate-parent profile matching and flat Runbook authority tests.
Confirm each against the actual adopted source before proposing a change.
Add RED fixtures for suffix/arranged paths, same-number different-family IDs,
three actual LAB destinations, README selection/coverage, traversal, unknown
domains, duplicate IDs and case collisions. Centralize existing discovery and
classification where possible; do not exempt filenames or sealed history.
Required boundary coverage is at least 80% for a new meaningful helper, with
independent code/security review. Reference examples are not full-corpus proof.

### W59 Preservation and move lease

Freeze input SHA and SHA256 for each leased document and shared consumer. Bind
artifact ID, created date, command/warning/recovery/evidence content and anchors
before the exact move. Review necessary relative-link and command-directory
adjustments rather than broadly refreshing all bodies. Use a bounded
archive-aware historical path map only if needed; it cannot duplicate active
documents or rewrite sealed records. Prepare an inverse exact mapping and
expected restored consumer/link checks before mutation of document paths.

### W60 Exact rename and coupled references

Only after feature writers finish their leased source, one writer performs
`git mv -- old new` with reviewed exact paths and coupled links/indexes/generated
projections. The command form is illustrative until the reviewed map supplies
real paths. Stop on a changed input and integrate both changes explicitly.
Each artifact remains in one active location, including actual typed LAB moves;
root LAB runtime/source/secret/data diff must be zero. A separate_target-only
plan is insufficient completion. No Docker or native operator command is run.

### W61 Populated READMEs

Write Korean metadata-valid READMEs for the Stage05 root, all three parent
families and each populated destination. Include purpose, included/excluded
scope, document ID/Korean title/exact link/one-line role, contribution criteria,
source/parent/related navigation, owner and verification. Explain Guide usage,
Policy controls/exceptions and Runbook execution/verification/recovery. Folder
routers link direct children; no empty advertised domain or placeholder summary
counts as complete. LAB READMEs explicitly distinguish document relocation from
unchanged LAB operations. Verify new READMEs are actually selected by metadata.

### W62 Final validation, delivery and handoff

Bind every final check to actual command, input revision, exit code and result.
Run path/ID/profile/language/body/lifecycle, active-link/anchor, command-directory,
catalog/binding, affected changed-CI and staged checks on the final candidate.
Broken active links must be zero; prove one active location per ID and complete
populated-folder README coverage. Preserve earlier failures and corrections.
Obtain independent current-head review before local-main integration. Deliver
old-to-new paths, IDs, source/target hashes, anchors, generated owner, rollback
map and final main SHA to SEC/SMTP/CLN/P01–P07/P09/P10 owners as relevant. A path
handoff does not complete any feature's runtime acceptance.

### Initial issuance verification — 2026-10-11

On the dedicated branch based on `4c83f14b11a77e13e582eb85d0bf256685472a95`,
the coordinator checked only the two active parent documents and this Task.
`check-document-metadata.py --mode check-changed --base-ref HEAD` with the three
explicit paths returned exit 0, selected 3, violations 0. After the source-gate
status clarification, the Task-only rerun returned exit 0, selected 1,
violations 0. `check-document-links.py --mode all` returned exit 0, 1205 documents,
11660 links, failures 0 and one existing archive-capture warning; historical
resolution was not verified. `check-document-corpus-lifecycle.py --base-ref HEAD`
returned exit 0, violations 0, with 5 archive migrations, 140 tombstones,
351 preserved records, 286 decisions and 374 recovery rows.

Independent exact-diff review accepted the active SPEC-0204 ownership, unique
W56–W62/Task15 routing and typed LAB destinations with no Critical or Important
finding. The final metadata and staged reruns bind the receipt-bearing bytes
before this commit. These admission checks do not complete the semantic reuse
study, full-corpus move map, helper tests, path-contract changes or relocation.
Functional source-gate input remains separate at `c7d56a383`; its original
aggregate exit 124 is preserved. No remote or operational command was executed.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Admission and reuse audit | 8 | W56 | Fixed-input reuse and ownership audit found a pure preflight gap; no source test or criterion completion is claimed | Fresh local/remote observation c26c3b93; source candidate c7d56a383 retained separately | PASS | W56 admission and reuse audit; continuation baseline | accepted |
| Semantic move map | 8 | W57 | Historical draft-review FAIL was corrected for the draft; final exact review, approval and writer leases remain pending | Actual tracked operations corpus at adopted source SHA | NOT_RUN | W57 exact semantic mapping; continuation baseline; source preparation receipts | pending |
| Path-contract regressions | 8 | W58 | RED/GREEN, scoped coverage and independent review of reused/new consumers | Frozen helper/tests/shared proposal hashes | NOT_RUN | W58 path contract and regression unit | pending |
| Preservation and rollback proof | 8 | W59 | Bind source hashes, original content, anchors, leases and inverse mapping | Reviewed exact source/target map | NOT_RUN | W59 preservation and move lease | pending |
| Atomic document relocation | 8 | W60 | One active location, coupled references and LAB runtime/source diff zero | Fixed feature-owner SHAs and transferred writer leases | NOT_RUN | W60 exact rename and coupled references | pending |
| Populated README coverage | 8 | W61 | Korean content, metadata selection, meaningful descriptions and navigation | Actual destination corpus and parent families | NOT_RUN | W61 populated READMEs | pending |
| Exact-head delivery and handoff | 8 | W62 | Actual affected gates, staged checks, independent review and local-main receipt | Final candidate/main SHA and exact inverse map | NOT_RUN | W62 final validation, delivery and handoff | pending |

## Review and Completion

This issuance and continuation deliver bounded documentation preparation only.
The initial admission STATIC checks and the bounded helper UNIT receipt are
recorded above. Final preparation STATIC and DELIVERY remain pending their
actual commands and exact final input. Full relocation UNIT, STATIC and DELIVERY
also remain pending until their actual commands and final inputs are recorded.
ISOLATED, HOME, MIGRATION, ROTATION and RECOVERY are NOT_RUN, and no operational
effect or service recovery is claimed. Current parent status and historical
P00/refresh evidence remain unchanged.

Use separate reversible logical commits for path-contract/tests, coupled exact
rename/link changes, populated README content and final validation/handoff.
Stage only owned files/hunks. Roll back only the reviewed inverse rename/link/
README and coupled source-contract unit, then revalidate identity uniqueness,
active links and consumers; never reset or delete another worker's changes.
Final receipt must name actual changes, excluded paths, acceptance mapping,
commands/input SHA/exit codes, failures/corrections, review and local delivery.
Remote push/PR/hosted CI is NOT_RUN unless actually executed in an adopted lane.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Completed P00 Task](../../0212-request-baseline-and-reconciliation/tasks/tsk-0003-active-contract-and-exclusions.md)
- [Operations documentation navigation](../../../05.operations/README.md)
- [Stage05 refresh owner](../../0227-stage05-format-refresh/spec.md)
- [Request routing](../../0212-request-baseline-and-reconciliation/spec.md)
