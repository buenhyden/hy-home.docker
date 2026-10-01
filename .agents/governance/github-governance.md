---
title: "GitHub Governance Policy"
version: "1.2.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
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
- CODEOWNERS-triggered reviews are mandatory wherever remote protection enforces them. Agents must read the enforced state rather than assume it: when `require_code_owner_reviews` is enabled, an owned path's review must be obtained before merge; when it is disabled, `.github/CODEOWNERS` remains the ownership and review-routing record and no longer gates merges. Report which of the two applies; never record a review that protection did not require and no person gave.

## 2. Pull Request and Review Contract

Issues provide intake, coordination, and branch links. The current Task owns
approval, evidence, and lifecycle state; closing a stale Issue does not
transition a Task. Projects is the preferred future coordination option and
Linear is an alternative; neither is adopted here and neither receives a sync
job. A remote Issue, tag, or release mutation requires approval naming the exact
target and action.

- A PR is complete only when: (a) all required status checks pass, (b) all required code reviews are approved, (c) no unresolved BLOCK-severity findings remain.
- Draft/WIP PRs are allowed for collaboration; section 3 owns what that means for merge readiness.
- Agents must not self-approve or bypass required reviewers.
- When agents propose changes, they must list which CODEOWNERS paths are touched and which review gates apply.
- Git history is the recovery mechanism. A current Task may name a temporary
  recovery commit, but must not turn a branch tip, expected SHA, checksum, or
  commit census into a standing merge Gate.

## 3. Merge and Branch Discipline

This section is the single owner of merge and branch-lifecycle rules. Both the
Git workflow policy and `.github/rulesets/main-protection.md` defer here; the
ruleset file records the observed remote state and issues no rule of its own.

- Deliver every change to `main` through a pull request. Agents do not push to
  `main` directly, do not force-push it, and do not bypass a required check,
  regardless of how few reviews protection currently requires.
- Delete a branch only when all of the following hold: its approved change and
  every referenced recovery commit are reachable from the delivered protected
  branch, its linked worktree is clean, and the owner has approved the deletion.
- Long-lived branches other than `main` require explicit user authorization.
- Do not rewrite a current Task's named recovery commit before integration. Use
  a merge commit or fast-forward rather than rewriting referenced objects.
  History cleanup beyond the completed feature branch requires explicit
  authorization.
- Draft or WIP pull requests are never merge-ready. They must list their
  remaining work in the PR template.
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
  linting, and explicit focused public-gate runs when the change needs them).
  Routine commit and push hooks do not invoke public profiles. Agents must not
  invoke `pre-commit run` directly.
  An approved final QA all-files run uses only
  `scripts/validation/run-agent-precommit-all-files.sh` in an initially clean
  linked worktree with co-located Task evidence and minimal allowed prefixes.
  Its evidence covers only Git-visible, non-ignored repository paths; it does
  not observe ignored/outside writes or provide process/filesystem sandboxing.
