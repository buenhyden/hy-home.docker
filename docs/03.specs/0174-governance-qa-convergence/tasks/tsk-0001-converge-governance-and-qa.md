---
title: "Governance and QA Convergence Task"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "specs"
artifact_id: "SPEC-0174-TSK-0001"
parent_ids:
- "SPEC-0174"
- "SPEC-0174-PLAN-0001"
created: "2026-09-05"
---

# Governance and QA Convergence Task

## Objective

Implement [SPEC-0174](../spec.md) against the named `main` baseline, preserving
other in-progress work and recording each verified logical change.

## Inputs

- User request dated 2026-09-05 (Asia/Seoul): retire shared runtime projections,
  consolidate common governance and provider mechanics, simplify QA/CI/gates and
  fixtures, audit current and historical documents, and create logical commits.
- Initial baseline: `591e3c607f97aa34739f41288b5243f0cd4f0aac`.
- Integrated upstream: `4c6d211129615eab372d720ebd209b6c27618c86`.
- Branch: `codex/governance-qa-convergence`; isolated worktree, initially clean.
- PRs #140 and #141 overlapped at initial inspection and were later merged by
  upstream. This task preserves both through the integrated main commit and does
  not mutate either source branch. Delivery is draft PR #142.
- Remote mutation scope: this feature branch and its PR only. Recovery is logical
  revert or closing the unmerged PR. No runtime, secret, protection, or merge change.

## Work Log

### Approved closeout review — 2026-09-05

The user requested finishing existing packages without new Spec/Plan/Task IDs,
merging local histories, and retaining a push-ready main without publishing.
SPEC-0173 owns the accepted integration and final verification. Independent
provider, gate, Python and policy reviews passed on the resolved main tree.
The temporary `governance-audit-snapshot.yml` transport was removed as already
required by this Task; no workflow was dispatched and no remote state changed.
This checkpoint enters ready for the approved handoff only. The original
execution and hosted observations below remain historical evidence.

### Original execution observations

- Retrieved committed repository objects through a read-only temporary Actions
  snapshot. The temporary workflow must be removed from the delivered tree.
- Inspected canonical provider registry, renderer, contracts, hooks, workflow
  definitions, active SPEC-0172, Stage 99 templates, and open PR overlap.
- Baseline provider/renderer/contract tests: 55 tests, exit 0.
- Hosted baseline full run `33879597896` failed when an aggregate environment
  selected incompatible Compose services. Independent profile checks had passed.
- At the initial protection readback, the code baseline was unchanged; contexts read
  `validation-changed` and `validation-full`. Earlier 12-context evidence is
  historical and is not the current control-plane state. This task changed no
  protection setting.

- Removed 38 tracked shared projections and their registry/renderer routes.
  Claude retains native projections; 14 Codex role adapters now explicitly read
  their canonical Stage 00 procedures. Negative retirement tests also preserve
  unknown content and reject broken symlink reintroduction without traversal.
- Consolidated Compose execution into one leaf per selected profile and shared
  the frontend dependency-install node. Reachable typed gate count changed from
  73 to 70 without removing the independent Compose selections or security checks.
- Corrected Greeting comment-target permissions, keeping the existing event
  model and least-write scope. Fork read-only token behavior remains unverified.
- Consolidated provider/GitHub QA instructions under the Stage 00 matrix and
  made PR fixture evidence conditional on the behavior that actually changed.
- Reused bounded changes from PR #140 at
  `06fd6ab191bc9d74c988088181a34844d1b41b17` (Compose workflow and contract tests)
  and PR #141 commits `c36846ff3a8eec982f20ba24bb02bf6137f2da3e`
  (provider QA routing) and `576c96d7c79e5da92c9338291b4918b306e299ae`
  (common QA policy consolidation). Additional retirement, de-duplication,
  permission, documentation, and fixture changes are verified in this candidate.
  Neither PR's prior test results are this candidate's results.
- Integrated the later upstream main commit without replacing its Dockerfile,
  hardening, document-lifecycle, template, or in-progress SPEC-0172 changes.
  Resolved two overlapping files by retaining the merged shared QA wording in
  the PR template and the added gate/workflow regression tests. The resulting
  implementation tree is `db9fbc6101ecb69d535a900720dabc0494194f47`.
- Published five logical implementation/cleanup/integration commits on the
  feature branch through a non-force ref update. The three temporary acquisition
  and reconstruction workflows are absent from the delivered implementation.
- The optional `graphify` CLI is unavailable in this execution environment;
  its graph refresh was not run. Both maintained LLM Wiki generators passed
  freshness checks after the evidence edits. Ruff check and format verification
  passed for all 15 changed Python files without altering them.
- Regenerated the LLM Wiki indexes and security readiness snapshot through their
  maintained generators. Fixed the new Spec's initially missing index row.

## Verification Evidence

Evidence checkpoint: 2026-09-05 06:51 Asia/Seoul. Pending hosted results below
are observations at this checkpoint, not a claim of later workflow outcomes.
The PR conversation records later remote check conclusions without making a
self-referential new code commit for each check result.

