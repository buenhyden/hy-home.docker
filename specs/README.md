# Technical Specifications Hub (`specs/`)

This directory is the absolute **Source of Truth** for the During-Development phase. It exists explicitly and exclusively for **Spec-Driven Development**.

## 1. Directory Structure

Specifications are organized by domain to ensure clarity and ease of navigation.

### 🏗️ Infrastructure (`specs/infra/`)

Core infrastructure implementation details, partitioned by deployment sequence.

- [baseline/](file:///home/hy/projects/hy-home.docker/specs/infra/baseline/spec.md): Root orchestration, kernel hardening, and Day-0 bootstrap.
- [automation/](file:///home/hy/projects/hy-home.docker/specs/infra/automation/spec.md): Autonomous sidecars, resource limits, and self-provisioning dashboards.

## 2. Path to Implementation

1. **Draft**: AI Planner Agent creates `spec.md` and `plan.md` in a feature folder.
2. **Approve**: Human Developer reviews and approves the spec.
3. **Execute**: AI Coder Agent implements changes following the spec.
4. **Verify**: Automated scripts and manual checks confirm success.

## 3. Compliance Standard (`[REQ-SPT-05]`)

Every `spec.md` in this directory MUST contain:

- **Section 0**: Mandatory governance checklists.
- **Section 5**: 3+ Given-When-Then Acceptance Criteria for core requirements (Rule `[REQ-SPT-10]`).
- **Section 7**: A detailed Verification Plan (Unit/Integration/E2E).
- **Section 8/9**: Quantified NFRs and Operational procedures.

---
> [!IMPORTANT]
> **NO SPEC, NO CODE.** Coder Agents MUST NOT modify infrastructure without an approved specification.
