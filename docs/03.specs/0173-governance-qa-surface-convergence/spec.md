---
title: "Governance and QA Surface Convergence Specification"
version: "0.2.0"
type: "sdlc/spec"
status: "active"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "specs"
artifact_id: "SPEC-0173"
parent_ids:
- "REQ-0024"
- "REQ-0026"
- "AD-0027"
- "AD-0030"
- "ADR-0029"
- "ADR-0031"
created: "2026-09-05"
---

# Governance and QA Surface Convergence Specification

## Overview

The repository has the intended two public validation profiles and a typed gate
runner, but executable ownership is divided between
`.github/workflow-contract.yml`, `scripts/manifest.yaml`, and runner-side
admission tables. Different gate identifiers can therefore execute the same
normalized command, completed migration evidence remains in current validation
paths, and compatibility wrappers preserve interfaces whose underlying modes no
longer exist.

This change converges the gate, script, test, fixture, document-governance, and
provider-projection surfaces around their current responsibilities. It removes
completed migration residue without weakening validation, preserves historical
identity recovery, and keeps Stage 00, Stage 03, Stage 90, and Stage 99 ownership
distinct.

## Boundaries and Inputs

- In scope: `.github/workflow-contract.yml`, `.github/workflows/ci-quality.yml`,
  `.pre-commit-config.yaml`, `scripts/manifest.yaml`, the typed gate libraries
  and runner, registered validators and generators, provider projection
  configuration, hooks, tests, fixtures, current operator documentation, and
  generated indexes affected by those paths.
- In scope: valid forward lifecycle reconciliation for SPEC-0172 and retirement
  of DATA-0068, DATA-0069, DATA-0073, and DATA-0074 after inbound-consumer and
  recovery checks pass.
- In scope: current-path and current-ID examples, test placement, fixture
  ownership, public command reduction, and removal of compatibility branches
  that have no current semantic consumer.
- Preserve: the six public suite names, the `changed` and `full` public profiles,
  the `validation-changed` and `validation-full` GitHub job names, `strict=true`,
  GitHub Actions app ID `15368`, artifact identity high-water, and frozen archive
  bodies.
- Preserve: historical readers required to prove issued identity high-water,
  tombstone inheritance, archive recovery, and immutable migration evidence.
- Out of scope: dependency upgrades unrelated to a reproduced gate failure,
  application behavior, service topology, live Compose execution, deployment,
  provider entitlement mutation, remote branch-protection mutation, tag,
  release, push, and pull request. The later user authorization permits local
  main integration and this feature's cleanup only after verified acceptance.
- Out of scope: secrets, credentials, certificates, user-global provider
  settings, shell history, raw log databases, and edits to preserved archive
  bodies.
- Baseline: local `main` at
  `71da6654e2fa3def174b238ad309c92fe46e9dae`, with cached `origin/main` at
  `4c6d211129615eab372d720ebd209b6c27618c86` and a clean worktree when the
  design was approved.

## Behavior Contract

1. `.github/workflow-contract.yml` is the only executable-composition owner. It
   owns public suite membership, gate nodes, entrypoints, normalized arguments,
   execution context, admitted environment, order, timeout, setup, and job roots.
2. `scripts/manifest.yaml` owns file inventory, kind, mutation capability,
   lifecycle, consumers, tests, disposition, check command, and generated
   outputs. It does not repeat public suite, argv, or execution-context data.
3. One aggregate plan may contain each canonical invocation identity at most
   once. The identity is the resolved repository path, normalized argv, public
   profile, execution context, and explicit semantic mode; two gate IDs cannot
   bypass this constraint.
4. Ambient environment is not the sole discriminator between two semantic
   validation modes. A mode that must execute separately is represented by a
   distinct bounded argv contract; otherwise the duplicate node is removed.
5. The public validation surface is limited to
   `run-ci-gate.py --profile changed`, its `--explain` form, and
   `run-ci-gate.py --profile full`. Provider rendering uses
   `provider_surface_renderer.py --check|--write` directly.
6. CI pre-commit execution continues to skip the two public profile hooks to
   prevent recursive re-entry. The controlled Agent all-files wrapper retains
   its approval, clean-worktree, allowed-prefix, and first-failure boundaries.
7. PostToolUse performs bounded post-edit work. A completion hook owns at most
   one changed aggregate for the same repository state; hooks do not manufacture
   approval, lifecycle state, or runtime evidence.
8. `scripts/lib/<domain>/` contains importable or sourceable domain logic.
   Executable operation and validation entrypoints live under
   `scripts/operations/` and `scripts/validation/` respectively.
