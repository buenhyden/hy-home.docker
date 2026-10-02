---
title: "Path-Aware Pull Request Regressions Implementation Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-02"
layer: "specs"
artifact_id: "SPEC-0200-PLAN-0001"
parent_ids:
- "SPEC-0200"
created: "2026-10-02"
---

# Path-Aware Pull Request Regressions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development or superpowers:executing-plans to
> implement this plan task by task. Steps use checkbox syntax for tracking.

## Objective

**Goal:** Keep one protected PR check while omitting two costly document
implementation regression groups from documentation-only candidates.

**Architecture:** Reuse the existing public gate's changed-root rules. Detach
the two named regression leaves from the document-corpus aggregate, register
them as bounded optional document-lifecycle roots, and select them when their
source, tests, registry or contract changes. The manual full profile retains
both leaves without a new workflow or selector.

**Tech Stack:** Python 3.14, unittest, the existing JSON gate contract,
GitHub Actions, Markdown and the Stage 99 document registry. No dependency
addition.

**Spec:** [SPEC-0200](spec.md), approved by the user on 2026-10-02.

## Dependencies

### Global constraints

- Keep the required validation-changed job name, PR triggers, main-security and
  update-main-current jobs, and the manual full route unchanged.
- Keep the existing document validators and the operations-catalog route for
  operations docs. Remove no active test or script solely for latency.
- Preserve the fail-closed unknown-path behavior and the typed optional-root
  allowlist. Do not add a workflow-level PR path filter.
- Write Spec, Plan and Task prose in English; README and Stage 05 explanatory
  prose follow their registered Korean language.
- SPEC-0182 and SPEC-0193 remain active until their deferred runtime
  acceptance is observed. No dev branch is to be created.

### Review focus

1. A docs/05.operations-only candidate must retain operations-catalog and
   document validators; Task 2 adds a plan assertion for this path.
2. A docs/99.templates/registry.json change can alter document rules and must
   select both named regressions; Task 2 tests this owner.
3. A mixed known-document and unknown path must fail closed to the complete
   relevant roots; Task 2 retains the existing unknown-path assertion.
4. A future unauthorized optional root must be rejected at parse time; Task 2
   extends the mutation test with a known mandatory and an unknown gate ID.
5. Manual full must contain each named regression once after aggregate
   extraction; Task 2 adds an exact-count assertion.

**File map and ownership**

| File | Responsibility |
| --- | --- |
| .github/workflow-contract.yml | Gate DAG and changed-root path data; retain one execution owner. |
| scripts/lib/gate/ci_gate_contract.py | Bounded optional-root allowlist and exact aggregate-child contract. |
| tests/lib/gate/test_ci_gate_contract.py | Typed rule, known/unknown path and mutation tests. |
| tests/validation/test_ci_gate_plan.py | Concrete selected invocation sets for docs, code, mixed and full. |
| .agents/governance/quality-standards.md | Canonical phase matrix and corrected CI pre-commit wording. |
| .agents/knowledge/verification-surface-map.md | Current gate ownership and verification navigation, only if its existing prose needs correction. |
| .github/README.md or existing .github navigation owner | Explain path-aware regression routing only where current operator guidance exists. |
| docs/03.specs/0200-path-aware-pr-regressions/tasks/tsk-0001-path-aware-pr-regressions.md | Sole acceptance and hosted-run evidence ledger after lifecycle activation. |

The Plan does not pre-authorize an unrelated script deletion. W1 must inspect
live callers and record a consumer/replacement reason for every proposed
removal. If there is no justified candidate, record retention.

## Execution Sequence

0. **W0 — Lifecycle bootstrap.** Deliver this draft Spec and Plan via a
   protected PR, then advance registered Spec draft → review → approved →
   active and Plan draft → approved → active transitions on a trusted main
   base. Create Task 0001 only after both parents are active, then advance its
   draft → ready → in-progress transitions before implementation. The user has
   approved the written Spec; that approval does not itself assert repository
   status transitions.
