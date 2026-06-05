---
status: completed
---

<!-- Target: docs/03.specs/workspace-doc-consistency-2026-05/spec.md -->

# Workspace Documentation Consistency 2026-05 Technical Specification

## Overview

This document is the technical specification for the May 2026 workspace documentation consistency and standardization improvement work. It systematically fixes structural inconsistencies across docs/01~05, scripts/, and .github/workflows/ identified by the `workspace-audit-2026-05` audit, and updates governance files. As a result of this specification, all documents referenced by AI Agents during work align with the template baseline.

## Strategic Boundaries & Non-goals

**Scope:**

- docs/02.architecture: standardize ADR/ARD title format
- docs/01.requirements: add missing sections (Overview, AI Agent Requirements)
- docs/03.specs: add Agent Role & IO Contract sections to 15 spec files, marked N/A where applicable
- docs/04.execution: standardize task file title prefixes and add suffixes to active plan titles
- docs/05.operations/policies: standardize `## Applies To` -> `## Policy Scope` headings across about 50 files
- docs/05.operations/guides, runbooks: add frontmatter `status:` fields
- docs/05.operations/incidents: add README template links
- docs/99.templates: confirm baseline, with no changes
- scripts/: fix executable permissions and shebangs for 2 files
- .github/workflows/: refresh GitHub Actions SHAs for 5 files
- docs/00.agent-governance/rules/: specify Policy Scope baseline and ADR/ARD title format rules

**Non-goals:**

- Document body/content revision; only structural/formatting fixes are performed.
- New requirements; only existing template baseline compliance is applied.
- Docker Compose or service configuration changes.
- Secret value or .env changes.
- Substantive changes to docs/99.templates.

## Related Inputs

- **PRD**: No matching PRD; this is an iterative workspace governance improvement session.
- **ARD**: No matching ARD.
- **Related ADRs**: No matching ADR.
- **Upstream Audit**: [../../03.specs/workspace-audit-2026-05/spec.md](../../03.specs/workspace-audit-2026-05/spec.md)

## Contracts

- **Config Contract**: all changes follow the `docs/99.templates/*.template.md` baseline.
- **Data / Interface Contract**:
  - ADR title format: `# ADR-NNNN: English Title`
  - ARD title format: `# Domain Architecture Reference Document (ARD)`
  - Policy heading: `## Policy Scope` (not `## Applies To`)
  - Agent Role section: `## Agent Role & IO Contract (If Applicable)`; use N/A when not applicable
  - Task title format: `# Task: [Task Name]`
  - frontmatter: every operations document (guides/policies/runbooks) requires a `status:` field
- **Governance Contract**: all changes must satisfy the completion criteria in `task-checklists.md`. Only structural/formatting fixes are allowed; body meaning changes are forbidden.

## Core Design

- **Component Boundary**: docs/01~05, scripts/, .github/workflows/, docs/00.agent-governance/rules/
- **Key Dependencies**: docs/99.templates (baseline documents), scripts/validation/ (validation scripts)
- **Tech Stack**: bash, sed, git (Conventional Commits)
- **Execution Strategy**: Foundation-first: confirm template baseline -> fix titles/structure -> perform bulk repeated fixes -> apply technical fixes -> synchronize governance.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: no file structure changes. Only frontmatter and section headings in existing files are modified.
- **Migration / Transition Plan**: separate each phase into an independent commit to preserve rollbackability.

## Interfaces & Data Structures

### Applied Rules Summary

| Document Type | Field/Heading | Existing Pattern                    | Target Pattern                                    |
| ---------- | ----------- | ----------------------------------- | -------------------------------------------------- |
| ADR        | H1 title    | `# ADR:`, `# ADR-YYYYMMDD:`, non-English | `# ADR-NNNN: English`                         |
| ARD        | H1 title    | `# ARD:`, no suffix                 | `# Domain ARD (ARD)`                               |
| Spec       | Section     | Agent Role missing                  | Add `## Agent Role & IO Contract (If Applicable)`  |
| Policy     | Heading     | `## Applies To`                     | `## Policy Scope`                                  |
| Operations | frontmatter | status missing                      | `status: active`                                   |
| Task       | H1 title    | `# Task Tracking...`, etc.          | `# Task: ...`                                      |

## API Contract (If Applicable)

- **API Spec**: N/A

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: AI Agent uses this specification to perform consistency fixes, bash/sed commands, and git commits.
- **Inputs**: docs/99.templates/_.template.md (baseline), docs/01~05/\*\*/_.md (edit target), scripts/ (edit target), .github/workflows/ (edit target)
- **Outputs**: updated Markdown files and git commit history
- **Success Definition**: all validation scripts pass and heading mismatches by type are 0.

