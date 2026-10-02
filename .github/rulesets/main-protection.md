# Main Branch Protection Tracked State and Recovery

This file is a local record of the intended and last verified GitHub settings.
It is not an agent instruction surface and does not apply remote repository
settings by itself.

## Observation Boundary

- The dated public snapshot remains at
  the retired DATA-0071 package, preserved under `docs/98.archive/retired/`;
  it is superseded historical evidence and is not current state.
- On 2026-09-05, the repository owner approved a PATCH limited to
  `branches/main/protection/required_status_checks`. The applied state and full
  protection read-back are recorded in
  the completed SPEC-0172 outcome (`docs/98.archive/completed/03.specs/0172-document-contract-convergence/spec.md#remote-control-plane-evidence`).
- That read-back verified `strict=true`, required contexts
  `validation-changed` and `validation-full`, and GitHub Actions app ID 15368.
  Review, CODEOWNERS, conversation-resolution, admin, signature,
  linear-history, force-push, deletion, creation, lock, and fork-sync settings
  were unchanged.
- On 2026-09-08, the repository owner approved two further changes and the
  applied state was read back through the authenticated API. Required contexts
  became `validation-changed` alone, and
  `required_pull_request_reviews.required_approving_review_count` became zero
  with `require_code_owner_reviews` false. The read-back reported
  `strict=true`, `allow_force_pushes=false`, `allow_deletions=false`,
  `required_conversation_resolution=true`, `enforce_admins=false`,
  `lock_branch=false` and `required_linear_history=false`, so pull requests are
  still required before merge and nothing was widened beyond the two approved
  fields. The prior full protection payload is retained outside the repository
  as the rollback source.
- On 2026-10-02, an authenticated read-only API check confirmed the current
  `main` protection still has strict `validation-changed` from Actions app
  15368, zero required approvals, no CODEOWNERS review, conversation
  resolution, and disabled force pushes and deletion. Repository rulesets were
  empty. Environments `qa-control` and `qa-tag-publish` existed with secret
  names `QA_VERIFIER_PRIVATE_KEY` and `QA_PUBLISHER_PRIVATE_KEY`, respectively;
  secret values were not read. Both environments admitted **protected branches**
  (`protected_branches=true`, `custom_branch_policies=false`), not a custom
  branch pattern restricted to `main`. The workflow did not reference either
  environment or secret. User-supplied App IDs 5156980 and 5156975 are not
  independently mapped to installed Apps by this read-back.
- Those two App credentials and environments are prepared but not activated by
  the tracked workflow. The existing `update-main-current` job already updates
  the channel tag with `GITHUB_TOKEN` after `main-security`. Activating a
  Publisher App in parallel would create a second tag writer. A Verifier App
  would need its own distinct provenance purpose and trusted event boundary;
  it is not required to remove duplicate QA. Before any future activation,
  confirm installation and permissions, decide whether it replaces an existing
  writer, and bind environment access to the intended branch rule. Such a
  control-plane change requires separate approval and read-back.

## Target Ruleset

- Target branch: `main`.
- Require pull requests before merge.
- Require zero approving reviews. The repository has a single collaborator who
  authors every pull request, and GitHub forbids self-approval, so any non-zero
  count names an approver who cannot exist and makes administrator bypass the
  only merge path.
- Do not require CODEOWNERS review, for the same reason. `.github/CODEOWNERS`
  stays as the ownership record it is and no longer gates merges.
- Require conversations to be resolved before merge.
- Block force pushes.
- Block branch deletion.
- Require the latest branch head to pass required checks before merge.
- Do not enforce squash/rebase-only or linear-history settings that would
  discard referenced objects, so delivered history can keep them.
- Recovery-commit preservation and branch deletion are stated once, in
  `.agents/governance/github-governance.md` section 3. This file records the
  settings that support those rules, not the rules themselves.

## Required Status Checks

Use the CI Quality Gates workflow job names as required checks:
`.github/workflow-contract.yml` owns their exact machine identity, and
the focused workflow checker proves that every required job projects its
registered root DAG exactly once through static typed-gate invocations.

- `validation-changed`

`validation-full` runs only on manual dispatch. Main pushes run `main-security`
on the merged revision, then `update-main-current` only after that audit succeeds.
Neither post-merge job is a PR pre-merge gate; a failure after a push cannot
retroactively prevent that merge. The required PR context remains
`validation-changed` on every PR event, including title edits.

GitHub treats a job skipped by a job-level condition as successful for required
checks. A whole workflow skipped by path/branch filters or a commit-message
instruction can leave its expected checks pending. A dependent aggregate also
needs explicit failure propagation: a skipped dependent job alone must not hide
a failed prerequisite. See the
[official required-check troubleshooting guide](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks).

A past merge blockage cannot be attributed to a skipped job without the actual
check-run, PR head or test-merge SHA, expected source app, and contemporaneous
protection configuration. The current required context is bound to GitHub
Actions app ID 15368 with `strict=true`; current dated read-back belongs in the
active Task, separately from the observations above.

## Rollback State

A difference from this desired contract is a prompt to inspect, not permission
to restore old settings. Obtain a fresh authenticated read-back and bind any
approved correction to the exact field, before-state, target and recovery.

For required checks, the current desired state is `validation-changed` alone,
`strict=true`, app ID 15368. Do not restore the retired individual-check list or
a previous two-context list from historical prose. Those contexts may no longer
be produced on the required event or revision. Other protection fields require
their own approved before-state and must not be reset incidentally.

If reverting a future approved change, use that change's captured before-state
only after confirming its checks are still produced by the matching workflow
and event. Verify the resulting setting with authenticated read-back and record
it in the current Task. Local Git recovery restores tracked definitions only.

## Application Boundary

Apply future changes only after explicit owner approval. Remote changes should
be performed through GitHub UI or an audited `gh api` command, then re-check:

- `gh api repos/buenhyden/hy-home.docker/rulesets --paginate`
- `gh api repos/buenhyden/hy-home.docker/branches/main/protection`

Every dated read-back is point-in-time evidence, not a perpetual guarantee.
Any later claim of remote enforcement requires a new authenticated read-back;
tracked workflow or policy files alone prove only repository configuration.
