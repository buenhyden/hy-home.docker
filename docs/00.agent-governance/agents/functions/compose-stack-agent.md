---
layer: agentic
---

# compose-stack-agent

## Overview

Reviews Docker Compose service definitions in `infra/` against QW-001~005
baseline criteria: restart policies, healthchecks, no-new-privileges, resource
limits, and secrets wiring.

## Purpose

Enforce quickwin baseline compliance for a single infra tier without mass-editing
all 47 compose files at once.

## Scope

**Covers:**

- Healthcheck probe design (HTTP, TCP, exec)
- Restart policy validation (`unless-stopped`)
- Resource limit presence (cpus, mem_limit)
- Secrets wiring correctness

**Excludes:**

- Security threat modeling (handled by container-threat-modeling)
- Full compose syntax validation (handled by infra-validate)

## Structure

- Reads spec from `docs/03.specs/<tier>/spec.md`
- Runs `bash scripts/validation/check-quickwin-baseline.sh`
- Proposes targeted edits to a single tier

## Agents

- **infra-implementer** — primary caller

## Skills

- `.claude/skills/compose-stack-agent/skill.md`

## Usage

- **Inputs:** target tier path, baseline check results, service spec
- **Outputs:** updated compose file, gap summary, post-edit validation output

## Related Documents

- `../../scopes/infra.md`
- `../README.md`
