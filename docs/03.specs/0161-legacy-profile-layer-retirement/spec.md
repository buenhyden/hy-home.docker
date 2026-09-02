---
title: Legacy Profile Layer Retirement Specification
version: 1.0.0
type: sdlc/spec
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0161
parent_ids: [REQ-0024, REQ-0026, AD-0030, ADR-0029]
created: 2026-09-03
updated: 2026-09-03
---

# Legacy Profile Layer Retirement Specification

## Overview

Document validation had two profile authorities. Alongside `registry.json`, the
validators loaded `docs/99.templates/support/document-metadata-profiles.yaml`
out of the pinned commit `49406580` and merged it over the Registry on every
run. The file is absent from the working tree, so its contract could only be
read through Git and could not be edited in place.

This package removes the second authority.

## Boundaries and Inputs

Owned here: the legacy envelope's four live sections, the loader that read
them, and the merge that layered them over the Registry.

Not owned here: `HistoricalDocument` itself, which legitimately pins frozen
archive digests in `archive.py` and `git_provenance.py`; the content of the
`common` contract, moved verbatim so its stale members stay a separate step.

Inputs: the Registry, and the frozen blob as a measurement source only.

## Behavior Contract

- `registry.json` is the only profile input; a non-JSON profiles argument fails
  closed rather than falling back.
- Classification is unchanged for every document the corpus contains.
- A route the Registry does not own is `unsupported`, with no legacy fallback.

## Technical Approach

Measure each section's live reach with an environment-independent probe, retire
the sections in ascending order of reach so every step is small, then delete the
loader once nothing calls it. The `common` section moves into `registry.json`
verbatim rather than being rewritten, so no step mixes a move with an edit.

## Interfaces and Data

| Surface | Change |
| :--- | :--- |
| `docs/99.templates/registry.json` | gains the `common` contract |
| `docs/99.templates/contracts/document-profile.schema.json` | requires `common` |
| `scripts/lib/document_governance/registry.py` | `DocumentRegistry.common` |
| `scripts/lib/document_governance/metadata/profile.py` | loader and merge deleted; `build_registry_profiles` builds from the Registry |
| `scripts/lib/document_governance/lifecycle/contract.py` | manifest inference drops its legacy fallback |

## Failure Modes and Guardrails

| Failure mode | Guardrail |
| :--- | :--- |
| A section looks dead but is reached at run time | Probe each section over a full gate run, and self-test the probe before trusting an empty result |
| Removing a section silently changes classification | Compare the before and after sets explicitly, and name every difference |
| A step hides a regression in the next | One commit per section, each with a green full gate |

## Acceptance Contract

1. No validator reads the frozen profile YAML.
2. `run-ci-gate.py --profile full` exits 0 after every step.
3. `HistoricalDocument` survives only for frozen archive digests.
4. Every removed behavior is either unreachable or measured equivalent.

## Traceability

- Extends SPEC-0160, which recorded this retirement as a scoped deferral.

## Related Documents

- [Stage 99 authority](../../99.templates/README.md)
- [Documentation protocol](../../00.agent-governance/policies/documentation-protocol.md)
