# Main Branch Protection Ruleset Proposal

This file is a local GitHub settings proposal only. It is not an agent
instruction surface, and it does not apply remote repository settings by
itself.

## Observation Boundary

- The dated public snapshot lives in
  `docs/90.references/data/governance/github-actions-control-plane-observation.yaml`.
- Authenticated current ruleset, branch-protection, required-check, review,
  environment, and repository-setting readback is unavailable.
- Control-plane verification is `unverified`; this proposal does not infer
  applied remote state from tracked files or public workflow metadata.
- A future verification pass records new evidence separately instead of
  rewriting the approved snapshot without source support.

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
`.github/workflow-contract.yml` owns their exact machine identity, and
`scripts/validation/check-repo-contracts.sh` retains the Stage 00 desired-state
comparison through the focused workflow checker.

- `docs-traceability`
- `docs-implementation-alignment`
- `repo-contracts`
- `agent-output-eval-fixture-gate`
- `supply-chain-fixture-policy`
- `dependency-vulnerability-audit`
- `git-flow-contract`
- `compose-validation`
- `compose-all-profiles-validation`
- `infrastructure-hardening`
- `template-security-baseline`
- `quickwin-baseline`
- `pre-commit`
- `frontend-quality`
- `storybook-coverage`
- `zizmor`

## Application Boundary

Apply future changes only after explicit owner approval. Remote changes should
be performed through GitHub UI or an audited `gh api` command, then re-check:

- `gh api repos/buenhyden/hy-home.docker/rulesets --paginate`
- `gh api repos/buenhyden/hy-home.docker/branches/main/protection`
