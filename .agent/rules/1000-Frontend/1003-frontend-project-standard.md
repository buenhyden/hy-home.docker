---
trigger: always_on
glob: ["**/*.{tsx,jsx,vue,svelte,html}", "src/**"]
description: "Frontend Project Structure Standards: Enforces Feature-First Architecture, vertical slicing, and clean horizontal shared boundaries."
---

# Frontend Project Structure Standards

- **Role**: Lead Frontend Architect
- **Purpose**: Define standards for organizing the frontend codebase to maximize discoverability, testability, and scalability through a Feature-First architecture.
- **Activates When**: initializing new frontend projects, creating new features, or refactoring existing directory structures.

**Trigger**: always_on — Apply during the organization and maintenance of all frontend directory structures.

## 1. Standards

### Principles

- **[REQ-FSTR-00] Repository Workspace Separation**
  - Frontend-related modules MUST be isolated within the `web/` or `app/` root directory depending on the target platform, explicitly separating it from backend implementations (`server/`).
- **[REQ-FSTR-01] Feature-First Vertical Slicing**
  - All application code MUST be organized by business domain/feature (e.g., `features/auth/`) rather than technical type (e.g., `components/`).
- **[REQ-FSTR-02] Public API Encapsulation**
  - Each feature folder MUST export its public interface via an `index.ts` file. Deep imports into feature sub-folders from external modules are PROHIBITED.
- **[REQ-FSTR-03] Absolute Import Primacy**
  - All internal imports MUST use absolute paths (e.g., `@/features/auth/...`) to avoid fragile and unreadable relative paths (e.g., `../../../../`).

### Directory Hierarchy

| Folder | Requirement ID | Responsibility |
| --- | --- | --- |
| `src/features` | [REQ-FSTR-04] | Business-domain vertical slices |
| `src/components/ui` | [REQ-FSTR-05] | Atomic, dumb UI primitives |
| `src/hooks/shared` | [REQ-FSTR-06] | Multi-feature reusable hooks |
| `src/lib` | [REQ-FSTR-07] | Third-party configurations & clients |

### Must

- **[REQ-FSTR-08] Standard Feature Sub-structure**
  - A feature folder MUST contain: `components/`, `hooks/`, `api/`, `types/`, and `index.ts`.
- **[REQ-FSTR-09] Strict Co-location**
  - Styles, tests, and assets specific to a single component MUST be co-located in the same directory as the component file.
- **[REQ-FSTR-10] Shared Logic Centralization**
  - Logic utilized by > 2 features MUST be elevated to the `shared/` or `core/` directory to prevent circular feature dependencies.

### Must Not

- **[BAN-FSTR-01] God-Component Accumulation**
  - DO NOT create monolithic components that serve multiple distinct business features; decompose into domain-specific features.
- **[BAN-FSTR-02] Deep Feature Imports**
  - Do NOT import from `src/features/feature-a/components/SubComponent.tsx`; always import from `@/features/feature-a`.

### Failure Handling

- **Stop Condition**: Stop feature creation if it is identified as having direct, circular dependencies on another feature's internal folders.

## 2. Procedures

- **[PROC-FSTR-01] Feature Onboarding**
  - IF creating a new vertical slice THEN MUST first define the public export interface in the `index.ts` to enforce boundaries.
- **[PROC-FSTR-02] Refactoring Audit**
  - Conduct a monthly audit of horizontal dependencies to ensure the `shared/` folder remains clean and is not becoming a "dumping ground".

## 3. Examples

### Clean Feature structure (Good)

```text
src/features/auth/
  ├── components/ (LoginForm.tsx)
  ├── hooks/ (useAuth.ts)
  ├── api/ (authClient.ts)
  └── index.ts (Public API)
```

## 4. Validation Criteria

- **[VAL-FSTR-01] Dependency Pass**
  - [ ] Automated check confirms zero cross-feature deep imports (bypassing `index.ts`).
- **[VAL-FSTR-02] Co-location Success**
  - [ ] audit confirms that 100% of unit tests reside next to their target components.
- **[VAL-FSTR-03] Path Correctness**
  - [ ] Zero relative imports (`../`) are present in the application-level logic.
