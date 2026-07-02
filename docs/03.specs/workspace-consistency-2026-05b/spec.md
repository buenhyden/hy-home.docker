---
status: completed
---

<!-- Target: docs/03.specs/workspace-consistency-2026-05b/spec.md -->

# Workspace Doc & Governance Consistency (2026-05b) Technical Specification

## Overview

This document is the technical specification for follow-up work after PR #89 (`workspace-doc-consistency-2026-05`). It completes workspace consistency through governance rule formalization (R4 Operations Profile Compliance, R5 Frontmatter Status), validation script expansion, templates, and small documentation fixes. As a result of this specification, `documentation-protocol.md` and the validation scripts fully align with the actual file baseline.

## Strategic Boundaries & Non-goals

**Scope:**

- `docs/00.agent-governance/rules/documentation-protocol.md`: add R4 (Operations Profile Compliance) and R5 (Frontmatter Status) rules.
- `docs/00.agent-governance/rules/github-governance.md`: add CI/CD job taxonomy section (Section 8).
- `scripts/validation/check-repo-contracts.sh`: add `## Common Checks` and `## Runbook Handoff` section requirements to guide profile checks.
- `docs/99.templates/README.md`: add guide.template.md and runbook.template.md to the list and add a design note for link conventions.
- `docs/99.templates/templates/spec-contracts/agent-design.template.md`: replace example filenames with directory links.
- `docs/05.operations/policies/01-gateway/nginx.md`: remove duplicate `## Policy Scope` heading.

**Non-goals:**

- No structural changes to docs/01~04.
- No new feature requirements.
- No Docker Compose or service configuration changes.
- No secret value or .env changes.

## Related Inputs

- **PRD**: No matching PRD; this is an iterative workspace governance improvement session.
- **ARD**: No matching ARD.
- **Related ADRs**: No matching ADR.
- **Predecessor Spec**: [../../03.specs/workspace-doc-consistency-2026-05/spec.md](../../03.specs/workspace-doc-consistency-2026-05/spec.md)

## Contracts

- **Config Contract**: all changes follow the `docs/99.templates/*.template.md` baseline.
- **Data / Interface Contract**:
  - R4: Operations guides must include `## Usage`, `## Common Checks`, and `## Runbook Handoff` sections.
  - R5: every operations document (guides/policies/runbooks) requires a `status:` frontmatter field.
  - CI/CD taxonomy: classify workflow jobs into lint, test, build, security, deploy, and notify tiers.
- **Governance Contract**: all changes must satisfy the completion criteria in `task-checklists.md`. Only structural/formatting fixes are allowed; body meaning changes are forbidden.

## Core Design

- **Component Boundary**: `docs/00.agent-governance/rules/`, `scripts/validation/`, `docs/99.templates/`, `docs/05.operations/policies/`
- **Key Dependencies**: `docs/99.templates` (baseline documents), `scripts/validation/` (validation scripts)
- **Tech Stack**: bash, git (Conventional Commits)
- **Execution Strategy**: Documentation-first: add rule documents -> strengthen scripts -> update templates/documents.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: no file structure changes. Only update section headings, add content, and remove duplicates in existing files.
- **Migration / Transition Plan**: separate each change into an independent commit to preserve rollbackability.

## Interfaces & Data Structures

### Applied Rules Summary

| Document Type           | Change                                             | Target State                                            |
| ------------------------ | -------------------------------------------------- | ------------------------------------------------------- |
| documentation-protocol   | Add R4, R5 rules                                   | Specify Operations guides profile and frontmatter requirements |
| github-governance        | Add Section 8 CI/CD taxonomy                       | Document CI/CD job classification system                |
| check-repo-contracts     | Strengthen guide profile checks                    | Include `## Common Checks`, `## Runbook Handoff` section validation |
| docs/99.templates/README | Add guide/runbook template list and link convention note | Refresh full template list                              |
| agent-design.template    | Replace example filename with directory link       | No virtual filename                                     |
| nginx.md                 | Remove duplicate `## Policy Scope` heading         | Exactly one heading exists                              |

