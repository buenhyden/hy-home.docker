---
trigger: always_on
glob: ["**/*"]
description: "Risk Management & Incident Response Standards: Enforces risk classification, mitigation for high-risk changes, and blameless post-mortems."
---

# Risk Management & Incident Response Standards

- **Role**: Reliability & Risk Architect
- **Purpose**: Define standards for identifying, mitigating, and responding to technical and operational risks to ensure system stability and data integrity.
- **Activates When**: Planning high-risk changes, responding to incidents, or conducting post-mortem reviews.

**Trigger**: always_on — Apply during all phases of change management and incident response.

## 1. Standards

### Principles

- **[REQ-RSK-01] Early Classification**
  - All technical changes MUST be classified by risk level (Low, Medium, High). Changes affecting core flows or data integrity are "High" by default.
- **[REQ-RSK-02] Blast Radius Minimization**
  - High-risk changes MUST utilize gradual rollout strategies (Feature flags, Canaries) to limit the potential impact of a failure.
- **[REQ-RSK-03] Blameless Post-Mortem Culture**
  - Incident reviews MUST focus on system and process failures rather than individual errors. The goal is learning and prevention, not blame.

### Risk Management Baseline

| Tier | Requirement ID | Critical Control |
| --- | --- | --- |
| Classification | [REQ-RSK-04] | Mandatory risk tiering in PRs |
| Rollback | [REQ-RSK-05] | Documented & tested rollback path |
| Incident | [REQ-RSK-06] | Defined Sev-1/2/3 criteria |
| Review | [REQ-RSK-07] | Blameless post-mortem for Sev-1/2 |

### Must

- **[REQ-RSK-08] Verified Rollback Feasibility**
  - High-risk changes MUST have a verified rollback plan that has been tested in a staging environment.
- **[REQ-RSK-09] Real-Time Monitoring Thresholds**
  - Every high-risk deployment MUST have associated monitoring alerts that trigger if core business metrics degrade.
- **[REQ-RSK-10] Documented Root Cause Analysis (RCA)**
  - All significant incidents MUST result in a documented RCA featuring a "Five Whys" analysis and actionable remediation items.

### Must Not

- **[BAN-RSK-01] High-Risk "Big Bang" Deployments**
  - DO NOT deploy high-risk architectural changes to 100% of users simultaneously. Use phased transitions.
- **[BAN-RSK-02] Speculative Incident Communication**
  - During an active incident, do NOT share speculative root causes with stakeholders; maintain communication based on verified facts.

### Failure Handling

- **Stop Condition**: Stop a planned change if the risk assessment identifies a single point of failure without a documented mitigation.

## 2. Procedures

- **[PROC-RSK-01] Risk Scoring Flow**
  - IF a PR affects > 500 lines or core security logic THEN MUST perform a formal risk scoring before merge approval.
- **[PROC-RSK-02] Incident Lifecycle**
  - UPON detection of a Sev-1 incident THEN MUST appoint an Incident Commander (IC) and establish a dedicated communication channel within 10 minutes.

## 3. Examples

### Risk Assessment (Good)

- **Risk Level**: High
- **Impact**: Potential downtime for checkout flow.
- **Mitigation**: Feature flag enabled for 5% of users; verify metrics for 60 mins.
- **Rollback**: Disable flag via dashboard.

## 4. Validation Criteria

- **[VAL-RSK-01] Rollout Success Rate**
  - [ ] Audit confirms that > 95% of high-risk changes utilize phased rollouts.
- **[VAL-RSK-02] RCA Action Completion**
  - [ ] Tracking system verifies that > 90% of remediation items from post-mortems are completed within the agreed SLA.
- **[VAL-RSK-03] Alert Precision**
  - [ ] Incident logs confirm that 100% of Sev-1 issues were detected by automated monitoring before user reports.
