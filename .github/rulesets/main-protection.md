# Main Branch Protection Ruleset Proposal

This file is a local GitHub settings proposal only. It is not an agent
instruction surface, and it does not apply remote repository settings by
itself.

## Current Remote State

- Verified read-only on 2026-07-04 by audited GitHub API calls during the
  document-contract follow-up pass. No remote settings were changed.
- Repository rulesets: classic branch protection active on `main`.
- Repository rulesets API returned `0`; no repository rulesets are active.
- Required status checks: 12 remote contexts currently required with strict/latest up-to-date branch requirement enabled:
  `docs-traceability`, `repo-contracts`, `git-flow-contract`, `compose-validation`,
  `compose-all-profiles-validation`, `infrastructure-hardening`, `template-security-baseline`,
  `quickwin-baseline`, `pre-commit`, `zizmor`, `frontend-quality`, `storybook-coverage`.
- Local CI contract includes `docs-implementation-alignment` and
  `agent-output-eval-fixture-gate`, but the 2026-07-04 read-only verification
  confirmed those contexts are not currently remote required checks. Agents
  must not assert remote enforcement for either context until repository
  protection is updated and reverified.
- Pull request review protection: 1 approving review required; CODEOWNERS review required.
- Conversation resolution: required before merge.
- Force pushes: disabled.
- Branch deletion: disabled.
- Admin enforcement: `enforce_admins=false`; agents still follow no-bypass governance policy locally.
- Linear history: not remotely required by branch protection; repository
  settings allow squash, rebase, and merge commits. Agents still prefer squash
  or rebase by local governance.
- Delete branch on merge: disabled.
- Agents must re-verify remote state in future audit passes before asserting enforcement.

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
- `docs-implementation-alignment`
- `repo-contracts`
- `agent-output-eval-fixture-gate`
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
