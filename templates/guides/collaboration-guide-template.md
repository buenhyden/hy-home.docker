# Development Process & Collaboration Guide

*Target Directory: `docs/manuals/collaboration-guide.md`*
*Description: This document defines the team's working agreements, development processes, and collaboration SLAs as per the 0202-collaboration-and-sla-standard.md rules.*

---

## 1. Team Roster & Decision Makers

Explicitly define who makes the final calls to prevent deadlocks.

| Role | Name | Responsibilities |
| ---- | ---- | ---------------- |
| **Product Owner (PO)** | [Name] | Business requirements, priority, final feature sign-off |
| **Tech Lead (TL)** | [Name] | Architecture decisions, code review final say, technical dispute resolution |
| **QA Lead** | [Name] | Test strategy, release sign-off |

## 2. Communication Channels & SLAs

Define how the team communicates and what the expected response times are to prevent flow-breaking delays.

| Channel | Purpose | Expected Response SLA |
| ------- | ------- | --------------------- |
| **Slack/Teams - #project-channel** | Daily syncs, quick questions | `< 4 hours` |
| **GitHub Pull Requests** | Code Review & Feedback | `< 24 business hours` |
| **Jira / GitHub Issues** | Task tracking, AC discussions | `< 24 business hours` |
| **Urgent Incidents (Pager)** | P0/SEV-1 Production Downs | `< 15 minutes` |

## 3. Development Methodology

- **Process Type**: [e.g., Scrum / Kanban / Shape Up]
- **Sprint Length**: [e.g., 2 weeks]
- **Rituals**:
  - **Planning**: [e.g., Every other Monday at 10 AM]
  - **Daily Standup**: [e.g., Async on Slack by 9:30 AM]
  - **Retrospective**: [e.g., Last Friday of the sprint]

## 4. Definition of Ready (DoR) & Definition of Done (DoD)

### Definition of Ready (Before coding starts)

- [ ] Issue has a clear **Problem Statement**.
- [ ] Issue has measurable **Acceptance Criteria (Given/When/Then)**.
- [ ] UI designs/Figma links are attached (if applicable).
- [ ] Technical implementation approach is approved (e.g., via ADR or Spec document).

### Definition of Done (Before merging/closing)

- [ ] All Acceptance Criteria are met and verified.
- [ ] Unit & Integration tests are written and passing in CI.
- [ ] Code has been reviewed and approved by at least **[N]** reviewers.
- [ ] Relevant documentation (API specs, runbooks) has been updated.
- [ ] Automated security and linting checks are green.

## 5. Branching & Merge Strategy

- **Branching Model**: [e.g., GitHub Flow / Trunk-Based Development]
- **Branch Naming**:
  - Features: `feat/[issue-id]-short-desc`
  - Bugs: `fix/[issue-id]-short-desc`
- **Merge Policy**:
  - [e.g., Direct pushes to `main` are strictly prohibited.]
  - [e.g., Squash and Merge is enforced for clean commit history.]

## 6. Code Review Guidelines

- **Reviewer Count**: Minimum **[N]** approvals required.
- **PR Size Limits**: PRs should ideally be under **[X]** lines of code to ensure quality reviews.
- **Reviewer Expectations**: Check for architecture alignment, test coverage, and security, not just syntax (which should be handled by formatters).

---

## 7. Collaboration Checklist (Initial Setup)

*Ensure all statements below are True before starting the project.*

- [ ] We have defined the final technical decision-maker.
- [ ] We have agreed upon communication SLAs for PR reviews.
- [ ] We have customized the DoR and DoD for our team's context.
- [ ] `.github/PULL_REQUEST_TEMPLATE.md` has been updated to reflect our DoD.
- [ ] `.github/ISSUE_TEMPLATE/*.md` has been updated to enforce GWT (Given/When/Then) Acceptance Criteria.
