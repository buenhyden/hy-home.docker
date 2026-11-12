---
title: "Legacy Document Status Ban Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0256-PLAN-0001"
parent_ids:
- "SPEC-0256"
created: "2026-11-04"
---

# Legacy Document Status Ban Plan

## Overview

### Goal and Boundary

Narrow the Registry lifecycles and profiles first, retire ADR-0011, remove the
archive scaffolding and receipt field, then state the rule and record the
evidence.

The Registry and its two schemas, `spec_packages.py`, the registry and Spec
Package tests, ADR-0011 and the documents that link to it, the archive
templates, the SDLC, the documentation protocol, the Stage 99 and decision
READMEs, and this package.

Parent Spec: [Spec](spec.md)

### Assumptions

The plan works under the approved Spec and assumes no authority beyond it.

## Dependencies

### Prerequisites

The approved Spec.

### Dependency Order

W1 has no dependency; W2 and W3 start after W1; W4 records the results after W1 to W3.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Remove legacy statuses and lineage keys from the Stage 01 to 03 lifecycles and profiles; add fail-closed tests | None | TSK-0001 | registry tests; metadata check-active |
| W2 | 2 | Summarize ADR-0011 into AD-0011, delete it, reserve 11, unlink inbound references | W1 | TSK-0001 | links alignment; corpus lifecycle |
| W3 | 3 | Remove the archive profiles and templates, the unread archive keys, and the receipt field; state the rule in governance | W1 | TSK-0001 | registry and Spec Package tests; review |
| W4 | 4 | Record local results | W1–W3 | TSK-0001 | the checks above |

### Change and Rollback

Revert the branch to restore the deleted bodies, profiles and templates; no outside state changes.

## Verification Plan

### Verification Matrix

Run `tests/lib/document_governance`, `tests/validation/lifecycle`, CI routing
and surface ownership, `test_ci_gate_evidence` under system python3,
`check-document-metadata.py` in `check-changed` and `check-active` modes,
`check-document-corpus-lifecycle.py`, `check-document-links.py` in `alignment`
and `commands` modes, `check-script-manifest.py`, the provider renderer
`--check`, and the agent governance contract.

### Stage Placement

The Plan places no stage-specific checks beyond the Verification Matrix; the Task records each run.

## Risks

### Risks and Mitigations

A check that still names a removed status or profile fails its unit suite, which W4 runs. Deleted bodies stay in version history.

### Escalation

Work stops and returns to the owner when a required check fails or an approval is missing, per the stop rules in [docs/03.specs/AGENTS.md](../AGENTS.md).

## Promotion Map

### Durable Meaning

The narrowed lifecycles and profiles live in the Registry and its schemas; the retired ADR-0011 is summarized in AD-0011; the rule is stated in the governance documents named in the Spec.

### Owner and Receipt

The owner is @buenhyden; the receipt is the Task named in the Work Breakdown.

- [Task](tasks/tsk-0001-legacy-document-status-ban.md)
