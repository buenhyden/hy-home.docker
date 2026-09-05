---
title: "Governance and QA Surface Convergence Implementation Plan"
version: "0.3.1"
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

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for
> a separately approved implementation. Steps use checkbox syntax; an unchecked
> step is prospective, not evidence of execution.

**Goal:** Plan a selective integration onto the user-fixed main baseline while
allowing an empty `.agents/` directory, retaining direct canonical skill reads,
and preserving both implementation histories without duplicate authority.

**Architecture:** Stage 00 owns policy; Stage 99 owns document and lifecycle
contracts. The target executable-composition owner is
`.github/workflow-contract.yml`; `scripts/manifest.yaml` owns file inventory.
Only native Claude/Codex surfaces are generated. An allowed empty `.agents/`
root is not a role, skill, policy, or memory authority.

**Tech Stack:** Python 3, PyYAML, Bash, Git, unittest, typed gate contracts,
repository-native document validators, and static Docker Compose checks.

**Spec:** `docs/03.specs/0173-governance-qa-surface-convergence/spec.md`

## Objective

This revision replaces the old prospective sequence, not its historical evidence.
Task 0001 through Task 0005 retain their actual RED/GREEN, review, and commit
records. The prior Plan is recoverable at `5547e07a2`; do not re-execute its
completed steps or use its shared-skill/transient-deletion instructions as the
integration contract.

The user subsequently authorized finishing this existing package, local main
integration and safe feature cleanup without new Spec/Plan/Task documents or
IDs. The latest approval explicitly includes adjusting the existing disposition
policy and correcting the two remaining Stop/README defects with independent
re-review. This supersedes the earlier planning-only checkpoint, not its
historical evidence. No remote or runtime action is authorized.

The rules-engineer cleared a generic typed divergent-branch handoff design.
W1 must implement and verify its exact preservation guards before predecessor
disposition. W4's independent bounded fixes can proceed while that contract is
implemented; neither their focused success nor policy clearance is final
integration acceptance.

### Global constraints

- Integration baseline: `c02fa282db30fa4576fa04bcd328a47fe7da8511`.
- Feature checkpoint: `5547e07a2ef0b5a8d5b16c2d96af02167f46a8ab`, plus the
  pre-existing task-owned working patch. Neither is a final green tree.
- Common ancestor: `71da6654e2fa3def174b238ad309c92fe46e9dae`.
- Preserve six suites: `agent-governance`, `document-contract`,
  `document-graph`, `document-lifecycle`, `operations`,
  `repository-integrity`.
- Preserve profiles `changed` and `full`, required jobs
  `validation-changed`/`validation-full`, `strict=true`, and app ID `15368`.
- Keep main's direct Stage 00 skill loading and Codex
  `native_skill_pattern: null`. Change only the whole-root prohibition:
  absence or an empty real `.agents/` directory is permitted.
- Do not restore `.agents/agents/`, `.agents/skills/`, generated
  `.agents/README.md`, or a `.codex/skills/` substitute. Unknown contents are
  preserved and reported for manual disposition, never automatically deleted.
- Empty directories are not tracked by Git. Do not add a placeholder file,
  unowned content, or a generator solely to force directory presence.
- Preserve main's substantive metadata/schema/SDLC changes and independent
  Compose selections; no whole-file "ours/theirs" resolution.
- Keep all frozen archive bytes unchanged, including completed SPEC-0172 and
  retired DATA-0068/0069/0073/0074 with Tombstones 0199-0202.
- Keep Spec allocation at least high-water 174/next 175 and Tombstone allocation
  at least high-water 202/next 203. Do not issue an ID in this planning turn.
- No validator exception, parallel registry, credential access, global setting
  change, service execution, push, PR, remote mutation, force operation, stash,
  reset, or clean. Existing cleanup requests remain conditional on verified
  integration and do not authorize discarding unmerged work.

## Dependencies

The current authorities to reconcile are REQ-0024/0026, AD-0027/0030,
ADR-0029/0031, Stage 00 bootstrap/provider/documentation/quality/approval/workflow
policies, Stage 99, and the two branch histories.

The main baseline adds SPEC-0174 and changes SPEC-0172's draft follow-up.
The feature already preserves a completed SPEC-0172. The earlier unqualified
draft-to-archive proposal was withdrawn. The approved generic divergent-branch
handoff now requires exact preservation and a verified receipt; ordinary
disposition still requires registered terminal transitions.

