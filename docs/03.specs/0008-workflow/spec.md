---
title: Workflow Capability Specification
type: specs/spec
layer: specification
status: active
owner: "@buenhyden"
artifact_id: SPEC-0008
parent_ids:
  - AD-0022
created: 2026-07-05
updated: 2026-09-01
---
# Workflow Capability Specification

## Overview

This specification defines the current Airflow and n8n workflow infrastructure
under infra/07-workflow/.

## Boundaries and Inputs

- Input architecture: AD-0022 and workflow decisions.
- In scope: Airflow and n8n Compose variants, dependencies, networks, health,
  configuration, secrets, and persistent state.
- Out of scope: business workflow definitions, external SaaS control planes,
  and unimplemented HA topology.

## Behavior Contract

- Airflow and n8n retain separate service, database, queue, worker, and
  management boundaries where tracked.
- Root profiles include only declared variants and preserve infra_net
  membership.
- Credentials use tracked secret references and health-dependent startup
  remains explicit.
- Floating images and undocumented runtime dependencies are not accepted.

## Technical Approach

Each workflow platform owns its Compose and development variant. Common
optimization, security, gateway, and observability contracts are composed at
the repository boundary. Deployment or scale expansion requires a new active
change packet rather than an informal phase.

## Interfaces and Data

Web management endpoints, worker queues, database connections, workflow state,
and volume mounts follow the tracked Compose definitions. No workflow payload
or credential is copied into Spec evidence.

## Failure Modes and Guardrails

Unhealthy database/queue dependencies, invalid network membership, secret
mismatch, or a variant that cannot render in its declared context fails closed.
Operators follow the matching Stage 05 subject.

## Acceptance Contract

- Workflow profiles and their selected variants render successfully.
- Tier hardening, template security, and link checks pass.
- Current Stage 05 guidance matches the tracked Airflow and n8n topology.
- No retired execution-stage path is required.

## Traceability

- [REQ-0019](../../01.requirements/0019-workflow-optimization-hardening.md)
- [AD-0022](../../02.architecture/descriptions/0022-workflow-optimization-hardening-architecture.md)
- [Workflow Operations catalog](../../05.operations/catalog/07-workflow/README.md)
