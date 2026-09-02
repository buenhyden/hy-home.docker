---
title: Data Capability Specification
type: sdlc/spec
layer: specs
status: active
owner: "@buenhyden"
artifact_id: SPEC-0004
parent_ids:
  - AD-0019
created: 2026-07-05
updated: 2026-09-01
---
# Data Capability Specification

## Overview

This specification defines the current configuration and hardening contract for
the data services under infra/04-data/.

## Boundaries and Inputs

- Input architecture: AD-0019 and engine-specific decisions.
- In scope: analytics, cache/KV, object storage, NoSQL, operational,
  relational, graph, and vector Compose services.
- Out of scope: product schemas, application queries, cloud migration, and
  unimplemented HA claims.

## Behavior Contract

- Each service retains an explicit Compose, network, persistent-state, secret,
  and health boundary.
- Common optimization templates are composed without overriding engine-owned
  configuration.
- Credential paths use tracked secret references and no plaintext values.
- Invalid expose tokens, missing required healthchecks, and duplicate static
  addresses fail validation.

## Technical Approach

The tier is divided into analytics, cache-and-kv, lake-and-object, nosql,
operational, relational, and specialized directories. Static hardening and
Compose rendering validate shared invariants; engine-specific backup,
retention, failover, or reindex procedures stay with the owning Operations
subject.

## Interfaces and Data

Services expose only their declared SQL, Redis/Valkey, S3-compatible, search,
graph, and vector interfaces. Persistent state remains in service-specific
volumes and credentials enter through Compose secret contracts.

## Failure Modes and Guardrails

Missing healthchecks, malformed Compose tokens, secret-path mismatch, storage
ambiguity, or an unapproved topology expansion blocks the change. Recovery is
engine-specific and must not be inferred from a static render pass.

## Acceptance Contract

- Target data Compose files render in the required root/profile context.
- scripts/hardening/check-all-hardening.sh 04-data passes.
- Template security and document traceability checks pass.
- AD-0019, this Spec, and Stage 05 procedures describe the tracked topology.

## Traceability

- [REQ-0016](../../01.requirements/0016-data-optimization-hardening.md)
- [AD-0019](../../02.architecture/descriptions/0019-data-optimization-hardening-architecture.md)
- [Data hardening guide](../../05.operations/catalog/04-data/0030-optimization-hardening/guide.md)
- [Data hardening policy](../../05.operations/catalog/04-data/0030-optimization-hardening/policy.md)
- [Data hardening runbook](../../05.operations/catalog/04-data/0030-optimization-hardening/runbook.md)
