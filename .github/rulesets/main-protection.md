# Main Branch Protection Ruleset Proposal

This file is a local GitHub settings proposal only. It is not an agent
instruction surface, and it does not apply remote repository settings by
itself.

## Current Remote State

- Verified on 2026-05-16 by read-only GitHub API calls.
- Repository rulesets: none returned by `gh api repos/buenhyden/hy-home.docker/rulesets --paginate`.
- `main` branch protection: enabled, but weaker than the target ruleset below.
- Required status checks: only `ci-summary`; strict up-to-date branch requirement is disabled.
- Pull request review protection: enabled object exists, but approving review count is `0` and CODEOWNERS review is not required.
- Conversation resolution, linear history, signed commits, and admin enforcement: disabled.
- Force pushes and branch deletion: disabled.
- Delete branch on merge: disabled.
- Merge methods: merge, squash, and rebase are all enabled.

## Target Ruleset

- Target branch: `main`.
- Require pull requests before merge.
- Require CODEOWNERS review for owned paths.
- Require conversations to be resolved before merge.
- Block force pushes.
- Block branch deletion.
- Require the latest branch head to pass required checks before merge.
- Prefer squash or rebase merge for a linear `main` history.
- Enable delete branch on merge after repository owner approval.

## Required Status Checks

Use the CI Quality Gates workflow job names as required checks:
`scripts/validation/check-repo-contracts.sh` enforces this list against
`.github/workflows/ci-quality.yml`.

- `docs-traceability`
- `repo-contracts`
- `git-flow-contract`
- `compose-validation`
- `compose-all-profiles-validation`
- `infrastructure-hardening`
- `template-security-baseline`
- `quickwin-baseline`
- `pre-commit`
- `zizmor`

## Application Boundary

Apply this proposal only after explicit owner approval. Until that approval and
remote application happen, this document is not evidence that branch protection
is enabled. Remote changes should be performed through GitHub UI or an audited
`gh api` command, then re-check:

- `gh api repos/buenhyden/hy-home.docker/rulesets --paginate`
- `gh api repos/buenhyden/hy-home.docker/branches/main/protection`
