---
title: "Conftest Recovery Runbook"
version: "1.0.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "RUN-0095"
parent_ids:
- "GDE-0095"
created: "2026-09-23"
---

# Conftest Recovery Runbook

## When to Use

The `conftest` job exits non-zero.

## Procedure

1. Run it and read the first failing line:

   ```bash
   docker compose --profile policy-check run --rm conftest
   ```

2. A failure in the `verify` summary is a broken rule or test in
   `infra/09-tooling/conftest/policy/`; fix the Rego before anything else.
3. `FAIL - <file> - compose - service <name>: …` or `… - dockerfile - …`
   names the declaration and the rule. Fix the declaration: add the profile,
   pin the image, move the literal into a Docker secret, or add `--checksum`.
4. If the declaration is intended (a new privileged need, for example), change
   the allowlist in the policy file with its reason in a reviewed change.
5. Exit `2` or an `exceptions` count above zero means a file did not parse;
   the named file is invalid YAML or Dockerfile syntax.

## Evidence

Record the three summary lines (verify, compose, dockerfile) and the source
commit.

## Rollback or Recovery

The job changes nothing and holds no state.

## Escalation

Stop on any request to mount `secrets/`, `.env` or the Docker socket into the
job, or to turn a `deny` into a `warn` to make a failing change pass.

## Traceability

- [Guide](../guides/0095-conftest.md) (`GDE-0095`)
- [Policy](../policies/0095-conftest.md) (`POL-0095`)
- [Conftest Compose](../../../infra/09-tooling/conftest/docker-compose.yml)

## Related Documents

- [Conftest package README](../../../infra/09-tooling/conftest/README.md)
