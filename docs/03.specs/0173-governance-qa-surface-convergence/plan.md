---
title: "Governance and QA Surface Convergence Implementation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "active"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "specs"
artifact_id: "SPEC-0173-PLAN-0001"
parent_ids:
- "SPEC-0173"
created: "2026-09-05"
---

# Governance and QA Surface Convergence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Converge the repository's gate, script, test, fixture, document, and
provider surfaces around current owners while removing completed migration and
compatibility residue without weakening validation.

**Architecture:** `.github/workflow-contract.yml` becomes the single executable
DAG owner, while `scripts/manifest.yaml` remains a non-executable ownership
inventory. Current document and provider adapters remain projections from Stage
99 and Stage 00; historical readers and retired evidence are isolated from
current validation.

**Tech Stack:** Python 3 standard library and PyYAML, Bash, JSON/YAML contracts,
`unittest`, Git, Docker Compose structural validation, pre-commit, and the
repository's Stage 00/03/90/98/99 document governance.

**Spec:** `docs/03.specs/0173-governance-qa-surface-convergence/spec.md`

## Objective

- Keep public profiles exactly `changed` and `full` and public suites exactly
  `agent-governance`, `document-contract`, `document-graph`,
  `document-lifecycle`, `operations`, and `repository-integrity`.
- Keep GitHub job names `validation-changed` and `validation-full`; preserve the
  tracked `strict=true` and GitHub Actions app ID `15368` protection contract.
- Do not add dependencies, validator exceptions, threshold reductions,
  migration allowlists, compatibility fallbacks, or new parallel registries.
- Do not edit a body under `docs/98.archive/{completed,superseded,retired}/`.
- When a current artifact is retired, preserve its registered body byte for
  byte, record the disposition in one package Tombstone, and do not rewrite
  frontmatter before the archive move.
- Preserve issued identity high-water and historical Git/archive recovery.
- Do not read secrets, credentials, certificates, user-global provider state,
  shell history, or raw log databases.
- Do not run Compose services, deploy, mutate provider entitlement or remote
  protection, push, open a PR, merge, tag, or release under this plan.
- Production code must not read `tests/` after Task 4.
- Every deletion follows a tracked-consumer cutover and a zero-inbound-reference
  check in the same Task.
- Each Task starts RED, reaches focused GREEN, records a logical commit, and is
  independently reviewable before the next Task begins.
- Implementation requires a separate execution approval; this planning package
  does not authorize its own execution.
- Before Task 1 implementation, advance SPEC-0173, this Plan, and Task 1 only
  through valid Registry lifecycle edges. Later Tasks remain draft until their
  predecessor is complete and they are ready to execute.

---

### Success Criteria

Deliver six bounded changes: reconcile the predecessor lifecycle, establish one
typed executable owner, remove obsolete script and operation routes, align tests
and fixtures, retire current document/provider residue, then regenerate and
validate the resulting repository once.

## Dependencies

- REQ-0024, AD-0027, and ADR-0029 own agent-governance source/projection
  separation.
- REQ-0026, AD-0030, and ADR-0031 own lifecycle, retirement, recovery, and
  frozen archive behavior.
- SPEC-0155, SPEC-0157, SPEC-0159, SPEC-0161, SPEC-0167, SPEC-0169, and
  SPEC-0170 are historical evidence of promised outcomes, not current authority.
- SPEC-0172 supplies the predecessor execution record whose lifecycle must be
  reconciled before its completed Spec can leave the current Stage 03 index.
- The approved audit baseline is local `main` at
  `71da6654e2fa3def174b238ad309c92fe46e9dae`; a new baseline is captured at
  execution time rather than reusing that SHA as a permanent invariant.
- `docs/99.templates/registry.json` owns profile, path, identity, lifecycle, and
  section grammar. `.github/workflow-contract.yml` owns the current gate graph.

### File Structure

| Responsibility | Resulting owner | Main change |
| --- | --- | --- |
| Executable gate DAG | `.github/workflow-contract.yml` | Own suites, nodes, argv, context, order, environment, timeout, roots |
| Gate parser and execution | `scripts/lib/gate/**`, `scripts/validation/ci_gate_runner.py` | Reject duplicate canonical invocation identities |
| Script inventory | `scripts/manifest.yaml` | Retain file/lifecycle/consumer/test/output data only |
| Public validation CLI | `scripts/validation/run-ci-gate.py` | Remain the only changed/full entrypoint |
| Provider projection | `scripts/operations/provider_surface_renderer.py` | Own direct check/write interface |
| Operation entrypoints | `scripts/operations/**` | Own rehearsal/runtime-facing commands |
| Operation examples | `examples/operations/**` | Own reusable synthetic rehearsal input |
| Library tests | `tests/lib/<domain>/**` | Test importable/sourceable domain behavior |
| CLI/context tests | `tests/validation/**` | Test entrypoints and aggregate routing |
| Historical document evidence | Stage 98 and isolated history readers | Never classify current authored documents |
| Current execution evidence | SPEC-0173 Task documents | Record actual commands only during execution |

## Execution Sequence

### Execution activation

Commit the planning package on the approved feature branch, create the isolated
worktree, and require a clean full-gate baseline before lifecycle activation.
Then record these valid Registry transitions as three reviewable commits:

```text
Commit A: Spec draft→review; Plan draft→approved; Task 1 draft→ready
Commit B: Spec review→approved; Plan remains approved
Commit C: Spec approved→active; Plan approved→active; Task 1 ready→in-progress
```

Use these commit subjects:

```text
docs(spec): record governance QA convergence review
docs(spec): approve governance QA convergence
docs(spec): activate governance QA convergence
```

Before each commit, run `check-document-metadata.py --mode check-changed
--base-ref HEAD`, the canonical lifecycle checker, the focused Spec-package
test, and `git diff --check`. Do not activate Tasks 2 through 6 early: advance
each Task through `draft→ready→in-progress` only after its predecessor's Plan
steps, focused checks, independent review, and logical commit are complete.
Active-stage occupancy forbids a terminal Task in current Stage 03, so record
intermediate completion in the Plan checklist and Task evidence; keep those
Task frontmatter states `in-progress` until the package's atomic terminal
disposition.

### Task 1: Reconcile lifecycle state and establish RED contracts

**Files:**

