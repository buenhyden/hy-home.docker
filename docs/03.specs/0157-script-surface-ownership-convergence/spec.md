---
profile_id: spec
status: active
artifact_id: SPEC-0157
artifact_type: spec
parent_ids: [REQ-0024, REQ-0025]
created: 2026-08-30
updated: 2026-08-31
---

# Script Surface Ownership Convergence Specification

## Overview

`scripts/` and `tests/` hold 97,264 lines whose directory layout no longer states
what owns what. Libraries and command entrypoints share one directory, and a
hand-maintained constant substitutes for the boundary the directory should
express. At the discovery snapshot, nineteen of forty-five test modules were
not reachable from a registered gate and eight of those were failing; the
post-Task-4 measured unregistered/failing set is authoritative for execution.

This Spec Package converges the script surface on one ownership rule, reduces the
machinery that no gate reaches, registers every test module, and splits the four
monolith files that exceed the repository's own 800-line cohesion limit by an
order of magnitude.

Reduction comes before restructuring. Moving unreachable code into a cleaner
directory produces a tidier version of the same excess.

## Boundaries and Inputs

### In Scope

- `scripts/` layout, and the library/entrypoint boundary within it.
- `tests/` layout, mirrored to the `scripts/` responsibility structure.
- Gate registration for every test module on disk.
- Unregistered modes of `check-document-corpus-lifecycle.py`.
- The pinned-commit recovery layer in `scripts/lib/document_governance/archive.py`.
- Census constants that a legitimate content change breaks.
- `scripts/README.md` and `tests/README.md`, where they contradict current governance.

### Out of Scope

- `docs/` content outside the two READMEs and the Stage 98 recovery procedure.
- Provider surfaces under `.agents/`, `.claude/`, `.codex/`, which are generated.
- `infra/`, `projects/`, and service code.
- SPEC-0155's remaining Tasks, which close on their own schedule.

### Inputs

- `scripts/manifest.yaml`.
- `scripts/lib/document_governance/suite_registry.py`, which owns suite binding.
- `scripts/validation/ci_gate_runner.py` and `.github/workflow-contract.yml`, which own gate registration.
- `docs/99.templates/registry.json`, the machine authority for document profiles.

## Behavior Contract

### One ownership rule

A directory states what its files are, and no constant restates it.

| Directory | Owns | Forbidden |
| :--- | :--- | :--- |
| `scripts/lib/<domain>/` | Importable domain logic | Manifest execution contexts or filesystem entrypoint ownership |
| `scripts/<surface>/` | Command entrypoints: argv, exit codes | Domain logic implementation |
| `tests/lib/<domain>/` | Library-unit tests for exactly `scripts/lib/<domain>/` | Another library domain's tests |
| `tests/validation/` | Validation and entrypoint tests | Library-unit ownership claims |

`NON_STANDALONE_VALIDATOR_PATHS` is derived from this rule and deleted as a
literal.

### Every test module is reachable

A test module on disk is registered in a gate or it is removed. There is no
third state. At the discovery snapshot, the unreached set included failing
modules, including one whose fixture copied a document from a deleted Spec
Package. Task 5 uses the post-Task-4 measured unregistered/failing set rather
than that historical count or its predecessor names.

### A census is derived, not frozen

Authoring one tombstone during this Spec Package's own design broke **eleven**
hand-maintained counts, one of them encoded in a test's name
(`test_all_188_preservation_decisions_are_unique_and_reviewed`). Creating this
Spec Package broke a twelfth. Counts that describe repository content are
computed from that content. A count stays pinned only when it guards a
deliberate decision, such as the number of registered validators, and then it
carries the reason in a comment.

### A test judges the corpus, never a deleted taxonomy

The test harness resurrects deleted documents from pinned commits and validates
against them. Measured: five test modules do it, `HISTORICAL_COMMIT` alone is
referenced 43 times, and **all seven** resurrected paths are absent from the
working tree, along with the `docs/99.templates/support/` directory that held
them.