The current root checkout exposes an empty read-only tmpfs at `.agents`.
The old main whole-root check fails there while renderer parity passes.
Do not remove/unmount it or hide it with an exemption. After W2 implements the
explicitly requested empty-root contract, that real empty directory is a valid
input; it is not evidence of native runtime acceptance.

### Source selection and owned paths

| Unit | Future implementation owner | Exact primary surfaces |
| --- | --- | --- |
| W1 | doc-writer, independently reviewed by rules-engineer | SPEC-0173 Spec/Plan/Task 0006; current SPEC-0172/0174 packages; Stage 03/98 indexes; Stage 99 Registry; document-governance Spec/archive/lifecycle tests |
| W2 | ci-cd-engineer, policy review first | Stage 00 provider/policy sources; agent-governance library; provider renderer; native surface tests and generated adapters |
| W3 | ci-cd-engineer | workflow contract; gate libraries/runner; manifest/checker; relocated operation/examples and their existing tests |
| W4 | hook-developer and doc-writer, separate diffs | event hook/routing tests; scripts README and existing generator guidance tests |
| W5 | doc-writer | validated predecessor package disposition; current reference corrections; declared generator outputs and indexes |
| W6 | qa-engineer plus independent reviewers | checks and Task 0006 evidence; no unrelated implementation |

## Execution Sequence

1. W1: Implement the approved identity-preservation rule and integration ledger.
2. W2: Reconcile the allowed-directory/direct-skill policy and its consumers.
3. W3: Integrate gate invariants and PostgreSQL operation ownership.
4. W4: Perform separately authorized Stop and README correction units.
5. W5: Close lifecycle handoff and regenerate only affected evidence.
6. W6: Verify the final content and obtain independent acceptance.

### W1: Identity decision and integration ledger

**Files:** Read both histories of
`docs/03.specs/0172-document-contract-convergence/`,
`docs/03.specs/0174-governance-qa-convergence/`,
`docs/98.archive/completed/03.specs/0172-document-contract-convergence/spec.md`,
`docs/99.templates/registry.json`,
`scripts/lib/document_governance/spec_packages.py`,
`scripts/lib/document_governance/archive.py`, and
`scripts/lib/document_governance/lifecycle/contract.py`.
Policy and machine owners are
`docs/00.agent-governance/policies/documentation-protocol.md`,
`docs/99.templates/contracts/document-frontmatter.schema.json`, Registry,
`scripts/lib/document_governance/spec_packages.py`, and existing Spec-package
and Registry tests. Record decisions in this package's Task 0006.

**Interfaces:** Consumes immutable baseline/feature objects and current Registry
edges. Produces a user-approved path/identity/disposition ledger and
acceptance-to-owner mapping; no implicit lifecycle permission.

- [ ] Capture main, feature, worktree, staged and unstaged state again:

```bash
git rev-parse main HEAD
git worktree list --porcelain
git status --short
git diff --check
git diff --name-status c02fa282d HEAD
git diff --name-status
```

- [ ] Inventory each c02 SPEC-0172/0174 Spec/Plan/Task obligation and assign its
  still-current behavior to Stage 00/01/02/05 plus an integration acceptance
  criterion in SPEC-0173. Keep source commit, blob, owner, created date and
  full artifact ID. Obtain exact objects using:

```bash
git ls-tree -r c02fa282d -- docs/03.specs/0172-document-contract-convergence docs/03.specs/0174-governance-qa-convergence
git ls-tree -r 5547e07a2 -- docs/98.archive/completed/03.specs/0172-document-contract-convergence
git show c02fa282d:docs/99.templates/registry.json
```

- [ ] Resolve **SPEC-0172 through the approved branch-handoff rule**. The feature's completed
  identity has no outgoing lifecycle edge. Do not reopen it, relabel main's
  draft as completed/superseded, overwrite its completed archive, or allocate
  SPEC-0175 merely to escape the conflict. Leave main's package and the existing
  archive unchanged. Register typed `branch_integration_receipts` on Task only:
  full source commit, original package path/ID, superseded preservation path,
  distinct target package path/ID, and `historical-superseded` disposition.
  Verify the exact source base, complete regular-file tree and byte equality,
  absence from current Stage 03, immutable same-ID completed Spec, and one valid
  target Task carrier. No per-ID or commit allowlist is permitted.
