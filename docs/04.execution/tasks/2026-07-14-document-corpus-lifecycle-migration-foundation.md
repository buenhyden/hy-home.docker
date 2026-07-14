---
status: active
artifact_id: task:2026-07-14-document-corpus-lifecycle-migration-foundation
artifact_type: task
parent_ids:
  - plan:2026-07-14-document-corpus-lifecycle-migration-foundation
---

# Task: Document Corpus Lifecycle Migration Foundation

## Overview

This Task is the durable execution ledger for Spec 131 and its six-unit
Foundation Plan. It records the approved baseline, bounded file responsibility,
fresh-agent assignments, RED/GREEN commands, independent reviews, logical
commits, generated evidence, controlled all-files result, and final closure.

Planning evidence was created on branch
codex/document-corpus-lifecycle-migration in linked worktree
.worktrees/document-corpus-lifecycle-migration. Implementation results remain
not run until recorded under the matching work unit.

## Inputs

- Spec: docs/03.specs/131-document-corpus-lifecycle-migration-foundation/spec.md
- Plan: docs/04.execution/plans/2026-07-14-document-corpus-lifecycle-migration-foundation.md
- Approved baseline: e00e1483
- Foundation work units: T-DCLM-001 through T-DCLM-006
- Current canonical audit:
  docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md
- Machine metadata owner:
  docs/99.templates/support/document-metadata-profiles.yaml
- Controlled QA owner:
  scripts/validation/run-agent-precommit-all-files.sh

## Goals and Non-goals

Goals:

- establish the migration, archive, retention, manifest, directory-budget, and
  review-signal control plane;
- add tested metadata and lifecycle validators with deterministic safe output;
- align Stage 00, Stage 98, Stage 99, local QA, and tracked CI definitions;
- publish the approved Foundation manifest and generated evidence;
- close with independent task and whole-branch reviews plus controlled
  all-files evidence.

Non-goals:

- migrate the active, operations, historical, archive, reference, generated,
  or README corpus;
- move Stage 04 leaves into year partitions;
- create immutable snapshot payloads;
- change Compose, infrastructure, deployment, secrets, provider-global
  settings, model policy, remote GitHub state, releases, or environments.

## Scope and Change Boundaries

Allowed authored paths:

- docs/00.agent-governance rules and progress memory directly required by
  Foundation;
- Spec 131 and its Stage 03 routing;
- this Plan, this Task, and existing Stage 04 routing;
- docs/90.references data/governance lifecycle evidence, canonical generated
  outputs, and routing;
- docs/98.archive/README.md only;
- Stage 99 support contracts and the common archive template;
- .github/workflows/document-corpus-lifecycle.yml;
- .pre-commit-config.yaml existing repo-contract routing only;
- scripts/README.md and Foundation validation/QA scripts;
- tests/validation focused Foundation tests.

Prohibited paths and actions:

- existing Stage 01 through Stage 05 corpus leaves;
- all 20 existing Stage 98 tombstones and any archive snapshot payload;
- broad Stage 90 authored corpus rewrites;
- _workspace diagnostics, local logs, auth files, tokens, credentials, private
  keys, shell history, raw logs, or secret values;
- runtime Compose, infra, deployment, environment, release, provider-global,
  or remote GitHub mutation;
- direct pre-commit run --all-files, --no-verify, history rewriting, or
  destructive Git cleanup.

Compose impact: none.

Security impact: validation and redaction hardening only. No credential,
secret-store, identity, network, runtime policy, or security-resource change.

Operations impact: documentation lifecycle governance only. No service,
incident, release, deployment, or on-call behavior changes.

Runtime impact: none. The tracked workflow is read-only quality automation and
does not deploy or mutate third-party state.

## Approval Evidence

Approval source:

- The user approved the hybrid archive model: provenance tombstone plus
  immutable Git commit/blob by default, with checksum-backed full snapshots
  only for audit, legal, or evidence-preserve cases.
- The user approved the six-package program and explicitly instructed
  continued implementation.
- The user approved Subagent-Driven execution with a fresh implementation agent
  and separate review agents.

Protected surfaces:

- Stage 00 and Stage 99 contracts may be changed within the approved
  Foundation scope.
- Existing archive tombstones, snapshot payloads, runtime surfaces, secrets,
  provider-global configuration, and remote GitHub state remain protected.

Approval boundary:

- Foundation contracts, validators, tests, local QA routing, and tracked
  read-only workflow definitions are authorized.
- Later Waves A through E, snapshot admission, runtime work, and remote
  mutation require their own approved Spec or explicit user approval.
- Local merge to main is excluded until finishing and separate user approval.

Rollback or recovery:

- Revert one logical Foundation task commit range in reverse order.
- Regenerate only derived outputs owned by the reverted task.
- Never use git reset --hard or rewrite branch history.

Redaction boundary:

- Evidence records commands, exit codes, stable finding codes, bounded paths,
  counts, and Git object identities.
- It never records body payloads, snapshot bytes, secret values, tokens,
  credentials, auth files, private keys, shell history, or raw logs.

## Work Breakdown

| Work unit | Responsibility | State |
| --- | --- | --- |
| T-DCLM-001 | Machine migration contract and static archive metadata | Complete — final Spec PASS and Quality PASS with Critical 0, Important 0, Minor 0 |
| T-DCLM-002 | Lifecycle companion, Git provenance, deterministic data | Complete — final range `9126a0aa..9fe234f6`; terminal Spec PASS and Quality retry PASS, each with Critical 0, Important 0, and Minor 1. The sole deferred Minor is behavior-preserving decomposition of the monolithic dispatcher. |
| T-DCLM-003 | Human contracts, archive template, Stage 98/00 routing | Not run |
| T-DCLM-004 | Repository contracts, local QA, tracked workflow | Not run |
| T-DCLM-005 | Foundation manifest and generated evidence | Not run |
| T-DCLM-006 | Full QA, wrapper, whole-branch review, closure | Not run |

## Work Log