- **GitHub Responsibility**: Ultimate SSoT gates, E2E tests, SARIF generation, and workflows requiring secrets.
- **Implementation**: The CI pre-commit runner owns its skip list. It skips
  checks already owned by dedicated gate leaves. The public validation hooks
  were removed, so no skip value for them remains. Callers must not supply
  `SKIP` or introduce a second orchestration path. See
  [the shared execution boundary](quality-standards.md#4-execution-boundary).

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

### 5.2 Evidence Boundary by Change Type

Use the [shared change-type verification matrix](quality-standards.md#5-change-type-verification-matrix)
for local checks, selected public suites, and skipped-check rationale. This
policy does not define a second matrix or additional provider-specific gates.

For PR-related work, record local command results separately from hosted run
IDs, head commits, job conclusions, required reviews, and observed protection
settings. Missing tools, unexecuted checks, and unavailable remote observations
must remain explicitly blocked, skipped with a reason, or unverified; they are
not passing evidence.

No task is complete by citing a CI-only gate alone when a cheap local check is
available, and no local-only check replaces required protected-branch gates.

## 6. Local Instruction Authority

- This repository does not adopt a GitHub-native instruction hierarchy for agent execution.
- Instruction authority lives in repo-local assets only:
  - root shims: `AGENTS.md`, `CLAUDE.md`
  - governance SSoT: `.agents/`
  - runtime controls: `.claude/settings.json`, `.claude/hooks/`, `.claude/agents/`, `.claude/skills/`
  - Codex runtime hooks: `.codex/hooks.json`
- GitHub is used here for repository protection, PR workflow, and Actions execution; it is not the canonical home of agent instruction policy.
- Any future GitHub-native instruction file must be treated as out-of-scope until the repository governance explicitly adopts it.

## 7. Completion Gate (GitHub-Specific)

Before an agent declares any PR-related task complete, it must confirm:

1. All required status checks are green (or note which are pending and why), and remote branch protection state is verified or explicitly reported as unverified.
2. All required reviews are approved (or note which are outstanding and who owns them).
3. No BLOCK-severity findings remain from code review or security audit.
4. CODEOWNERS-triggered reviewers have been notified if paths are owned and remote protection enforces owner review; when it does not, state that instead of claiming a review.
5. No secrets, long-lived credentials, or unpinned action references were introduced.

If any gate is unmet, the task status is "blocked" not "done."

## 8. CI/CD Job Taxonomy

`ci-quality.yml` defines four jobs with distinct event and permission boundaries.
The [canonical phase matrix](quality-standards.md#canonical-delivery-phase-matrix)
owns when each check runs. `.github/workflow-contract.yml` owns the six-suite
composition, changed-path impact rules, gate DAG, admitted environment keys,
and pinned Actions; the focused checker enforces triggers, permissions, timeouts,
steps and dependencies. Archive, metadata, lifecycle and repository-contract
checks remain leaves behind the two public profiles, not separate required
status contexts.

### Quality Jobs and Required Status

| Job ID | Route | Event |
| :--- | :--- | :--- |
| `validation-changed` | `changed`, including git-flow on title edits | opened, synchronized, reopened and edited PRs to main |
| `validation-full` | `full` | manual dispatch |
| `main-security` | registered Zizmor adapter and SARIF upload | main push |
| `update-main-current` | leased channel tag update after successful `main-security` | main push |

Only `validation-changed` is the PR required status. A title edit reruns the
same changed profile: the edited run can cancel a synchronize run, so a
narrower success would not prove the candidate revision. The protected-branch settings remain a remote
fact that must be read back before merge. Main security observes the merged
SHA; it does not replace pre-merge protection. The tag job alone receives
`contents: write`; quality jobs remain read-only except the SARIF permission.
Release tags remain governed by the release procedure. A failed main-security
job must leave the tag job skipped, and a stale or rejected tag push must leave
the existing pointer intact.

### Non-Gating GitHub Automation

| Workflow                 | Purpose                    |
| ------------------------ | -------------------------- |
| `greetings.yml`          | welcome new contributors   |
| `stale.yml`              | manage stale issues and PRs |
| `pr-labeler.yml`         | apply PR labels            |
| `generate-changelog.yml` | verify that an existing release tag has a CHANGELOG entry |

Agent all-files execution remains limited to the separately approved controlled
wrapper; neither required profile grants Agent authorization.

**Coupling constraint:** when changing quality jobs or required status identity,
update all three tracked surfaces together:

1. `.github/workflow-contract.yml`
2. `.github/workflows/ci-quality.yml`
3. `.github/rulesets/main-protection.md` Required Status Checks

Then update this explanatory table. Local validation does not prove that any
of these checks ran remotely or that GitHub applies the proposed protection.

## Related Documents

- `.agents/governance/git-workflow.md`
- `.agents/governance/quality-standards.md`
- `.agents/governance/standards.md`
- `.agents/governance/bootstrap.md`
- `.agents/governance/providers/README.md`
- `.claude/provider.md`
- `.codex/provider.md`
- `.github/repository-surface.md`
- `.github/rulesets/main-protection.md`
- `docs/05.operations/runbooks/0009-release-management.md`

## References

- <https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets>
- <https://docs.github.com/en/actions/reference/security/secure-use>
- <https://docs.github.com/en/actions/how-tos/monitor-workflows>
- <https://github.com/zizmorcore/zizmor/releases/tag/v1.28.0>