- [ ] Before any eventual archive mutation, add isolated regression cases in
  `tests/lib/document_governance/test_archive.py`,
  `tests/lib/document_governance/test_identity_history.py`, and
  `tests/lib/document_governance/test_spec_packages.py`:
  reject terminal-ID reopening and unreceipted draft-to-archive shortcuts; preserve the
  original completed body; prove every full package member's recovery.
  Example negative invariant using the actual Registry:

```python
registry = json.loads((ROOT / "docs/99.templates/registry.json").read_text())
edges = registry["lifecycles"]["spec"]["transitions"]
self.assertEqual([], edges["completed"])
self.assertNotIn("superseded", edges["draft"])
self.assertIn("superseded", edges["active"])
```

  Keep the lifecycle graph unchanged. Test current and completed-archive Task
  receipt carriers, missing/duplicate carrier, wrong base/path/identity, invalid
  target, changed/missing/extra/unsafe members, and ordinary terminal
  preservation. The completed carrier is the unchanged receipt preserved after
  atomic target completion, not current policy authority.
- [ ] Freeze an exact per-path keep/merge/move/disposition ledger covering both
  commit deltas and the existing WIP. Preserve both histories and future recovery
  references; no rebase/squash or whole-side conflict selection. Agree how to
  checkpoint each WIP logical unit before any Git merge; do not overwrite dirty
  paths or hide them in stash. Execution uses the existing isolated feature
  worktree, not direct main edits.
- [x] Obtain explicit implementation approval and independent policy design clearance.
  Proposed evidence commit: `docs(spec): approve bounded main integration`.
  Stage only reviewed package evidence; do not commit rejected code as complete.

### W2: Allow an empty directory without restoring duplicate authority

**Files:** Modify canonical sources first:
`docs/00.agent-governance/providers/codex.md`,
`docs/00.agent-governance/providers/registry.yaml`,
`docs/00.agent-governance/policies/agentic.md`,
`docs/00.agent-governance/policies/provider-capability-matrix.md`,
`docs/00.agent-governance/policies/stage-authoring-matrix.md`,
`docs/00.agent-governance/policies/approval-boundaries.md`,
`docs/01.requirements/0024-agent-governance-standardization.md`,
`docs/02.architecture/descriptions/0027-agent-governance-canonical-adapter.md`,
and `docs/02.architecture/decisions/0029-workspace-governance-authority.md`.
If an accepted ADR needs supersession rather than a compatible clarification,
stop for that separate decision instead of silently rewriting its choice.
Code owners:
`scripts/lib/agent_governance/agent_governance_contract.py`,
`scripts/operations/provider_surface_renderer.py`,
`scripts/hooks/agent-event-hook.sh`.
Tests:
`tests/lib/agent_governance/test_agent_governance_contract.py`,
`tests/validation/test_provider_native_surfaces.py`,
`tests/validation/test_provider_surface_renderer.py`.
Only affected `.claude/` and `.codex/` outputs are generated.

**Interfaces:** One agent-governance library rule returns findings for the
optional root and is consumed by governance validation and renderer check/write.
Do not copy feature commit `5547e07a2` wholesale: its subtree-only assumption is
not the new directory-without-projections contract.

- [ ] Add an empty-root acceptance test before changing the whole-root rule:

```python
with tempfile.TemporaryDirectory() as directory:
    root = pathlib.Path(directory)
    copy_governance_fixture(root)
    (root / ".agents").mkdir(exist_ok=True)
    findings = contract.validate_repository(
        root, contract.load_contract_bundle(root), "providers"
    )
    self.assertFalse(any(item.path.startswith(".agents") for item in findings))
```

  Run the library test on c02 behavior and record the retired-root RED finding.
  Adapt the existing fixture copier to main's native-only surfaces, not to a
  second shared projection.
- [ ] Add file, symlink (including broken link), FIFO, nonempty root, forbidden
  `agents`/`skills` child, and permission-denied cases. Absence and an empty
  real directory pass; unreadable/unverifiable or nonempty roots fail without
  following children or reading their contents. A read-only empty root also
  passes. Use temporary input, never chmod/remove the host mount.
- [ ] Implement the rule in the existing library with no-follow descriptor
  operations. Distinguish missing root, directory, unsupported object and
  enumeration failure. Inspect child names only; preserve unknown objects.
  Both renderer modes call this same owner; write refuses before any generated
  write/quarantine when the root fails validation.