| Date | Work unit | Agent role | Result |
| --- | --- | --- | --- |
| 2026-07-14 | Planning | Controller | Spec 131 approved and activated; Plan and Task evidence shell authored. |
| 2026-07-14 | T-DCLM-001 | Fresh implementation agent | Added the exact migration registry, metadata registry v2, fail-closed static archive validation, and RED/GREEN coverage. The authored scope is the Task 1 file set plus `docs/00.agent-governance/memory/progress.md`, included as a documented deviation because the root `AGENTS.md` bootstrap makes progress updates mandatory. Self-review passed; subsequent rows record the independent reviews and remediation. |
| 2026-07-14 | T-DCLM-001 generated fallout | Fresh implementation agent | The first repository-contract run found only the canonical frontmatter semantic inventory stale after registry v2. The controller approved regenerating that owner in the Task 1 generated follow-up together with any LLM Wiki/index coverage fallout; this is a scoped deviation from the brief's two-file generated follow-up list, not broad corpus mutation. |
| 2026-07-14 | T-DCLM-001 specification-review remediation | Fresh implementation agent | Resolved specification findings I-01 and I-02 by machine-declaring exact manifest types, nullability, domains, deterministic ordering, destructive execution prerequisites, and bounded exception semantics. Added static synthetic validation without Git lookup, snapshot-byte access, or a repository exception file. Subsequent independent review confirmed both findings closed. |
| 2026-07-14 | T-DCLM-001 specification re-review remediation | Fresh implementation agent | Resolved I-03 by deriving artifact-ID/status nullability from the selected metadata profile and reusing the canonical non-empty artifact-ID value rule. The `readme` profile proves the declared exception path, while `reference` proves `exempt` cannot bypass required identity/status. No Git lookup or snapshot-byte access was added. |
| 2026-07-14 | T-DCLM-001 quality-review remediation | Fresh implementation agent | Resolved I-Q01 and I-Q02 by sharing the contract-owned immutable-snapshot disposition allowlist with static archive validation and scalar-guarding both archive selectors before conditional membership. Added value-free admission findings, list/mapping regressions for both selectors, and a changed/new CLI no-traceback regression. |
| 2026-07-14 | T-DCLM-001 final independent reviews | Fresh specification and quality reviewers | The complete range `afc51b29..e9db5afb` received Spec PASS with Critical 0 and Important 0 and Quality PASS with Critical 0, Important 0, and Minor 0. I-01/I-02/I-03 and I-Q01/I-Q02 are closed; T-DCLM-001 is complete and T-DCLM-002 is clear to proceed. |
| 2026-07-14 | T-DCLM-002 | Fresh implementation agent | Added the focused lifecycle companion and 22-test suite through strict RED/GREEN. The companion reuses the canonical metadata module without repurposing its `Manifest` type; implements the fixed 16-mode CLI, immutable manifest data contracts, exact YAML load/render, promoted-wave enforcement, introduced-only impact validation, Git commit/blob/path and snapshot SHA-256 provenance, value-free confidentiality findings, duplicate candidates, review signals, 100/150 budgets, bounded exceptions, and deterministic summary/ledger/snapshot interfaces. Self-review PASS; no corpus leaf, existing tombstone, snapshot payload, exception file, runtime, workflow, secret, provider, or remote state changed. |
| 2026-07-14 | T-DCLM-002 generated fallout | Fresh implementation agent | Staged only the new script and test for Git-backed discovery, then ran the four Task 2 canonical owners in the approved order. Only owner-produced changed files are eligible for the separate generated commit; exact freshness results are recorded below. |
| 2026-07-14 | T-DCLM-002 review remediation | Fresh remediation agent | Resolved all seven Important specification findings, all five Important quality findings, and both Minor quality findings from the first independent reviews. The companion now validates CLI shape before metadata-module execution, delegates static manifest/exception grammar to the Task 1 canonical validators, processes NUL-delimited deletion/rename evidence and every direct relation class, binds manifest rows to baseline and result truth, preserves unsuppressible explicit safety classes, blocks all remaining `check-full` findings, redacts every declared payload class, reads tracked manifest/snapshot inputs through no-follow directory descriptors, preserves Unicode title identity, and proves all 16 modes through shape, success/write, and exit-class matrices. No Task 3, workflow, runtime, corpus migration, existing tombstone, snapshot payload, secret, provider, or remote surface changed. |
| 2026-07-14 | T-DCLM-002 specification re-review remediation | Fresh remediation agent | The fresh complete-range specification re-review closed I-01 through I-07 and identified I-08: explicit candidate modes incorrectly required a manifest to be staged before the Plan-authorized validation step. Added separate no-follow in-root candidate loading and canonical-byte comparison without the promoted-manifest tracked-file precondition. Real subprocess regressions prove `check-manifest`, `generate-summary`, and `check-summary` accept a safe untracked candidate before staging while all three reject symlink, traversal, and out-of-root candidates without output mutation. Promoted and impacted manifest consumption remains tracked-only. |
| 2026-07-14 | T-DCLM-002 final-review remediation | Fresh remediation and takeover-finisher agents | Resolved final specification I-09 and quality I-FQ01 through I-FQ03. Lifecycle corpus discovery now enumerates tracked regular Markdown blobs, preflights every path component without symlink following, snapshots safe bytes once, and reuses those bytes for link and duplicate inspection. Archive rows bind the original source profile to a canonical validated Stage 98 archive target while preserving stable identity, provenance, replacement, preservation, evidence, and pass/pass review requirements. Directory-budget approval now requires a real tracked regular canonical Plan with active/completed state and pass/pass manifest reviews; missing, untracked, symlinked, wrong-profile, draft, and unreviewed references remain blocked. The companion and focused tests were committed as `eb52185c`; no corpus leaf, tombstone payload, workflow, runtime, provider, secret, or remote surface changed. |
| 2026-07-14 | T-DCLM-002 closure-review remediation | Fresh remediation agent | Resolved closure specification I-09-R1/I-10/I-11, closure quality I-CQ01 through I-CQ05, and M-CQ02. `check-impacted` now admits safe untracked typed Markdown into the same no-follow held snapshot and applies pre-stage 149/150 budgets; diagnostic and generated-output boundaries never forward metadata payloads; archive admission binds the manifest baseline blob, dynamic disposition replacement semantics, and one tracked canonical replacement; partition approval validates canonical Plan metadata, relationships, serialization order, placeholders, and body role. Generated Markdown tables escape control and pipe characters. No Task 3, corpus leaf, existing tombstone, archive payload, exception, workflow, runtime, provider, secret, or remote surface changed. |
| 2026-07-14 | T-DCLM-002 final acceptance remediation | Fresh remediation agent | Resolved specification I-12 and quality I-AQ01 through I-AQ04. Real `check-impacted` now omits only index-owned Markdown paths proven absent by the current unstaged delete/rename state while retaining old paths as relation triggers and new rename paths as current records; unsafe modes, symlinks, non-regular paths, malformed Git output, and unexpected I/O remain fail-closed. Every top-level corpus safety path is sanitized before output. Merge replacements resolve uniquely to the tracked canonical merge result by path or artifact ID; optional delete replacements receive the same canonical proof. Archive result relations validate against one held full current/result manifest, including all multi-row result targets, without suppressing missing, self, wrong-type, ordering, cycle, or supersession-state findings. Commit `9bea953b` changes only the lifecycle companion and focused tests; no Task 3, corpus leaf, existing tombstone, archive payload, workflow, runtime, provider, secret, or remote surface changed. |
| 2026-07-14 | T-DCLM-002 release-gate remediation | Fresh remediation agent | Resolved specification I-13 and quality I-RQ01 in commit `6c33c66c`. A merge row remains bound to removed baseline source A while its uniquely resolved held tracked target retains canonical identity B; target path, profile, body, lifecycle state, current bytes, and pre-existing baseline identity are attested without weakening non-merge identity checks. All five writers and three paired checkers now share descriptor-relative no-follow traversal, reject final/intermediate symlinks and non-regular entries with exit 3, admit normal absolute temporary paths, compare held regular bytes, and publish LF bytes through same-directory atomic replacement. Deterministic swap and interrupted-write regressions prove victim preservation, no redirected creation, no partial publication, and temporary-file cleanup. No Task 3, corpus leaf, tombstone, archive payload, workflow, runtime, provider, secret, or remote surface changed. |
| 2026-07-14 | T-DCLM-002 final release-quality remediation | Fresh remediation agent | Resolved I-FRQ01 in `8001a95c` through strict RED/GREEN. A resolved merge target whose stable identity B differs from baseline source A must map to exactly one baseline owner; that owner must preserve canonical ID, inferred and declared type, and lifecycle truth at the current result, or be represented by exactly one same-wave move/merge attestation to that result. Real Git regressions reject a B created only after baseline, both path and ID replacement forms, a baseline duplicate B removed before result, and a wrong-profile baseline B corrected only after baseline. Existing pre-baseline distinct-ID path/ID replacements, an explicitly attested same-wave B move, and same-ID new-target consolidation remain valid. Focused 6/6 and combined lifecycle/metadata 262/262 passed; live, four generated-owner, and repository gates passed. Graphify refreshed to 23,999 nodes / 26,386 edges / 1,561 communities, remained advisory for two unrelated inferred edges and generic graph noise, and was corroborated against tracked Stage 00/03/04/99 and executable owners before restoration. No public API, Task 3 surface, corpus leaf, tombstone, archive payload, workflow, runtime, provider, secret, or remote surface changed. |
| 2026-07-14 | T-DCLM-002 sign-off remediation | Fresh remediation agent | Resolved specification I-FRQ01-R1 and quality I-SQ01/I-SQ02 in `1c9ef624` through strict RED/GREEN. Exact baseline owner paths now require mode `100644` or `100755`, object type `blob`, an exact UTF-8 path match, a full object ID, and blob re-verification before ownership can authorize a distinct-ID merge. A changed same-path owner requires exactly one `migrate` peer with exact source/target/ID/type/status binding, a canonical transition, pass/pass reviews, complete evidence, and no replacement; moved-owner attestations retain their existing `move`/`merge` behavior under the same review/evidence boundary. Real Git fixtures cover parseable `120000` metadata, synthetic `160000`, tree/missing paths, regular modes, path/ID replacements, valid `active` to `completed`, missing/duplicate/wrong/incomplete peers, and reverse transition. No public API, Task 3 surface, corpus leaf, tombstone, archive payload, workflow, runtime, provider, secret, or remote surface changed. |
| 2026-07-14 | T-DCLM-002 terminal independent reviews | Fresh specification reviewer and separate quality retry reviewer | The complete range `9126a0aa..9fe234f6` received Spec PASS with Critical 0, Important 0, and Minor 1 and Quality retry PASS with Critical 0, Important 0, and Minor 1. Every prior Critical/Important gate is closed. Both reviewers retained only the same non-blocking recommendation to decompose the monolithic lifecycle dispatcher in a later behavior-preserving package with characterization/equivalence tests. T-DCLM-002 is complete and T-DCLM-003 is unblocked. |

