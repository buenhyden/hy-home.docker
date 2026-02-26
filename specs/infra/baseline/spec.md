---
title: 'Infrastructure Baseline Implementation Spec'
status: 'Implementation'
version: '1.0'
owner: 'Platform Architect'
prd_reference: '../../../docs/prd/infra-baseline-prd.md'
api_reference: 'N/A'
arch_reference: '../../../docs/ard/infra-baseline-ard.md'
tags: ['spec', 'implementation', 'infra', 'baseline']
---

# Implementation Specification: Infrastructure Baseline

> **Status**: Implementation
> **Related PRD**: [infra-baseline-prd.md](../../../docs/prd/infra-baseline-prd.md)
> **Related ARD**: [infra-baseline-ard.md](../../../docs/ard/infra-baseline-ard.md)

_Target Directory: `specs/infra/baseline/spec.md`_

---

## 0. Pre-Implementation Checklist (Governance)

### 0.1 Architecture / Tech Stack

| Item               | Check Question                                        | Required | Alignment Notes | Where to document |
| ------------------ | ----------------------------------------------------- | -------- | --------------- | ----------------- |
| Architecture Style | Is the style Monolith/Modular Monolith/Microservices? | Must     | Modular Compose | Section 1 |
| Service Boundaries | Are module boundaries documented (diagram/text)?      | Must     | `infra/<domain>` | Section 1 |
| Backend Stack      | Are language/framework/libs decided? | Must     | Docker Compose v2.20+ | Section 1 |

### 0.2 Quality / Testing / Security

| Item            | Check Question                                 | Required | Alignment Notes | Where to document |
| --------------- | ---------------------------------------------- | -------- | --------------- | ----------------- |
| Test Strategy   | Levels (Unit/Integration/E2E/Load) defined?    | Must     | YAML & Readiness checks | Section 7 |
| AuthN/AuthZ     | Is auth approach designed (token/OAuth/RBAC)?  | Must     | Docker Secrets | Section 4 |
| Data Protection | Encryption/access policies for sensitive data? | Must     | Mounted Secrets | Section 9 |

### 0.3 Operations / Deployment / Monitoring

| Item         | Check Question                                           | Required | Alignment Notes | Where to document |
| ------------ | -------------------------------------------------------- | -------- | --------------- | ----------------- |
| Environments | Are tiers (dev/staging/prod) clarified for this feature? | Must     | Local Home-Lab | Section 9 |
| Logging      | Required structured logs defined (fields, IDs)?          | Must     | Alloy discovery | Section 9 |
| Secrets      | Are backup policies defined for added data?              | Must     | File-based backups | Section 9 |

---

## 1. Technical Overview & Architecture Style

This specification governs the core setup and security hardening of the primary infrastructure engine using a modular Docker Compose orchestrator.

- **Component Boundary**: Root `docker-compose.yml` and Tier-1 service configurations.
- **Tech Stack**: Docker Compose v2.20+, YAML 3.8, Docker Secrets.

## 2. Coded Requirements (Traceability)

| ID                | Requirement Description | Priority | Parent PRD REQ |
| ----------------- | ----------------------- | -------- | -------------- |
| **REQ-SPC-001** | Implement `include` pattern for sub-compose imports | Critical | REQ-PRD-FUN-01 |
| **REQ-SPC-002** | Add `no-new-privileges:true` and `cap_drop: [ALL]` | Critical | REQ-PRD-FUN-01 |
| **REQ-SPC-003** | Standardize Bootstrap & Secrets Prerequisites | High | REQ-PRD-FUN-03 |
| **REQ-SPC-004** | Standardize Local TLS paths (secrets/certs/) | High | REQ-PRD-FUN-04 |

## 3. Data Modeling & Storage Strategy

- **Persistence**: Bind-mounts pointing to `${DEFAULT_DATA_DIR}` for performance and host-level control.
- **Secrets Strategy**: 100% usage of Docker Secrets (canonical `/run/secrets/` path).

## 4. Interfaces & Data Structures

- **Registry Interface**: The root `docker-compose.yml` acts as the master registry for all `infra/` modules.
- **Security Context**: Every service definition MUST include a `security_opt: ["no-new-privileges:true"]` block.

## 5. Acceptance Criteria (GWT)

### REQ-SPC-001: Aggregated Config Verification

- **Given** a directory structure with `infra/01-gateway` and `infra/02-auth`.
- **When** executing `docker compose config`.
- **Then** the output contains services from both sub-directories.
- **And** no duplicate network or volume definitions exist.

### REQ-SPC-002: Kernel Hardening Verification

- **Given** any Tier-1 service (e.g., Traefik).
- **When** the container is inspected via `docker inspect`.
- **Then** `HostConfig.SecurityOpt` contains `no-new-privileges:true`.
- **And** `HostConfig.CapDrop` contains `ALL`.

### REQ-SPC-003: Preflight Failure Logic

- **Given** a missing `.env` file or empty `secrets/` directory.
- **When** running the `preflight-compose.sh` script.
- **Then** the script exits with code 1.
- **And** the terminal output explicitly names the missing prerequisite.

## 6. Component Breakdown

- **`docker-compose.yml`**: Entry point using `include` to pull in domain-specific stacks.
- **`infra/01-gateway/traefik.yml`**: Ingress controller with TLS and auth middleware.
- **`infra/04-data/postgres.yml`**: HA database cluster with secrets-based auth.

## 7. Verification Plan (Testing & QA)

- **[VAL-SPC-001] Schema Validation**: All compose files MUST pass `yamllint` with zero errors.
- **[VAL-SPC-002] Security Audit**: Execution of `docker-bench-security` should show 100% compliance for "Container Hardening" section.
- **[VAL-SPC-003] Bootstrap Test**: Executing `make bootstrap` on a fresh lab machine must reach "Healthy" status in < 10 mins.

## 8. Non-Functional Requirements (NFR) & Scalability

- **Security**: 0.0 critical vulnerabilities in base images (distroless preferred).
- **Boot Performance**: `docker compose up -d` must complete initial pulling/starting in < 5 mins on gigabit fiber.

## 9. Operations & Observability

- **Secrets Rotation**: Replace target `.txt` file in `secrets/` and restart the specific service.
- **Observability**: Standardized `observability.logs=true` label on all containers.
