# Pull Request

> **Warning**: Your PR title MUST follow the **Conventional Commits** format (`feat:`, `fix:`, `docs:`, etc.) as mandated by `docs/00.agent-governance/rules/git-workflow.md`.
> Human `feat/` and `fix/` source branches MUST include an issue ID segment, for example `feat/123-add-service`.

## Related Specification

- **Spec File:** [Link to the file in `docs/03.specs`]
- **Issue:** Resolves #

## Change Type

- [ ] Feature
- [ ] Bug fix
- [ ] Refactor
- [ ] Documentation
- [ ] Operations / Runbook

## Readiness

- [ ] Ready for review
- [ ] Draft/WIP (explain remaining work below)

[If Draft/WIP, list the remaining work and blocking checks.]

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

- Coverage target: [90% applicable / N/A]
- Coverage rationale: [Explain coverage result or why this PR is docs/infra/config-only]
- Fix/Refactor evidence: [For bug fixes, list regression evidence. For refactors, state behavior-preserving checks.]

## Harness Impact

- [ ] No harness surface changed
- [ ] `docker-compose.yml` or `infra/**` changed
- [ ] `secrets/**` path, registry, or secret mapping changed
- [ ] `.env.example` changed
- [ ] `scripts/**` validation, hardening, hook, or operation command changed
- [ ] `.github/workflows/**` changed
- [ ] `docs/00.agent-governance/**` changed
- [ ] `docs/05.operations/**` changed
- [ ] `docs/99.templates/**` changed

If any harness surface changed, list exact validation evidence:

```bash
bash scripts/validation/validate-harness.sh
bash scripts/validation/run-local-qa-gates.sh --script-backed
# Compose-affecting changes only:
bash scripts/validation/validate-docker-compose.sh --preflight
```

Secret handling:

- [ ] No secret values, tokens, private keys, or certificate contents are included
- [ ] Secret-related changes record only path, ID, registry, and redacted evidence

See [Approval Boundaries](../docs/00.agent-governance/rules/approval-boundaries.md) for protected surfaces.

## Risk Assessment

- Risk Level: [Low/Medium/High]
- Rollback Plan: [Describe rollback or mitigation]

## Validations

- [ ] I have reviewed the relevant governance rules under `docs/00.agent-governance/rules`.
- [ ] My source branch follows the governed branch policy in `docs/00.agent-governance/rules/git-workflow.md`.
- [ ] My code strictly follows the Implementation Specification.
- [ ] Documentation has been added/updated using `docs/99.templates`, or marked N/A with a reason.
- [ ] **Commit Standard**: My Pull Request title uses Conventional Commits format.
- [ ] Required GitHub Actions checks are passing or pending checks are explained above.
- [ ] CODEOWNERS-triggered reviewers have been requested for owned paths.
- [ ] Commits are small, logical, and reviewable, or squash strategy is documented.
- [ ] Draft/WIP state is accurate and remaining work is listed when applicable.
- [ ] I have run tests locally.
- [ ] I have listed exact validation commands and outcomes above.
- [ ] No secrets or credentials are included in this PR.
- [ ] If operational behavior changed, runbook updates were added under `docs/05.operations`.
