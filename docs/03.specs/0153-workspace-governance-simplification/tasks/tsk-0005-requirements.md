---
profile_id: task
status: completed
artifact_id: task-0153-0005
artifact_type: task
parent_ids:
  - SPEC-0153
  - plan-0153
created: 2026-08-21
updated: 2026-08-22
---

# Task 0005: Requirements

## Objective

Unify Stage 01 into prefixless Requirement Packages with package-qualified FR, NFR, and IF identities.

## Inputs

- [Specification](../spec.md)
- [Implementation Plan](../plan.md)
- [Migration 0003](../../../98.archive/migrations/mig-0003-workspace-governance-simplification.md)
- Task 4 governance convergence, Stage 99 requirements profile, approved Migration owner_task 5 rows.

## Work Log

| Event | Actual result |
| :--- | :--- |
| Boundary freeze | Migration rows `mig-0003-r0132` through `mig-0003-r0156` resolve to exactly 25 tracked sources, 25 absent targets before execution, 74 declared edges across 72 unique declared consumers, and 78 live current consumers. The union is 79 because `docs/00.agent-governance/providers/codex.md` was already converged while predecessor Spec 0136 and five focused tests exposed additional live references. |
| RED | `PYTHONPATH=. python3 -m unittest tests.validation.test_requirement_packages tests.validation.test_four_digit_document_identity -v` ran 29 tests with 8 failures: 7 exact Task 5 assertions failed because `requirements.py` did not exist; the eighth was the pre-existing Stage 00 incident-route publication residual. |
| Conversion preview | A deterministic `/tmp` preview reviewed all 25 package mappings, 152 requirement mappings, and 82 acceptance mappings. SHA-256: `c234c49062970553ed424a0400962fc67976e1de16b8c04a76d7bf181d53deab`. No ambiguous owner, kind, or acceptance mapping existed; the helper and output were removed after review. |
| Native moves | Executed exactly one literal native `git mv` for each approved row `r0132`–`r0156`. All 25 prefixless targets exist and all 25 legacy sources are absent. The reviewed 113-path initial packet and 12-path fix set were combined into the logical Task 5 commit. |
| Package rewrite | Preserved the problem, goals, stakeholders, constraints, acceptance meaning, risks, dependencies, and trace links in every package. Current declarations are 152 unique child IDs: 138 FR and 14 NFR; no source declared a distinct solution-independent interface requirement, so no IF ID was invented. The 82 acceptance entries reference their corresponding full FR IDs. |
| Allocation and consumers | Advanced only issued NFR high-water state: `REQ-0003.NFR=7/8`, `REQ-0024.NFR=13/14`, and `REQ-0025.NFR=16/17`; no FR or IF high-water was lowered. Rewrote 78 live current consumer/template paths and identities while preserving the frozen Migration packet, its selection/edge digests, recovery fields, and archived evidence. |
| Validation implementation | Added frozen bounded parsing for regular non-symlink UTF-8 files, exact path/package ownership, required registered sections, typed/monotonic child declarations, item/byte limits, and fail-closed legacy, bare, malformed, duplicate, reused, wrong-kind, foreign-owner, and executable OpenAPI/GraphQL/Proto rejection. Metadata validation consumes the canonical parser and exposes only a read-only legacy relation alias for immutable pre-migration evidence. |
| Fix round 1 RED | The stale taxonomy test first failed `25 != 0`. New focused mutations then failed because Registry child spaces exposed no `current_issued`; FR-9999 and reserved `REQ-0001-IF-0001` were accepted; seven embedded OpenAPI 2/3 JSON/YAML/indented, non-Query GraphQL, and proto2/3 payloads were accepted; a current Architecture consumer resolved `prd-0001`; Spec 0136 exposed undeclared NFR/IF IDs and no acceptance-to-FR statement; and valid-prefix short-read plus concurrent-growth mutations were accepted. |
| Fix round 1 implementation | Added 75 package/kind `current_issued` sets covering 152 current declarations and preserving 83 issued-history reservations; allocation advance now requires coherent high-water, next-number, and current-issued state. Embedded executable-family detection, stable verified-EOF reads, archive-only legacy Requirement relations, and the bounded Spec 0136 dangling-ID/acceptance correction now fail closed. The canonical taxonomy test requires exactly 25 prefixless `requirements-package` records. |
| Fix round 2 RED | The public parser accepted a package missing one current declaration. A paired package and Registry mutation reintroduced reserved `REQ-0003-FR-0005`. Six additional OpenAPI, GraphQL, and implicit Proto variants were accepted. A retired interface identity in Stage 01 and retired path/ID injections in the changed Spec 0136 consumers were also accepted. |
| Fix round 2 implementation | Added an explicit terminal `reserved_history` partition to all 75 child spaces. Registry invariants require current and reserved sets to be sorted, disjoint, bounded, and a complete classification through high-water; the public parser requires exact document-to-`current_issued` agreement. Bounded JSON token decoding, YAML comment handling, directive/extension-aware GraphQL recognition, implicit Proto2 recognition, and shared retired-reference detection close the remaining parser and Spec-consumer variants. |
| Fix round 3 RED | A coherent candidate removed `REQ-0003.FR` number 5 from `reserved_history`, added it to `current_issued` and the package, and passed snapshot-only validation. The Registry transition API and trusted-baseline requirement were absent. Flow-style OpenAPI YAML, a directive-bearing GraphQL extension with its brace on the next line, and a one-line implicit Proto2 message/service/RPC payload were accepted; three prose controls remained accepted. |
| Fix round 3 implementation | Added an explicit append-only allocation transition validator. Its trusted predecessor is derived deterministically from the staged Registry high-water state plus the 25 staged Requirement Package declarations, or from an explicitly selected commit. Prior reservations must remain reserved; prior current IDs may remain current or retire; new current IDs must be the contiguous advance strictly above prior high-water. Registry validation, public parsing, and Stage loading require the trusted baseline whenever allocation-transition mode is enabled. Bounded flow-YAML, next-line GraphQL, and one-line Proto token recognition closes the payload variants without rejecting the prose controls. |
| Fix round 4 RED | Thirteen exact negative subcases failed and two bounded-runner subcases errored before their production edits: a root Requirement high-water regression passed Registry transition validation, public parsing, and Stage loading, and an advanced root omitted its new package; changed/contracts CLI modes accepted a paired reserved-ID reclassification; five quoted/anchored/multiline OpenAPI, GraphQL, and imported-type Proto payloads passed; moving-ref and moving-index reads were not snapshotted; and no pre-buffer stdout/stderr cap existed. The pinned-commit and expanded prose controls remained positive. |
| Fix round 4 implementation | Root package high-water is now append-only and every child-space package is bounded by it. Metadata changed/contracts gates validate both Registry and the complete Stage 01 corpus in transition mode. Git refs resolve once to commit OIDs; explicitly requested index snapshots capture path-to-blob mappings once; all later reads use immutable blob OIDs through an argv-only, timeout-bound, streaming stdout/stderr cap with package/path/high-water bounds. Bounded syntax grammars cover quoted, multiline, tagged, and anchored OpenAPI flow values, multiline GraphQL declarations/directives/extensions, and Proto services using imported request/response types. |
| Fix round 5 RED | Seven exact failures remained: a candidate `high_water=10000` expanded 9,975 missing-space findings; changed/contracts modes trusted a staged reserved-ID reclassification whenever the worktree Registry differed harmlessly; and folded/literal block-scalar OpenAPI, comment-separated GraphQL with balanced nested directive input, and Proto aggregate service options before RPC were accepted. Prose controls remained positive. |
| Fix round 5 implementation | Schema and runtime now cap identity values, arrays, child mappings, trusted paths, and package counts at 9,999 before range/set/finding expansion. Production metadata gates always compare against the pinned explicit merge-base, or pinned `HEAD` as the no-ref safe default; the Git index is available only through an explicit internal `":"` revision. Legacy predecessor packages are deterministically translated from their section/subsection declarations without consulting candidate allocation fields. Bounded comment stripping, tokenization, and balanced delimiter scanning close the remaining OpenAPI, GraphQL, and Proto variants. |
| Final approval and closeout | Independent contract and Python/security reviewers approved the final packet at `C0/I0/M0`. The controller reran 69 focused tests, changed metadata, repository contracts, syntax, and diff checks, then created logical commit `218d66934828da41fce9a9a14cb35d3d7e94bd04` (`refactor(requirements): unify requirement packages`). |

