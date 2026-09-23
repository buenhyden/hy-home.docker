---
title: "Conftest Operations Policy"
version: "1.0.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "POL-0095"
parent_ids:
- "AD-0009"
created: "2026-09-23"
---

# Conftest Operations Policy

## Overview

The Rego rules under `infra/09-tooling/conftest/policy/` are an executable
subset of the repository's container baseline. They add no new rule; each one
restates a control another policy already owns.

## Policy Scope

The rules, their allowlists, the job's access and how a failure is resolved.

## Controls

- Every rule has a unit test in the same directory, and the job runs
  `conftest verify` before testing the source; a rule without a failing and a
  passing case is not merged.
- An allowlist entry (for example `cadvisor` for privileged) names the service
  and the reason in the policy file. Allowlists grow only by a reviewed change.
- A new `deny` must pass on the current source before it is merged; a rule the
  source cannot meet starts as `warn`.
- The job mounts only `infra/` read-only, runs without a network and as a
  non-root user. It must never mount `secrets/`, `.env` or the Docker socket.
- Fix the declaration, not the rule, when a `deny` fires.

## Exceptions

None beyond the allowlists in the policy files.

## Verification

`conftest verify` (policy unit tests) and a clean `conftest test` over all
Compose files and Dockerfiles; a deliberately bad file must fail every rule.

## Review Cadence

Review when a container baseline control changes, on a Conftest or OPA major
upgrade, and whenever an allowlist entry is added.

## Traceability

- [Guide](guide.md) (`GDE-0095`)
- [Runbook](runbook.md) (`RUN-0095`)
- [Compose profile vocabulary](../../00-workspace/0078-compose-profile-vocabulary/policy.md)

## Related Documents

- [Conftest Compose source](../../../../../infra/09-tooling/conftest/docker-compose.yml)
- [Dependency version management](../../00-workspace/0086-dependency-version-management/policy.md)
