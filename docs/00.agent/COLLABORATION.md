---
title: 'Team Collaboration Guide'
layer: 'manuals'
---

# Team Collaboration Guide

## 1. Environment & IDE Rules

- **Native WSL2**: Always use VS Code `Remote - WSL` extension. Do NOT modify files across the OS boundary (e.g., from Windows Explorer to Linux path).

## 2. Pre-Development (Planning)

- **Planner Agent**: Use `docs/99.templates/prd.template.md` and `docs/99.templates/spec.template.md`.
- **Approval**: Humans MUST approve the PRD and Spec before code generation begins.

## 3. During-Development (Implementation)

- **Coders**: Implement logic EXACTLY as specified. Do not invent edge cases.
- **Hallucinations**: If the agent gets stuck, stop it and adjust the `docs/04.specs/` or `docs/07.guides/`.

## 4. Post-Development (Review & Ops)

- **Reviewer**: AI performs initial linting and security checks.
- **DevOps**: Use `docs/99.templates/runbook.template.md` to update deployment guides.

## 5. Metadata & Layering

- Every Markdown file MUST include the `layer:` frontmatter.
- Follow the flat documentation taxonomy rooted in `docs/`.
