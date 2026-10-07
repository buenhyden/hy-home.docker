# Pull Request

> **Warning**: Your PR title MUST follow the **Conventional Commits** format (`feat:`, `fix:`, `docs:`, etc.) as mandated by `.agents/governance/git-workflow.md`.
> Human `feat/` and `fix/` source branches MUST include an issue ID segment, for example `feat/123-add-service`.

## Related Specification

- **Spec File:** [Link to the file in `docs/03.specs`]
- **Execution Task:** [Link to the Task that owns checks, results and acceptance]
- **Issue:** Resolves #

Issues own requests and priority; Specs own contracts; Tasks own execution.
Link those owners rather than copying Spec criteria or a Task work log here.
Projects may show a filtered work view without changing Task lifecycle.

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

Link the Task evidence and summarize the checks relevant to this change.

```bash
# Example:
# Focused regression or explicit formatting command and result, when applicable
```

- Fix/Refactor evidence: [For bug fixes, list regression evidence. For refactors, state behavior-preserving checks.]
- Remote candidate: [PR head/base, workflow run, selected checks and conclusion]
- Unexecuted lanes: [Check, reason and next owner; source changes are not runtime proof]

## Harness Impact

- [ ] No harness surface changed
- [ ] `docker-compose.yml` or `infra/**` changed
- [ ] `secrets/**` path, registry, or secret mapping changed
- [ ] `.env.example` changed
- [ ] `scripts/**` validation, hardening, hook, or operation command changed
- [ ] `.github/workflows/**` changed
- [ ] Root shims or `.claude/**`, `.codex/**` changed
- [ ] `.agents/**` changed
- [ ] `docs/05.operations/**` changed
- [ ] `docs/99.templates/**` changed
- [ ] Main release preparation changes `CHANGELOG.md`

For release preparation, provide the proposed bare SemVer version and exact
dated `## [version] - YYYY-MM-DD` entry. Release tags and GitHub Releases are
created only by the separately authorized main release producer after merging;
this PR does not publish a release or move historical refs.

For affected surfaces, select checks from the
[shared change-type verification matrix](../.agents/governance/quality-standards.md#5-change-type-verification-matrix).
Record the selected command, execution environment, result, and reason for any
unexecuted check in Validation Evidence. This template adds no gate and does
not require both public profiles for every harness change.

Report hosted evidence separately: head commit, workflow run, job conclusion,
and any required review or branch-protection blocker. Local checks do not prove
hosted acceptance; a skipped or unexecuted check is not passing evidence.

Secret handling:

- [ ] No secret values, tokens, private keys, or certificate contents are included
- [ ] Secret-related changes record only path, ID, registry, and redacted evidence

Current contract evidence (when lifecycle, permission, parser or gate behavior
changes; otherwise record N/A and the reason in Validation Evidence):

- [ ] The implementation owner and independent reviewer differ
- [ ] Focused regression evidence covers the changed current invariant and failure boundary
- [ ] Registered candidate results and required acceptance are linked in the Task
- [ ] Source/provider configuration is not presented as live native-event execution

See [Approval Boundaries](../.agents/governance/approval-boundaries.md) for protected surfaces.

## Risk Assessment

- Risk Level: [Low/Medium/High]
- Rollback Plan: [Describe rollback or mitigation]

## Validations

- [ ] I have reviewed the relevant governance policies under `.agents/governance/`.
- [ ] My source branch follows the governed branch policy in `.agents/governance/git-workflow.md`.
- [ ] My code strictly follows the Implementation Specification.
- [ ] Documentation has been added/updated using `docs/99.templates`, or marked N/A with a reason.
- [ ] **Commit Standard**: My Pull Request title uses Conventional Commits format.
- [ ] Required GitHub Actions checks are passing or pending checks are explained above.
- [ ] CODEOWNERS-triggered reviewers have been requested for owned paths, or marked N/A because remote protection does not enforce owner review.
- [ ] Commits are small, logical, and reviewable.
- [ ] Draft/WIP state is accurate and remaining work is listed when applicable.
- [ ] Applicable focused development checks are recorded; aggregate candidate QA is owned by the remote PR.
- [ ] I have listed exact validation commands and outcomes above.
- [ ] No secrets or credentials are included in this PR.
- [ ] If operational behavior changed, runbook updates were added under `docs/05.operations`.
