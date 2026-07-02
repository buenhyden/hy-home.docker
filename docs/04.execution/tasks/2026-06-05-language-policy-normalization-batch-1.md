---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-06-05-language-policy-normalization-batch-1.md -->

# Task: Language Policy Normalization Batch 1

## Overview

This task records the second implementation pass for the repository language
policy goal. It normalizes a bounded set of `docs/03.specs` leaf documents to
English and adds explicit category-level purpose/language rules for
`docs/90.references`.

## Inputs

- **User Objective**: Continue applying clear language-writing rules across
  agent-facing, human-facing, and mixed documentation surfaces.
- **Requested Skills**: `document-release`, `humanize-korean`.
- **Parent Audit Evidence**: [Language Policy Boundary Audit](./2026-06-05-language-policy-boundary-audit.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)

## Working Rules

- `docs/03.specs/**` leaf documents are English-only technical contracts.
- `docs/90.references/**` documents are stable references, not active policy,
  runbooks, plans, tasks, runtime truth, or incident evidence.
- Human-facing reference README and learning/glossary/reference prose use
  Korean by default while preserving upstream technical terms.
- LLM/generated/HADS/machine-readable reference surfaces may use English when
  that improves provider-neutral parsing or validator consistency.
- Preserve commands, paths, service names, agent names, evidence IDs, Docker
  profiles, environment variables, image names, and upstream terms exactly.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `docs/03.specs` bounded leaf batch and `docs/90.references` README/category rules | User-provided language policy objective | 9 spec/agent-design files; 7 reference README files | `docs/03.specs` leaf backlog was 23 files; reference category READMEs had roles but not explicit language rules | 9 `docs/03.specs` leaf files have no Korean text or legacy Korean-labeled overview headings; reference category roles now include language rules | `git revert` or equivalent patch | No secret values, token, private key, certificate contents, or `.env` values |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Normalize a bounded `docs/03.specs` leaf batch to English. | doc | User constraint / specs English-only | Language normalization batch 1 | Korean-character scan and legacy overview-heading scan against 9 target files | Codex | Done |
| T-002 | Add `docs/90.references` purpose/language rules at repository and category levels. | doc | User constraint / references purpose and language rules | Reference language boundary | `bash scripts/validation/check-repo-contracts.sh` | Codex | Done |
| T-003 | Update progress and generated indexes after adding this task evidence. | doc | Documentation release workflow | Evidence closure | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | Codex | Done |

## Normalized Spec Files

The following English-only target files now have no Korean text and no
legacy Korean-labeled overview heading:

- [Open WebUI Spec](../../03.specs/08-ai/open-webui.md)
- [LLM Wiki Spec](../../03.specs/llm-wiki-agent-first-completion/spec.md)
- [Docs Taxonomy Migration Spec](../../03.specs/docs-taxonomy-agent-first-migration/spec.md)
- [Communication Tier Spec](../../03.specs/10-communication/spec.md)
- [Home Docker Revalidation Follow-up Spec](../../03.specs/home-docker-revalidation-deferred-follow-up/spec.md)
- [Analytics Tier Spec](../../03.specs/04-data-analytics/spec.md)
- [Gateway Tier Spec](../../03.specs/01-gateway/spec.md)
- [Standardize Infra Net Spec](../../03.specs/standardize-infra-net/spec.md)
- [Workflow Cross-Validation Agent Design](../../03.specs/07-workflow/agent-design.md)

## Reference Role Coverage

| Reference Category | Role Clarified | Language Rule Added |
| --- | --- | --- |
| `docs/90.references/README.md` | Repository-level stable reference role and category routing | Korean for human-facing references; English allowed for generated/LLM/HADS/machine-readable surfaces |
| `docs/90.references/data/docker/README.md` | Docker image/version interpretation and registry context | Korean prose with image/tag, Compose path, JSON key, and command terms preserved |
| `docs/90.references/data/glossary/README.md` | Stable vocabulary and stage-boundary terms | Korean definitions with canonical stage and technical terms preserved |
| `docs/90.references/data/hads/README.md` | HADS profile and validator-backed AI-readable boundary | English allowed for HADS/profile/validator terms; Korean explanatory notes allowed |
| `docs/90.references/data/kubernetes/README.md` | Kubernetes and k3s/k3d migration reference context | Korean prose with Kubernetes/k3s/k3d resource terms preserved |
| `docs/90.references/data/learning/README.md` | CS/CE/SE learning roadmap and theory references | Korean learning prose with source titles and upstream terms preserved |
| `docs/90.references/data/llm-wiki/README.md` | Repo-local LLM navigation map and generated path index | Korean README; English allowed for generated indexes and LLM-facing navigation |

## Validation Results

| Command | Result |
| --- | --- |
| Korean-character and legacy overview-heading scan against the 9 normalized target files | PASS: no matches after normalization. |
| Korean-character file count under `docs/03.specs` excluding `README.md` | 14 leaf files remain after this batch. |
| Korean-character file count under `docs/04.execution/plans` excluding `README.md` | 57 leaf files remain before plan normalization. |
| Korean-character file count under `docs/04.execution/tasks` excluding `README.md` | 59 leaf files remain before task normalization. |
| Repository-wide legacy overview-heading scan | PASS: no legacy overview-heading matches remain after heading normalization. |
| `bash scripts/validation/check-repo-contracts.sh` | PASS: failures=0. |
| `bash scripts/validation/check-doc-traceability.sh` | PASS: failures=0. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS after regenerating `docs/90.references/data/llm-wiki/index.md` for the new task path. |
| `git diff --check` | PASS. |

## Verification Summary

- **Test Commands**:
  - `git diff --check`
  - `bash scripts/validation/check-repo-contracts.sh`
  - `bash scripts/validation/check-doc-traceability.sh`
  - `bash scripts/knowledge/generate-llm-wiki-index.sh --check`
- **Eval Commands**: N/A for documentation language normalization.
- **Logs / Evidence Location**: This task and
  `docs/00.agent-governance/memory/progress.md`.

## Remaining Risks

- Full English-only normalization remains incomplete: 14 `docs/03.specs` leaf
  files, 57 plan leaf files, and 59 task leaf files still contain Korean text.
- `docs/90.references` now has category language rules, but non-README
  reference documents were not bulk-polished in this batch.
- Repository-wide legacy overview headings were normalized to `Overview`, and
  the validator now uses `## Overview` as the required heading.

## Follow-up Tasks

- Continue `docs/03.specs` leaf normalization in bounded batches.
- Normalize `docs/04.execution/plans/**` leaf documents to English.
- Normalize `docs/04.execution/tasks/**` leaf documents to English while
  preserving historical evidence meaning.
- Review non-README `docs/90.references/**` documents for category language-rule
  consistency.
- After active normalization, add hard Korean-character enforcement for
  English-only surfaces.

## Related Documents

- **Boundary Audit Task**: [2026-06-05-language-policy-boundary-audit.md](./2026-06-05-language-policy-boundary-audit.md)
- **Task Index**: [README.md](./README.md)
- **References Index**: [../../90.references/README.md](../../90.references/README.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