- Modify: `.github/rulesets/main-protection.md`
- Modify: `docs/00.agent-governance/policies/documentation-protocol.md`
- Modify: `docs/01.requirements/0026-document-retention-and-retirement.md`
- Modify: `docs/02.architecture/descriptions/0030-document-lifecycle-governance.md`
- Modify: `docs/02.architecture/decisions/0031-preserved-archive-record.md`
- Modify: `docs/03.specs/README.md`
- Modify then preserve: `docs/03.specs/0172-document-contract-convergence/spec.md`
- Remove after recovery proof: `docs/03.specs/0172-document-contract-convergence/plan.md`
- Remove after recovery proof: `docs/03.specs/0172-document-contract-convergence/tasks/tsk-0001-document-contract-convergence.md`
- Create by move: `docs/98.archive/completed/03.specs/0172-document-contract-convergence/spec.md`
- Modify: `docs/98.archive/README.md`
- Modify: the exact RES-0002, RES-0084, and RES-0085 consumers of SPEC-0172 evidence
- Regenerate: `docs/90.references/data/0076-llm-wiki-stage-category-coverage/README.md`
- Regenerate: `docs/90.references/data/0082-llm-wiki-index/README.md`
- Modify: `scripts/lib/document_governance/spec_packages.py`
- Modify: `tests/lib/document_governance/test_spec_packages.py`
- Verify: `tests/lib/document_governance/test_archive.py`
- Verify: `tests/lib/document_governance/test_identity_history.py`
- Update evidence: `docs/03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0001-lifecycle-and-red-contracts.md`

**Interfaces:**

- Consumes: Registry `spec`, `plan`, and `task` lifecycle graphs; Git regular
  blobs; current Stage 03 index.
- Produces: a completed SPEC-0172 outcome Spec in Stage 98, recoverable transient
  Plan/Task history, and RED tests used by Tasks 2 through 5.

- [x] **Step 1: Capture a fresh execution baseline**

Run:

```bash
git status --short --branch
git rev-parse HEAD
git rev-parse main
git rev-parse origin/main
git rev-list --left-right --count origin/main...main
git worktree list --porcelain
git stash list
python3 scripts/validation/run-ci-gate.py --profile full
```

Expected: clean worktree, exact SHAs recorded in Task 1, and full exit `0`. If
the tree is not clean or full fails, record the pre-existing condition and stop
without changing lifecycle state.

- [x] **Step 2: Add a failing index/frontmatter agreement test**

Add this helper and assertion to
`tests/lib/document_governance/test_spec_packages.py` using the file's existing
frontmatter loader:

```python
def current_spec_rows(index_text: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in index_text.splitlines():
        if line.startswith("| SPEC-"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            rows[cells[0]] = cells[2]
    return rows


def test_current_index_does_not_claim_active_for_draft_spec(self) -> None:
    rows = current_spec_rows((ROOT / "docs/03.specs/README.md").read_text())
    metadata = load_frontmatter(
        ROOT / "docs/03.specs/0172-document-contract-convergence/spec.md"
    )
    self.assertFalse(metadata["status"] == "draft" and "active" in rows["SPEC-0172"])
```

- [x] **Step 3: Run the lifecycle test and verify RED**

Run:

```bash
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_spec_packages -v
```

Expected: FAIL identifying `SPEC-0172` as draft while the index claims active.

- [x] **Step 4: Record and commit each valid forward transition**

Use only registered transitions and keep the package in the current tree until
its terminal move:

```text
Commit A: Spec draft→review; Plan draft→approved; Task draft→ready
Commit B: Spec review→approved; Plan and Task remain approved/ready
Commit C: Spec approved→active; Plan approved→active; Task ready→in-progress
```

For each commit, run:

```bash
PYTHONPATH=. python3 -m unittest discover -s tests/validation/lifecycle -p 'test_*.py'
python3 scripts/validation/check-document-corpus-lifecycle.py
```

Expected: exit `0` at every intermediate state. Do not combine a missing edge
into one commit. There is no standalone terminal-state commit: the corpus
lifecycle rejects terminal documents that remain in current Stage 03, so the
terminal Spec transition and preservation occur atomically in Step 6.

- [x] **Step 5: Prove transient Plan and Task recovery before removal**

Run exact blob checks from the active-state `HEAD` produced by Commit C:

```bash
git ls-tree -r --name-only HEAD -- docs/03.specs/0172-document-contract-convergence
git cat-file -e HEAD:docs/03.specs/0172-document-contract-convergence/plan.md
git cat-file -e HEAD:docs/03.specs/0172-document-contract-convergence/tasks/tsk-0001-document-contract-convergence.md
rg -n '0172-document-contract-convergence/(plan|tasks/)' --glob '!docs/98.archive/**' .
```

Expected: both blobs are regular and recoverable; current inbound references are
limited to indexes or documents being updated in this same step.

- [x] **Step 6: Preserve the completed Spec and remove transient execution bodies**

In one atomic patch, transition `spec.md` from `active` to `completed` and move
it to
`docs/98.archive/completed/03.specs/0172-document-contract-convergence/spec.md`.
Remove the current active `plan.md` and Task after Step 5 succeeds; their exact
regular blobs remain recoverable from the Step 5 commit. Transfer the live
RES-0085 identity-recovery decision tuple to SPEC-0173 Task 1, update every
current inbound consumer, and update the Stage 03 and Stage 98 indexes to link
the completed Spec without creating redirect files or copying transient bodies
into the archive.

Correct the stale Stage 00 sentence that requires terminal Task bodies to be
preserved so it agrees with the current Stage 03 and Registry
`transient-after-completion` contract. Add a focused assertion that Stage 00,
Stage 03, and the Registry describe the same terminal Plan/Task disposition.
This Stage 00 policy change requires independent rules-engineer review.

- [x] **Step 7: Run focused lifecycle, archive, and recovery GREEN checks**

Run:

```bash
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_spec_packages -v
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_archive -v
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_identity_history -v
PYTHONPATH=. python3 -m unittest discover -s tests/validation/lifecycle -p 'test_*.py'
python3 scripts/validation/check-document-corpus-lifecycle.py
```

Expected: PASS with SPEC-0172 absent from current packages and recoverable from
its preserved Spec plus Git history.

- [x] **Step 8: Commit the reconciled predecessor**

After the transition commits above, create the terminal preservation commit:

