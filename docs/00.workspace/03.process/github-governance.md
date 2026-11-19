---
title: "GitHub Governance Policy"
version: "1.12.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-19"
---

# GitHub Governance Policy

## Purpose and Scope

### Objective

Normative policy baseline aligning agent behavior with GitHub repository operations.
A stricter rule in another canonical governance owner prevails over this document.

#### Authority

This policy is the canonical owner of repository protection, pull requests, hosted workflows, and remote actions under [bootstrap precedence](../../../.agents/governance/bootstrap.md#authority-and-precedence).

### Applies To

Repository protection, pull requests, hosted workflows, and separately authorized remote actions.

#### Exclusions

None: this document states no exclusion.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| GITHUB-GOVERNANCE-R1 | Always | Required: treat `main` as a protected branch with no direct pushes, no force pushes and no bypass of required checks, even where GitHub does not fully enforce it | none | none |
| GITHUB-GOVERNANCE-R2 | Always | Forbidden: treating this agent behavior contract as evidence of applied GitHub settings | none | none |
| GITHUB-GOVERNANCE-R3 | Always | Required: report remote control-plane state as `unverified` until it is authenticated and read back for the named repository | none | none |
| GITHUB-GOVERNANCE-R4 | Claiming remote enforcement | Required: authenticate and read back remote branch protection and ruleset state first | none | dated authenticated read-backs in `.github/rulesets/main-protection.md` |
| GITHUB-GOVERNANCE-R5 | Always | Forbidden: treating tracked files as proof of applied control-plane state | none | none |
| GITHUB-GOVERNANCE-R6 | Remote enforcement absent or unknown | Required: follow protected-branch discipline locally and report remote enforcement as blocked or unverified | none | none |
| GITHUB-GOVERNANCE-R7 | Always | Required: treat the required status checks listed in `.github/rulesets/main-protection.md` as the local desired contract | none | none |
| GITHUB-GOVERNANCE-R8 | Declaring a PR ready to merge | Required: verify remote checks separately or explicitly report that remote verification is unavailable | none | none |
| GITHUB-GOVERNANCE-R9 | CODEOWNERS-triggered review | Required: read the enforced protection state rather than assume it | none | none |
| GITHUB-GOVERNANCE-R10 | `require_code_owner_reviews` enabled | Required: obtain an owned path's review before merge | none | none |
| GITHUB-GOVERNANCE-R11 | `require_code_owner_reviews` disabled | Required: treat `.github/CODEOWNERS` as the ownership and review-routing record, not a merge gate | none | none |
| GITHUB-GOVERNANCE-R12 | CODEOWNERS-triggered review | Required: report which of the enabled or disabled states applies | none | none |
| GITHUB-GOVERNANCE-R13 | Always | Forbidden: recording a review that protection did not require and no person gave | none | none |
| GITHUB-GOVERNANCE-R14 | Always | Required: keep approval, evidence and lifecycle state in the current Task; Issues provide intake, coordination and branch links | none | none |
| GITHUB-GOVERNANCE-R15 | Issue closed by hand or by a closing keyword | Forbidden: treating it as a Task transition or an acceptance record | none | none |
| GITHUB-GOVERNANCE-R16 | Adding a GitHub Project or an automation permission for it | Required: owner approval naming it | none | none |
| GITHUB-GOVERNANCE-R17 | A GitHub Project exists | Forbidden: treating its fields as Task execution authority; they stay coordination data | none | none |
| GITHUB-GOVERNANCE-R18 | Issue intake | Required: keep Issue intake and priority plus Spec/Task links | none | none |
| GITHUB-GOVERNANCE-R19 | Issue intake | Forbidden: copying Spec/Task full bodies or bidirectional state synchronization | none | none |
| GITHUB-GOVERNANCE-R20 | Remote Issue, tag or release mutation | Required: approval naming the exact target and action | none | none |
| GITHUB-GOVERNANCE-R21 | Declaring a PR complete | Required: all required status checks pass, all required code reviews are approved and no unresolved `blocker` findings remain | none | none |
| GITHUB-GOVERNANCE-R22 | Collaboration | Allowed: Draft/WIP PRs; section 3 owns their merge readiness | none | none |
| GITHUB-GOVERNANCE-R23 | Review | Forbidden: self-approving or bypassing required reviewers | none | none |
| GITHUB-GOVERNANCE-R24 | Classifying a change's risk | Required: use the Review risk class read with the change-type verification matrix and protected surfaces | none | none |
| GITHUB-GOVERNANCE-R25 | PR candidate | Required: the required `candidate-quality` check runs the static and contract checks | none | none |
| GITHUB-GOVERNANCE-R26 | High-risk final diff | Required: review it in a fresh context separate from the one that wrote it, against the diff review checklist | none | none |
| GITHUB-GOVERNANCE-R123 | Medium-risk diff | Required: one primary review in a fresh context by a read-only reviewer who did not write it, against the diff review checklist | none | none |
| GITHUB-GOVERNANCE-R27 | Low-risk diff | Required: close it with the author check the Review risk policy defines | none | none |
| GITHUB-GOVERNANCE-R28 | Criterion acceptance | Required: the owner accepts each criterion explicitly in the Task's Criterion Acceptance | none | Task Criterion Acceptance |
| GITHUB-GOVERNANCE-R29 | Criterion acceptance | Forbidden: treating a merge as acceptance | none | none |
| GITHUB-GOVERNANCE-R30 | Review path | Forbidden: calling a model-inference API | none | none |
| GITHUB-GOVERNANCE-R31 | Recording reviews | Forbidden: recording one person's review as two independent approvals | none | none |
| GITHUB-GOVERNANCE-R32 | Owner acceptance | Forbidden: letting an automated check, App or signature stand in for the owner's acceptance | none | none |
| GITHUB-GOVERNANCE-R33 | Acceptance or ADR decision | Allowed: making it without a signed commit or tag | none | none |
| GITHUB-GOVERNANCE-R34 | Agent proposes changes | Required: list the CODEOWNERS paths touched and the review gates that apply | none | none |
| GITHUB-GOVERNANCE-R35 | Current Task | Allowed: naming a temporary recovery commit | none | none |
| GITHUB-GOVERNANCE-R36 | Current Task | Forbidden: turning a branch tip, expected SHA, checksum or commit census into a standing merge Gate | none | none |
| GITHUB-GOVERNANCE-R37 | Always | Forbidden: `.github/rulesets/main-protection.md` issuing a merge or branch rule of its own | none | none |
| GITHUB-GOVERNANCE-R38 | Change delivered to `main` | Required: deliver it through a pull request | none | none |
| GITHUB-GOVERNANCE-R39 | `main` | Forbidden: pushing directly, force-pushing or bypassing a required check, regardless of how few reviews protection requires | none | none |
| GITHUB-GOVERNANCE-R40 | Branch deletion | Required: the approved change and every referenced recovery commit are reachable from the delivered protected branch, the linked worktree is clean and the request or owner asks | none | none |
| GITHUB-GOVERNANCE-R41 | Long-lived branch other than `main` | Required: explicit user authorization | none | none |
| GITHUB-GOVERNANCE-R42 | Before integration | Forbidden: rewriting a current Task's named recovery commit | none | none |
| GITHUB-GOVERNANCE-R43 | Integrating referenced objects | Required: use a merge commit or fast-forward rather than rewriting them | none | none |
| GITHUB-GOVERNANCE-R44 | History cleanup beyond the completed feature branch | Required: explicit authorization | none | none |
| GITHUB-GOVERNANCE-R45 | Renovate PR (`renovate/**`) | Required: follow the same pull request protocol | none | none |
| GITHUB-GOVERNANCE-R46 | Always | Required: branch protection requires up-to-date branches and stays strict | none | none |
| GITHUB-GOVERNANCE-R47 | Bringing a Renovate branch up to date | Required: run Renovate (the `rebase` label or a new run) | none | none |
| GITHUB-GOVERNANCE-R48 | Bringing a Renovate branch up to date | Forbidden: using GitHub update-branch | commit-message check fails its merge commit | none |
| GITHUB-GOVERNANCE-R49 | Merging Renovate PRs | Required: merge one dependency PR at a time, most security-relevant first | none | none |
| GITHUB-GOVERNANCE-R50 | Renovate PR | Forbidden: closing it by hand | none | none |
| GITHUB-GOVERNANCE-R51 | Renovate PR to be closed | Required: let Renovate close it | none | none |
| GITHUB-GOVERNANCE-R52 | Merged image change | Required: a separate approval for the HOME recreate | none | none |
| GITHUB-GOVERNANCE-R53 | Dependency updates | Required: follow the update rules and procedure in `0086-dependency-version-management.md` | none | none |
| GITHUB-GOVERNANCE-R54 | Draft or WIP PR | Forbidden: treating it as merge-ready | none | none |
| GITHUB-GOVERNANCE-R55 | Draft or WIP PR | Required: list its remaining work in the PR template | none | none |
| GITHUB-GOVERNANCE-R56 | Another agent's in-progress branch | Forbidden: modifying it without explicit coordination | none | none |
| GITHUB-GOVERNANCE-R57 | Workflows | Required: use least-privilege `GITHUB_TOKEN`, requesting only the permissions the job needs | none | none |
| GITHUB-GOVERNANCE-R58 | Cloud credentials | Required: prefer OIDC-based credentials over long-lived repository secrets | none | none |
| GITHUB-GOVERNANCE-R59 | Proposing or reviewing workflow changes | Required: flag any long-lived cloud secret as a `medium` finding | none | none |
| GITHUB-GOVERNANCE-R60 | Action references | Required: pin to a full commit SHA, not a tag, floating branch or `@latest` | `sha_pinning_required` repository setting | none |
| GITHUB-GOVERNANCE-R61 | Direct external Action | Required: record its manifest URL, retrieval date, runtime, approved consumers and security disposition in `.github/workflow-contract.yml` | `scripts/lib/gate/github_workflow_contract.py` rejects unregistered Actions and runtimes other than `node24` or `composite` | none |
| GITHUB-GOVERNANCE-R62 | Always | Forbidden: secrets in log output (`echo $SECRET`, `run: env`, etc.) | none | none |
| GITHUB-GOVERNANCE-R63 | Secret-in-log pattern found | Required: raise a `blocker` finding | none | none |
| GITHUB-GOVERNANCE-R64 | Untrusted input into `$GITHUB_ENV`, `$GITHUB_OUTPUT` or `run:` interpolation | Required: raise a `blocker` finding | none | none |
| GITHUB-GOVERNANCE-R65 | Reusable workflow called from an external repository | Required: pin and review it before use | none | none |
| GITHUB-GOVERNANCE-R66 | Local execution | Required: explicit formatting, focused RED/GREEN, message validation and read-only diagnostic checks, selected by the shared execution boundary | none | none |
| GITHUB-GOVERNANCE-R67 | Local execution | Forbidden: direct Agent pre-commit/all-files bypass | none | none |
| GITHUB-GOVERNANCE-R68 | Remote PR | Required: the public changed entrypoint owns aggregate candidate QA once | none | none |
| GITHUB-GOVERNANCE-R69 | Feature push | Forbidden: repeating aggregate candidate QA | none | none |
| GITHUB-GOVERNANCE-R70 | Remote PR required check | Required: keep required selection inside an always-present PR workflow rather than path-skipping the required check | none | none |
| GITHUB-GOVERNANCE-R71 | Main | Required: treat merged-revision security/SARIF as a distinct observation, not a second candidate run | none | none |
| GITHUB-GOVERNANCE-R72 | Manual release producer | Required: run it only once the user names its exact version and trusted main revision | none | none |
| GITHUB-GOVERNANCE-R73 | User approves remote GitHub mutation | Required: bind the action to a concrete repository and remote surface before changing state | none | none |
| GITHUB-GOVERNANCE-R74 | User approves remote GitHub mutation | Required: Task evidence includes approval source, target repository, target setting or object, command class, before- and after-state evidence and rollback or recovery path | none | Task evidence |
| GITHUB-GOVERNANCE-R75 | Merging a pull request | Required: merge only a PR the current request asks to merge, after its required checks pass | none | none |
| GITHUB-GOVERNANCE-R76 | Remote GitHub mutation | Forbidden: bypassing required checks, weakening protected-branch rules or exposing GitHub secrets unless the user names that concrete action and target | none | none |
| GITHUB-GOVERNANCE-R77 | Read-only remote checks | Allowed: recording them as verification evidence | none | none |
| GITHUB-GOVERNANCE-R78 | Remote state approved but not changed | Required: report it as verified-only, not as a mutation | none | none |
| GITHUB-GOVERNANCE-R79 | Tracked workflow file | Forbidden: treating it as evidence that a remote schedule, manual dispatch, job or required check ran | none | none |
| GITHUB-GOVERNANCE-R80 | Approved workflow definition | Allowed: authoring and validating it locally and pushing it with the request's branch and pull request | none | none |
| GITHUB-GOVERNANCE-R81 | Until the user names the repository and remote surface | Forbidden: dispatching a workflow, enabling it remotely or changing GitHub checks, rulesets, branch protection, environments, deployments or releases | none | none |
| GITHUB-GOVERNANCE-R82 | Local checks, selected public suites and skipped-check rationale | Required: use the shared change-type verification matrix | none | none |
| GITHUB-GOVERNANCE-R83 | Always | Forbidden: this policy defining a second matrix or additional provider-specific gates | none | none |
| GITHUB-GOVERNANCE-R84 | PR-related work | Required: record local command results separately from hosted run IDs, head commits, job conclusions, required reviews and observed protection settings | none | none |
| GITHUB-GOVERNANCE-R85 | Missing tool, unexecuted check or unavailable remote observation | Required: keep it explicitly blocked, skipped with a reason, or unverified | none | none |
| GITHUB-GOVERNANCE-R86 | Missing tool, unexecuted check or unavailable remote observation | Forbidden: treating it as passing evidence | none | none |
| GITHUB-GOVERNANCE-R87 | Task completion | Forbidden: citing a CI-only gate alone when a cheap local check is available | none | none |
| GITHUB-GOVERNANCE-R88 | Task completion | Forbidden: letting a local-only check replace required protected-branch gates | none | none |
| GITHUB-GOVERNANCE-R89 | Change to a QA definition | Required: tie the current owner's actual acceptance to that diff and revision | none | none |
| GITHUB-GOVERNANCE-R90 | Change to a QA definition | Required: record in the Task the source and revision of the trusted base definition it was compared with | none | Task record of the trusted base source and revision |
| GITHUB-GOVERNANCE-R91 | Ordinary documentation change | Allowed: no added QA-definition approval step | none | none |
| GITHUB-GOVERNANCE-R92 | Reusing an approval | Required: follow approval boundaries | none | none |
| GITHUB-GOVERNANCE-R93 | Candidate runs its own workflow, controller and configuration | Forbidden: treating its success as showing the QA definition is unchanged or approved | none | none |
| GITHUB-GOVERNANCE-R94 | Current `candidate-quality` | Forbidden: treating it as evidence of a trusted base runner or of an independent approval of a definition change | none | none |
| GITHUB-GOVERNANCE-R95 | Enforcing QA definition trust remotely | Required: a verification definition the candidate cannot modify plus protection settings consuming its result, each separately approved, applied and read back | none | none |
| GITHUB-GOVERNANCE-R96 | Always | Forbidden: treating a local revision of this policy as an observation of remote QA definition enforcement | none | none |
| GITHUB-GOVERNANCE-R97 | Implementing QA definition trust | Forbidden: checking out or running candidate code in a privileged `pull_request_target` runner | none | none |
| GITHUB-GOVERNANCE-R98 | Implementing QA definition trust | Forbidden: creating a new App or credential implicitly | none | none |
| GITHUB-GOVERNANCE-R99 | Agent execution | Forbidden: adopting a GitHub-native instruction hierarchy or treating GitHub as the canonical home of agent instruction policy | none | none |
| GITHUB-GOVERNANCE-R100 | Always | Required: take instruction authority from repo-local assets only: root shims, `.agents/`, folder agent guides and authored adapters | none | none |
| GITHUB-GOVERNANCE-R101 | Native runtime controls and generated projections | Forbidden: owning any instruction authority; they only consume it | none | none |
| GITHUB-GOVERNANCE-R102 | Future GitHub-native instruction file | Required: treat it as out of scope until repository governance explicitly adopts it | none | none |
| GITHUB-GOVERNANCE-R103 | Stage responsibility | Required: take it from the canonical phase matrix | none | none |
| GITHUB-GOVERNANCE-R104 | Job identities, event/permission boundaries, prerequisites, gate DAG, change impact and Action provenance | Required: keep them in `.github/workflow-contract.yml` as the one typed source | generic focused checker compares workflow definitions to `.github/workflow-contract.yml` | none |
| GITHUB-GOVERNANCE-R105 | Workflow definitions | Forbidden: maintaining another copied job/action census | none | none |
| GITHUB-GOVERNANCE-R106 | PR candidate shard jobs | Required: invoke `changed` with read-only permissions and validated merge, base and head context | none | none |
| GITHUB-GOVERNANCE-R107 | PR candidate routing | Required: start the document shard only when the selector gives it leaves | none | none |
| GITHUB-GOVERNANCE-R108 | Required `candidate-quality` aggregate | Required: need routing and every shard; accept a skipped document shard only after successful routing selects no leaves and the shard supplies no execution output; fail on a missing, failed, cancelled or contradictory result | none | none |
| GITHUB-GOVERNANCE-R109 | CI/CD workflow set | Forbidden: registering a feature-push, title-edit or main full-profile rerun | none | none |
| GITHUB-GOVERNANCE-R110 | Main security job | Required: write only its SARIF result | none | none |
| GITHUB-GOVERNANCE-R111 | Release publication | Required: a main-only manual workflow with `contents: write` restricted to its producer, creating a SemVer tag and complete draft assets before publish | none | none |
| GITHUB-GOVERNANCE-R112 | Release publication | Forbidden: a second tag-push or moving-channel producer | none | none |
| GITHUB-GOVERNANCE-R113 | Non-QA coordination jobs (greetings, stale threads, PR labels) | Required: keep their pin, permission and event safety checked | none | none |
| GITHUB-GOVERNANCE-R114 | Non-QA coordination jobs | Forbidden: owning candidate acceptance | none | none |
| GITHUB-GOVERNANCE-R115 | External automatic security integrations | Required: their own actual remote observation | none | none |
| GITHUB-GOVERNANCE-R116 | External automatic security integrations | Forbidden: treating an edit to tracked YAML as disabling them | none | none |
| GITHUB-GOVERNANCE-R117 | Job identity or required context changes | Required: update workflow-contract, workflow YAML and tracked protection target together, then observe remote state separately | none | none |
| GITHUB-GOVERNANCE-R118 | Proposed required context | Forbidden: treating it as effective protection | none | none |
| GITHUB-GOVERNANCE-R119 | Source and remote state differ | Forbidden: introducing an administrative bypass | none | none |
| GITHUB-GOVERNANCE-R120 | Issue forms | Required: collect problem/request, priority and optional contract/execution links | none | none |
| GITHUB-GOVERNANCE-R121 | Spec and Task records | Required: Specs retain AC/contracts and Tasks retain actual commands, results, acceptance and authorization | none | none |
| GITHUB-GOVERNANCE-R122 | Mirroring Task state to Projects | Forbidden: adding an App/PAT just to mirror Task state | none | none |

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
  [Review risk](../04.quality/quality-standards.md#11-review-risk) defines, read with the
  [change-type verification matrix](../04.quality/quality-standards.md#5-change-type-verification-matrix)
  and the [protected surfaces](../04.quality/approval-boundaries.md#enforcement).
  The required `candidate-quality` check runs the static and contract checks.
  A high-risk final diff is reviewed in a fresh context separate from the one
  that wrote it, against the [diff review checklist](../../../.agents/prompts/diff-review.md);
  a medium-risk diff gets one primary review by a read-only reviewer in a
  fresh context who did not write it; a low-risk diff closes with the author
  check that policy defines. The owner then accepts
  each criterion explicitly in the Task's Criterion Acceptance, which a merge
  is not. Git history and the recovery rules below cover rollback. The review
  path calls no model-inference API, under the
  [agentic policy](../../../.agents/governance/agentic.md#execution-rules). One person's review is never
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
  `docs/05.operations/02.policies/10.platform-and-backup/0086-dependency-version-management.md`.
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
  [execution boundary](../04.quality/quality-standards.md#4-execution-boundary) owns their
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

Use the [shared change-type verification matrix](../04.quality/quality-standards.md#5-change-type-verification-matrix)
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
[approval boundaries](../04.quality/approval-boundaries.md#authorization-source-and-records).

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
  own none of it, per [bootstrap](../../../.agents/governance/bootstrap.md#authority-and-precedence):
  `.claude/settings.json`, `.claude/hooks/`, `.claude/agents/`,
  `.claude/skills/`, `.claude/output-styles/`, `.codex/hooks.json`,
  `.codex/config.toml`.
- GitHub is used here for repository protection, PR workflow, and Actions execution; it is not the canonical home of agent instruction policy.
- Any future GitHub-native instruction file must be treated as out-of-scope until the repository governance explicitly adopts it.

#### 8. CI/CD Job Taxonomy

The [canonical phase matrix](../04.quality/quality-standards.md#canonical-delivery-phase-matrix)
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

No exception is granted here; a separately authorized operation follows [Approval boundaries](../04.quality/approval-boundaries.md).

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

Four rules name a check the policy ties to them (R48, R60, R61, R104); every other rule names none:

- Protection and remote read-back: R1-R8.
- CODEOWNERS review: R9-R13, R34.
- Issues, Tasks and Projects: R14-R20, R120-R122.
- PR completion, review and acceptance: R21-R33, R123.
- Recovery, merge and branch discipline: R35-R44, R54-R56.
- Renovate and dependency updates: R45-R47, R49-R53.
- Actions security: R57-R59, R62-R65.
- Execution boundary: R66-R72.
- Remote mutation and tracked workflow definitions: R73-R81.
- Evidence by change type: R82-R88.
- QA definition trust: R89-R98.
- Local instruction authority: R99-R102.
- CI/CD job taxonomy: R103, R105-R119.
- Enforcement gap: tracked files do not prove applied control-plane state; remote protection stays `unverified` until authenticated read-back, and a proposed required context is not effective protection.
- Enforcement gap: remote enforcement of QA definition trust needs a separately approved, applied and read-back verification definition and protection settings; a local revision of this policy observes none of it.
- Rules stated under Enforcement (the GitHub-specific Completion Gate) are outside this table.

## Ownership

### Owner

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](../04.quality/approval-boundaries.md#authorization-source-and-records)).

### Review Triggers

Changes land in place with Task evidence; related documents:

- [Provider index](../../../.agents/governance/providers/README.md)
- [Claude adapter](../../../.claude/provider.md)
- [Codex adapter](../../../.codex/provider.md)
- [Repository surface](../../../.github/repository-surface.md)
- [Main protection](../../../.github/rulesets/main-protection.md)
- [Platform and backup runbooks](../../05.operations/03.runbooks/10.platform-and-backup/README.md)
- [Git workflow](git-workflow.md)
- [Quality standards](../04.quality/quality-standards.md)
- [AI agent standards](../../../.agents/governance/standards.md)
- [Bootstrap policy](../../../.agents/governance/bootstrap.md)
