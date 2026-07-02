---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-17-requirements-standardization.md -->

# docs/01.requirements Remediation Plan

## Overview

This document is the implementation plan for aligning the `docs/01.requirements` PRD document set with the `docs/99.templates/templates/sdlc/prd.template.md` contract. It restores document structure, link traceability, canonical docs taxonomy, and validation evidence without changing the product meaning of the requirements.

## Context

`docs/01.requirements` is the starting point for overall design and implementation, but some PRDs deviate from template section names, H1 format, and Related Documents link format. Existing `docs/superpowers/` artifacts also remain tracked and break the repo top-level docs taxonomy, while the LLM Wiki index is stale from before path changes.

## Goals & In-Scope

- **Goals**:
  - Make 23 PRDs and `docs/01.requirements/README.md` follow the PRD stage purpose and template rules.
  - Standardize Related Documents links as clickable target-relative Markdown links.
  - Remove tracked legacy artifacts under `docs/superpowers/` to restore the canonical docs taxonomy.
  - Synchronize the LLM Wiki index and governance progress log with the current documentation state.
- **In Scope**:
  - `docs/01.requirements/`
  - `docs/99.templates/templates/sdlc/prd.template.md`
  - adjacent auth traceability link in `docs/02.architecture/requirements/0002-auth-architecture.md`
  - `docs/04.execution/plans/README.md`
  - `docs/00.agent-governance/memory/progress.md`
  - `docs/90.references/llm-wiki/llm-wiki-index.md`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not newly define PRD product requirements, priorities, success metrics, or service behavior.
  - Do not create new PRD, ARD, ADR, Spec, Task, or Operations documents.
  - Do not invent the absence of gateway and communication hardening PRDs as new TODOs or requirements.
- **Out of Scope**:
  - Runtime configuration, Docker Compose behavior, service settings, and public API changes
  - unrelated untracked `projects/storybook/mcp/`

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Remove tracked legacy artifacts under `docs/superpowers/` | `docs/superpowers/**` | REQ-PRD-DOC-001 | `test ! -d docs/superpowers` |
| PLN-002 | Update PRD template Related Documents examples to clickable Markdown links | `docs/99.templates/templates/sdlc/prd.template.md` | REQ-PRD-DOC-002 | Template keeps target-relative guidance and has no backticked pseudo-links |
| PLN-003 | Normalize PRD H1s and required sections to the template contract | `docs/01.requirements/*.md` | REQ-PRD-DOC-003 | PRD scan: exactly one H1, required sections present |
| PLN-004 | Fix Related Documents links and auth ADR placeholder | `docs/01.requirements/*.md`, `docs/02.architecture/requirements/0002-auth-architecture.md` | REQ-PRD-DOC-004 | No backticked pseudo-links, no `####-` placeholder paths, local links resolve |
| PLN-005 | Update execution plan index and governance progress | `docs/04.execution/plans/README.md`, `docs/00.agent-governance/memory/progress.md` | REQ-PRD-DOC-005 | Parent README references this plan, progress log records evidence |
| PLN-006 | Regenerate LLM Wiki index | `docs/90.references/llm-wiki/llm-wiki-index.md` | REQ-PRD-DOC-006 | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` passes |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Workspace | Confirm unrelated untracked Storybook MCP remains no-touch | `git status --short --untracked-files=all` | `projects/storybook/mcp/` may remain untracked; no unintended files appear |
| VAL-PLN-002 | PRD Structure | Count and validate PRD structural contract | Custom Python scan over `docs/01.requirements/2026-*.md` | 23 PRDs, `status: draft`, Target comments, one H1, required sections, no broken local links |
| VAL-PLN-003 | Link Format | Ensure pseudo-links are gone | Custom scan for backticked Related Documents pseudo-links | No matches |
| VAL-PLN-004 | Placeholder/H1 | Ensure placeholder paths and invalid H1s are gone | `rg -n '####-\|^# PRD\|^# Product Requirements Document\|Product Requirements Document$' docs/01.requirements/2026-*.md` | No matches |
| VAL-PLN-005 | Wiki Freshness | Verify generated LLM Wiki index is current | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS |
| VAL-PLN-006 | Traceability | Verify plan/operations traceability remains synchronized | `bash scripts/validation/check-doc-traceability.sh` | PASS |
| VAL-PLN-007 | Repo Contract | Verify repository contracts pass | `bash scripts/validation/check-repo-contracts.sh` | PASS |
| VAL-PLN-008 | Diff Hygiene | Verify no whitespace errors | `git diff --check` | PASS |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Section additions accidentally invent product scope | High | Add only summaries derived from existing bullets in the same PRD or linked canonical docs |
| Canonical taxonomy remains broken after deletion | High | Remove tracked `docs/superpowers` files and verify with `check-repo-contracts.sh` |
| LLM Wiki index remains stale after path changes | Medium | Regenerate index and run `generate-llm-wiki-index.sh --check` |
| Unrelated untracked Storybook MCP gets staged | High | Do not stage or edit `projects/storybook/mcp/`; verify with `git status --short --untracked-files=all` |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Custom PRD structural/link scan must pass before final validators.
- **Sandbox / Canary Rollout**: Not applicable; documentation-only remediation.
- **Human Approval Gate**: This plan is based on the user-approved remediation scope.
- **Rollback Trigger**: Revert only this branch's scoped documentation changes if repo contract or PRD scans cannot be made to pass.
- **Prompt / Model Promotion Criteria**: Not applicable; no model or prompt runtime changes.

## Completion Criteria

- [x] Scoped PRD/template/taxonomy cleanup completed
- [x] LLM Wiki index regenerated
- [x] Required validation commands passed
- [x] `projects/storybook/mcp/` left untouched

## Related Documents

- **PRD README**: [../../01.requirements/README.md](../../01.requirements/README.md)
- **Execution Task**: [../tasks/2026-05-17-requirements-standardization.md](../tasks/2026-05-17-requirements-standardization.md)
- **PRD Template**: [../../99.templates/templates/sdlc/prd.template.md](../../99.templates/templates/sdlc/prd.template.md)
- **README Template**: [../../99.templates/templates/common/readme.template.md](../../99.templates/templates/common/readme.template.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
