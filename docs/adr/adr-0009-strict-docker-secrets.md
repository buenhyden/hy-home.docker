# Architecture Decision Record (ADR)

## Title: Strict Docker Secrets Adoption

- **Status:** Accepted
- **Date:** 2026-02-27
- **Authors:** Security Architect
- **Deciders:** Security & DevOps Team

## 1. Context and Problem Statement

Sensitive information (passwords, API tokens) is currently partially scattered across `.env` files and hardcoded values. We need a uniform, high-security method for handling secrets that ensures zero environment variable leakage in `docker inspect` and terminal logs.

## 2. Decision Drivers

- **Security**: Zero plaintext in runtime metadata.
- **Compliance**: Adherence to the project's "Secrets-First" policy.
- **Standardization**: Uniform mount points for all tiers.

## 3. Decision Outcome

**Chosen option: "Mandatory Secret Mounting"**, because all sensitive data MUST be stored in `secrets/**/*.txt` and mounted as files. We will also implement a validation script to enforce this.

### 3.1 Core Engineering Pillars Alignment

- **Security**: Enforces secrets as files (Docker secrets) and avoids plaintext in compose env blocks.
- **Observability**: Reduces risk of secret leakage into logs/metrics (no env-dump patterns).
- **Compliance**: Establishes a strict, auditable standard for local environments handling sensitive configs.
- **Performance**: No measurable runtime cost; improves human performance by removing ambiguity.
- **Documentation**: Makes secret sources and mount paths deterministic across all services.
- **Localization**: Not applicable (secret handling policy).

### 3.2 Positive Consequences

- Enhanced security posture; zero plaintext in terminal history.
- Reduced risk of accidental log exposure.

### 3.3 Negative Consequences

- Increased complexity in local setup (manual file creation).

## 4. Alternatives Considered (Pros and Cons)

### Environment Variable Injection (Encrypted)

Using tools like SOPS to encrypt .env files.

- **Good**, because it integrates well with Git.
- **Bad**, because it still exposes plaintext to the process environment at runtime.

## 5. Confidence Level & Technical Requirements

- **Confidence Rating**: High
- **Notes**: Crucial for production-readiness.
- **Technical Requirements Addressed**: REQ-PRD-BASE-FUN-02, REQ-PRD-BASE-MET-02, REQ-PRD-SYS-MET-01

## 6. Related Documents (Traceability)

- **Feature PRD**: [Infrastructure Baseline PRD](../prd/infra-baseline-prd.md), [System Optimization PRD](../prd/system-optimization-prd.md)
- **Feature Spec**: [Infrastructure Baseline Spec](../../specs/infra/baseline/spec.md)
- **Related ADRs**: [ADR-0002: Secrets-First Management Policy](./adr-0002-secrets-first-management.md)