Each implementation row will record the fresh agent identity, exact bounded
assignment, changed paths, self-review, deviations, and handoff. Reviewer rows
will be separate from implementation rows.

## Verification Evidence

Planned exact command families:

- metadata registry and changed/new checks;
- focused metadata and lifecycle unittest suites;
- Python compile and Bash syntax checks;
- Foundation contract, manifest, provenance, budget, duplicate, and ledger
  checks;
- repository contracts, document traceability, and implementation alignment;
- canonical security, audit-matrix, LLM Wiki, and metadata-inventory
  generation/check modes;
- Graphify refresh and advisory health corroboration;
- controlled all-files wrapper from a clean linked worktree.

Expected evidence:

- RED before each behavior implementation and GREEN after;
- zero Foundation blocking findings;
- legacy full-corpus debt reported as advisory until Wave E;
- deterministic write/check equality;
- no payload leakage or unexpected changed path;
- clean Git status after final closure.

T-DCLM-001 actual evidence:

- RED: `python3 -m unittest tests.validation.test_document_metadata.ProfileSchemaTests tests.validation.test_document_metadata.MetadataValidationTests -v` ran 41 tests and failed with 25 expected assertion failures. The failures were limited to registry schema v2, the absent migration contract, archive enum/condition validation, object/hash/path shapes, and snapshot/replacement conditions.
- Focused GREEN: the same command passed 41 of 41 tests.
- Full GREEN: `python3 -m unittest tests.validation.test_document_metadata -v` passed 187 of 187 tests in 67.458 seconds.
- Compatibility: `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref e00e1483` selected 10 paths with zero violations, zero legacy exceptions, and zero transition overrides.
- Advisory baseline: `python3 scripts/validation/check-document-metadata.py --mode check-active` selected 365 active records and retained the pre-existing 1,290 advisory findings. Its nonzero exit is expected and was not promoted to a Foundation blocking gate.
- Static checks: `git diff --check` and `python3 -m py_compile scripts/validation/check-document-metadata.py` passed.
- Repository integration before the generated follow-up: metadata repository contracts reported zero violations and document traceability passed 46 catalog pairs with zero failures. The aggregate repository-contract gate reported only the expected stale canonical frontmatter inventory; its owner regeneration and final rerun are recorded in the generated follow-up evidence.
- Generated owner fallout: the LLM Wiki index regenerated with 1,300 paths, category coverage regenerated with 1,299 safe paths, and the canonical frontmatter semantic inventory regenerated with 904 records and 2,160 advisory findings. The increase is the explicit Wave D debt created by applying registry v2 to the unmodified existing tombstones; it does not promote those records to changed/new blocking.
- Generated check modes passed for all three outputs. The final `bash scripts/validation/check-repo-contracts.sh` rerun completed with `failures=0`, including metadata repository contracts at zero violations and a fresh advisory inventory.
- Graphify: `graphify update .` completed with 23,485 nodes, 24,978 edges, and 1,545 communities. Health remained advisory only for two unrelated cross-root inferred edges; zero volume, gitlink, generated/minified, source-contamination, or meaningless-god-node findings were reported. The claims above were corroborated against the tracked validator, registries, tests, Stage 00 governance, Spec 131, and this Plan/Task. Generated Graphify outputs were restored and excluded from the commit.
- Specification-review RED: three focused tests failed for the intended missing surfaces: absent manifest field-contract declarations, absent static manifest validation, and absent bounded exception validation.
- Self-review RED: the focused static-manifest method exposed five malformed enum values escaping as `TypeError`; the minimal type-guard fix converted every case to fail-closed `ProfileError` behavior.
- Remediation focused GREEN: the three manifest/exception contract methods passed 3 of 3 tests, including exact loader mutations and synthetic wildcard, global, ownerless, reasonless, permanent, expired, unknown-code, empty-exit, unsafe-evidence, and future-approval cases.
- Remediation full GREEN: `python3 -m unittest tests.validation.test_document_metadata -q` passed 190 of 190 tests in 70.351 seconds.
- Remediation compatibility: explicit-base changed mode selected 10 paths with zero violations, zero legacy exceptions, and zero transition overrides; `python3 -m py_compile` and `git diff --check` passed.
- Remediation repository integration: `bash scripts/validation/check-repo-contracts.sh` completed with `failures=0`, including metadata repository contracts at zero violations.
- Remediation Graphify: `graphify update .` completed with 23,519 nodes, 25,050 edges, and 1,545 communities. The report remained advisory for two unrelated ambiguous cross-root references and generic high-degree/isolated-node noise; the remediation claims were corroborated against the tracked migration contract, validator, tests, Stage 00 governance, Spec 131, Plan, and Task. Generated Graphify outputs were restored and excluded from the fix commit.
- I-03 RED: four focused methods produced the three intended defect signals (two assertion failures and one migration-validation error) while the positive declared `readme` profile exception passed. The failures proved that the contract still named `disposition-exempt`, a typed `reference` row could null required identity/status, and the migration-only lowercase/colon grammar rejected a canonically valid non-empty ID.
- I-03 focused GREEN: the same four methods passed 4 of 4, covering the exact contract declaration, real `readme` exception, typed `reference` rejection under `exempt`, and canonical acceptance of `reference:Source`.
- I-03 full GREEN: `python3 -m unittest tests.validation.test_document_metadata -q` passed 193 of 193 tests in the final 69.155-second rerun after strengthening the typed-profile negative into independent artifact-ID/status subcases.
- I-03 compatibility and integration: explicit-base changed mode selected 10 paths with zero violations, zero legacy exceptions, and zero transition overrides; `python3 -m py_compile`, `git diff --check`, and repository contracts passed with `failures=0`.
- I-03 Graphify: `graphify update .` completed with 23,525 nodes, 25,064 edges, and 1,546 communities. The report remained advisory for the same two unrelated ambiguous cross-root references and generic isolated-node/community noise; claims were corroborated against the tracked metadata registry, migration contract, checker, tests, Stage 00 governance, Spec 131, Plan, and Task. Generated Graphify outputs were restored and excluded from the fix commit.
- Quality-remediation RED: three focused methods produced nine intended defect signals—four missing immutable-snapshot admission findings, four uncaught list/mapping selector `TypeError` errors, and one changed/new CLI bounded-output failure—while the `evidence-preserve` positive remained accepted.
- Quality-remediation focused GREEN: the same three methods passed 3 of 3. Negative archive dispositions `superseded`, `duplicate`, `conflict`, and `withdrawn` receive `archive-snapshot-disposition-forbidden`; `evidence-preserve` does not. List/mapping `archive_disposition` and `preservation_class` values retain their existing invalid-selector findings without exceptions, and the CLI emits no traceback.
- Quality-remediation full GREEN: `python3 -m unittest tests.validation.test_document_metadata -q` passed 196 of 196 tests in 71.660 seconds.
- Quality-remediation compatibility and integration: explicit-base changed mode selected 10 paths with zero violations, zero legacy exceptions, and zero transition overrides; `python3 -m py_compile`, `git diff --check`, and repository contracts passed with `failures=0`.
- Quality-remediation Graphify: `graphify update .` completed with 23,539 nodes, 25,086 edges, and 1,548 communities. The report remained advisory for the same two unrelated ambiguous cross-root references and generic isolated-node/community noise; claims were corroborated against the tracked migration contract, metadata registry, checker, tests, Stage 00 governance, Spec 131, Plan, and Task. Generated Graphify outputs were restored and excluded from the fix commit.
- Closure evidence: final specification and quality reports cover `afc51b29..e9db5afb`; a fresh explicit-base changed-mode check selected 10 paths with zero violations, zero legacy exceptions, and zero transition overrides, and `git diff --check` passed.

