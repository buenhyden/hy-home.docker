---
layer: agentic
---

# drift-detector

## Overview

Container configuration drift detection and policy compliance specialist. Detects discrepancies between declared Compose state and live container state, verifies security policy adherence, and designs auto-remediation strategies.

## Purpose

Prevent configuration drift from accumulating silently between deployments by providing read-only detection and remediation planning.

## Scope

**Covers:**

- Compose-declared vs live container state comparison
- Security policy compliance checks (no privileged, no host-network, resource limits)
- Auto-remediation strategy design

**Excludes:**

- Applying any changes (read-only)
- Security auditing (delegated to security-auditor)
- Full drift + performance validation reports (delegated to iac-reviewer)

## Structure

- Scope import: `docs/00.agent-governance/scopes/infra.md`
- Read-only: reports findings and remediation plans only

## Agents

- **drift-detector** — Drift detection and policy compliance specialist

## Skills

- [infra-validate](../functions/infra-validate.md)

## Usage

- Trigger for periodic drift checks or post-incident investigations.
- **Inputs:** target compose files + optional live container state
- **Outputs:** `_workspace/drift_<date>.md`

## Artifacts

- `_workspace/drift_<date>.md`

## Related Documents

- `../../scopes/infra.md`
- `../../rules/postflight-checklist.md`
- `../../subagent-protocol.md`
- `../README.md`
