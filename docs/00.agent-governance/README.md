---
layer: agentic
---

# AI Agent Governance Hub

Welcome to the central governance directory for AI Agents. This folder defines the rules, scopes, and protocols for all automated and assisted development tasks.

## 1. Context & Objective

- **Purpose**: To provide a single source of truth (SSoT) for AI agent behavior, technical constraints, and governance protocols.
- **Identity Protocol**: AI Agents must establish identity via [AGENTS.md](../../AGENTS.md) and load this hub at session start.
- **Compliance**: All work must follow the **01-11 Stage-Gate Taxonomy**. Decisions must be anchored in ADRs, and implementations must be grounded in approved Specs.

## 2. Requirements & Constraints

- **Directory Structure**:
    - `rules/`: Universal core governance, persona mapping, and repository-wide standards.
    - `scopes/`: Layer-specific technical instructions and constraints (Architecture, Backend, Infra, etc.).
    - `claude-provider.md`: Provider-specific configuration for Claude Code.
    - `gemini-provider.md`: Provider-specific configuration for Gemini CLI.
- **Language Policy**:
    - **Governance Documentation**: All files in this directory MUST be written in **English** (token optimized).
    - **User Communication**: AI Agents MUST translate all responses and notifications into manual **Korean**.
    - **Rule Enforcement**: Follow the centralized policy in [language-policy.md](rules/language-policy.md).

## 3. Implementation Flow

### Gateway Dispatcher (JIT Context)

Use the following JIT loading markers to ingest task-specific context from the documentation taxonomy:

| Marker | Target README | Intent |
| :--- | :--- | :--- |
| `[LOAD:PRD]` | `docs/01.prd/README.md` | High-level requirements & vision |
| `[LOAD:ARD]` | `docs/02.ard/README.md` | Architectural reference & qualities |
| `[LOAD:ADR]` | `docs/03.adr/README.md` | Technical decisions & records |
| `[LOAD:SPECS]` | `docs/04.specs/README.md` | SSoT technical specifications |
| `[LOAD:PLANS]` | `docs/05.plans/README.md` | Implementation & validation plans |
| `[LOAD:TASKS]` | `docs/06.tasks/README.md` | Granular task & progress tracking |
| `[LOAD:RUNBOOKS]` | `docs/09.runbooks/README.md` | Operational execution procedures |

### Specialized Rule Dispatcher

| Strategy | Rule File | Dispatcher Marker |
| :--- | :--- | :--- |
| **Core Governance** | `rules/bootstrap.md` | `[LOAD:RULES:BOOTSTRAP]` |
| **Persona Matrix** | `rules/persona-matrix.md` | `[LOAD:RULES:PERSONA]` |
| **Language Policy** | `rules/language-policy.md` | `[LOAD:RULES:LANG]` |
| **Git Workflow** | `rules/git-workflow.md` | `[LOAD:RULES:GIT]` |
| **Operations** | `scopes/ops.md` | `[LOAD:RULES:OPS]` |
| **Documentation** | `scopes/docs.md` | `[LOAD:RULES:DOCS]` |

## 4. Operational Procedures

### Technical Scopes (Layer Map)

Agents MUST load the corresponding scope from `scopes/` before performing work in a specific layer:

- **Architecture**: `scopes/architecture.md` (`[LOAD:RULES:ARCH]`)
- **Backend**: `scopes/backend.md` (`[LOAD:RULES:BACKEND]`)
- **Frontend**: `scopes/frontend.md` (`[LOAD:RULES:FRONTEND]`)
- **Infrastructure**: `scopes/infra.md` (`[LOAD:RULES:INFRA]`)
- **Mobile**: `scopes/mobile.md` (`[LOAD:RULES:MOBILE]`)
- **Product**: `scopes/product.md` (`[LOAD:RULES:PRODUCT]`)
- **QA**: `scopes/qa.md` (`[LOAD:RULES:QA]`)
- **Security**: `scopes/security.md` (`[LOAD:RULES:SECURITY]`)
- **Ops**: `scopes/ops.md` (`[LOAD:RULES:OPS]`)
- **Common**: `scopes/common.md` (`[LOAD:RULES:COMMON]`)
- **Entry**: `scopes/entry.md` (`[LOAD:RULES:ENTRY]`)
- **Meta**: `scopes/meta.md` (`[LOAD:RULES:META]`)
- **Agentic**: `scopes/agentic.md` (`[LOAD:RULES:AGENTIC]`)

## 5. Maintenance & Safety

- **Updating Governance**: All changes to files in this directory must be documented in an ADR if they significantly alter agent behavior or repository taxonomy.
- **Validation**: Ensure any changes to dispatcher markers are reflected in root shims.
