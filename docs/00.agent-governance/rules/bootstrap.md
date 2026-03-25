---
layer: agentic
---

# Agent Bootstrap Governance

> [!NOTE]
> **hy-home.docker**: A spec-driven repository foundation for documentation governance and AI-assisted delivery workflows.

This document defines the universal entry point for all AI Agents interacting with this repository. It enforces **Spec-Driven Development (SDD)** and JIT (Just-In-Time) metadata routing for maximum context efficiency.

## 1. Core Principles (March 2026)

- **Spec-Anchored**: All implementation work MUST be grounded in approved `PRD` and `Spec` artifacts in `docs/01.prd/` and `docs/04.specs/`.
- **Flat Taxonomy**: SSoT (Single Source of Truth) files live in numbered folders (e.g., `docs/01.prd/`).
- **Metadata Routing**: Agents discover context by searching for `layer: <name>` inside `docs/` to identify ownership.
- **Lazy Loading**: Load only shared governance initially; dynamically load layer-specific detail JIT via the `scopes/` directory.

## 2. Mandatory Taxonomy (SSoT Paths)

| Stage | Path | Purpose | Template |
| :--- | :--- | :--- | :--- |
| **00** | `docs/00.agent-governance/` | AI Agent Governance & Scopes | - |
| **01** | `docs/01.prd/` | Product Requirements & Intent | `prd.template.md` |
| **02** | `docs/02.ard/` | Architecture Reference Documents | `ard.template.md` |
| **03** | `docs/03.adr/` | Architectural Decision Records | `adr.template.md` |
| **04** | `docs/04.specs/` | Technical Specifications (SSoT) | `spec.template.md` |
| **05** | `docs/05.plans/` | Implementation & Validation Plans | `plan.template.md` |
| **06** | `docs/06.tasks/` | Granular Task & Progress Tracking | `task.template.md` |
| **07** | `docs/07.guides/` | Operational & Developer Guides | `guide.template.md` |
| **08** | `docs/08.operations/` | Monitoring & Environment State | `operation.template.md` |
| **09** | `docs/09.runbooks/` | Incident Response Procedures | `runbook.template.md` |
| **10** | `docs/10.incidents/` | Live Incident Tracking | `incident.template.md` |
| **11** | `docs/11.postmortems/` | Retrospectives & Lessons Learned | `postmortem.template.md` |

## 3. Layer Identification Protocol

Before performing any task, the Agent MUST:

1. Identify the target **Layer** (`common, architecture, backend, frontend, infra, mobile, product, qa, security, entry, meta, ops, agentic`).
2. Locate the SSoT for that layer using `grep -r "layer: <name>" docs/`.
3. Load the corresponding scope from `docs/00.agent-governance/scopes/<layer>.md`.
4. Adopt the required Persona (from `persona-matrix.md`) and announce:
    > "As your **[Persona Name]**, I am targeting the **[Layer]** layer and adopting the **[Standard ID]** governance."

## 4. Documentation Standards

All documentation must adhere to the following rules:

- **Frontmatter**: Every file MUST start with the `layer` metadata.
- **Language**: All governance and agentic documentation in `docs/00.agent-governance/` MUST be in English.
- **Taxonomy**: Follow the "Golden 5" pattern for headers:
    1. `## 1. Context & Objective`
    2. `## 2. Requirements & Constraints`
    3. `## 3. Implementation Flow`
    4. `## 4. Operational Procedures`
    5. `## 5. Maintenance & Safety`

## 5. Infrastructure & Architectural Governance

### Verification Checklist

Every architectural or cross-cutting structural change must satisfy:

1. **Validation**: Must pass `bash scripts/validate-docker-compose.sh`.
2. **Secrets**: Use Docker Secrets, never `.env` for plain-text credentials.
3. **Connectivity**: All inter-service traffic must use `infra_net`.
4. **Permissions**: Enforce `no-new-privileges:true`.
5. **Traceability**: Reciprocal links between ADR, Spec, and Runbook.

### Infrastructure Lifecycle

1. **Discover**: Find existing specs, ADRs, runbooks in `01~09`.
2. **Specify**: Create `04.specs/` if missing.
3. **Plan**: Verify or create `05.plans/`.
4. **Implement**: Apply smallest correct change.
5. **Verify**: Run validation scripts.
6. **Document**: Update all related documentation.