The consequence is not theoretical. `load_transition_overrides` required
`evidence_task` to match `docs/03.specs/spec-<slug>/task.md`, a shape with zero
instances in this repository, because that is the shape the resurrected profile
blob defines. The validator was matching the harness rather than the corpus, and
the override was unsatisfiable for as long as that held. This is the same
pinned-commit pattern SPEC-0155 Task 4 removed from `load_profiles`, surviving
in the largest test file in the repository.

A document-contract fixture states what the repository is now. It is derived
from the current Stage 99 Registry or template and changed by one field for a
negative case; it never copies a deleted body. Recovery behavior is different:
it is exercised in a temporary Git repository or against a current Stage 98
recovery row, where proving a regular blob is the behavior under test.

### History scanning does not grow without bound

`identity_history.py` reads the complete patch history of each stage directory
and greps it for identifiers. Measured at this commit: `docs/03.specs` is 17.4 MB
and `docs/90.references` is 20.6 MB of patch text, both past the 16 MiB bound
the scan enforced. Deleting a 2.4 MB document is what pushed `docs/03.specs`
over, so corpus cleanup makes the scan more expensive, and the bound was raised
to 64 MiB as a stopgap that names this Spec Package as the owner of the fix. The
scan must obtain identifiers from Git rather than read every diff.

### A mode is registered or removed

`check-document-corpus-lifecycle.py` exposes eighteen modes; three are
registered. `check-recovery` is registered because re-proving that every
tombstone's `commit:path` resolves to a regular Git blob is a real guarantee.
The other fourteen are removed.

## Technical Approach

### Target layout

```text
scripts/
├── README.md
├── manifest.yaml
├── lib/
│   ├── document_governance/
│   ├── gate/               # ci_gate_contract, ci_gate_adapters,
│   │                       #   github_workflow_contract, suite_registry
│   ├── agent_governance/   # agent_governance_contract
│   ├── supply_chain/       # grype_db_seed, supply-chain policy
│   ├── target_surface/     # target_surface_contract, *_delta_contract
│   └── ops/                # operational library scripts
├── validation/             # document-governance and execution-context entrypoints
├── gate/                   # run-ci-gate, run-ci-precommit, run-local-qa-gates
├── security/
├── operations/
├── knowledge/
└── hooks/

tests/
├── README.md
├── fixtures/
├── lib/
│   ├── document_governance/
│   ├── gate/
│   ├── supply_chain/
│   ├── target_surface/
│   ├── agent_governance/
│   └── ops/
└── validation/             # entrypoint tests, including agent-output evaluation
```

`tests/docs/`, `tests/qa/`, and `tests/setup/` hold only a README each and
describe a structure that was never built. They are replaced by the directories
above.

### Monolith split

| File | Lines | Becomes |
| :--- | ---: | :--- |
| `metadata_validator.py` | 6,774 | `lib/document_governance/metadata/` — profile, lifecycle, heading, identity, reference |
| `check-document-corpus-lifecycle.py` | 6,484 | one entrypoint plus `lib/document_governance/lifecycle/` |
| `test_document_metadata.py` | 8,426 | one module per production module above |
| `test_document_corpus_lifecycle.py` | 7,022 | one module per production module above |

The split happens after reduction and after registration, so it operates on code
that is both smaller and covered.

## Interfaces and Data

- `scripts/manifest.yaml` rows change `path` and `tests` for every moved file. Row count is unchanged by the move itself.
- `suite_registry.py` keeps `PUBLIC_SUITE_OWNERSHIP` keyed by the new paths and loses `NON_STANDALONE_VALIDATOR_PATHS`.
- `ci_gate_runner.py` and `.github/workflow-contract.yml` gain the module names that are currently unregistered.
- Python import paths change for every moved module. No public CLI name changes, so no caller outside this repository is affected.

## Failure Modes and Guardrails

| Failure mode | Guardrail |
| :--- | :--- |
| A move silently drops a gate binding | `check-script-manifest.py` and the validator-count pins fail closed |
| Reduction removes a live guarantee | Every removal names its consumers, measured before deletion, per SPEC-0155 ruling 1 |
| A split changes behavior | `--profile full` is compared before and after each split commit |
| A repaired test is made to pass rather than fixed | Each member of the post-Task-4 measured unregistered/failing set gets a stated root cause and a disposition |
| Evidence documents cite moved paths | Historical citations stay as literals; only clickable links are updated |
| A truncated search is read as proof of absence | Absence is proven with an untruncated sweep; SPEC-0155 recorded this failure |

