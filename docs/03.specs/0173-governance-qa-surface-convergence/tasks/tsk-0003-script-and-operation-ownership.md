---
title: "Script and Operation Ownership Task"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "specs"
artifact_id: "SPEC-0173-TSK-0003"
parent_ids:
- "SPEC-0173"
- "SPEC-0173-PLAN-0001"
created: "2026-09-05"
---

# Script and Operation Ownership Task

## Objective

Remove obsolete wrappers and one-off validation surfaces, relocate operational
entrypoints to their canonical domain, and resolve self-successor lifecycle
residue in the script inventory.

## Inputs

- [SPEC-0173](../spec.md), its [implementation plan](../plan.md), and the gate
  composition established by Task 0002.
- `scripts/validation/`, `scripts/lib/`, `scripts/operations/`,
  `scripts/hardening/`, `scripts/hooks/`, `scripts/knowledge/`, and the script
  manifest.
- The wrapper, compatibility, mutation-mode, report, and transition findings
  enumerated in the Plan.

## Work Log

Task 2 converged executable composition at `93a26645` and recorded its focused
evidence at `da88af1d`. Task 3 became ready at `41145af4` and started at
`083eed03`. The initial manifest RED reproduced seven self-successor records;
the bounded cutover then moved every current consumer before deleting a public
wrapper or semantic owner.

Implementation commit `174c29d9` removes the two document-link shell wrappers,
the local QA and harness compatibility dispatchers, the target-surface
executable subsystem, and the standalone audit coverage report. Document graph
validation now has one Python owner, the typed gate is the only public aggregate
CLI, and audit coverage is generated and checked by the audit implementation
matrix owner.

The Compose readiness implementation moved to a non-executable
`scripts/lib/ops/` library behind an executable `scripts/operations/`
entrypoint. The PostgreSQL rehearsal also moved to `scripts/operations/`; its
registered aggregate route is restricted to `--check-config-only`, so no
runtime mutation mode is reachable from validation. Current Requirement,
Architecture, Operations, Research, and Audit consumers were cut over, and the
two affected generated reference outputs were refreshed through their owners.

## Verification Evidence

| Check | Result |
| --- | --- |
| Manifest RED | Seven self-successor records reproduced before implementation |
| Script manifest | `check-script-manifest.py` passed; 58 focused tests passed |
| Gate contract and runner | 16 contract tests and 32 runner tests passed; each public plan retained unique normalized invocations |
| GitHub workflow contract | 47 tests passed with 11 intentional Wave-C skips; executable modes and static gate routes passed |
| Document graph | 37 focused tests passed and `check-document-links.py --mode all` reported 689 documents, 5,748 links, and 0 failures |
| Operation boundaries | 46 Compose readiness tests and 51 PostgreSQL rehearsal tests passed; shell syntax passed for both operation entrypoints and the source-only library |
| Entrypoints and audit matrix | 3 validator-entrypoint tests and 9 audit-criterion tests passed; matrix `--check` passed after regeneration |
| Generated references | Audit matrix and both LLM Wiki outputs passed their canonical freshness checks |
| Typed changed profile | `run-ci-gate.py --profile changed --explain` listed each selected canonical entrypoint once and executed none |
| Current residue | Zero current references to deleted Task 3 paths outside the four Task 5 target-surface DATA packages and their registry mapping |
| Metadata and whitespace | Changed metadata selected 25 documents with 0 violations; `git diff --check` passed |

## Review Evidence

Focused mutation tests reject duplicate public invocations, runtime validator
rebinding, executable manifest composition, untracked entrypoints, self-
successors, and operation authority drift. The final independent repository
review remains assigned to Task 0006 and must recheck that retired paths have
no current consumer and that operational write modes are not reachable from
validation profiles.

## Commit Ledger

| Commit | Scope |
| --- | --- |
| `083eed03` | Start Task 3 from the accepted Task 2 milestone |
| `174c29d9` | Align command ownership, relocate operation entrypoints, remove obsolete wrappers and target-surface executables, and cut over current consumers |

This evidence checkpoint does not predict its own commit identity.

## Rulings

- Keep a wrapper only when it is a documented public compatibility boundary
  with a current consumer.
- Validation profiles may call operation check modes but never operation write
  modes.
- Resolve transition records to a real successor or a terminal lifecycle; a
  script cannot be its own successor.

## Deferred Items

- Historical Git blobs and immutable archive evidence are not rewritten.
- New general-purpose script frameworks are outside the bounded convergence
  scope.
- The four target-surface DATA packages and their registry mapping remain a
  Task 0005 lifecycle retirement; they are not current executable consumers.
- Reverting `174c29d9` is the Task 3 rollback boundary. Restoring only a wrapper
  or target-surface library would recreate split ownership and is not a valid
  partial rollback.

## Related Documents

- [SPEC-0173 package](../spec.md)
- [SPEC-0173 implementation plan](../plan.md)
- [Gate composition Task](tsk-0002-gate-composition-convergence.md)
