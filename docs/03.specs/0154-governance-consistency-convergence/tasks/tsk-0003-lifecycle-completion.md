---
profile_id: task
status: completed
artifact_id: task-0154-0003
artifact_type: task
parent_ids: [SPEC-0154, plan-0154]
created: 2026-08-30
updated: 2026-08-30
---

# Lifecycle Completion

## Objective

Register a `spec-package` lifecycle with a terminal `completed` status, register `Related Documents` on the 16 content profiles that omit it, correct the two invalid Stage 98 statuses, and complete `generated_roots`. Plan Task 3.

## Inputs

- `docs/99.templates/registry.json` `lifecycles`, `transitions`, and `profiles`.
- `docs/00.agent-governance/providers/registry.yaml` `generated_roots`.
- `scripts/operations/provider_surface_renderer.py` lines 289 to 293 and `EXPECTED_GENERATED_ROOTS`.
- `docs/98.archive/migrations/000{1,2}-*.md`.

## Work Log

| Step | Action | Result |
| :--- | :--- | :--- |
| 1 | Added the `spec-package` lifecycle and bound the `spec` profile to it | `statuses` are `draft, active, completed, superseded, retired`; `transitions.spec` and `profiles[spec].lifecycle_id` both name it |
| 2 | Verified | `check-document-metadata.py` exit 0; `test_registry` 34 tests OK |
| 3 | Registered `Related Documents` on the 16 content profiles that omitted it | All 24 section-bearing profiles now declare it |
| 4 | Corrected the two Stage 98 migration statuses, then completed their frontmatter | `invalid-status` 2 to 0; corpus findings 13 to 11 |
| 5 | Extended `generated_roots` with the two directory-shaped renderer outputs | `.agents/rules` and `.agents/workflows` added; `EXPECTED_GENERATED_ROOTS` extended to match |
| 6 | Verified | See Verification Evidence |
| 7 | Committed | See Commit Ledger |

**Deviation 1, scope.** Step 4 was written as a status correction. Once the
status was valid the same two documents still carried four findings:
`artifact-type-mismatch`, `missing-parent`, `missing-required-key`, and
`profile-id-mismatch`. They were missing `profile_id`, `created`, and `updated`
entirely, and declared `artifact_type: archive` where the profile requires
`migration`. `mig-0003` already has the correct shape, so both were completed to
match it rather than left half-corrected. See Ruling 2 for the parent evidence.

**Deviation 2, a wrong instruction in the Spec.** SPEC-0154 section 3 said to
add all five renderer outputs to `generated_roots`. That would break the
renderer: `_current_managed_files` raises `managed root is not a directory` for
any non-directory entry, and three of the five are single files. Only
`.agents/rules` and `.agents/workflows` are directories. The Spec was corrected
before the change was applied, and the three file routes are recorded as a
deferred item.

**Rollback.** `git revert` of the Task 3 commit restores the previous lifecycle
binding, the two migrations' frontmatter, and both generated-roots tuples
together. No document body was rewritten.

**Skipped checks.** `run-ci-gate.py --profile full` runs at the plan's final
Verification. Compose, hardening, and runtime checks are N/A.

## Verification Evidence

| Command | Before | After |
| :--- | :--- | :--- |
| `check-document-metadata.py` | exit 0, 13 findings, 2 `invalid-status` | exit 0, **11 findings, 0 `invalid-status`** |
| `check-agent-governance-contract.py --mode repository --section all` | exit 0 | exit 0 |
| `check-document-links.py --mode all` | exit 0 | exit 0 |
| `sync-provider-surfaces.sh --check` | exit 0 | exit 0, and `--write` reported `drift=0` with no file deleted |
| `python3 -m unittest tests.lib.document_governance.test_registry` | 34 OK | 34 OK |
| `python3 -m unittest tests.validation.test_provider_surface_renderer` | not run | 13 OK |
| `python3 -m unittest tests.validation.test_agent_governance_contract` | 3 errors | 3 errors, unchanged |

**Pre-existing failure, not caused by this Task.**
`test_mutable_task_token_evidence_is_statement_bounded` errors on three cases
with `FileNotFoundError` for
`docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0004-stage00.md`.
No SPEC-0153 exists in the repository. The same three errors reproduce on the
branch point `e2ef015e` in a clean linked worktree, so the test pins a path that
was removed before this work began.

**Directory-shape probe.** `.agents/rules` and `.agents/workflows` are
directories; `.agents/README.md`, `.claude/CLAUDE.md`, and `.codex/README.md`
are files. Confirmed before the registry edit.

**Prune safety.** After adding the two directories as managed roots, `--write`
reported `drift=0` and `git status` showed no deletion, so nothing inside them
was pruned.

## Review Evidence

Pending independent review. The implementer self-check found one material
defect: SPEC-0154 section 3 instructed a change that would have raised
`managed root is not a directory` in the renderer. The Spec was corrected before
the change was applied.

## Commit Ledger

| Subject | Paths |
| :--- | :--- |
| `feat(registry): Give a Spec Package a way to be finished` | `docs/99.templates/registry.json`, `docs/98.archive/migrations/000{1,2}-*.md`, `docs/00.agent-governance/providers/registry.yaml`, `scripts/validation/agent_governance_contract.py`, `docs/03.specs/0154-*/spec.md` |

## Rulings

Plan rulings 1 to 5 apply. Three execution rulings were made.

1. **A dedicated `spec-package` lifecycle, not a change to `living`.** Adding
   `completed` to `living` would give it to 26 profiles including `policy` and
   `readme`, for which completion has no meaning. The new lifecycle is bound to
   the `spec` profile only.
2. **Both migrations' parent is SPEC-0136, established from evidence, not
   inferred from the name.** `docs/03.specs/0136-sdlc-taxonomy-convergence/`
   holds Task 10B, its `spec.md` references `mig-0001`, its `plan.md` references
   both, and its `tsk-0001` references `mig-0002`. `spec` is in the migration
   profile's `allowed_parent_profiles`. `created` came from each document's own
   `archived_at`.
3. **`generated_roots` means managed directories, not generated files.** The
   renderer treats each entry as a directory it may scan and prune. Forcing the
   three single-file routes into it would have broken the renderer rather than
   documented them.

## Deferred Items

- `.agents/README.md`, `.claude/CLAUDE.md`, and `.codex/README.md` are generated
  by `provider_surface_renderer.py` lines 289 to 293 but are named in no
  declarative field. A reader of `registry.yaml` alone cannot tell they are
  generated. Closing this needs a generated-file manifest that does not exist
  today; routed to SPEC-0155, which owns manifest and validator surface.
- `tests/validation/test_agent_governance_contract.py` pins
  `docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0004-stage00.md`,
  which no longer exists. Three errors, pre-existing at `e2ef015e`. Routed to
  SPEC-0155.
- A `git stash` entry duplicating this Task's changes remains at `stash@{0}`
  after a `stash pop` reported `중지함` while still restoring the working tree.
  Its content is byte-identical to what was committed. It was left in place
  rather than dropped, because `stash@{1}` is a pre-existing user stash and
  stash surgery is not this Task's authority.

## Related Documents

- [Plan](../plan.md)
- [Specification](../spec.md)
