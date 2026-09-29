---
title: "Compose Host Port Exposure Plan"
version: "0.3.0"
type: "sdlc/plan"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0188-PLAN-0001"
parent_ids:
- "SPEC-0188"
created: "2026-09-29"
---

# Compose Host Port Exposure Plan

## Objective

Bind the 35 flagged host port publications that [SPEC-0188](spec.md) lists to
the narrowest interface their consumers need, and make wildcard publication a
Conftest `deny`.

## Dependencies

- The owner's answers to the two Spec open questions.
- Docker available locally for `check-conftest-policy.sh`.

## Execution Sequence

1. W1: Record the 35 findings and each port's consumer in the Task (criteria
   1, 6).
2. W2: Scope the Conftest rule and add its tests, tests first (criterion 1).
3. W3: Bind Group C in `mng-db`, observability (`pyroscope`), `locust`,
   `supabase`, `opensearch`, `kafka`, and `valkey-cluster` to `127.0.0.1`,
   one commit per leaf (criterion 2).
4. W4: Add the LAN address key and bind Group B (`loki`, `tempo`, `alloy`,
   `mng-valkey`, `pg-router`, `nginx`) to it (criterion 3).
5. W5: Promote the rule to `deny` once the job reports zero findings
   (criterion 4).
6. W6: Update POL-0096, GDE-0096, POL-0095, GDE-0095, the Conftest README, and
   the affected service documents (criterion 5).
7. W7: Run `validate-docker-compose.sh`, the gate members including
   `check-conftest-policy.sh`, and both unit suites (criterion 6).

## Risk and Rollback

Each Compose leaf changes in its own commit, so reverting one commit restores
one leaf's bindings. No running service changes until an operator recreates
it.

## Verification

- `bash scripts/validation/check-conftest-policy.sh` reports no host
  publication findings, and `conftest verify` passes the new tests.
- `bash scripts/validation/validate-docker-compose.sh` passes.
- Changed-profile gate members, `tests/lib`, and `tests/validation` pass.

## Rulings

None yet.
