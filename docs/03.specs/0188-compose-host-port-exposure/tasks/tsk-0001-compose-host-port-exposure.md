---
title: "Compose Host Port Exposure"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0188-TSK-0001"
parent_ids:
- "SPEC-0188"
- "SPEC-0188-PLAN-0001"
created: "2026-09-29"
---

# Compose Host Port Exposure

## Objective

Execute W1 through W7 of the [Plan](../plan.md) and record the evidence for
every acceptance criterion of [SPEC-0188](../spec.md).

## Inputs

- The owner's request of 2026-09-29 to analyze the 35 Conftest warnings and
  plan their remediation.
- `check-conftest-policy.sh` on `main` at `d6b68128e`: 299 tests, 264 passed,
  35 warnings, 0 failures; policy unit tests 66 passed.
- A read-only survey of each flagged service's profiles, routes, consumers,
  and documented exposure intent.

## Work Log

- 2026-09-29: Spec, Plan, and Task drafted on branch
  `fix/compose-host-port-exposure`. Execution waits for owner approval and
  answers to the Spec open questions.

## Verification Evidence

Not started.

## Review Evidence

None yet.

## Commit Ledger

None yet.

## Rulings

None yet.

## Deferred Items

- `VALKEY_MNG_HOST_POST` is a consistently used misspelling of a host-port key.
  Renaming it changes an operator `.env` key, so it needs its own change.
- POL-0047 and POL-0049 call Pyroscope and Tempo `OPTIONAL`, while POL-0078
  adds `profiling` and `tracing` to HOME.
