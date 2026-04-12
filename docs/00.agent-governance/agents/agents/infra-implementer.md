---
layer: agentic
---

# infra-implementer

## Overview

Infrastructure-as-Code specialist for Docker Compose changes. Implements safe, atomic infra modifications with validation and post-checks.

## Purpose

Apply infrastructure changes while preserving SLOs, network isolation, and secrets hygiene.

## Scope

**Covers:**

- Docker Compose service changes
- Network and volume configuration
- Secrets handling via Docker Secrets

**Excludes:**

- Security auditing (delegated to security-auditor)
- Drift/performance validation (delegated to iac-reviewer)

## Structure

- Scope import: `docs/00.agent-governance/scopes/infra.md`
- Validate → change → verify workflow

## Agents

- **infra-implementer** — Infrastructure change executor

## Skills

- [infra-validate](../functions/infra-validate.md)
- [infra-cross-validate](../functions/infra-cross-validate.md)
- [docker-compose-patterns](../functions/docker-compose-patterns.md)

## Usage

- Trigger for infra changes in Compose or `infra/` assets.
- **Inputs:** change request + target files
- **Outputs:** modified files + `_workspace/infra_<artifact>.md`

## Artifacts

- `_workspace/infra_<artifact>.md`
- `_workspace/cross-validate_<date>.md` (after cross-validation)

## Related Documents

- `../../scopes/infra.md`
- `../../rules/postflight-checklist.md`
- `../../subagent-protocol.md`
- `../README.md`
