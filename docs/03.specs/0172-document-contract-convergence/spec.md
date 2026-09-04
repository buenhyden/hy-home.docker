---
title: "Document Contract Convergence Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-04"
layer: "specs"
artifact_id: "SPEC-0172"
parent_ids:
- "REQ-0024"
- "REQ-0026"
- "AD-0027"
- "AD-0030"
- "ADR-0029"
- "ADR-0031"
created: "2026-09-04"
---

# Document Contract Convergence Specification

## Overview

The repository separates Stage 00 policy, Stage 99 machine contracts, templates,
validators, and authored documents, but those surfaces do not yet express one
contract. The Registry uses `profile_id` beside `type`, Stage 01 and Stage 02
README files teach deprecated classifier keys, the frontmatter schema is
open-ended, and templates use incompatible placeholder forms.

This package converges those surfaces without changing secrets, credentials,
certificates, deployed workload state, or frozen archive bodies. Follow-up
integration evidence is gathered through a feature branch, pull request,
Hosted CI, and bounded read-only provider, runtime, and repository observations.

## Boundaries and Inputs

- In scope: Stage 00 documentation, SDLC, lifecycle, operations, and archive
  policy; REQ-0024 and REQ-0026; AD-0027 and AD-0030; Stage README files; the
  Stage 99 Registry, schemas, templates, catalog, validators, and tests.
- In scope: active authored metadata and headings where safe migration is needed.
- Preserve the Operations domain/subject route, independent subject and role
  identities, incident year partitions, CODEOWNERS ownership, and ID high-water.
- In scope after the 2026-09-04 follow-up authorization: feature-branch commits,
  push, pull request, Hosted CI observation, provider entitlement observation,
  runtime inventory observation, and remote branch-protection inspection.
- Conditional and not executable without an exact target contract: deployment,
  provider mutation, branch-protection mutation, tag, release, and merge. Each
  needs a named target, intended before/after state, verification, and rollback;
  merge additionally requires explicit user authorization.
- Out of scope: secret or certificate reads and direct writes to `main`.
- Out of scope: formatting or rewriting preserved bodies under
  `docs/98.archive/{completed,superseded,retired}/`.

## Behavior Contract

1. Stage 00 owns semantics; Stage 99 owns the sole machine profile contract;
   schemas own structure and scalar grammar; templates project the contract;
   validators execute it; README prose explains navigation and responsibility.
2. Governed authored frontmatter uses `type` as its only classifier, with a
   lowercase kebab-case `family/kind` value. A short Registry `id` is an internal
   routing key mapped one-to-one to exactly one unique `type`.
3. Every governed path matches exactly one profile. Template-required profiles
   have exactly one source with no orphan or duplicate form.
4. Required, optional, forbidden, ordered, const, enum, identity, and lifecycle
   rules come from the Registry; scalar grammar rejects undeclared keys.
5. Markdown templates use `{{UPPER_SNAKE_CASE}}` and explicit author prompts;
   native contracts use `__UPPER_SNAKE_CASE__`; authored documents contain none.
6. Requirement Packages own PRD, SRS, and interface-requirement perspectives
   without parallel profiles. Descriptions and ADRs keep separate roles.
7. Spec, Plan, and Task retain behavior, sequence, and evidence boundaries with
   acceptance-to-work-to-evidence coverage.
8. Guide, Policy, Runbook, Incident, and Postmortem remain distinct. Release
   evidence uses one consumer-backed repository mode.
9. Frozen archive bodies remain byte-preserved and formatter-excluded; historical
   citation may not become a current authority dependency.
10. A new governed document starts at its lifecycle `initial_status`; every
    declared state is reachable from it, and terminal states are exactly those
    with no outgoing transition.

## Technical Approach

Create this package with the valid pre-migration template, measure the corpus,
then change Registry, schemas, templates, consumers, and tests as one contract
slice. Migrate active prose and metadata only after focused negative tests pass.
Keep legacy archive payloads on unmanaged preservation profiles.

## Interfaces and Data

- `docs/99.templates/registry.json`: path, profile, frontmatter, identity,
  lifecycle, relationship, section, template, and allocation authority.
- `docs/99.templates/contracts/document-profile.schema.json`: Registry shape.
- `docs/99.templates/contracts/document-frontmatter.schema.json`: frontmatter
  scalar and collection grammar.
- `docs/99.templates/templates/**`: placeholder-aware copy sources.
- `scripts/lib/document_governance/**`: Registry-backed execution.
- `tests/lib/document_governance/**` and `tests/validation/**`: conformance and
  negative/boundary fixtures.

## Failure Modes and Guardrails

- Partial migration makes paths unclassifiable. Update each contract slice
  atomically and run focused tests after each patch.
- A closed schema rejects legitimate provenance. Inventory active keys before
  finalizing the grammar and preserve profile-declared extensions.
- Placeholder residue reaches authored documents. Separate template-aware and
  authored validation modes.
- Formatter mutation corrupts frozen evidence. Prove ignore coverage first and
  treat any frozen-body diff as a hard stop.
- Local evidence is overstated. Record local PASS, FAIL, SKIP, and DEFER without
  inferring hosted, provider, or runtime acceptance.
- A broad integration request lacks an exact mutation target. Complete safe
  observations and PR integration first, then stop at the exact unresolved
  deployment, protection, tag, release, or merge decision.

## Acceptance Contract

1. The Task records a gap matrix with current state, target state, affected
   files, migration, validator, and test columns.
2. Active prose and authored frontmatter contain no deprecated classifier key;
   frozen preservation payloads are excluded from migration.
3. Registry, schemas, templates, validators, and tests agree on one stable
   internal profile `id`, its unique `family/kind` `type`, their one-to-one
   mapping, and exact frontmatter grammar.
4. Path/profile, template, placeholder, key order, identity, high-water,
   lifecycle, section, traceability, index, archive, and formatter checks pass.
5. Changed/full gates, traceability, current lifecycle CLI, diff checks, Hosted
   CI, provider entitlement, runtime inventory, and branch protection report
   exact observed outcomes without converting observation into acceptance.
6. The final diff changes no frozen archive body and contains no secret,
   credential, certificate, or runtime configuration payload.

## Traceability

- Requirements: REQ-0024 and REQ-0026.
- Architecture: AD-0027 and AD-0030.
- Decisions: ADR-0029 and ADR-0031.
- Execution: SPEC-0172-PLAN-0001 and SPEC-0172-TSK-0001.

## Operational Impact

The candidate diff has no runtime payload. Read-only runtime and remote
observations are evidence only. Deployment, provider, protection, tag, release,
and merge mutations remain stopped until their exact execution contract is
approved.

## Related Documents

- [Implementation plan](plan.md)
- [Execution task](tasks/tsk-0001-document-contract-convergence.md)
