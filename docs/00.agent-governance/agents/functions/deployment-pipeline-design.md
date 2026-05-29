---
layer: agentic
---

# deployment-pipeline-design

## Overview

Deployment pipeline design function for the `hy-home.docker` workspace. Designs and audits the
repository's GitHub Actions workflows and gate placement, adapted for Docker Compose delivery.

## Purpose

Keep CI/CD pipelines safe, measurable, and aligned with workspace SLOs and the CI/CD pattern set.

## Scope

**Covers:**

- GitHub Actions workflow design and review (`.github/workflows/*.yml`, e.g. `ci-quality.yml`)
- Security/quality gate placement using `ci-cd-patterns`
- Anti-duplication between local pre-commit and CI jobs (per `rules/github-governance.md`)

**Excludes:**

- Generic deployment runbooks (external `deployment-procedures` skill)
- Deployment strategy theory (see `ci-cd-patterns`)

## Structure

- Map change → select workflow/gates → validate against governance → capture pipeline doc

## Agents

- **ci-cd-engineer** — primary caller

## Skills

- Runtime mirror: `.claude/skills/deployment-pipeline-design/skill.md`

## Usage

- Trigger when designing or auditing CI/CD pipelines for this repository.
- **Inputs:** changed workflows, gate requirements
- **Outputs:** pipeline design/audit doc in `_workspace/`

## Artifacts

- `_workspace/pipeline_design_<date>.md`

## Related Documents

- `../../scopes/ops.md`
- `../functions/ci-cd-patterns.md`
- `../../rules/github-governance.md`
- `../README.md`
