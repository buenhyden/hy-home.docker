---
title: "GitHub Governance Policy"
version: "1.7.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-29"
---

# GitHub Governance Policy

## Overview

Normative policy baseline aligning agent behavior with GitHub repository operations.
Repo-local stricter rules always override this document; never weaken them on the basis of this policy.

## Scope

Repository protection, pull requests, hosted workflows, and separately authorized remote actions.

## Rules

### 1. Repository Protection Contract

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

### 2. Pull Request and Review Contract

Issues provide intake, coordination, and branch links. The current Task owns
approval, evidence, and lifecycle state; closing a stale Issue does not
transition a Task. This repository uses no GitHub Project: with one developer,
Issues cover intake and priority and Tasks cover execution, so a Project
would only repeat Task state. Adding one needs the owner's approval naming
it, and its fields stay coordination data, never Task execution authority.
Keep Issue intake and priority plus Spec/Task links, without copying their
full bodies or bidirectional state synchronization. A remote Issue, tag, or release mutation requires approval naming the exact
target and action.

- A PR is complete only when: (a) all required status checks pass, (b) all required code reviews are approved, (c) no unresolved BLOCK-severity findings remain.
- Draft/WIP PRs are allowed for collaboration; section 3 owns what that means for merge readiness.
- Agents must not self-approve or bypass required reviewers.
- This repository has one developer and no second reviewer. That risk is
  handled by the required `candidate-quality` check, a review of the final diff
  in a fresh context separate from the one that wrote it, and the owner's own
  merge. The review path calls no AI-agent API: no workflow, hook, or script
  sends the diff to a model provider, and an agent review runs only inside the
  developer's own interactive session. One person's review is never recorded as
  two independent approvals, and an automated check, App, or signature does not
  stand in for the owner's acceptance.
- When agents propose changes, they must list which CODEOWNERS paths are touched and which review gates apply.
- Git history is the recovery mechanism. A current Task may name a temporary
  recovery commit, but must not turn a branch tip, expected SHA, checksum, or
  commit census into a standing merge Gate.

### 3. Merge and Branch Discipline

This section is the single owner of merge and branch-lifecycle rules. Both the
Git workflow policy and `.github/rulesets/main-protection.md` defer here; the
ruleset file records the observed remote state and issues no rule of its own.

- Deliver every change to `main` through a pull request. Agents do not push to
  `main` directly, do not force-push it, and do not bypass a required check,
  regardless of how few reviews protection currently requires.
- Delete a branch only when all of the following hold: its approved change and
  every referenced recovery commit are reachable from the delivered protected
  branch, its linked worktree is clean, and the current request or the owner
  asks for the deletion.
- Long-lived branches other than `main` require explicit user authorization.
- Do not rewrite a current Task's named recovery commit before integration. Use
  a merge commit or fast-forward rather than rewriting referenced objects.
  History cleanup beyond the completed feature branch requires explicit
  authorization.
- Draft or WIP pull requests are never merge-ready. They must list their
  remaining work in the PR template.
- Agents must never modify another agent's in-progress branch without explicit coordination.

### 4. GitHub Actions Security Contract

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

### 5. Execution Boundary (Local vs Remote)