| Check | Outcome | Boundary |
| --- | --- | --- |
| Baseline provider tests | PASS, 55 tests | baseline only |
| Candidate provider/native/renderer tests | PASS, 57 tests | regression after observed failing tests |
| Hook and provider parity tests | PASS, 25 tests | existing safety controls retained |
| Gate/workflow tests | OK, 63 tests, 11 pre-existing skips | includes rejection and de-duplication regressions |
| Provider renderer | PASS, 2 providers, 0 drift | static translation; not native account entitlement |
| Workflow contract | PASS, 6 workflows, 8 jobs, 8 Actions | temporary transport workflows excluded from delivered tree |
| Metadata repository contracts | PASS, 0 violations | rechecked after integration and evidence edits |
| Document links | PASS, 685 documents, 5,772 links | rechecked after integration and evidence edits |
| Lifecycle and recovery | PASS, 0 violations | preservation integrity, not historical-content cleanup |
| Compose selection | PASS, every-declared, 28 selections, 232 services | configuration validation; no live deployment |
| Public local full, initial complete attempt | FAIL, 3 cleanup subcases | stopped at runner lifecycle regression; not a full pass |
| Identical cleanup regression under init | PASS | no runner deadline, skip, assertion, or production change |
| Public local full under init, initial baseline candidate | PASS, exit 0 | tree `72eb9b1528501e639c06524a9a2bfefb2af0f924`; not the later upstream integration |
| Integrated gate/workflow regressions | OK, 63 tests, 11 existing skips | 52 executed, 0 failures, tree `db9fbc6101ecb69d535a900720dabc0494194f47` |
| Integrated public local full | PASS, exit 0 | tree `db9fbc6101ecb69d535a900720dabc0494194f47`; clean venv and proper init semantics |
| Integrated hosted full | running at checkpoint, run `33922214372` | actual GitHub environment on the identical implementation tree; not the protected PR check |
| PR required QA | running at checkpoint, run `33922559580` | PR #142 head `dbee92c0177c407fb9360d819b0d82f30e5a666a` |
| PR Greeting and Labeler | PASS, runs `33922559860` and `33922559452` | this same-repository PR only; not fork-token or actual comment-write coverage |

The initial full run retained zombie descendants with parent PID 1 after the
unchanged 250 ms cleanup bound. A task-local Linux child-subreaper reproduced a
proper init environment and the same failing test passed. The task-local probe
and init shim are not new repository gates or fixture requirements. Containerized
local QA needs an init process; the canonical runner and lifecycle tests were not
weakened. A clean Python virtual environment also isolates the gate's generated
bootstrap from unrelated environment-managed Python startup hooks.

The temporary source and tool acquisition runs passed, but neither is QA evidence.
All three temporary acquisition/transport workflows have been removed from the
implementation tree. Two initial reconstruction runs failed before QA and are
not QA evidence. Full hosted results and independent reviews remain separate
boundaries. A tree-level hosted result does not substitute for the final PR head
check, SARIF-upload acceptance, or independent review.

## Review Evidence

Self-review covered the exact candidate diff, generated ownership, retired-path
rejection, unchanged provider controls, gate composition, and permission scope. Independent policy/code review and CODEOWNERS approval
have not been obtained; do not infer them from implementation or test output.

## Commit Ledger

Commit by independently reviewable units: provider retirement and its contract;
QA execution and regressions; common documentation and evidence; temporary
transport removal. Commit IDs are available in the delivered branch/PR, avoiding
self-referential commit hashes inside the file being committed.

## Rulings

- Keep provider selection, permissions, hook control, and secret safety intact.
- Do not claim `.codex/skills` auto-discovery. Codex reads canonical procedures
  explicitly after the shared runtime directory is removed.
- Unavailable dependencies, hosted results, or reviews are recorded as unverified.

## Deferred Items

The user request is not fully complete. Acceptance remains open for:

- Retiring incompatible active historical audit/research content, including
  AUD-0019 through AUD-0032 and stale runtime statements in RES-0002. The exact
  11-report/161-criterion audit contract, semantic-closure gate, generated audit
  matrix, and their fixtures must be retired or generalized together; their
  existing passing checks do not prove the prose matches current governance.
- A full semantic review and consolidation of every SDLC term/template and every
  in-progress document. This candidate fixes the coupled runtime README route,
  PR evidence, current provider documents, and its own Spec/Plan/Task package;
  it does not claim an exhaustive semantic corpus rewrite.
- Hosted final acceptance, fork-token automation behavior, and independent
  code/policy review. The local scanner remains intentionally CI-routed in the existing
  executable contract; this candidate does not claim newly supported local SARIF.
- Final PR-head acceptance and independent review after the evidence-only
  update. Do not infer either from an earlier tree or workflow result.

No deployment, provider entitlement probe, global configuration, branch-protection
mutation, tag, release, or PR merge is authorized by this repository-change scope.
