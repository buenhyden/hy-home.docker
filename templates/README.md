# Standardized Templates

This directory contains the immutable foundations for all documentation and specifications generated in this project.

## Golden Rule for AI Agents

**NO HALLUCINATED FORMATTING.**
When generating an ADR, ARD, PRD, Runbook, or Spec, you MUST read the exact markdown structure of the template in this folder and output your document adhering to its headers and structure.

## Available Templates & Their Destinations

| Template File                                | Destination Directory | Created By          | Purpose                                  |
|----------------------------------------------|-----------------------|---------------------|------------------------------------------|
| `architecture/adr-template.md`               | `docs/adr/`           | Planner Agent       | Documenting architecture decisions (Why) |
| `architecture/ard-template.md`               | `docs/ard/`           | Planner Agent       | Documenting deep technical systems (How) |
| `product/prd-template.md`                    | `docs/prd/`           | Planner Agent       | Defining product requirements (What)     |
| `engineering/spec-template.md`               | `specs/`              | Planner Agent       | Exact instructions for Coder Agents      |
| `engineering/api-spec-template.md`           | `specs/<feature>/api/`| Planner Agent       | Exact instructions for API contracts     |
| `operations/runbook-template.md`             | `runbooks/`           | DevOps / Coder      | Executable operational procedures        |
| `operations/postmortem-template.md`          | `docs/manuals/`       | DevOps / Human      | Incident reporting (SEV-1/2)             |
| `guides/collaboration-guide-template.md`     | `docs/manuals/`       | Human / Planner     | Initial collaboration agreements         |
| `guides/operations-guide-template.md`        | `docs/manuals/`       | DevOps              | Deployment readiness checks              |
| `guides/qa-security-guide-template.md`       | `docs/manuals/`       | QA / Sec Agent      | Testing & Quality standards              |
| `project/readme-template.md`                 | `/`                   | Planner Agent       | Initial Readme generation                |
| `project/plan-template.md`                   | `/`                   | Planner Agent       | Initial Project Planning generation      |

## Adding New Templates

If the project requires a new standardized document type (e.g., specific security audit report), the structure should be defined here as `[name]-template.md` before agents are instructed to produce it.
