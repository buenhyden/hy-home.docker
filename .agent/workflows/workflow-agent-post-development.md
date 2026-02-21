---
description: AI Reviewer & DevOps Agent logic for the Post-Development phase.
---

# Workflow: Agent Post-Development

This workflow defines the execution loop for the **Reviewer Agent** and **DevOps Agent** when a Pull Request is opened.

## 1. Code Review (Reviewer Agent)

When triggered on a PR:

1. **Spec Alignment**: Compare the PR diff against the originating `specs/<feature>/spec.md`. Find any code that implements undocumented logic.
2. **QA & Coverage**: Ensure that the tests correspond to the GWT acceptance criteria. Reject the PR if no tests are added for new logic.
3. **Security**: Scan for OWASP vulnerabilities or hardcoded secrets. Check adherence to `.agent/rules/2200-security-pillar.md` if present.
4. **Architecture Compliance**: Verify that the PR does not violate the agreed-upon tech stack, database, or NFRs defined in the Architecture Checklist / ARD. Reject if unauthorized tech is introduced without a corresponding ADR.
5. **Action**: Leave specific review comments on the PR. If any constraints are violated, block the merge.

## 2. Operational Handoff (DevOps Agent)

Once the PR logic is sound and the Reviewer Agent is satisfied:

1. Check if the PR introduces new operational needs (new database tables, environment variables, cron jobs, etc.).
2. If so, generate or update a runbook.
3. **Template Enforcement**: You MUST use `templates/operations/runbook-template.md`.
4. **Location Rule**: Save it to `runbooks/[service]-runbook.md`. **NEVER** save to `docs/runbook`.
5. **Infrastructure Sync**: If the PR requires new infrastructure, update the corresponding Infrastructure as Code (IaC) files (e.g., Terraform or Helm charts).
6. **Changelog Automation**: Generate semantic versioning release notes based on the PR changes and append them to `CHANGELOG.md`.

## 3. End State

Notify the human that the AI checks and operational documentation steps are complete, passing the final merge authority to them.
