---
title: 'Contributing Guide'
layer: 'guides'
---

# Contributing Guide

## 1. Spec-Driven Development

All new features require a specification in `docs/specs/`. PRs without an approved spec will be rejected.

## 2. Template Enforcement

Use `templates/` for all documentation artifacts (ADR, PRD, Runbook, etc.).

## 3. Quality Assurance (Pre-PR Gates)

- **Coverage**: Maintain > 80% baseline.
- **Tests**: Unified Unit/Integration tests.
- **Linting**: Markdown MUST follow `MD001` to `MD051`.
- **Infrastructure**: Execute within WSL2 filesystem; no absolute host paths.

## 4. Pull Request Process

- **Naming**: `feature/`, `fix/`, or `docs/`.
- **Commits**: Conventional Commits.
- **Traceability**: PRs must reference the corresponding `docs/specs/` file.

## 5. Agent Governance

All contributions must comply with rules in `docs/agentic/rules/`.