## Tools & Tool Contract (If Applicable)

- **Tool List**: bash, grep, sed, find, chmod, git
- **Permission Boundary**: only files under docs/01~05, scripts/, .github/workflows/, and docs/00.agent-governance/rules/ may be modified. Substantive docs/99.templates changes are forbidden.
- **Failure Handling**: when a sed pattern does not match, make no file change; inspect manually and retry.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**: N/A
- **Policy Constraints**: N/A
- **Versioning Rule**: N/A

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: N/A
- **Long-term Memory**: N/A
- **Retrieval Boundary**: N/A

## Guardrails (If Applicable)

- **Input Guardrails**: always confirm the current pattern with grep before running sed commands.
- **Output Guardrails**: after each phase, use validation commands to confirm zero remaining mismatches.
- **Blocked Conditions**: if a docs/99.templates file has a pattern different from the baseline, stop immediately and inspect.
- **Escalation Rule**: do not commit when validation scripts fail.

## Evaluation (If Applicable)

- **Eval Types**: structural validation (grep/find-based)
- **Metrics**: mismatch count by type, which must be 0
- **Datasets / Fixtures**: all docs/01~05/\*_/_.md files
- **How to Run**: see the Verification section below

## Edge Cases & Error Handling

- **Error 1**: sed pattern spans multiple lines; perform only single-line replacements, and edit manually when complex.
- **Error 2**: add status to a file with no frontmatter; create a frontmatter block first, then add status.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: sed changes an unexpected pattern.
- **Fallback**: review `git diff`, then roll back with `git checkout -- <file>`.
- **Human Escalation**: report to a human when pattern mismatches occur in 10 or more files.

## Verification

```bash
BASE=/home/hy/project-infra/hy-home.docker
cd "$BASE"

# ADR title format
grep "^# " docs/02.architecture/decisions/*.md | grep -v "ADR-[0-9]\{4\}:"

# ARD (ARD) suffix
grep "^# " docs/02.architecture/requirements/*.md | grep -v "(ARD)"

# Spec Agent Role section
grep -rL "## Agent Role" docs/03.specs/*/spec.md

# Policies Policy Scope heading
grep -rl "^## Applies To" docs/05.operations/policies/

# Operations status frontmatter
find docs/05.operations -name "*.md" ! -name "README.md" | xargs grep -rL "^status:" | wc -l

# scripts executable permission
ls -la scripts/lib/hardening-lib.sh | grep "^-rwxr-xr-x"

# repo contracts
bash scripts/validation/check-repo-contracts.sh

# doc traceability
bash scripts/validation/check-doc-traceability.sh
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: `grep "^# " docs/02.architecture/decisions/*.md | grep -v "ADR-[0-9]\{4\}:"` returns an empty result, excluding README; ADR title format is 100% compliant.
- **VAL-SPC-002**: `grep "^# " docs/02.architecture/requirements/*.md | grep -v "(ARD)"` returns an empty result, excluding README; ARD title format is 100% compliant.
- **VAL-SPC-003**: `grep -rL "## Agent Role" docs/03.specs/*/spec.md` returns an empty result; all specs have the Agent Role section.
- **VAL-SPC-004**: `grep -rl "^## Applies To" docs/05.operations/policies/` returns an empty result; Policy Scope headings are 100% unified.
- **VAL-SPC-005**: operations docs have 0 missing status frontmatter fields.
- **VAL-SPC-006**: `scripts/lib/hardening-lib.sh` has executable permission 755.
- **VAL-SPC-007**: `bash scripts/validation/check-repo-contracts.sh` passes.
- **VAL-SPC-008**: `bash scripts/validation/check-doc-traceability.sh` passes.

## Related Documents

- **Upstream Audit Spec**: [workspace-audit-2026-05 spec](../../03.specs/workspace-audit-2026-05/spec.md)
- **Plan**: [2026-05-28 workspace doc consistency plan](../../04.execution/plans/2026-05-28-workspace-doc-consistency.md)
- **Tasks**: [2026-05-28 workspace doc consistency tasks](../../04.execution/tasks/2026-05-28-workspace-doc-consistency.md)
- **Templates**: [docs/99.templates/](../../99.templates/)
- **Governance Rules**: [docs/00.agent-governance/rules/](../../00.agent-governance/rules/)
