---
title: "Legacy Document Status Ban Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-04"
layer: "specs"
artifact_id: "SPEC-0255-PLAN-0001"
parent_ids:
- "SPEC-0255"
created: "2026-11-04"
---

# Legacy Document Status Ban Plan

## Overview

Narrow the Registry lifecycles and profiles first, retire ADR-0011, remove the
archive scaffolding and receipt field, then state the rule and record the
evidence.

## Scope

The Registry and its two schemas, `spec_packages.py`, the registry and Spec
Package tests, ADR-0011 and the documents that link to it, the archive
templates, the SDLC, the documentation protocol, the Stage 99 and decision
READMEs, and this package.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Remove legacy statuses and lineage keys from the Stage 01 to 03 lifecycles and profiles; add fail-closed tests | None | TSK-0001 | registry tests; metadata check-active |
| W2 | 2 | Summarize ADR-0011 into AD-0011, delete it, reserve 11, unlink inbound references | W1 | TSK-0001 | links alignment; corpus lifecycle |
| W3 | 3 | Remove the archive profiles and templates, the unread archive keys, and the receipt field; state the rule in governance | W1 | TSK-0001 | registry and Spec Package tests; review |
| W4 | 4 | Record local results | W1–W3 | TSK-0001 | the checks above |

## Verification Plan

Run `tests/lib/document_governance`, `tests/validation/lifecycle`, CI routing
and surface ownership, `test_ci_gate_evidence` under system python3,
`check-document-metadata.py` in `check-changed` and `check-active` modes,
`check-document-corpus-lifecycle.py`, `check-document-links.py` in `alignment`
and `commands` modes, `check-script-manifest.py`, the provider renderer
`--check`, and the agent governance contract.

## Risks and Recovery

### Risks and Rollback

A check that still names a removed status or profile fails its unit suite,
which W4 runs. Deleted bodies stay in version history. Revert the branch to
restore them; no outside state changes.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-legacy-document-status-ban.md)
