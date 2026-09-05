---
title: "Governance and QA Surface Convergence Specification"
version: "0.3.4"
type: "sdlc/spec"
status: "active"
owner: "@buenhyden"
updated: "2026-09-06"
layer: "specs"
artifact_id: "SPEC-0173"
parent_ids:
- "REQ-0024"
- "REQ-0026"
- "AD-0027"
- "AD-0030"
- "ADR-0031"
- "ADR-0032"
supersedes:
- "SPEC-0174"
created: "2026-09-05"
---

# Governance and QA Surface Convergence Specification

## Overview

The reviewed governance/QA convergence, canonical `.agents/` relocation,
clean-worktree ownership repair and bounded Python cleanup are integrated on
local main at `8176cdee732954415bc5462d6d4d43da4e319394`. Native Claude/Codex
adapters, Stage 99 machine contracts, executable owners and frozen execution
evidence remain preserved. The existing package remains active: Tasks 0001
through 0005 retain their implementation milestones and Task 0006 remains the
sole ledger for package review and outstanding acceptance evidence.

## Boundaries and Inputs

- Original relocation provenance: local main
  `e5685b42c92039618ae86cca8736b6a425630221`, then clean. Current review
  baseline: local main `8176cdee732954415bc5462d6d4d43da4e319394`;
  `codex/0173-agent-governance-home` points to the same commit.
- In scope: all former governance sources and their direct/indirect consumers,
  provider/core contracts, Registry/schema/templates, hooks, tests, active links,
  navigation, CI selection and affected registered generated outputs.
- The latest explicit user request adopts relocation after suitability review
  and replaces the earlier empty-container/direct-read restriction. It authorizes
  normal scoped approval for protected `.agents` and `.codex` writes.
- Preserve: existing role/skill IDs, permissions/model settings, six suites/two
  profiles, required CI jobs, strict protection contract, Operations identity
  routes, issued-ID high-water and all existing frozen archive bytes.
- Durable-owner promotion remains open because REQ-0026, AD-0030, and accepted
  ADR-0031 still describe transient Plan/Task deletion while canonical policy
  and executable package guards require full-package preservation. Reconcile
  the Requirement and Description only after a bounded design review. Preserve
  ADR-0031's accepted body; changing its decision requires a reviewed successor
  and the applicable reciprocal supersession lifecycle. No successor identity
  or design outcome is selected by this specification update.
- The subsequent user instruction authorizes local commits of the reviewed
  relocation and continued review/execution of safe follow-up verification.
- The reviewed relocation (`6c283d395`), reproducible ownership and Wiki repair
  (`c265bacc5`), evidence checkpoint (`a8c6ede82`), and bounded lint cleanup
  (`8176cdee7`) now form the integrated local baseline. Current authorization
  covers the `8176cdee7` checkpoint and follow-up on the same work branch; it
  does not imply integration of later unreviewed work.
- Out of scope: additional integration, push, PR, fetch/pull, deployment, live
  Compose/service actions, credentials/environment contents, certificates,
  global settings, new servers/plugins, model entitlement and hook trust changes.

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
13. `.agents/governance`, `.agents/roles` and callable `.agents/skills` are the
    canonical common sources. Native provider files remain adapters/mechanics.
    All original governance files have an explicit reviewed disposition. The old
    governance root has no remaining live reader, generator, route or directory.
    Canonical skills have standard native entry metadata and explicit-invocation
    controls; no implicit permission/tool/model expansion is introduced.
14. A manifest transition has a different successor and a bounded removal
    condition. A self-successor cannot justify an indefinite transition state.
15. Local configuration, tests, and generated parity do not prove Hosted CI,
    provider entitlement, remote protection, deployed runtime, cost, or model
    quality.

## Technical Approach

Treat the integrated `8176cdee7` tree as the implemented baseline. Preserve the
reviewed source dispositions, accepted ADR-0032, superseded ADR-0029, provider
source/output boundary, document discovery, link rebasing, hook routing and
test-ownership repair. Further work reconciles the active package and collects
only evidence whose actual inputs are available and authorized.

Canonical skill shape, direct loading and static provider checks have passed;
they do not establish normal native discovery. The whole-migration aggregate
remains blocked by its actual PostgreSQL operating/image leaf. Keep that leaf
selected and record BLOCKED or NOT_RUN until its inputs and execution boundary
permit direct observation. Do not convert focused or synthetic PASS results
into aggregate, native runtime, Hosted CI or remote acceptance.

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
  in one reviewed change set.
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
    No new Spec/Plan/Task is allocated; the successor authority ADR follows its
    own monotonic allocation. No package is dropped solely because Git can recover it.
13. DATA-0068, DATA-0069, DATA-0073, and DATA-0074 leave the current data index
    through registered lifecycle transitions. Their archived `README.md` bodies
    are byte-identical and Tombstones `tomb-DATA-0068`, `tomb-DATA-0069`,
    `tomb-DATA-0073`, and `tomb-DATA-0074` own their disposition without any
    frozen archive body edit.
14. All 77 original common files have a reviewed disposition; `.agents` is the
    sole common authority with 14 unchanged role IDs and 23 explicit-invocation
    skill packages. Native projections are deterministic consumers; old live
    governance paths and `.codex/skills` substitutes are absent.
15. Applicable focused tests, script manifest, metadata/lifecycle discovery,
    generated checks and `git diff --check` pass after cutover. Inspect changed
    selection and run its public gate only with authorized inputs; full is
    conditional on current policy/impact. Required unexecuted checks are
    explicitly BLOCKED or NOT_RUN and are never promoted to an aggregate PASS.
16. Final evidence distinguishes local-executed, configured, repository-enforced,
    unverified runtime, unverified entitlement, and unverified remote state.

## Traceability

- Requirements: REQ-0024 and REQ-0026.
- Architecture: AD-0027 and AD-0030.
- Decisions: ADR-0032 and ADR-0031.
- Execution: SPEC-0173-PLAN-0001 and SPEC-0173-TSK-0001 through
  SPEC-0173-TSK-0006.
- Completed evidence: SPEC-0155, SPEC-0157, SPEC-0159, SPEC-0161, SPEC-0167,
  SPEC-0169, and SPEC-0170.
- Predecessor reconciliation evidence: SPEC-0172.

## Open Questions

Durable-owner promotion has one unresolved design dependency: align REQ-0026
and AD-0030 with canonical full-package preservation and define the reviewed
successor treatment needed to change accepted ADR-0031 without rewriting it.
That design must be approved before those owners or identity allocation change.
Actual PostgreSQL operating/image inputs, normal native startup without
unauthorized auth or global-runtime side effects, Hosted CI, provider
entitlement, and remote branch protection remain separate observation
prerequisites or limits.

## Operational Impact

The implemented relocation preserves integrated gate and fixture ownership and
provides the canonical native skill shape. It does not prove that normal native
startup discovers or invokes those skills, and it does not start, stop or
reconfigure services. Rollback remains a reviewed restoration of the affected
baseline slice; no reset, clean, force push, or archive-body rewrite is part of
the plan.

## Related Documents

- [Implementation plan](plan.md)
- [Stage 03 index](../README.md)
- [Workspace governance authority](../../02.architecture/decisions/0032-canonical-agent-governance-home.md)
- [Document lifecycle architecture](../../02.architecture/descriptions/0030-document-lifecycle-governance.md)