T-DCLM-002 actual evidence:

- RED: `python3 -m unittest discover -s tests/validation -p 'test_document_corpus_lifecycle.py' -v` failed with the expected single import error because `check-document-corpus-lifecycle.py` did not exist.
- Focused GREEN: the same discovery command passed 22 of 22 tests in 13.047 seconds. Coverage includes fixed modes and CLI misuse ordering; frozen public data contracts; exact manifest keys, source coverage, ordering, target/disposition rules, baseline commits, destructive review/evidence; advisory/blocking promoted manifests; Git commit/blob/path equality; immutable snapshot path and dual SHA-256 equality; secret/credential/token/private-key/shell-history/raw-log rejection without payload leakage; paired ledger/snapshot write-check equality; duplicate ordering and cross-type exclusion; direct impacted consumers/links; non-mutating review signals; exact 99/100 and 149/150 budgets; and bounded exceptions including omitted-owner handling.
- Metadata compatibility: `python3 -m unittest tests.validation.test_document_metadata -q` passed 196 of 196 tests in 64.891 seconds.
- Static and contract checks: `python3 -m py_compile scripts/validation/check-document-corpus-lifecycle.py scripts/validation/check-document-metadata.py`, `python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-contract`, and `git diff --check` passed.
- Deterministic manifest interfaces: Foundation skeleton generation at baseline `e00e1483` produced exactly 24 pending rows; `check-manifest`, `generate-summary`, and `check-summary` passed against temporary outputs without repository publication.
- Promoted and impacted checks: `check-promoted` reported zero violations. The implementation-agent run of `check-impacted --base-ref e00e1483` selected 126 directly changed or directly related records and reported zero blocking violations; the existing 118-leaf Stage 04 Task directory emitted only its configured advisory warning. The takeover finisher reran the command after the Task/progress evidence edits and selected 127 records with the same zero blocking findings and advisory-only directory warning.
- Advisory full report: `report-full` completed with 2,774 bounded findings and zero parser, contract, Git, path, redaction, or internal safety failures. It returned zero without suppressing debt or consuming an exception file.
- Generated fallout: the security-readiness, audit-matrix, LLM Wiki index, and LLM Wiki coverage owners ran in the prescribed order after staging the new script/test discovery paths. All four produced no Git diff, and their check modes passed at 13 controls, 1,300 Wiki paths, and 1,299 safe coverage paths; therefore the Plan-authorized generated commit is correctly omitted.
- Takeover verification: focused lifecycle tests passed 22 of 22 in 13.636 seconds; metadata compatibility passed 196 of 196 in 71.343 seconds; `py_compile`, lifecycle `check-contract`, `check-promoted`, explicit-base `check-impacted`, `git diff --check`, generated owner check modes, and repository contracts (`failures=0`) passed.
- Review-remediation RED: the 13-method regression class produced 21 expected failures and three expected errors before behavior changes. The failures covered early metadata execution, canonical static ownership, nested exception values, delete/rename impact triggers, manifest baseline/result truth, warning-only `check-full`, safety suppression, redaction gaps, symlink escapes, and Unicode title loss.
- Review-remediation GREEN: the expanded lifecycle suite passed 38 of 38 tests, including table-driven shape, success/write/no-write, ordinary exit, and safety exit matrices for all 16 modes. Canonical metadata compatibility passed 196 of 196 tests in 72.085 seconds. Python compile, `git diff --check`, document traceability (`46/0`), repository contracts (`failures=0`), and the four generated-owner checks passed.
- Review-remediation live checks: `check-contract`, `check-promoted`, `check-impacted --base-ref 9126a0aa`, and `report-full` all returned zero. Impacted validation selected 38 records with zero blocking violations and only the existing 118-leaf Task warning. The full report retained 2,774 bounded findings with zero safety failures.
- Review-remediation generated fallout: security readiness, audit matrix, LLM Wiki index, and LLM Wiki coverage were regenerated in canonical order and produced no Git diff; checks remained fresh at 13 controls, 1,300 paths, and 1,299 safe coverage paths.
- Review-remediation Graphify: `graphify update .` completed at HEAD `43d7d149` with 23,756 nodes, 25,807 edges, and 1,549 communities. Because the graph cannot include uncommitted remediation and still contains broad generic graph communities, it remains advisory; claims were corroborated against the tracked validator, tests, Stage 00, Spec 131, Plan, Task, and Stage 99 owners. Graphify collateral was restored.
- I-08 RED: `python3 -m unittest tests.validation.test_document_corpus_lifecycle.CandidateManifestCliTests -v` ran two real-CLI methods; the safe untracked candidate method failed with exit 3 while the unsafe candidate method passed, reproducing the tracked-file precondition without weakening the existing path-safety boundary.
- I-08 focused GREEN: the same two methods passed in 15.794 seconds. The three explicit modes accepted the canonical untracked Foundation candidate before staging; each mode rejected symlink, traversal, and out-of-root candidates with exit 3 and no output creation.
- I-08 full GREEN and compatibility: the lifecycle suite passed 40 of 40 tests in 40.696 seconds, canonical metadata compatibility passed 196 of 196 tests in 70.251 seconds, and Python compile passed. Promoted-manifest consumers still use the tracked regular-file loader and comparator; only explicit candidate modes use the untracked no-follow path.
- Graphify: `graphify update .` completed against HEAD `9126a0aa` with 23,683 nodes, 25,600 edges, and 1,547 communities. The report remained advisory because generic language/test symbols dominated the god-node list and two Compose/config references were ambiguous. Claims were corroborated against the tracked lifecycle validator and tests, the observability Compose source, Stage 00 governance, Spec 131, Plan, and this Task. `graphify-out/GRAPH_REPORT.md` and `graphify-out/graph.json` were restored to HEAD and excluded from the implementation commit.
- Final-review remediation RED: the independent specification review found I-09 and the separate quality review found I-FQ01 through I-FQ03. Bounded temporary-repository probes demonstrated that a nonexistent partition Plan suppressed the 150-leaf block, a tracked Markdown symlink exposed outside bytes, and a valid source-profile-to-archive-profile transition could not satisfy result attestation.
- Final-review remediation focused GREEN: `python3 -m unittest tests.validation.test_document_corpus_lifecycle.FinalReviewRemediationTests -v` passed 4 of 4 tests in the takeover finisher's 8.624-second rerun. Coverage includes final and intermediate Markdown symlink rejection across every corpus-reading mode without payload or output mutation, positive and negative canonical archive transitions, missing/untracked/symlink/wrong-profile/draft/unreviewed partition Plans, a valid tracked canonical Plan, and immediate eligible-leaf counting exclusions.
- Final-review remediation full GREEN and compatibility: `python3 -m unittest tests.validation.test_document_corpus_lifecycle -q` passed 44 of 44 tests in 52.746 seconds. The prior final-remediation compatibility run passed canonical metadata 196 of 196. `python3 -m py_compile`, `git diff --check`, document traceability, generated-owner freshness, and the four canonical owner checks passed.
- Final-review remediation live checks: `check-contract` and `check-promoted` returned zero; `check-impacted --base-ref 9126a0aa` selected 38 records with zero blocking violations and only the existing 118-leaf Task warning. A direct repository-backed probe of `docs/04.execution/plans/2026-07-14-document-corpus-lifecycle-migration-foundation.md` returned zero partition-approval findings. The advisory full report retained 2,774 bounded findings and zero safety failures.
- Final-review remediation repository integration: after the evidence edits, explicit-base metadata validation selected 2 paths with zero violations, legacy exceptions, or transition overrides; document traceability passed at 46 catalog pairs and zero failures; and `bash scripts/validation/check-repo-contracts.sh` completed with `failures=0`. Graphify output remained restored and untracked by this change; its stale advisory report was not treated as authoritative, and claims were corroborated against the tracked companion/tests, Stage 00 governance, Spec 131, the active Foundation Plan, and this Task.
- Closure-review RED: seven focused methods produced 17 intended assertion failures and zero runtime errors. The failures reproduced safe untracked omission, diagnostic payload emission, missing archive baseline-blob binding, unconditional archive replacement, unresolved canonical replacement, incomplete Plan authorization, and Markdown table injection.
- Closure-review focused GREEN: all seven focused methods passed. Real CLI fixtures cover valid/invalid untracked records, unsafe final/intermediate untracked symlinks with no outside marker, pre-stage 149/150 boundaries, prohibited diagnostic classes across full/impacted/archive/generated modes, and ordinary unresolved IDs without value emission. Git fixtures cover same/different baseline blobs, git-history and immutable-snapshot preservation, every archive disposition replacement variant, missing/untracked/symlink/wrong-profile/wrong-status/wrong-body/self/target/duplicate replacement cases, and path/unique-ID resolution behavior. Plan fixtures cover scalar optional fields, unresolved/self/wrong-type parents, key order, placeholders, required/forbidden headings, and a canonical positive.
- Closure-review full GREEN and compatibility: lifecycle tests passed 50 of 50 in 104.326 seconds; canonical metadata tests passed 197 of 197 in 79.336 seconds. Python compilation and `git diff --check` passed.
- Closure-review live checks: `check-contract` and `check-promoted` returned zero; `check-impacted --base-ref 9126a0aa` selected 38 records with zero blocking violations and the existing Task-directory warning only; `report-full` returned zero with 2,774 bounded generic findings and zero safety failures.
- Closure-review integration: security-readiness, audit-matrix, LLM Wiki index, and LLM Wiki coverage check modes were fresh. `bash scripts/validation/check-repo-contracts.sh` returned `failures=0`. Graphify refreshed at committed contract HEAD `cb84d6c4` to 23,882 nodes, 26,131 edges, and 1,558 communities; two unrelated Compose/config edges remained ambiguous, so the graph was advisory and corroborated against tracked Stage 00/03/04/99 owners and executable sources before generated outputs were restored.
- Final-acceptance RED: five focused methods produced 25 intended assertion failures and zero runtime errors. The failures reproduced real CLI rejection of unstaged deletion and rename, token-shaped `_CorpusSafetyError` path disclosure across ten corpus-reading modes, missing/mismatched/untracked/invalid merge and delete replacements, and suppressed archive parent/supersession graph errors. The multi-row canonical positive already passed and remained a preservation oracle.
- Final-acceptance focused GREEN: `python3 -m unittest tests.validation.test_document_corpus_lifecycle.AcceptanceFindingRemediationTests -v` passed 5 of 5 in 11.869 seconds after adding explicit merge symlink and invalid-profile coverage. Real subprocess fixtures prove deletion selects the surviving link dependent, rename selects the new record plus its dependent, every corpus mode exits 3 without emitting the token-shaped filename or mutating output, valid merge path/ID and delete replacement path pass, and invalid replacements fail closed.
- Final-acceptance full GREEN and compatibility: lifecycle discovery passed 55 of 55 tests in 113.212 seconds; canonical metadata passed 197 of 197 in 74.224 seconds. Python compilation, `git diff --check`, and cached diff hygiene passed.
- Final-acceptance live and integration checks: `check-contract` and `check-promoted` returned zero; `check-impacted --base-ref 9126a0aa` selected 38 records with zero blocking violations and the existing Task-directory warning only; `report-full` retained 2,774 bounded findings with zero safety failures. Security-readiness, audit-matrix, LLM Wiki index, and LLM Wiki coverage were fresh, and repository contracts returned `failures=0`.
- Final-acceptance Graphify: `graphify update .` completed with 23,924 nodes, 26,246 edges, and 1,560 communities. Health remained advisory only for two unrelated cross-root inferred edges; claims were corroborated against the tracked lifecycle companion/tests, Stage 00 governance, Spec 131, this Plan/Task, and Stage 99 owners before `graphify-out/GRAPH_REPORT.md` and `graphify-out/graph.json` were restored.
- Release-gate RED/GREEN: seven focused methods initially produced 22 expected failures and zero errors across the distinct-ID merge positive, sixteen writer/checker symlink cases, three non-regular checker cases, atomic final swap, and interrupted write. After remediation, the focused set passed 7/7; the complete acceptance class passed 12/12 after retaining the prior same-ID consolidation positive.
- Release-gate full compatibility: `python3 -m unittest tests.validation.test_document_corpus_lifecycle tests.validation.test_document_metadata` passed 258/258 before the additional same-ID preservation regression; the final lifecycle rerun passed 62/62 and the unchanged metadata suite remained 197/197. Python compile and `git diff --check` passed.
- Release-gate live and generated checks: `check-contract` and `check-promoted` returned zero; `check-impacted --base-ref 9126a0aa` selected 38 with zero blocking violations and the existing Task-directory warning; `report-full` retained 2,774 advisory findings and zero safety failures. Security readiness, audit matrix, LLM Wiki index, and LLM Wiki coverage regenerated without diff and passed check mode at 13 controls, 1,300 paths, and 1,299 safe paths. Repository contracts returned `failures=0`.
- Release-gate Graphify: `graphify update .` completed with 23,968 nodes, 26,344 edges, and 1,561 communities. The report remained advisory because it was commit-bound to `4e8afaf8` while the fix was initially uncommitted and retained one unrelated ambiguous Compose edge. Claims were corroborated against the held-path implementation/tests, Stage 00 governance, Spec 131, the active Plan/Task, and Stage 99 contracts before both generated Graphify files were restored.
- Sign-off RED/GREEN: five focused real-Git methods initially produced four expected failures: both path and artifact-ID forms accepted a parseable `120000` baseline owner, and both forms rejected an exact same-path `active` to `completed` owner transition with a separately attested peer. The regular/non-regular characterization and already-failing invalid-peer cases remained preservation oracles. After remediation, the expanded focused set passed 8/8 in 8.642 seconds, including prior moved-owner, same-ID new-target, and ordinary canonical replacement positives.
- Sign-off full compatibility: `python3 -m unittest tests.validation.test_document_corpus_lifecycle tests.validation.test_document_metadata -q` passed 267/267 in 201.795 seconds. Python compilation, working-tree and cached diff hygiene passed.
- Sign-off live and generated checks: `check-contract` and `check-promoted` returned zero; `check-impacted --base-ref 9126a0aa` selected 38 with zero blocking violations and the existing Task-directory advisory; `report-full` retained 2,774 advisory findings and zero safety failures. Security readiness, audit matrix, LLM Wiki index, and LLM Wiki coverage check modes were fresh, and repository contracts returned `failures=0`.
- Sign-off Graphify: `graphify update .` completed at `1c9ef624` with 24,033 nodes, 26,464 edges, and 1,563 communities. The report remained advisory for one unrelated cAdvisor/Pyroscope inferred Compose relationship and generic thin communities. Tracked observability Compose proves those services are independent siblings, and lifecycle claims were corroborated against the tracked validator/tests, Stage 00 governance, Spec 131, this Plan/Task, and Stage 99 before both graph outputs were restored.
- Safety boundary: Git commands use argument arrays and verify commit/blob types before comparison. Library functions return stable findings and never print payload bytes. Snapshot fixtures proved rejection of prohibited confidentiality classes while finding paths/messages remained value-free.
- Scope preservation: no broad corpus leaf, existing tombstone, archive evidence payload, Stage 04 partition, exception file, workflow, runtime, Compose, infrastructure, deployment, secret, credential, provider instruction, or remote state changed.
- Closure bookkeeping verification: explicit-base metadata validation against `9fe234f6` selected the two changed tracked evidence documents with zero violations, zero legacy exceptions, and zero transition overrides; `git diff --check` passed. No implementation, contract, or test file changed during closure.

