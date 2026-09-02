---
title: AI Capability Specification
version: 1.0.0
type: sdlc/spec
layer: specs
status: active
owner: "@buenhyden"
artifact_id: SPEC-0009
parent_ids:
  - AD-0013
  - AD-0023
created: 2026-07-05
updated: 2026-09-01
---
# AI Capability Specification

## Overview

This specification defines the current local AI serving capability provided by
Ollama and Open WebUI under infra/08-ai/.

## Boundaries and Inputs

- Input architecture: AD-0013, AD-0023, and their active decisions.
- In scope: Ollama, Ollama exporter, Open WebUI, Compose configuration,
  networks, health, storage, gateway, and telemetry integration.
- Out of scope: model quality claims, provider entitlement, user-global model
  configuration, and external hosted inference.

## Behavior Contract

- Ollama provides the tracked local inference endpoint and persistent model
  state.
- Open WebUI consumes the declared Ollama endpoint and exposes only its tracked
  gateway boundary.
- The exporter publishes operational metrics without exposing prompt, token,
  credential, or model data.
- Model availability is observed at runtime and is never inferred from a
  document or provider catalog.

## Technical Approach

Ollama and Open WebUI retain independent service directories joined through
infra_net. Common optimization, gateway, security, and observability contracts
are composed from their current owners. Provider-model evaluation remains an
Agent-governance concern and does not alter this runtime capability.

## Interfaces and Data

Internal inference, Web UI, and metrics endpoints follow the tracked Compose
definitions. Model files and application state remain in declared volumes;
secrets are injected through repository contracts and never recorded in
documentation evidence.

## Failure Modes and Guardrails

Unavailable models, failed healthchecks, invalid endpoint routing, excessive
resource use, or secret-bearing output blocks runtime acceptance. Static
configuration success alone is not a live model claim.

## Acceptance Contract

- AI profiles render with the current Compose configuration.
- Tier hardening and template security checks pass.
- Ollama, exporter, and Open WebUI Operations procedures match the tracked
  topology.
- No migration or phase document is required as current input.

## Traceability

- [REQ-0020](../../01.requirements/0020-ai-optimization-hardening.md)
- [AD-0013](../../02.architecture/descriptions/0013-open-webui-architecture.md)
- [AD-0023](../../02.architecture/descriptions/0023-ai-optimization-hardening-architecture.md)
- [AI Operations catalog](../../05.operations/catalog/08-ai/README.md)
