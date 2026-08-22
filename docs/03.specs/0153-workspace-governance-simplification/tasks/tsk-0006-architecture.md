---
profile_id: task
status: completed
artifact_id: task-0153-0006
artifact_type: task
parent_ids:
  - SPEC-0153
  - plan-0153
created: 2026-08-21
updated: 2026-08-22
---

# Task 0006: Architecture

## Objective

Move Architecture Descriptions and ADRs to prefixless paths while preserving AD and ADR stable identities and reciprocal supersession.

## Inputs

- [Specification](../spec.md)
- [Implementation Plan](../plan.md)
- [Migration 0003](../../../98.archive/migrations/mig-0003-workspace-governance-simplification.md)
- Task 5 Requirement Packages, Stage 99 architecture profiles, approved Migration owner_task 6 rows.

## Work Log

| Event | Actual result |
| :--- | :--- |
| Boundary freeze | Migration rows `mig-0003-r0157` through `mig-0003-r0207` resolve to exactly 51 native renames: 25 Architecture Descriptions and 26 ADRs. The Task 5-state preflight found 51 sources, zero targets, 50 tracked-source rows plus the Task 1-created ADR-0029 row, 183 declared edges across 113 unique declared consumers, 138 live active matches, and a 139-path normalized declaration/live union. |
| RED | Before production edits, `rtk python3 -m unittest tests.validation.test_architecture_documents.ArchitectureDocumentTests.test_current_architecture_corpus_is_prefixless_and_uppercase -v` failed its only test with exactly 102 findings: 51 prefixed paths and 51 lowercase stable IDs. The focused negative fixtures also cover lowercase IDs, path-number mismatch, duplicate identity, symlink/non-regular/oversized/non-UTF-8 input, dangling/asymmetric/cyclic supersession, an archived superseded ADR, and restoration of the retired Stage 02 requirement subdirectory. |
| Native moves | Executed exactly one literal `git mv` for every approved row `r0157`–`r0207`. The final inventory has 25 prefixless description targets and 26 prefixless decision targets, zero prefixed sources, and 51 native rename entries. No bulk move or row reinterpretation occurred. |
| Corpus rewrite | Uppercased all 51 stable IDs without renumbering, preserved the 25 `AD-####` and 26 `ADR-####` identities, normalized the registered Stage 99 sections, and rewrote the 139-path declaration/live consumer union. Stage 02 indexes publish the exact inventory and prefixless examples. Frozen Stage 98 evidence remains unchanged; the bounded Stage 99 legacy-profile transition input and explicit negative fixtures remain the only scan exclusions. |
| Supersession | ADR-0029 is `active`, supersedes ADR-0027, and points to its prefixless path. ADR-0027 remains in Stage 02 as `superseded`, reciprocally names ADR-0029, and is neither archived nor deleted. The other 49 architecture documents retain their lifecycle. |
| Validator | Added a 512 KiB-per-document, 256-document bounded parser that accepts only registered regular non-symlink UTF-8 files, returns frozen records, enforces directory-owned type/path/number/uppercase-ID identity, and rejects restoration of the retired Stage 02 requirement subdirectory. Reads now compare device, inode, mode, size, nanosecond modification/change times, and expected bytes after verified EOF. The reciprocal graph validator rejects dangling, asymmetric, cyclic, archived, cross-type, ineffective-successor, and non-superseded-predecessor edges. Metadata and taxonomy validation consume the canonical architecture identity. |
| Fix round 1 | Reproduced the reviewer packet before fixes: the exact architecture/taxonomy command had one retired-route publication failure; the frozen legacy metadata packet had two template-role errors and six relation-test failures; the Task 2 legacy-profile target assertion failed; a deterministic same-inode 70 KiB mixed read was accepted; and rejected/draft/retired successors plus an active predecessor were accepted by the graph. Rephrased Task evidence without publishing the forbidden route, restored frozen legacy fixtures, preserved exact legacy-ID resolution without reopening the canonical alias, and added verified-EOF and lifecycle enforcement. |
| Baseline attribution | The post-fix full metadata suite reran all 258 tests in `161.361s` and now has exactly `20 failures, 1 error`: 19 pre-existing Task 5 temporary-Registry trusted-base subcases plus the pre-existing Task 4 retired-route failure/error. All nine Task 6-owned template/changed-mode/changed-path/Task-2 failures are removed. Link traceability retains one Task 7-planned non-regular Stage 04 residual; alignment retains the shared Task 4/7 route and archive-link baseline. |
| Final approval and closeout | Independent contract and Python/security reviewers approved the fix-round packet at `C0/I0/M0`. The controller reran 28 focused tests, changed metadata, repository contracts, syntax, diff, and Migration preservation checks, then created logical commit `7001e8d984aadccfa942afd765cdcab9db43c84f` (`refactor(architecture): use prefixless document paths`). |

## Verification Evidence

