---
title: "Infrastructure Agent Guide"
version: "0.2.1"
type: "common/agent-guide"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
---

# Infrastructure Agent Guide

## Overview

`infra/` holds the service definitions: tier and component directories own
their Compose fragments, build sources and mounted configuration, and the root
`docker-compose.yml` aggregates them through `include`. This guide routes an
agent that changes them. The human guide is [README.md](README.md).

## Scope

Every Compose fragment, Dockerfile, mounted configuration file and service
README under `infra/`, plus the `infra/*.json` policy inputs. Live container
state is out of scope: editing a file never starts, stops or recreates a
service.

## Working Rules

- Find the target tier and an existing service pattern first, and follow
  `common-optimizations.yml` for shared settings.
- Add a new fragment to the root `docker-compose.yml` `include` list, give
  each service its `profiles:`, and keep its profile membership in the Compose
  profile vocabulary policy in step.
- Reference secrets only by file or secret name. Never write a secret value
  in Compose, configuration or a README.
- Pin images through their projection or updater owner and record build pins in
  the owning Dockerfile.
- Update the service README with the Compose change, using the Service
  Documentation Rubric in [README.md](README.md), and keep the operations
  Guide's `implementation_services` mapping accurate.
- `docker compose up`, `down`, `restart` or any change to live data needs its
  own approval; static validation is the default.

## Canonical References

- [Bootstrap](../.agents/governance/bootstrap.md),
  [agentic governance](../.agents/governance/agentic.md),
  [approval boundaries](../.agents/governance/approval-boundaries.md),
  [environment constraints](../.agents/governance/environment-constraints.md),
  [quality standards](../.agents/governance/quality-standards.md).
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

## Verification

- `bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh`
- `python3 scripts/validation/check-operations-catalog.py`
- `python3 scripts/validation/check-supply-chain-policy.py`

## Related Documents

- [Infrastructure README](README.md)
- [Operations index](../docs/05.operations/README.md)
- [Secret management](../secrets/README.md)
