---
title: "Fail-Closed Infrastructure Static Validation"
version: "0.1.0"
type: "sdlc/task"
status: "ready"
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

## Verification Evidence

NOT_RUN: W4 RED/GREEN H, Bash syntax, available lint and isolated structural
acceptance. Fake binaries prove helper behavior, not real Compose correctness.
No installed yamllint/shellcheck was observed during preflight; do not install.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| R09 | W4 | NOT_RUN | infra-validate helper and skill |
| R34 | W4 | NOT_RUN | Existing command/helper contract |
| R39 | W4 | NOT_RUN | Existing helper regression tests |

## Review Evidence

Implementation review pending. Review must cover no-follow tracked-source
copying, repository-local owned temporary cleanup, graph validation before
Compose, sanitized child environment, bounded execution and safe diagnostics.

## Commit Ledger

Root creates and validates real draft, ready and in-progress predecessors
before authorizing implementation. No W4 implementation commit yet.

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

Real runtime/secret and provider/native observations remain separately scoped.
W5 owns style classification; no concurrent writer may change the shared test file.
