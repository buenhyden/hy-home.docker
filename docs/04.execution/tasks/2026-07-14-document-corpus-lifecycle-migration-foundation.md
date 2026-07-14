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
| T-DCLM-001 | Machine migration contract and static archive metadata | Implementation and specification review complete; quality remediation awaiting re-review |
| T-DCLM-002 | Lifecycle companion, Git provenance, deterministic data | Not run |
| T-DCLM-003 | Human contracts, archive template, Stage 98/00 routing | Not run |
| T-DCLM-004 | Repository contracts, local QA, tracked workflow | Not run |
| T-DCLM-005 | Foundation manifest and generated evidence | Not run |
| T-DCLM-006 | Full QA, wrapper, whole-branch review, closure | Not run |

## Work Log

| Date | Work unit | Agent role | Result |
| --- | --- | --- | --- |
| 2026-07-14 | Planning | Controller | Spec 131 approved and activated; Plan and Task evidence shell authored. |
| 2026-07-14 | T-DCLM-001 | Fresh implementation agent | Added the exact migration registry, metadata registry v2, fail-closed static archive validation, and RED/GREEN coverage. The authored scope is the Task 1 file set plus `docs/00.agent-governance/memory/progress.md`, included as a documented deviation because the root `AGENTS.md` bootstrap makes progress updates mandatory. Self-review passed; specification and quality review remain assigned to fresh reviewers. |
| 2026-07-14 | T-DCLM-001 generated fallout | Fresh implementation agent | The first repository-contract run found only the canonical frontmatter semantic inventory stale after registry v2. The controller approved regenerating that owner in the Task 1 generated follow-up together with any LLM Wiki/index coverage fallout; this is a scoped deviation from the brief's two-file generated follow-up list, not broad corpus mutation. |
| 2026-07-14 | T-DCLM-001 specification-review remediation | Fresh implementation agent | Resolved specification findings I-01 and I-02 by machine-declaring exact manifest types, nullability, domains, deterministic ordering, destructive execution prerequisites, and bounded exception semantics. Added static synthetic validation without Git lookup, snapshot-byte access, or a repository exception file. Fresh specification re-review remains required. |
| 2026-07-14 | T-DCLM-001 specification re-review remediation | Fresh implementation agent | Resolved I-03 by deriving artifact-ID/status nullability from the selected metadata profile and reusing the canonical non-empty artifact-ID value rule. The `readme` profile proves the declared exception path, while `reference` proves `exempt` cannot bypass required identity/status. No Git lookup or snapshot-byte access was added. |
| 2026-07-14 | T-DCLM-001 quality-review remediation | Fresh implementation agent | Resolved I-Q01 and I-Q02 by sharing the contract-owned immutable-snapshot disposition allowlist with static archive validation and scalar-guarding both archive selectors before conditional membership. Added value-free admission findings, list/mapping regressions for both selectors, and a changed/new CLI no-traceback regression. |

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

Verification results: T-DCLM-001 implementation and I-01/I-02/I-03/I-Q01/I-Q02 remediation GREEN. Final specification re-review passed with Critical 0 and Important 0; fresh quality re-review is pending.

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

Specification review verdict: the first T-DCLM-001 review returned FAIL with Critical 0 and Important 2; I-01 and I-02 were resolved in `ab33b64f`. The re-review returned FAIL with Critical 0 and Important 1; I-03 was resolved in `602994f2`. The final specification re-review of `afc51b29..602994f2` returned PASS with Critical 0 and Important 0.

Quality review verdict: the T-DCLM-001 review of `afc51b29..602994f2` returned FAIL with Critical 0, Important 2, and Minor 0. I-Q01 identified missing immutable-snapshot disposition admission; I-Q02 identified uncaught non-scalar archive-selector `TypeError` escapes. Both are implemented and await fresh quality re-review.

Review findings and disposition: I-01 and I-02 resolved in `ab33b64f`; I-03 resolved in `602994f2`; I-Q01 and I-Q02 resolved in the pending `fix(docs): harden archive snapshot validation` logical commit. Fresh quality re-review is required before T-DCLM-002.

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
- T-DCLM-001 quality-review remediation — `fix(docs): harden archive snapshot validation`; identity is assigned by the remediation commit operation and will be appended to the ignored implementation report.

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
