---
title: Script Surface Ownership Convergence Outcome
version: 1.0.0
type: sdlc/spec
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0157
parent_ids: [REQ-0024, REQ-0025]
created: 2026-08-30
updated: 2026-09-01
---
# Script Surface Ownership Convergence Outcome

## Overview

This completed change made directory placement, manifest registration, and test
reachability express script ownership directly. Its terminal Plan and Task are
removed after this durable write-back.

## Boundaries and Inputs

The change covered scripts/, tests/, their READMEs, manifest rows, gate
registration, document-governance fixtures, and bounded Git recovery logic.
Provider projections and service runtime behavior were not redesigned.

## Behavior Contract

- scripts/lib/<domain>/ contains importable domain logic.
- scripts/validation/, scripts/gate/, scripts/security/, and
  scripts/operations/ contain command entrypoints for their declared surfaces.
- tests/lib/<domain>/ mirrors library ownership; tests/validation/ covers
  entrypoints and validation behavior.
- Every test module on disk is reachable from the registered full profile or is
  removed.
- Current-contract tests use current Registry/template inputs or minimal
  temporary repositories, never deleted workspace documents.
- Script and test inventories are derived rather than frozen as corpus counts.

## Technical Approach

Unreachable code was removed before modules were moved. Multi-responsibility
files were split along domain, lifecycle, metadata, and entrypoint boundaries,
then manifest paths, imports, suite bindings, and tests were updated together.

## Interfaces and Data

The public CLI names and six suite responsibilities remain stable.
scripts/manifest.yaml owns inventory, .github/workflow-contract.yml owns CI
routing, and Stage 99 owns document contracts.

## Failure Modes and Guardrails

An unregistered module, library with entrypoint mutation, entrypoint containing
domain logic, stale import, fixed corpus count, deleted-body fixture, or
unbounded history scan blocks acceptance.

## Acceptance Contract

The current layout follows the ownership rule, manifest and suite routing cover
the on-disk test set, current fixtures pass without historical authorities, and
the full profile succeeds.

## Traceability

- [REQ-0024](../../../../01.requirements/0024-agent-governance-standardization.md)
- [REQ-0025](../../../../01.requirements/0025-operational-readiness-closure.md)
- [ADR-0029](../../../../02.architecture/decisions/0029-workspace-governance-authority.md)
- [SPEC-0154](../0154-governance-consistency-convergence/spec.md)
- [SPEC-0155](../0155-validation-surface-reduction/spec.md)
- [Scripts README](../../../../../scripts/README.md)
- [Script manifest](../../../../../scripts/manifest.yaml)
