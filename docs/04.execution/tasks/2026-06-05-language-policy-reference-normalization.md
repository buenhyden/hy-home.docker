---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-06-05-language-policy-reference-normalization.md -->

# Task: Language Policy Reference Normalization

## Overview

This task records the bounded `docs/90.references` normalization pass for the
repository language policy goal. It closes the remaining non-README reference
category consistency backlog that was left after the spec, plan, and task leaf
surfaces reached zero Korean-character files.

## Inputs

- **User Objective**: Finish work called out under Remaining Risks and Follow-up
  Tasks for the repository language policy goal.
- **Requested Skills**: `document-release`, `humanize-korean`.
- **Previous Evidence**: [Language Policy Task Normalization Batch 7](./2026-06-05-language-policy-task-normalization-batch-7.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)

## Working Rules

- Non-README `docs/90.references/**` reference documents must be consistent
  with the English-only language boundary before hard enforcement is added.
- Generated `docs/90.references/llm-wiki/index.md` is excluded from the
  reference language scan because it is path-only generated output.
- Preserve commands, paths, service names, evidence IDs, upstream terms, runtime
  values, no-touch boundaries, and historical audit numbers exactly.
- Treat stale Graphify output as advisory only; corroborate against tracked
  source files and validators.
- Keep this task evidence English-only because `docs/04.execution/tasks/**`
  is an English-only execution evidence surface.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `docs/90.references` non-README reference documents | User continuation request for remaining risks and follow-up tasks | 7 reference files | 7 non-README reference files contained Korean text, excluding generated `llm-wiki/index.md` | 0 non-README reference files contain Korean text under the same exclusions | `git revert` or equivalent patch | No secret values, tokens, private keys, certificate contents, raw logs, shell history, or `.env` values |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Normalize the remaining non-README `docs/90.references` files to English-only content. | doc | User constraint / reference language consistency | Reference normalization pass | Korean-character scan against `docs/90.references` with README and generated-index exclusions | Codex | Done |
| T-002 | Confirm the prior specs, plans, and tasks English-only closure remains intact. | doc | Language policy boundary audit | Follow-up closure | Korean-character file counts for specs, plans, and tasks | Codex | Done |
| T-003 | Refresh generated index evidence for the new task path. | doc | Documentation release workflow | Evidence closure | LLM Wiki index generation and check | Codex | Done |

## Normalized Reference Files

The following non-README reference files now have no Korean text:

- [Docker image version interpretation](../../90.references/docker/image-version-interpretation.md)
- [Stable reference terms](../../90.references/glossary/stable-reference-terms.md)
- [HADS profile](../../90.references/hads/profile.md)
- [Docker Compose to k3s/k3d migration](../../90.references/kubernetes/docker-compose-to-k3s-migration.md)
- [Learning roadmap v1](../../90.references/learning/roadmap-v1.md)
- [Learning roadmap](../../90.references/learning/roadmap.md)
- [LLM Wiki repository map](../../90.references/llm-wiki/repository-map.md)

## Validation Results

| Command | Result |
| --- | --- |
| Korean-character file count under `docs/90.references`, excluding `README.md` and generated `llm-wiki/index.md` | 0 files remain. |
| Korean-character file count under `docs/03.specs`, excluding `README.md` | 0 leaf files remain. |
| Korean-character file count under `docs/04.execution/plans`, excluding `README.md` | 0 leaf files remain. |
| Korean-character file count under `docs/04.execution/tasks`, excluding `README.md` | 0 leaf files remain. |
| `git diff --check` | PASS. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh` | PASS: generated `docs/90.references/llm-wiki/index.md` with 1077 paths. |

## Verification Summary

- **Test Commands**:
  - Korean-character file count under `docs/90.references`, excluding
    `README.md` and generated `llm-wiki/index.md`
  - Korean-character file counts for `docs/03.specs`, `docs/04.execution/plans`,
    and `docs/04.execution/tasks`
  - `git diff --check`
  - `bash scripts/knowledge/generate-llm-wiki-index.sh`
- **Eval Commands**: N/A for documentation language normalization.
- **Logs / Evidence Location**: This task and
  `docs/00.agent-governance/memory/progress.md`.

## Remaining Risks

- The non-README `docs/90.references/**` reference consistency backlog is
  closed.
- Hard Korean-character enforcement still needs to be added for the closed
  English-only surfaces so future drift fails validation.

## Follow-up Tasks

- Add hard Korean-character enforcement for the closed English-only surfaces in
  repository validation.

## Related Documents

- **Boundary Audit Task**: [2026-06-05-language-policy-boundary-audit.md](./2026-06-05-language-policy-boundary-audit.md)
- **Final Task Normalization Evidence**: [2026-06-05-language-policy-task-normalization-batch-7.md](./2026-06-05-language-policy-task-normalization-batch-7.md)
- **Task Index**: [README.md](./README.md)
- **Plans Index**: [../plans/README.md](../plans/README.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