```bash
git add .github/rulesets/main-protection.md \
  docs/00.agent-governance/policies/documentation-protocol.md \
  docs/01.requirements/0026-document-retention-and-retirement.md \
  docs/02.architecture/descriptions/0030-document-lifecycle-governance.md \
  docs/02.architecture/decisions/0031-preserved-archive-record.md \
  docs/03.specs/README.md \
  docs/03.specs/0172-document-contract-convergence \
  docs/03.specs/0173-governance-qa-surface-convergence/plan.md \
  docs/03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0001-lifecycle-and-red-contracts.md \
  docs/90.references/data/0076-llm-wiki-stage-category-coverage/README.md \
  docs/90.references/data/0082-llm-wiki-index/README.md \
  docs/90.references/research/0002-agentic-engineering-research-pack/README.md \
  docs/90.references/research/0084-github-actions-platform \
  docs/90.references/research/0085-workspace-engineering-main-baseline-assessment \
  docs/98.archive/README.md \
  docs/98.archive/completed/03.specs/0172-document-contract-convergence/spec.md \
  scripts/lib/document_governance/spec_packages.py \
  tests/lib/document_governance/test_spec_packages.py
git commit -m "docs(spec): preserve completed document convergence"
```

### Task 2: Converge executable gate composition

**Files:**

- Modify: `.github/workflow-contract.yml`
- Modify: `scripts/lib/gate/ci_gate_contract.py`
- Modify: `scripts/lib/gate/github_workflow_contract.py`
- Modify: `scripts/validation/ci_gate_runner.py`
- Modify: `scripts/manifest.yaml`
- Delete after cutover: `scripts/lib/document_governance/suite_registry.py`
- Modify: `tests/validation/test_ci_gate_runner.py`
- Modify: `tests/lib/gate/test_ci_gate_contract.py`
- Modify: `tests/lib/gate/test_github_workflow_contract.py`
- Modify: `tests/validation/test_script_manifest.py`
- Modify: `tests/lib/test_surface_ownership.py`
- Update evidence: `docs/03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0002-gate-composition-convergence.md`

**Interfaces:**

- Consumes: six suite names and two public profiles from the Spec; current
  `GateNode`, `GateRegistry`, and `GateInvocation` contracts.
- Produces: `canonical_invocation_key(...)`, a workflow-contract-owned public
  suite registry, and duplicate-free public plans.

- [x] **Step 1: Add a helper that builds every public plan without execution**

In `tests/validation/test_ci_gate_runner.py`, add:

```python
def build_public_plan(profile: str, context: runner.ExecutionContext):
    root = ROOT
    document = runner.load_contract_document(root)
    registry = runner.parse_gate_registry(document, ".github/workflow-contract.yml")
    public_contract = runner.parse_public_gate_contract(document)
    suites = runner.select_public_suites(public_contract, profile, ())
    roots = runner.public_root_gate_ids(public_contract, suites)
    return runner.build_public_validation_plan(
        registry, roots, suites, context, profile=profile
    )
```

Update the production signatures in the same Task so the workflow contract,
not a manifest-derived suite model, is passed to plan construction.

- [x] **Step 2: Add the failing canonical invocation uniqueness test**

```python
def test_every_public_plan_has_unique_canonical_invocations(self) -> None:
    cases = (
        ("changed", runner.ExecutionContext.LOCAL),
        ("changed", runner.ExecutionContext.PULL_REQUEST),
        ("full", runner.ExecutionContext.LOCAL),
        ("full", runner.ExecutionContext.PUSH),
        ("full", runner.ExecutionContext.WORKFLOW_DISPATCH),
    )
    for profile, context in cases:
        plan = build_public_plan(profile, context)
        keys = [
            runner.canonical_invocation_key(
                ROOT, item, profile=profile, context=context
            )
            for item in plan
        ]
        self.assertEqual(len(keys), len(set(keys)), (profile, context))
```

- [x] **Step 3: Verify RED against the two measured duplicates**

Run:

```bash
PYTHONPATH=. python3 -m unittest tests.validation.test_ci_gate_runner.CiGateRunnerContractTests.test_every_public_plan_has_unique_canonical_invocations -v
```

Expected: FAIL for Compose under full/local and for `npm ci --prefix
projects/storybook/nextjs` under pull-request/push/workflow-dispatch plans.

- [x] **Step 4: Move public suite composition into the workflow contract**

Make `public_gate` in `.github/workflow-contract.yml` own, for every validator:

```json
{
  "suite": "document-graph",
  "gate_id": "leaf.document-links",
  "entrypoint": "scripts/validation/check-document-links.py",
  "argv": ["--mode", "all"],
  "contexts": ["local", "pull_request", "push", "workflow_dispatch"]
}
```

Extend the existing bounded JSON parser and schema checks rather than adding a
second file. Remove `public_suites`, `execution_argv`, and
`execution_contexts` from all manifest rows. Make the manifest validator reject
those keys so executable ownership cannot drift back.

- [x] **Step 5: Implement canonical invocation identity and rejection**

Add to `scripts/validation/ci_gate_runner.py`:

```python
def canonical_invocation_key(
    root: pathlib.Path,
    invocation: GateInvocation,
    *,
    profile: str,
    context: ExecutionContext,
) -> tuple[pathlib.Path, tuple[str, ...], str, str]:
    resolved = (root / invocation.entrypoint).resolve(strict=True)
    return resolved, tuple(invocation.argv), profile, context.value
```

After plan construction, collect keys and raise
`GateContractError("ci-gate-invocation-duplicate", gate_id, message)` when two
gate IDs produce one key. Keep the diagnostic value stable in focused tests.

- [x] **Step 6: Remove the duplicate Compose aggregate path**

The current no-argument Compose validator already validates every declared
profile independently. Keep one `leaf.compose-validation` invocation and remove
`ci.compose-all-profiles-validation`, `leaf.compose-all-profiles-validation`,
and `local.compose-all-profiles-validation`. Remove the retired
`local-harness`, `local-script-backed`, and `local-all-profiles` profile-root
grammar after all callers use public `changed|full`.

Do not set `HYHOME_COMPOSE_PROFILES` in full. The existing no-environment route
continues to enumerate every declared profile.

- [x] **Step 7: Share the frontend dependency setup node**

Replace `setup.frontend-node-dependencies` and
`setup.storybook-node-dependencies` with one setup node whose single command is:

```text
scripts/lib/gate/ci_gate_adapters.py run-npm ci --prefix projects/storybook/nextjs
```

Point both frontend and Storybook aggregates at that node. DAG expansion must
emit the shared node once by gate ID and once by canonical invocation identity.

- [x] **Step 8: Remove the manifest-backed suite parser**

Move reusable bounded parsing into `scripts/lib/gate/ci_gate_contract.py`, update
imports, and delete `scripts/lib/document_governance/suite_registry.py` only
after `rg -n 'document_governance.*suite_registry|load_public_suite_registry'`
returns no current consumer.

