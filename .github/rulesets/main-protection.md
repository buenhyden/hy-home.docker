# Main Branch Protection Ruleset Proposal

This file is a local GitHub settings proposal only. It is not an agent
instruction surface, and it does not apply remote repository settings by
itself.

## Observation Boundary

- The dated public snapshot lives in
  `docs/90.references/data/0071-github-actions-control-plane-observation/data.yaml`.
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
- Preserve referenced recovery commits in delivered history using merge commits
  or fast-forward. Do not enforce squash/rebase-only or linear-history settings
  that would discard referenced objects.
- Delete merged branches only after referenced recovery commits and regular
  source blobs are verified reachable from `main`, with owner approval.

## Required Status Checks

Use the CI Quality Gates workflow job names as required checks:
`.github/workflow-contract.yml` owns their exact machine identity, and
the focused workflow checker proves that every required job projects its
registered root DAG exactly once through static typed-gate invocations.

- `validation-changed`
- `validation-full`

## Application Boundary

Apply future changes only after explicit owner approval. Remote changes should
be performed through GitHub UI or an audited `gh api` command, then re-check:

- `gh api repos/buenhyden/hy-home.docker/rulesets --paginate`
- `gh api repos/buenhyden/hy-home.docker/branches/main/protection`

Until that separately approved readback succeeds, both checks above remain
tracked desired state rather than evidence of remote enforcement.