- [ ] Update the named current policy/architecture consumers to permit this
  root without granting it authority. Keep Registry v2, native Claude skills,
  direct Codex skill reads, `native_skill_pattern: null`, and no generated
  `.agents/README.md`/shared skills. Do not introduce a placeholder or new
  runtime README profile. Update the hook's whole-root edit warning to the new
  empty-root/non-authority rule without changing Stop behavior in this unit.
- [ ] Run RED/GREEN and then native projection generation and checks:

```bash
PYTHONPATH=. python3 -m unittest tests.lib.agent_governance.test_agent_governance_contract tests.validation.test_provider_native_surfaces tests.validation.test_provider_surface_renderer -v
python3 scripts/operations/provider_surface_renderer.py --write
python3 scripts/operations/provider_surface_renderer.py --check
python3 scripts/validation/check-agent-governance-contract.py --section providers
git diff --check
```

- [ ] Obtain independent code and policy review. Commit canonical source, tests,
  and generated adapters atomically:
  `fix(governance): allow empty agent directory with direct skills`.

### W3: Select gate and operation improvements without reverting main

**Files:** `.github/workflow-contract.yml`,
`scripts/lib/gate/ci_gate_contract.py`,
`scripts/lib/gate/github_workflow_contract.py`,
`scripts/validation/ci_gate_runner.py`,
`scripts/manifest.yaml`,
`scripts/validation/check-script-manifest.py`,
`scripts/operations/rehearse-postgres-logical-upgrade.sh`,
`examples/operations/postgres-logical-upgrade/`;
tests in `tests/lib/gate/`,
`tests/validation/test_ci_gate_model.py`,
`tests/validation/test_ci_gate_plan.py`,
`tests/validation/test_ci_gate_execution_context.py`,
`tests/validation/test_postgres_logical_upgrade_rehearsal.py`,
`tests/validation/test_script_manifest.py`,
`tests/lib/test_surface_ownership.py`, and
`tests/lib/document_governance/lifecycle/__init__.py`.
Remove the old `scripts/lib/ops/rehearse-postgres-logical-upgrade.sh` and
`tests/fixtures/postgres-logical-upgrade/` only with their existing operation,
manifest, runbook, test and workflow consumers cut over in that atomic change.
Runbook: `docs/05.operations/catalog/04-data/0032-postgresql-logical-upgrade-restore-rehearsal/runbook.md`.

**Interfaces:** Preserve main's one Compose leaf and
`setup.frontend-node-dependencies` identifier. Port feature's
`canonical_invocation_key(root, invocation, profile=..., context=...)` and
`ci-gate-invocation-duplicate` rejection; keep descriptor execution intact.

- [ ] Exercise feature's existing canonical-key negative tests against the
  pre-integration runner; record RED or exact already-present behavior. Use
  resolved entrypoint plus normalized argv, public profile and execution context;
  semantic modes remain explicit argv, not ambient environment.
- [ ] Merge the workflow-owned public composition and inventory-only manifest
  as a single gate slice. Preserve c02 Greeting permissions and unrelated
  workflow fixes. Keep no-env independent Compose selection and one frontend
  setup node; adapt feature's old Storybook node-ID assertions to main's ID.
- [ ] Carry the reviewed transition contract: final sample-delivery operation is
  active; transitioning rows require a distinct tracked successor, non-retain
  disposition and nonblank `removal_condition`. Active rows omit the condition.
  Do not restore a second composition registry.
- [ ] Register the promoted lifecycle module exactly once and preserve its
  discovery initializer. Verify every test module's reachability:

```bash
PYTHONPATH=. python3 -m unittest tests.validation.test_ci_gate_plan.CiGateRunnerContractTests.test_every_public_plan_has_unique_canonical_invocations tests.lib.test_surface_ownership.SurfaceOwnershipTests.test_every_test_module_is_reachable_from_the_full_profile -v
PYTHONPATH=. python3 -m unittest discover -s tests/lib/gate -p 'test_*.py'
PYTHONPATH=. python3 -m unittest discover -s tests/validation -p 'test_ci_gate*.py'
python3 scripts/validation/check-script-manifest.py
```

