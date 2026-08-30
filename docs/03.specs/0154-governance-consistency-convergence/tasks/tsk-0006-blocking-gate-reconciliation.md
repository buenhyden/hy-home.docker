---
profile_id: task
status: completed
artifact_id: task-0154-0006
artifact_type: task
parent_ids: [SPEC-0154, plan-0154]
created: 2026-08-30
updated: 2026-08-30
---

# Blocking Gate Reconciliation

## Objective

Run the metadata gate in the mode CI actually enforces, resolve what this Spec
Package caused, and route what it did not. Added after Tasks 1 to 5, because
those Tasks verified against the advisory inventory and never against the
blocking condition.

## Inputs

- `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref e2ef015e`.
- `docs/99.templates/registry.json`, profiles `governance-role`, `governance-skill`, `governance-policy`.
- `scripts/lib/document_governance/metadata_validator.py` lines 2396 to 2445 and 6115 to 6150.

## Work Log

| Step | Action                                                                | Result                                                    |
| :--- | :-------------------------------------------------------------------- | :-------------------------------------------------------- |
| 0    | Ran the blocking mode for the first time                              | **7 violations**, against exit 0 in the advisory mode     |
| 1    | Measured the section vocabulary of the 14 role and 23 skill documents | Both sets are 100 percent uniform                         |
| 2    | Registered both vocabularies as `required_sections`                   | 7 to **5**                                                |
| 3    | Added `supersedes: [SPEC-0131]` to SPEC-0136                          | 5 to **4**                                                |
| 4    | Added a `free-form-sections` exception plus a validator branch        | **Zero effect.** Reverted, see the deviation              |
| 5    | Located the emission site for the remaining heading findings          | `metadata_validator.py:2442`, reading `registry.profiles` |
| 6    | Probed the mechanism by registering the 13 changed headings           | 4 to **2**, mechanism confirmed, probe reverted           |
| 7    | Read the transition override contract                                 | Unreachable for every path in the repository, see below   |

**Deviation, an unsupported claim was committed and then withdrawn.** Step 4
added `exceptions: [{"kind": "free-form-sections"}]` to two profiles with a
validator branch honoring it, and the commit message claimed it resolved the
policy heading findings. Measurement after the fact showed the
`body-heading-forbidden` count identical with and without the change. It was
reverted in a commit that states the unsupported claim and names what actually
worked. The diagnosis given at the time, that `profiles` lacks `_registry` on
this route, was itself wrong: it measured a bare `load_profiles()` call, while
the CLI builds its profiles through the adapter at `metadata_validator.py:5151`,
which does inject `_registry`. The revert stands because the change had no
effect; only its stated cause was wrong.

**Rollback.** `git revert` of the Task 6 commits restores the previous section
registrations and removes the SPEC-0136 `supersedes` field.

**Skipped checks.** None.

## Verification Evidence

| Measure                                                         | Task 5 end | Task 6 end |
| :-------------------------------------------------------------- | ---------: | ---------: |
| `check-changed --base-ref e2ef015e` violations                  |          7 |      **4** |
| `governance-role` documents with a registered section contract  |          0 |     **14** |
| `governance-skill` documents with a registered section contract |          0 |     **23** |
| `replacement-free-supersession` records                         |          1 |      **0** |

| Command                                                               | Result                                             |
| :-------------------------------------------------------------------- | :------------------------------------------------- |
| `check-document-metadata.py` (full inventory)                         | exit 0                                             |
| `check-document-links.py --mode all`                                  | exit 0                                             |
| `check-agent-governance-contract.py --mode repository --section all`  | exit 0                                             |
| `python3 -m unittest tests.lib.document_governance.test_registry`     | OK                                                 |
| `check-document-metadata.py --mode check-changed --base-ref e2ef015e` | **violations=4**                                   |
| `run-ci-gate.py --profile full`                                       | exit 1, the identity-scan test routed to SPEC-0155 |

## Review Evidence

Pending independent review. Self-review found the Step 4 defect and the wrong
diagnosis attached to it; both are recorded above rather than removed from the
history.

## Commit Ledger

| Subject                                                                              | Paths                                                                                      |
| :----------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------- |
| `fix(registry): State the section contract Stage 00 documents actually follow`       | `docs/99.templates/registry.json`, `docs/03.specs/0136-*/spec.md`                          |
| `revert(registry): Withdraw the free-form-sections exception, which changed nothing` | `docs/99.templates/registry.json`, `scripts/lib/document_governance/metadata_validator.py` |
| `docs(spec): Close SPEC-0154 with four violations routed to SPEC-0155`               | this Task, `../spec.md`, `../plan.md`, `../../0155-*/spec.md`                              |

## Rulings

1. **The blocking mode is the acceptance condition, not the inventory.**
   `check-document-metadata.py` with no mode reports an advisory inventory and
   exits 0 while CI fails. Tasks 1 to 5 of this Spec Package verified against
   the advisory form. Every future acceptance contract in this repository names
   `--mode check-changed --base-ref <merge-base>` explicitly.
2. **A fix that cannot be measured is not a fix.** Step 4 was committed on
   reasoning rather than on a before-and-after count. The rule applied from
   Step 5 onward is that a validator or registry change is measured against the
   failing condition before its commit message describes what it does.
3. **The two remaining heading findings are not this Spec Package's to close.**
   The mechanism is confirmed, but the only available lever registers headings
   per profile, and `governance-policy` spans 16 documents with a heterogeneous
   heading vocabulary. Registering only the 13 headings this Spec Package
   changed would whitelist its own edits and leave the rest of the profile
   unregistered, which is the asymmetry this Task exists to expose rather than
   exploit. SPEC-0155 owns the choice between a real contract and an honest
   free-form declaration.

## Deferred Items

Four blocking violations remain and are routed to SPEC-0155.

| Finding                                     | Path                                                | Verified mechanism                                                                                                                                                                                                                                                                                                                                        |
| :------------------------------------------ | :-------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `body-heading-forbidden` count=6            | `policies/quality-standards.md`                     | `governance-policy` registers `required_sections: ["Related Documents"]` and `optional_sections: []`, so every other H2 in all 16 documents of the profile is unregistered. Only headings a change introduces are counted, so the corpus passes while a change to it fails. Registering the changed headings drops the count to 0, measured.              |
| `body-heading-forbidden` count=3            | `policies/environment-constraints.md`               | Same profile, same mechanism.                                                                                                                                                                                                                                                                                                                             |
| `invalid-transition: archived -> completed` | `migrations/0001-sdlc-taxonomy-convergence.md`      | The override at `metadata_validator.py:6135` requires `evidence_task` to start with `docs/03.specs/spec-` **and** to be named `task.md`. The repository holds 0 directories matching `docs/03.specs/spec-*` and 0 files named `task.md` against 15 named `tsk-*.md`. No path in this repository can satisfy the contract, so the override is unreachable. |
| `invalid-transition: archived -> completed` | `migrations/0002-operations-catalog-convergence.md` | Same unreachable override.                                                                                                                                                                                                                                                                                                                                |

The identity-scan failure in `--profile full` remains routed to SPEC-0155 from
Task 5.

## Related Documents

- [Plan](../plan.md)
- [Specification](../spec.md)
- [Validation surface reduction](../../0155-validation-surface-reduction/spec.md)
