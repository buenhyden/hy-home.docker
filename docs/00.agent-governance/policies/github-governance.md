---
profile_id: governance-policy
layer: agentic
---

# GitHub Governance Policy

Normative policy baseline aligning agent behavior with GitHub repository operations.
Repo-local stricter rules always override this document; never weaken them on the basis of this policy.

## 1. Repository Protection Contract

- Agents must treat `main` as a protected branch: no direct pushes, no force pushes, no bypass of required checks.
- This is an agent behavior contract, not evidence of applied GitHub settings.
  Remote control-plane state remains `unverified` until it is authenticated and
  read back for the named repository.
- "No exceptions" is mandatory agent behavior even when GitHub admin enforcement or repository rulesets do not fully enforce the same boundary.
- Remote branch protection and ruleset state must be authenticated and read
  back before claiming enforcement. The tracked desired-state proposal lives
  in `.github/rulesets/main-protection.md`; tracked files do not prove applied
  control-plane state.
- If remote enforcement is absent or unknown, agents must still follow protected-branch discipline locally and report the remote enforcement state as blocked or unverified.
- Required status checks listed in `.github/rulesets/main-protection.md` define
  the local desired contract. Agents must not declare a PR ready to merge
  without separately verified remote checks, or must explicitly report that
  remote verification is unavailable.
- CODEOWNERS-triggered reviews are mandatory. If a changed path is owned by a CODEOWNERS entry, that review must be obtained before merge — agents must note this requirement when completing PR review tasks.

## 2. Pull Request and Review Contract

- A PR is complete only when: (a) all required status checks pass, (b) all required code reviews are approved, (c) no unresolved BLOCK-severity findings remain.
- Draft/WIP PRs are allowed for collaboration, but they must not be treated as merge-ready and must list remaining work in the PR template.
- Agents must not self-approve or bypass required reviewers.
- When agents propose changes, they must list which CODEOWNERS paths are touched and which review gates apply.
- Git history is the recovery mechanism. A current Task may name a temporary
  recovery commit, but must not turn a branch tip, expected SHA, checksum, or
  commit census into a standing merge Gate.

## 3. Merge and Branch Discipline

- Delete a feature branch only after its approved change is reachable from the
  delivered protected branch and its linked worktree is clean.
- Long-lived branches other than `main` require explicit user authorization.
- Do not rewrite a current Task's named recovery commit before integration.
  History cleanup beyond the completed feature branch requires explicit
  authorization.
- Agents must never modify another agent's in-progress branch without explicit coordination.

## 4. GitHub Actions Security Contract

- Workflows must use least-privilege `GITHUB_TOKEN` — request only the permissions the job actually needs.
- Prefer OIDC-based cloud credentials over long-lived secrets stored as repository secrets. When proposing or reviewing workflow changes, flag any use of long-lived cloud secrets as a WARN finding.
- Pin actions to a specific commit SHA or a digest-verified tag, not a floating branch or `@latest`.
- `.github/workflow-contract.yml` records the locally verified manifest URL,
  retrieval date, runtime, approved consumers, and security disposition for
  every direct external Action. The focused checker rejects unregistered
  Actions and Node 20 runtime evidence.
- Secrets must never appear in log output (`echo $SECRET`, `run: env`, etc.). Flag any such pattern as BLOCK.
- Untrusted input into `$GITHUB_ENV`, `$GITHUB_OUTPUT`, or `run:` interpolation is a security injection risk — flag as BLOCK.
- Reusable workflows called from external repositories must be pinned and reviewed before use.

## 5. Execution Boundary (Local vs Remote)

- **Anti-Duplication**: Do not execute heavy workloads (e.g., Zizmor, Storybook ESLint) redundantly across both local `pre-commit` and dedicated GitHub Action jobs.
- **Local Responsibility**: Fail-fast static analysis (formatting, simple
  linting, the public `changed` profile for pre-commit, and the public `full`
  profile for pre-push). Agents must not invoke `pre-commit run` directly.
  An approved final QA all-files run uses only
  `scripts/validation/run-agent-precommit-all-files.sh` in an initially clean
  linked worktree with co-located Task evidence and minimal allowed prefixes.
  Its evidence covers only Git-visible, non-ignored repository paths; it does
  not observe ignored/outside writes or provide process/filesystem sandboxing.
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

### 5.1 Tracked Workflow Definition Boundary

