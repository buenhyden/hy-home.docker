---
title: "Implementation Alignment Batch 2 Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-04"
layer: "specs"
artifact_id: "SPEC-0257-TSK-0001"
parent_ids:
- "SPEC-0257-PLAN-0001"
created: "2026-11-04"
---

# Implementation Alignment Batch 2 Task

## Overview

### Objective

Apply the batch 2 findings SPEC-0255 deferred.

## Inputs and Authorization

The user directed that README, AGENTS.md and the Stage 01, 02, 05 and 99
documents be checked against the implementation and corrected ("현재에 맞게
수정하고 보완한다"), including "Missing owners", and on 2026-11-04 said "Not
started 중 지금 실행할 수 있는 요구사항을 검토하여 진행한다." SPEC-0255 lists
these findings under its batch 2 open issue. This Task pushes and merges
nothing; the coordinator pushes the branch and opens the pull request.

## Work Log

### Current contract decision

The user's direction authorizes this Spec and Plan as written.

### Current readiness and execution

Inputs, work units and checks are recorded here. The Task is ready and in
progress under the approved parents. Hosted CI has not run.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0257 | draft | approved | #current-contract-decision |
| SPEC-0257-PLAN-0001 | draft | approved | #current-contract-decision |
| SPEC-0257-TSK-0001 | draft | ready | #current-readiness-and-execution |
| SPEC-0257-TSK-0001 | ready | in-progress | #current-readiness-and-execution |

### Decisions

- **Numbering:** PR #730 holds SPEC-0256, so this package takes SPEC-0257 and
  the Registry Spec high-water is 257.
- **Operations paths:** the catalog moved each guide, policy and runbook into
  a domain folder. A missing path is rewritten only when exactly one file of
  the same category and name exists; all 250 matched one file.
- **Registry entries:** `docs/03.specs/0123-...` and
  `docs/90.references/audits/0023-...` no longer exist, so the two maps are
  empty. The keys stay because the loader and schema read them.
- **Secret owners:** the guide that already lists a service's secrets gets
  the missing names: Airflow and OAuth2 Proxy monitor ACL passwords, the
  SeaweedFS JWT and S3 admin keys, the Grafana reader password and the three
  `hyhome-platform` dev-db role passwords.

### Changed

- 47 infra READMEs: 250 backticked operations paths.
- `infra/06-observability/grafana/README.md`: Compose link to the tier file.
- `infra/09-platform-ops/README.md`: audience names people only.
- `docs/99.templates/registry.json`: the two dangling entries and the Spec
  counter.
- GDE-0015, GDE-0024, GDE-0041, GDE-0050 and GDE-0100: secret names.

### Open issues

- PR #730 also edits the Registry; whichever branch merges second resolves
  the Spec counter.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1 | W1 | path-scan | backticked `docs/` paths in `infra/**/README.md`, main b56fd4480 | FAIL | 250 missing paths; 54 resolve | required | - |
| E2 | 1 | W1 | path-scan | the same scan after W1 | PASS | 250 rewritten, zero unresolved | required | E1 |
| E3 | 4 | W4 | secret-name-scan | Compose top-level secret names against `docs/05.operations`, `docs/02.architecture` and infra READMEs, main b56fd4480 | FAIL | 9 of 88 names missing | required | - |
| E4 | 4 | W4 | secret-name-scan | the same scan after W4 | PASS | 88 of 88 names appear in an owning document | required | E3 |
| E5 | 5 | W5 | metadata-changed | `check-changed --base-ref origin/main`, revision 1d1aac4ba, base main 0ab42bc30 | PASS | 57 selected, zero violations | required | - |
| E6 | 5 | W5 | metadata-active | `check-active`, revision 1d1aac4ba | PASS | 503 selected, zero violations | required | - |
| E7 | 3 | W3 | corpus-lifecycle | `check-document-corpus-lifecycle.py --base-ref origin/main`, revision 1d1aac4ba | PASS | lifecycle and occupancy zero | required | - |
| E8 | 5 | W5 | operations-catalog | `check-operations-catalog.py`, revision 1d1aac4ba | PASS | PASS | required | - |
| E9 | 2 | W2 | links-modes | alignment, navigation, language, traceability, entrypoint and commands, revision 1d1aac4ba | PASS | every mode PASS | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | - | - | @buenhyden |
| 2 | pending | - | - | @buenhyden |
| 3 | pending | - | - | @buenhyden |
| 4 | pending | - | - | @buenhyden |
| 5 | pending | - | - | @buenhyden |

## Review and Completion

Local checks E2 and E4 to E9 pass. No independent review has run and hosted
CI is not observed; no criterion is accepted yet.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
