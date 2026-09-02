---
title: Security Capability Specification
version: 1.0.0
type: sdlc/spec
layer: specs
status: active
owner: "@buenhyden"
artifact_id: SPEC-0003
parent_ids:
  - AD-0018
created: 2026-07-05
updated: 2026-09-01
---
# Security Capability Specification

## Overview

This specification defines the current Vault and Vault Agent capability under
infra/03-security/. It is a living implementation contract, not a rollout
phase or future HA promise.

## Boundaries and Inputs

- Input architecture: AD-0018 and the Vault decisions linked from it.
- In scope: Vault configuration, policies, AppRole files, templates, health,
  persistent state, and Compose integration.
- Out of scope: application business configuration, external KMS/HSM
  operation, and undeployed HA topology.

## Behavior Contract

- Vault stores secret source data through the configured KV-v2 paths.
- Vault Agent authenticates through AppRole, maintains its bounded token state,
  and renders service-scoped output under /vault/out.
- Placeholder paths and plaintext secret values are rejected from tracked
  configuration.
- Vault and Vault Agent expose health signals suitable for bounded validation.

## Technical Approach

The implementation uses infra/03-security/vault/docker-compose.yml and its
configuration, policy, and template files. The Compose services inherit the
current common optimization contract and join the repository network. Raft
multi-node, auto-unseal, or remote audit expansion requires a separately
approved current Requirement and ADR.

## Interfaces and Data

- KV-v2 source path family: secret/data/hy-home/<tier>/<service>.
- Agent token state: /vault/agent/token.
- Rendered service output: /vault/out/<service>/<key>.
- Secret values never enter documentation or validation output.

## Failure Modes and Guardrails

Missing AppRole material, sealed Vault state, path/key mismatch, unhealthy
Agent, or missing render output fails closed. Operators follow the Vault
runbook; an Agent may not invent, print, or recover secret values.

## Acceptance Contract

- Security and core Compose profiles render successfully.
- scripts/hardening/check-all-hardening.sh 03-security passes.
- scripts/validation/check-template-security-baseline.sh passes.
- Current Operations policy and runbook describe the same topology and failure
  boundary.

## Traceability

- [REQ-0015](../../01.requirements/0015-security-optimization-hardening.md)
- [AD-0018](../../02.architecture/descriptions/0018-security-optimization-hardening-architecture.md)
- [Vault policy](../../05.operations/catalog/03-security/0016-vault/policy.md)
- [Vault runbook](../../05.operations/catalog/03-security/0016-vault/runbook.md)
