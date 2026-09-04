# Main Branch Protection Ruleset Proposal

This file is a local GitHub settings proposal only. It is not an agent
instruction surface, and it does not apply remote repository settings by
itself.

## Observation Boundary

- The dated public snapshot remains unchanged at
  `docs/90.references/data/0071-github-actions-control-plane-observation/data.yaml`.
- Authenticated `GET /repos/buenhyden/hy-home.docker/branches/main` was read on
  2026-09-05 (Asia/Seoul), at code SHA
  `591e3c607f97aa34739f41288b5243f0cd4f0aac`. It reported `protected: true`,
  `validation-changed` and `validation-full`, both bound to App `15368`, and
  enforcement level `non_admins`.
- This is a branch-summary observation, not full protection verification.
  The detailed `/branches/main/protection` read returned HTTP 403. Strict mode,
  review requirements, administrator enforcement, bypasses, rulesets, and
  environment settings therefore remain unverified.
- No remote setting was changed. New observation evidence belongs to the
  SPEC-0174 Task; it does not rewrite the frozen public snapshot.

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

The two required-check names were observed in the authenticated branch summary
above. The remaining target settings are desired state until detailed readback
confirms them; the partial observation must not be presented as full enforcement.
