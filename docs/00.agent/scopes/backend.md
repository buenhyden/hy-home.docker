---
title: 'Backend Engineering Scope'
layer: backend
---

# Backend Engineering Scope

Standardized patterns for Node.js, Python, and Go services.

## 1. Context & Objective
- **Goal**: Delivery of performant, secure, and observable APIs.

## 2. Requirements & Constraints
- **Runtime**: Node.js 22+ (LTS).
- **ORM**: Prisma for TypeScript, SQLAlchemy for Python.

## 3. Implementation Flow
1. Generate Prisma schema/models.
2. Implement Business Logic (Services).
3. Expose via Controller layer with Zod validation.

## 4. Operational Procedures
- Logs must follow the standardized JSON format.

## 5. Maintenance & Safety
- Unit test coverage MUST be >80% for domain logic.

