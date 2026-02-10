# Agent Rules & Governance Checklist

This guide maps the **5 Governance Pillars** to the active **Agent Rules**
(`.agent/rules`). It demonstrates how the AI agent is programmed to autonomously
enforce the project's standards.

## How to Use This Map (as an Agent)

1. Start with **PRD + Plan + Spec** rules (Business/Product) to confirm the work is well-defined and traceable.
2. Confirm architecture baselines and documentation hierarchy (Architecture/Stack), then create ADR/ARD links if needed.
3. Only then implement code, ensuring changes map back to PRD/Spec requirement IDs and pass quality/ops gates.

## 1. Business & Product Checklist

**Role Enforced**: Lead Project Manager

| Checklist Item | Enforcing Rule | Description |
| :--- | :--- | :--- |
| **Requirements Traceability** | [`0200-workflow-standard.md`](../../.agent/rules/0200-Workflows/0200-workflow-standard.md) | Enforces that every code change maps to a refined Issue/Task. |
| **Acceptance Criteria** | [`0200-workflow-standard.md`](../../.agent/rules/0200-Workflows/0200-workflow-standard.md) | Requires GWT (Given-When-Then) format for "Ready" items. |
| **PRD & Spec Governance** | [`0120-requirements-and-specifications-standard.md`](../../.agent/rules/0100-Standards/0120-requirements-and-specifications-standard.md) | Enforces measurable PRD metrics, spec structure, and requirement ID traceability. |
| **Issue Derived from PRD/Spec** | [`0201-project-management-standard.md`](../../.agent/rules/0200-Workflows/0201-project-management-standard.md) | Requires issues to be created/refined from PRD/Spec with testable AC. |

## 2. Architecture & Tech Stack Checklist

**Role Enforced**: Senior Principal Engineer

| Checklist Item | Enforcing Rule | Description |
| :--- | :--- | :--- |
| **Proactive Reasoning** | [`0000-agentic-pillar-standard.md`](../../.agent/rules/0000-Agents/0000-agentic-pillar-standard.md) | Mandates logical dependency analysis and "Think before Act". |
| **Stack Alignment** | [`0002-strong-reasoner-agent.md`](../../.agent/rules/0000-Agents/0002-strong-reasoner-agent.md) | Enforces alignment with `ARCHITECTURE.md` and Stack rules. |
| **Architecture Baseline & ADRs** | [`0130-architecture-standard.md`](../../.agent/rules/0100-Standards/0130-architecture-standard.md) | Governs architecture blueprint alignment and ADR expectations for significant decisions. |
| **PRD/ADR/ARD Hierarchy** | [`1910-architecture-documentation.md`](../../.agent/rules/1900-Architecture_Patterns/1910-architecture-documentation.md) | Enforces documentation hierarchy and template compliance for PRD/ADR/ARD artifacts. |
| **Tech Stack Standard** | [`0150-tech-stack-standard.md`](../../.agent/rules/0100-Standards/0150-tech-stack-standard.md) | Ensures stack decisions align with the project's documented baseline. |

## 3. Development Process & Collaboration Checklist

**Role Enforced**: DevOps Governance

| Checklist Item | Enforcing Rule | Description |
| :--- | :--- | :--- |
| **Branching Strategy** | [`0200-workflow-standard.md`](../../.agent/rules/0200-Workflows/0200-workflow-standard.md) | Enforces `<type>/<id>-<desc>` naming convention. |
| **Commit Discipline** | [`0200-workflow-standard.md`](../../.agent/rules/0200-Workflows/0200-workflow-standard.md) | Enforces Conventional Commits style. |
| **PR Quality Gate** | [`0200-workflow-standard.md`](../../.agent/rules/0200-Workflows/0200-workflow-standard.md) | Blocks merging if CI checks fail or PR description is empty. |
| **Documentation Standards** | [`2100-documentation-pillar.md`](../../.agent/rules/2100-Documentation/2100-documentation-pillar.md) | Enforces documentation structure and link integrity for `docs/**/*.md` and `README.md`. |

## 4. Quality, Testing & Security Checklist

**Role Enforced**: QA Automation Engineer / Security Engineer

| Checklist Item | Enforcing Rule | Description |
| :--- | :--- | :--- |
| **Testing Pyramid** | [`0700-testing-and-qa-standard.md`](../../.agent/rules/0700-Testing_and_QA/0700-testing-and-qa-standard.md) | Enforces appropriate mix of Unit/Integration/E2E tests. |
| **Coverage (>80%)** | [`0700-testing-and-qa-standard.md`](../../.agent/rules/0700-Testing_and_QA/0700-testing-and-qa-standard.md) | Mandates 80% coverage and 100% on new logic. |
| **Test Writing (AAA/Isolation)** | [`0017-code-test-writing-standard.md`](../../.agent/rules/0000-Agents/0017-code-test-writing-standard.md) | Enforces AAA structure, isolation-first unit testing, determinism, and test traceability. |
| **Secure by Default** | [`2200-security-pillar.md`](../../.agent/rules/2200-Security/2200-security-pillar.md) | Enforces OWASP A01-A10 (Auth, Secrets, Injection). |
| **Quality Policy (Docs)** | [`audit-security-qa.md`](../manuals/audit-security-qa.md) | Declares test levels (Unit/Integration/E2E/Load), coverage targets, and review expectations. |
| **PR Quality Checklist** | [`.github/PULL_REQUEST_TEMPLATE.md`](../../.github/PULL_REQUEST_TEMPLATE.md) | Enforces local test pass, coverage targets, spec checklist completion, and docs validation. |

## 5. Operations, Deployment & Monitoring Checklist

**Role Enforced**: Site Reliability Engineer (SRE)

| Checklist Item | Enforcing Rule | Description |
| :--- | :--- | :--- |
| **Structured Logging** | [`2600-observability-pillar.md`](../../.agent/rules/2600-Observability/2600-observability-pillar.md) | Mandates JSON format for logs with correlation IDs. |
| **RED Metrics** | [`2600-observability-pillar.md`](../../.agent/rules/2600-Observability/2600-observability-pillar.md) | Requires Rate, Errors, Duration metrics for all services. |
| **RPO/RTO Targets** | [`2600-observability-pillar.md`](../../.agent/rules/2600-Observability/2600-observability-pillar.md) | Aligns system reliability goals with `OPERATIONS.md`. |
