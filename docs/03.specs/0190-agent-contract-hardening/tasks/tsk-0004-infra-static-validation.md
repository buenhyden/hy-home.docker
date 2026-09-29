---
title: "Fail-Closed Infrastructure Static Validation"
version: "1.0.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0190-TSK-0004"
parent_ids:
- "SPEC-0190"
- "SPEC-0190-PLAN-0001"
created: "2026-09-29"
---

# Fail-Closed Infrastructure Static Validation

## Objective

Implement Plan W4: required infrastructure checks fail closed, run only against
proven isolated synthetic inputs, and preserve exact safe result states.
Own R09/R34/R39 evidence with supporting units retaining their receipts.

## Inputs

- [Approved Spec](../spec.md), [approved Plan](../plan.md), W3 commit `60a5b209e`.
- Existing user approval covers local implementation, tests, independent review
  and logical commits. No real environment, secrets, daemon, install or remote action.
- Primary writer: infra-implementer; independent IaC/security review is read-only.
- Exact implementation paths: `.agents/skills/infra-validate/scripts/static-checks.sh`,
  `.agents/skills/infra-validate/SKILL.md`, and
  `tests/validation/test_agent_governance_ci_routing.py`. Root owns this Task.
  The retained public Compose validator is read-only and keeps its interface.

## Work Log

- Read-only caller audit identified real-checkout environment creation and
  unconstrained secret-path effects in the retained validator's default path.
- Prepared synthetic fake-PATH cases before implementation. Required tools,
  plugin detection, direct Git failure, mixed exit precedence and timeout
  termination must remain visible independently of configuration validity.
- Current tracked Compose graph contains absolute/unresolved external paths;
  unproven isolation must produce BLOCKED before Docker, not an inferred PASS.

- During W4 the owner explicitly revised future W9 from retaining `evals/`
  to migrating its four-file subsystem into `.agents/evaluations/`. Root
  amended Spec/Plan 1.1.0 and opened a read-only exact consumer audit before
  any move. W4 implementation scope and separate runtime boundaries are unchanged.

## Verification Evidence

- RED: focused helper class exited 1; five tests exposed six expected contract
  failures in missing-tool reporting, Git/plugin failure, unsafe graph handling,
  cwd-independent execution and isolation.
- Final focused class: 13/13 PASS; independent reviewer rerun in 9.798s.
- Final H: registered sanitized unittest adapter for
  `tests.validation.test_agent_governance_ci_routing -v`, exit 0,
  43/43 tests in 15.675s.
- `bash -n .agents/skills/infra-validate/scripts/static-checks.sh`: exit 0.
- `git diff --check --cached`: exit 0; exact three implementation files only.
- Actual helper: exit 2, PASS=9 FAIL=0 BLOCKED=6 NOT_RUN=2. The actual graph is
  outside the conservative supported subset; yamllint and shellcheck are absent.
  Compose checks are prerequisite-blocked, with no Docker/Compose/daemon access.
  Cleanup passed and no invocation-owned fixture remained.
- Fake tools prove routing, isolation, timeout and aggregation behavior; they
  do not establish real Compose or linter semantics. No installation occurred.
- Observed final index contained only the same reviewed three files; working
  copies matched the reviewed diff. Root adds only this Task and Plan evidence.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| R09 | W4 | Helper behavior PASS; real required-tool acceptance BLOCKED | infra-validate helper and skill |
| R34 | W4 | Existing entrypoint retained; focused and full H PASS | Existing command/helper contract |
| R39 | W4 | Failure/isolation contract PASS; cross-unit/native proof remains open | Existing helper regression tests |

## Review Evidence

Independent read-only IaC review CLEAR on the final exact three-file diff.
Review confirmed finite supported graph fields, conservative include-object and
extends rejection, independent lint after graph failure, live bounded Git capture,
isolated Python and child environment, no-follow/identity-checked inputs,
exclusive fixture writes, explicit lint configuration, owned cleanup, complete
child-exit metadata and FAIL-over-BLOCKED precedence. Helper is 788 lines.
The reviewed implementation preserves the public Compose validator unchanged.

## Commit Ledger

Task predecessors: draft `f37c9451d`, ready `46aaab815`, in-progress `9eb97f3d3`.
The user-directed future evaluation migration was recorded in `4aa3d0011`.
This completed local implementation Task is committed with its reviewed helper;
Git owns the implementation hash. Spec-wide environment acceptance stays open.

## Rulings

- Reuse the existing validator only within an invocation-owned repository-local
  fixture with synthetic values. Do not source or render the real environment.
- Git/Bash/Python with installed PyYAML/Docker Compose/yamllint and conditional
  shellcheck form the declared required set. Extra execution tools are explicit.
- Exit precedence is executed FAIL 1, incomplete required evidence BLOCKED 2,
  all applicable required checks PASS 0. Runtime/secret observations are NOT_RUN.
- Unknown include/extends/env/config/secret/build/bind paths block before Docker.
  A missing tool or current unprovable graph is an environment/control blocker;
  continue independent approved units without weakening requirements.

## Deferred Items

W10 retains actual tool-dependent, runtime/secret and provider/native acceptance.
The observed BLOCKED result cannot close those criteria or the overall Spec.
W5 owns the next serial change to style classification and the shared test file.