- [x] **Step 9: Run focused GREEN tests and inspect all plans**

Run:

```bash
PYTHONPATH=. python3 -m unittest tests.lib.gate.test_ci_gate_contract -v
PYTHONPATH=. python3 -m unittest tests.validation.test_ci_gate_runner -v
PYTHONPATH=. python3 -m unittest tests.lib.gate.test_github_workflow_contract -v
PYTHONPATH=. python3 -m unittest tests.validation.test_script_manifest -v
python3 scripts/validation/run-ci-gate.py --profile changed --explain
python3 scripts/validation/run-ci-gate.py --profile full --explain
```

Expected: all tests PASS; the five context plans have zero duplicate canonical
keys; the six suite names and two public profiles are unchanged.

- [ ] **Step 10: Commit the gate cutover**

```bash
git add .github/workflow-contract.yml scripts/lib/gate scripts/validation/ci_gate_runner.py scripts/manifest.yaml tests
git commit -m "refactor(gate): converge executable composition"
```

### Task 3: Align script and operation ownership

**Files:**

- Delete: `scripts/validation/check-doc-implementation-alignment.sh`
- Delete: `scripts/validation/check-doc-traceability.sh`
- Delete: `scripts/validation/run-local-qa-gates.sh`
- Delete: `scripts/lib/ops/validate-harness.sh`
- Delete: `scripts/lib/target_surface/target_surface_contract.py`
- Delete: `scripts/lib/target_surface/target_surface_delta_contract.py`
- Delete: `scripts/validation/check-target-surface-contract.py`
- Delete: `scripts/validation/check-target-surface-delta-contract.py`
- Move: `scripts/lib/ops/rehearse-postgres-logical-upgrade.sh` to `scripts/operations/rehearse-postgres-logical-upgrade.sh`
- Move: `scripts/validation/compose-core-readiness.lib.sh` to `scripts/lib/ops/compose-core-readiness.sh`
- Move and rename: `scripts/validation/run-compose-core-readiness.sh` to `scripts/operations/check-compose-core-readiness.sh`
- Merge then delete: `scripts/validation/report-audit-pack-coverage.sh`
- Modify: `scripts/validation/generate-audit-implementation-matrix.sh`
- Modify: `scripts/validation/check-script-manifest.py`
- Modify: `scripts/manifest.yaml`
- Modify: `scripts/README.md`, `.github/repository-surface.md`, and tracked callers
- Modify: focused entrypoint, manifest, operation, and document-link tests
- Update evidence: `docs/03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0003-script-and-operation-ownership.md`

**Interfaces:**

- Consumes: Task 2 workflow-owned suite and invocation records.
- Produces: one direct document-link validator, one typed public gate CLI,
  purpose-owned operation entrypoints, and a manifest with bounded transitions.

- [ ] **Step 1: Add manifest tests for bounded transitions and consumers**

Add to `tests/validation/test_script_manifest.py`:

```python
def test_transition_successor_is_distinct(self) -> None:
    for row in load_manifest_rows():
        if row["lifecycle"] == "transition":
            self.assertNotEqual(row["path"], row.get("successor"), row["path"])


def test_retained_public_entrypoint_has_current_consumer(self) -> None:
    for row in load_manifest_rows():
        if row["kind"] in {"validator", "runner", "operations"}:
            if row["disposition"] == "retain":
                self.assertTrue(row["consumers"], row["path"])
```

- [ ] **Step 2: Run the manifest tests and verify RED**

Run:

```bash
PYTHONPATH=. python3 -m unittest tests.validation.test_script_manifest -v
```

Expected: FAIL for the measured self-successors and consumerless retained or
transition entrypoints.

- [ ] **Step 3: Cut document-link consumers to one validator**

Replace every current call of either shell wrapper with:

```bash
python3 scripts/validation/check-document-links.py --mode all
```

Remove the two wrapper rows and duplicate document-graph gate nodes only after:

```bash
rg -n 'check-doc-(implementation-alignment|traceability)\.sh' --glob '!docs/98.archive/**' .
```

returns no current consumer.

- [ ] **Step 4: Remove obsolete local and harness dispatchers**

Replace current `run-local-qa-gates.sh` callers with `run-ci-gate.py` and replace
`--explain` callers with the typed CLI's own `--explain`. Delete
`validate-harness.sh` instead of restoring the removed `--harness` profile.

Expected public commands after cutover:

```bash
python3 scripts/validation/run-ci-gate.py --profile changed
python3 scripts/validation/run-ci-gate.py --profile changed --explain
python3 scripts/validation/run-ci-gate.py --profile full
```

- [ ] **Step 5: Retire the target-surface executable subsystem**

Delete the target-surface libraries, CLI wrappers, workflow nodes, manifest
rows, and focused tests after Task 2 covers current invocation ownership and
the Stage 99 metadata/lifecycle validators cover current documents. Keep no
redirect wrapper or compatibility import.

- [ ] **Step 6: Move operation entrypoints out of library and validation trees**

Move the PostgreSQL rehearsal and Compose readiness files to the paths listed
above. Update script-relative root resolution, runbooks, manifest entries, and
tests atomically. Register the PostgreSQL public operation check with explicit
argv `--check-config-only`; no runtime mode runs from a validation aggregate.

- [ ] **Step 7: Merge audit coverage into the matrix check**

Move the current coverage predicate from `report-audit-pack-coverage.sh` into
`generate-audit-implementation-matrix.sh --check`. Keep a single generated
output owner and remove the standalone report wrapper, manifest row, and gate
leaf.

- [ ] **Step 8: Resolve every remaining manifest disposition**

For each former self-successor row, choose exactly one result:

- `active + retain` when the current path is the final interface;
- a distinct successor plus a tracked removal condition during this Task; or
- deletion after consumer cutover.

No manifest row may remain `transition` solely because earlier Specs used that
label.

- [ ] **Step 9: Run focused GREEN checks**

Run:

```bash
python3 scripts/validation/check-script-manifest.py
PYTHONPATH=. python3 -m unittest tests.validation.test_script_manifest -v
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_links -v
PYTHONPATH=. python3 -m unittest tests.validation.test_validator_entrypoints -v
bash -n scripts/operations/rehearse-postgres-logical-upgrade.sh
bash -n scripts/operations/check-compose-core-readiness.sh
python3 scripts/validation/run-ci-gate.py --profile changed --explain
```

Expected: PASS and zero current inbound references to deleted entrypoints.

- [ ] **Step 10: Commit the script ownership change**