- [ ] Obtain independent gate review; commit `refactor(gate): integrate canonical invocation ownership`.
- [ ] In a separate operation slice, preserve `f8ce954cc` with its relocation,
  example bytes, `leaf.postgres-logical-upgrade-config` check-only route and
  consumer cutover. Root discovery must remain:

```bash
SCRIPT_PATH="$(readlink -f -- "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd -P)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd -P)"
```

- [ ] Reproduce old held-descriptor failure only in the existing temporary
  fixture, then run the actual corrected runner test and full operation owner:

```bash
PYTHONPATH=. python3 -m unittest tests.validation.test_postgres_logical_upgrade_rehearsal -v
```

  Require exit 0, `status=check-passed`, `cleanup_status=passed`, and no real
  Docker service. Do not add source-only evidence as a substitute for the real
  `execute_execution_plan` regression. Review and commit
  `fix(operations): integrate verified PostgreSQL entrypoint`.

### W4: Approved renewed bounded corrections

**Files:** `scripts/hooks/agent-event-hook.sh`,
`tests/validation/test_agent_governance_ci_routing.py`,
`scripts/README.md`, `tests/validation/test_script_manifest.py`.
The user's latest explicit approval renews these two named corrections and
their independent re-review; it does not authorize unrelated fixes.

**Interfaces:** Stop emits a blocking JSON result when dirty/error state cannot
be cleared; README write instructions invoke the existing explicit write mode.

- [x] Obtain explicit approval separately naming the downstream Stop byte-bound
  and the remaining README write examples, plus independent re-review. Do not
  classify these as automatically authorized by W1 integration.
- [ ] Extend the existing fake-Git routing regression for both providers with
  80 path rows that approach a legal relative PATH_MAX length:

```python
segments = "/".join(["x" * 200] * 18)
porcelain = "\n".join(f"?? {segments}/file-{i:03d}.txt" for i in range(80))
self.assertGreater(len(porcelain.encode("utf-8")), 131072)
```

  Feed this to the current fake-Git helper; require parseable blocking JSON,
  no SessionEnd, and at most one changed aggregate. Add a multibyte path case
  and retain malformed Git, timeout and retry tests. Witness RED before fixing.
- [ ] Preserve feature's FD input and parser failure guard, 540-second gate
  timeout plus five-second termination bound, both-provider retry guard, and
  600-second Claude hook contract. Bound displayed path diagnostics to 6000
  UTF-8 bytes before any remaining environment transport; bound the final
  reason as well or send it over a descriptor. Preserve a nonempty explicit
  truncation notice. Never let truncation produce an empty clean-state result.
  A byte-aware display core can use:

```python
payload = "\n".join(paths[:80]).encode("utf-8")
display = payload[:6000].decode("utf-8", errors="ignore")
if len(payload) > 6000:
    display += "\n[additional changed-path bytes omitted]"
```

  This is diagnostic display only: full dirty-state detection is not truncated.
  Do not discard W2's revised directory warning while applying the hook slice.
- [ ] Run the routing suite and independent review. Commit
  `fix(hooks): bound completion diagnostics by bytes`.
- [ ] In a separate documentation slice, change the maintenance entries for
  `generate-audit-implementation-matrix.sh`,
  `generate-security-automation-readiness.sh`, and
  `generate-supply-chain-sample-service-summary.sh` to explicit `--write`.
  The first audit “generate and check” example also needs `--write`; leave
  read-only advisory/check listings unchanged. Exact executable examples:

```bash
bash scripts/validation/generate-audit-implementation-matrix.sh --write
bash scripts/validation/generate-audit-implementation-matrix.sh --check
bash scripts/validation/generate-security-automation-readiness.sh --write
bash scripts/security/generate-supply-chain-sample-service-summary.sh --write
```

- [ ] Add a focused README contract test, scoped to the “Generated index
  maintenance” row and audit refresh code block, so checking only DATA-0059/0061
  cannot mask these omissions. Assert each exact command above in its write
  context; verify the audit check command still exists. Witness RED, fix prose,
  run the manifest test owner, and get independent documentation review.
  Commit `docs(qa): correct remaining generator write routes`.

### W5: Lifecycle closeout and derived evidence

**Files:** Current SPEC-0174 Spec/Plan/Task and eventual matching package paths
under `docs/98.archive/superseded/03.specs/0174-governance-qa-convergence/`;
`docs/03.specs/README.md`, `docs/98.archive/README.md`,
`docs/99.templates/registry.json`; Task 0006 promotion receipt.
Reference source corrections: AUD-0019/0020/0026/0027/0030/0032 READMEs,
REQ-0025, ADR-0028, AD-0028, scripts/tests READMEs.
Do not overwrite main's additional metadata/SDLC work with these feature files.

