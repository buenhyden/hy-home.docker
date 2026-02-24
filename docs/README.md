# Documentation Hub (`docs/`)

This directory contains long-term, human-readable project documentation used across planning, design, and reference delivery.

## 1. Necessity and Purpose

This directory exists to permanently store the "Why" and "What" of the system. It is absolutely necessary because it acts as the stable knowledge base that survives beyond single feature implementations or operational incidents.

- **Isolate product/design knowledge** from executable logic (`specs/`), operational scripts (`runbooks/`), and AI Automation logic (`.agent/workflows/`).
- Serve as the primary reference point for **Human Developers** and **AI Planner Agents** trying to understand the overarching system constraints.

## 2. Sub-Directories & Required Content

Each sub-directory serves a distinct, non-overlapping purpose. Documents created here MUST use their respective templates from the `templates/` folder.

## 🗺️ Documentation Navigator (Role-Based)

### 🏗️ For Architects

- **Rationale**: [Architecture Decisions (ADR)](adr/README.md) — The "Why" behind the stack.
- **Constraints**: [Architecture Requirements (ARD)](ard/README.md) — NFRs and boundaries.
- **Optimization**: [Architecture Optimization Strategy](guides/arch-optimization-strategy.md).

### 💻 For Developers

- **Lifecycle**: [Feature Delivery Roadmap](guides/README.md) — Pre, During, and Post development guides.
- **Blueprints**: [Technical Context Hub](context/README.md) — Service-specific implementation details.
- **Prerequisites**: [Product Requirements (PRD)](prd/README.md).

### 🛠️ For DevOps & Operators

- **Incident Hub**: [Runbooks Catalog](../runbooks/README.md) — Actionable CLI guides.
- **Central Index**: [OPERATIONS.md](../OPERATIONS.md) — Operational readiness and strategy.
- **Configuration**: [Infrastructure Lifecycle](context/core/infra-lifecycle-ops.md).

---

## Folder Taxonomy

- [**`adr/`**](adr/README.md) — **Architecture Decision Records**.
- [**`ard/`**](ard/README.md) — **Architecture Reference Documents**.
- [**`prd/`**](prd/README.md) — **Product Requirements Documents**.
- [**`context/`**](context/README.md) — **Technical Blueprints & Service Setup**.
- [**`guides/`**](guides/README.md) — **Platform Lifecycle & Workflows**.
- [**`manuals/`**](manuals/README.md) — **Collaboration & Standards**.

## 3. Explicit Boundaries & Anti-Patterns

1. **NO RUNBOOKS ALLOWED**: Do NOT create a `docs/runbook/` folder. All playbooks, incident response guides, and deployment workflows **MUST go in the root `/runbooks/` directory**.
2. **NO SPECS ALLOWED**: Do NOT place implementation specs here. All feature-specific coding specifications and plans belong in `/specs/`.
3. **NO AI WORKFLOWS ALLOWED**: Do NOT place AI agent behavioral guidelines or prompts here. Those belong strictly in `.agent/workflows/`.
4. **TEMPLATE MANDATORY**: Any new ADR, ARD, or PRD created in this folder **MUST** be generated from its respective counterpart in the `templates/` directory.
5. **DOCUMENTATION PILLAR**: All content in this directory is subject to the Document Pillar (`.agent/rules/2100-documentation-pillar.md`) and must adhere to the Diátaxis framework where applicable.
6. **PROJECT-SPECIFIC OVERRIDES**: The `guides/` and `manuals/` folders serve as the official location for project-specific overrides to the generic `.agent/rules/`. AI Agents will prioritize instructions in these local guides during execution.
