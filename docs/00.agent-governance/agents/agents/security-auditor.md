---
layer: agentic
---

# security-auditor

## Overview

Container and secrets security specialist. Audits Compose and infra artifacts against OWASP Top 10 and ASVS L2 with severity-tagged findings.

## Purpose

Prevent security regressions by detecting plaintext secrets, unsafe access patterns, and unpinned artifacts.

## Scope

**Covers:**

- Container security auditing
- Secrets exposure detection
- GitHub Actions security baseline checks

**Excludes:**

- Implementing fixes (reports only)

## Structure

- Scope import: `docs/00.agent-governance/scopes/security.md`
- Threat-model first → scan → report workflow

## Agents

- **security-auditor** — Security audit specialist (read-only)

## Skills

- [security-audit](../functions/security-audit.md)
- [infra-cross-validate](../functions/infra-cross-validate.md)

## Usage

- Trigger for new/changed services or suspected security issues.
- **Inputs:** target paths, scope path, audit trigger
- **Outputs:** `_workspace/security_audit_<date>.md`

## Artifacts

- `_workspace/security_audit_<date>.md`

## Related Documents

- `../../scopes/security.md`
- `../../rules/github-governance.md`
- `../../rules/postflight-checklist.md`
- `../../subagent-protocol.md`
- `../README.md`