## API Contract (If Applicable)

- **API Spec**: N/A

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: AI Agent uses this specification to add governance rules, expand scripts, and update templates/documents.
- **Inputs**: `docs/99.templates/*.template.md` (baseline), `docs/00.agent-governance/rules/` (edit target), `scripts/validation/` (edit target), `docs/05.operations/` (edit target)
- **Outputs**: updated Markdown/shell files and git commit history
- **Success Definition**: `check-repo-contracts.sh` and `check-doc-traceability.sh` pass with failures=0.

## Tools & Tool Contract (If Applicable)

- **Tool List**: bash, git
- **Permission Boundary**: only files under `docs/00.agent-governance/rules/`, `scripts/validation/`, `docs/99.templates/`, and `docs/05.operations/policies/` may be modified.
- **Failure Handling**: when scripts fail, review `git diff` and roll back.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**: N/A
- **Policy Constraints**: N/A
- **Versioning Rule**: N/A

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: N/A
- **Long-term Memory**: N/A
- **Retrieval Boundary**: N/A

## Guardrails (If Applicable)

- **Input Guardrails**: check the current target-file state with grep before changes.
- **Output Guardrails**: after each change, use validation commands to confirm zero remaining mismatches.
- **Blocked Conditions**: do not commit when validation scripts fail.
- **Escalation Rule**: stop immediately and report to a human when unexpected pattern changes are found.

## Evaluation (If Applicable)

- **Eval Types**: structural validation (bash/grep-based)
- **Metrics**: validation failure count, which must be 0
- **Datasets / Fixtures**: all modified files
- **How to Run**: see the Verification section below

## Edge Cases & Error Handling

- **Error 1**: choose rule insertion position while preserving existing section order and numbering.
- **Error 2**: existing files fail after script check strengthening; update those files to match the spec.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: script changes introduce false positives.
- **Fallback**: review `git diff`, then roll back with `git checkout -- <file>`.
- **Human Escalation**: report to a human when validation scripts fail unexpected files.

## Verification

```bash
cd /home/hy/projects/hy-home.docker

# Confirm R4/R5 rules exist
grep -c "R4\|R5" docs/00.agent-governance/rules/documentation-protocol.md

# Confirm CI/CD taxonomy section exists
grep -c "CI/CD" docs/00.agent-governance/rules/github-governance.md

# Confirm guide profile check strengthening
grep "Common Checks" scripts/validation/check-repo-contracts.sh

# repo contracts validation
bash scripts/validation/check-repo-contracts.sh

# doc traceability validation
bash scripts/validation/check-doc-traceability.sh
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: R4 and R5 rules exist in `documentation-protocol.md`.
- **VAL-SPC-002**: CI/CD job taxonomy section (Section 8) exists in `github-governance.md`.
- **VAL-SPC-003**: `check-repo-contracts.sh` checks `## Common Checks` and `## Runbook Handoff`.
- **VAL-SPC-004**: `docs/99.templates/README.md` includes guide.template.md and runbook.template.md in the list.
- **VAL-SPC-005**: `nginx.md` has no duplicate `## Policy Scope` heading.
- **VAL-SPC-006**: `bash scripts/validation/check-repo-contracts.sh` passes with failures=0.
- **VAL-SPC-007**: `bash scripts/validation/check-doc-traceability.sh` passes with failures=0.

## Related Documents

- **Predecessor Spec**: [workspace-doc-consistency-2026-05 spec](../../03.specs/workspace-doc-consistency-2026-05/spec.md)
- **Plan**: [2026-05-29 workspace consistency 2026-05b plan](../../04.execution/plans/2026-05-29-workspace-consistency-2026-05b.md)
- **Tasks**: [2026-05-29 workspace consistency 2026-05b tasks](../../04.execution/tasks/2026-05-29-workspace-consistency-2026-05b.md)
- **Templates**: [docs/99.templates/](../../99.templates/)
- **Governance Rules**: [docs/00.agent-governance/rules/](../../00.agent-governance/rules/)
