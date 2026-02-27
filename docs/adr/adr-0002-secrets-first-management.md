# Architecture Decision Record (ADR)

## Title: Secrets-First Management Policy

- **Status:** Accepted
- **Date:** 2026-02-26
- **Authors:** Security Engineer
- **Deciders:** DevOps Team

## 1. Context and Problem Statement

Hardcoding seeds, passwords, and API keys in `.env` files or directly in Compose files leads to repository leakage and poor security posture. Environment variables are often logged or visible in `docker inspect`, creating a major vulnerability.

## 2. Decision Drivers

- **Security**: Prevents credential exposure in Git and runtime inspection.
- **Compliance**: Follows secret management best practices for local development.
- **Portability**: Compatible with Swarm and Kubernetes secret patterns (file-based).

## 3. Decision Outcome

**Chosen option: "Mandatory Docker Secrets"**, because it ensures all sensitive credentials are stored in `secrets/**/*.txt` and mounted into containers at runtime as files, rather than environment variables.

### 3.1 Core Engineering Pillars Alignment

- **Security**: Prevents plaintext secrets from living in compose files or process environments (`docker inspect`, crash dumps, shell history).
- **Observability**: Reduces the likelihood of secret leakage through log scrapes or environment-dump troubleshooting.
- **Compliance**: Establishes a consistent secret handling policy required for audits (one secret = one file, mounted at runtime).
- **Performance**: Secret reads are trivial; no measurable overhead.
- **Documentation**: Standardizes how all docs refer to secrets (`secrets/**/*.txt` + `/run/secrets/*`).
- **Localization**: Not applicable (secret handling policy).

### 3.2 Positive Consequences

- Environment variables do not contain sensitive data.
- Standardized mounting point (`/run/secrets/`).

### 3.3 Negative Consequences

- Slightly more complex local setup; users must create the `secrets/` directory and files.

## 4. Alternatives Considered (Pros and Cons)

### Environment Variables (.env)

The standard Docker Compose approach.

- **Good**, because it is simple to use and universally supported.
- **Bad**, because secrets are shown in `docker inspect`, visible to all users on the host, and prone to accidental logging.

## 5. Confidence Level & Technical Requirements

- **Confidence Rating**: High
- **Notes**: Industry standard for secure container orchestration.
- **Technical Requirements Addressed**: REQ-PRD-BASE-FUN-02, REQ-PRD-BASE-MET-02

## 6. Related Documents (Traceability)

- **Feature PRD**: [Infrastructure Baseline PRD](../prd/infra-baseline-prd.md)
- **Feature Spec**: [Infrastructure Baseline Spec](../../specs/infra/baseline/spec.md)
- **Related ADRs**: [ADR-0009: Strict Docker Secrets Adoption](./adr-0009-strict-docker-secrets.md)
