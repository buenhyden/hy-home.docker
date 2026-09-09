---
title: "Governance and QA Surface Convergence Specification"
version: "0.6.1"
type: "sdlc/spec"
status: "active"
owner: "@buenhyden"
updated: "2026-09-09"
layer: "specs"
artifact_id: "SPEC-0173"
parent_ids:
- "REQ-0024"
- "REQ-0026"
- "AD-0027"
- "AD-0030"
- "ADR-0032"
- "ADR-0033"
supersedes:
- "SPEC-0174"
created: "2026-09-05"
---

# Governance and QA Surface Convergence Specification

## Overview

Converge the remaining governance, QA, workflow, and commit consumers using the
implemented canonical-home migration. Tasks 0001 through 0005 retain their
reviewed implementation evidence; Task 0006 owns this local follow-up and all
remaining package acceptance. Historical checkpoint SHAs in that Task are
provenance, not permanent validation inputs.

## Boundaries and Inputs

- Reuse REQ-0024, REQ-0026, AD-0027, AD-0030, and accepted ADR-0032/0033.
  Full-package preservation is already implemented; ADR-0031 is superseded.
- The 2026-09-08 user request authorizes scoped local source, policy, document,
  configuration, regression, fixture, generated-output changes and logical
  commits. Fetch and authenticated remote reads are authorized observations.
- Inspect the actual fetched main, branch, worktree, index, and working tree;
  record the measured SHA and ownership only in Task 0006. Preserve unrelated
  changes; current Task authorization determines local integration/disposition.
- In scope: `.agents/`, `.claude/`, `.codex/`, `.github/`, `scripts/`, `tests/`,
  connected `evals/`, `examples/`, `_workspace/`, root tool/commit configuration,
  and affected active, working, and historical document consumers. Project-local
  QA is included only where its real package inputs change.
- Preserve the six public suites, two profiles, `validation-changed` required
  status identity, required detection coverage, fail-closed safety boundaries,
  source/generated distinction, and immutable archive bodies.
- Exclude push, PR creation/merge, workflow dispatch, remote settings, releases,
  tags, operational service actions, real secrets, and user-global configuration.
  Unavailable runtime/hosted observations remain separate from local completion.

### Approved option A follow-up

The user's subsequent option A approval narrows the renewed work to current
ownership/path/context prose, prepared-tool preservation in post-edit hooks,
and reuse of the audit generator's validated pack within one invocation.
Task 0006 owns this approval and the current baseline. Preserve public CLI,
suite membership, aggregate composition, native permissions, and frozen bytes.
The legacy graph, historical audit census, active operations template markers,
and cross-domain architecture consolidation are deferred option B candidates.
Task 0006 owns the later explicit local-integration and cleanup approval;
execute that disposition only after verified completion. Remote delivery and
terminal package disposition remain outside this follow-up.

### Approved follow-up: QA and document consolidation

The 2026-09-09 request authorizes review and authoring this Spec, its Plan and
Task 0006. The subsequent explicit answer puts **operations execution planning
on hold**. Neither synthetic runtime rehearsal planning nor service deployment,
restart, recovery or runtime execution is included. Existing configuration-only
and deterministic QA routes remain subjects of review, not operational proof.

Reuse this active package and its existing identities. W16 planning is delivered.
After the W17-W21 review, the user's instruction to inspect the Task and Plan
and proceed authorizes the reviewed implementation scope and logical local
commits. Task 0006 records this approval, the W20 taxonomy-consumer correction,
and execution evidence. W20 starts with the auth pilot and retains the current
owner's semantic-transfer review before each domain retirement. Operations
planning remains on hold. Prior W16 integration/cleanup is complete; it does
not authorize new remote writes or terminal package promotion. The latest
separate user request now prioritizes committing the in-progress snapshot,
local main integration and force cleanup of task-owned branches/worktrees;
Task 0006 owns that disposition and outstanding acceptance. Current nonterminal
metadata remains unchanged.

The approved scope is bounded to the existing public QA graph and its inactive
semantic-parser consumers, audit census and current evidence consumers, active
operations-document authoring residue, and the nine overlapping Stage 02 owner
pairs identified in Task 0006. No new QA registry, wrapper, policy home, document
package, ID, provider runtime experiment or dependency upgrade is proposed.

## Behavior Contract

