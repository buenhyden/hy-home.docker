---
title: README Entrypoint Form Registration Specification
version: 1.0.0
type: sdlc/spec
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0160
parent_ids: [REQ-0024, REQ-0026, AD-0030, ADR-0029]
created: 2026-09-02
updated: 2026-09-02
---

# README Entrypoint Form Registration Specification

## Overview

SPEC-0159 converged document type, layer, identity, and the Stage 99 template
layout, but it left every README outside a handful of `docs/` routes classified
only by the frozen legacy profile YAML, which registry-native validation skips.
The result was a corpus of entrypoint documents with no enforced authoring form
and no single owner.

This package registers one Stage 99 form for each README entrypoint kind —
repository, documentation, stage, package, and runtime-governance — and extends
the Registry just far enough to name them.

## Boundaries and Inputs

Owned here:

- the five shared README forms under `docs/99.templates/templates/common/`;
- the Registry profiles, roles, and path vocabulary those forms need;
- the frontmatter the newly registered documents must carry.

Not owned here:

- the legacy transition envelope's `common`, `document_families`, and
  `archive_profiles` sections, which remain loaded;
- `_workspace/**` and the `tests/` suite notes, which stay outside the Registry;
- any README body restructuring beyond what the section contract already met.

Inputs: the Stage 99 Registry, the frozen legacy profile YAML as a measurement
source only, and the tracked README corpus.

## Behavior Contract

- Every README entrypoint kind resolves to exactly one registered Stage 99 form.
- The Registry may name a path outside `docs/` only for a bounded set of
  repository entrypoint roots.
- A projected README carries its form's frontmatter; provider instruction files
  stay provider-owned and frontmatter-free.
- Stage 03 packages carry no README, and the profile that permitted one is gone.

## Technical Approach

Three Registry vocabulary additions carry the work: a `{category}` token for the
Stage 90 category indexes, a `{subpath}` token for nested entrypoint trees, and
`_registry_owned_root` for the bounded non-docs roots. Each new profile then
binds one template role, and the affected documents gain the frontmatter their
profile requires. Where a document is generated, its generator emits the
frontmatter instead.

## Interfaces and Data

| Surface | Change |
| :--- | :--- |
| `docs/99.templates/registry.json` | six profiles added, two retired, three roles rebound |
| `scripts/lib/document_governance/registry.py` | non-docs root allowlist, `{category}` and `{subpath}` tokens |
| `scripts/lib/document_governance/metadata/profile.py` | glob translation for the new tokens |
| `scripts/operations/provider_surface_renderer.py` | frontmatter on projected READMEs |

## Failure Modes and Guardrails

- Widening Registry authority past the entrypoint roots is prevented by the
  explicit `_NON_DOCS_ROOTS` and `_NON_DOCS_FILES` allowlist.
- `test_target_runtime_readmes_stay_outside_the_document_registry` still fails
  closed for every target-root README that is not a registered entrypoint form.
- `template-source-duplicate` still forbids one template serving two roles, so a
  form cannot silently cover a second profile.

## Acceptance Contract

- `run-ci-gate.py --profile full` exits 0.
- All five entrypoint forms exist in `templates/common/` and each has a role.
- No Stage 03 package carries a README.
- Each Stage 90 category, package, and member level resolves to its own form.

## Traceability

- Extends SPEC-0159.
- Implements the README-form requirements in REQ-0024 and REQ-0026.

## Related Documents

- [Stage 99 authority](../../../../99.templates/README.md)
- [Documentation protocol](../../../../00.agent-governance/policies/documentation-protocol.md)