Verification results: T-DCLM-001 and T-DCLM-002 are complete. The T-DCLM-002
implementation range `9126a0aa..9fe234f6` is GREEN and received terminal Spec
PASS and separate Quality retry PASS, each with Critical 0, Important 0, and
Minor 1. The only deferred Minor is behavior-preserving decomposition of the
monolithic dispatcher; T-DCLM-003 is unblocked.

## Controlled Agent Pre-commit Evidence

Controlled wrapper command:

scripts/validation/run-agent-precommit-all-files.sh with this tracked Task and
the explicit allow-prefix set in the Plan.

Allowed prefixes:

- .github/workflows/document-corpus-lifecycle.yml
- .pre-commit-config.yaml
- docs/00.agent-governance/rules
- docs/00.agent-governance/memory/progress.md
- docs/03.specs/131-document-corpus-lifecycle-migration-foundation
- docs/03.specs/README.md
- docs/04.execution
- docs/90.references/data/governance/document-corpus-lifecycle
- docs/90.references/data/governance/audit-implementation-matrix.md
- docs/90.references/data/security/security-automation-readiness.md
- docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md
- docs/90.references/llm-wiki/llm-wiki-index.md
- docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md
- docs/98.archive/README.md
- docs/99.templates/support
- docs/99.templates/templates/common
- scripts/README.md
- scripts/validation/check-document-corpus-lifecycle.py
- scripts/validation/check-document-metadata.py
- scripts/validation/check-repo-contracts.sh
- scripts/validation/recommend-qa-gates.sh
- scripts/validation/run-local-qa-gates.sh
- tests/validation/test_document_metadata.py
- tests/validation/test_document_corpus_lifecycle.py

