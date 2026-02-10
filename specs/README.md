# Specifications (Spec-Driven Development)

## 📂 Folder Scope

This directory is the **Active Workspace** for technical implementation. It is distinct from the **Knowledge Base** (`docs/`).

| Directory | Purpose | Content |
| :--- | :--- | :--- |
| **`specs/`** | **Building** | `plan.md`, `spec.md`, temporary assets for active implementation. |
| **`docs/`** | **Reference** | Standards, Manuals, PRDs, ADRs, ARDs. |

### Governance

- **Source of Truth**: During active development, `specs/<feature>/spec.md` is the source of truth.
- **Migration**: Once a feature is stable, key architectural patterns should be documented in `docs/ard/`, but the spec remains as a record of the implementation plan.

## The Flow

1. **Create a Plan**: Create a subfolder for your feature (e.g., `specs/auth-system/`).
2. **Draft the Plan**: Create a `plan.md` file describing your requirements.
3. **Bootstrap**: Run the setup script to generate a workspace tailored to that
   plan.

```bash
# Example
# Windows
./scripts/setup-workspace.ps1 -PlanPath specs/auth-system/plan.md

# Mac/Linux
./scripts/setup-workspace.sh specs/auth-system/plan.md
```

Optional scaffolding:

```bash
./scripts/new-plan.sh "Auth System" auth-system your-name node
```

## Structure

- **`plan.md`**: The high-level implementation plan (Goals, user stories).
- **`spec.md`**: Technical specification (Schema, APIs), must reference the PRD.
- **PRD (Product Requirements)**: Stored in `docs/prd/<feature>-prd.md` (Vision,
  Metrics, Personas, Use Cases).

Use `templates/spec-template.md` and `templates/prd-template.md` as your
baselines.

Specs should complete the architecture/stack checklist in
`templates/spec-template.md` Section 0 and link ADRs (`docs/adr/`) when a
decision is significant.

## Quick Start

- Windows: `./scripts/new-prd.ps1 -Feature "my-feature" -WithSpec`
- Unix: `WITH_SPEC=1 ./scripts/new-prd.sh "my-feature"`
