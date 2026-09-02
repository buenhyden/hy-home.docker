---
title: Document Taxonomy and Identity Convergence Specification
version: 1.0.0
type: sdlc/spec
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0159
parent_ids: [REQ-0024, REQ-0026, AD-0030, ADR-0029]
created: 2026-09-02
updated: 2026-09-02
---

# Document Taxonomy and Identity Convergence Specification

## Overview

The corpus already carried the registered identity patterns, but three metadata
surfaces disagreed with each other. `type` mixed a stage-directory name with a
document role, `layer` repeated values the stage path already stated, and the
Stage 99 template layout did not match the roles the Registry declared. An
in-flight change had also placed an unquoted `#.#.#` version placeholder in
nineteen templates, where `#` opens a YAML comment, so the registered document
contract gate was failing at the design baseline.

This package converges the three surfaces on one taxonomy, makes `version` an
explicit envelope key, and reduces Stage 99 to a single catalog.

## Boundaries and Inputs

In scope: the `type` and `layer` frontmatter values across every stage, the
Stage 99 template layout and registry bindings, the frontmatter envelope, the
Stage 00 and Stage 99 layer exemption, and the validator and test surfaces that
encode those values.

Out of scope: artifact identity patterns, which the Registry, the corpus, and
the documentation protocol already agreed on; the legacy transition layer in
`scripts/lib/document_governance/` that `lifecycle/contract.py` loads at run
time; and any change to Stage 90 historical evidence.

Inputs: the Stage 99 Registry, the tracked corpus, the registered gate, and the
predecessor package SPEC-0158.

## Behavior Contract

- Every `type` is a `family/kind` pair whose family names the owning authority:
  `governance`, `sdlc`, `operation`, `reference`, `archive`, or `common`.
- Every `layer` is the owning stage directory name without its numeric prefix.
  Stage 00 and Stage 99 documents declare no `layer`.
- Every managed document and template declares a semantic `version`. Only the
  two provider-owned runtime projections are exempt.
- Each Registry profile binds at most one template role, and each template role
  resolves to exactly one profile.
- A Stage 99 template carries literal placeholders and never a concrete target
  path.

## Technical Approach

Retype and relayer the corpus from one table derived from the Registry, then
move the template sources to the declared layout and rebuild `template_roles`
from a single mapping so profile and role cannot drift apart. Replace the
duplicated placeholder-substitution tables with one exported table so the
frontmatter schema stays strict for authored documents while templates keep
readable placeholders.

Three validator defects surfaced once profiles that previously had no template
gained one; each is repaired at its cause rather than by relaxing the contract.

## Interfaces and Data

- `docs/99.templates/registry.json` — profiles, types, template roles,
  identity allocation.
- `docs/99.templates/contracts/frontmatter.schema.json` — typed value shapes.
- `scripts/lib/document_governance/` — registry, metadata, archive, taxonomy,
  and lifecycle validators.
- `scripts/validation/run-ci-gate.py --profile full` — the registered gate.

## Failure Modes and Guardrails

- A YAML comment character in an unquoted placeholder silently parses as null;
  every template placeholder that contains `#` is quoted.
- Heading enforcement previously routed on `template_id`, so a profile that
  gained a template lost its section contract; routing now follows whether the
  profile is a typed SDLC target.
- Stage 98 migrations are digest-frozen; each repin is admitted only after the
  body is verified byte-identical to its predecessor blob.
- An auto-formatter joined deliberately split string literals that a line-scanning
  policy check depends on; that file is edited without the formatter in the loop.

## Acceptance Contract

1. `python3 scripts/validation/run-ci-gate.py --profile full` exits 0.
2. No document declares a retired `profile_id`, `artifact_type`, `stage`, or
   `last-updated` key.
3. No Stage 00 or Stage 99 document declares `layer`.
4. Every managed document declares a semantic `version`.
5. The Stage 99 template layout equals the roles the Registry declares.

## Traceability

- [REQ-0024](../../01.requirements/0024-agent-governance-standardization.md)
- [REQ-0026](../../01.requirements/0026-document-retention-and-retirement.md)
- [AD-0030](../../02.architecture/descriptions/0030-document-lifecycle-governance.md)
- [ADR-0029](../../02.architecture/decisions/0029-workspace-governance-authority.md)
- [Plan](./plan.md)
- [Task](./tasks/tsk-0001-taxonomy-convergence.md)

## Open Questions

None. The three interpretation choices this package faced were decided by the
requester before execution and are recorded in the Task rulings.

## Operational Impact

Authoring routes change: contributors resolve a template role in the Registry
and copy from the single Stage 99 catalog. No runtime, Compose, or deployment
behavior changes.

## Related Documents

- [Documentation protocol](../../00.agent-governance/policies/documentation-protocol.md)
- [Stage authoring matrix](../../00.agent-governance/policies/stage-authoring-matrix.md)
- [Stage 99 authority](../../99.templates/README.md)