Exit status: not run.

Snapshot result: not run.

Observation boundary: Git-visible path sets and safe hook summaries only.

Path sets: not run.

Disposition: not run.

## Review Evidence

Implementation review verdict: T-DCLM-001 self-review PASS after remediation. The implementation is bounded to machine contracts, static manifest/exception and archive-frontmatter validation, tests, Task evidence, and the mandatory progress log. It adds no Git-object probe, snapshot-byte access, corpus migration, existing tombstone edit, exception file, runtime mutation, secret handling, or remote action. Stable diagnostics contain only keys, codes, safe paths, counts, dates, and shape requirements.

Specification review verdict: the first T-DCLM-001 review returned FAIL with Critical 0 and Important 2; I-01 and I-02 were resolved in `ab33b64f`. The re-review returned FAIL with Critical 0 and Important 1; I-03 was resolved in `602994f2`. The final specification review of `afc51b29..e9db5afb` returned PASS with Critical 0 and Important 0.

Quality review verdict: the first T-DCLM-001 quality review of `afc51b29..602994f2` returned FAIL with Critical 0, Important 2, and Minor 0. I-Q01 identified missing immutable-snapshot disposition admission; I-Q02 identified uncaught non-scalar archive-selector `TypeError` escapes. Both were resolved in `e9db5afb`; the final quality review of `afc51b29..e9db5afb` returned PASS with Critical 0, Important 0, and Minor 0.