9. `tests/lib/<domain>/` verifies library behavior, `tests/validation/` verifies
   CLI and execution context, and `tests/fixtures/` contains test-only synthetic
   input. Production scripts do not read `tests/`.
10. Static fixture files are retained only when the serialized format is itself
    a contract with independent reuse value. Single-field negative variants use
    deterministic table-driven builders.
11. Current document validators accept only the Stage 99 current path and ID
    grammar. Historical path readers are isolated to Git-history, archive, and
    recovery responsibilities and cannot classify current authored documents.
12. Completed target-surface migration snapshots cannot remain current
    validation authorities. Their historical evidence is retired through the
    registered lifecycle after all current consumers are cut over.
13. Stage 00 remains the canonical role, skill, provider, permission, and hook
    owner. Native `.claude/**` and `.codex/**` remain generated adapters.
    Codex reads canonical Stage 00 skills directly. An absent or empty real
    `.agents/` directory is allowed, but shared role/skill/README projections
    and `.codex/skills/` are not restored. Nonempty or unverifiable roots fail
    closed without deleting unknown contents.
14. A manifest transition has a different successor and a bounded removal
    condition. A self-successor cannot justify an indefinite transition state.
15. Local configuration, tests, and generated parity do not prove Hosted CI,
    provider entitlement, remote protection, deployed runtime, cost, or model
    quality.

## Technical Approach

First add negative tests for lifecycle/index disagreement, duplicate canonical
invocations, divided executable ownership, production-to-test fixture access,
legacy current-path admission, and unconsumed provider compatibility output.
Before implementing those contracts, activate this Spec, its Plan, and the
current Task through each registered lifecycle edge in separate reviewed
commits; later Tasks activate only when their predecessor is complete.
Move public suite and invocation data into the workflow contract and reduce the
manifest to inventory metadata. Then cut consumers over before deleting wrappers,
move operation entrypoints and reusable examples to their owning trees, split
mixed tests, isolate historical readers, retire completed migration data, and
regenerate only declared outputs.

Each independently reviewable slice ends with focused tests and a logical
commit. The final aggregate runs only after generated output and links are
fresh. No validator exception, allowlist, threshold reduction, or compatibility
fallback is introduced to make the migration pass.

## Interfaces and Data

- `.github/workflow-contract.yml`: single executable DAG and public suite
  composition document.
- `scripts/lib/gate/ci_gate_contract.py`: bounded contract reader, parser, and
  graph validation.
- `scripts/validation/ci_gate_runner.py`: context derivation, canonical
  invocation identity, plan construction, and verified execution.
- `scripts/manifest.yaml`: non-executable file ownership inventory.
- `scripts/operations/provider_surface_renderer.py`: sole provider projection
  check/write CLI.
- `scripts/lib/document_governance/**`: current document contract plus isolated
  historical identity and archive readers.
- `examples/operations/**`: reusable synthetic operational rehearsal input.
- `tests/lib/**`: library behavior tests and deterministic builders.
- `tests/validation/**`: CLI, entrypoint, execution-context, and aggregate tests.
- `docs/90.references/data/**`: generated or advisory evidence that remains
  current only while a current consumer exists.

The gate runner exposes one canonical identity helper with this contract:

```python
def canonical_invocation_key(
    root: pathlib.Path,
    invocation: GateInvocation,
    *,
    profile: str,
    context: ExecutionContext,
) -> tuple[pathlib.Path, tuple[str, ...], str, str]:
    """Return resolved path, normalized argv, profile, and execution context."""
```

## Failure Modes and Guardrails

- A composition cutover can omit a leaf. Capture the pre-change plan per public
  profile/context and compare the semantic leaf set after removing only the
  approved duplicate and retired migration leaves.
- Two different modes can be collapsed accidentally. Require an explicit argv
  difference and a focused behavior test before admitting two invocations of
  one entrypoint.
- Wrapper deletion can break a tracked consumer. Require zero tracked inbound
  references before deleting each wrapper and update docs, manifest, workflow,
  tests, and generators atomically.
- Fixture movement can change rehearsal defaults. Compare bytes or parsed
  payloads before and after the move and update the operation, test, and runbook
  in one commit.
- Removing legacy grammar can break identity recovery. Keep full-history tests
  separate and prove the current classifier rejects the same legacy path that
  the history reader accepts as preserved evidence.
- Retiring generated data can leave a current link. Run inbound-link, metadata,
  lifecycle, recovery, generated-freshness, and LLM Wiki checks before and after
  the transition. Preserve each registered DATA `README.md` byte for byte in
  Stage 98, record disposition in one sealed package Tombstone, and rely on
  exact Git recovery proof for unregistered generated payloads.
- Provider compatibility removal can affect an external untracked consumer.
  Record that boundary as unverified and retain native Claude/Codex interfaces
  and direct canonical skill loading, not shared projections.
