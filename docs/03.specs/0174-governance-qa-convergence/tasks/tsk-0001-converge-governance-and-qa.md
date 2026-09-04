---
title: "Governance and QA Convergence Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
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
- Baseline: `591e3c607f97aa34739f41288b5243f0cd4f0aac`.
- Branch: `codex/governance-qa-convergence`; isolated worktree, initially clean.
- Open PRs #140 and #141 overlap; their branches are not modified by this task.
- Remote mutation scope: this feature branch and its PR only. Recovery is logical
  revert or closing the unmerged PR. No runtime, secret, protection, or merge change.

## Work Log

- Retrieved committed repository objects through a read-only temporary Actions
  snapshot. The temporary workflow must be removed from the delivered tree.
- Inspected canonical provider registry, renderer, contracts, hooks, workflow
  definitions, active SPEC-0172, Stage 99 templates, and open PR overlap.
- Baseline provider/renderer/contract tests: 55 tests, exit 0.
- Hosted baseline full run `33879597896` failed when an aggregate environment
  selected incompatible Compose services. Independent profile checks had passed.
- Re-read remote `main`: code baseline unchanged; required contexts now read
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
- Regenerated the LLM Wiki indexes and security readiness snapshot through their
  maintained generators. Fixed the new Spec's initially missing index row.

## Verification Evidence

| Check | Outcome | Boundary |
| --- | --- | --- |
| Baseline provider tests | PASS, 55 tests | baseline only |
| Candidate provider/native/renderer tests | PASS, 57 tests | regression after observed failing tests |
| Hook and provider parity tests | PASS, 25 tests | existing safety controls retained |
| Gate/workflow tests | OK, 63 tests, 11 pre-existing skips | includes rejection and de-duplication regressions |
| Provider renderer | PASS, 2 providers, 0 drift | static translation; not native account entitlement |
| Workflow contract | PASS, 6 workflows, 8 jobs, 8 Actions | temporary transport workflows excluded from delivered tree |
| Metadata repository contracts | PASS, 0 violations | registered document and template structure |
| Document links | PASS, 685 documents, 5,772 links | traceability on candidate tree before this evidence update |
| Lifecycle and recovery | PASS, 0 violations | preservation integrity, not historical-content cleanup |
| Compose selection | PASS, every-declared, 28 selections, 232 services | configuration validation; no live deployment |
| Public local full, initial complete attempt | FAIL, 3 cleanup subcases | stopped at runner lifecycle regression; not a full pass |
| Identical cleanup regression under init | PASS | no runner deadline, skip, assertion, or production change |
| Public local full under init | pending | result must be recorded after the complete command ends |
| Candidate hosted QA | pending | not inferred from local or other PR results |

The initial full run retained zombie descendants with parent PID 1 after the
unchanged 250 ms cleanup bound. A task-local Linux child-subreaper reproduced a
proper init environment and the same failing test passed. The task-local probe
and init shim are not new repository gates or fixture requirements. Containerized
local QA needs an init process; the canonical runner and lifecycle tests were not
weakened. A clean Python virtual environment also isolates the gate's generated
bootstrap from unrelated environment-managed Python startup hooks.

The temporary source and tool acquisition runs passed, but neither is QA evidence.
The complete final candidate must remove every temporary acquisition/transport
workflow. Full hosted results and independent reviews remain separate boundaries.

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
- Hosted full QA, fork-token automation behavior, and independent code/policy
  review. The local scanner remains intentionally CI-routed in the existing
  executable contract; this candidate does not claim newly supported local SARIF.
- Integration of overlapping PRs #140 and #141. Their branches remain intact;
  maintainers must re-evaluate the common diff rather than blindly merge both.

No deployment, provider entitlement probe, global configuration, branch-protection
mutation, tag, release, or PR merge is authorized by this repository-change scope.
