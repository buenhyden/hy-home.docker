# Architecture Requirements Documents (ARD)

This directory contains Architecture Requirements Documents that define the technical requirements and constraints for system architecture.

## What is an ARD?

An Architecture Requirements Document (ARD) captures the "how" of system architecture - the technical requirements, constraints, and non-functional requirements that shape the system design. Unlike ADRs which capture decisions, ARDs capture requirements.

### ARD vs ADR

| Document | Focus | Question Answered |
| --- | --- | --- |
| **ADR** | Decisions | "Why did we choose X?" |
| **ARD** | Requirements | "What must the system do?" |

## When to Create an ARD

Create an ARD when:

- Starting a new project or major feature
- Defining technical constraints and NFRs
- Documenting system boundaries and scope
- Establishing performance/security requirements

## How to Create an ARD

1. **Determine Domain/Feature**: ARDs MUST be placed inside a specific business domain folder (e.g., `docs/ard/auth/`, `docs/ard/payments/`).
2. **Use the Template**: Copy `templates/architecture/ard-template.md` to this directory
3. **Name Convention**: `[system]-requirements.md` (e.g., `payment-service-requirements.md`)
4. **Fill All Sections**: Business goals, scope, functional/non-functional requirements, constraints

```bash
# Example workflow
mkdir -p docs/ard/users
cp templates/architecture/ard-template.md docs/ard/users/user-service-requirements.md
# Edit the file with your requirements
```

## ARD Template

All ARDs MUST use `templates/architecture/ard-template.md`. The template includes:

| Section | Purpose |
| --- | --- |
| **Introduction** | High-level overview |
| **Business Goals** | Top-level objectives |
| **Scope** | System boundaries |
| **Functional Requirements** | Core technical capabilities |
| **Non-Functional Requirements** | Performance, scalability, reliability, security |
| **Constraints** | External limitations |

## Key Sections

### Non-Functional Requirements (NFRs)

NFRs are critical for ARDs. Document:

- **Performance**: Latency, throughput, response times
- **Scalability**: Load projections, scaling strategy
- **Reliability**: Uptime SLA, RTO/RPO
- **Security**: Encryption, compliance, authentication
- **Observability**: Logging, metrics, tracing

### Constraints

Document factors that limit architectural choices:

- Budget limitations
- Technology constraints
- Team expertise
- Regulatory compliance
- Legacy system integration

## Relationship to Other Documents

```text
[Business Need]
      ↓
docs/prd/ (What - Product Requirements)
      ↓
docs/ard/ (How - Architecture Requirements, validated via 6 Core Engineering Pillars)
      ↓
docs/adr/ (Why - Architecture Decisions)
      ↓
specs/ (Implementation Specifications)
```

## AI Agent Guidelines

When working with ARDs:

1. **Read before designing**: Check existing ARDs in the relevant domain folders for requirements
2. **Use template**: Always use `templates/architecture/ard-template.md`
3. **Be specific**: Quantify NFRs (e.g., "99.9% uptime" not "high availability")
4. **Link to ADRs**: Reference relevant ADRs in constraints section
5. **Pillar Validation**: Validate that ARDs align with `.agent/rules/1910-architecture-documentation.md` and account for the 6 Core Engineering Pillars (Security, Observability, Performance, Compliance, Documentation, Localization).

## Index of ARDs

| Document | System | Last Updated |
| --- | --- | --- |
| - | *No ARDs yet* | - |

> Add entries to this index as ARDs are created.
