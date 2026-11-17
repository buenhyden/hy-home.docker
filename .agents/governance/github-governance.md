---
title: "GitHub Governance Policy"
version: "1.11.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
---

# GitHub Governance Policy

## Purpose and Scope

### Objective

Normative policy baseline aligning agent behavior with GitHub repository operations.
A stricter rule in another canonical governance owner prevails over this document.

#### Authority

This policy is the canonical owner of repository protection, pull requests, hosted workflows, and remote actions under [bootstrap precedence](bootstrap.md#authority-and-precedence).

### Applies To

Repository protection, pull requests, hosted workflows, and separately authorized remote actions.

#### Exclusions

None: this document states no exclusion.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| GITHUB-GOVERNANCE-R1 | Always | Required: treat `main` as a protected branch with no direct pushes, no force pushes and no bypass of required checks, even where GitHub does not fully enforce it | none | none |
| GITHUB-GOVERNANCE-R2 | Always | Required: report remote control-plane state as `unverified` until authenticated and read back for the named repository | none | `.github/rulesets/main-protection.md` dated authenticated read-backs |
| GITHUB-GOVERNANCE-R3 | Claiming remote enforcement | Forbidden: claiming enforcement before authenticated read-back of branch protection and rulesets | none | `.github/rulesets/main-protection.md` dated authenticated read-backs |
| GITHUB-GOVERNANCE-R4 | Remote enforcement absent or unknown | Required: follow protected-branch discipline locally and report remote enforcement as blocked or unverified | none | none |
| GITHUB-GOVERNANCE-R5 | PR readiness | Forbidden: declaring a PR ready to merge without separately verified remote checks, unless remote verification is reported unavailable | none | none |
| GITHUB-GOVERNANCE-R6 | `require_code_owner_reviews` enabled | Required: obtain the owned path's review before merge | none | none |
| GITHUB-GOVERNANCE-R7 | Any CODEOWNERS-triggered review | Required: read the enforced state rather than assume it and report which applies | none | none |
| GITHUB-GOVERNANCE-R8 | Any CODEOWNERS-triggered review | Forbidden: recording a review that protection did not require and no person gave | none | none |
| GITHUB-GOVERNANCE-R9 | Issue closed by hand or by closing keyword | Forbidden: treating it as a Task transition or acceptance record | none | none |
| GITHUB-GOVERNANCE-R10 | Adding a GitHub Project or its automation permission | Required: owner approval naming it; its fields stay coordination data and never Task execution authority | none | none |
| GITHUB-GOVERNANCE-R11 | Issue intake | Forbidden: copying Spec/Task full bodies or bidirectional state synchronization | none | none |
| GITHUB-GOVERNANCE-R12 | Remote Issue, tag or release mutation | Required: approval naming the exact target and action | none | none |
| GITHUB-GOVERNANCE-R13 | Pull request completion | Required: all required status checks pass, all required reviews approved and no unresolved `blocker` findings | none | Task Criterion Acceptance |
| GITHUB-GOVERNANCE-R14 | Draft/WIP PR | Allowed: Draft/WIP PRs for collaboration; section 3 owns merge readiness | none | none |
| GITHUB-GOVERNANCE-R15 | Review | Forbidden: self-approval or bypassing required reviewers | none | none |
| GITHUB-GOVERNANCE-R16 | One-developer repository | Required: classify risk per Review risk read with the change-type verification matrix and protected surfaces | none | none |
| GITHUB-GOVERNANCE-R17 | One-developer repository | Required: the `candidate-quality` check runs the static and contract checks | `candidate-quality` check | none |
| GITHUB-GOVERNANCE-R18 | High-risk final diff | Required: review in a fresh context separate from the writer, against the diff review checklist | manual | none |
| GITHUB-GOVERNANCE-R19 | Low-risk diff | Required: close with the author check defined by the Review risk policy | none | none |
| GITHUB-GOVERNANCE-R20 | Criterion acceptance | Required: the owner accepts each criterion explicitly in the Task's Criterion Acceptance; a merge is not acceptance | manual | Task Criterion Acceptance |
| GITHUB-GOVERNANCE-R21 | Review path | Forbidden: calling a model-inference API | none | none |
| GITHUB-GOVERNANCE-R22 | Review records | Forbidden: recording one person's review as two independent approvals | none | none |
| GITHUB-GOVERNANCE-R23 | Owner acceptance | Forbidden: letting an automated check, App or signature stand in for the owner's acceptance | none | none |
| GITHUB-GOVERNANCE-R24 | Acceptance or ADR decision | Forbidden: requiring a signed commit or tag | none | none |
| GITHUB-GOVERNANCE-R25 | Agent proposes changes | Required: list the CODEOWNERS paths touched and the review gates that apply | none | none |
| GITHUB-GOVERNANCE-R26 | Current Task | Allowed: naming a temporary recovery commit | none | none |
| GITHUB-GOVERNANCE-R27 | Current Task | Forbidden: turning a branch tip, expected SHA, checksum or commit census into a standing merge Gate | none | none |
| GITHUB-GOVERNANCE-R28 | Change delivered to `main` | Required: deliver through a pull request | none | none |
| GITHUB-GOVERNANCE-R29 | `main` | Forbidden: pushing directly, force-pushing or bypassing a required check regardless of required review count | none | none |
| GITHUB-GOVERNANCE-R30 | Branch deletion | Required: delete only when the change and recovery commits are reachable from the delivered branch, the linked worktree is clean and the request or owner asks | none | none |
| GITHUB-GOVERNANCE-R31 | Long-lived branch other than `main` | Required: explicit user authorization | none | none |
| GITHUB-GOVERNANCE-R32 | Current Task's named recovery commit | Forbidden: rewriting it before integration; use a merge commit or fast-forward | none | none |
| GITHUB-GOVERNANCE-R33 | History cleanup beyond the completed feature branch | Required: explicit authorization | none | none |
| GITHUB-GOVERNANCE-R34 | Renovate PR | Required: follow the same protocol; bring the branch up to date by running Renovate, not GitHub update-branch | manual | none |
| GITHUB-GOVERNANCE-R35 | Renovate PRs | Required: merge one dependency PR at a time, most security-relevant first | none | none |
| GITHUB-GOVERNANCE-R36 | Renovate PR | Forbidden: closing it by hand | none | none |
| GITHUB-GOVERNANCE-R37 | Merged image change | Required: the HOME recreate gets its own approval | none | none |
| GITHUB-GOVERNANCE-R38 | Draft or WIP PR | Forbidden: merging it; list remaining work in the PR template | none | none |
| GITHUB-GOVERNANCE-R39 | Another agent's in-progress branch | Forbidden: modifying it without explicit coordination | none | none |
| GITHUB-GOVERNANCE-R40 | Workflow authoring or review | Required: least-privilege `GITHUB_TOKEN` requesting only needed permissions | none | none |
| GITHUB-GOVERNANCE-R41 | Proposing or reviewing workflow changes | Required: prefer OIDC cloud credentials and flag long-lived cloud secrets as a `medium` finding | none | none |
| GITHUB-GOVERNANCE-R42 | Action references | Required: pin to a full commit SHA, not a tag, floating branch or `@latest` | `sha_pinning_required` repository setting | none |
| GITHUB-GOVERNANCE-R43 | Direct external Action | Required: record manifest URL, retrieval date, runtime, approved consumers and security disposition in `.github/workflow-contract.yml` | `scripts/lib/gate/github_workflow_contract.py` rejects unregistered Actions and runtimes other than `node24` or `composite` | `.github/workflow-contract.yml` |
| GITHUB-GOVERNANCE-R44 | Secret in log output | Forbidden: secrets in log output; raise a `blocker` finding | none | none |
| GITHUB-GOVERNANCE-R45 | Untrusted input | Forbidden: untrusted input into `$GITHUB_ENV`, `$GITHUB_OUTPUT` or `run:` interpolation; raise a `blocker` finding | none | none |
| GITHUB-GOVERNANCE-R46 | External reusable workflow | Required: pin and review before use | none | none |
| GITHUB-GOVERNANCE-R47 | Local checks | Required: explicit formatting, focused RED/GREEN, message validation and read-only diagnostic checks, selected by the shared execution boundary | none | none |
| GITHUB-GOVERNANCE-R48 | Local checks | Forbidden: direct Agent pre-commit/all-files bypass | none | none |
| GITHUB-GOVERNANCE-R49 | Remote PR | Required: the public changed entrypoint owns aggregate candidate QA once, with required selection inside an always-present PR workflow rather than path-skipping the required check | `candidate-quality` PR workflow | none |
| GITHUB-GOVERNANCE-R50 | Feature push | Forbidden: repeating aggregate candidate QA | none | none |
| GITHUB-GOVERNANCE-R51 | Main | Required: treat merged-revision security/SARIF as a distinct observation, not a second candidate run | none | none |
| GITHUB-GOVERNANCE-R52 | Manual release producer | Required: run only once the user names its exact version and trusted main revision | none | none |
| GITHUB-GOVERNANCE-R53 | User approves remote GitHub mutation | Required: bind the action to a concrete repository and remote surface | none | none |
| GITHUB-GOVERNANCE-R54 | User approves remote GitHub mutation | Required: record approval source, target repository, setting or object, command class, before/after state and rollback in Task evidence | manual | Task evidence |
| GITHUB-GOVERNANCE-R55 | Merge | Required: merge only a PR the current request asks to merge, after its required checks pass | none | none |
| GITHUB-GOVERNANCE-R56 | Remote mutation | Forbidden: bypassing required checks, weakening protected-branch rules or exposing GitHub secrets unless the user names that action and target | none | none |
| GITHUB-GOVERNANCE-R57 | Read-only remote checks | Allowed: record them as verification evidence | none | none |
| GITHUB-GOVERNANCE-R58 | Remote state approved but not changed | Required: report as verified-only, not as a mutation | none | none |
| GITHUB-GOVERNANCE-R59 | Tracked workflow file | Allowed: author and validate an approved definition locally and push it with the request's branch and PR | none | none |
| GITHUB-GOVERNANCE-R60 | Tracked workflow file | Forbidden: dispatching it, enabling it remotely, or changing GitHub checks, rulesets, branch protection, environments, deployments or releases until the user names the repository and remote surface | none | none |
| GITHUB-GOVERNANCE-R61 | PR-related work | Required: use the shared change-type verification matrix | shared change-type verification matrix in `quality-standards.md` | none |
| GITHUB-GOVERNANCE-R62 | PR-related work | Required: record local command results separately from hosted run IDs, head commits, job conclusions, reviews and protection settings | none | Task record of local and hosted results |
| GITHUB-GOVERNANCE-R63 | Missing tool, unexecuted check or unavailable remote observation | Required: report as blocked, skipped with a reason, or unverified | none | none |
| GITHUB-GOVERNANCE-R64 | Task completion | Forbidden: citing a CI-only gate alone when a cheap local check is available | none | none |
| GITHUB-GOVERNANCE-R65 | Task completion | Forbidden: letting a local-only check replace required protected-branch gates | none | none |
| GITHUB-GOVERNANCE-R66 | Change to a QA definition | Required: tie the owner's actual acceptance to the diff and revision and record the trusted base definition's source and revision in the Task | manual | Task record of trusted base source and revision |
| GITHUB-GOVERNANCE-R67 | Ordinary documentation change | Allowed: no added QA-definition approval step | none | none |
| GITHUB-GOVERNANCE-R68 | Candidate runs its own workflow, controller and configuration | Forbidden: treating its success as proof that the QA definition is unchanged or approved | none | none |
| GITHUB-GOVERNANCE-R69 | Current `candidate-quality` | Forbidden: treating it as evidence of a trusted base runner or an independent approval of a definition change | none | none |
| GITHUB-GOVERNANCE-R70 | Remote enforcement of QA definition trust | Required: a verification definition the candidate cannot modify plus consuming protection settings, each separately approved, applied and read back | none | none |
| GITHUB-GOVERNANCE-R71 | Implementing QA definition trust | Forbidden: checking out or running candidate code in a privileged `pull_request_target` runner, or creating a new App or credential implicitly | none | none |
| GITHUB-GOVERNANCE-R72 | Always | Forbidden: adopting a GitHub-native instruction hierarchy for agent execution | none | none |
| GITHUB-GOVERNANCE-R73 | Always | Required: take instruction authority from repo-local assets only (root shims, `.agents/`, folder agent guides, authored adapters) | none | none |
| GITHUB-GOVERNANCE-R74 | Native runtime controls and generated projections | Forbidden: owning any instruction authority; they only consume it | none | none |
| GITHUB-GOVERNANCE-R75 | Future GitHub-native instruction file | Forbidden: treating it as in scope until governance explicitly adopts it | none | none |
| GITHUB-GOVERNANCE-R76 | PR candidate routing | Required: `candidate-quality` needs routing and every shard; accept a skipped document shard only after successful routing selects no leaves and the shard supplies no execution output; fail on missing, failed, cancelled or contradictory results | required `candidate-quality` aggregate | none |
| GITHUB-GOVERNANCE-R77 | CI/CD workflow set | Forbidden: registering a feature-push, title-edit or main full-profile rerun | none | none |
| GITHUB-GOVERNANCE-R78 | Release publication | Required: main-only manual workflow with `contents: write` restricted to its producer, creating a SemVer tag and complete draft assets before publish | none | none |
| GITHUB-GOVERNANCE-R79 | Release publication | Forbidden: a second tag-push or moving-channel producer | none | none |
| GITHUB-GOVERNANCE-R80 | Non-QA coordination jobs (greetings, stale threads, PR labels) | Required: keep their pin, permission and event safety checked | none | none |
| GITHUB-GOVERNANCE-R81 | Non-QA coordination jobs | Forbidden: owning candidate acceptance | none | none |
| GITHUB-GOVERNANCE-R82 | External automatic security integrations | Required: their own actual remote observation; editing tracked YAML does not disable them | none | none |
| GITHUB-GOVERNANCE-R83 | CI/CD job identity or required context changes | Required: update workflow-contract, workflow YAML and tracked protection target together, then observe remote state separately | none | Separate remote-state observation |
| GITHUB-GOVERNANCE-R84 | Source and remote state differ | Forbidden: introducing an administrative bypass | none | none |
| GITHUB-GOVERNANCE-R85 | Issue forms | Required: collect problem/request, priority and optional contract/execution links; Specs retain AC/contracts and Tasks retain commands, results, acceptance and authorization | none | none |
| GITHUB-GOVERNANCE-R86 | Project state mirroring | Forbidden: adding an App/PAT just to mirror Task state | none | none |

#### 1. Repository Protection Contract

- Agents must treat `main` as a protected branch: no direct pushes, no force pushes, no bypass of required checks.
- This is an agent behavior contract, not evidence of applied GitHub settings.
  Remote control-plane state remains `unverified` until it is authenticated and
  read back for the named repository.
- "No exceptions" is mandatory agent behavior even when GitHub admin enforcement or repository rulesets do not fully enforce the same boundary.
- Remote branch protection and ruleset state must be authenticated and read
  back before claiming enforcement. `.github/rulesets/main-protection.md`
  records the target settings and dated authenticated read-backs; tracked
  files do not prove applied control-plane state.
- If remote enforcement is absent or unknown, agents must still follow protected-branch discipline locally and report the remote enforcement state as blocked or unverified.
- Required status checks listed in `.github/rulesets/main-protection.md` define
  the local desired contract. Agents must not declare a PR ready to merge
  without separately verified remote checks, or must explicitly report that
  remote verification is unavailable.
- CODEOWNERS-triggered reviews are mandatory wherever remote protection enforces them. Agents must read the enforced state rather than assume it: when `require_code_owner_reviews` is enabled, an owned path's review must be obtained before merge; when it is disabled, `.github/CODEOWNERS` remains the ownership and review-routing record and no longer gates merges. Report which of the two applies; never record a review that protection did not require and no person gave.

#### 2. Pull Request and Review Contract

Issues provide intake, coordination, and branch links. The current Task owns
approval, evidence, and lifecycle state; closing an Issue, by hand or through
a merged pull request's closing keyword, never transitions a Task or records
acceptance. This repository uses no GitHub Project: with one developer,
Issues cover intake and priority and Tasks cover execution, so a Project
would only repeat Task state. Adding one, or an automation permission for it, needs the owner's approval
naming it, and its fields stay coordination data, never Task execution authority.
Keep Issue intake and priority plus Spec/Task links, without copying their
full bodies or bidirectional state synchronization. A remote Issue, tag, or release mutation requires approval naming the exact
target and action.

- A PR is complete only when: (a) all required status checks pass, (b) all required code reviews are approved, (c) no unresolved `blocker` findings remain.
- Draft/WIP PRs are allowed for collaboration; section 3 owns what that means for merge readiness.
- Agents must not self-approve or bypass required reviewers.
- This repository has one developer and no second reviewer. That risk is
  handled by five parts together. The change's risk class is the one
  [Review risk](workflows.md#review-risk) defines, read with the
  [change-type verification matrix](quality-standards.md#5-change-type-verification-matrix)
  and the [protected surfaces](approval-boundaries.md#enforcement).
  The required `candidate-quality` check runs the static and contract checks.
  A high-risk final diff is reviewed in a fresh context separate from the one
  that wrote it, against the [diff review checklist](../prompts/diff-review.md);
  a low-risk diff closes with the author check that policy defines. The owner then accepts
  each criterion explicitly in the Task's Criterion Acceptance, which a merge
  is not. Git history and the recovery rules below cover rollback. The review
  path calls no model-inference API, under the
  [agentic policy](agentic.md#execution-rules). One person's review is never
  recorded as two independent approvals, and an automated check, App, or
  signature does not stand in for the owner's acceptance. No acceptance or
  ADR decision requires a signed commit or tag; GitHub's signed-commit
  protection is a separate server setting.
- When agents propose changes, they must list which CODEOWNERS paths are touched and which review gates apply.
- Git history is the recovery mechanism. A current Task may name a temporary
  recovery commit, but must not turn a branch tip, expected SHA, checksum, or
  commit census into a standing merge Gate.

#### 3. Merge and Branch Discipline

This section is the single owner of merge and branch-lifecycle rules. Both the
Git workflow policy and `.github/rulesets/main-protection.md` defer here; the
ruleset file records the target settings and dated read-backs and issues no
rule of its own.

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
- Renovate pull requests (`renovate/**`) follow the same protocol. The branch
  protection requires up-to-date branches and stays strict. Bring a Renovate
  branch up to date by running Renovate (the `rebase` label or a new run), not
  with GitHub update-branch, whose merge commit fails the commit-message check.
  Merge one dependency PR at a time, most security-relevant first. Never close a
  Renovate PR by hand, because closing ignores that version; let Renovate close
  it. A merged image change does not apply itself: the HOME recreate needs its
  own approval, and CI does not build local images. The update rules and
  procedure are owned by
  `docs/05.operations/policies/10-platform-and-backup/0086-dependency-version-management.md`.
- Draft or WIP pull requests are never merge-ready. They must list their
  remaining work in the PR template.
- Agents must never modify another agent's in-progress branch without explicit coordination.

#### 4. GitHub Actions Security Contract

- Workflows must use least-privilege `GITHUB_TOKEN` — request only the permissions the job actually needs.
- Prefer OIDC-based cloud credentials over long-lived secrets stored as repository secrets. When proposing or reviewing workflow changes, flag any use of long-lived cloud secrets as a `medium` finding.
- Pin actions to a full commit SHA, not a tag, floating branch or `@latest`.
  The repository setting `sha_pinning_required` enforces this on GitHub's side
  since 2026-11-14.
- `.github/workflow-contract.yml` records the locally verified manifest URL,
  retrieval date, runtime, approved consumers, and security disposition for
  every direct external Action. The focused checker
  (`scripts/lib/gate/github_workflow_contract.py`) rejects unregistered Actions
  and any runtime other than `node24` or `composite`.
- Secrets must never appear in log output (`echo $SECRET`, `run: env`, etc.). Raise a `blocker` finding for any such pattern.
- Untrusted input into `$GITHUB_ENV`, `$GITHUB_OUTPUT`, or `run:` interpolation is a security injection risk — raise a `blocker` finding.
- Reusable workflows called from external repositories must be pinned and reviewed before use.

#### 5. Execution Boundary (Local vs Remote)

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
add this approval step, and approval reuse follows
[approval boundaries](approval-boundaries.md#authorization-source-and-records).

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

#### 6. Local Instruction Authority

- This repository does not adopt a GitHub-native instruction hierarchy for agent execution.
- Instruction authority lives in repo-local assets only:
  - root shims: `AGENTS.md`, `CLAUDE.md`
  - governance SSoT: `.agents/`
  - folder agent guides: the `AGENTS.md` files the Registry
    `folder-agent-guide` profile lists, ranked below canonical governance and
    routing only, per the [documentation protocol](documentation-protocol.md#readme-and-agentsmd)
  - authored adapters: `.claude/provider.md`, `.codex/provider.md`
- Native runtime controls and generated projections consume that authority and
  own none of it, per [bootstrap](bootstrap.md#authority-and-precedence):
  `.claude/settings.json`, `.claude/hooks/`, `.claude/agents/`,
  `.claude/skills/`, `.claude/output-styles/`, `.codex/hooks.json`,
  `.codex/config.toml`.
- GitHub is used here for repository protection, PR workflow, and Actions execution; it is not the canonical home of agent instruction policy.
- Any future GitHub-native instruction file must be treated as out-of-scope until the repository governance explicitly adopts it.

#### 8. CI/CD Job Taxonomy

The [canonical phase matrix](quality-standards.md#canonical-delivery-phase-matrix)
owns stage responsibility. `.github/workflow-contract.yml` owns exact job
identities, event/permission boundaries, selected prerequisites, gate DAG,
change impact and immutable Action provenance. The generic focused checker
compares workflow definitions to that one typed source instead of maintaining
another copied job/action census.

The PR candidate invokes `changed` in shard jobs with read-only permissions
and validated merge, base and head context. Routing uses the same selector
to start the document shard only when it has leaves, while core starts
independently. The required `candidate-quality` aggregate needs routing and
every shard. It accepts a skipped document shard only after successful routing
explicitly selects no leaves and the shard supplies no execution output. A
missing, failed, cancelled or contradictory result fails the aggregate. No feature-push, title-edit or main full-profile rerun
is registered: with merge commits only and strict up-to-date protection, the
merged tree is the tree the candidate checked, and pull request titles never
become commit subjects. The separate main security job writes only its SARIF result. Release
publication is a main-only manual workflow, with `contents: write` restricted to
its producer. It creates a SemVer tag and complete draft assets before publish;
there is no second tag-push or moving-channel producer. Immutable releases are
enabled on the repository since 2026-11-14, so a published release's tag and
assets cannot change afterward.

Greetings, stale-thread handling and PR labels are non-QA coordination jobs.
Their pin, permission and event safety remain checked; they do not own candidate
acceptance. External automatic security integrations require their own actual
remote observation and are not disabled by editing tracked YAML.

When job identity or required context changes, update workflow-contract,
workflow YAML and tracked protection target together, then observe the remote
state separately. A proposed required context is not effective protection.
Never introduce an administrative bypass when source and remote state differ.

#### Issues and Projects

Issue forms (`.github/ISSUE_TEMPLATE/`) collect problem/request, priority and
optional contract/execution links. Specs retain AC/contracts; Tasks retain
actual commands, results, acceptance and authorization. The Project rule is in
§2. GitHub's repository token cannot access Projects; do not add an App/PAT
just to mirror Task state. See
[Project automation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/automating-projects-using-actions).

#### References

- <https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets>
- <https://docs.github.com/en/actions/reference/security/secure-use>
- <https://docs.github.com/en/actions/how-tos/monitor-workflows>
- <https://github.com/zizmorcore/zizmor/releases/tag/v1.28.0>

### Exceptions

#### Exception Conditions

No exception is granted here; a separately authorized operation follows [Approval boundaries](approval-boundaries.md).

#### Approval and Review

None: no exception exists to approve.

## Enforcement

### Mechanisms

#### 7. Completion Gate (GitHub-Specific)

Before an agent declares any PR-related task complete, it must confirm:

1. All required status checks are green (or note which are pending and why), and remote branch protection state is verified or explicitly reported as unverified.
2. All required reviews are approved (or note which are outstanding and who owns them).
3. No `blocker` findings remain from code review or security audit.
4. CODEOWNERS-triggered reviewers have been notified if paths are owned and remote protection enforces owner review; when it does not, state that instead of claiming a review.
5. No secrets, long-lived credentials, or unpinned action references were introduced.

If any gate is unmet, the task status is "blocked" not "done."

### Limits

The policy names checks for workflow pinning, PR completion and the aggregate gate, but most rules rest on review, approval or remote state it does not control.

- Protection: R1-R5 rest on manual review or name no check.
- CODEOWNERS: R6-R8 rest on manual review or name no check.
- Issues: R9-R11, R85-R86 rest on manual review or name no check.
- Remote mutation: R12, R53-R58 rest on manual review or name no check.
- PR: R13-R15, R38 rest on manual review or name no check.
- PR review: R16, R18-R25 rest on manual review or name no check.
- Recovery: R26-R27 rest on manual review or name no check.
- Merge: R28-R29 rest on manual review or name no check.
- Branch: R30-R33, R39 rest on manual review or name no check.
- Renovate: R34-R37 rest on manual review or name no check.
- Actions: R40-R41, R44-R46 rest on manual review or name no check.
- Execution: R47-R48, R50-R52 rest on manual review or name no check.
- Workflow: R59-R60 rest on manual review or name no check.
- Evidence: R62-R65 rest on manual review or name no check.
- QA definition: R66-R71 rest on manual review or name no check.
- Authority: R72-R75 rest on manual review or name no check.
- CI/CD: R77-R84 rest on manual review or name no check.
- Enforcement gap: remote branch protection and rulesets are not applied by tracked files; state stays `unverified` until authenticated read-back.
- Enforcement gap: QA definition trust cannot be enforced remotely without a separately approved verification definition and protection settings read back; a local revision observes none of it.

## Ownership

### Owner

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](approval-boundaries.md#authorization-source-and-records)).

### Review Triggers

Changes land in place with Task evidence; related documents:

- [Provider index](providers/README.md)
- [Claude adapter](../../.claude/provider.md)
- [Codex adapter](../../.codex/provider.md)
- [Repository surface](../../.github/repository-surface.md)
- [Main protection](../../.github/rulesets/main-protection.md)
- [Platform and backup runbooks](../../docs/05.operations/runbooks/10-platform-and-backup/README.md)
- [Git workflow](git-workflow.md)
- [Quality standards](quality-standards.md)
- [AI agent standards](standards.md)
- [Bootstrap policy](bootstrap.md)
