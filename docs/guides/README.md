# Development Guides

This folder contains lifecycle guides for AI-assisted and human-assisted delivery.

## Guides

- `pre-development-guide.md` — requirements, PRD/ADR/spec creation, approval gate
- `development-guide.md` — implementation standards, testing, CI expectations
- `post-development-guide.md` — review, deployment readiness, runbook and incident readiness

Use these guides as the default execution path for feature delivery.

## Agent Rule Overrides

This directory is critical for AI-Human alignment. While general rules live in `.agent/rules/`, files in `docs/guides/` serve as project-specific and team-specific overrides. AI Agents are instructed to prioritize the constraints and working agreements documented here over the global generic rules.
