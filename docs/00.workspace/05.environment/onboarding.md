---
title: "Environment Onboarding"
version: "0.1.0"
type: "governance/control"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-19"
created: "2026-11-19"
observed_at: "2026-11-19"
review_cycle: "on-tool-change"
---

# Environment Onboarding

## Overview

What a contributor prepares once to work in this workspace, and the first
checks that show the environment is ready. The setup steps themselves stay with
their owners: the [repository README](../../../README.md) for the Docker host,
`.env` and secret layout, the [scripts README](../../../scripts/README.md) for the
validation toolchain, and the [tests README](../../../tests/README.md) for test
runs. This guide connects them and names the boundaries between environments.

## Scope

Included: a local development checkout on Linux with Git, Docker Engine and
Docker Compose v2, Python 3 and Bash. Excluded: the operating host's services,
real secret values, provider accounts and hosted CI, whose results a local run
never stands in for.

## Rules

### Supported environment

| Need | Source of truth |
| --- | --- |
| Git, Docker Engine, Docker Compose v2, a local `.env` from `.env.example`, required files under `secrets/` | [Repository README prerequisites](../../../README.md#prerequisites) |
| Python validation dependencies | `scripts/requirements.txt`, installed from the hash lock `scripts/requirements-controller.lock` |
| Opt-in integration tests | `tests/requirements-integration.txt` and a Docker daemon |

### Python environment

Install the hash lock into its own venv and put that venv's `bin` first on
`PATH` before running scripts or tests. Distribution Python packages can be
older: with `jsonschema` 4.10 there is no `referencing`, and the secret
catalog, SMTP generator, root resource, wiki preparation and metadata sync tests
fail on import or on a nested `python3` call, because some scripts call the
`python3` on `PATH`.

```bash
python3 -m venv .venv
.venv/bin/pip install --require-hashes -r scripts/requirements-controller.lock
export PATH="$PWD/.venv/bin:$PATH"
```

`.venv/` is ignored by Git. Never install into the system interpreter to make a
check pass.

### First checks

Run these from the repository root after the setup above. None of them changes
a running service.

```bash
bash scripts/validation/validate-docker-compose.sh --preflight
python3 scripts/validation/run-ci-gate.py --profile changed --explain
PYTHONPATH=. python3 -m unittest tests.lib.test_surface_ownership
```

The preflight checks `.env`, required secret and certificate files, key
directories and external networks without creating them. The gate explain
lists what a change would run without running it. A local result is local
evidence only; the pull request's hosted checks own candidate acceptance.

### Environment boundaries

- A worktree, the HOME operating checkout and a LAB topology are different
  environments; a result in one is not evidence for another.
- The local agent tooling (memory, capture, analysis, forecast, dispatch,
  observe) is maintained through [harness maintenance](../06.maintenance/harness-maintenance.md).
- Secret values are never copied into a checkout, a log or evidence; only
  paths and IDs are recorded.

## Evidence

### Provenance

Written on 2026-11-19 by SPEC-0212 TSK-0097 from the repository, scripts and
tests READMEs at `main` `eadd81adc`. On that day nine test modules failed under
the system `python3` for lack of `referencing` and passed with the hash-locked
venv first on `PATH`.

### Refresh Triggers

- A prerequisite, lock file or first-check command changes in its owner README.
- A new environment class is added.

## Related Documents

- [Harness maintenance](../06.maintenance/harness-maintenance.md)
- [Repository README](../../../README.md)
- [Scripts README](../../../scripts/README.md)
- [Tests README](../../../tests/README.md)
