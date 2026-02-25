---
goal: 'Apply baseline container hardening across all infra compose files and align documentation indexes/terms.'
version: '1.0'
date_created: '2026-02-24'
last_updated: '2026-02-24'
owner: 'Platform/DevOps'
status: 'Planned'
tags: ['implementation', 'planning', 'infra', 'security', 'documentation']
stack: 'python'
---

# Infra Security & Doc Consistency Implementation Plan

_Target Directory: `specs/infra-security-consistency/plan.md`_

## 1. Context & Introduction

This plan implements baseline security hardening for all infra Docker Compose files and performs a consistency pass across documentation and indexes. It is scoped to minimal, non-structural edits aligned with `ARCHITECTURE.md` and documentation standards.

## 2. Goals & In-Scope

- **Goals:**
  - Enforce `no-new-privileges:true` and `cap_drop: [ALL]` (or justified exceptions) across all infra compose services.
  - Normalize doc indexes/links and terminology for internal operators.
- **In-Scope (Scope of this Plan):**
  - All `infra/**/docker-compose*.yml|yaml` and root `docker-compose.yml`.
  - `docs/`, `operations/`, `runbooks/`, `templates/`, `ARCHITECTURE.md`, `OPERATIONS.md`.

## 3. Non-Goals & Out-of-Scope

- **Non-Goals:**
  - Behavior changes to services or adding new services.
- **Out-of-Scope:**
  - Template structure changes, Kubernetes manifests, and non-Compose deployments.

## 4. Requirements & Constraints

- **Requirements:**
  - `[REQ-001]`: Add baseline `security_opt` and `cap_drop` to infra compose services unless exceptions are documented.
  - `[REQ-002]`: Document exceptions (root/cap_add/read_only constraints) inline and in spec.
  - `[REQ-003]`: Fix doc indexes, terms, and internal links with minimal, safe edits.
- **Constraints:**
  - Templates are text-only edits (no header/structure changes).
  - Keep KR/EN language mixed; only normalize inconsistent labels.

## 5. Work Breakdown (Tasks & Traceability)

| Task     | Description | Files Affected | Target REQ | Validation Criteria |
| -------- | ----------- | -------------- | ---------- | ------------------- |
| TASK-001 | Create PRD/Plan/Spec docs | `docs/prd/infra-security-consistency-prd.md`, `specs/infra-security-consistency/*` | [REQ-001] | Files match templates and link correctly |
| TASK-002 | Compose hardening | `infra/**/docker-compose*.yml|yaml` | [REQ-001] | Each service has baseline security or exception |
| TASK-003 | Doc consistency pass | `docs/**`, `operations/**`, `runbooks/**`, `templates/**`, `ARCHITECTURE.md`, `OPERATIONS.md` | [REQ-003] | Links resolve and terminology is consistent |
| TASK-004 | Verification | N/A | [REQ-001] | compose config, yamllint, link checks pass or reported |

## 6. Verification Plan

| ID          | Level       | Description                              | Command / How to Run | Pass Criteria |
| ----------- | ----------- | ---------------------------------------- | -------------------- | ------------- |
| VAL-PLN-001 | Compose     | Render config for touched compose files  | `docker compose -f <file> config` | All succeed |
| VAL-PLN-002 | Lint/Build  | YAML lint on touched YAML files          | `yamllint <files>` | Zero errors |
| VAL-PLN-003 | Docs        | Verify internal links resolve            | Scripted link check | Zero broken links |

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| Some images require root or special capabilities | Med | Document exceptions and minimize changes |
| Read-only FS breaks runtime expectations | Med | Only apply to safe services; add tmpfs as needed |

## 8. Completion Criteria

- [ ] All tasks completed
- [ ] Verification checks passed (or failures documented)
- [ ] Documentation updated

## 9. References

- **PRD**: `docs/prd/infra-security-consistency-prd.md`
- **Spec**: `specs/infra-security-consistency/spec.md`
- **ADRs**: `docs/adr/README.md`
