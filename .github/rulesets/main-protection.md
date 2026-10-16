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
- On 2026-10-13, `main` was pushed directly twice, at 11:16:06Z
  (`338c607d8` to `4072f8af8`) and 12:10:11Z (`40f194e99` to `5a93ea054`),
  without a pull request. The pushes came from local worktree branches that
  tracked `origin/main`, most likely through an editor's sync; the pusher was
  not identified. The last protection read-back (2026-09-08) reported
  `enforce_admins=false`, under which an admin credential can push to `main`
  directly; it was not read again on 2026-10-13. The owner can close that by enabling
  admin enforcement or a ruleset with no bypass actor. The repository now adds
  a tracked `pre-push` guard (`scripts/hooks/pre-push-guard.sh`), initially
  installed through pre-commit, and agent-side denials
  (SPEC-0241); neither changes the remote settings.
- On 2026-10-14, at the owner's direction (AskUserQuestion), `enforce_admins`
  was enabled with `gh api -X POST
  repos/buenhyden/hy-home.docker/branches/main/protection/enforce_admins`.
  Authenticated read-back before and after, at 2026-10-14T08:46:11Z, showed
  `enforce_admins` false then true, and every other field identical:
  `strict=true`, `contexts=[]`, zero required approvals, conversation
  resolution on, force pushes, deletions and linear history off, branch not
  locked. Admin credentials now need a pull request to change `main`. The
  same day the main checkout installed the `pre-commit`, `commit-msg` and
  `pre-push` hooks. Rollback is `gh api -X DELETE` on the same endpoint, by
  separate approval.
- On 2026-10-15, authenticated read-only protection lookup confirmed
  `enforce_admins=true`, `strict=true`, empty `contexts` and `checks`, zero
  required approvals, conversation resolution on, and force pushes and
  deletion off. The current producer's name is still not a required remote
  check. Local source tests do not close that gap. The raw-ref guard now has
  a repository-local installer so every ref, including deletions, is checked
  before any pre-commit selection; installation and an observed Git push
  rejection remain separate evidence in the current Task.
- On 2026-10-16 KST, an observed successful `candidate-quality` PR check from
  GitHub Actions app ID 15368 preceded a PATCH limited to
  `branches/main/protection/required_status_checks`. A general progress
  approval preceded an automatic-review rejection because the change persists
  for future main PRs. An exact follow-up question named `main`, required
  status checks, and that future-PR effect; the user then approved main required
  check settings. Authenticated before/after read-back verified the normalized
  before state `{"strict":true,"contexts":[],"checks":[]}` and after state
  `{"strict":true,"contexts":["candidate-quality"],"checks":[{"context":"candidate-quality","app_id":15368}]}`.
  All other protection fields and empty rulesets were unchanged. The narrow
  rollback is `{"strict":true,"contexts":[],"checks":[]}`; use it only
  after a fresh read-back and separate approval.
- Later on 2026-10-16, independent authenticated read-only lookups using API
  versions `2026-03-10` and `2022-11-28` confirmed the configured target:
  `strict=true`, projected `contexts=["candidate-quality"]`, and
  `checks=[{"context":"candidate-quality","app_id":15368}]`. PR 505 at head
  `e459c4ec1aaf652ad26d17e67daaf7ff5bb23aac` was `BLOCKED` while its only
  unsatisfied observed condition was the failed App 15368 `candidate-quality`
  check. This proves the failed-current-head negative case without a merge
  attempt; it does not prove the remaining enforcement cases below.
- A later read-only observation bound PR 506 head
  `2fbcf8982945d6e8d3666e6940e3accde728c768` to a successful App 15368
  `candidate-quality` check and confirmed the protected PR merged as main
  `89eb43f683a11587cf4f125be534ae720c20a55c`. This is a matching-success
  observation for that exact head, not a claim about later revisions or the
  unexercised missing, stale and wrong-App cases.

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
  deletion denial remain separate controls. The live read-back matches this
  target; any future correction requires its own approved setting change.
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

The current 2026-10-16 KST authenticated read-back has `strict=true` and the
single required check `candidate-quality` from GitHub Actions app ID `15368`;
the API contexts are `candidate-quality`. It followed an observed successful
PR check, a first automatic-review rejection because the setting affects all
future main PRs, and a new exact user approval. The scoped PATCH changed only
`branches/main/protection/required_status_checks`; the before, after, PATCH,
and rollback scratch receipts are supplementary only at
`/tmp/hyhome-r13-main-protection-before.json`,
`/tmp/hyhome-r13-main-protection-after.json`,
`/tmp/hyhome-r13-required-status-checks-patch.json`, and
`/tmp/hyhome-r13-required-status-checks-rollback.json`. This document retains
the canonical normalized before state `{"strict":true,"contexts":[],"checks":[]}`,
after state `{"strict":true,"contexts":["candidate-quality"],"checks":[{"context":"candidate-quality","app_id":15368}]}`, and rollback
`{"strict":true,"contexts":[],"checks":[]}`. Read-back confirmed
all other protection fields unchanged, including admin enforcement, conversation
resolution, review settings, force-push/deletion denial, and empty rulesets.
No stale retired `validation-changed` context was restored.

If a future read-back drifts to the exact empty-check state, the minimal
recovery is limited to
`branches/main/protection/required_status_checks` with this payload:

```json
{"strict":true,"checks":[{"context":"candidate-quality","app_id":15368}]}
```

The payload omits deprecated `contexts`; GitHub may project the check name into
that read-back field. It preserves strict mode and binds the candidate check to
the observed GitHub Actions App. Administrator enforcement, reviews,
conversation resolution, force-push denial and deletion denial are outside the
scoped PATCH and must compare equal before and after. Recovery requires a fresh
empty-state read-back, an exclusive operator window and separate owner
approval. It is not pending while the live target already matches.

```bash
set -euo pipefail
umask 077
workdir="$(mktemp -d /tmp/hyhome-main-protection.XXXXXX)"
before="$workdir/before.json"
immediate="$workdir/immediate-before.json"
after="$workdir/after.json"
proposed="$workdir/proposed.json"
rollback="$workdir/rollback.json"
gh api -H "X-GitHub-Api-Version: 2026-03-10" repos/buenhyden/hy-home.docker/branches/main/protection > "$before"
jq -e '.required_status_checks.strict == true and .required_status_checks.contexts == [] and .required_status_checks.checks == []' "$before"
jq '.required_status_checks | {strict,contexts,checks}' "$before" > "$rollback"
printf '%s\n' '{"strict":true,"checks":[{"context":"candidate-quality","app_id":15368}]}' > "$proposed"
gh api -H "X-GitHub-Api-Version: 2026-03-10" repos/buenhyden/hy-home.docker/branches/main/protection > "$immediate"
cmp -s "$before" "$immediate"
gh api -H "X-GitHub-Api-Version: 2026-03-10" --method PATCH repos/buenhyden/hy-home.docker/branches/main/protection/required_status_checks --input "$proposed"
gh api -H "X-GitHub-Api-Version: 2026-03-10" repos/buenhyden/hy-home.docker/branches/main/protection > "$after"
jq -S 'del(.required_status_checks)' "$before" > "$workdir/before-unmodified.json"
jq -S 'del(.required_status_checks)' "$after" > "$workdir/after-unmodified.json"
cmp -s "$workdir/before-unmodified.json" "$workdir/after-unmodified.json"
jq -e '.required_status_checks as $r | $r.strict == true and $r.checks == [{"context":"candidate-quality","app_id":15368}] and (($r.contexts == []) or ($r.contexts == ["candidate-quality"])) and ([($r.contexts[]?), $r.checks[].context] | unique) == ["candidate-quality"]' "$after"
```

The PATCH command is the approval boundary. Any failed assertion stops
acceptance. Rolling a recovery back to the captured empty state weakens the
currently observed control and needs another separate approval. After that
approval, PATCH the captured payload, read the full resource again, and compare
all unmodified fields:

```bash
gh api -H "X-GitHub-Api-Version: 2026-03-10" --method PATCH repos/buenhyden/hy-home.docker/branches/main/protection/required_status_checks --input "$rollback"
gh api -H "X-GitHub-Api-Version: 2026-03-10" repos/buenhyden/hy-home.docker/branches/main/protection > "$workdir/rollback-readback.json"
jq -e '.required_status_checks.strict == true and .required_status_checks.contexts == [] and .required_status_checks.checks == []' "$workdir/rollback-readback.json"
jq -S 'del(.required_status_checks)' "$workdir/rollback-readback.json" > "$workdir/rollback-unmodified.json"
cmp -s "$workdir/before-unmodified.json" "$workdir/rollback-unmodified.json"
```

The recorded producer metadata proves only its named SHA. The fresh PR 505
observation proves only the failed-current-head negative case. No PATCH is
pending while the live read-back matches the target:

| Case | Required current input | Expected observation | Current status |
| --- | --- | --- | --- |
| Missing check | Current PR head with no `candidate-quality` check | Merge state blocked; no matching current-head check run | NOT_RUN |
| Failed check | PR 505 head `e459c4ec1aaf652ad26d17e67daaf7ff5bb23aac` with App 15368 failure | Merge state `BLOCKED`; current-head conclusion is failure and every other observed check succeeded or skipped | PASS |
| Stale success | New PR head after a prior head succeeded | Merge state blocked; success exists only on the old SHA | NOT_RUN |
| Wrong App | Same check name from a separately installed App | Merge state blocked; App ID differs from 15368 | BLOCKED until such an independently permissioned App exists |
| Matching success | PR 506 head `2fbcf8982945d6e8d3666e6940e3accde728c768` with App 15368 success and every other protection condition satisfied | Required-check state was satisfied and the protected PR merged as main `89eb43f683a11587cf4f125be534ae720c20a55c` | PASS |

For each available case, capture both the PR merge state and current head's
check runs. Do not invoke a merge as a test. A wrong-App case cannot be
synthesized by editing JSON and remains blocked until a separately permissioned
App produces it.

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

- `gh api -H "X-GitHub-Api-Version: 2026-03-10" repos/buenhyden/hy-home.docker/rulesets --paginate`
- `gh api -H "X-GitHub-Api-Version: 2026-03-10" repos/buenhyden/hy-home.docker/branches/main/protection`

Every dated read-back is point-in-time evidence, not a perpetual guarantee.
Any later claim of remote enforcement requires a new authenticated read-back;
tracked workflow or policy files alone prove only repository configuration.
