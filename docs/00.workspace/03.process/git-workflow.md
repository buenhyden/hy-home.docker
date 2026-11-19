---
title: "Git Workflow Governance"
version: "1.10.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-20"
---

# Git Workflow Governance

## Purpose and Scope

### Objective

This rule defines the mandatory git workflow for all contributors and agents.

#### Authority

This policy is the canonical owner of local Git authoring, branch integration, commits, review, and remote delivery boundaries under [bootstrap precedence](../../../.agents/governance/bootstrap.md#authority-and-precedence).

### Applies To

Local Git authoring, branch integration, commits, review, and remote delivery boundaries.

#### Exclusions

None: this document states no exclusion.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| GIT-WORKFLOW-R1 | Every commit | Required: use Conventional Commits in the form `<type>[(<scope>)][!]: <Description>` | `.cz.toml` grammar read by the `commit-msg` hook and the PR commit-range check | none |
| GIT-WORKFLOW-R2 | Every commit | Required: use explicit scopes where possible | none | none |
| GIT-WORKFLOW-R3 | Every commit | Required: the type is a key in `.cz.toml`'s `change_type_map` | `.cz.toml` grammar read by the `commit-msg` hook and the PR commit-range check | none |
| GIT-WORKFLOW-R4 | Every commit | Required: the description starts with a capital letter and does not end with a period | `.cz.toml` grammar read by the `commit-msg` hook and the PR commit-range check | none |
| GIT-WORKFLOW-R5 | A commit body is present | Required: the body is one block with no blank line inside it | `.cz.toml` grammar read by the `commit-msg` hook and the PR commit-range check | none |
| GIT-WORKFLOW-R6 | A commit body is present | Forbidden: a body line starting with a word followed by a colon and a space | none | none |
| GIT-WORKFLOW-R7 | A body line reads like a trailer | Required: rewrap the sentence | none | none |
| GIT-WORKFLOW-R8 | A body line reads like a trailer | Forbidden: reaching for `--no-verify` | none | none |
| GIT-WORKFLOW-R9 | Trailers are present | Required: trailers come last, after a single blank line | `.cz.toml` grammar read by the `commit-msg` hook and the PR commit-range check | none |
| GIT-WORKFLOW-R10 | Every commit | Required: the header stays within the `.cz.toml` header length | `.cz.toml` grammar read by the `commit-msg` hook and the PR commit-range check | none |
| GIT-WORKFLOW-R11 | Always | Required: treat `.cz.toml` as the sole executable authority for allowed types, message grammar and header length | none | none |
| GIT-WORKFLOW-R12 | commit-msg delivery is unconfirmed or diagnosis is needed | Required: validate the draft with `cz check --message-length-limit 75 --message ...` before starting the commit | none | none |
| GIT-WORKFLOW-R13 | Judging commit-message enforcement | Required: observe whether a `commit-msg` hook is actually installed | none | none |
| GIT-WORKFLOW-R14 | Judging commit-message enforcement | Forbidden: treating the configuration alone as enforcement evidence | none | none |
| GIT-WORKFLOW-R15 | An ordinary commit | Required: prepare the message file, stage the reviewed changes and run `git commit -F /tmp/commit-message.txt` | none | none |
| GIT-WORKFLOW-R16 | An ordinary commit | Forbidden: repeating beforehand the style checks the observed pre-commit and commit-msg hooks run on the same input | none | none |
| GIT-WORKFLOW-R17 | Delivery of the installed checks is unconfirmed or a diagnosis is needed | Allowed: run `scripts/validation/run-ci-precommit.sh --mode local-staged` on an isolated copy of the index with the registered pins | none | none |
| GIT-WORKFLOW-R18 | The local-staged check fails | Required: fix, review the diff, restage and commit normally | none | none |
| GIT-WORKFLOW-R19 | The index changes | Forbidden: reusing an earlier PASS | none | none |
| GIT-WORKFLOW-R20 | Always | Forbidden: the local-staged controller replacing a user-global hook | none | none |
| GIT-WORKFLOW-R21 | Always | Forbidden: claiming automatic enforcement from configuration alone | none | none |
| GIT-WORKFLOW-R22 | Always | Required: keep `main` as the protected baseline | none | none |
| GIT-WORKFLOW-R23 | A short-lived human branch | Required: name it `<type>/<short-description>` with `type` a `.cz.toml` change type | none | none |
| GIT-WORKFLOW-R24 | An existing intake Issue ID applies | Allowed: the Issue ID precedes the branch description | none | none |
| GIT-WORKFLOW-R25 | Naming a branch | Forbidden: creating a duplicate Issue or copying the Spec/Task merely to satisfy a branch name | none | none |
| GIT-WORKFLOW-R26 | An emergency hotfix | Required: name the branch `hotfix/<short-description>` | none | none |
| GIT-WORKFLOW-R27 | An emergency hotfix | Required: preserve the same PR, validation and explicit runtime authorization boundaries | none | none |
| GIT-WORKFLOW-R28 | Tool-generated PR branches | Allowed: `renovate/**` and `codex/**` branches, for tool-generated PR branches only | none | none |
| GIT-WORKFLOW-R29 | Always | Required: Renovate is the sole dependency updater | none | none |
| GIT-WORKFLOW-R30 | An automation branch | Required: merge through the PR protocol and required checks | none | none |
| GIT-WORKFLOW-R31 | A branch's linked worktree | Required: create it under the ignored `.worktrees/<branch>` directory | none | none |
| GIT-WORKFLOW-R32 | The work ends | Required: remove the worktree and its merged branch | none | none |
| GIT-WORKFLOW-R33 | A detached checkout a script creates and removes inside its own scratch directory | Allowed: treat it as outside the branch worktree rules | none | none |
| GIT-WORKFLOW-R34 | Starting a new branch or worktree | Required: start from the latest committed state the work builds on, normally `main` after the previous PR merged | none | none |
| GIT-WORKFLOW-R35 | Making room for a new branch or worktree | Forbidden: stashing, resetting, discarding or force-committing uncommitted user work | none | none |
| GIT-WORKFLOW-R36 | Uncommitted user work is in the way | Required: stop and ask | none | none |
| GIT-WORKFLOW-R37 | Opening or updating a PR | Required: self-review the changes first | none | none |
| GIT-WORKFLOW-R38 | Opening or updating a PR | Required: run focused authoring checks and inspect the selected prerequisites | none | none |
| GIT-WORKFLOW-R39 | The same declared input and trust boundary | Forbidden: repeating the aggregate QA the remote PR candidate owns before push or after merge | none | none |
| GIT-WORKFLOW-R40 | Before result-only Task evidence recording | Required: run document-link validation locally on the final source input | none | none |
| GIT-WORKFLOW-R41 | Document-link validation has run | Required: record its bound input and result in the Task | none | Task record |
| GIT-WORKFLOW-R42 | A result-only addition | Required: use minimum document checks | none | none |
| GIT-WORKFLOW-R43 | A result-only addition | Required: check only new or changed link destinations in that Task rather than the whole corpus | none | none |
| GIT-WORKFLOW-R44 | Remote PR QA | Required: exclude the link leaf | none | none |
| GIT-WORKFLOW-R45 | Remote PR QA | Required: keep the metadata, relationship, lifecycle and applicable operations catalog checks | none | none |
| GIT-WORKFLOW-R46 | Governance work | Required: ensure linked stage docs remain accurate | none | none |
| GIT-WORKFLOW-R47 | Before declaring a PR done | Required: apply the Completion Gate from `docs/00.workspace/03.process/github-governance.md` | none | none |
| GIT-WORKFLOW-R48 | Work is incomplete | Required: mark the PR Draft/WIP | none | none |
| GIT-WORKFLOW-R49 | The PR is not ready | Forbidden: requesting final review | none | none |
| GIT-WORKFLOW-R50 | Merge readiness and branch lifecycle | Required: follow `docs/00.workspace/03.process/github-governance.md` section 3 | none | none |
| GIT-WORKFLOW-R51 | A pull request | Required: carry the work of one Spec Package | none | none |
| GIT-WORKFLOW-R52 | A pull request | Allowed: hold several of that Spec's Tasks as separate logical commits | none | none |
| GIT-WORKFLOW-R53 | A pull request | Forbidden: mixing Specs | none | none |
| GIT-WORKFLOW-R54 | Always | Required: keep commits atomic and reviewable | none | none |
| GIT-WORKFLOW-R55 | A cleanup proposal | Required: document it in the PR | none | none |
| GIT-WORKFLOW-R56 | A cleanup proposal | Required: satisfy the recovery-commit and history-rewrite rules of `docs/00.workspace/03.process/github-governance.md` section 3 | none | none |
| GIT-WORKFLOW-R57 | Requesting review | Required: request it only after self-review and programmatic checks pass | none | none |
| GIT-WORKFLOW-R58 | Requesting review | Required: summarize scope, risk and how to verify | none | none |
| GIT-WORKFLOW-R59 | Review feedback before re-requesting review | Required: resolve or reply to each finding, re-run affected checks and record what changed | none | none |
| GIT-WORKFLOW-R60 | A user-visible or operational defect correction | Required: use `fix` | none | none |
| GIT-WORKFLOW-R61 | A user-visible or operational defect correction | Required: include regression evidence | none | none |
| GIT-WORKFLOW-R62 | A structure change | Required: use `refactor` only for behavior-preserving changes | none | none |
| GIT-WORKFLOW-R63 | A `refactor` change | Required: list checks that demonstrate unchanged behavior | none | none |
| GIT-WORKFLOW-R64 | Applicable IDs exist | Required: reference issue IDs, ADR IDs or plan/task IDs | none | none |
| GIT-WORKFLOW-R65 | A Git or GitHub automatic merge subject | Allowed: it is exempt from the grammar (`allowed_prefixes`, owner decision of 2026-11-14) | `.cz.toml` `allowed_prefixes` read by the `commit-msg` hook and the PR commit-range check | none |
| GIT-WORKFLOW-R66 | A commit message | Forbidden: fixup and squash escapes | none | none |
| GIT-WORKFLOW-R67 | A main-targeted release-preparation PR | Required: maintain `CHANGELOG.md` in Keep a Changelog form | none | none |
| GIT-WORKFLOW-R68 | A development push | Forbidden: generating or publishing a changelog | none | none |
| GIT-WORKFLOW-R69 | A future release tag | Required: `v` plus strict SemVer (`.cz.toml` `tag_format`) | none | none |
| GIT-WORKFLOW-R70 | Always | Forbidden: pushing a tag independently | none | none |
| GIT-WORKFLOW-R71 | Releasing | Required: the release producer is the one defined in `docs/00.workspace/03.process/github-governance.md` section 8 | none | none |
| GIT-WORKFLOW-R72 | An existing non-SemVer historical ref | Required: keep it as evidence | none | none |
| GIT-WORKFLOW-R73 | Deleting or rewriting an existing non-SemVer historical ref | Required: the owner's approval for that ref | manual | none |
| GIT-WORKFLOW-R74 | A specific release publication | Required: its exact version, commit, approved target and recovery path | none | none |
| GIT-WORKFLOW-R75 | A specific release publication | Required: select `RUN-0009` through the platform and backup runbook index | none | none |
| GIT-WORKFLOW-R76 | Repository-modifying agent work | Required: create logical Conventional Commits after verification and before declaring the task done | none | none |
| GIT-WORKFLOW-R77 | Repository-modifying agent work | Required: split commits by reviewable concern unless inseparable | none | none |
| GIT-WORKFLOW-R78 | Repository-modifying agent work | Required: stage only files or hunks owned by the current task | none | none |
| GIT-WORKFLOW-R79 | Repository-modifying agent work | Required: leave unrelated untracked files and user changes untouched | none | none |
| GIT-WORKFLOW-R80 | The user asks not to commit, the work is exploratory or incomplete, required checks or approvals are missing, or the commit would include secrets or unrelated changes | Forbidden: committing | none | none |
| GIT-WORKFLOW-R81 | A commit is withheld | Required: report the reason and remaining state | none | none |
| GIT-WORKFLOW-R82 | Local staged diagnosis | Required: support an unborn index, report a valid empty index as NOT_APPLICABLE, and reject changed source index/HEAD or cancelled execution instead of reusing its result | `run-ci-precommit.sh --mode local-staged` | none |
| GIT-WORKFLOW-R83 | Native pre-push ref input | Required: inspect every update including an unterminated final record; reject malformed records and any main target update while retaining the empty-update no-op | `pre-push-guard.sh` | none |

#### 1. Commit Standards

Use Conventional Commits with explicit scopes where possible.

- Format: `<type>[(<scope>)][!]: <Description>`; brackets denote optional
  parts and are not literal characters.
- Types: the keys in `.cz.toml`'s `change_type_map`. That map is the executable
  type vocabulary.
- The description starts with a capital letter and does not end with a
  period. The body, when present, is one block with no blank line inside
  it, and no body line starts with a word followed by a colon and a space,
  because the grammar cannot tell such a line from a trailer and stops
  reading the body there. Rewrap the sentence rather than reaching for
  `--no-verify`. Trailers come last, after a single blank line. `.cz.toml`
  is the sole executable authority for the allowed types, message grammar,
  and header length. Its interactive type choices explain each type; this
  policy governs commit usage and workflow.
- If commit-msg delivery is unconfirmed or diagnosis is needed, validate
  the draft with
  `cz check --message-length-limit 75 --message "feat(auth): Add login guard"`
  before starting the commit. Observe whether a `commit-msg` hook is actually
  installed; the configuration alone is not enforcement evidence. The remote
  candidate also validates the authenticated contributor commit range.

Immediately before an ordinary commit, stage the reviewed changes and run:

```bash
git commit -F /tmp/commit-message.txt
```

Prepare the message file before the command above. The read-only
pre-commit and commit-msg hooks actually observed on a normal commit check
the final index and message, so the same style checks on the same input are
not repeated beforehand. When delivery of the installed checks is
unconfirmed or a diagnosis is needed,
`scripts/validation/run-ci-precommit.sh --mode local-staged` checks an
isolated copy of the index with the registered pins. That controller
installs no hook and keeps the effective secret guard. On failure, fix,
review the diff, restage, and commit normally; when the index changes, an
earlier PASS is not reused. It never replaces a user-global hook or claims
automatic enforcement from configuration alone.

The diagnostic accepts the first staged tree before any branch commit and
reports an empty staged scope as `NOT_APPLICABLE`, without invoking checks.
It rechecks the source index tree and HEAD after inspecting the isolated
candidate; drift requires a new run against the current input. Cancellation
returns a signal exit and cleans its own temporary worktree. An unborn
diagnosis uses an unreferenced empty base for that worktree and does not
create or advance a source branch. These diagnostic results do not replace
the installed normal commit or remote candidate checks.

#### 2. Branching Strategy

- Protected baseline: `main`
- Short-lived human branches use `<type>/<short-description>`, where `type` is
  a `.cz.toml` change type; an existing intake Issue ID may precede the
  description. Do not create a duplicate Issue or copy the Spec/Task merely to
  satisfy a branch name.
- Emergency hotfix branches use `hotfix/<short-description>` and preserve the
  same PR, validation and explicit runtime authorization boundaries.
- Automation branch exceptions: `renovate/**` and `codex/**` are allowed for
  tool-generated PR branches only (Renovate is the sole dependency updater;
  see `docs/05.operations/02.policies/10.platform-and-backup/0086-dependency-version-management.md`). They must still merge through the PR
  protocol and required checks.
- Create a branch's linked worktree under the ignored `.worktrees/<branch>`
  directory. Remove a worktree and its merged branch when the work ends. A
  detached checkout that a script creates and removes inside its own scratch
  directory is not a branch worktree.
- Start a new branch or worktree from the latest committed state the work
  builds on, normally `main` after the previous pull request merged. Never
  stash, reset, discard, or force-commit uncommitted user work to make room;
  stop and ask instead.

#### 3. Pull Request Protocol

1. Self-review changes before opening or updating a PR.
2. Run focused authoring checks and inspect the selected prerequisites; the
   remote PR candidate owns aggregate QA. Do not repeat it before push or after
   merge for the same declared input/trust boundary.
3. Run document-link validation locally on the final source input before
   result-only Task evidence recording. Record its bound input and result in
   the Task. Result-only additions use minimum document checks; check new or
   changed link destinations only in that Task rather than repeating the whole
   corpus. Remote PR QA excludes the link leaf; metadata, relationship,
   lifecycle and applicable operations catalog checks remain.
4. For governance work, ensure linked stage docs remain accurate.
5. Apply the Completion Gate from `docs/00.workspace/03.process/github-governance.md` before declaring the PR done.
6. Mark incomplete work as Draft/WIP and do not request final review until the PR is ready. Merge readiness and branch lifecycle belong to `docs/00.workspace/03.process/github-governance.md` section 3.
7. A pull request carries the work of one Spec Package. It may hold several
   of that Spec's Tasks as separate logical commits, and it never mixes
   Specs.
8. Keep commits atomic and reviewable. Document any cleanup proposal in the PR;
   the recovery-commit and history-rewrite rules it must satisfy are owned by
   `docs/00.workspace/03.process/github-governance.md` section 3.
9. Request review only after self-review and programmatic checks pass. Summarize scope, risk, and how to verify so reviewers can act efficiently.
10. Incorporate review feedback explicitly: resolve or reply to each finding, re-run affected checks, and record what changed before re-requesting review.

#### 4. Operational Best Practices

- Use `fix` for user-visible or operational defect corrections and include regression evidence.
- Use `refactor` only for behavior-preserving structure changes and list checks that demonstrate unchanged behavior.
- Reference issue IDs, ADR IDs, or plan/task IDs when applicable.
- `.gitmessage` is an authoring aid for the `.cz.toml` grammar, which every
  consumer reads: the `commit-msg` hook and the pull request commit-range
  check. Only Git's and GitHub's automatic merge subjects are exempt
  (`allowed_prefixes`), by the owner's decision of 2026-11-14, so a
  `Merge branch 'main' into …` update commit passes; fixup and squash escapes
  stay disabled. GitHub's synthetic candidate merge is outside the validated
  contributor commit range.
- Main-targeted release-preparation PRs maintain `CHANGELOG.md` in Keep a
  Changelog form. No development push generates or publishes a changelog.
- Future release tags are `v` plus strict SemVer (`.cz.toml` `tag_format`). Do
  not push a tag independently; the release producer is defined in
  `docs/00.workspace/03.process/github-governance.md` section 8. Existing non-SemVer
  historical refs remain evidence; deleting or rewriting one needs the owner's
  approval for that ref.
- A specific release publication still requires its exact version, commit,
  approved target and recovery path. Select `RUN-0009` through the
  [platform and backup runbook index](../../05.operations/03.runbooks/10.platform-and-backup/README.md).

#### 5. Agent Completion Commit Discipline

- For repository-modifying agent work, the completion default is to create
  logical Conventional Commits after verification and before declaring the task
  done.
- Split commits by reviewable concern: documentation evidence, runtime hook
  behavior, validators, generated graph outputs, and similar units should not be
  mixed unless they are inseparable.
- Stage only files or hunks owned by the current task. Leave unrelated untracked
  files and user changes untouched.
- Do not commit when the user explicitly asks not to commit, the work is
  exploratory or incomplete, required checks/approvals are missing, or committing
  would include secrets or unrelated changes. In that case, report the reason and
  remaining state.

### Exceptions

#### Exception Conditions

No exception is granted here; a separately authorized operation follows [Approval boundaries](../04.quality/approval-boundaries.md).

#### Approval and Review

None: no exception exists to approve.

## Enforcement

### Mechanisms

#### 6. Enforcement

Changes that bypass checks or violate secret safety must not be merged.
GitHub-specific enforcement rules (branch protection, required checks, CODEOWNERS, Actions security) are governed by `docs/00.workspace/03.process/github-governance.md`.

#### 7. Git action stages

Each Git action is checked before, during or after it only where a real
trigger exists. A check after the fact records; it never claims to have
blocked. Client hooks can be bypassed with `--no-verify`, so only the server
rows are enforcement.

| Cell | Trigger and input | Action |
| --- | --- | --- |
| Commit before | `run-ci-precommit.sh --mode local-staged` on the index tree | Run only if installed delivery is unconfirmed or diagnosis is needed |
| Commit during | Installed `pre-commit` hook on the index; `commit-msg` hook on the message file | Run: blocks the commit |
| Commit after | No `post-commit` hook | Not applicable: nothing could block |
| Push before | Installed native `pre-push` guard on the pushed refs | Run: refuses any `refs/heads/main` update and nothing else; it runs no QA, because the pull request candidate owns it |
| Push during | GitHub branch protection on `main` | Observe: the server accepts or refuses |
| Push after | Git has no `post-push` hook; the `push` event on `main` runs `main-security` | Observe: security audit of the merged input |
| PR before | No hook. The agent runs `python3 scripts/validation/run-ci-gate.py --profile changed` (inspect with `--explain`) on the final source, including the local candidate preflight when selected, then fills every section of `.github/PULL_REQUEST_TEMPLATE.md` | Observe: a local, advisory route; opening a PR is a separate remote write, and no gate reads the PR body |
| PR during | `pull_request` `opened`, `synchronize` or `reopened`; candidate shard jobs and the `candidate-quality` aggregate | Run: required check on the merge candidate |
| PR after | Gate evidence artifacts per shard | Observe: each artifact is bound to its run |
| Merge before | Branch protection: strict up to date, required `candidate-quality`, resolved conversations | Run (server): blocks the merge |
| Merge during | Merge commit only; no merge queue | Not applicable: no queue, and the strict rule already tested this tree |
| Merge after | `push` on `main` | Reuse: the merged tree equals the checked candidate; `main-security` runs |

The `pull_request` types stay `opened`, `synchronize` and `reopened`, decided
from the inputs the candidate actually reads. Those are the base, head and merge
commits, never the PR title, body or draft state: no job condition filters on
`draft`, and no gate consumes `github.event.pull_request.title` or `.body`.
`edited` therefore changes no gate input and `ready_for_review` changes no
checked tree, and neither type is added. A later check that reads the PR body
must add `edited` in the same change, and a check that skips draft PRs must add
`ready_for_review`; the workflow contract rejects any trigger type it does not
list.

SDLC phases and document Stages are separate axes from these cells, and the
current Task records each binding's evidence.

### Limits

Only the commit grammar rows and the merge-subject exemption name a check, and deleting a historical ref rests on owner approval; the other rules name none.

- Commit standards outside the grammar (R2, R6-R8, R11-R14) name no check; the `cz check` route is an optional diagnosis, not enforcement.
- Ordinary-commit and local-staged diagnosis rules (R15-R21) name no check; the local-staged run is an optional diagnosis.
- Branching, worktree and new-branch-start rules (R22-R36) name no check.
- Pull request protocol steps (R37-R59) name no check.
- Operational best practices (R60-R64, R66-R72, R74-R75) name no check.
- Deleting or rewriting a historical ref (R73) rests on the owner's approval for that ref.
- Agent completion commit discipline (R76-R81) names no check.
- The policy states that client hooks, including the `commit-msg` hook named for the grammar rows, can be bypassed with `--no-verify`.
- Rules stated under Enforcement / Mechanisms are outside this table.

## Ownership

### Owner

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](../04.quality/approval-boundaries.md#authorization-source-and-records)).

### Review Triggers

Changes land in place with Task evidence; related documents:

- [Quality standards](../04.quality/quality-standards.md)
- [Operations runbook index](../../05.operations/03.runbooks/README.md)
- [GitHub governance](github-governance.md)
- [Bootstrap policy](../../../.agents/governance/bootstrap.md)