1. **W1 — Baseline and dependency closure.** Reconfirm required status,
   remote branches, current timing, two target leaves, source imports,
   fixture readers, registry dependencies and every path prefix. Record
   phase ownership and script/test disposition in Task 0001.
2. **W2 — Routing with RED/GREEN proof.** Add focused failing selection and
   mutation tests. Change only the contract DAG, typed optional-root list
   and path rules needed to make them pass. Preserve all non-target leaves.
3. **W3 — Governance and delivery.** Correct stale skip-list prose, update
   existing navigation only where needed, run focused tests and one changed
   gate on the final candidate, obtain independent review, then deliver via
   protected PR. Compare hosted elapsed time with run 36939016845 and record
   main-push/tag results without replaying full QA.
4. **W4 — Lifecycle closure.** Advance Task and then Plan/Spec through their
   allowed terminal transitions with acceptance receipts and complete
   repository cleanup. Reconcile completed-package navigation separately;
   do not falsify SPEC-0182 or SPEC-0193 closure.

### Task 0: W0 — Register and activate the package

**Files:** Modify only this package's spec.md and plan.md lifecycle
metadata; create Task 0001 after both parents become active.

**Interfaces:** Produces a trusted active package and a current Task ledger
for W1–W4.

- [ ] Review the written Plan and execution method with the user.
- [ ] Push the draft package branch and merge its protected PR only after
  hosted validation-changed succeeds. Record PR, candidate SHA, run and merge
  SHA.
- [ ] On fresh main bases, advance each registered lifecycle edge with the
  changed-document checker and required hosted result. Do not compress
  transitions or edit main directly.
- [ ] Create Task 0001 in draft under active parents; validate its identity
  and lifecycle; advance draft → ready → in-progress on trusted main bases
  before W1 implementation begins.

### Task 1: W1 — Baseline and path ownership

**Files:** Read the gate contract, selector, target test imports and
manifest; write only Task 0001 evidence.

**Interfaces:** Produces a path → affected regression leaf table and a
baseline invocation set for Task 2.

- [ ] Record main/origin-main SHA, the remote required status and one recent
  successful PR timing. Confirm only main exists remotely.
- [ ] Trace both named leaves' imported code, fixtures and registry reads.
  List exact changed-root prefixes; include gate contract and tests.
- [ ] Record the current changed plan for a Stage 03-only path, an operations
  doc, a document implementation path and full. Capture all non-target
  invocation IDs so Task 2 can prove parity.
- [ ] Inspect each apparent one-off, duplicate, legacy or deprecated
  script/test by manifest, caller and gate reachability. Record retain or
  evidence-backed removal; no quota.

### Task 2: W2 — Select only relevant document regressions

**Files:** Modify .github/workflow-contract.yml,
scripts/lib/gate/ci_gate_contract.py,
tests/lib/gate/test_ci_gate_contract.py and
tests/validation/test_ci_gate_plan.py.

**Interfaces:** Consumes W1's path table. Produces unchanged public
run-ci-gate.py CLI with typed optional document roots.

- [ ] Add RED tests named
  test_document_only_plan_keeps_validators_and_omits_implementation_regressions,
  test_operations_doc_plan_keeps_catalog,
  test_document_owner_changes_select_regressions,
  test_mixed_unknown_path_keeps_document_regressions and
  test_full_plan_keeps_document_regressions_once. Assert exact target
  leaf IDs and retained validator IDs, not just plan length.
- [ ] Extend the existing changed-root mutation test to reject an
  unauthorized mandatory root, unknown root and duplicate prefix. Run
  python3 -m unittest tests.lib.gate.test_ci_gate_contract
  tests.validation.test_ci_gate_plan -v; confirm the new tests fail for
  the expected old routing.
- [ ] Remove only leaf.local-document-metadata-tests and
  leaf.document-governance-library-regressions from the
  local.document-corpus-lifecycle aggregate. Add both to the document-
  lifecycle suite roots and the exact aggregate-child model. Extend
  _OPTIONAL_CHANGED_ROOT_GATE_IDS with only these IDs and register W1's
  owner prefixes in changed_root_rules.
