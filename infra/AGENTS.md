---
title: "Infrastructure Agent Guide"
version: "0.4.2"
type: "common/agent-guide"
status: "active"
owner: "@buenhyden"
updated: "2026-11-19"
---

# Infrastructure Agent Guide

## Scope

### Allowed Scope

#### Allowed Surface

`infra/` holds the service definitions: tier and component directories own
their Compose fragments, build sources and mounted configuration, and the root
`docker-compose.yml` aggregates them through `include`. This guide routes an
agent that changes them. The human guide is [README.md](README.md).

Every Compose fragment, Dockerfile, mounted configuration file and service
README under `infra/`, plus the `infra/*.json` policy inputs.

#### Non-goals

Live container state is out of scope: editing a file never starts, stops or
recreates a service.

### Instruction Precedence

When this guide and the owner of a rule it summarizes disagree, the owner wins
and this guide is corrected
([documentation protocol](../docs/00.workspace/03.process/documentation-protocol.md#readme-and-agentsmd)).
[Bootstrap](../.agents/governance/bootstrap.md#authority-and-precedence)
sets the full precedence order; a folder guide routes only and never overrides
canonical governance or a Stage contract.

## Workflow

### Intake

- [Bootstrap](../.agents/governance/bootstrap.md),
  [agentic governance](../.agents/governance/agentic.md),
  [approval boundaries](../docs/00.workspace/04.quality/approval-boundaries.md),
  [environment constraints](../.agents/governance/environment-constraints.md),
  [quality standards](../docs/00.workspace/04.quality/quality-standards.md).
- Roles: [`infra-implementer`](../.agents/roles/infra-implementer.md),
  [`iac-reviewer`](../.agents/roles/iac-reviewer.md),
  [`security-auditor`](../.agents/roles/security-auditor.md),
  [`drift-detector`](../.agents/roles/drift-detector.md).
- Skills: [`docker-compose-patterns`](../.agents/skills/docker-compose-patterns/SKILL.md),
  [`compose-stack-agent`](../.agents/skills/compose-stack-agent/SKILL.md),
  [`infra-validate`](../.agents/skills/infra-validate/SKILL.md),
  [`infra-cross-validate`](../.agents/skills/infra-cross-validate/SKILL.md),
  [`container-threat-modeling`](../.agents/skills/container-threat-modeling/SKILL.md).
- Hook rules: [`block-plaintext-secret-compose`](../.agents/governance/hooks/hookify.block-plaintext-secret-compose.md);
  Claude delivers the Compose pre-check through `.claude/hooks/docker-compose-pre.sh`,
  Codex through `.codex/hooks.json`.
- Provider loading: [Claude adapter](../.claude/provider.md),
  [Codex adapter](../.codex/provider.md).

### Execution

#### Inspect and Change

- Find the target tier and an existing service pattern first, and follow
  `common-optimizations.yml` for shared settings.
- Add a new fragment to the root `docker-compose.yml` `include` list, give
  each service its `profiles:`, and keep its profile membership in the Compose
  profile vocabulary policy in step.
- Update the service README with the Compose change, using the Service
  Documentation Rubric in [README.md](README.md), and keep the operations
  Guide's `implementation_services` mapping accurate.

#### Local Obligations

- Pin images through their projection or updater owner and record build pins in
  the owning Dockerfile.

## Boundaries

### Authority

Stop and report when this guide and its canonical owner disagree (the owner
wins and this guide is corrected), when an action needs an approval that
[approval boundaries](../docs/00.workspace/04.quality/approval-boundaries.md)
has not granted, or when a required check fails.

### Secrets and External Effects

- Reference secrets only by file or secret name. Never write a secret value
  in Compose, configuration or a README.
- `docker compose up`, `down`, `restart` or any change to live data needs its
  own approval; static validation is the default.

## Verification

### Checks

- `bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh`
- `python3 scripts/validation/check-operations-catalog.py`
- `python3 scripts/validation/check-supply-chain-policy.py`

### Reporting

#### Evidence and Limits

Record each check's command, revision and exit in the current Task. These
checks are static or local; they do not prove runtime state, native provider
delivery, remote enforcement or owner acceptance.

#### Handoff

Record progress, decisions and evidence in the current Task, and leave the
next owner named there. Human-facing and related documents:

- [Infrastructure README](README.md)
- [Operations index](../docs/05.operations/README.md)
- [Secret management](../secrets/README.md)
