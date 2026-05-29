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

`ci-quality.yml` 워크플로우는 두 가지 범주의 잡을 정의한다.

### 로컬 스크립트 기반 QA 게이트 (required status checks)

아래 잡은 로컬에서도 실행 가능한 스크립트를 실행하며, `check-repo-contracts.sh`의
`required_jobs` 목록에 포함되어야 한다:

| Job ID                            | Script                                                         |
| --------------------------------- | -------------------------------------------------------------- |
| `docs-traceability`               | `scripts/validation/check-doc-traceability.sh`                 |
| `repo-contracts`                  | `scripts/validation/check-repo-contracts.sh`                   |
| `git-flow-contract`               | 인라인 git log 검사                                            |
| `compose-validation`              | `scripts/validation/validate-docker-compose.sh`                |
| `compose-all-profiles-validation` | `scripts/validation/validate-docker-compose.sh` (all profiles) |
| `infrastructure-hardening`        | `scripts/hardening/check-all-hardening.sh`                     |
| `template-security-baseline`      | `scripts/validation/check-template-security-baseline.sh`       |
| `quickwin-baseline`               | `scripts/validation/check-quickwin-baseline.sh`                |
| `pre-commit`                      | pre-commit 훅 스위트                                           |
| `frontend-quality`                | frontend lint/typecheck/build                                  |
| `zizmor`                          | GitHub Actions 보안 스캐너 (로컬 동급 없음)                    |
| `storybook-coverage`              | `scripts/validation/check-storybook-contract.sh`               |

### GitHub 네이티브 자동화 (QA 게이트 아님, required check 아님)

| Workflow                 | Purpose               |
| ------------------------ | --------------------- |
| `greetings.yml`          | 신규 기여자 환영      |
| `stale.yml`              | 오래된 이슈/PR 관리   |
| `pr-labeler.yml`         | PR 자동 레이블        |
| `generate-changelog.yml` | 릴리스 변경 로그 생성 |

**커플링 제약:** `ci-quality.yml`에 새 잡을 추가할 때는 다음 세 곳을 동시에 업데이트해야 한다:

1. `scripts/validation/check-repo-contracts.sh`의 `required_jobs`
2. `.github/rulesets/main-protection.md`의 Required Status Checks 목록
3. 이 섹션의 테이블

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