1. `.github/workflow-contract.yml` is the only executable-composition owner. It
   owns public suite membership, gate nodes, entrypoints, normalized arguments,
   execution context, admitted environment, order, timeout, setup, and suite roots.
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
9. `tests/lib/<domain>/` verifies library behavior and `tests/validation/`
   verifies CLI and execution context. Test-only synthetic input lives in
   underscore-prefixed modules beside the suite that uses it; Task 0004 emptied
   `tests/fixtures/` and the directory is absent. Production scripts do not read
   `tests/`.
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

Use existing owners in place. `.agents/governance/` owns common policy, authored
provider adapters own native loading, the Provider Registry owns translations,
the workflow contract owns execution, the script manifest owns inventory,
Stage 99 owns document shape, and Task 0006 owns evidence.

Prefer correcting these consumers over adding a wrapper or registry. Remove the
standalone tech-stack workflow while retaining its required drift leaf; its
command, inputs, and context duplicate the required validation without measured
additional value. Align root-only hook selection with the public selector, keep
index and working-tree evidence distinct, and fail explicitly when a comparison
base cannot be resolved. Preserve CI pre-commit anti-recursion.

Use `.cz.toml` as the executable commit vocabulary and message-shape owner;
policy explains it, PR identity checks consume it, and other tool-specific
translations have behavioral parity tests. Preserve existing accepted types and
avoid tightening unrelated restrictions. Check and fix remain explicit; no
read-only QA command silently edits source. Update active stale package claims
against their current owners, retaining dated Task and frozen archive evidence.

### Follow-up design

- **QA composition:** preserve the two profiles, six suites and existing public
  CLI. Compare actual expanded invocations by entrypoint, argv, cwd, context,
  configuration and input snapshot. Converge structural validation and public
  expansion on the public suite roots. Migrate every consumer of the obsolete
  job-root composition before removing its nodes;
  reachability from one root set alone is insufficient deletion evidence.
- **Inactive semantic parser:** prefer retiring its unused call graph after
  mapping each skipped safety case to an active projection, DAG or runner test.
  Keep helpers with active callers. If an existing safety intent lacks active
  coverage, add a behavior regression at its actual owner before removal. Do not
  re-enable a general shell interpreter solely to make skipped tests execute.
- **Census:** preserve stable audit criterion identity/schema completeness and
  frozen migration provenance. Current corpus membership, profile coverage and
  ownership come from tracked paths, Stage 99 and lifecycle records. Remove
  copied current-count assertions and stale current prose; derive display totals
  from the validated owner. Never derive the expected criterion set from the
  same possibly incomplete input being checked. Changing that stable set or
  retention policy is outside this proposal.
- **Operations-document residue:** remove obsolete authoring markers from
  reviewed active target documents while preserving procedures, IDs and valid
  examples. Keep the existing target-residue check; do not relax it to accept
  current debt. Stage 98 frozen bodies are not cleanup targets.
- **Architecture ownership:** consolidate each overlapping pair into its
  established base Description after clause-level comparison. Preserve distinct
  security, data, topology and hardening decisions, and route procedural details
  to their existing Stage 05 subject. A genuinely distinct capability may keep
  a separate explicitly scoped owner only after review proves that split. Do
  not merge all domains into one document or invent service behavior.
- **Lifecycle:** migrate active links, labels, full IDs, indexes and consumers
  with each domain change. Preserve source artifact IDs and use the registered
  supersession/archive/recovery transition only after semantic transfer is
  complete. Existing frozen bytes and historical identity readers remain intact.

Task 0006 owns the dated census and disposition inventory. Counts and baseline
SHAs in that inventory are observations, not future gate constants. Durable QA
behavior belongs to AD-0027 and the existing executable owners; document
ownership and preservation belong to REQ-0026, AD-0030 and Stage 99.

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

Criteria 1-24 retain the existing contract. Criterion 25 is the authorized W16
planning deliverable; criteria 26-30 cover the newly approved W17-W21 work and
remain NOT_RUN until verified. This continuation grants no new main integration,
remote write or runtime authority. Keep the numbered criteria in one continuous list so formatting
preserves the Plan and Task references.

1. The six public suite names and two public profiles remain unchanged.
2. `validation-changed` and `validation-full` remain the quality jobs for PR
   and push/manual respectively. Only `validation-changed` is the desired PR
   required status context, with `strict=true` and app ID `15368`.
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
14. The original migration dispositions remain historical Task evidence;
    `.agents` is the sole common authority with registered roles and explicit
    skill packages. Native projections are deterministic consumers; old live
    governance paths and `.codex/skills` substitutes are absent.
