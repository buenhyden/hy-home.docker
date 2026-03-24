---
title: 'Collaboration Manual'
status: 'Active | Draft'
version: 'v1.0.0'
date: 'YYYY-MM-DD'
owner: 'buenhyden'
layer: 'common'
tags: ['manual', 'collaboration', 'workflow']
---

# Collaboration Manual

> **Status**: [Active | Draft]
> **Version**: v1.0.0
> **Date**: YYYY-MM-DD
> **Layer**: common
> **Review Cycle**: Quarterly

**Overview (KR):** [팀의 협업 방식, 커뮤니케이션 채널, 그리고 코드 리뷰 및 배포 슬롯에 대한 약속을 한국어로 1-2문장 요약하세요.]

---

## 1. Team Roles & Governance

| Role | Responsibility | Primary Contact |
| ---- | -------------- | --------------- |
| **Product Owner** | Requirements & Priority | [Name] |
| **Tech Lead** | Architecture & Quality | [Name] |
| **DevOps/SRE** | Infrastructure & Availability | [Name] |

---

## 2. Communication Strategy

* **Sync**: [e.g., Daily Standup @ 10:00 AM]
* **Async**: [e.g., Slack for quick Qs, GitHub for code]
* **SLA**:
  * PR Review: < 24 hours
  * Critical Bug: < 4 hours

---

## 3. Development Workflow

### 3.1. Definition of Ready (DoR)

* [ ] Clear Acceptance Criteria (AC)
* [ ] Technical approach approved
* [ ] Mockups/Designs available (if UI)

### 3.2. Definition of Done (DoD)

* [ ] Tests pass (Unit, Integration)
* [ ] Documentation updated
* [ ] Security scan passed
* [ ] Peer review approved

---

## 4. GitHub Standards

* **Branching**: [e.g., Trunk-based / GitHub Flow]
* **Pull Requests**:
  * Use the project PR template.
  * Link to the related issue.
  * Keep PRs small (< 400 lines).

---

## 5. Escalation & Conflict Resolution

1. Peer discussion.
2. Tech Lead / PO arbitration.
3. Post-mortem/Retrospective for process improvement.
