---
title: Documentation Taxonomy Migration Outcome
version: 1.0.0
type: sdlc/spec
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0093
parent_ids:
  - AD-0027
created: 2026-07-05
updated: 2026-09-01
---
# Documentation Taxonomy Migration Outcome

## Overview

This completed change established the numbered documentation stages and
aligned Agent authoring with those paths. It is retained as an outcome record,
not as current migration procedure.

## Boundaries and Inputs

The change covered the repository documentation taxonomy, stage indexes, Agent
authoring routes, and links. Current path and profile authority now belongs to
the Stage 99 Registry; current Agent workflow belongs to Stage 00.

## Behavior Contract

- Stage 00 owns AI Agent governance.
- Stages 01, 02, and 03 own the SDLC requirement, architecture, and
  specification chain.
- Stage 05 owns Operations; Stage 90 owns non-normative evidence; Stage 98 is
  historical; Stage 99 owns typed document contracts.
- No retired execution-stage path or compatibility redirect is current.

## Technical Approach

The migration rewrote tracked paths and links, installed stage indexes, and
bound documents to registered profiles. Later convergence work replaced its
one-time ledger behavior with current-tree validation.

## Interfaces and Data

The durable interfaces are docs/README.md, each stage README, the Stage 99
Registry, and Stage 00 authoring policy.

## Failure Modes and Guardrails

This document must not be used to restore retired routes, preserve duplicate
bodies, or bypass the current Registry. A future taxonomy change requires a new
active Spec Package.

## Acceptance Contract

The current docs tree uses registered stage paths and profiles, current links
resolve, and Agent bootstrap routes through Stage 00. Those owners supersede
the execution details that completed this change.

## Traceability

- [AD-0027](../../../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md)
- [Stage 00 authoring matrix](../../../../00.agent-governance/policies/stage-authoring-matrix.md)
- [Stage 99 Registry](../../../../99.templates/registry.json)
- [Documentation index](../../../../README.md)