15. Applicable focused tests, script manifest, metadata/lifecycle discovery,
    generated checks and `git diff --check` pass after cutover. Inspect changed
    selection and run its public gate only with authorized inputs; full is
    conditional on current policy/impact. Required unexecuted checks are
    explicitly BLOCKED or NOT_RUN and are never promoted to an aggregate PASS.
16. Final evidence distinguishes local-executed, configured, repository-enforced,
    unverified runtime, unverified entitlement, and unverified remote state.

17. Root-only tool/commit configuration reaches public validation. Selector
    regressions cover staged/unstaged/partial snapshots, rename/delete/add,
    spaces, empty diff, initial commits, and unavailable/shallow base history.
18. Commit hook, lightweight message check, PR title/branch, examples, and
    release/changelog translations agree on accepted type and message behavior.
19. Tech-stack drift remains required after duplicate workflow removal; workflow,
    contract, checker, tests, consumers, and active docs transition together.
20. Local checks report actual exit/context/inputs and keep source bytes intact;
    hosted jobs, managed automation, and deployment are separate evidence.
21. Native edit payloads share pre/post path and replacement extraction: physical
    in-root Claude absolute paths work; Codex multi-file patches reach all file
    rules and checks; external/symlink paths and malformed edits fail closed.
    Project permissions contain no arbitrary Git/Python allow grant, and Stop
    retry handling remains bounded. Static tests do not imply live delivery.

22. Post-edit validation preserves the explicitly prepared tool search order;
    it does not automatically promote user-global tools over that environment.
    Explicit bootstrap remains separate from source-preserving check execution.
23. The audit matrix generator reuses the pack already validated by its semantic
    check, while malformed input, semantic failure and stale output still fail.
    The standalone validators and public aggregate remain behaviorally intact.
24. Current provider, ownership, changelog and metadata-base guidance each matches
    its executable owner. Registered generated text uses current document paths;
    new remote observations retain their actual SHA and event.

25. The Spec, Plan and Task identify confirmed findings versus candidates,
    compare alternatives, name owners, dependencies, checks and recovery, and
    record the operations-planning hold. Existing IDs, historical receipts and
    nonterminal lifecycle states remain intact. This is the current planning
    deliverable; it does not establish implementation approval or completion.
26. After approval, public plans retain their required semantic leaf coverage
    without duplicate invocation identities. Removed legacy nodes and inactive
    parser helpers have no active caller; each formerly skipped safety intent
    has an active negative test or a reviewed explanation that its syntax is
    rejected at the current boundary. Missing/cyclic/unsafe contracts still fail.
27. After approval, current corpus checks derive coverage from canonical owners
    without historical counts as current acceptance. Stable criterion omission,
    duplicate IDs, invalid schema, stale output and corrupt recovery evidence
    still fail. Dated audit facts are distinguished from current observations.
28. After approval, the reviewed active operations-document scope has no obsolete
    authoring residue; valid examples, procedure content, IDs and frozen archive
    bytes remain intact. Metadata report generation is not claimed as its source.
29. After approval, every reviewed architecture capability has an unambiguous
    owner and a source-clause-to-destination mapping. Unique obligations are
    preserved before supersession; active links and generated navigation resolve
    to the retained owner, with registered archive and recovery evidence.
30. After approval, each coherent implementation unit has relevant regression,
    exact diff review and normal-hook commit evidence. Final local validation
    names its snapshot and context; hosted, provider and operations observations
    remain separate. Unmeasured savings and held runtime plans are never PASS.

## Traceability

- Requirements: REQ-0024 and REQ-0026.
- Architecture: AD-0027 and AD-0030.
- Decisions: ADR-0032 and ADR-0033; ADR-0031 is superseded evidence.
- Execution: SPEC-0173-PLAN-0001 and SPEC-0173-TSK-0001 through
  SPEC-0173-TSK-0006.
- Completed evidence: SPEC-0155, SPEC-0157, SPEC-0159, SPEC-0161, SPEC-0167,
  SPEC-0169, and SPEC-0170.
- Predecessor reconciliation evidence: SPEC-0172.

## Open Questions

Normal native hook delivery, provider entitlement, and hosted verification of
new local commits require their actual execution evidence. Local permission and
available tool inputs determine which validation routes can run; absent inputs
are NOT-RUN or BLOCKED, never inferred PASS. These are separate observations;
they do not add live execution requirements to the numbered acceptance contract.
Local completion and authorized local integration use their applicable evidence.
Terminal package disposition separately follows the registered lifecycle rules.

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
