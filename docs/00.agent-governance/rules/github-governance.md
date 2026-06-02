---
layer: agentic
---

# GitHub Governance Policy

Normative policy baseline aligning agent behavior with GitHub repository operations.
Repo-local stricter rules always override this document; never weaken them on the basis of this policy.

## 1. Repository Protection Contract

- Agents must treat `main` as a protected branch: no direct pushes, no force pushes, no bypass of required checks.
- This is an agent behavior contract. Remote branch protection was verified active on 2026-05-28 (12 required remote contexts, 1 approving review, CODEOWNERS required, conversation resolution required, no force-push/deletion, `enforce_admins=false`). Agents must re-verify remote state in future audit passes before asserting enforcement.
- "No exceptions" is mandatory agent behavior even when GitHub admin enforcement or repository rulesets do not fully enforce the same boundary.
- Remote branch protection and ruleset state must be verified from GitHub before claiming enforcement is active. The local verified-state record lives in `.github/rulesets/main-protection.md`.
- If remote enforcement is absent or unknown, agents must still follow protected-branch discipline locally and report the remote enforcement state as blocked or unverified.
- Required status checks listed in `.github/rulesets/main-protection.md` must pass before any PR is considered ready to merge. Agents must not declare "done" until those checks are green or explicitly report why remote enforcement could not be verified.
- CODEOWNERS-triggered reviews are mandatory. If a changed path is owned by a CODEOWNERS entry, that review must be obtained before merge — agents must note this requirement when completing PR review tasks.

## 2. Pull Request and Review Contract

- A PR is complete only when: (a) all required status checks pass, (b) all required code reviews are approved, (c) no unresolved BLOCK-severity findings remain.
- Draft/WIP PRs are allowed for collaboration, but they must not be treated as merge-ready and must list remaining work in the PR template.
- Agents must not self-approve or bypass required reviewers.
- When agents propose changes, they must list which CODEOWNERS paths are touched and which review gates apply.
- Merge method discipline: prefer squash or rebase to keep `main` history linear unless the project explicitly allows merge commits.

## 3. Merge and Branch Discipline

- Feature branches must be deleted after merge.
- Long-lived branches other than `main` require explicit user authorization.
- Rebase onto `main` before requesting merge if the branch diverges by more than a trivial number of commits.
- Agents must never modify another agent's in-progress branch without explicit coordination.

## 4. GitHub Actions Security Contract

- Workflows must use least-privilege `GITHUB_TOKEN` — request only the permissions the job actually needs.
- Prefer OIDC-based cloud credentials over long-lived secrets stored as repository secrets. When proposing or reviewing workflow changes, flag any use of long-lived cloud secrets as a WARN finding.
- Pin actions to a specific commit SHA or a digest-verified tag, not a floating branch or `@latest`.
- Secrets must never appear in log output (`echo $SECRET`, `run: env`, etc.). Flag any such pattern as BLOCK.
- Untrusted input into `$GITHUB_ENV`, `$GITHUB_OUTPUT`, or `run:` interpolation is a security injection risk — flag as BLOCK.
- Reusable workflows called from external repositories must be pinned and reviewed before use.

## 5. Execution Boundary (Local vs Remote)

- **Anti-Duplication**: Do not execute heavy workloads (e.g., Zizmor, Storybook ESLint) redundantly across both local `pre-commit` and dedicated GitHub Action jobs.
- **Local Responsibility**: Fail-fast static analysis (formatting, simple linting, pre-push contract scripts).
- **GitHub Responsibility**: Ultimate SSoT gates, E2E tests, SARIF generation, and workflows requiring secrets.
- **Implementation**: If a tool requires a dedicated CI job (e.g., for SARIF uploads), it must be removed from the local `.pre-commit-config.yaml` or skipped in the CI `pre-commit` runner via the `SKIP` environment variable.

### 5.0 Approved Remote Mutation Protocol

When the user approves remote GitHub mutation, agents must still bind the action
to a concrete repository and remote surface before changing state. Task evidence
must include the approval source, target repository, target setting or object,
command class, before-state evidence, after-state evidence, and rollback or
recovery path. Do not merge PRs, bypass required checks, weaken protected-branch
rules, or expose GitHub secrets unless the user separately names that concrete
action and target.

Read-only remote checks may be recorded as verification evidence. Remote state
that was approved but not changed must be reported as verified-only, not as a
mutation.

### 5.1 Evidence Boundary by Change Type

Agents must align local checks, CI-only gates, and skipped-check rationale with
the QA scope matrix. For PR-related work, the completion summary or task
evidence must state:

