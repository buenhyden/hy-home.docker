---
title: "Gate Composition Convergence Task"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "specs"
artifact_id: "SPEC-0173-TSK-0002"
parent_ids:
- "SPEC-0173"
- "SPEC-0173-PLAN-0001"
created: "2026-09-05"
---

# Gate Composition Convergence Task

## Objective

Make the workflow contract the single executable composition owner and prove
that each canonical leaf invocation occurs once per public profile and context.

## Inputs

- [SPEC-0173](../spec.md), its [implementation plan](../plan.md), and the RED
  contracts produced by Task 0001.
- `.github/workflow-contract.yml`, `scripts/manifest.yaml`, the gate runner,
  setup dispatchers, CI workflow, pre-commit configuration, and focused tests.
- Baseline duplicate identities for Compose validation and frontend dependency
  setup.

## Work Log

Task 1 completed its implementation milestone at `b7fb8911` after preserving
SPEC-0172, proving recovery, and passing independent review. Task 2 starts from
that clean state. The canonical invocation uniqueness test first reproduced
both measured duplicate families: changed/pull-request rendered 31 invocations
for 30 identities, full/local rendered 50 for 49, full/push rendered 63 for 61,
and full/workflow-dispatch rendered 62 for 60.

Implementation commit `93a26645` moves public validator suite, argv, and
context ownership into `.github/workflow-contract.yml`; `scripts/manifest.yaml`
now owns inventory, lifecycle, consumers, and tests only and rejects the three
retired executable fields. The runner rejects duplicate normalized
`realpath + argv + profile + context` identities with
`ci-gate-invocation-duplicate`. The redundant Compose route, second frontend
dependency setup, node/profile-root compatibility grammar, orphan generated
freshness aggregate, manifest-backed suite parser, and its mirrored test were
removed after all current consumers moved to `PublicGateContract`.

The Plan listed `tests/lib/document_governance/test_surface_ownership.py`; the
tracked owner is `tests/lib/test_surface_ownership.py`, so the Plan path was
corrected without changing scope.

## Verification Evidence

| Check | Result |
| --- | --- |
| Canonical invocation RED | Reproduced npm setup and Compose duplicates with the exact counts recorded in the Work Log |
| Gate contract | 16 tests passed, including bounded manifest input, retired profile grammar, graph mutation, public ownership, contexts, and capability weakening |
| Gate runner | 32 tests passed across all public profiles and execution contexts |
| GitHub workflow contract | 47 tests passed; 11 existing Wave-C skips remained intentional |
| Script manifest | 55 tests passed and `check-script-manifest.py` returned exit 0 |
| Surface ownership and target delta | 27 tests passed |
| Agentic audit semantic freshness | 33 tests passed after its ownership mutations moved to `public_gate.validators` |
| Reference, metadata, operations, tech-stack, and PostgreSQL consumers | Focused suites passed after cutover; the PostgreSQL inventory assertion passed independently |
| Live workflow gate | `check-github-workflow-contract.py` passed with 6 workflows, 8 jobs, and 8 pinned actions |
| Public explain plans | changed and full each rendered 20 unique local validator entrypoints, exit 0 |
| Storybook contract | Direct checker passed after sharing one npm setup node |
| Whitespace | `git diff --check`, exit 0 before the implementation commit |

## Review Evidence

Mutation coverage confirms that the manifest rejects executable composition,
the workflow contract rejects duplicate validators and retired profile fields,
and the runner rejects duplicate normalized invocations. The final independent
repository review remains assigned to Task 0006 and must confirm that no second
executable registry or hidden aggregate was introduced.

## Commit Ledger

| Commit | Scope |
| --- | --- |
| `17cb7c48` | Start Task 2 from the accepted Task 1 milestone |
| `93a26645` | Converge executable composition, remove duplicate routes and the obsolete suite registry, and cut over current consumers |

This evidence checkpoint does not predict its own commit identity.

## Rulings

- `.github/workflow-contract.yml` owns executable ordering and routing.
- `scripts/manifest.yaml` remains an inventory and lifecycle owner; it does not
  retain duplicate suite, context, or argument composition.
- Remove duplicate invocations rather than suppressing duplicate diagnostics.
- Preserve direct Compose validator support for `HYHOME_COMPOSE_PROFILES` while
  forbidding aggregate runner injection of that variable.
- Derive graph reachability from CI job roots and public suite roots instead of
  maintaining a second local profile-root taxonomy.

## Deferred Items

- Changing remote required checks, branch protection, or Hosted CI state is
  outside this Task.
- The `validation-changed` and `validation-full` public names remain stable.
- Reverting `93a26645` is the rollback boundary. Partial restoration of the
  manifest fields, profile roots, or deleted suite parser would recreate split
  ownership and is not a valid rollback.

## Related Documents

- [SPEC-0173 package](../spec.md)
- [SPEC-0173 implementation plan](../plan.md)
- [Lifecycle and RED contracts Task](tsk-0001-lifecycle-and-red-contracts.md)
