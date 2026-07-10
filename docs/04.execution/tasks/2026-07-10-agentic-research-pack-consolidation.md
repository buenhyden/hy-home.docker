---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md -->

# Task: Agentic Research Pack Consolidation

## Overview

This document tracks the source research, canonical document changes,
supersession work, logical commits, reviews, and verification evidence for the
agentic research pack consolidation defined by Spec 122 and its implementation
plan.

## Inputs

- **Parent Spec**:
  [Agentic Research Pack Consolidation](../../03.specs/122-agentic-research-pack-consolidation/spec.md)
- **Parent Plan**:
  [Agentic Research Pack Consolidation Plan](../plans/2026-07-10-agentic-research-pack-consolidation.md)
- **Canonical Research Pack**:
  [Agentic Engineering Research Pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- **Duplicate Pack**:
  [2026-07-07 Update](../../90.references/research/2026-07-07-agentic-research-pack-update/README.md)

## Working Rules

- Use tracked repo-local files and active stage documents for workspace truth.
- Use official vendor, standards, original-paper, and official-repository
  sources for external research.
- Apply the provider-model cutoff at 2026-07-10 10:00 KST (01:00 UTC).
- Record source metadata and concise evidence; do not paste raw pages, raw
  command output, diagnostics, shell history, or secret material.
- Keep Stage 90 advisory and record active-policy/runtime changes as follow-up
  gaps.
- Use one sequential implementer and one task-scoped review gate per task.
- Commit each clean reviewed task as one logical unit.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-ARC-001 | Refresh workspace baseline, spec-driven SDLC, document roles, and source evidence | doc | VAL-ARC-002, VAL-ARC-007, VAL-ARC-009 | PLN-ARC-001 | Category/role coverage, validators, commit range, task review | Documentation implementer | Todo |
| T-ARC-002 | Add cutoff-bound provider model landscape and refresh task selection | doc/eval | VAL-ARC-003, VAL-ARC-004 | PLN-ARC-002 | Model/lifecycle totals, cutoff exceptions, provider sources, validators, task review | Documentation implementer | Todo |
| T-ARC-003 | Consolidate harness, loop, provider implementation, and AI agent catalogs | doc | VAL-ARC-002, VAL-ARC-005 | PLN-ARC-003 | Capability sources, stale-claim disposition, validators, task review | Documentation implementer | Todo |
| T-ARC-004 | Refresh QA/CI/formatting and automation/pipeline/workflow research | doc | VAL-ARC-002, VAL-ARC-008 | PLN-ARC-004 | Gate/job inventory, evidence classes, validators, task review | Documentation implementer | Todo |
| T-ARC-005 | Refresh Docker Compose/infrastructure and security-governance research | doc/security | VAL-ARC-002, VAL-ARC-008 | PLN-ARC-005 | Rechecked Compose evidence, security status/gap matrix, validators, task review | Documentation implementer | Todo |
| T-ARC-006 | Finalize indexes, supersede duplicate pack, close lifecycle and validation | doc/eval | VAL-ARC-001, VAL-ARC-005, VAL-ARC-006, VAL-ARC-007, VAL-ARC-008, VAL-ARC-009, VAL-ARC-010 | PLN-ARC-006 | Coverage/disposition matrix, final checks, whole-branch review, closure commit | Workflow supervisor | Todo |

## Phase View

### Phase 1: Workspace and Lifecycle Baseline

- [ ] T-ARC-001 Refresh workspace baseline, SDLC, document roles, and evidence.

### Phase 2: Provider and Agent Research

- [ ] T-ARC-002 Add provider model landscape and task-selection analysis.
- [ ] T-ARC-003 Consolidate harness, loop, provider, and AI agent research.

### Phase 3: Quality, Infrastructure, and Security

- [ ] T-ARC-004 Refresh QA/CI/formatting and automation research.
- [ ] T-ARC-005 Refresh Compose/infrastructure and security research.

### Phase 4: Consolidation Closure

- [ ] T-ARC-006 Supersede the duplicate pack, close indexes/lifecycle, and
      record final evidence.

## Source Evidence Contract

Each task appends a source ledger with these exact fields:

| Source URL / repo path | Owner / source class | Supported claim | Published / updated | Retrieved | Cutoff disposition | Caveat | Task |
| --- | --- | --- | --- | --- | --- | --- | --- |

The table starts empty because no implementation research has been executed.
Rows are added only after a task verifies the source. A mutable page that cannot
prove the model cutoff must use `historical state unverified`.

## Task Review Evidence Contract

For each task, record:

- task-brief path;
- implementer report path;
- base and head commits;
- covering commands and summarized results;
- spec-compliance verdict;
- document-quality verdict;
- fixed Critical/Important findings and re-review outcome;
- remaining Minor findings for final review.

## Verification Summary

The implementation records final results for:

```bash
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh
bash scripts/validation/check-repo-contracts.sh
```

Plan-authoring checks are recorded in the current progress entry and commit;
task-specific results are added here during execution.

## Deviation Notes

No implementation deviation exists at plan creation. Any later deviation must
name the affected task, plan requirement, reason, approval or evidence owner,
verification impact, and final disposition.

## Related Documents

- **Parent Spec**:
  [Agentic Research Pack Consolidation](../../03.specs/122-agentic-research-pack-consolidation/spec.md)
- **Parent Plan**:
  [Agentic Research Pack Consolidation Plan](../plans/2026-07-10-agentic-research-pack-consolidation.md)
- **Previous Task Evidence**:
  [Agentic Research Pack Refresh](./2026-07-05-agentic-research-pack-refresh.md)
- **Canonical Research Pack**:
  [Agentic Engineering Research Pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- **Research Category**:
  [Research References](../../90.references/research/README.md)
