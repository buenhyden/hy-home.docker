# Architecture Decision Record (ADR)

_Target Directory: `docs/adr/adr-0002-secrets-first-management.md`_

## Title: adr-0002: Secrets-First Management

- **Status:** Accepted
- **Date:** 2026-02-26
- **Authors:** Security Engineer
- **Deciders:** DevOps Team

## 1. Context and Problem Statement

Hardcoding seeds, passwords, and API keys in `.env` files or directly in Compose files leads to repository leakage and poor security posture.

## 2. Decision Drivers

- **Security**: Prevents credential exposure in Git.
- **Compliance**: Follows secret management best practices.
- **Portability**: Compatible with Swarm and Kubernetes secret patterns.

## 3. Decision Outcome

**Chosen option: "Mandatory Docker Secrets"**, because it ensures all sensitive credentials are stored in `secrets/**/*.txt` and mounted into containers at runtime as files, rather than environment variables.

### 3.1 Core Engineering Pillars Alignment

- **Security**: Aligns with `[REQ-SEC-01]` by ensuring zero-plaintext leaks.
- **Operations**: Simplifies secret rotation in production-like environments.

### 3.2 Positive Consequences

- Environment variables do not contain sensitive data.
- Standardized mounting point (`/run/secrets/`).

### 3.3 Negative Consequences

- Slightly more complex local setup (file creation required).

## 4. Alternatives Considered

### Environment Variables (.env)

- **Good**: Simple to use.
- **Bad**: Secrets shown in `docker inspect` and prone to accidental logging.

## 5. Confidence Level

- **Confidence Rating**: High
