# Collaborating in this Framework

## Necessity & Required Content

This file is absolutely necessary to establish the operational handoffs between Human Developers and the Multi Sub-Agent System. While `AGENTS.md` defines what the AI does, this file defines how the *Human* manages the AI.
**What Must Be Written Here**:

- Workflow handoff rules across Pre-Dev, During-Dev, and Post-Dev phases.
- Conflict resolution tactics for AI Hallucinations.
- Pointers to mandatory collaborative processes.

## 0. Mandatory Project Kickoff

Before any major development begins, the team MUST establish working agreements.

- **Action**: Use `templates/guides/collaboration-guide-template.md` to create `docs/manuals/collaboration-guide.md`.
- **Requirement**: Answer all 11 items in the **Development Process & Collaboration Checklist** (e.g., Branching Strategy, SLA, DoD, Code Review rules).
- **Enforcement**: AI Agents will verify the existence and completeness of this guide during project initialization.

## 1. Requesting Work (Pre-Development)

When requesting new features, humans should primarily interact with the **Planner Agent**.

- **Human**: Defines the high-level business need in an Issue or a prompt.
- **AI (Planner)**: Utilizes `templates/product/prd-template.md` to generate a PRD (`docs/prd/`).
- **AI (Planner)**: Once the PRD is approved, it writes an Implementation Spec in `specs/` using `templates/engineering/spec-template.md`.
- **Human**: MUST approve the final spec before any code is generated.

## 2. Code Implementation Workflow (During-Development)

Humans generally **do not write boilerplate**.

- **AI (Backend/Frontend Coder)**: Implements code and inline tests EXACTLY as specified in `specs/`.
- **Rule of Thumb**: The AI should never invent undocumented edge cases. If missing, it must stop and ask.
- **Human**: Provide domain-specific guidance only when the AI encounters genuine architectural friction not covered by `ARCHITECTURE.md`.

## 3. Code Review & Deployment (Post-Development)

- **AI (Reviewer)**: Performs initial linting, security checks, and spec-compliance verification on the PR.
- **Human**: Final merge approval, focusing on business value and preventing regressions.
- **AI (DevOps)**: Instructed to generate/update the deployment guide in `runbooks/` using `templates/operations/runbook-template.md`.

## 4. Resolving Conflicts (AI Hallucinations)

If an AI Agent hallucinates or gets stuck in a loop:

1. Explicitly stop the agent.
2. Manually adjust the specification in `specs/` or add rigid constraints to `docs/guides/` or `llms.txt`.
3. Re-prompt the agent, pointing them firmly to the specific markdown line they disregarded.

## 5. Evolving the Rules (Collaborating on Standards)

Standard Agent Rules live in `.agent/rules/`. Project-specific context lives in `llms.txt` or `docs/guides/`.

1. **Project-Specific Overrides**: Humans can define overrides to global `.agent/rules/` within `llms.txt` or specific `docs/guides/`. Agents will prioritize `llms.txt` for project context.
2. **Global Rule Updates**: If a global standard needs to evolve, humans must update the corresponding markdown file in `.agent/rules/` to ensure all future Agents act upon the new intent.
3. **Contradictions**: If human instructions contradict an established `.agent/rule/`, the Agent will flag the violation based on `.agent/rules/` and request explicit confirmation to bypass or update the rule.
