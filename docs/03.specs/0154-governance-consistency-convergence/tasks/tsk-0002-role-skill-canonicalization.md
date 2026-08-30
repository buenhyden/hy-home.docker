---
profile_id: task
status: completed
artifact_id: task-0154-0002
artifact_type: task
parent_ids: [SPEC-0154, plan-0154]
created: 2026-08-30
updated: 2026-08-30
---

# Role and Skill Canonicalization

## Objective

Narrow the Stage 99 `governance-role` profile to the agent-role genre and rename the two skills whose identifiers collide with globally installed provider skills. Plan Task 2.

## Inputs

- Task 1 result: `roles/` holds only agent roles.
- `docs/99.templates/registry.json` `profiles[governance-role]`.
- `docs/00.agent-governance/skills/{code-reviewer,test-automator}.md` and the two roles that reference them.

## Work Log

| Step | Action | Result |
| :--- | :--- | :--- |
| 0 | Corrected three plan commands before executing | See Rulings 1 to 3 |
| 1 | Confirmed `roles/` holds only agent roles | 14 files, all carrying `agent_id`; a field-presence probe confirmed all 14 already carry all seven fields |
| 2 | Narrowed `profiles[governance-role]` | Seven fields moved to `required_frontmatter`; `optional_frontmatter` is now empty |
| 3 | Verified the profile change | `check-document-metadata.py` exit 0; `test_registry` failed with `KeyError: 'agent_id'` and was extended |
| 4 | Renamed the two colliding skills | `code-reviewer.md` to `change-review-execution.md`, `test-automator.md` to `test-authoring.md`, with `function_id` and title updated |
| 5 | Updated the referring roles | `roles/code-reviewer.md` and `roles/qa-engineer.md` `skill_ids` and Related Documents |
| 6 | Regenerated the projections | `--write` reported `providers=2 drift=0`; `.agents/skills` and `.claude/skills` hold 23 each, matching 23 canonical skills |
| 7 | Verified | See Verification Evidence |

**Deviation.** Step 7 found two canonical skills still linking the old
identifiers: `skills/e2e-testing.md` to `test-automator.md` and
`skills/code-review-dimensions.md` to `code-reviewer.md`. The registered link
gate did not catch them because `docs/00.agent-governance` is outside its
`DOC_ROOTS`. Both were repointed and the projections regenerated. This is the
same gate hole Task 5 closes, observed a second time.

**Rollback.** `git revert` of the Task 2 commit restores the two skill
filenames, the profile shape, and the test sample values together.

**Skipped checks.** `run-ci-gate.py --profile full` runs at the plan's final
Verification. Compose, hardening, and runtime checks are N/A.

## Verification Evidence

| Command | Result |
| :--- | :--- |
| `python3 scripts/validation/check-agent-governance-contract.py --mode repository --section all` | exit 0, `PASS failures=0` |
| `python3 scripts/validation/check-document-metadata.py` | exit 0, 596 tracked, 13 findings, no `governance-role` finding |
| `python3 scripts/validation/check-document-links.py --mode all` | exit 0, `failures=0` |
| `python3 -m unittest tests.lib.document_governance.test_registry` | `KeyError: 'agent_id'` before the test extension; `Ran 34 tests OK` after |
| `bash scripts/operations/sync-provider-surfaces.sh --write` | exit 0, `providers=2 drift=0` |
| `bash scripts/operations/sync-provider-surfaces.sh --check` | exit 0 |
| `grep -rn "skills/code-reviewer.md\|skills/test-automator.md" docs/00.agent-governance .claude .agents .codex scripts` | no match |

**Runtime evidence for the collision fix.** After the rename, the session's
skill listing surfaced `change-review-execution` and `test-authoring` as
project skills alongside the globally installed `code-reviewer` and
`test-automator`. Before the rename the project skills did not appear at all,
which is what the Spec predicted.

## Review Evidence

Pending independent review. The implementer self-check found one material
defect during execution: two canonical skills still linked the pre-rename
identifiers and no registered gate reported it.

## Commit Ledger

| Subject | Paths |
| :--- | :--- |
| `docs(governance): Give the runtime-routing role fields a required contract` | `docs/99.templates/registry.json`, `docs/00.agent-governance/skills/`, `docs/00.agent-governance/roles/{code-reviewer,qa-engineer}.md`, `tests/lib/document_governance/test_registry.py`, `.agents/skills/`, `.claude/skills/`, `docs/03.specs/0154-*/plan.md` |

## Rulings

Plan rulings 1 to 5 apply. Four execution rulings were made.

1. **`sync-provider-surfaces.sh` needs `--write` to regenerate.** Its default is
   `--check`, which reports drift and exits 1 without writing. The plan was
   corrected before this Task ran.
2. **This repository runs `unittest`, not `pytest`.** `pytest` is not installed
   and `ci_gate_adapters.py` dispatches `run-unittest`. Every `pytest` command
   in the plan was rewritten as `python3 -m unittest`.
3. **`registry.json` is edited textually, not re-serialized.** A
   `json.dumps(indent=2)` round trip reformatted 2,021 lines because the file
   stores arrays inline. The change was reverted and reapplied as a two-line
   text edit.
4. **The registry test was extended, not weakened.**
   `test_every_canonical_markdown_profile_has_a_satisfiable_profile_id_contract`
   builds synthetic frontmatter from a sample-value table and raised
   `KeyError: 'agent_id'` once the fields became required. Five real values were
   added to that table: `agent_id: rules-engineer`, `tier: worker`,
   `work_profile: routine-validation`, `permission_profile: read-only`, and
   `skill_ids: [policy-gate-agent]`. No assertion was relaxed.

## Deferred Items

- The plan's `sync-provider-surfaces.sh --check && git diff --exit-code`
  verification is only meaningful from an otherwise clean tree. During a Task it
  reports the Task's own staged changes. The renderer's `--check` exit code is
  the load-bearing signal; the `git diff` clause runs at the plan's final
  Verification.

## Related Documents

- [Plan](../plan.md)
- [Specification](../spec.md)
