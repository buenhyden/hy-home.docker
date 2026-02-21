# Architecture Decision Records (ADR)

This directory contains Architecture Decision Records for the project. ADRs document significant architectural decisions along with their context and consequences.

## What is an ADR?

An Architecture Decision Record (ADR) captures a significant architectural decision, including:

- **Context**: The issue motivating the decision
- **Decision**: The change being proposed or made
- **Consequences**: What becomes easier or more difficult as a result

ADRs provide a historical record of "why" the system is built the way it is, making it easier for future maintainers (both human and AI) to understand the rationale behind architectural choices. All ADRs are strictly governed by the Architecture Design Standards (`.agent/rules/0130-architecture-standard.md`) and must be verified by the Reviewer Agent.

## When to Create an ADR

Create an ADR when making decisions that:

- Affect the structure or characteristics of the system
- Impact multiple components or services
- Involve trade-offs between alternatives
- Would benefit from future reference

### Examples of ADR-Worthy Decisions

- Choice of database technology
- Selection of API architecture style (REST vs GraphQL)
- Adoption of a specific framework
- Security authentication approach
- Deployment strategy

## How to Create an ADR

1. **Determine Domain/Feature**: ADRs MUST be placed inside a specific business domain folder (e.g., `docs/adr/auth/`, `docs/adr/payments/`). Do NOT place them directly in the root of `docs/adr/` unless they are truly global.
2. **Name Convention**: `NNNN-title-with-dashes.md` (e.g., `0001-database-selection.md`)
3. **Fill All Sections**: Context, Decision, Consequences, Alternatives
4. **Set Status**: Proposed → Accepted (or Rejected)

```bash
# Example workflow
mkdir -p docs/adr/core-infra
cp templates/architecture/adr-template.md docs/adr/core-infra/0001-use-postgresql.md
# Edit the file with your decision details
```

## ADR Template

All ADRs MUST use `templates/architecture/adr-template.md`. The template includes:

| Section | Purpose |
| --- | --- |
| **Title** | Short noun phrase describing the decision |
| **Status** | Proposed, Accepted, Rejected, Deprecated, Superseded |
| **Context** | Problem statement and background |
| **Decision** | The change being proposed/made |
| **Consequences** | Positive and negative impacts |
| **Alternatives** | Options considered and why not chosen |

## Naming Convention

```text
docs/adr/
├── core-infra/
│   ├── 0001-use-postgresql.md
│   └── 0002-api-gateway-pattern.md
├── identity/
│   └── 0003-microservices-communication.md
└── ...
```

- Use 4-digit sequential numbers
- Use lowercase with hyphens
- Keep titles short and descriptive

## Status Lifecycle

```text
[Proposed] → [Accepted] → (may become [Deprecated] or [Superseded])
     ↓
[Rejected]
```

- **Proposed**: Under discussion
- **Accepted**: Approved and active
- **Rejected**: Not approved
- **Deprecated**: No longer recommended
- **Superseded**: Replaced by a newer ADR

## AI Agent Guidelines

When working with ADRs:

1. **Read before proposing**: Check existing ADRs in corresponding domain folders for related decisions
2. **Use template**: Always use `templates/architecture/adr-template.md`
3. **Document alternatives**: AI agents must consider and document alternatives
4. **Reference in specs**: Decisions in ADRs should be referenced in `specs/`
5. **Governance Compliance**: The Planner and Reviewer Agents must evaluate all proposed decisions against `.agent/rules/1901-architecture-rules.md` to prevent anti-patterns.

## Index of ADRs

| Number | Title | Status | Date |
| --- | --- | --- | --- |
| - | *No ADRs yet* | - | - |

> Add entries to this index as ADRs are created.