- A broad test split can create duplicate execution. The gate inventory must
  prove every discovered test module is reached once and every production
  responsibility has a focused owner.
- SPEC-0172's completed record is immutable. Its divergent main follow-up must
  not reopen that identity or receive a fabricated terminal status. The approved
  branch-reconciliation rule requires exact source-package preservation and a
  typed Task receipt binding the source and distinct active integration owner.
  Ordinary live packages still require registered lifecycle transitions.

## Acceptance Contract

1. The six public suite names and two public profiles remain unchanged.
2. `validation-changed` and `validation-full` remain the only required quality
   jobs, and the tracked protection contract retains `strict=true` and app ID
   `15368`.
3. Expanding changed/local, changed/pull-request, full/local, full/push, and
   full/workflow-dispatch plans yields no duplicate canonical invocation key.
4. The former duplicate Compose validation and Storybook/Next.js npm bootstrap
   each execute once per aggregate without reducing their semantic coverage.
5. `scripts/manifest.yaml` contains no `public_suites`, `execution_argv`, or
   `execution_contexts` ownership and contains no self-successor transition.
6. `validate-harness.sh`, `run-local-qa-gates.sh`, the two document-link shell
   wrappers, `sync-provider-surfaces.sh`, and the target-surface migration
   subsystem have no tracked current consumer and are absent.
7. All retained public commands have one documented owner, one focused test
   route, and one aggregate route.
8. No production path under `scripts/` reads `tests/` or `tests/fixtures/`.
9. Library and CLI tests follow the documented `tests/lib` and
   `tests/validation` boundary; discovery-only placeholder modules are absent.
10. Sample delivery fixtures contain no completed Spec number, and supply-chain
    negative variants are generated deterministically from retained schema
    goldens.
11. Current document validators reject legacy basenames and abbreviated
    Requirement IDs while full-history identity allocation and archive recovery
    continue to pass.
12. SPEC-0172's completed record remains unchanged. Every file of main's
    divergent follow-up is preserved byte-for-byte under the approved generic
    branch-handoff rule, with a verified Task receipt and obligation transfer.
    SPEC-0174 follows registered transitions and full-package preservation.
    No new Spec/Plan/Task or artifact ID is allocated; no current package is
    dropped solely because Git can recover it.
13. DATA-0068, DATA-0069, DATA-0073, and DATA-0074 leave the current data index
    through registered lifecycle transitions. Their archived `README.md` bodies
    are byte-identical and Tombstones `tomb-DATA-0068`, `tomb-DATA-0069`,
    `tomb-DATA-0073`, and `tomb-DATA-0074` own their disposition without any
    frozen archive body edit.
14. `.agents/agents/**`, `.agents/skills/**`, generated `.agents/README.md`,
    and `.codex/skills/**` are absent. An empty real `.agents/` directory,
    including a read-only one, passes the same library rule in renderer and
    provider validation; native projections match renderer output.
15. Focused tests, script manifest validation, metadata discovery, lifecycle
    discovery, generated checks, `git diff --check`, and the canonical full gate
    pass after all cutovers.
16. Final evidence distinguishes local-executed, configured, repository-enforced,
    unverified runtime, unverified entitlement, and unverified remote state.

## Traceability

- Requirements: REQ-0024 and REQ-0026.
- Architecture: AD-0027 and AD-0030.
- Decisions: ADR-0029 and ADR-0031.
- Execution: SPEC-0173-PLAN-0001 and SPEC-0173-TSK-0001 through
  SPEC-0173-TSK-0006.
- Completed evidence: SPEC-0155, SPEC-0157, SPEC-0159, SPEC-0161, SPEC-0167,
  SPEC-0169, and SPEC-0170.
- Predecessor reconciliation evidence: SPEC-0172.

## Open Questions

No unresolved design choice blocks planning. External consumers of
`.agents/agents/**`, current Hosted CI status, provider entitlement, and remote
branch protection remain observation limits rather than implementation inputs.

## Operational Impact

The planned change reduces local and Hosted validation duplication and makes
rehearsal inputs discoverable outside the test tree. It does not start, stop, or
reconfigure a service. Provider changes are limited to generated repository
adapters and do not assert native runtime acceptance. Rollback is a normal
logical commit revert; no reset, clean, force push, or archive-body rewrite is
part of the plan.

## Related Documents

- [Implementation plan](plan.md)
- [Stage 03 index](../README.md)
- [Workspace governance authority](../../02.architecture/decisions/0029-workspace-governance-authority.md)
- [Document lifecycle architecture](../../02.architecture/descriptions/0030-document-lifecycle-governance.md)
