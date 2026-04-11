---
layer: agentic
---

# iac-reviewer

## Overview

Infrastructure drift detector and configuration cross-checker. Reviews Docker Compose state against running containers and validates resource declarations.

## Purpose

Provide read-only drift and performance validation to prevent configuration and SLO regressions.

## Scope

**Covers:**

- Drift detection between declared and live infra state
- Network, secrets, volumes, and resource checks
- SLO risk detection for missing health checks or limits

**Excludes:**

- Applying changes (reports only)

## Structure

- Scope import: `docs/00.agent-governance/scopes/infra.md`
- Evidence-based findings with severity tags

## Agents

- **iac-reviewer** — Drift and performance validator (read-only)

## Skills

- [infra-validate](../functions/infra-validate.md)
- [infra-cross-validate](../functions/infra-cross-validate.md)

## Usage

- Trigger after infra changes or as part of cross-validation.
- **Inputs:** compose files, optional live container snapshot
- **Outputs:** `_workspace/iac_review_<date>.md`, `_workspace/cross-validate_<date>.md`

## Artifacts

- `_workspace/iac_review_<date>.md`
- `_workspace/cross-validate_<date>.md`

## Related Documents

- `../../scopes/infra.md`
- `../../rules/postflight-checklist.md`
- `../../subagent-protocol.md`
- `../README.md`
