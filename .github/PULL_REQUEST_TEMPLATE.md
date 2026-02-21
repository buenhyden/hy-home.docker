# Pull Request

> **Warning**: Your PR Title MUST follow the **Conventional Commits** format (`feat:`, `fix:`, `docs:`, etc.) as mandated by `.agent/rules/0401-git-workflow-standard.md`!

## Related Specification

- **Spec File:** [Link to the file in `specs/`]
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

- [ ] I have read the `CONTRIBUTING.md` document.
- [ ] My code strictly follows the Implementation Specification.
- [ ] Documentation has been added/updated utilizing the `templates/` folder (if applicable).
- [ ] **Commit Standard**: My Pull Request title uses Conventional Commits format.
- [ ] I have run tests locally.
- [ ] **Test Coverage Baseline:** I have verified unit test lines coverage is > 80% (`npm run test:coverage` or equivalent).
- [ ] No secrets or credentials are included in this PR.
- [ ] If operational behavior changed, runbook updates were added under `runbooks/`.
