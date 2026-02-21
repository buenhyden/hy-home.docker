# Product Requirements Documents (PRD)

This directory contains Product Requirements Documents that define the "what" of product features - the business requirements, user stories, and success metrics.

## What is a PRD?

A Product Requirements Document (PRD) captures the business perspective of a feature:

- **What** the product should do
- **Why** it's being built
- **Who** it's for
- **How** success will be measured

PRDs are the starting point for the Spec-Driven Development workflow.

## When to Create a PRD

Create a PRD when:

- Starting a new feature or product
- Defining user requirements and business goals
- Before creating implementation specifications
- Communicating product decisions to stakeholders

## How to Create a PRD

1. **Determine Domain/Feature**: PRDs MUST be placed inside a specific business domain folder (e.g., `docs/prd/auth/`, `docs/prd/payments/`). Do NOT place PRDs directly in the root of `docs/prd/`.
2. **Use the Template**: Copy `templates/product/prd-template.md` to this directory
3. **Name Convention**: `[feature]-prd.md` (e.g., `user-authentication-prd.md`)
4. **Fill All Sections**: Overview, audience, metrics, user stories, scope
5. **Get Approval**: PRD must be approved before specs are created

```bash
# Example workflow
mkdir -p docs/prd/payments
cp templates/product/prd-template.md docs/prd/payments/payment-integration-prd.md
# Edit the file with your requirements
# Get human approval before proceeding to specs/
```

## PRD Template

All PRDs MUST use `templates/product/prd-template.md`. The template includes:

| Section | Purpose |
| --- | --- |
| **Product Overview** | What and why |
| **Target Audience** | User personas |
| **Success Metrics** | Measurable goals |
| **User Stories & Features** | Requirements with acceptance criteria |
| **Out of Scope** | Explicit exclusions |
| **Dependencies** | External requirements |

## User Story Format

Use the standard format:

```text
As a [persona], I want to [action] so that [benefit].
```

Each user story must include:

- **Title**: Short descriptor
- **Description**: Detailed explanation
- **Acceptance Criteria**: Specific, testable conditions

### Example

```markdown
**Feature**: User Login with Email

As a returning user, I want to log in with my email so that I can access my account quickly.

**Acceptance Criteria**:
- Email and password fields are visible on login page
- "Forgot Password" link is available
- Error message shown for invalid credentials
- Redirect to dashboard on successful login
```

## Success Metrics

Define quantifiable and measurable success criteria as mandated by `[REQ-SPT-01] Explicit Success Metric Grounding`:

| Metric Type | Example |
| --- | --- |
| **Business** | Increase conversion by 5% |
| **User** | Reduce time-to-complete by 30% |
| **Technical** | API response time < 200ms |

## Relationship to Other Documents

```text
[User Need]
      ↓
docs/prd/ (What - Product Requirements)
      ↓
docs/ard/ (How - Architecture Requirements)
      ↓
specs/ (Implementation Specifications)
```

## PRD to Spec Workflow

1. **Planner Agent** creates PRD in `docs/prd/`, adhering to `.agent/rules/0120-requirements-and-specifications-standard.md`.
2. **Human** reviews and approves PRD.
3. **Planner Agent** generates spec in `specs/`.
4. **Reviewer Agent** validates specs against the PRD and formatting rules, ensuring GWT testability before implementation begins.
5. **Coder Agents** implement based on spec.

## AI Agent Guidelines

When working with PRDs:

1. **Use template**: Always use `templates/product/prd-template.md`
2. **Be specific**: Define quantifiable success metrics (No vague terms like "fast" without an explicit baseline).
3. **Include acceptance criteria**: Every feature needs testable criteria
4. **Link to specs**: After approval, create corresponding `specs/[feature]-spec.md`

## Index of PRDs

| Document | Feature | Status | Last Updated |
| --- | --- | --- | --- |
| - | *No PRDs yet* | - | - |

> Add entries to this index as PRDs are created.