## Verification Evidence

| Check | Command | Result |
| :--- | :--- | :--- |
| Requirement package GREEN | `rtk python3 -m unittest tests.validation.test_requirement_packages -v` | PASS: `20/20`; exactly 25 packages load with `REQ-0001`–`REQ-0025`; root and child allocation transitions, exact allocation state, permanent reservations, coherent new allocation, syntax-aware payload variants/prose controls, retired consumers, and stable-read mutations fail closed. |
| Changed metadata | `rtk python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD` | PASS: `selected=100 violations=0 legacy_exceptions=0 transition_overrides=0`. |
| Repository contracts | `python3 scripts/validation/check-document-metadata.py --profiles docs/99.templates/registry.json --mode check-contracts --base-ref HEAD` | PASS: `metadata repository contracts: violations=0`. |
| Focused metadata regressions | `rtk python3 -m unittest tests.validation.test_document_metadata.Task5ChangedMetadataRegressionTests -v` | PASS: `18/18`, including historical-positive/current-negative legacy Requirement relations and both actual changed/contracts CLI rejection variants for paired reserved-ID reclassification, including mixed staged/worktree state. |
| Taxonomy | `rtk python3 -m unittest tests.validation.test_document_taxonomy -q` | `12/14`; the canonical Stage 01 assertion passes. The exact residuals are 26 ADRs where the predecessor test expects 25 and two intentional legacy Stage 02 rejection examples in the current Spec 0153 package. This Task no longer republishes that forbidden route literal. |
| Four-digit identity | `PYTHONPATH=. python3 -m unittest tests.validation.test_four_digit_document_identity -v` | `21/22`; sole residual is the pre-existing Stage 00 incident-route assertion for `documentation-protocol.md` and `stage-authoring-matrix.md`, reproduced during RED and outside Task 5. |
| Active legacy package path/ID scans | Bounded `rg` scans of live consumers, excluding the current Spec 0153 Plan's explicit RED fixtures and this Task's quoted RED/evidence literals | PASS: zero retired Requirement paths/IDs, bare child IDs, or live relation aliases. The stricter Spec 0136 consumer scan and its eight retired-reference injections are green. |
| Registry contract | `rtk python3 -m unittest tests.validation.test_document_registry -q` | PASS: `31/31`, including bounded allocation expansion, root regression, coherent reservation reclassification, missing trusted baseline, pinned/moving ref, explicit moving-index snapshot, and pre-buffer stdout/stderr bound coverage. |
| Frozen Migration contract | `rtk python3 -m unittest tests.validation.test_workspace_governance_migration -q`; SHA-256 | Digest/selection checks pass; suite is `8/17` with nine Task 3/4 and current uncommitted Task-evidence state assertions. Migration bytes remain SHA-256 `271f21c50cf4ab765422ee552de244a4340c160e53149231eb6be45f03476ab9`; no YAML row, digest, or recovery commit changed. |
| Traceability links | `python3 scripts/validation/check-document-links.py --mode traceability` | One shared-worktree residual only: `document-not-regular` for Task 1-moved `docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`; `documents=362 links=2747 failures=1`. |
| Python quality | Ruff and `python3 -m py_compile` over the three implementation modules and four focused test files | PASS. |
| Git hygiene | reviewed packet hashes; `git diff --check`; controller commit | Initial 113-path staged binary diff SHA-256 was `1e3377c538ee9faa06174a709cb84fa12bc7bc7795c280b45525e186236da781`; the frozen initial review packet SHA-256 was `b7167ab66c05ae7f443c9723fff757c12f3f652ed6a9976de3ea612fc9835010`. The combined reviewed implementation passed cached and working-tree diff checks and was committed as `218d66934828da41fce9a9a14cb35d3d7e94bd04`. No push, remote, runtime, credential, or secret operation occurred. |

