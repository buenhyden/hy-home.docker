# Main Branch Protection Tracked State and Recovery

This file is a local record of the intended and last verified GitHub settings.
It is not an agent instruction surface and does not apply remote repository
settings by itself.

## Observation Boundary

- The dated public snapshot remains at
  `docs/90.references/data/0071-github-actions-control-plane-observation/data.yaml`;
  it is historical evidence and is not rewritten as current state.
- On 2026-09-05, the repository owner approved a PATCH limited to
  `branches/main/protection/required_status_checks`. The applied state and full
  protection read-back are recorded in
  [the completed SPEC-0172 outcome](../../docs/98.archive/completed/03.specs/0172-document-contract-convergence/spec.md#remote-control-plane-evidence).
- That read-back verified `strict=true`, required contexts
  `validation-changed` and `validation-full`, and GitHub Actions app ID 15368.
  Review, CODEOWNERS, conversation-resolution, admin, signature,
  linear-history, force-push, deletion, creation, lock, and fork-sync settings
  were unchanged.
- Environment, deployment, release, and later control-plane state remain
  `unverified` unless a newer approved observation records them.

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

Both checks were bound to GitHub Actions app ID 15368 in the 2026-09-05
read-back. `strict=true` remains required.

## Rollback State

If a later authenticated read-back does not match the two aggregate checks,
restore the exact pre-change state captured on 2026-09-05:

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
- `frontend-quality`
- `storybook-coverage`

Keep `strict=true`. Bind every restored context to app ID 15368 except
`frontend-quality`, whose captured before-state was unbound.

## Application Boundary

Apply future changes only after explicit owner approval. Remote changes should
be performed through GitHub UI or an audited `gh api` command, then re-check:

- `gh api repos/buenhyden/hy-home.docker/rulesets --paginate`
- `gh api repos/buenhyden/hy-home.docker/branches/main/protection`

The 2026-09-05 read-back is point-in-time evidence, not a perpetual guarantee.
Any later claim of remote enforcement requires a new authenticated read-back;
tracked workflow or policy files alone prove only repository configuration.
