---
title: "Document Contract Convergence Specification"
version: "0.2.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-05"
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

The existing convergence introduced the closed frontmatter schema, one-to-one
Registry ID/type mapping, normalized templates, and frozen archive preservation.
This local follow-up closes independently reproduced gaps in literal values,
template validation, author-prompt residue and active navigation semantics.

## Boundaries and Inputs

- The 2026-09-05 request authorizes local documentation and validation changes
  in the current `main` checkout. Do not stage, commit, switch branches, fetch,
  push, create a PR, or perform a remote or runtime operation in this follow-up.
- Reuse REQ-0024, REQ-0026, AD-0027, AD-0030, ADR-0029 and ADR-0031. Do not
  duplicate requirements or rewrite an accepted architecture decision.
- Scope includes Stage 00 semantics; Stage 99 Registry, schemas and templates;
  metadata consumers, direct tests, Stage README navigation, and this package.
- Preserve Operations domain/subject identities, incident year partitions,
  CODEOWNERS ownership, issued ID high-water, provider-native syntax, and frozen
  archive bodies. Real environment, secret and certificate content is excluded.
- Earlier remote/Hosted authorizations and observations remain historical Task
  evidence. They do not authorize actions under this narrower current request.

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

Reuse this existing package and its execution Task, measure the current corpus,
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
5. Changed/full routing is inspected before execution. An invocation that would
   consume real environment or secret content is DEFER under this request;
   static document leaves are executed separately and are not aggregate PASS.
6. The diff changes no frozen body, provider runtime projection, infrastructure
   service, secret, credential or certificate payload. The current index and
   HEAD remain unchanged, and no remote/live acceptance is asserted.

## Traceability

- Requirements: REQ-0024 and REQ-0026.
- Architecture: AD-0027 and AD-0030.
- Decisions: ADR-0029 and ADR-0031.
- Execution: SPEC-0172-PLAN-0001 and SPEC-0172-TSK-0001.

## Operational Impact

This follow-up changes documentation and its validation contracts only. Public
full/changed routes can include Compose validation, so their exact selection
must be inspected before invocation; a real `.env` must never be consumed to
produce document evidence. Safe static results and deferred aggregate results
remain distinct in the Task.

## Related Documents

- [Implementation plan](plan.md)
- [Execution task](tasks/tsk-0001-document-contract-convergence.md)