| Change Type | Required Local Evidence | CI-Only Evidence | Required Skip Rationale |
| --- | --- | --- | --- |
| Docs or governance docs | Diff hygiene, repo contracts, doc traceability, provider sync when provider docs changed | Required docs/repo contract jobs | Domain tests are N/A for docs-only changes. |
| Archive/tombstone migration | Diff hygiene, stale active-reference scans, repo contracts, doc traceability, archive ledger review | Required docs/repo contract jobs | Domain tests and runtime checks are N/A unless behavior/config changed. |
| Hook, script, or validator | Targeted command output plus repo contracts | Required quality/security jobs | GitHub-only permissions, SARIF upload, or protected remote state if not locally runnable. |
| Runtime or Docker config | Compose/hardening/local smoke checks when approved | Compose and hardening jobs | Live mutation skipped without approval. |
| GitHub workflow/protection | Static review and local contract checks | GitHub Actions and branch-protection verification | Any remote state not verified must be reported as unverified, not done. |

No task is complete by citing a CI-only gate alone when a cheap local check is
available, and no local-only check replaces required protected-branch gates.

## 6. Local Instruction Authority

- This repository does not adopt a GitHub-native instruction hierarchy for agent execution.
- Instruction authority lives in repo-local assets only:
  - root shims: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`
  - governance SSoT: `docs/00.agent-governance/`
  - runtime controls: `.claude/settings.json`, `.claude/hooks/`, `.claude/agents/`, `.claude/skills/`
  - Codex runtime hooks: `.codex/hooks.json`
- GitHub is used here for repository protection, PR workflow, and Actions execution; it is not the canonical home of agent instruction policy.
- Any future GitHub-native instruction file must be treated as out-of-scope until the repository governance explicitly adopts it.

## 7. Completion Gate (GitHub-Specific)

Before an agent declares any PR-related task complete, it must confirm:

1. All required status checks are green (or note which are pending and why), and remote branch protection state is verified or explicitly reported as unverified.
2. All required reviews are approved (or note which are outstanding and who owns them).
3. No BLOCK-severity findings remain from code review or security audit.
4. CODEOWNERS-triggered reviewers have been notified if paths are owned.
5. No secrets, long-lived credentials, or unpinned action references were introduced.

If any gate is unmet, the task status is "blocked" not "done."

## 8. CI/CD Job Taxonomy

`ci-quality.yml` defines required quality gates and separate GitHub-native
automation. Required job IDs must stay in sync with
`check-repo-contracts.sh` and `.github/rulesets/main-protection.md`.
Archive/tombstone validation is part of the `repo-contracts` gate: active
target-stage truth checks stay separate from `docs/98.archive` tombstone
template/status checks.

### Required Quality Gates

| Job ID                            | Execution Surface                                      |
| --------------------------------- | ------------------------------------------------------ |
| `docs-traceability`               | `scripts/validation/check-doc-traceability.sh`         |
| `repo-contracts`                  | `scripts/validation/check-repo-contracts.sh`           |
| `git-flow-contract`               | inline PR title and source-branch shell check          |
| `compose-validation`              | `scripts/validation/validate-docker-compose.sh`        |
| `compose-all-profiles-validation` | `validate-docker-compose.sh` with all governed profiles |
| `infrastructure-hardening`        | `scripts/hardening/check-all-hardening.sh`             |
| `template-security-baseline`      | `scripts/validation/check-template-security-baseline.sh` |
| `quickwin-baseline`               | `scripts/validation/check-quickwin-baseline.sh`        |
| `pre-commit`                      | pre-commit hook suite with project-specific skips      |
| `frontend-quality`                | Storybook Next.js lint, typecheck, app build, and static build |
| `storybook-coverage`              | Storybook Next.js coverage via npm script              |
| `zizmor`                          | GitHub Actions security scan with SARIF upload; GitHub-only gate |

`zizmor` is intentionally GitHub-only because its gate uploads SARIF with
GitHub security permissions. Do not duplicate it inside the local pre-commit
runner.

### Non-Gating GitHub Automation

| Workflow                 | Purpose                    |
| ------------------------ | -------------------------- |
| `greetings.yml`          | welcome new contributors   |
| `stale.yml`              | manage stale issues and PRs |
| `pr-labeler.yml`         | apply PR labels            |
| `generate-changelog.yml` | generate release changelog |

**Coupling constraint:** when adding, removing, or renaming a required job in
`ci-quality.yml`, update all three places together:

1. `required_jobs` in `scripts/validation/check-repo-contracts.sh`
2. `.github/rulesets/main-protection.md` Required Status Checks
3. this section's Required Quality Gates table

## Related Documents

- `docs/00.agent-governance/rules/git-workflow.md`
- `docs/00.agent-governance/rules/quality-standards.md`
- `docs/00.agent-governance/rules/standards.md`
- `docs/00.agent-governance/rules/bootstrap.md`
- `docs/00.agent-governance/providers/agents-md.md`
- `docs/00.agent-governance/providers/claude.md`
- `docs/00.agent-governance/providers/gemini.md`
- `docs/00.agent-governance/providers/codex.md`
- `docs/00.agent-governance/memory/progress.md`
- `docs/00.agent-governance/memory/github-ci-contract-audit.md`
- `docs/05.operations/runbooks/release-management.md`

## References

- <https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets>
- <https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions>