## Review Evidence

| Review | Status | Findings and disposition |
| :--- | :--- | :--- |
| Final independent reviews | APPROVED (`C0/I0/M0`) | Contract and Python/security reviewers independently verified bounded allocation expansion, mixed staged/worktree predecessor isolation, executable-contract detection, evidence accuracy, frozen Migration bytes, and controller gate results. |

## Commit Ledger

| Commit | Description |
| :--- | :--- |
| `218d66934828da41fce9a9a14cb35d3d7e94bd04` | `refactor(requirements): unify requirement packages`; parent-owned logical Task 5 implementation commit. Migration recovery commits remain intentionally unbound until Task 13. |

## Rulings

- Requirement sources contained no separately declared solution-independent interface requirements; explicit empty Interface Requirements sections preserve that fact without inventing IF identities.
- Legacy `prd-####` relation resolution is read-only compatibility for immutable archive evidence; it is not an allocation namespace and cannot create or reuse an ID.
- `current_issued` is the bounded present-state set. Numbers at or below high-water but absent from that set remain reserved history and cannot be reintroduced; a new declaration requires an atomic Registry allocation advance.
- `reserved_history` is terminal allocation history. It is disjoint from `current_issued`, and together the two sets must classify every issued number through high-water; no transition moves a terminal reservation back to current state.
- Snapshot partition validity is necessary but not sufficient for an allocation change. Production transition mode requires a pinned commit predecessor and fails closed without it; index comparison is an explicit internal-only snapshot option.
- A trusted non-index ref is resolved once to a commit OID. An explicitly requested internal index predecessor is one captured path-to-blob snapshot; moving refs or later index writes cannot change the bytes used by an in-flight validation.

## Deferred Items

- Task 13 recovery binding remains parent-owned.
