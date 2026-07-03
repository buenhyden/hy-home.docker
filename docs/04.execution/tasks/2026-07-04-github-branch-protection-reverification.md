---
status: completed
---

<!-- Target: docs/04.execution/tasks/2026-07-04-github-branch-protection-reverification.md -->

# Task: GitHub Branch Protection Reverification

## Overview

This task records the read-only remote GitHub re-verification for
`WDC-GAP-022`. It updates local evidence for `main` branch protection without
mutating GitHub settings, workflows, rulesets, credentials, or repository
configuration.

## Inputs

- **Parent Plan**: [Document contract remediation batch plan](../plans/2026-07-03-document-contract-remediation-batches.md)
- **Source Register**: [Document contract gap register](../../90.references/audits/document-contracts/gap-register.md)
- **Local GitHub Protection Record**: [main protection proposal](../../../.github/rulesets/main-protection.md)
- **GitHub Governance Policy**: [GitHub governance](../../00.agent-governance/rules/github-governance.md)

## Working Rules

- Use GitHub API reads only.
- Do not create, update, or delete remote rulesets, branch protection, workflow
  settings, repository settings, PRs, labels, branches, secrets, or credentials.
- Do not record GitHub token values, credentials, raw logs, shell history, or
  secret material.
- Treat the local governance rule as stricter than remote enforcement when
  remote settings are weaker.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `.github/rulesets/main-protection.md`; `docs/00.agent-governance/rules/github-governance.md` | User continuation for the next document-contract follow-up and WDC-GAP-022 remote re-verification gate | Local record of remote GitHub branch protection state | Local record was last verified on 2026-05-28 and was marked historical in `WDC-GAP-022`. | Local record now states 2026-07-04 read-only verification: classic branch protection remains active on `main`, rulesets are not active, 12 remote required checks are enforced, and `docs-implementation-alignment` is not yet remotely required. | `git revert` the GitHub branch-protection re-verification commit | No remote mutations; no GitHub token values, credentials, secret values, raw logs, shell history, or private keys |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Verify GitHub CLI authentication and repository identity without recording token values. | doc | N/A | PLN-WDC-RM-002 / WDC-GAP-022 | `gh auth status`; `gh repo view --json nameWithOwner,url,defaultBranchRef` | Codex | Done |
| T-002 | Read remote rulesets and `main` branch protection through GitHub API. | doc | N/A | PLN-WDC-RM-002 / WDC-GAP-022 | `gh api repos/buenhyden/hy-home.docker/rulesets --paginate --jq 'length'`; `gh api repos/buenhyden/hy-home.docker/branches/main/protection --jq ...` | Codex | Done |
| T-003 | Update local branch-protection evidence and governance wording. | doc | N/A | PLN-WDC-RM-002 / WDC-GAP-022 | Local diff review | Codex | Done |
| T-004 | Regenerate indexes and run documentation validation. | doc | N/A | VAL-WDC-RM-001 through VAL-WDC-RM-007 | Verification Summary | Codex | Done |

## Remote Verification Summary

| Check | Result |
| --- | --- |
| Repository | `buenhyden/hy-home.docker` |
| Default branch | `main` |
| Repository rulesets | `0`; no repository rulesets are active |
| Protection model | Classic branch protection active on `main` |
| Required status checks | 12 contexts, strict/latest up-to-date branch enabled |
| Required check contexts | `docs-traceability`, `repo-contracts`, `git-flow-contract`, `compose-validation`, `compose-all-profiles-validation`, `infrastructure-hardening`, `template-security-baseline`, `quickwin-baseline`, `pre-commit`, `zizmor`, `frontend-quality`, `storybook-coverage` |
| Local-only required check gap | `docs-implementation-alignment` is present in local CI contract but not remotely required as of 2026-07-04 |
| Pull request reviews | 1 approving review required; CODEOWNERS review required |
| Conversation resolution | Required |
| Force pushes | Disabled |
| Branch deletion | Disabled |
| Admin enforcement | `false`; local no-bypass governance still applies |
| Required linear history | Not remotely required |
| Merge methods | Squash, rebase, and merge commits are allowed |
| Delete branch on merge | Disabled |
| Remote mutation | None |

## Verification Summary

- **Test Commands**:
  - `gh auth status`
  - `gh repo view --json nameWithOwner,url,defaultBranchRef`
  - `gh api repos/buenhyden/hy-home.docker/rulesets --paginate --jq 'length'`
  - `gh api repos/buenhyden/hy-home.docker/branches/main/protection --jq '{...}'`
  - `gh api repos/buenhyden/hy-home.docker --jq '{...}'`
  - `git diff --check`
  - `bash scripts/knowledge/generate-llm-wiki-index.sh --check`
  - `bash scripts/operations/sync-provider-surfaces.sh --check`
  - `bash scripts/validation/check-doc-traceability.sh`
  - `bash scripts/validation/check-doc-implementation-alignment.sh`
  - `bash -n scripts/validation/check-repo-contracts.sh`
  - `bash scripts/validation/check-repo-contracts.sh`
- **Eval Commands**: N/A for read-only GitHub governance evidence.
- **Logs / Evidence Location**: This task document, `.github/rulesets/main-protection.md`,
  `docs/00.agent-governance/rules/github-governance.md`, and the source
  `gap-register.md`.
- **Results**:
  - PASS: GitHub CLI repository identity is `buenhyden/hy-home.docker` with
    default branch `main`.
  - PASS: read-only rulesets query returned `0`.
  - PASS: read-only branch protection query returned classic branch protection
    with 12 remote required checks and strict/latest up-to-date branch enabled.
  - PASS: generated `docs/90.references/llm-wiki/llm-wiki-index.md` with
    1130 paths.
  - PASS: provider surfaces have no drift.
  - PASS: doc traceability reports `failures=0`.
  - PASS: doc implementation alignment reports `failures=0`,
    `stage_docs_total=550`, and `removed_template_mentions_total=0`.
  - PASS: repo-contract shell syntax is valid.
  - Expected FAIL: full repo contracts report `failures=2`, confined to the
    known out-of-scope Keycloak hardening image mismatch and tech-stack
    expected-image drift. The changed document template gate reports
    `changed_template_docs_total=4`, `normalized_changed_template_docs_total=4`,
    and `legacy_changed_template_docs_skipped=0`.
- **Manual Checks**: Confirmed that this task did not mutate remote GitHub
  settings, workflows, rulesets, branch protection, repository settings, PRs,
  labels, branches, secrets, or credentials. `docs-implementation-alignment`
  remains a local required CI contract but not a remote required check.

## Related Documents

- **Parent Plan**: [Document contract remediation batch plan](../plans/2026-07-03-document-contract-remediation-batches.md)
- **Source Register**: [Document contract gap register](../../90.references/audits/document-contracts/gap-register.md)
- **Local GitHub Protection Record**: [main protection proposal](../../../.github/rulesets/main-protection.md)
- **GitHub Governance Policy**: [GitHub governance](../../00.agent-governance/rules/github-governance.md)
