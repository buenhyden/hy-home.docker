# System Architecture

This document defines the high-level architecture of projects created from this template. It serves as a blueprint that should be customized for each new project.

## 1. System Context & Necessity

This template provides a standardized foundation for building software projects.

**Necessity**: This specific `ARCHITECTURE.md` file is absolutely essential as the global, unchanging architectural law of the repository. While `docs/adr/` handles specific component decisions over time and `docs/ard/` holds deep architectural diagrams, this root file holds the *highest-level constraints and checklists* that must NEVER be violated by any human or AI agent without a formal override.

**What Must Be Written Here**:

- The overarching architecture style (Microservices vs Monolith).
- The list of acceptable core tech stacks.
- The Architectural Checklist that every new feature MUST pass before entering the `specs/` phase.

### Core Architecture Pillars

- **Spec-Driven Development**: `specs/` uniquely drives all implementation.
- **AI-Assisted Development**: Multi Sub-Agent AI system phases (`AGENTS.md`).
- **Template-Based Documentation**: Consistent output enforced via `templates/`.
- **Strict Boundary Segregation**: Clear division of Knowledge (`docs/`), Implementation (`specs/`, `web/`, `app/`, `server/`), and Operations (`runbooks/`).

## 2. Core Constraints & Decisions

### Core Constraints & Decisions

| Decision                | Rationale                                                                           |
|-------------------------|-------------------------------------------------------------------------------------|
| **Spec-Driven Code**    | Eliminates AI hallucination by giving Coder Agents a hard, human-approved target.   |
| **Templates Mandatory** | Ensures parsing consistency for future AI tasks (PRDs, Specs, Runbooks).            |
| **Dedicated Runbooks**  | Prevents ops scripts from getting lost in `docs/` hierarchies.                      |

> See `docs/adr/` for detailed Architecture Decision Records that shaped this specific system logic.

## 3. Architecture & Tech Stack Checklist

When starting a project or writing an Architecture Reference Document (ARD), the following checklist MUST be addressed and agreed upon by the Human and Planner Agent:

| Category | Check Question | Priority | Notes / Decisions |
| --- | --- | --- | --- |
| **Architecture Style** | Is the architectural style decided (e.g., Monolithic, Modular Monolith, Microservices)? | **Mandatory** | |
| **Service Boundaries** | Are the boundaries and responsibilities of core services/modules expressed in diagrams/docs? | **Mandatory** | |
| **Domain Model** | Are core domain entities (e.g., User, Document) and relations defined (ER/UML)? | **Mandatory** | |
| **Tech Stack (Backend)** | Have the language, framework, and key libraries (e.g., web framework, ORM) been decided? | **Mandatory** | |
| **Tech Stack (Frontend)** | Have the framework (React/Vue/Next), state management, and build tools been decided? | **Mandatory** | |
| **Database** | Have the primary DB engine (e.g., MySQL, PostgreSQL, MongoDB) and schema strategy been decided? | **Mandatory** | |
| **Messaging / Async** | Is a message broker (e.g., Kafka, RabbitMQ) or async processing method defined? | *Optional* | |
| **Infrastructure** | Is the deployment target (Cloud/On-Prem, Kubernetes, Serverless) decided? | **Mandatory** | |
| **Non-Functional Req** | Are NFRs (Availability, Latency, Throughput) defined with quantitative metrics? | **Mandatory** | |
| **Scalability Strategy** | Are Scale-up/out, partitioning, or caching strategies drafted? | *Optional* | |
| **Arch. Principles** | Is there a documented list of architectural principles, including "what NOT to do"? | *Optional* | |
| **ADR Management** | Is there a process established to leave ADRs for key technical decisions? | *Optional* | Yes, use `docs/adr/`. |
| **Pillar Alignment** | Does the architecture align with the 6 Core Pillars (Security `2200`, Performance `2300`, Observability `2600`, Compliance `2400`, Documentation `2100`, Localization `2500`)? | **Mandatory** | See `.agent/rules/`. |
| **Agent Rule Compliance** | Does the tech stack selection comply with language/framework specific laws (e.g., `1200-Nextjs.md`) defined in `.agent/rules/`? | **Mandatory** | |

> **Process Enforcement**: The Planner Agent MUST explicitly answer all items of this checklist when creating an ARD, adhering to `.agent/rules/1910-architecture-documentation.md` and `.agent/rules/1901-architecture-rules.md`. The Reviewer Agent MUST verify that any code changes (e.g., in a PR) do not violate these agreed-upon decisions (such as unauthorized Tech Stack or DB changes) before merging.

## 4. Reference Technology Stack (Template)

Customize the following for your specific project upon cloning.

| Layer        | Recommended Technology         | Purpose                              |
| ------------ | ------------------------------ | ------------------------------------ |
| **Frontend** | React / Next.js / TailwindCSS  | Client-side interactions             |
| **Backend**  | Node.js / Python / Go / Rust   | Server-side APIs and logic           |
| **Database** | PostgreSQL / MongoDB           | Data persistence                     |
| **DevOps**   | Docker / GitHub Actions        | CI/CD and Containerization           |

## 4. Integration & Separation Points

### Document vs Code vs Operations

- **`docs/`**: Holds "Why" and "What" (PRD, ADR, ARD).
- **`specs/`**: Holds "Exactly How" prior to coding.
- **`runbooks/`**: Holds executable scripts and "What to do when X fails."

### Extending the Architecture

1. **Design Changes**: Create an ADR in `docs/adr/` using `templates/architecture/adr-template.md`.
2. **Data Structure Changes**: Document via ARD in `docs/ard/` using `templates/architecture/ard-template.md`.
3. **Execution Rules**: Modify `.agent/rules/` to enforce new architectural linters globally.

---
> **Note**: This architecture document must be kept strictly to high-level system design. For operational procedures, alerting logic, or CI orchestration, consult `OPERATIONS.md`.