| Check | Command | Result |
| :--- | :--- | :--- |
| Architecture and taxonomy GREEN | `rtk python3 -m unittest tests.validation.test_architecture_documents tests.validation.test_document_taxonomy -v` | PASS: expanded `28/28` in `3.271s`; the original 24 cases remain green and four fix-round cases cover same-inode mutation, ineffective/predecessor lifecycle edges, a valid superseded-successor chain, and negative metadata CLI integration. |
| Frozen-profile regression packet | Exact TemplateRoleInference, four ChangedPathGit, two ChangedModeRollout, and Task2 target-route methods | PASS: `8/8` methods covering all nine formerly failing Task 6 cases in `11.542s`. Frozen legacy paths/IDs remain fixtures; the canonical current assertions explicitly use Registry profiles. Exact legacy IDs resolve inside the legacy envelope while the canonical Requirement alias remains archive-only. |
| Full metadata | `rtk python3 -m unittest tests.validation.test_document_metadata -v` | Baseline: `258` tests in `161.361s`, `20 failures, 1 error`; only the attributed Task 5 trusted-base and Task 4 publication residuals remain. |
| Changed metadata | `rtk python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD` | PASS: `selected=127 violations=0 legacy_exceptions=1 transition_overrides=0`; the sole exception is the unchanged two-deficit Task 8 baseline in `docs/99.templates/README.md` (`new_deficits=0`). |
| Repository contracts | `rtk python3 scripts/validation/check-document-metadata.py --mode check-contracts --base-ref HEAD` | PASS: `metadata repository contracts: violations=0`. |
| Four-digit identity | `rtk python3 -m unittest tests.validation.test_four_digit_document_identity -v` | `21/22`; both current Stage 02 path/frontmatter assertions pass. The sole residual is the pre-existing Task 4 incident-route publication assertion for `documentation-protocol.md` and `stage-authoring-matrix.md`. |
| Active old-path/lowercase-ID scan | Bounded PCRE2 `rg` scan over active docs, infra, scripts, tests, and root entry documents | PASS: zero matches after excluding only Stage 98 evidence, `document-metadata-profiles.yaml` and its explicit metadata test fixtures as the bounded legacy transition envelope, the frozen Migration validator, and the architecture validator's explicit negative fixture. A direct scan of this Task evidence also finds no forbidden Stage 02 requirement-route literal. |
| Traceability links | `rtk python3 scripts/validation/check-document-links.py --mode traceability` | Baseline: `documents=362 links=2749 catalog_pairs_total=46 archive_direct_links_total=15 removed_template_mentions_total=0 failures=1`; sole failure is the Task 7-planned non-regular `docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`. No Task 6 old-path failure remains. |
| Alignment links | `rtk python3 scripts/validation/check-document-links.py --mode alignment` | Baseline: `documents=362 links=2749 failures=251`; findings are the shared Task 4/7 planned Stage 04 and active/archive-link baseline, not Task 6 old-path failures. |
| Python quality | Ruff and `python3 -m py_compile` over `architecture.py`, `metadata_validator.py`, `taxonomy.py`, and the three focused test modules | PASS: Ruff `[]`, compilation exit `0`. |
| Git and preservation | Source/target/status recount; cached and working-tree `git diff --check`; Migration SHA-256 | Final recount before commit: descriptions `25`, decisions `26`, old sources `0`, native renames `51`; both diff checks passed. Migration SHA-256 remains `271f21c50cf4ab765422ee552de244a4340c160e53149231eb6be45f03476ab9`. The reviewed implementation was committed as `7001e8d984aadccfa942afd765cdcab9db43c84f`. |

## Review Evidence

| Review | Status | Findings and disposition |
| :--- | :--- | :--- |
| Initial independent reviews | CHANGES_REQUIRED (`C0/I4/M0`) | Found one evidence-route regression, nine frozen-profile fixture cases, a same-inode mixed-read race, and ineffective supersession successors. |
| Fix round 1 independent re-reviews | APPROVED (`C0/I0/M0`) | Both reviewers reproduced the fixes, the 258-test baseline attribution, Stage 02 inventory and reciprocal ADR relation, focused gates, consumer convergence, and Migration preservation. |

## Commit Ledger

| Commit | Description |
| :--- | :--- |
| `7001e8d984aadccfa942afd765cdcab9db43c84f` | `refactor(architecture): use prefixless document paths`; parent-owned logical Task 6 implementation commit. Migration recovery commits remain intentionally unbound until Task 13. |

## Rulings

- Stage 02 directory ownership, not a filename prefix, determines whether a document is an Architecture Description or ADR; stable frontmatter identities remain uppercase `AD-####` and `ADR-####`.
- Superseded ADRs remain in Stage 02. Reciprocal `supersedes`/`superseded_by` edges must name existing ADR nodes, be asymmetric only in direction, and remain acyclic.
- The retired Stage 02 requirement subdirectory is forbidden. Stage 01 Requirement Packages are the sole stable upstream requirement inputs.
- `docs/99.templates/support/document-metadata-profiles.yaml` remains a bounded legacy transition input; the canonical current Registry and all current template-selection consumers publish prefixless Stage 02 routes.
- Exact artifact IDs in the frozen legacy profile envelope remain resolvable for relation-boundary tests. The read-only `prd-####` alias derived from a canonical Requirement Package remains restricted to immutable Stage 98 evidence.

## Deferred Items

- Task 4 owns the two retired incident-route publication assertions.
- Task 7 owns the non-regular Stage 04 task and the downstream link-alignment baseline.
- Task 13 owns Migration recovery binding; Migration 0003 remains byte-identical and its Task 6 rows remain `planned` with null recovery commits until then.
