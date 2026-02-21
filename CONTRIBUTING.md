# Contributing Guidelines

## Necessity & Required Content

This file is necessary to define the exact, mechanical steps a human must take to successfully merge code into this repository. While `COLLABORATING.md` outlines the high-level human-AI relationship, this file outlines the raw pre-requisites for Pull Requests.
**What Must Be Written Here**:

- Hard Code Quality Gates (Coverage, Linting).
- Branch naming and Conventional Commit rules.
- Spec-Driven PR referencing requirements.

## 1. Spec-Driven Core Rule

All new features **must** begin with a specification in the `specs/` folder. Pull Requests that add code without an approved, corresponding specification will be immediately rejected without review.

## 2. Template Enforcement

If your contribution involves documentation (ADR, PRD, Runbook, etc.), you **MUST** use the predefined templates located in the `templates/` directory.

- Do not invent your own format for Architecture Decision Records. Use `templates/architecture/adr-template.md`.
- Ensure all sections are filled out before submitting.

## 3. Local QA & Test Coverage (Pre-PR Gate)

We enforce strict Quality Assurance metrics. Before you pull request, you must successfully pass local checks:

1. **Coverages**: The PR must meet or maintain the project coverage baseline (**> 80%**).
2. **Test Layers**: Are Unit and Integration tests functioning as defined by the Spec and `.agent/rules/0700-testing-and-qa-standard.md`?
3. **Linting**: No static typing or linting errors allowed.
4. **Agent Rule Compliance**: All code MUST comply with the organizational standards in `.agent/rules/` (primarily `0140-engineering-excellence.md` and `2220-secure-coding.md`). The Reviewer Agent strictly evaluates PRs against these rules.

## 4. Pull Request Process

1. **Branch Naming**: Ensure your branch name follows the convention: `feature/XXX`, `fix/XXX`, or `docs/XXX`.
2. **Commit Messages**: Use Conventional Commits.
3. **Traceability**: Your PR description **must** reference the specific file in `specs/` it addresses.

## 5. Multi Sub-Agent Interaction

As part of the PR process, an AI Reviewer Agent may automatically review your PR. You must address their automated feedback before a human maintainer reviews the code. Do not dismiss AI-generated comments unless they hallucinate a requirement not in the original Spec.

## 6. Required References

- AI System roles: `AGENTS.md`
- Collaboration Hand-offs: `COLLABORATING.md`
- Code of Conduct: `CODE_OF_CONDUCT.md`
