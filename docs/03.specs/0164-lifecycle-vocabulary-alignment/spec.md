---
title: Lifecycle Vocabulary Alignment Specification
version: 1.0.0
type: sdlc/spec
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0164
parent_ids: [REQ-0024, REQ-0026, AD-0030, ADR-0029]
created: 2026-09-03
updated: 2026-09-03
---

# Lifecycle Vocabulary Alignment Specification

## Overview

Every document profile declares a lifecycle: a status vocabulary and a
transition graph. This package checks that each declaration matches what its
documents and templates can actually be, and corrects the ones that do not.

Four mismatches were found. Two profiles declared states their documents are
forbidden to hold, one declared a vocabulary that both omitted a status it uses
and offered three it can never reach, one lifecycle duplicated another exactly,
and 51 documents sat outside their own lifecycle by carrying no status at all.

## Boundaries and Inputs

Owned here: the `lifecycle_id` binding of every profile, the lifecycle
definitions themselves, whether `status` is required where a lifecycle exists,
and the status of every document that lacked one.

Not owned here: the `execution` graph's `draft -> completed` edge, which the
repository declared deliberately and its Tasks use; the never-reached statuses
`retired`, `blocked`, `cancelled`, and `rejected`, which are legitimate states
that have not occurred; the `invalid-template-placeholder` rule and the
`docs/`-only record inventory, both reported.

Inputs: the Stage 99 Registry, the tracked corpus, and the template set.

## Behavior Contract

- A profile declares a lifecycle only if its documents may carry a status.
- A profile's lifecycle contains every status its documents can hold and no
  status they cannot reach.
- No two lifecycles are the same state machine under different names.
- A profile that declares a lifecycle requires `status`.
- A template carries the initial status of the profile it seeds.

## Technical Approach

Derive the contract from the Registry, derive observed usage from the corpus,
and compare by set difference. Where they disagree, decide from the profile's
role: a provider-owned projection has no state, a template mirrors its target's
initial state, and a document kept current is `living`.

Correct the contract only where the role makes the answer determinate. Where
the repository made a deliberate choice this package disagrees with, report it
rather than overrule it.

## Interfaces and Data

| Surface | Change |
| :--- | :--- |
| `docs/99.templates/registry.json` | three bindings corrected, `template` lifecycle added, `point-in-time` removed, `status` required for 12 profiles |
| `scripts/lib/document_governance/metadata/reference.py` | `invalid-template-status` reachable from the full route |
| 51 documents across six profiles | `status: active` added in frontmatter order |
| two `infra/` package READMEs | completed to their profile's required envelope |

## Failure Modes and Guardrails

| Failure mode | Guardrail |
| :--- | :--- |
| A lifecycle is removed as a duplicate while the machines differ | Assert the statuses and transitions are equal inside the change |
| A binding is dropped when the profile still needs a vocabulary | Run the profile contract tests; `template-source` was caught this way |
| A widened rule drags in unrelated findings | Keep the excluded codes explicit and report what they would say |
| Filling a status hides a deeper envelope defect | Complete the envelope where the frontmatter was already invalid |

## Acceptance Contract

1. No profile declares a lifecycle whose statuses its documents cannot hold.
2. No two lifecycles share a state machine.
3. Zero lifecycle-bound documents carry no status.
4. Deleting a status reports `missing-required-key` for every bound profile.
5. `run-ci-gate.py --profile full` exits 0 after every commit.

## Traceability

- Continues SPEC-0162, which made `invalid-status` and `invalid-transition`
  reachable but did not check that the declared vocabulary was correct.

## Related Documents

- [Stage 99 authority](../../99.templates/README.md)
- [Documentation protocol](../../00.agent-governance/policies/documentation-protocol.md)