A tracked workflow file is a local repository definition, not evidence that a
remote schedule, manual dispatch, job, or required check ran. Agents may author
and validate an approved workflow definition locally, but must not dispatch it,
push it, enable it remotely, or change GitHub checks, rulesets, branch
protection, environments, deployments, or releases without separate explicit
approval for that repository and remote surface.

`.github/workflows/document-corpus-lifecycle.yml` is read-only quality
automation. Its scheduled and manual job blocks lifecycle contract and promoted
manifest failures while reporting bounded full-corpus debt and duplicate
candidates advisory-only. It does not upload corpus or snapshot payloads, add a
required status check, or replace the existing `repo-contracts` pull-request
and push consumer. Local validation of this tracked definition must be reported
separately from unverified remote execution state.

### 5.2 Evidence Boundary by Change Type

Agents must align local checks, CI-only gates, and skipped-check rationale with
the QA scope matrix. For PR-related work, the completion summary or task
evidence must state:

| Change Type | Required Local Evidence | CI-Only Evidence | Required Skip Rationale |
| --- | --- | --- | --- |
| Docs or governance docs | Diff hygiene, doc implementation alignment, repo contracts, doc traceability, provider sync when provider docs changed | Required docs/repo contract jobs | Domain tests are N/A for docs-only changes. |
| Historical-file cleanup | Diff hygiene, stale active-reference scan, and minimal metadata/link checks | Required docs/repo contract jobs | Domain tests and runtime checks are N/A unless behavior/config changed. |
| Hook, script, or validator | Targeted command output plus repo contracts | Required quality/security jobs | GitHub-only permissions, SARIF upload, or protected remote state if not locally runnable. |
| Runtime or Docker config | Compose/hardening/local smoke checks when approved | Compose and hardening jobs | Live mutation skipped without approval. |
| GitHub workflow/protection | Static review and local contract checks | GitHub Actions and branch-protection verification | Any remote state not verified must be reported as unverified, not done. |

No task is complete by citing a CI-only gate alone when a cheap local check is
available, and no local-only check replaces required protected-branch gates.

## 6. Local Instruction Authority

- This repository does not adopt a GitHub-native instruction hierarchy for agent execution.
- Instruction authority lives in repo-local assets only:
  - root shims: `AGENTS.md`, `CLAUDE.md`
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

`ci-quality.yml` defines exactly two required quality jobs:
`validation-changed` for pull requests and `validation-full` for push/manual
events. `.github/workflow-contract.yml` owns the six-suite composition,
changed-path impact rules, gate DAG, admitted environment keys, and direct
external Actions. Each required job contains one static public profile command;
the focused checker retains trigger, permission, timeout, Action, and
workflow-shape checks.
Archive/tombstone, metadata, lifecycle, runtime-version, and repository-contract
checks remain atomic leaves behind the two public profiles. Their composition is
owned by `.github/workflow-contract.yml`; none is a separate required GitHub job.

### Required Quality Gates

| Job ID | Public profile | Event |
| :--- | :--- | :--- |
| `validation-changed` | `changed` | pull request |
| `validation-full` | `full` | push or manual dispatch |

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
| `document-corpus-lifecycle.yml` | report read-only scheduled/manual lifecycle debt and duplicate candidates |
| `tech-stack-version-sync.yml` | check curated version-registry drift for governed Compose/version changes |

Agent all-files execution remains limited to the separately approved controlled
wrapper; neither required profile grants Agent authorization.

**Coupling constraint:** when adding, removing, or renaming a required job,
update all three tracked surfaces together:

1. `.github/workflow-contract.yml`
2. `.github/workflows/ci-quality.yml`
3. `.github/rulesets/main-protection.md` Required Status Checks

Then update this explanatory table. Local validation does not prove that any
of these checks ran remotely or that GitHub applies the proposed protection.

## Related Documents

- `docs/00.agent-governance/policies/git-workflow.md`
- `docs/00.agent-governance/policies/quality-standards.md`
- `docs/00.agent-governance/policies/standards.md`
- `docs/00.agent-governance/policies/bootstrap.md`
- `docs/00.agent-governance/providers/README.md`
- `docs/00.agent-governance/providers/claude.md`
- `docs/00.agent-governance/providers/codex.md`
- `.github/INDEX.md`
- `.github/rulesets/main-protection.md`
- `docs/05.operations/catalog/00-workspace/0009-release-management/runbook.md`

## References

- <https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets>
- <https://docs.github.com/en/actions/reference/security/secure-use>
- <https://docs.github.com/en/actions/how-tos/monitor-workflows>
- <https://github.com/zizmorcore/zizmor/releases/tag/v1.28.0>