- [ ] Run the two focused unittest modules, the workflow-contract checker,
  and run-ci-gate.py --profile changed --explain for docs-only,
  implementation and mixed/unknown contexts using the focused plan tests;
  inspect actual changed and full CLI explanations. Confirm the intended
  leaves are selected or omitted and each full leaf appears once.
- [ ] Commit this independently reviewable behavior change using a
  conventional ci: message.

### Task 3: W3 — Align governance and verify the candidate

**Files:** Modify .agents/governance/quality-standards.md and only
necessary existing .github/ or verification-map guidance; update Task 0001.

**Interfaces:** Produces the final tracked policy and evidence needed for
acceptance criteria 1–6.

- [ ] Replace the stale claim that run-ci-precommit.sh sets its own SKIP
  list with its actual rejection of caller SKIP and pinned CI command.
  Describe the document-only and code-change PR routes without a second
  quality matrix.
- [ ] Run focused selector, workflow and document metadata checks. Run
  python3 scripts/validation/run-ci-gate.py --profile changed once on the
  final candidate; avoid rerunning full after a green PR result.
- [ ] Obtain an independent read-only final diff review and resolve
  actionable findings. Record skipped environment-specific gates honestly.
- [ ] Push the candidate PR, require hosted validation-changed success on
  the final SHA, merge through main protection and observe main-security
  then update-main-current. Compare hosted PR elapsed time with baseline,
  recording variance rather than promising a fixed speed.

### Task 4: W4 — Finish lifecycle and clean refs

**Files:** Modify only this package's Task, Plan, Spec and existing
Stage 03 navigation as required by their lifecycle states.

**Interfaces:** Produces terminal acceptance receipts and equal local,
origin and remote main refs.

- [ ] Map each Spec criterion 1–6 to exact Task evidence and permanent
  policy owner. Preserve any unresolved evidence as an explicit deferred
  item, not a completed assertion.
- [ ] Advance Task and Plan/Spec only through allowed transitions on
  protected PR bases, validating each candidate. Do not mark terminal
  status until all criteria are proved.
- [ ] Recheck all Stage 03 package statuses against Task evidence; correct
  stale navigation or contradictory completed-package receipt text without
  changing genuinely active SPEC-0182/SPEC-0193.
- [ ] Delete merged development branches and worktrees after comparing
  patch equivalence. Fetch and fast-forward local main; verify equality
  with origin/main and remote main plus main-current read-back.

## Risk and Rollback

A missing owner prefix could bypass the two regressions. Keep the parser's
closed allowlist, W1 dependency table, owner-path tests and unknown-path
fallback; if hosted evidence exposes a gap, revert the routing commit through
a protected PR. A regression moved out of the aggregate could vanish from
manual full; the exact-count test and workflow contract block that. No
runtime service, credential or release tag is changed.

## Verification

- RED/GREEN: python3 -m unittest tests.lib.gate.test_ci_gate_contract
  tests.validation.test_ci_gate_plan -v.
- Contract: python3 scripts/validation/check-github-workflow-contract.py.
- Document lifecycle: python3 scripts/validation/check-document-metadata.py
  --mode check-changed --base-ref origin/main, and
  python3 scripts/validation/check-document-corpus-lifecycle.py
  --base-ref origin/main.
- Integration: python3 scripts/validation/run-ci-gate.py --profile changed
  on the final candidate; full profile is available manually and is
  statically proven by exact-plan tests.
- Hosted: required validation-changed on the final PR SHA, main-security and
  update-main-current on merged main SHA. Compare PR wall-clock to run
  36939016845; a timing result alone never substitutes for gate parity.

## Rulings

The current protected branch has only validation-changed as a required
context. Workflow-level path filtering can leave it pending and is not
permitted. SPEC-0199 already removed phase-level duplicate public gates and
implemented main-current; this Plan changes only the expensive regression
selection inside that required PR gate. The existing selector is sufficient;
there is no reason to add a second workflow, gate runner or test framework.