```bash
git add scripts .github tests docs/05.operations
git commit -m "refactor(scripts): align current command ownership"
```

### Task 4: Converge test placement and fixture ownership

**Files:**

- Move CLI cases from `tests/lib/document_governance/metadata/test_identity.py` to `tests/validation/test_document_metadata_identity_cli.py`
- Split: `tests/validation/test_ci_gate_runner.py` into model, plan, and execution-context modules where responsibilities already have separate production owners
- Split: `tests/validation/test_supply_chain_policy.py` into policy, wrapper, and secure-output modules
- Split: `tests/validation/test_script_manifest.py` into current inventory and historical migration tests, then delete the completed-migration portion after Task 5 cutover
- Move: `tests/lib/ops/test_postgres_logical_upgrade_rehearsal.py` to `tests/validation/test_postgres_logical_upgrade_rehearsal.py`
- Delete: `tests/validation/lifecycle/test_promoted.py`
- Create: `tests/lib/supply_chain/_fixtures.py`
- Create: `tests/validation/_sample_delivery_fixtures.py`
- Move: `tests/fixtures/compose-core-readiness/**` to `examples/operations/compose-core-readiness/**`
- Move: `tests/fixtures/postgres-logical-upgrade/**` to `examples/operations/postgres-logical-upgrade/**`
- Move and rename retained sample-delivery goldens to `examples/operations/sample-service-delivery/**`
- Move retained external supply-chain schema goldens to `examples/operations/supply-chain/**`
- Delete after replacement: `tests/fixtures/agentic-audit/task-evidence.md`
- Modify: every production and test consumer of these paths
- Update evidence: `docs/03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0004-test-and-fixture-convergence.md`

**Interfaces:**

- Consumes: purpose-owned entrypoints from Task 3 and the test layout contract
  in `tests/README.md`.
- Produces: test-only builders, operation-owned examples, focused test modules,
  and a zero production-to-tests dependency invariant.

- [ ] **Step 1: Add a failing production-to-tests dependency test**

Add to the current inventory test module:

```python
def test_production_scripts_do_not_reference_tests_tree(self) -> None:
    violations: list[str] = []
    for path in sorted((ROOT / "scripts").rglob("*")):
        if path.is_file() and path.suffix in {".py", ".sh"}:
            text = path.read_text(encoding="utf-8")
            if "tests/fixtures/" in text or 'ROOT / "tests"' in text:
                violations.append(path.relative_to(ROOT).as_posix())
    self.assertEqual([], violations)
```

- [ ] **Step 2: Verify RED lists the four measured production consumers**

Run:

```bash
PYTHONPATH=. python3 -m unittest tests.validation.test_script_manifest -v
```

Expected: FAIL naming supply-chain, Compose readiness, PostgreSQL rehearsal, and
sample-service delivery consumers.

- [ ] **Step 3: Create deterministic supply-chain fixture builders**

In `tests/lib/supply_chain/_fixtures.py`, define one pure builder per external
shape. For example:

```python
def grype_report(*, severity: str = "Low", exception_expires: str | None = None) -> dict[str, object]:
    match: dict[str, object] = {
        "vulnerability": {"id": "CVE-2099-0001", "severity": severity},
        "artifact": {"name": "sample", "version": "1.0.0"},
    }
    if exception_expires is not None:
        match["matchDetails"] = [{"searchedBy": {"exception_expires": exception_expires}}]
    return {"matches": [match]}
```

Retain one readable golden for each serialized external contract actually parsed:
CycloneDX, in-toto provenance, Cosign verification, Grype, and Scorecard. Build
single-field valid/invalid variants in temporary directories.

- [ ] **Step 4: Remove completed Spec identity from sample fixtures**

Rename retained files to generic names:

```text
verdict.baseline.accepted.json
verdict.candidate.accepted.json
verification-verdict.pair.json
```

Generate rejected and digest-mismatch variants from
`tests/validation/_sample_delivery_fixtures.py`. Assert schema and digest
behavior, not the former `spec126` producer label or 2026-07-19 task date.

- [ ] **Step 5: Move reusable operation inputs to `examples/operations`**

Move the Compose readiness, PostgreSQL SQL/topology, sample delivery, and
supply-chain goldens. Update operation defaults and runbook links in the same
patch. Compare SHA-256 before and after every pure move; only generic sample
identity changes may alter content.

- [ ] **Step 6: Replace the agentic Task evidence file with a local builder**

Construct a minimal temporary Task body inside
`test_agentic_audit_semantic_freshness.py` and manifest tests:

```python
def task_evidence(*, task_id: str = "SPEC-9999-TSK-0001") -> str:
    return (
        "# Synthetic Task Evidence\n\n"
        f"| Task | Result |\n| --- | --- |\n| {task_id} | PASS |\n"
    )
```

Delete `tests/fixtures/agentic-audit/task-evidence.md` after both consumers use
the builder.

- [ ] **Step 7: Enforce library/CLI placement**

Move subprocess, argument, exit-code, generated-output, and execution-context
tests to `tests/validation/`. Keep pure parsing, state, and transformation tests
under `tests/lib/`. Delete the empty promoted placeholder; place real promoted
library assertions under `tests/lib/document_governance/lifecycle/` and keep
entrypoint mode assertions under `tests/validation/lifecycle/`.

- [ ] **Step 8: Split only multi-responsibility large modules**

Use the existing class boundaries as file boundaries. Preserve test method
names and assertions during pure moves, then update the workflow test inventory
so each module executes once. Do not split the one-class agent-output evaluator
module solely because of line count.

- [ ] **Step 9: Run focused GREEN checks**

Run:

```bash
PYTHONPATH=. python3 -m unittest discover -s tests/lib/document_governance/metadata -p 'test_*.py'
PYTHONPATH=. python3 -m unittest discover -s tests/validation/lifecycle -p 'test_*.py'
PYTHONPATH=. python3 -m unittest discover -s tests/lib/supply_chain -p 'test_*.py'
PYTHONPATH=. python3 -m unittest discover -s tests/validation -p 'test_*fixture*.py'
PYTHONPATH=. python3 -m unittest tests.validation.test_script_manifest -v
rg -n 'tests/fixtures/' scripts
rg -n 'spec126|T-AER-' tests examples scripts docs/05.operations
```

Expected: tests PASS; both searches return no current production or fixture
identity residue.

- [ ] **Step 10: Commit the test and fixture convergence**

```bash
git add tests examples scripts docs/05.operations .github/workflow-contract.yml
git commit -m "refactor(test): converge fixture and ownership boundaries"
```

