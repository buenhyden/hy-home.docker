---
title: Document Lifecycle Convergence Specification
version: 1.0.0
type: sdlc/spec
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0169
parent_ids: [REQ-0026, AD-0030, ADR-0030]
created: 2026-09-03
updated: 2026-09-04
---

# Document Lifecycle Convergence Specification

## Overview

Three stages declared a section contract that nothing enforced. Two mutations
proved it: adding an unregistered heading to a Stage 03 spec passed the gate, and
deleting its required `Traceability` heading also passed. `validate_body_contract`
checked sections only for profiles without a `template_id`, and every Stage 01,
02, and 03 type declares one.

The corpus drifted accordingly. Across 349 stage documents, 192 missed a required
heading and 272 carried headings no profile registered. The damage had two
distinct shapes, and they needed different remedies.

For the operations catalog the registry was wrong about the corpus. All 192
`guide`, `policy`, and `runbook` documents missed required headings and carried
unregistered ones, while the corpus itself was uniform: 59 of 66 guides shared
one signature. The registry and the three operations templates agreed with each
other and with nothing on disk.

For Stages 01 to 03 the corpus was wrong about itself. Requirements, decisions,
and descriptions carried two generations of section vocabulary stacked together,
and Stage 01 held nine `optimization-hardening` requirements whose clauses named
Traefik middleware chains, healthcheck mechanisms, and compose declarations.
Stage 01 owns solution-independent requirements; a requirement that breaks when
the gateway changes is not one.

## Boundaries and Inputs

- In scope: `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`,
  `docs/05.operations/catalog`, `docs/98.archive`, the Stage 99 registry, the
  three operations templates, and the body-contract validator.
- In scope: the retention, retirement, and tombstone rules owned by REQ-0026,
  AD-0030, ADR-0030, and `documentation-protocol.md`.
- Out of scope: the content of individual services and procedures. This package
  moves and normalizes documents; it does not rewrite operational knowledge.
- Out of scope: `docs/00.agent-governance` policy authority, which is updated in
  place rather than restructured.

## Behavior Contract

1. A registered section contract is enforced for every profile that declares
   one, not only for profiles without a template.
2. The operations catalog vocabulary is the registered one, reconciled to what
   the corpus consistently uses, plus `Traceability`.
3. Stage 01 holds no requirement that names a specific implementation artifact.
4. A retired document in any stage leaves one tombstone, including Stage 01 and
   Stage 02, which have no tombstone namespace today.
5. A completed Spec Package retains `spec.md` and no execution members once its
   outcomes reach a canonical owner.
6. A Stage 03 package is a bounded change contract. A package that describes a
   steady state is retired to the Stage 02 and Stage 05 owners of that state.

## Technical Approach

Declaration precedes cleanup precedes enforcement. Turning enforcement on first
would block every intermediate commit behind 272 documents, so the validator
change lands last.

Phase 1 rewrites the declarations: the registry's `guide`, `policy`, and
`runbook` sections and their three templates adopt the corpus core plus
`Traceability`; REQ-0026, AD-0030, ADR-0030, and `documentation-protocol.md`
gain the Stage 01/02 retirement route, the tombstone namespace rule, and a
concrete member-disposal test; the four competing Stage 03 title conventions
collapse to one.

Phase 2 proves destination coverage per domain before moving anything, relocates
the solution-dependent clauses of `REQ-0014` through `REQ-0022` and the nine
hardening architecture descriptions to their charter owners, retires them with
tombstones, and strips the stacked legacy headings from 66 documents. The nine
hardening ADRs stay: an ADR records a decision at a point in time, and merging
one destroys the record it exists to keep.

Phase 3 retires the twelve permanently-active domain packages and removes the
execution members from the eleven completed packages that retain them.

Phase 4 normalizes the 192 catalog documents to the reconciled vocabulary.

Phase 5 removes the typed-target bypass in `validate_body_contract` and proves
the contract now fails closed in both directions.

## Interfaces and Data

- `docs/99.templates/registry.json`: section contracts, tombstone paths, and the
  spec identity space.
- `docs/99.templates/templates/operations/{guide,policy,runbook}.template.md`.
- `scripts/lib/document_governance/metadata/heading.py`: the enforcement branch.
- `docs/98.archive/tombstones/{01.requirements,02.architecture}/`: new namespaces.
- `.github/workflow-contract.yml`: unchanged; the affected paths already route to
  the document contract suites.

## Failure Modes and Guardrails

- A document is retired whose content no destination actually owns. Guarded by
  proving coverage per domain first; a domain that fails the proof is reported,
  not retired.
- Enforcement lands and an unmeasured profile fails closed. Guarded by measuring
  the blast radius per profile in Phase 1 and re-measuring before Phase 5.
- A tombstone is written without a recoverable commit. Guarded by the existing
  tombstone contract, which requires the recovery commit as a field.
- The catalog normalization invents content to satisfy a heading. Guarded by the
  chosen vocabulary being the one the corpus already uses; only `Traceability`
  is new, and it is a link list, not prose.

## Acceptance Contract

1. `run-ci-gate.py --profile full` exits `0` at every phase boundary.
2. Across the four stages, unregistered headings and missing required headings
   both reach zero.
3. Mutation evidence: an unregistered heading and a deleted required heading each
   fail the gate for `spec`, `requirement`, `adr`, `architecture-description`,
   `guide`, `policy`, and `runbook`.
4. Every retired document has exactly one tombstone naming its replacement and
   recovery commit.
5. Stage 03 contains no package that is `active` without execution members.

## Traceability

- Parents: REQ-0026 (document retention and retirement), AD-0030 (document
  lifecycle governance), ADR-0030 (tombstone retirement record).
- Predecessors: SPEC-0158 established lifecycle convergence, SPEC-0159 the
  taxonomy identity, SPEC-0164 the lifecycle vocabulary. This package enforces
  what they declared.

## Related Documents

- [Implementation plan](plan.md)
- [Execution task](tasks/tsk-0001-document-lifecycle-convergence.md)
- [Documentation protocol](../../../../00.agent-governance/policies/documentation-protocol.md)