T-DCLM-002 implementer self-review verdict: PASS. The public names, signatures, nullability, mode tuple, argument surface, and exit classes match the approved Plan. Invalid CLI shapes return 2 before opening repository files; parser/contract/Git/path/redaction/internal safety failures return 3; ordinary blocking findings return 1; advisory reports return 0. Manifest, summary, archive-ledger, and snapshot-manifest checks compare canonical bytes without mutation. The implementation imports the canonical metadata parser, `Record`, `Finding`, safe-path logic, and artifact-ID manifest builder without renaming or repurposing metadata `Manifest`.

T-DCLM-002 first independent review verdicts: specification FAIL with Critical
0 and Important 7; quality FAIL with Critical 0, Important 5, and Minor 2.
Review-remediation regressions and implementation closed I-01 through I-07,
I-Q01 through I-Q05, M-Q01, and M-Q02. Later complete-range reviews verified
the remediated boundaries.

T-DCLM-002 first fresh specification re-review verdict: FAIL with Critical 0,
Important 1, and Minor 0 over `9126a0aa..82cbb9c0`. I-01 through I-07 were
confirmed closed. I-08 identified the explicit candidate modes' staged-file
precondition; the focused RED/GREEN remediation above separated untracked
candidate validation from tracked promoted-manifest consumption.