### Task 5: Retire document and provider compatibility residue

**Files:**

- Modify: `scripts/lib/document_governance/metadata/identity.py`
- Modify: `scripts/lib/document_governance/metadata/lifecycle.py`
- Modify: `scripts/lib/document_governance/metadata/profile.py`
- Modify: `scripts/lib/document_governance/lifecycle/promoted.py`
- Modify: `scripts/lib/document_governance/registry.py`
- Modify: `scripts/lib/document_governance/identity_history.py`
- Modify: `scripts/lib/document_governance/archive.py`
- Modify: related document-governance tests
- Modify: `docs/05.operations/catalog/00-workspace/0004-harness-agent-first-engineering/policy.md`
- Modify: `docs/05.operations/catalog/00-workspace/0009-release-management/runbook.md`
- Retire: `docs/90.references/data/0068-target-surface-convergence-summary/**`
- Retire: `docs/90.references/data/0069-target-surface-convergence/**`
- Retire: `docs/90.references/data/0073-target-surface-delta-manifest/**`
- Retire: `docs/90.references/data/0074-target-surface-delta-summary/**`
- Modify: `docs/90.references/data/README.md`
- Modify: `docs/99.templates/registry.json`
- Create: `docs/98.archive/tombstones/90.references/0199-target-surface-convergence-summary.md`
- Create: `docs/98.archive/tombstones/90.references/0200-target-surface-convergence.md`
- Create: `docs/98.archive/tombstones/90.references/0201-target-surface-delta-manifest.md`
- Create: `docs/98.archive/tombstones/90.references/0202-target-surface-delta-summary.md`
- Modify: `docs/98.archive/README.md`
- Delete: `scripts/operations/sync-provider-surfaces.sh`
- Modify: `scripts/operations/provider_surface_renderer.py`
- Modify: `docs/00.agent-governance/providers/registry.yaml`
- Modify: provider contracts, policies, READMEs, workflow node, manifest, and tests
- Remove through renderer: `.agents/agents/**`
- Keep and regenerate: `.agents/skills/**`, `.claude/**`, `.codex/**`
- Modify: `scripts/hooks/post-tool-validate.sh`, `scripts/hooks/agent-event-hook.sh`
- Update evidence: `docs/03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0005-document-and-provider-residue.md`

**Interfaces:**

- Consumes: Stage 99 current grammar, archive/history recovery contract, Stage
  00 provider Registry, and direct renderer CLI.
- Produces: strict current classifiers, isolated historical readers, retired
  migration data, native provider projections, and one completion-time changed
  aggregate route.

- [ ] **Step 1: Add paired current-versus-history path tests**

Add focused tests with one shared legacy sample:

```python
LEGACY_REQUIREMENT = pathlib.PurePosixPath(
    "docs/01.requirements/prd-0042-preserved.md"
)

def test_current_classifier_rejects_legacy_requirement_path(self) -> None:
    self.assertIsNone(classify_current_path(LEGACY_REQUIREMENT))

def test_history_reader_recovers_legacy_requirement_identity(self) -> None:
    self.assertEqual("REQ-0042", recover_historical_identity(LEGACY_REQUIREMENT))
```

The current classifier and historical reader must be distinct imported
functions. Do not add an active compatibility option.

- [ ] **Step 2: Verify RED for legacy current classification**

Run:

```bash
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_identity_history -v
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_metadata_validator -v
```

Expected: the new current-classifier assertion fails while the history reader
continues to recover the issued identity.

- [ ] **Step 3: Isolate historical grammar**

Move `prd-`, `srs-`, `ifr-`, `spec-*`, and legacy `chg-*` parsing used only for
issued-ID or archive recovery into `identity_history.py` or `archive.py`.
Remove `_legacy_profiles`, `_PRD_PATH`, `_SRS_PATH`, `_IFR_PATH`, and legacy
relation fallback from active metadata/profile code. Update synthetic current
tests to use numeric current paths and owner-qualified Requirement IDs.

- [ ] **Step 4: Correct current operator examples**

Replace `docs/03.specs/spec-*/plan.md` and `spec-*/task.md` in the harness policy
with the registered numeric package and `tasks/tsk-####-*.md` paths. Replace the
release runbook's `spec126-*` command with the generic operation example path
created in Task 4.

- [ ] **Step 5: Prove target-surface data has no current semantic consumer**

Run:

```bash
rg -n '(0068-target-surface|0069-target-surface|0073-target-surface|0074-target-surface)' --glob '!docs/98.archive/**' .
python3 scripts/validation/check-document-links.py --mode all
python3 scripts/validation/check-document-corpus-lifecycle.py
```

Update current code, tests, indexes, and generated consumers until only the four
packages and their retirement patch remain.

- [ ] **Step 6: Retire the four completed migration DATA packages**

Recheck that the Tombstone high-water is still `0198` and stop on any collision.
In one atomic retirement patch, advance the Registry high-water to `0202` and
next allocation to `0203`, then create these sealed disposition records:

```text
0199-target-surface-convergence-summary.md -> tomb-DATA-0068
0200-target-surface-convergence.md -> tomb-DATA-0069
0201-target-surface-delta-manifest.md -> tomb-DATA-0073
0202-target-surface-delta-summary.md -> tomb-DATA-0074
```

For each package, move its registered `README.md` byte for byte to the
deterministic Stage 98 retired reference-data path selected by the archive
validator and record the exact regular-blob recovery commit in its Tombstone.
Delete unregistered generated payloads only after their exact Git recovery proof
is recorded. Update the current data and archive indexes in the same patch. Do
not change publication frontmatter before the move and do not edit the archived
body after it enters Stage 98.

- [ ] **Step 7: Add a failing provider compatibility-root test**

In `tests/validation/test_provider_surface_renderer.py`, assert the expected
projection has only native/shared roots:

```python
def test_projection_omits_provider_neutral_agent_compatibility_root(self) -> None:
    projection = expected_native_projection(ROOT)
    self.assertFalse(any(path.is_relative_to(pathlib.PurePosixPath(".agents/agents")) for path in projection))
    self.assertTrue(any(path.is_relative_to(pathlib.PurePosixPath(".agents/skills")) for path in projection))
    self.assertTrue(any(path.is_relative_to(pathlib.PurePosixPath(".claude")) for path in projection))
    self.assertTrue(any(path.is_relative_to(pathlib.PurePosixPath(".codex")) for path in projection))
```

Expected before implementation: FAIL because `.agents/agents` is still
generated.

