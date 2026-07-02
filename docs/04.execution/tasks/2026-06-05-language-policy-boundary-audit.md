---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-06-05-language-policy-boundary-audit.md -->

# Task: Language Policy Boundary Audit

## Overview

This task records the first implementation pass for the repository-wide
language boundary goal. It aligns the canonical policy, root README, docs
README, templates, and operations bucket roles so future document edits can
consistently separate agent-facing English contracts from human-facing Korean
project and operations content.

## Inputs

- **User Objective**: Apply a clear Language Policy across AI Agent documents,
  human-facing project documents, and mixed-audience documents.
- **Expanded Objective**: Apply language-writing rules across other `docs/**`
  surfaces and root `README.md`.
- **Requested Skills**: `document-release`, `humanize-korean`.
- **Governance Policy**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)

## Working Rules

- `docs/03.specs/**` must be English-only.
- `docs/04.execution/plans/**` must be English-only.
- `docs/04.execution/tasks/**` must be English-only.
- `docs/05.operations/{guides,incidents,policies,runbooks}/**` must preserve
  bucket roles and use Korean for human-facing prose while preserving technical
  identifiers exactly.
- Root `README.md`, folder READMEs, requirements, references, and other
  human-facing docs are Korean by default unless their target stage requires
  English.
- Mixed-audience docs preserve machine-checkable contracts in English and use
  Korean for human-facing context.
- Do not rewrite historical evidence in bulk without a bounded follow-up batch
  and validation evidence.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| Governance / templates / validation / root and docs README / operations README docs | User-provided language policy objective | `README.md`, `docs/README.md`, `docs/00.agent-governance/**`, `docs/99.templates/**`, `docs/05.operations/**`, `scripts/validation/check-repo-contracts.sh` | `docs/03` and `docs/04` templates used legacy Korean-labeled overview headings; active English-only stage docs still contain Korean text; root and docs README language boundaries were too broad | Language boundary policy added; root/docs README boundaries clarified; English-only templates normalized; operations bucket roles clarified; current drift recorded below | `git revert` or equivalent patch | No secret values, token, private key, or certificate contents |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Audit Korean text in English-only spec, plan, and task surfaces. | doc | User objective / item 1 | Language boundary audit | Korean-character file scan across specs, plans, and tasks | Codex | Done |
| T-002 | Align Stage 00 language policy and stage matrix. | doc | User objective / item 2 | Policy baseline | `bash scripts/validation/check-repo-contracts.sh` | Codex | Done |
| T-003 | Normalize English-only templates for specs, plans, and tasks. | doc | User objective / constraints | Template baseline | Korean-character and legacy overview-heading scan across English-only templates | Codex | Done |
| T-004 | Clarify operations guide/policy/runbook/incident bucket roles and Korean human-facing language boundary. | doc | User objective / operations constraint | Operations README baseline | `bash scripts/validation/check-repo-contracts.sh` | Codex | Done |
| T-005 | Clarify repository-wide README and docs-stage language rules beyond the original spec/plan/task/operations scope. | doc | Expanded user objective | README and stage baseline | `bash scripts/validation/check-repo-contracts.sh` | Codex | Done |

## Language Boundary Coverage Map

| Surface | Required Language Boundary | Current Evidence | Status |
| --- | --- | --- | --- |
| `docs/00.agent-governance/**` | English-only | Existing governance policy and README already require English-only. | Covered |
| Root `README.md` | Korean human-facing entrypoint; technical identifiers unchanged | Documentation standards now include the repository language table. | Covered for README contract |
| `docs/README.md` | Korean human-facing docs entrypoint; stage-specific boundaries explicit | Documentation standards now include the docs language table. | Covered for README contract |
| `docs/01.requirements/**` | Korean human-facing requirements; technical identifiers unchanged | Added to governance protocol and stage matrix. | Covered for policy contract |
| `docs/02.architecture/**` | Mixed audience: Korean rationale; English IDs/titles/quality attributes preserved | Added to governance protocol and stage matrix. | Covered for policy contract |
| `docs/03.specs/**` templates | English-only | English-only rule added; template Korean text removed. | Covered for new/changed templates |
| `docs/04.execution/plans/**` template | English-only | English-only rule added; template Korean text removed. | Covered for new/changed templates |
| `docs/04.execution/tasks/**` template | English-only | English-only rule added; template Korean text removed. | Covered for new/changed templates |
| `docs/05.operations/guides/**` | Korean human-facing guide body; technical identifiers unchanged | Guide README and template updated with role/language boundary. | Covered for bucket contract |
| `docs/05.operations/policies/**` | Korean human-facing controls; technical identifiers unchanged | Policy README and template updated with role/language boundary. | Covered for bucket contract |
| `docs/05.operations/runbooks/**` | Korean human-facing procedure; commands/evidence unchanged | Runbook README and template updated with role/language boundary. | Covered for bucket contract |
| `docs/05.operations/incidents/**` | Korean incident narrative; technical evidence unchanged | Incidents README updated with role/language boundary. | Covered for bucket contract |
| `docs/90.references/**` | Audience-specific: generated/LLM indexes may be English; human references Korean by default | Added to governance protocol, matrix, and README language tables. | Covered for policy contract |
| `docs/98.archive/**` | Concise tombstones; preserve original paths, IDs, dates, and titles | Added to governance protocol, matrix, and README language tables. | Covered for policy contract |
| `docs/99.templates/**` | Match target stage language boundary | README and template language rules updated. | Covered for template contract |

