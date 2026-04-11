---
layer: agentic
---

# infra-validate

## Overview

Pre/post Docker Compose validation pipeline. Ensures static correctness, drift detection, SLO checks, and post-flight health verification.

## Purpose

Provide a repeatable, auditable validation sequence around infrastructure changes.

## Scope

**Covers:**

- Pre-flight Compose validation
- Drift detection (optional live env)
- Post-flight health checks

**Excludes:**

- Security auditing (handled by security-auditor)
- Drift/performance review reports (handled by iac-reviewer)

## Structure

- Phases: Pre-flight → Static validate → Drift check → Apply → Post-flight
- Uses `bash scripts/validate-docker-compose.sh` and `docker compose` commands

## Agents

- **infra-implementer** — primary caller
- **iac-reviewer** — secondary caller

## Skills

- This function is a reusable orchestration skill.

## Usage

- Trigger before and after infra changes.
- **Inputs:** target compose files, change scope
- **Outputs:** validation logs and optional drift notes

## Artifacts

- `_workspace/drift_<date>.md` (if drift detected)

## Related Documents

- `../../scopes/infra.md`
- `../../rules/postflight-checklist.md`
- `../README.md`