- [ ] **Step 8: Cut provider consumers to the direct renderer**

Replace every current command with:

```bash
python3 scripts/operations/provider_surface_renderer.py --check
python3 scripts/operations/provider_surface_renderer.py --write
```

Update the workflow leaf, manifest, Stage 00 policies, scripts README, and tests.
Remove the compatibility section's `agent_pattern`, remove `.agents/agents` from
`generated_roots`, then run renderer write mode to remove only renderer-owned
stale projection files. Delete `sync-provider-surfaces.sh` after zero current
inbound references.

- [ ] **Step 9: Converge PostToolUse and Stop responsibilities**

Keep PostToolUse formatting/syntax behavior but remove its unconditional public
changed aggregate. Make Stop detect any in-scope Git-visible change and execute
the changed profile once. Preserve the retry guard and logical-commit safety
gate. Update both Claude and Codex generated hook projections from the Stage 00
registry and add parity tests for the single completion-time aggregate.

- [ ] **Step 10: Run focused GREEN checks**

Run:

```bash
PYTHONPATH=. python3 -m unittest discover -s tests/lib/document_governance -p 'test_*.py'
PYTHONPATH=. python3 -m unittest tests.validation.test_provider_surface_renderer -v
PYTHONPATH=. python3 -m unittest tests.lib.agent_governance.test_agent_governance_contract -v
PYTHONPATH=. python3 -m unittest tests.validation.test_provider_hook_parity -v
python3 scripts/operations/provider_surface_renderer.py --check
python3 scripts/validation/check-document-metadata.py --mode check-active
python3 scripts/validation/check-document-corpus-lifecycle.py
python3 scripts/validation/check-document-links.py --mode all
```

Expected: PASS; current classifiers reject legacy paths; history recovery
passes; `.agents/agents` and compatibility wrapper references are absent.

- [ ] **Step 11: Commit document and provider retirement**

```bash
git add docs scripts tests .agents .claude .codex .github/workflow-contract.yml
git commit -m "refactor(governance): retire compatibility residue"
```

### Task 6: Regenerate evidence and run final verification

**Files:**

- Modify through generators: declared current outputs under `docs/90.references/data/**`
- Modify through generator: `llms.txt`, `llms-full.txt`, DATA-0076, and DATA-0082
- Modify: `docs/03.specs/README.md`
- Modify: `docs/90.references/data/README.md`
- Modify: `scripts/README.md`, `tests/README.md`, `.github/repository-surface.md`
- Modify with actual evidence: all six SPEC-0173 Task documents
- Modify with durable outcomes: `docs/03.specs/0173-governance-qa-surface-convergence/spec.md`

**Interfaces:**

- Consumes: Tasks 1 through 5 at focused GREEN.
- Produces: fresh generated outputs, exact Task evidence, one final full-gate
  result, independent review findings, and an implementation-ready completion
  decision.

- [ ] **Step 1: List every declared generator and its check/write command**

Run:

```bash
python3 scripts/validation/check-script-manifest.py
rg -n 'check_command:|outputs:' scripts/manifest.yaml
```

Expected: every current generated output has one owner and every retired output
has no current generator consumer.

- [ ] **Step 2: Regenerate only outputs made stale by Tasks 1 through 5**

Run the applicable write modes in dependency order:

```bash
python3 scripts/operations/provider_surface_renderer.py --write
bash scripts/operations/generate-compose-profile-service-coverage.sh
bash scripts/operations/generate-tech-stack-version-provenance.sh
bash scripts/validation/generate-audit-implementation-matrix.sh
bash scripts/validation/generate-security-automation-readiness.sh
bash scripts/security/generate-supply-chain-sample-service-summary.sh
python3 scripts/knowledge/generate-llm-wiki.py --write
```

Skip a generator only when its tracked inputs and output paths are unchanged;
record that exact reason in Task 6.

- [ ] **Step 3: Run every generated freshness check**

Run:

```bash
python3 scripts/operations/provider_surface_renderer.py --check
bash scripts/operations/generate-compose-profile-service-coverage.sh --check
bash scripts/operations/generate-tech-stack-version-provenance.sh --check
bash scripts/validation/generate-audit-implementation-matrix.sh --check
bash scripts/validation/generate-security-automation-readiness.sh --check
bash scripts/security/generate-supply-chain-sample-service-summary.sh --check
python3 scripts/knowledge/generate-llm-wiki.py --check
```

Expected: all exit `0` without modifying files.

- [ ] **Step 4: Run focused ownership and governance suites**

Run:

```bash
python3 scripts/validation/check-script-manifest.py
PYTHONPATH=. python3 -m unittest discover -s tests/lib/document_governance/metadata -p 'test_*.py'
PYTHONPATH=. python3 -m unittest discover -s tests/validation/lifecycle -p 'test_*.py'
PYTHONPATH=. python3 -m unittest discover -s tests/lib/gate -p 'test_*.py'
PYTHONPATH=. python3 -m unittest discover -s tests/validation -p 'test_ci_gate*.py'
PYTHONPATH=. python3 -m unittest tests.validation.test_provider_surface_renderer -v
python3 scripts/validation/check-document-links.py --mode all
python3 scripts/validation/check-document-corpus-lifecycle.py
```

Expected: all PASS. Record test counts from output rather than encoding them as
permanent assertions.

- [ ] **Step 5: Verify path, identity, fixture, and compatibility residue is zero**

Run:

```bash
rg -n 'docs/03\.specs/spec-|docs/01\.requirements/(prd-|srs-|ifr-)' --glob '!docs/98.archive/**' docs scripts tests examples
rg -n 'artifact_id:[[:space:]]*(FR-|NFR-|IF-)' docs
rg -n 'tests/fixtures/' scripts
rg -n '(run-local-qa-gates|validate-harness|sync-provider-surfaces|check-doc-implementation-alignment|check-doc-traceability)' --glob '!docs/98.archive/**' .
rg -n '\.agents/agents' --glob '!docs/98.archive/**' .
```

Expected: no current ownership or invocation residue. Explicit historical
recovery fixtures may appear only in isolated history tests and must be named as
such in the Task evidence.

- [ ] **Step 6: Run the pre-review candidate aggregate once**

Run:

```bash
git diff --check
python3 scripts/validation/run-ci-gate.py --profile full
git status --short --branch
```

Expected: diff check and full exit `0`; status lists only approved Task-owned
paths. Do not separately rerun workloads already executed by this full profile
on the same input. This is a review candidate, not final completion evidence,
because Step 8 will change the evidence documents.

