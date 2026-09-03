---
title: Template Contract Enforcement Specification
version: 1.0.0
type: sdlc/spec
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0165
parent_ids: [REQ-0024, REQ-0026, AD-0030, ADR-0029]
created: 2026-09-03
updated: 2026-09-03
---

# Template Contract Enforcement Specification

## Overview

Template sources were excluded from the full validation route because the
contract they would have been judged against was wrong. Opening it reported 36
findings against 34 templates, and every one was the rule misfiring rather than
a template being wrong.

This package corrects the contract, removes the exclusion, and registers the
catalog that makes a template findable.

## Boundaries and Inputs

Owned here: the template placeholder rule, the `parent_ids` exemption, the
`readme` template special case, the record-loop exclusion, and the catalog
completeness contract.

Not owned here: template body content, which already satisfies every target
profile's required sections.

Inputs: the Stage 99 Registry, the 34 Markdown templates, and the catalog.

## Behavior Contract

- A template must render a placeholder only for keys no profile fixes.
- A placeholder-shaped value must be one the Registry registers.
- A template carries `parent_ids` only where its target profile declares the key.
- Every registered template role whose source exists is linked from the catalog.
- No template rule is unreachable from `run-ci-gate.py --profile full`.

## Technical Approach

Open the excluded route, read every finding as a hypothesis about the rule
rather than about the template, and check each against how templates actually
use the key. Correct the rule where the corpus contradicts it, then remove the
exclusion so the corrected contract is enforced.

## Interfaces and Data

| Surface | Change |
| :--- | :--- |
| `docs/99.templates/registry.json` | `common.template_required_placeholders`; `template_catalog` |
| `docs/99.templates/contracts/document-profile.schema.json` | requires `template_catalog` |
| `scripts/lib/document_governance/metadata/heading.py` | placeholder scope, `parent_ids` exemption, readme case removed |
| `scripts/lib/document_governance/metadata/reference.py` | exclusion removed; catalog enforced |
| `scripts/lib/document_governance/registry.py` | `DocumentRegistry.template_catalog` |

## Failure Modes and Guardrails

| Failure mode | Guardrail |
| :--- | :--- |
| A misfiring rule is silenced instead of corrected | Measure how templates use the key before changing either |
| Removing an exclusion drags in unrelated findings | Correct every finding's cause first, then remove it |
| A new rule enumerates nothing | Assert the governed count is non-zero |

## Acceptance Contract

1. All 34 Markdown templates pass full validation with the exclusion removed.
2. Each corrected rule still reports the defect it exists for.
3. A catalog missing a registered role is reported.
4. `run-ci-gate.py --profile full` exits 0 after every commit.

## Traceability

- Continues SPEC-0164, which corrected the lifecycle a template may declare but
  left the rest of the template contract unenforced.

## Related Documents

- [Stage 99 authority](../../99.templates/README.md)
- [Documentation protocol](../../00.agent-governance/policies/documentation-protocol.md)
