---
title: Validation Surface Reduction Outcome
version: 1.0.0
type: sdlc/spec
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0155
parent_ids: [REQ-0024, REQ-0025]
created: 2026-08-30
updated: 2026-09-01
---
# Validation Surface Reduction Outcome

## Overview

This completed change removed duplicate and unreachable validation machinery
while preserving the six public suite responsibilities and their focused
predicates.

## Boundaries and Inputs

The change covered scripts and tests that implemented document governance,
Agent governance, gate routing, generated evidence, and current fixtures. It
did not relax a current Requirement or treat line-count reduction as success.

## Behavior Contract

- Every atomic validator is registered once in scripts/manifest.yaml.
- Public suites compose focused validators and own no duplicate predicates.
- Current document fixtures derive from Stage 99 or construct minimal temporary
  cases; they do not resurrect deleted workspace bodies.
- Corpus counts are derived unless a deliberate fixed contract explains the
  pin.
- Network-dependent observation remains advisory where a deterministic local
  policy owns blocking behavior.

## Technical Approach

Unreachable modes and duplicate wrappers were removed, shared domain logic was
consolidated, generated-output checks were retained only for current consumers,
and blocking modes were tested directly.

## Interfaces and Data

The durable interfaces are scripts/manifest.yaml, the six public suite names,
.github/workflow-contract.yml, Stage 99 Registry, focused validators, and their
tests.

## Failure Modes and Guardrails

A removed guarantee with a live consumer, an unregistered test, duplicated
suite ownership, a resurrected fixture, or a success claim based only on fewer
lines blocks acceptance.

## Acceptance Contract

Changed and full profiles pass, manifest and workflow routing agree, every
current test is reachable, and no current validator requires a retired Spec,
Task, audit body, or fixed workspace commit as contract authority.

## Traceability

- [REQ-0024](../../../../01.requirements/0024-agent-governance-standardization.md)
- [REQ-0025](../../../../01.requirements/0025-operational-readiness-closure.md)
- [ADR-0029](../../../../02.architecture/decisions/0029-workspace-governance-authority.md)
- [SPEC-0154](../0154-governance-consistency-convergence/spec.md)
- [SPEC-0157](../0157-script-surface-ownership-convergence/spec.md)
- [Script manifest](../../../../../scripts/manifest.yaml)
