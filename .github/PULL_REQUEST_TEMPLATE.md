# Pull Request

> **Warning**: Your PR title MUST follow the **Conventional Commits** format (`feat:`, `fix:`, `docs:`, etc.) as mandated by `docs/00.agent-governance/rules/git-workflow.md`.

## Related Specification

- **Spec File:** [Link to the file in `docs/04.specs`]
- **Issue:** Resolves #

## Change Type

- [ ] Feature
- [ ] Bug fix
- [ ] Refactor
- [ ] Documentation
- [ ] Operations / Runbook

## Description

[Describe the changes made in this pull request]

## Breaking Changes

- [ ] No breaking changes
- [ ] Breaking changes included (describe below)

[If breaking, describe migration path and impact]

## Validation Evidence

List exact commands used and outcome.

```bash
# Example:
# npm test
# npm run lint
```

## Risk Assessment

- Risk Level: [Low/Medium/High]
- Rollback Plan: [Describe rollback or mitigation]

## Validations

- [ ] I have reviewed the relevant governance rules under `docs/00.agent-governance/rules`.
- [ ] My code strictly follows the Implementation Specification.
- [ ] Documentation has been added/updated using `docs/99.templates` (if applicable).
- [ ] **Commit Standard**: My Pull Request title uses Conventional Commits format.
- [ ] I have run tests locally.
- [ ] I have listed exact validation commands and outcomes above.
- [ ] No secrets or credentials are included in this PR.
- [ ] If operational behavior changed, runbook updates were added under `docs/09.runbooks`.
