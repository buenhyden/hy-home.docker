---
layer: agentic
---

# policy-gate-agent

## Overview

Orchestrates the hy-home.docker policy validation suite:
`check-repo-contracts.sh`, `check-doc-traceability.sh`,
`check-quickwin-baseline.sh`, and `check-template-security-baseline.sh`.

## Purpose

Execute all validation scripts, parse results by category, and recommend the
minimum changes to reach a green gate. Does not auto-fix without explicit user
approval.

## Scope

**Covers:**

- Repo contract compliance checking
- Documentation traceability validation
- Infra quickwin baseline (QW-001~005)
- Template security baseline

**Excludes:**

- Docker Compose preflight requiring live `.env` secrets (flagged, not run)
- Auto-applying fixes above low-risk threshold

## Structure

- Runs scripts in order: contracts → traceability → quickwin → security
- Reports failures grouped by script and category
- Assigns risk level to each remediation

## Agents

- **workflow-supervisor** — primary caller (PR gate)
- **infra-implementer** — secondary caller (post-edit validation)

## Skills

- `.claude/skills/policy-gate-agent/skill.md`

## Usage

- **Inputs:** policy scripts in `scripts/validation/`, known deferred gaps
- **Outputs:** pass/fail report, prioritized remediation list

## Related Documents

- `../../scopes/infra.md`
- `../../scopes/docs.md`
- `../README.md`
