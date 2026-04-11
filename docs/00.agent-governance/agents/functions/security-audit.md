---
layer: agentic
---

# security-audit

## Overview

Threat-model-first security audit orchestration function for the workspace. Covers container, Compose, workflow, and code-security audits with remediation-oriented reporting.

## Purpose

Provide a repeatable audit flow that detects security regressions early and records actionable, evidence-backed findings.

## Scope

**Covers:**

- container and Compose security auditing
- workflow and automation security auditing
- secret exposure and dependency risk review

**Excludes:**

- implementing fixes
- real-time SOC operations

## Structure

- Runtime mirror: `.claude/skills/security-audit/skill.md`
- Threat-model first → scan → report workflow

## Agents

- **security-auditor** — primary operator
- **workflow-supervisor** — coordination support
- **incident-responder** — incident-linked escalation path

## Skills

- This function is a reusable orchestration skill.

## Usage

- Trigger for security audits of code, infra, or workflow assets.
- **Inputs:** target paths, audit trigger, optional incident context
- **Outputs:** `_workspace/security_audit_<date>.md`

## Artifacts

- `_workspace/security_audit_<date>.md`

## Related Documents

- `../../scopes/security.md`
- `../../rules/github-governance.md`
- `../../rules/postflight-checklist.md`
- `../README.md`
