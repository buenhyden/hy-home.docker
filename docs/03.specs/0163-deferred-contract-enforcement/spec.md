---
title: Deferred Contract Enforcement Specification
version: 1.0.0
type: sdlc/spec
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0163
parent_ids: [REQ-0024, REQ-0026, AD-0030, ADR-0029]
created: 2026-09-03
updated: 2026-09-03
---

# Deferred Contract Enforcement Specification

## Overview

SPEC-0162 closed three unreachable validation rules and recorded three items it
did not resolve: a README section check that skipped most of the corpus, a
forbidden-key contract that enforced nothing, and an open question about whether
Stage 98 holds parallel authority copies.

This package resolves all three. Each turned out to be a different shape of the
same defect: a contract the repository declares and the gate does not decide on.

## Boundaries and Inputs

Owned here: the README section check's profile selection; the union of
`common.globally_forbidden` into per-record forbidden keys; the diagnostic
quality of an archive contract violation; and the two documents that fail once
the section check covers them.

Not owned here: the content of any archive body, which is verified as a pointer
record and left unchanged; the 66 archive raise sites that do not name a
tombstone.

Inputs: the Stage 99 Registry and the tracked document corpus.

## Behavior Contract

- A README is checked against the `required_sections` of its own profile.
- A key in `common.globally_forbidden` is reported as forbidden repository-wide,
  distinctly from a key that is merely undeclared.
- An archive document that violates its contract is reported as a finding that
  names it, not as an internal error.

## Technical Approach

Measure each declared contract by applying the exact defect it claims to catch
and recording whether the gate decides. Where a contract is unenforced, decide
between enforcing it and deleting it on evidence rather than preference: enforce
when the declaration carries information the alternative check loses, delete
when it is strictly redundant.

Fix documents before enforcement when enforcement would otherwise leave the gate
red between commits.

## Interfaces and Data

| Surface | Change |
| :--- | :--- |
| `scripts/lib/document_governance/metadata/reference.py` | README sections come from the classified profile |
| `scripts/lib/document_governance/metadata/lifecycle.py` | `globally_forbidden` joins each profile's forbidden set |
| `scripts/lib/document_governance/archive.py` | `ArchiveContractError` carries the offending path |
| `scripts/lib/document_governance/lifecycle/recovery.py` | archive violations are findings with exit 1 |
| `scripts/validation/generate-audit-implementation-matrix.sh` | emits the sections the `data` profile requires |
| `infra/04-data/relational/postgresql-cluster/README.md` | heading drift corrected |

## Failure Modes and Guardrails

| Failure mode | Guardrail |
| :--- | :--- |
| Enforcement lands before the corpus conforms | Fix the failing documents in the preceding commit |
| A widened check enforces the wrong profile's contract | Read the classified profile, and test one document per profile |
| A probe deletes a section the profile does not require | Confirm the section is in the profile's required list before reading the result |
| An unenforced contract is deleted when it carried information | Compare what each candidate check reports, not just whether it reports |

## Acceptance Contract

1. Every README profile that declares sections reports a missing one.
2. Every key in `globally_forbidden` reports a code distinct from an undeclared
   key.
3. An archive contract violation names the document and exits 1.
4. `run-ci-gate.py --profile full` exits 0 after every commit.

## Traceability

- Resolves the three deferred items recorded in SPEC-0162.

## Related Documents

- [Stage 99 authority](../../99.templates/README.md)
- [Documentation protocol](../../00.agent-governance/policies/documentation-protocol.md)
