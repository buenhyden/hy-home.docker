---
layer: agentic
---

# infra-cross-validate

## Overview

Cross-validation orchestrator after infra changes. Runs security audit followed by drift + performance validation.

## Purpose

Ensure infrastructure changes are validated by independent security and drift/performance checks.

## Scope

**Covers:**

- Security audit handoff to security-auditor
- Drift/performance validation by iac-reviewer
- Result capture and notification

**Excludes:**

- Applying infra changes

## Structure

- Phase 1: security-auditor audit
- Phase 2: iac-reviewer drift + performance checks
- Phase 3: result merge and recording

## Agents

- **infra-implementer** — orchestrates pipeline
- **security-auditor** — security audit
- **iac-reviewer** — drift/performance validation

## Skills

- Depends on [infra-validate](infra-validate.md)

## Usage

- Trigger after infra change and post-flight validation.
- **Inputs:** changed file list
- **Outputs:** `_workspace/cross-validate_<date>.md`

## Artifacts

- `_workspace/cross-validate_<date>.md`

## Related Documents

- `../../scopes/infra.md`
- `../../scopes/security.md`
- `../../rules/github-governance.md`
- `../README.md`
