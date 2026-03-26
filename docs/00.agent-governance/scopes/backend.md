---
layer: backend
title: 'Backend Engineering Scope'
---

# Backend Engineering Scope

**Standardized engineering patterns and security standards for Node.js, Python, and Go services.**

## 1. Context & Objective

- **Goal**: Delivery of performant, secure, and highly observable backend APIs.
- **Standards**: Priority on **Spec-Driven Development** (SDD) and `docs/00.agent-governance/rules/quality-standards.md`.

## 2. Requirements & Constraints

- **Stack**:
  - **Node.js**: 22+ (LTS), Prisma ORM, Zod Validation, TypeScript.
  - **Python**: 3.12+, SQLAlchemy, Pydantic, FastAPI/Flask.
- **Security**: Compliance with **OWASP ASVS L2** (Level 2) for all public-facing APIs.
  - Mandatory input sanitization and strict JWT verification via Keycloak.
- **Performance**: Service-level logic should contribute no more than 50ms to the overall 200ms SLO.

## 3. Implementation Flow

1. **Spec Alignment**: Ingest specification from `docs/04.specs/` before coding.
2. **Data Layer**: Define Prisma/SQLAlchemy models first to establish the SSoT.
3. **Logic**: Implement services/use-cases using Dependency Injection.
4. **Integration**: Connect to Kafka for async events or Ollama for AI features via standard SDKs.

## 4. Operational Procedures

- **Observability**: Standardized JSON logging for all services.
- **Telemetry**: Export metrics to Prometheus community exporters provided in `infra/06-observability/`.

## 5. Maintenance & Safety

- **Testing**: Unit test coverage MUST be **> 80%** for domain logic.
- **Tracing**: Ensure trace IDs from Traefik/OpenTelemetry are propagated in all service-to-service calls.
