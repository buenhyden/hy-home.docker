---
title: Validation Blind Spot Closure Specification
version: 1.0.0
type: sdlc/spec
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0162
parent_ids: [REQ-0024, REQ-0026, AD-0030, ADR-0029]
created: 2026-09-03
updated: 2026-09-03
---

# Validation Blind Spot Closure Specification

## Overview

The document-governance gate reported zero violations while several of its own
rules could not fire. A rule is a blind spot, not a guarantee, when it is
declared in a validator but unreachable in the route the repository actually
runs. Three such rules were found and confirmed by negative test, and each had
already let a real defect through.

This package closes them and registers the one rule the corpus stated only in
prose.

## Boundaries and Inputs

Owned here: the reachability of `invalid-status`, `template-placeholder-in-target`,
and `invalid-transition` from `--profile full`; the Stage 03 and Stage 90 index
contract; the stale members of the shared `common` contract; policy prose that
restated the machine contract; the ten hook policies shipped with an unreplaced
`<title>`.

Not owned here: the immutable Git history of past status changes, and the
`98.archive` disposition, both reported rather than changed.

Inputs: the Stage 99 Registry, the tracked document corpus, and Git history as
a measurement source only.

## Behavior Contract

- A document whose status is outside its lifecycle is reported, whatever its
  status happens to be.
- The placeholder check tests the vocabulary templates actually declare.
- The full profile compares the working tree against a committed predecessor,
  so a lifecycle transition is checked where the contract is verified.
- A registered package absent from the index that enumerates it is reported.
- Every registered README profile has a lifecycle, so status is a state machine
  rather than a free string.

## Technical Approach

Measure before changing. For each suspected blind spot, run the rule's own
route, apply the exact defect it claims to catch, and record whether it fires.
Change only what the measurement names, then apply the same negative test to
confirm the rule now fires and a legal case still does not.

Contract before documents: a rule is registered in `registry.json` in the same
change that enforces it, because a contract with no enforcement repeats the
defect this package exists to remove.

## Interfaces and Data

| Surface | Change |
| :--- | :--- |
| `scripts/lib/document_governance/metadata/reference.py` | record validation no longer gates on the status being correct; the full route supplies a predecessor; index membership is enforced |
| `scripts/lib/document_governance/registry.py` | `DocumentRegistry.indexes`; `index-profile-unknown` |
| `docs/99.templates/registry.json` | `common` members corrected; six README lifecycles bound; `template_placeholders` derived from real tokens; `indexes` registered |
| `docs/99.templates/contracts/document-profile.schema.json` | requires `indexes` |
| `docs/99.templates/templates/references/` | member templates named after their roles |
| `docs/00.agent-governance/policies/documentation-protocol.md` | points at the Registry instead of restating it |

## Failure Modes and Guardrails

| Failure mode | Guardrail |
| :--- | :--- |
| A green gate is read as proof the rule ran | Apply the defect the rule claims to catch and confirm it is reported |
| A repaired rule over-fires on legal input | Test the legal case in the same step as the illegal one |
| A new rule enumerates nothing and passes vacuously | Assert the governed document count is non-zero |
| Past events are judged by a later contract | Validate at the change boundary, never over immutable history |
| A measurement probe reports an empty result that is really a probe failure | Self-test every probe against a known-positive case before trusting it |

## Acceptance Contract

1. Each closed blind spot is demonstrated by a negative test that failed to fire
   before the change and fires after it.
2. No repaired rule reports a legal case.
3. `run-ci-gate.py --profile full` exits 0 after every commit.
4. Defects found and not fixed are reported with their measurement, not left
   implicit.

## Traceability

- Continues SPEC-0161, whose deferred item was the stale `common` contract.
- Extends SPEC-0158, which registered the Stage 90 package lifecycle whose index
  rule this package makes executable.

## Related Documents

- [Stage 99 authority](../../99.templates/README.md)
- [Documentation protocol](../../00.agent-governance/policies/documentation-protocol.md)