T-DCLM-002 final pre-remediation review verdicts over
`9126a0aa..ee4b6846`: specification FAIL with Critical 0, Important 1, and
Minor 1; quality FAIL with Critical 0, Important 3, and Minor 2. Specification
I-09 and quality I-FQ03 identified the same unproved partition-Plan
authorization. Quality I-FQ01 identified corpus Markdown symlink following and
value leakage; I-FQ02 identified the unrepresentable
source-profile-to-archive-profile transition. Commit `eb52185c` added focused
regressions and remediated every Important finding. The stale ignored report
finding was corrected in the implementation handoff.

T-DCLM-002 closure review verdicts over `9126a0aa..554253e6`:
specification FAIL with Critical 0, Important 3, and Minor 0; quality FAIL with
Critical 0, Important 5, and Minor 2. Contract commit `cb84d6c4` deferred
archive replacement truth to the validated target disposition. Lifecycle
commit `2c1b0c46` closed I-09-R1/I-10/I-11, I-CQ01 through I-CQ05, and M-CQ02
with the focused and full evidence above. M-CQ01 was retained as a
non-blocking later orchestration-refactor opportunity.

T-DCLM-002 final acceptance reviews over `9126a0aa..8a7c9c7c`:
specification FAIL with Critical 0, Important 1, and Minor 1; quality FAIL with
Critical 0, Important 4, and Minor 1. Commit `9bea953b` closed specification
I-12 and quality I-AQ01 through I-AQ04 with real CLI deletion/rename handling,
mandatory final safety-path sanitization, disposition-aware canonical
replacement binding for merge/delete, and full held result-manifest relation
validation for archive.

T-DCLM-002 release-gate reviews over `9126a0aa..4e8afaf8`:
specification FAIL with Critical 0, Important 1, and Minor 1 for I-13; quality
FAIL with Critical 0, Important 1, and Minor 1 for I-RQ01. Commit `6c33c66c`
closed both Important findings with distinct source/owner merge attestation and
one no-follow atomic output boundary.

T-DCLM-002 sign-off reviews over `9126a0aa..7ff6a841`: specification FAIL with
Critical 0, Important 1, and Minor 1 for I-FRQ01-R1; quality FAIL with Critical
0, Important 2, and Minor 1 for I-SQ01/I-SQ02. Commit `1c9ef624` closed the
non-regular baseline-owner and exact same-path lifecycle-attestation gaps
without changing public interfaces or the preserved merge/output matrix.

T-DCLM-002 terminal reviews over `9126a0aa..9fe234f6`: specification PASS with
Critical 0, Important 0, and Minor 1; separate quality retry PASS with Critical
0, Important 0, and Minor 1. All earlier Critical and Important findings are
closed. Both reviewers retained only the same deferred Minor: split the
monolithic dispatcher in a later behavior-preserving package with
characterization/equivalence tests. This does not block Task 3.

Review findings and disposition: I-01 and I-02 resolved in `ab33b64f`; I-03 resolved in `602994f2`; I-Q01 and I-Q02 resolved in `e9db5afb`. Final specification and quality reviews are clean, T-DCLM-001 is closed, and T-DCLM-002 is unblocked.

## Commit Ledger

Planning baseline:

- 15fdac5d — docs(spec): define corpus lifecycle migration foundation
- 313c36ed — docs(generated): refresh corpus design indexes
- c6b3d9bc — docs(spec): clarify canonical stage routing

Foundation logical commits:

- `d40540a0` — T-DCLM-001 `feat(docs): define corpus lifecycle machine contracts`.
- `a224f93d` — T-DCLM-001 generated follow-up `docs(generated): index lifecycle machine contract`.
- `ab33b64f` — T-DCLM-001 specification-review remediation `fix(docs): enforce corpus lifecycle machine contracts`.
- `602994f2` — T-DCLM-001 specification re-review remediation `fix(docs): honor metadata profile identity rules`.
- `e9db5afb` — T-DCLM-001 quality-review remediation `fix(docs): harden archive snapshot validation`.
- `43d7d149` — T-DCLM-002 `feat(validation): add document corpus lifecycle checks`.
- `82cbb9c0` — T-DCLM-002 first-review remediation `fix(validation): harden document corpus lifecycle checks`.
- `ee4b6846` — T-DCLM-002 I-08 remediation `fix(validation): allow pre-stage lifecycle candidates`.
- `eb52185c` — T-DCLM-002 final-review remediation `fix(validation): close lifecycle safety boundaries`.
- `cb84d6c4` — T-DCLM-002 closure contract remediation `fix(docs): defer archive replacement truth`.
- `2c1b0c46` — T-DCLM-002 closure implementation remediation `fix(validation): close lifecycle corpus review blockers`.
- `9bea953b` — T-DCLM-002 final acceptance remediation `fix(validation): close lifecycle acceptance boundaries`.
- `6c33c66c` — T-DCLM-002 release-gate remediation `fix(validation): close lifecycle release blockers`.
- `8001a95c` — T-DCLM-002 final release-quality remediation `fix(validation): bind merge owners to baseline provenance`.
- `1c9ef624` — T-DCLM-002 sign-off remediation `fix(validation): close lifecycle sign-off gaps`.

The reviewed T-DCLM-002 implementation and remediation range ends at
`9fe234f6`. The later ledger-only closure commit records the terminal verdicts
and does not alter the reviewed implementation, contracts, or tests.

Commit validation: each entry must name its work unit, review verdicts, focused
GREEN commands, and generated fallout before closure.

## Deferred and Blocked Items

Deferred:

- T-DCLM-003 must update `docs/99.templates/templates/common/archive.template.md` with the four v2 archive source keys and remove the exact-path transitional source exemption. Regression coverage proves the exemption does not relax new/changed archive targets.
- Spec 132 — active SDLC graph migration;
- Spec 133 — operations document migration;
- Spec 134 — completed/superseded evidence and Stage 04 year partition;
- Spec 135 — existing tombstone provenance and approved snapshots;
- Spec 136 — Stage 90, README, generated, _workspace, .github, and final
  full-corpus enforcement.

Blocked items: none at planning time.

Deferral destination: the named later-wave Specs and their separately approved
Plans/Tasks.

## Related Documents

- [Foundation Spec](../../03.specs/131-document-corpus-lifecycle-migration-foundation/spec.md)
- [Foundation Plan](../plans/2026-07-14-document-corpus-lifecycle-migration-foundation.md)
- [Stage 04 Tasks](./README.md)
- [Canonical implementation audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Metadata registry](../../99.templates/support/document-metadata-profiles.yaml)
- [Controlled all-files wrapper](../../../scripts/validation/run-agent-precommit-all-files.sh)