**Interfaces:** Consumes W1's approved identity decision and verified owner
transfer. Produces registered terminal disposition, complete preserved packages,
unchanged frozen bodies and fresh generated outputs.

- [ ] SPEC-0172 disposition remains controlled by W1, not by this generic
  closeout. Do not supply a fabricated route in its place.
- [ ] For SPEC-0174, obtain real review/approval for closeout and use separate
  registered edges; these are not retrospective approvals of old implementation:

| Checkpoint | Spec | Plan | Task |
| --- | --- | --- | --- |
| A | draft → review | draft → approved | draft → ready |
| B | review → approved | approved retained | ready retained |
| C | approved → active | approved → active | ready → in-progress |
| D, only after verified transfer | active → superseded | active → cancelled | in-progress → cancelled |

  An active Plan requires an active Spec. Checkpoint B therefore leaves the
  Plan approved; checkpoint C activates Spec, Plan and Task atomically. This
  corrects the rejected sequence without weakening the existing state contract.
  Check each nonterminal checkpoint before committing. Bind current owner
  SPEC-0173 with reciprocal lineage where the profiles allow it. At D,
  transition and full-package preservation are one atomic disposition; no
  terminal documents remain in current Stage 03. Preserve the approved
  terminal source bytes, not an edited frozen body. Keep c02 source objects
  reachable as the earlier observation. Only W1's verified divergent-source
  receipt permits nonterminal preservation; never claim unobserved acceptance
  as completed.
- [ ] Prove archive/lineage/identity behavior in isolated fixtures first.
  If dual historical SPEC-0172 disposition or SPEC-0174 package-member rules
  reject the proposed route, stop for a lifecycle decision; no new exception,
  speculative ID, or alternate path. Commands:

```bash
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_archive tests.lib.document_governance.test_identity_history tests.lib.document_governance.test_spec_packages -v
PYTHONPATH=. python3 -m unittest discover -s tests/validation/lifecycle -p 'test_*.py'
python3 scripts/validation/check-document-corpus-lifecycle.py
python3 scripts/validation/check-document-links.py --mode all
```

- [ ] Reconcile Registry max-issued values, current indexes, references and
  promotion receipt atomically. Correct archive README wording to distinguish
  the three Registry-frozen legacy migration ledgers from normally linted
  authored migrations/tombstones; do not edit those frozen ledgers.
- [ ] Preserve the feature's accepted current-vs-historical audit corrections,
  but re-evaluate every current provider statement against W2 (no shared
  skills). Do not treat past two-provider parity as current native acceptance.
- [ ] Regenerate only changed-input outputs, in this order: provider native
  projections; DATA-0059/0061 owner outputs; DATA-0065 audit matrix;
  DATA-0078 security readiness; DATA-0079 supply-chain summary; DATA-0072 hook
  parity if dispatch inputs changed; DATA-0076/0082 LLM Wiki.
  Use each existing manifest-declared owner and explicit `--write`, followed
  by `--check`. If inputs did not change, record the skip and run check mode.
  Do not write authored `llms.txt`, excluded `llms-full.txt`, or Graphify
  output by hand.
- [ ] Review source/disposition and derived-output changes independently.
  Use logical commits `docs(spec): preserve approved predecessor handoff`
  and `chore(data): refresh integrated governance evidence`.

### W6: Final verification and handoff

**Files:** Task 0006 owns exact acceptance mapping, command outcomes, review
findings, rollback references, and limitations. The Spec owns durable target
behavior; none of the earlier candidate runs proves this integrated tree.

**Interfaces:** Consumes accepted W1-W5 and committed executable entrypoints.
Produces independently reviewed final-tree evidence, not deployment claims.

- [ ] In Task 0006 map Spec acceptance 1-16 to W1-W6 and Stage 00/01/02/05
  owners. Use observed PASS or justified SKIP; never a count-only policy or
  candidate success copied from another tree.
- [ ] Run focused suites, then source-derived freshness checks before the
  heavy aggregate. Commit reviewed executable changes before descriptor
  identity admission; do not bypass the tracked-object check.
