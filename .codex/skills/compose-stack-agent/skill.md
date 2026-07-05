---
name: compose-stack-agent
description: >
  Review Docker Compose service definitions for hy-home.docker. Validates
  healthcheck presence, restart policies, secrets wiring, resource limits,
  and service layering against check-quickwin-baseline.sh criteria.
---

# compose-stack-agent

Reviews and improves Docker Compose service definitions in `infra/`.

## Trigger Examples

- "Review the healthcheck config for infra/03-security/"
- "Check if all services in infra/06-observability/ have restart policies"
- "Validate the compose stack for tier 04-data"

## Purpose

Enforce QW-001~005 baseline criteria and correct service-layer design for a
single infra tier or file. Does not mass-edit all 47 files at once.

## Bootstrap

1. Read `AGENTS.md` and `docs/00.agent-governance/scopes/infra.md`.
2. Read `graphify-out/GRAPH_REPORT.md`; treat as advisory if unhealthy.
3. Identify the target tier path under `infra/`.
4. Run `bash scripts/validation/check-quickwin-baseline.sh` to get current state.

## Working Rules

- Target one tier or file per invocation unless explicitly told otherwise.
- Never read or print secret values from `secrets/`.
- Healthcheck probes must match the service protocol (HTTP, TCP, exec).
- `restart: unless-stopped` is the default restart policy for stateful services.
- Resource limits (`cpus`, `mem_limit`) must be set before marking QW-004 done.
- Reference `docs/03.specs/` for the service spec before changing behavior.

## Inputs

| Input | Source |
| ----- | ------ |
| Target tier or compose file | User message |
| Baseline check results | `bash scripts/validation/check-quickwin-baseline.sh` |
| Service spec | `docs/03.specs/NNN-<tier>/spec.md` |

## Outputs

- Updated compose file with healthcheck, restart, and resource limit additions
- Summary of changes made and remaining gaps
- Verification output from `check-quickwin-baseline.sh` after edit

## Related Skills

- `infra-validate` — full compose validation after edits
- `security-audit` — security hardening review
- `policy-gate-agent` — QW baseline policy check