- [ ] **Step 7: Perform independent policy and code review**

Review the exact branch diff for:

- validation coverage loss;
- executable ownership duplication;
- archive-body mutation;
- current/historical grammar leakage;
- unsafe provider deletion;
- operation/test fixture coupling;
- missing generated outputs or inbound links.

Record Critical, Important, and Minor counts plus every remediation rerun in
Task 6. Do not mark complete while a blocking finding remains.

- [ ] **Step 8: Write durable outcomes and final evidence**

Update the Spec only with behavior that is actually current. Update each Task's
Work Log, Verification Evidence, Review Evidence, and Commit Ledger with exact
commands, exit codes, and commit SHAs. Runtime, entitlement, Hosted CI, and
remote protection remain `UNVERIFIED` unless separately authorized and observed.

- [ ] **Step 9: Regenerate evidence-derived outputs and verify the final tree**

Rerun only generators whose tracked inputs include the Spec or Task evidence,
then run their check modes. On that final content, execute at least:

```bash
python3 scripts/validation/check-script-manifest.py
PYTHONPATH=. python3 -m unittest discover -s tests -p 'test_*.py'
PYTHONPATH=. python3 -m unittest discover -s tests/lib/document_governance/metadata -p 'test_*.py'
PYTHONPATH=. python3 -m unittest discover -s tests/validation/lifecycle -p 'test_*.py'
PYTHONPATH=. python3 -m unittest tests.validation.test_provider_surface_renderer -v
PYTHONPATH=. python3 -m unittest tests.lib.agent_governance.test_agent_governance_contract -v
PYTHONPATH=. python3 -m unittest tests.validation.test_provider_hook_parity -v
python3 scripts/operations/provider_surface_renderer.py --check
python3 scripts/validation/check-document-metadata.py --mode check-active
python3 scripts/validation/check-document-corpus-lifecycle.py
python3 scripts/validation/check-document-links.py --mode all
git diff --check
python3 scripts/validation/run-ci-gate.py --profile full
git status --short --branch
```

Repeat the residue scans from Step 5 and the canonical-invocation uniqueness
test from Task 2. The Step 6 candidate and this final aggregate have different
inputs; never repeat the heavy aggregate on an unchanged tree. Make no content
change after this final verification except the commit object created by the
next step.

- [ ] **Step 10: Commit the final generated and evidence state**

```bash
git add docs scripts tests examples .agents .claude .codex .github llms.txt llms-full.txt
git commit -m "docs(spec): record governance QA convergence evidence"
```

Do not push, open a PR, merge, tag, release, or terminalize SPEC-0173 without a
separate approval covering that action and its exact target.

## Risk and Rollback

| Risk | Prevention | Rollback |
| --- | --- | --- |
| Missing validation leaf | Before/after semantic leaf inventory; duplicate rejection | Revert Task 2 commit |
| Wrapper external consumer | Tracked zero-inbound proof; external boundary recorded unverified | Revert Task 3 or Task 5 commit |
| Changed Compose coverage | Keep one no-env every-declared invocation and existing profile assertions | Revert gate-node consolidation |
| Lost historical identity | Paired current reject/history recover tests | Revert only history isolation commit |
| Fixture semantic drift | SHA-256 or parsed-payload comparison across moves | Revert Task 4 commit |
| Archive corruption | Never edit frozen bodies; use registered transitions before move | Revert pre-terminal commit; never patch frozen body |
| Provider projection loss | Keep native Claude/Codex/shared-skill roots and direct renderer checks | Restore compatibility registry route and rerender through normal revert |
| Hook validation gap | Focused event parity tests and one completion-time changed gate | Revert hook portion of Task 5 |
| Generated stale output | One declared owner and write/check pair | Rerun only owning generator or revert Task 6 |

Rollback uses normal `git revert` for committed logical slices or a reviewed
inverse patch before commit. The plan never uses reset, clean, stash, force
push, validator bypass, or frozen archive editing.

## Verification

The completion evidence must contain:

1. Fresh branch, HEAD, main, cached origin/main, worktree, stash, and status.
2. Pre-change and post-change public plans for five profile/context cases.
3. Zero duplicate canonical invocation identities.
4. Exact removed and retained leaf inventory.
5. Manifest ownership and transition checks.
6. Metadata and lifecycle focused discovery results.
7. Gate, provider, operation, supply-chain, and fixture focused results.
8. Zero production reference to `tests/fixtures`.
9. Current-path rejection and historical-recovery acceptance evidence.
10. Provider renderer write/check and native projection parity.
11. Generated write/check results and LLM Wiki freshness.
12. `git diff --check` and one final full profile result.
13. Independent review result and remediation reruns.
14. Explicit `UNVERIFIED` labels for runtime, entitlement, Hosted CI, and remote
    state not observed under an additional approval.

## Rulings

- Use SPEC-0173 because the Registry and Git history show SPEC high-water 172
  and no issued SPEC-0173 or higher artifact.
- Do not expand SPEC-0172 with the new work; reconcile and preserve its completed
  outcome first.
- Prefer `.github/workflow-contract.yml` over the manifest as executable DAG
  owner because it already owns nodes, roots, ordering, setup, environment,
  timeout, workflow, and job bindings.
- Keep `scripts/manifest.yaml` as the sole file inventory but remove executable
  composition fields from it.
- Remove obsolete modes and wrappers rather than restoring compatibility.
- Keep one canonical Compose full-coverage invocation; do not use an inherited
  environment value to manufacture a second mode.
- Retire target-surface snapshots because they describe a completed migration,
  not a present-tense repository invariant.
- Preserve static fixture files only where the serialized external format is
  part of the contract; generate single-field negative variants in tests.
- Preserve `.agents/skills`, Claude adapters, and Codex adapters; retire only the
  provider-neutral agent compatibility projection with no tracked runtime
  consumer.
- Treat completed Specs as evidence. Current policy, Registry, architecture,
  operation, and executable contracts remain authoritative.

## Related Documents

- [Specification](spec.md)
- [Task 1](tasks/tsk-0001-lifecycle-and-red-contracts.md)
- [Task 2](tasks/tsk-0002-gate-composition-convergence.md)
- [Task 3](tasks/tsk-0003-script-and-operation-ownership.md)
- [Task 4](tasks/tsk-0004-test-and-fixture-convergence.md)
- [Task 5](tasks/tsk-0005-document-and-provider-residue.md)
- [Task 6](tasks/tsk-0006-generated-evidence-and-final-verification.md)