- [ ] Execute on final content. The latest minimum-check instruction replaces
  separate repeat discoveries below with the canonical full profile's existing
  leaf coverage. Run a direct focused check only for a changed integration
  boundary or to diagnose the first failing leaf:

```bash
git diff --check
python3 scripts/validation/run-ci-gate.py --profile full
git status --short
```

  Run the canonical-key and full-profile reachability tests from W3 as well.
  Scan current script/docs/template examples for forbidden basename prefixes,
  shorthand Requirement IDs, old operation routes and shared generated skills.
  Classify actual historical quotations separately; do not delete them by age.
  No production script may read `tests/`; no generator runs write mode in a
  validation aggregate.
- [ ] Record first failure and stop at the applicable retry bound. Never rerun
  unchanged heavy aggregates for reassurance. After evidence edits, regenerate
  only affected derived outputs and verify their new content once.
- [ ] Obtain independent code, Python and policy review for exact final diff
  and evidence. A separate reviewer owns each verdict.
- [ ] Only after green acceptance, invoke finishing-a-development-branch under
  the user's current integration/cleanup instruction. Preserve recovery commits.
  Merge reviewed feature commits into local main, resolve conflicts there under
  the user's latest instruction, verify the result, and clean only fully
  integrated feature state. Prepare for push without performing a remote push.
  Reuse unchanged focused evidence and avoid duplicate heavy aggregates under
  the user's minimum-check instruction; retain the final mandatory gate.

## Risk and Rollback

| Risk | Guard | Recovery |
| --- | --- | --- |
| Terminal SPEC-0172 reopened | W1 hard identity gate | Keep both existing histories untouched; request decision |
| Main changes lost in wide merge | Per-path ledger and semantic review | Reviewed inverse patch or logical revert; no whole-side resolution |
| Empty root becomes duplicate policy tree | W2 single rule and negative tests | Revert source/projection logical commit; preserve unknown contents |
| Read-only root causes unsafe cleanup | Enumerate names without mutation | Report unverifiable state; never remove/unmount |
| Stop appears clean after truncation | Dirty detection separate from byte-bounded display | Revert hook slice; completion remains blocked |
| Gate coverage drops | All-module reachability and canonical uniqueness | Revert gate slice with consumer map |
| Frozen evidence rewritten | Exact Git blob comparison and legal terminal disposition | Stop; restore only through approved recovery, never patch frozen bodies |
| Stale generated data | One owner and explicit write/check | Regenerate from reviewed source or revert that logical output |

## Verification

Revision checks are metadata/profile, internal links, whitespace, and independent
policy/code review. W1 requires a tested generic preservation contract before
integration; W4 requires new RED/GREEN evidence and independent re-review.
No validation exception is authorized. Run the full gate only on the final
integrated content after focused findings have been resolved.

Implementation acceptance is W6, not these planning checks. Preserve test counts
as dated Task evidence, including pre-existing skips; never promote them into
permanent policy. Hosted CI, remote protection, runtime, deployment and provider
entitlement remain unverified.

## Rulings

- Existing SPEC-0173/Task 0006 owns integration planning; no new package or ID.
- The current user direction changes the target policy to permit an empty
  `.agents/` directory while retaining direct skill loading. It authorizes
  implementing that bounded change as part of the approved integration.
- W4 correction approvals are distinct from integration approval and from the
  exhausted prior attempt. No agent handoff resets the retry bound.
- W1's approved route is exact divergent-source preservation with a typed Task
  receipt, not a lifecycle edge or ID-specific exception. Implementation and
  negative tests must prove the route before any package is moved.
- No `docs/superpowers/plans/` artifact is created; this co-located Plan is the
  canonical execution design.

## Related Documents

- [Specification](spec.md)
- [Task 0006 evidence](tasks/tsk-0006-generated-evidence-and-final-verification.md)
- [Task 0001 historical lifecycle evidence](tasks/tsk-0001-lifecycle-and-red-contracts.md)
- [Task 0002 gate evidence](tasks/tsk-0002-gate-composition-convergence.md)
- [Task 0003 operation evidence](tasks/tsk-0003-script-and-operation-ownership.md)
- [Task 0004 fixture evidence](tasks/tsk-0004-test-and-fixture-convergence.md)
- [Task 0005 provider evidence](tasks/tsk-0005-document-and-provider-residue.md)
- [Stage 03 index](../README.md)