- **Local**: explicit formatting, focused RED/GREEN, message validation and
  read-only diagnostic checks. The shared
  [execution boundary](quality-standards.md#4-execution-boundary) owns their
  selection and prohibits direct Agent pre-commit/all-files bypass.
- **Remote PR**: the public changed entrypoint owns aggregate candidate QA once.
  Feature push does not repeat it; required selection is inside an always-present
  PR workflow rather than path-skipping its required check.
- **Main**: merged-revision security/SARIF is a distinct observation, not a
  second candidate run. The sole manual release producer runs only once the user
  names its exact version and trusted main revision.

#### 5.0 Approved Remote Mutation Protocol

When the user approves remote GitHub mutation, agents must still bind the action
to a concrete repository and remote surface before changing state. Task evidence
must include the approval source, target repository, target setting or object,
command class, before-state evidence, after-state evidence, and rollback or
recovery path. Merge only a pull request the current request asks to merge,
after its required checks pass. Do not bypass required checks, weaken
protected-branch rules, or expose GitHub secrets unless the user names that
concrete action and target.

Read-only remote checks may be recorded as verification evidence. Remote state
that was approved but not changed must be reported as verified-only, not as a
mutation.

#### 5.1 Tracked Workflow Definition Boundary

A tracked workflow file is a local repository definition, not evidence that a
remote schedule, manual dispatch, job, or required check ran. Agents may author
and validate an approved workflow definition locally and push it with the
request's branch and pull request, but must not dispatch it, enable it
remotely, or change GitHub checks, rulesets, branch protection, environments,
deployments, or releases until the user names that repository and remote
surface.

#### 5.2 Evidence Boundary by Change Type

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

#### 5.3 QA Definition Trust and Amendment

A change to a QA definition ties the current owner's actual acceptance to
that diff and revision, and records in the Task the source and revision of
the trusted base definition it was compared with. The QA definitions are
`.github/workflows/`, `.github/workflow-contract.yml`, `scripts/lib/gate/`,
`scripts/validation/ci_gate_runner.py`, `scripts/validation/run-ci-gate.py`,
the QA dependency pins, and `.pre-commit-config.yaml`. An ordinary documentation change does not
add this approval step, and an explicit approval already given for the same
scope is not requested again.

A success from a candidate running its own workflow, controller, and
configuration never shows that the QA definition is unchanged or approved.
The current `candidate-quality` is evidence of the candidate's run, not of
a trusted base runner or of an independent approval of a definition change.
Enforcing this boundary remotely needs a verification definition the
candidate cannot modify, plus protection settings that consume its result,
each separately approved, applied, and read back. A local revision of this
policy is not an observation of such remote enforcement. Implementing it
never checks out or runs candidate code in a privileged
`pull_request_target` runner, and never creates a new App or credential
implicitly.

### 6. Local Instruction Authority

- This repository does not adopt a GitHub-native instruction hierarchy for agent execution.
- Instruction authority lives in repo-local assets only:
  - root shims: `AGENTS.md`, `CLAUDE.md`
  - governance SSoT: `.agents/`
  - runtime controls: `.claude/settings.json`, `.claude/hooks/`, `.claude/agents/`, `.claude/skills/`
  - Codex runtime hooks: `.codex/hooks.json`
- GitHub is used here for repository protection, PR workflow, and Actions execution; it is not the canonical home of agent instruction policy.
- Any future GitHub-native instruction file must be treated as out-of-scope until the repository governance explicitly adopts it.

### 8. CI/CD Job Taxonomy

The [canonical phase matrix](quality-standards.md#canonical-delivery-phase-matrix)
owns stage responsibility. `.github/workflow-contract.yml` owns exact job
identities, event/permission boundaries, selected prerequisites, gate DAG,
change impact and immutable Action provenance. The generic focused checker
compares workflow definitions to that one typed source instead of maintaining
another copied job/action census.

The PR candidate invokes `changed` once with read-only permissions and validated
base/head context. No feature-push, title-edit or main full-profile rerun is
registered. The separate main security job writes only its SARIF result. Release
publication is a main-only manual workflow, with `contents: write` restricted to
its producer. It creates a SemVer tag and complete draft assets before publish;
there is no second tag-push or moving-channel producer.

Greetings, stale-thread handling and PR labels are non-QA coordination jobs.
Their pin, permission and event safety remain checked; they do not own candidate
acceptance. External automatic security integrations require their own actual
remote observation and are not disabled by editing tracked YAML.

When job identity or required context changes, update workflow-contract,
workflow YAML and tracked protection target together, then observe the remote
state separately. A proposed required context is not effective protection.
Never introduce an administrative bypass when source and remote state differ.

#### Issues and Projects

Issue forms collect problem/request, priority and optional contract/execution
links. Specs retain AC/contracts; Tasks retain actual commands, results,
acceptance and authorization. A Project may show owner, priority and linked
Issue/PR state as a view; it must not overwrite document lifecycle or duplicate
an execution ledger. No Project exists today (§2), and adding one or its
automation permission needs the owner's approval. GitHub's repository token cannot access Projects; do
not add an App/PAT just to mirror Task state. See
[Project automation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/automating-projects-using-actions).

### References

- <https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets>
- <https://docs.github.com/en/actions/reference/security/secure-use>
- <https://docs.github.com/en/actions/how-tos/monitor-workflows>
- <https://github.com/zizmorcore/zizmor/releases/tag/v1.28.0>

## Exceptions

No exception is granted here; a separately authorized operation follows [Approval boundaries](approval-boundaries.md).

## Verification

### 7. Completion Gate (GitHub-Specific)

Before an agent declares any PR-related task complete, it must confirm:

1. All required status checks are green (or note which are pending and why), and remote branch protection state is verified or explicitly reported as unverified.
2. All required reviews are approved (or note which are outstanding and who owns them).
3. No BLOCK-severity findings remain from code review or security audit.
4. CODEOWNERS-triggered reviewers have been notified if paths are owned and remote protection enforces owner review; when it does not, state that instead of claiming a review.
5. No secrets, long-lived credentials, or unpinned action references were introduced.

If any gate is unmet, the task status is "blocked" not "done."

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
- `docs/05.operations/runbooks/10-platform-and-backup/0009-release-management.md`
