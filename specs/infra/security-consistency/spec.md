---
title: 'Infra Security & Doc Consistency Implementation Spec'
status: 'Draft'
version: '1.0'
owner: 'Platform/DevOps'
prd_reference: '../../docs/prd/infra-security-consistency-prd.md'
api_reference: 'N/A'
arch_reference: '../../ARCHITECTURE.md'
tags: ['spec', 'implementation', 'infra', 'security', 'documentation']
---

# Implementation Specification (Spec)

> **Status**: Draft
> **Related PRD**: `../../docs/prd/infra-security-consistency-prd.md`
> **Related API Spec**: N/A
> **Related Architecture**: `../../ARCHITECTURE.md`

_Target Directory: `specs/infra-security-consistency/spec.md`_
_Note: This document is the absolute Source of Truth for Coder Agents. NO CODE can be generated without it._

---

## 0. Pre-Implementation Checklist (Governance)

> **Mandatory**: Coder agents MUST verify these checklists before generating code.

### 0.1 Architecture / Tech Stack

| Item               | Check Question                                        | Required | Alignment Notes | Where to document |
| ------------------ | ----------------------------------------------------- | -------- | --------------- | ----------------- |
| Architecture Style | Is the style Monolith/Modular Monolith/Microservices? | Must     | Infra Compose stack, modular services | Section 1 |
| Service Boundaries | Are module boundaries documented (diagram/text)?      | Must     | `infra/<domain>` and docs/context | Section 1 |
| Domain Model       | Are core domain entities and relationships defined?   | Must     | N/A for infra config changes | Section 3 |
| Backend Stack      | Are language/framework/libs (web, ORM, auth) decided? | Must     | Docker Compose / service images | Section 1 |
| Frontend Stack     | Are framework/state/build tools decided?              | Must     | N/A | Section 1 |

### 0.2 Quality / Testing / Security

| Item            | Check Question                                 | Required | Alignment Notes | Where to document |
| --------------- | ---------------------------------------------- | -------- | --------------- | ----------------- |
| Test Strategy   | Levels (Unit/Integration/E2E/Load) defined?    | Must     | Compose config + yamllint + link check | Section 7 |
| Test Tooling    | Agreed framework/runner and mock strategy?     | Must     | `docker compose`, `yamllint` | Section 7 |
| Coverage Policy | Are goals defined as numbers (e.g., 100%)?      | Must     | 100% compose coverage | Section 7 |
| AuthN/AuthZ     | Is auth approach designed (token/OAuth/RBAC)?  | Must     | N/A | Section 4 |
| Data Protection | Encryption/access policies for sensitive data? | Must     | Secrets remain in `secrets/` | Section 9 |
| Performance     | Are Core Web Vitals/Latency metrics targeted?  | Must     | N/A | Section 8 |
| Accessibility   | Is WCAG compliance integrated (contrast/ARIA)? | Must     | N/A | Section 8 |

### 0.3 Operations / Deployment / Monitoring

| Item         | Check Question                                           | Required | Alignment Notes | Where to document |
| ------------ | -------------------------------------------------------- | -------- | --------------- | ----------------- |
| Environments | Are tiers (dev/staging/prod) clarified for this feature? | Must     | `OPERATIONS.md` | OPERATIONS.md |
| Logging      | Required structured logs defined (fields, IDs)?          | Must     | No change | Section 9 |
| Monitoring   | Metrics and dashboards defined (RED/USE)?                | Must     | No change | Section 9 |
| Alerts       | Are alert thresholds and routing defined?                | Must     | No change | Section 9 |
| Backups      | Are backup policies defined for added data?              | Must     | No new data | Section 9 |

---

## 1. Technical Overview & Architecture Style

This change applies baseline container security to all infra Docker Compose services and aligns documentation indexes/links for operators. The architecture is a modular infra stack grouped by domain under `infra/<domain>`.

- **Component Boundary**: Infra compose files and documentation only.
- **Key Dependencies**: Docker Compose, yamllint, existing docs/runbooks structure.
- **Tech Stack**: Docker Compose YAML, existing service images.

## 2. Coded Requirements (Traceability)

| ID                | Requirement Description | Priority | Parent PRD REQ |
| ----------------- | ----------------------- | -------- | -------------- |
| **REQ-SPC-001** | Add `security_opt` with `no-new-privileges:true` to all infra services | Critical | REQ-PRD-FUN-01 |
| **REQ-SPC-002** | Add `cap_drop: [ALL]` to all infra services | Critical | REQ-PRD-FUN-01 |
| **REQ-SPC-003** | Document exceptions where `cap_add`/root/writeable FS required | High | REQ-PRD-FUN-02 |
| **REQ-SPC-004** | Align doc indexes and links | High | REQ-PRD-FUN-03 |
| **REQ-SPC-005** | Keep templates text-only edits | High | REQ-PRD-FUN-04 |

## 3. Data Modeling & Storage Strategy

No schema or data model changes. This is configuration and documentation only.

## 4. Interfaces & Data Structures

No public interfaces or API payloads are modified.

### 4.1. Core Interfaces

N/A

### 4.2. AuthN / AuthZ (Required if protected data/actions)

N/A

## 5. Component Breakdown

- **`infra/**/docker-compose*.yml|yaml`**: Add baseline `security_opt` and `cap_drop`, document exceptions inline.
- **`docker-compose.yml`**: No functional change; ensure aligns with security guidance in docs.
- **`docs/**`, `operations/**`, `runbooks/**`**: Fix inconsistent terms and links.
- **`templates/**`**: Text-only cleanup, no structural change.

## 6. Edge Cases & Error Handling

- **Service needs root**: If root is required, document exception and avoid `user` changes.
- **Service needs `cap_add`**: Keep `cap_add` and note `cap_drop` exception or limited drops.
- **Read-only FS**: Only set `read_only: true` when service already supports it; add `tmpfs` for required writable paths.

**Known Exceptions (Initial):**
- `infra/04-data/seaweedfs/docker-compose.yml` → `seaweedfs-mount` uses `privileged` + `SYS_ADMIN`; `cap_drop` intentionally omitted.
- `infra/04-data/opensearch/docker-compose.cluster.yml` → `opensearch-node*` require `IPC_LOCK` for `bootstrap.memory_lock=true` (drop all, add IPC_LOCK).

## 7. Verification Plan (Testing & QA)

- **[VAL-SPC-001] Compose**: `docker compose -f <file> config` for all touched compose files.
- **[VAL-SPC-002] Lint**: `yamllint <touched yaml>` using `.yamllint` rules.
- **[VAL-SPC-003] Docs**: Scripted check for broken relative links.
- **[VAL-SPC-004] Coverage**: 100% of compose files in scope are reviewed for baseline security.

## 8. Non-Functional Requirements (NFR) & Scalability

No NFR changes. This work reduces operational risk by standardizing baseline security options.

## 9. Operations & Observability

- **Deployment Strategy**: No deployment changes.
- **Monitoring & Alerts**: No changes.
- **Logging**: No changes.
- **Data Protection**: No changes; secrets remain in `secrets/`.
- **Sensitive Data Handling**: Avoid introducing plaintext secrets into compose files.
