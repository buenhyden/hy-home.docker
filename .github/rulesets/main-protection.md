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
- At that observation, those two App credentials and environments were prepared but not activated by
  the tracked workflow. The then-existing `update-main-current` job updated
  the channel tag with `GITHUB_TOKEN` after `main-security`. Activating a
  Publisher App in parallel would create a second tag writer. A Verifier App
  would need its own distinct provenance purpose and trusted event boundary;
  it is not required to remove duplicate QA. Before any future activation,
  confirm installation and permissions, decide whether it replaces an existing
  writer, and bind environment access to the intended branch rule. Such a
  control-plane change requires separate approval and read-back.

- On 2026-10-07, the owner explicitly authorized removal of the stale
  `validation-changed` context. Authenticated before/after read-back verified
  `contexts=[]`, `checks=[]`, `strict=true`, with every other protection field
  unchanged; rulesets and effective rules were empty. Receipt and rollback
  payloads were retained outside tracked source. This is a dated observation,
  not evidence that a later candidate context is already required.

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
- Require the one produced PR candidate context `candidate-quality` from
  GitHub Actions. Pull requests, resolved conversations, force-push denial and
  deletion denial remain separate controls. Applying this new target requires
  its own approved setting change after a real check-run is observed.
- Do not enforce squash/rebase-only or linear-history settings that would
  discard referenced objects, so delivered history can keep them.
- Recovery-commit preservation and branch deletion are stated once, in
  `.agents/governance/github-governance.md` section 3. This file records the
  settings that support those rules, not the rules themselves.

## Required Status Checks

The source target is `candidate-quality` alone: one always-present PR job runs
selected changed validation. Individual leaves are not separate contexts.
There is no feature-push QA, title-edit validation, or main full-profile repeat.
Main security/SARIF uses merged input and a different trust purpose; it is not
candidate acceptance. Manual SemVer publication is a separate approved action.

The current last read-back is the empty context set above. Source implementation
of the new producer does not activate protection. Before proposing its actual
setting, verify the PR job's exact name, source App, head/merge revision and
success/failure behavior, then capture the full before-state and scoped rollback.
No stale retired `validation-changed` context may be restored from old prose.

A whole workflow skipped by path/branch filters or commit instructions can leave
an expected check pending. Selection happens inside the PR workflow; title edits
do not replace revision evidence. See the
[required-check troubleshooting guide](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks).

## Rollback State

A difference from this desired contract is a prompt to inspect, not permission
to restore old settings. Obtain a fresh authenticated read-back and bind any
approved correction to the exact field, before-state, target and recovery.

Do not restore a retired context or copied historical list. The candidate
producer and its exact source identity must be observed before any approved
setting change. Other protection fields must not be reset incidentally.

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