## Acceptance Contract

1. Every file under `scripts/lib/` is importable and its manifest row declares no execution contexts.
2. Every file under `scripts/validation/`, `scripts/gate/`, `scripts/security/`, and `scripts/operations/` is an entrypoint and implements no domain logic.
3. `NON_STANDALONE_VALIDATOR_PATHS` no longer exists.
4. Test modules on disk and test modules run by `--profile full` are the same set.
5. Each module in the post-Task-4 measured unregistered/failing set passes or is removed with a recorded reason.
6. `check-document-corpus-lifecycle.py` exposes exactly four modes, all registered.
7. `provenance_policy.py` no longer exists. `TASK10_BASELINE_COMMIT` and
   `APPROVED_BASELINE_RECOVERY_PATHS` stay: SPEC-0155 measured that commit as the
   lookup point for 234 deleted documents' recovery records, so removing it would
   delete a live guarantee rather than dead SHA tracking.
8. `docs/98.archive/README.md` states the recovery procedure without pinning a commit. Closed by SPEC-0155; this item guards against regression.
9. Adding one tombstone changes no count literal in `scripts/` or `tests/`, and no test name contains a count.
10. The identity scan's cost does not grow with repository history, and `MAX_GIT_OUTPUT_BYTES` is not a stopgap.
11. No document-contract or target-surface test resurrects a deleted document
    from a fixed workspace commit. `HistoricalDocument` remains only in tests
    whose subject is current Stage 98 recovery, and those tests use a temporary
    Git repository or a current recovery row.
12. No file under `scripts/` or `tests/` exceeds 800 lines, or the exception is registered with a reason.
13. `scripts/README.md` and `tests/README.md` contain no reference to Stage 04 and no claim that the blocking metadata gate is inactive.
14. `run-ci-gate.py --profile full` exits 0.

## Traceability

| Requirement | Coverage |
| :--- | :--- |
| REQ-0024 Agent governance standardization | The ownership rule, gate registration for every module, and the provider surfaces left generated and untouched |
| REQ-0025 Operational readiness closure | The post-Task-4 measured unregistered/failing set identifies this requirement's current verification surface. Registering and repairing that measured set restores the evidence REQ-0025 claims without running. |

Inherited from SPEC-0155, which closed with these three items open and
measured, not assumed:

| SPEC-0155 item | State at its close | Where it lands here |
| :--- | :--- | :--- |
| 5, no `f259c139` in `docs/` | Closed. The normative pin is gone from Stage 98; the constant stays in `archive.py` because it is the lookup point for 234 documents' recovery records | Only as data for the reduction, never as a deletion target |
| 7, full inventory blocking | Closed. `--mode check-active` already blocks 421 documents at zero violations | Nothing inherited |
| 13, transition override wiring | Path contract and status set corrected; still unreachable, since no gate passes `--transition-override-file` | Retired or wired, with the reason recorded |
| Test harness on resurrected profiles | `test_document_metadata.py` runs the checker against a profile blob read from a pinned commit, knowing only the retired taxonomy | The current-authority fixture work in Acceptance 11 and the monolith split |

SPEC-0155 acceptance item 6 was corrected rather than inherited: it demanded that
`docs/04.execution` not appear in `scripts/`, and nine of its ten occurrences are
absence assertions and pinned history reads that enforce the removal the item
checks.

Predecessor: SPEC-0155 reduced the validation surface's content. This Spec
Package converges its structure. The two are sequential, not overlapping:
SPEC-0155 removed what no gate reached inside the existing layout; SPEC-0157
changes the layout so the same drift cannot recur silently.

## Related Documents

- [Validation surface reduction](../0155-validation-surface-reduction/spec.md)
- [Governance consistency convergence](../0154-governance-consistency-convergence/spec.md)
- [Stage 99 document registry](../../99.templates/registry.json)
- [Scripts README](../../../scripts/README.md)