## Audit Findings

| Check | Result | Notes |
| --- | --- | --- |
| Korean text in `docs/03.specs` | 43 files total; 23 non-README leaf files | Active document normalization remains a follow-up batch. |
| Korean text in `docs/04.execution/plans` | 58 files total; 57 non-README leaf files | Active document normalization remains a follow-up batch. |
| Korean text in `docs/04.execution/tasks` | 61 files total; 60 non-README leaf files | Active document normalization remains a follow-up batch. |
| Korean text or legacy Korean-labeled overview headings in English-only templates | 0 matches after this pass | Applies to spec, API spec, agent design, data model, service, tests, plan, and task templates. |
| Korean text in `docs/00.agent-governance` | 0 files | Existing governance surface already matches English-only policy. |
| Korean text in human-facing/mixed surfaces | Expected | `docs/01.requirements`, `docs/02.architecture`, `docs/05.operations`, `docs/90.references`, `docs/98.archive`, `docs/99.templates`, root `README.md`, and folder READMEs now have explicit boundary rules instead of a single broad default. |

## Validation Results

| Command | Result |
| --- | --- |
| Korean-character file count under `docs/03.specs` | 43 files before active-doc normalization. |
| Korean-character file count under `docs/03.specs` excluding `README.md` | 23 non-README leaf files before active-doc normalization. |
| Korean-character file count under `docs/04.execution/plans` | 58 files before active-doc normalization. |
| Korean-character file count under `docs/04.execution/plans` excluding `README.md` | 57 non-README leaf files before active-doc normalization. |
| Korean-character file count under `docs/04.execution/tasks` | 61 files before active-doc normalization. |
| Korean-character file count under `docs/04.execution/tasks` excluding `README.md` | 60 non-README leaf files before active-doc normalization. |
| Korean-character and legacy overview-heading scan across English-only templates | PASS: no matches after template normalization. |
| `bash scripts/validation/check-repo-contracts.sh` | PASS: failures=0. |
| `bash scripts/validation/check-doc-traceability.sh` | PASS: failures=0. |
| `bash scripts/validation/validate-harness.sh` | PASS: wrapper, traceability, implementation alignment, Compose, hardening, template/security baseline, and repository contracts passed. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS after regenerating `docs/90.references/data/llm-wiki/index.md` for the new task path. |
| `git diff --check` | PASS. |

## Verification Summary

- **Test Commands**:
  - `bash scripts/validation/check-repo-contracts.sh`
  - `bash scripts/validation/check-doc-traceability.sh`
  - `bash scripts/validation/validate-harness.sh`
  - `bash scripts/knowledge/generate-llm-wiki-index.sh --check`
  - `git diff --check`
- **Eval Commands**: N/A for documentation policy and template alignment.
- **Logs / Evidence Location**: This task and
  `docs/00.agent-governance/memory/progress.md`.

## Remaining Risks

- Full active-document normalization is not complete. Current audit found 162
  Markdown files with Korean text under English-only spec/plan/task surfaces
  when README and folder-index files are included, and 140 non-README leaf
  documents that still need bounded English normalization.
- Repo contracts now require `## Overview`; historical Korean-labeled overview
  headings have been normalized repository-wide.
- Existing human-facing and mixed-audience documents outside the edited README
  and template surfaces were not bulk-polished in this pass; they now have a
  policy target for future bounded batches.
- No hard language-boundary gate was added yet. Enforcing it immediately would
  fail against the known spec/plan/task normalization backlog.

## Follow-up Tasks

- Normalize active `docs/03.specs/**` documents to English in bounded batches.
- Normalize active `docs/04.execution/plans/**` documents to English in bounded
  batches.
- Normalize active `docs/04.execution/tasks/**` documents to English in bounded
  batches, preserving historical evidence meaning.
- Review `docs/01.requirements/**`, `docs/02.architecture/**`,
  `docs/90.references/**`, and `docs/98.archive/**` in bounded batches for
  consistency with the newly documented mixed/human-facing rules.
- Add a repo-contract language-boundary gate after the English-only backlog is
  remediated and any README/folder-index exceptions are explicitly modeled.
- After active normalization, add hard Korean-character enforcement for
  English-only surfaces.

## Related Documents

- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Templates README**: [Templates README](../../99.templates/README.md)
- **Operations Guides**: [Operations guides README](../../05.operations/guides/README.md)
- **Operations Policies**: [Operations policies README](../../05.operations/policies/README.md)
- **Operations Runbooks**: [Operations runbooks README](../../05.operations/runbooks/README.md)
- **Incident Records**: [Incident records README](../../05.operations/incidents/README.md)
