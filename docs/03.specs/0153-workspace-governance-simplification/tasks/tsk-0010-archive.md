---
profile_id: task
status: active
artifact_id: task-0153-0010
artifact_type: task
parent_ids:
  - SPEC-0153
  - plan-0153
created: 2026-08-21
updated: 2026-08-27
---

# Task 0010: Archive

## Objective

Minimize Stage 98 to migrations and stable-path tombstones backed by Git history.

## Inputs

- [Specification](../spec.md)
- [Implementation Plan](../plan.md)
- [Migration 0003](../../../98.archive/migrations/0003-workspace-governance-simplification.md)
- Task 9 reference convergence, Stage 99 archive profiles, approved Migration owner_task 10 rows.

## Work Log

| Event | Actual result |
| :--- | :--- |
| RED | Added minimal Archive and provenance-policy mutations; the focused suite failed 11/11 because the Task 10 authority modules did not exist. |
| Preservation review | Classified 146 Change packets as `git-only` and 38 retired stable paths as `minimal-tombstone`; every disposition has an approved reviewer decision. |
| Recovery preflight | Proved 234 Change members and 38 Tombstone bodies as regular Git blobs before deletion. Fourteen members from seven packets lacked legacy archive metadata and use the controller-approved `f259c139fb7da166609029cdd3657de87e639f6b:<former-stage-98-path>` tuple. |
| Structural execution | Executed 41 literal native `git mv` operations (three Migrations and 38 Tombstones), retained Migration 0003 byte-identically, deleted 234 duplicate Change bodies, and removed the retired empty `changes/` root. |
| Consumer convergence | Repointed prefixless Migration consumers; current active documents now route through the Archive README or Migrations rather than individual Tombstones; excluded individual Tombstones/retired Change bodies from the canonical LLM Wiki generator. |
| Recovery hardening | Centralized full-commit recovery proof behind fixed-argv Git with pre-Git identity validation, simultaneous bounded pipe drains, a 15-second per-process deadline, process-group cleanup, and three-step commit/tree/blob-object verification. |
| Review remediation | Closed the first independent review's broad-scan, semantic-schema, and missing-blob fail-open findings. Repository provenance now covers authored `.github`, `infra`, Stage 90 Data, Stage 98, and Stage 99 support/template text; Migration 0003's frozen hash and exact Task 10 row semantics are enforced in production recovery mode. |
| Metadata convergence | The first changed-metadata run exposed 136 Task 10-owned violations. Stage 98 README/Data consumers and Tombstone lifecycle metadata were repaired, while the three byte-preserved Migration moves use exact source-baseline recognition; the rerun selected 300 paths with zero violations. |

## Verification Evidence

| Check | Command | Result |
| :--- | :--- | :--- |
| RED | `python3 -m unittest -v tests.validation.test_archive_minimization tests.validation.test_provenance_policy` | Expected failure: 11/11 tests failed before the new modules existed. |
| Recovery preflight | Task 10 bounded recovery audit over the pre-change corpus | Change `234/234`, Tombstone `38/38`, violations `0`; controller baseline exceptions `14`. |
| Focused GREEN | `python3 -m unittest -v tests.validation.test_archive_minimization tests.validation.test_provenance_policy` | `23/23` passed in the controller rerun, including missing-blob, frozen-row semantic mutation, minimal superseded-ADR Tombstone, traversal, and invalid-identity cases. |
| Lifecycle recovery | `python3 -m unittest -v ...Task7CorpusConvergenceTests.test_every_tombstone_has_exact_git_provenance ...test_check_recovery_mode_uses_minimal_archive_authority` | `2/2` passed; runtime mode reported three Migrations, 38 Tombstones, 184 decisions, 272 recovery rows, zero violations. |
| Generator mutation | `python3 -m unittest -v tests.validation.test_generate_llm_wiki.LlmWikiGeneratorTests.test_generated_index_excludes_individual_archive_evidence` | RED reproduced one Tombstone leak; GREEN passed after exact noncurrent-prefix exclusion. |
| Generated references | `python3 scripts/knowledge/generate-llm-wiki.py --write && python3 scripts/knowledge/generate-llm-wiki.py --check` | Both registered Data outputs regenerated and check passed. |
| Archive consumers | Supply-chain and security-readiness generators `--write` then `--check`; active Tombstone concrete-path scan | Both generators passed; concrete active Tombstone consumers `0`. |
| Metadata | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD` | `selected=300`, `violations=0`, four exact base-existing structural-move exceptions, no transition override. |
| Shared link graph | `python3 -m unittest -v tests.validation.test_document_links.DocumentGraphTests` | `17/17` passed; current-to-Archive README/Migration is allowed and current-to-Tombstone remains rejected. |
| Link alignment diagnostic | `python3 scripts/validation/check-document-links.py --mode alignment` | `archive_direct_links_total=0`; 28 inherited missing/oversized/non-regular link findings remain outside Task 10. |
| Static checks | `py_compile`; focused Ruff; `bash -n`; JSON/YAML parse; `git diff --check` | Passed. |
| Frozen Migration | `sha256sum docs/98.archive/migrations/0003-workspace-governance-simplification.md` | `271f21c50cf4ab765422ee552de244a4340c160e53149231eb6be45f03476ab9`. |

### Recovered Audit Task Status

The semantic audit consumer previously read a deleted Stage 98 body directly.
Task 10 recovered that body as a regular Git blob and records only the four
status facts the current semantic gate consumes; the retired body is not copied.

| Task | Recovery evidence | Status |
| :--- | :--- | :--- |
| T-AER-007 | Validated Git recovery tuple for the former agentic audit Task body | Done |
| T-AER-008 | Validated Git recovery tuple for the former agentic audit Task body | Done |
| T-AER-009 | Validated Git recovery tuple for the former agentic audit Task body | Done |
| T-AER-012 | Validated Git recovery tuple for the former agentic audit Task body | Done |

## Review Evidence

| Review | Status | Findings and disposition |
| :--- | :--- | :--- |
| Preservation audit | Complete | 184 unique artifacts classified; missing provenance on seven packets was escalated and resolved by the controller-reviewed Task 10 baseline tuple. |
| Independent Task 10 re-review | Approved | Initial reviews found two important provenance/schema gaps and one critical missing-blob fail-open. All three were remediated; final spec and Python re-reviews returned `C0/I0/M0`, including a production-entrypoint missing-blob mutation. |

## Commit Ledger

| Commit | Description |
| :--- | :--- |

## Rulings

- Git history is the default body archive. Completed Change evidence receives no replacement body or Tombstone unless a stable deleted path requires direct lookup.
- The fourteen missing-metadata members use the controller-approved Task 10 clean baseline; all other Change members retain their pre-existing approved recovery tuple.
- Migration 0003 remains byte-identical in Task 10; Task 13 alone owns its durable compaction.

## Deferred Items

- Full repository gates remain owned by the later gate/closure tasks. Task 10 reports only focused checks and owner-classified diagnostics.
- `generate-audit-implementation-matrix.sh --check` remains blocked before output comparison by the inherited Task 9 flat Stage 90 audit path `docs/90.references/audits/ref-0026-implementation-overview.md`; Task 10's Archive Migration source/output line is aligned and this task does not widen into the stale Stage 90 audit contract.
- Link alignment retains 28 inherited missing, oversized, or non-regular target findings; its Task 10 Archive-boundary count is zero.
