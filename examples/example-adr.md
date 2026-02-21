# Example: Architecture Decision Record (ADR)

This is a concrete example of an ADR following the `templates/architecture/adr-template.md` structure.

---

## Architecture Decision Record

## Title: Use PostgreSQL as Primary Database

**Status:** Accepted

**Date:** 2024-01-15

**Deciders:** John Doe (Tech Lead), Jane Smith (Architect), Dev Team

## Context

We need a primary database for our new microservices platform. The database must support ACID transactions, handle relational data, and scale to support millions of users. The team has experience with both SQL and NoSQL databases.

## Decision

We will use PostgreSQL as our primary database for all transactional microservices.

## Consequences

- **Positive:**
  - Strong ACID compliance ensures data integrity
  - Excellent JSON support via JSONB columns allows flexibility
  - Mature ecosystem with proven reliability
  - Team familiarity reduces onboarding time
  - Built-in support for full-text search

- **Negative:**
  - Horizontal scaling is more complex compared to NoSQL solutions
  - May require connection pooling (PgBouncer) for high-traffic scenarios
  - Schema migrations require careful planning

## Core Engineering Pillars Alignment

- **Security (`[REQ-SEC-01]`)**: Excellent role-based access control and encrypted connection support.
- **Observability (`[REQ-OBS-01]`)**: Extensive metrics available via pg_stat_statements; integrates perfectly with Datadog/Prometheus standard stacks.
- **Compliance (`[REQ-CMP-01]`)**: Supported natively by all major cloud providers (AWS RDS, GCP Cloud SQL) ensuring SOC2/HIPAA compliance boundary management.
- **Performance (`[REQ-PERF-01]`)**: Exceeds required TPS for transactional services. JSONB queries provide near NoSQL read performance.

## Alternatives Considered

- **Alternative 1:** MongoDB - Rejected because we need strong ACID guarantees for financial transactions.
- **Alternative 2:** CockroachDB - Rejected due to higher operational complexity and cost at our current scale.
