---
title: "Git Workflow Governance"
version: "1.9.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
---

# Git Workflow Governance

## Purpose and Scope

### Objective

This rule defines the mandatory git workflow for all contributors and agents.

#### Authority

This policy is the canonical owner of local Git authoring, branch integration, commits, review, and remote delivery boundaries under [bootstrap precedence](bootstrap.md#authority-and-precedence).

### Applies To

Local Git authoring, branch integration, commits, review, and remote delivery boundaries.

#### Exclusions

None: this document states no exclusion.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| GIT-WORKFLOW-R1 | Every commit | Required: use Conventional Commits `<type>[(<scope>)][!]: <Description>` with explicit scopes where possible | `.cz.toml` / installed `commit-msg` hook / remote contributor commit-range check | Hook observation or `cz check` output |
| GIT-WORKFLOW-R2 | Every commit | Required: types are the keys in `change_type_map` of `.cz.toml` | `.cz.toml` `change_type_map` | none |
| GIT-WORKFLOW-R3 | Every commit | Required: description starts with a capital letter and does not end with a period | `.cz.toml` grammar | none |
| GIT-WORKFLOW-R4 | Every commit | Required: body is one block with no blank line and no line starting with a word followed by a colon and a space | `.cz.toml` grammar | none |
| GIT-WORKFLOW-R5 | A body line reads like a trailer | Required: rewrap the sentence; Forbidden: reaching for `--no-verify` | none | none |
| GIT-WORKFLOW-R6 | Every commit | Required: trailers come last after a single blank line | `.cz.toml` grammar | none |
| GIT-WORKFLOW-R7 | Every commit | Required: header length stays within the `.cz.toml` limit | `.cz.toml` / `cz check --message-length-limit 75` | none |
| GIT-WORKFLOW-R8 | commit-msg delivery is unconfirmed or diagnosis is needed | Required: validate the draft with `cz check --message-length-limit 75 --message ...` before starting the commit | none | `cz check` output |
| GIT-WORKFLOW-R9 | Judging commit enforcement | Required: observe whether a `commit-msg` hook is actually installed; configuration alone is not enforcement evidence | none | Hook observation |
| GIT-WORKFLOW-R10 | An ordinary commit | Required: stage the reviewed changes, prepare the message file, then run `git commit -F /tmp/commit-message.txt` | none | none |
| GIT-WORKFLOW-R11 | An ordinary commit | Forbidden: repeating the style checks on the same input beforehand that the observed pre-commit and commit-msg hooks run | none | none |
| GIT-WORKFLOW-R12 | Delivery of installed checks unconfirmed or diagnosis needed | Allowed: run `scripts/validation/run-ci-precommit.sh --mode local-staged` on an isolated copy of the index with the registered pins; it installs no hook and keeps the effective secret guard | `scripts/validation/run-ci-precommit.sh --mode local-staged` | none |
| GIT-WORKFLOW-R13 | The local-staged check fails | Required: fix, review the diff, restage and commit normally | none | none |
| GIT-WORKFLOW-R14 | The index changes | Forbidden: reusing an earlier PASS | none | none |
| GIT-WORKFLOW-R15 | Always | Forbidden: claiming automatic enforcement from configuration alone or replacing a user-global hook | none | none |
| GIT-WORKFLOW-R16 | Branching | Required: keep `main` as the protected baseline | none | none |
| GIT-WORKFLOW-R17 | A short-lived human branch | Required: name it `<type>/<short-description>` with `type` a `.cz.toml` change type; an existing intake Issue ID may precede the description | none | none |
| GIT-WORKFLOW-R18 | Naming a branch | Forbidden: creating a duplicate Issue or copying the Spec/Task merely to satisfy a branch name | none | none |
| GIT-WORKFLOW-R19 | An emergency hotfix | Required: use `hotfix/<short-description>` and preserve the same PR, validation and explicit runtime authorization boundaries | none | none |
| GIT-WORKFLOW-R20 | Tool-generated PR branches | Allowed: `renovate/**` and `codex/**` branches for tool-generated PR branches only | none | none |
| GIT-WORKFLOW-R21 | An automation branch | Required: merge through the PR protocol and required checks | none | none |
| GIT-WORKFLOW-R22 | A branch's linked worktree | Required: create it under the ignored `.worktrees/<branch>` directory | none | none |
| GIT-WORKFLOW-R23 | Work ends | Required: remove the worktree and its merged branch | none | none |
| GIT-WORKFLOW-R24 | A detached checkout a script creates and removes in its own scratch directory | Allowed: it is not a branch worktree | none | none |
| GIT-WORKFLOW-R25 | Starting a new branch or worktree | Required: start from the latest committed state the work builds on, normally `main` after the previous PR merged | none | none |
| GIT-WORKFLOW-R26 | Making room for a new branch or worktree | Forbidden: stashing, resetting, discarding or force-committing uncommitted user work | none | none |
| GIT-WORKFLOW-R27 | Uncommitted user work blocks a new branch or worktree | Required: stop and ask | none | none |
| GIT-WORKFLOW-R28 | A PR is opened or updated | Required: self-review changes first | none | none |
| GIT-WORKFLOW-R29 | A PR is opened or updated | Required: run focused authoring checks and inspect the selected prerequisites | none | none |
| GIT-WORKFLOW-R30 | The same declared input and trust boundary | Forbidden: repeating the aggregate QA the remote PR candidate owns before push or after merge | none | none |
| GIT-WORKFLOW-R31 | A PR is opened or updated | Required: run document-link validation locally on the final source input before result-only Task evidence recording and record its bound input and result in the Task | none | Task record of the bound input and result |
| GIT-WORKFLOW-R32 | A result-only addition | Required: use minimum document checks and check only new or changed link destinations in that Task | none | none |
| GIT-WORKFLOW-R33 | Governance work | Required: ensure linked stage docs remain accurate | none | none |
| GIT-WORKFLOW-R34 | Declaring a PR done | Required: apply the Completion Gate from `.agents/governance/github-governance.md` | none | none |
| GIT-WORKFLOW-R35 | Work is incomplete | Required: mark the PR Draft/WIP; Forbidden: requesting final review until it is ready | none | none |
| GIT-WORKFLOW-R36 | A PR | Required: carry the work of one Spec Package, possibly several of its Tasks as separate logical commits; Forbidden: mixing Specs | none | none |
| GIT-WORKFLOW-R37 | Commits | Required: keep commits atomic and reviewable | none | none |
| GIT-WORKFLOW-R38 | A cleanup proposal | Required: document it in the PR and satisfy the recovery-commit and history-rewrite rules in `github-governance.md` section 3 | none | none |
| GIT-WORKFLOW-R39 | Requesting review | Required: request only after self-review and programmatic checks pass, and summarize scope, risk and how to verify | none | none |
| GIT-WORKFLOW-R40 | Review feedback | Required: resolve or reply to each finding, re-run affected checks and record what changed before re-requesting review | none | none |
| GIT-WORKFLOW-R41 | A user-visible or operational defect correction | Required: use `fix` and include regression evidence | none | none |
| GIT-WORKFLOW-R42 | A structure change | Required: use `refactor` only for behavior-preserving changes and list checks that show unchanged behavior | none | none |
| GIT-WORKFLOW-R43 | Applicable IDs exist | Required: reference issue IDs, ADR IDs or plan/task IDs | none | none |
| GIT-WORKFLOW-R44 | A Git or GitHub automatic merge subject | Allowed: it is exempt from the grammar through `allowed_prefixes` by the owner's decision of 2026-11-14 | `.cz.toml` `allowed_prefixes` | none |
| GIT-WORKFLOW-R45 | A commit message | Forbidden: using fixup or squash escapes | none | none |
| GIT-WORKFLOW-R46 | A main-targeted release-preparation PR | Required: maintain `CHANGELOG.md` in Keep a Changelog form | none | none |
| GIT-WORKFLOW-R47 | A development push | Forbidden: generating or publishing a changelog | none | none |
| GIT-WORKFLOW-R48 | A future release tag | Required: `v` plus strict SemVer | `.cz.toml` `tag_format` | none |
| GIT-WORKFLOW-R49 | Pushing a tag | Forbidden: pushing a tag independently; the release producer is defined in `github-governance.md` section 8 | none | none |
| GIT-WORKFLOW-R50 | An existing non-SemVer historical ref | Required: keep it as evidence; deleting or rewriting one needs the owner's approval for that ref | manual | none |
| GIT-WORKFLOW-R51 | A specific release publication | Required: have its exact version, commit, approved target and recovery path, and select `RUN-0009` through the platform and backup runbook index | none | none |
| GIT-WORKFLOW-R52 | Repository-modifying agent work | Required: create logical Conventional Commits after verification and before declaring the task done | none | none |
| GIT-WORKFLOW-R53 | Repository-modifying agent work | Required: split commits by reviewable concern unless inseparable | none | none |
| GIT-WORKFLOW-R54 | Repository-modifying agent work | Required: stage only files or hunks owned by the current task and leave unrelated untracked files and user changes untouched | none | none |
| GIT-WORKFLOW-R55 | The user asks not to commit, work is exploratory or incomplete, checks or approvals are missing, or the commit would include secrets or unrelated changes | Forbidden: committing | none | none |
| GIT-WORKFLOW-R56 | A commit is withheld | Required: report the reason and remaining state | none | Report of reason and remaining state |

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
  see `docs/05.operations/policies/10-platform-and-backup/0086-dependency-version-management.md`). They must still merge through the PR
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
5. Apply the Completion Gate from `.agents/governance/github-governance.md` before declaring the PR done.
6. Mark incomplete work as Draft/WIP and do not request final review until the PR is ready. Merge readiness and branch lifecycle belong to `.agents/governance/github-governance.md` section 3.
7. A pull request carries the work of one Spec Package. It may hold several
   of that Spec's Tasks as separate logical commits, and it never mixes
   Specs.
8. Keep commits atomic and reviewable. Document any cleanup proposal in the PR;
   the recovery-commit and history-rewrite rules it must satisfy are owned by
   `.agents/governance/github-governance.md` section 3.
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
  `.agents/governance/github-governance.md` section 8. Existing non-SemVer
  historical refs remain evidence; deleting or rewriting one needs the owner's
  approval for that ref.
- A specific release publication still requires its exact version, commit,
  approved target and recovery path. Select `RUN-0009` through the
  [platform and backup runbook index](../../docs/05.operations/runbooks/10-platform-and-backup/README.md).

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

No exception is granted here; a separately authorized operation follows [Approval boundaries](approval-boundaries.md).

#### Approval and Review

None: no exception exists to approve.

## Enforcement

### Mechanisms

#### 6. Enforcement

Changes that bypass checks or violate secret safety must not be merged.
GitHub-specific enforcement rules (branch protection, required checks, CODEOWNERS, Actions security) are governed by `.agents/governance/github-governance.md`.

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

Only the commit grammar and the server-side rows are mechanically enforced; the remaining rules rest on review or agent discipline.

- Client hooks can be bypassed with `--no-verify`; only the server rows are enforcement, and whether a `commit-msg` hook is installed must be observed (R5, R9).
- Commit workflow steps and the local-staged diagnosis rules (R10-R11, R13-R15) name no check.
- Branch naming, worktree and new-branch-start rules name no check (R17-R27).
- Pull request protocol steps (R28-R40) rest on review; no gate reads the PR body, and the local `--profile changed` run is advisory.
- Operational best practices (R41-R51) rest on review; only release tag format is tied to `.cz.toml`, and historical refs need owner approval.
- Agent completion commit discipline (R52-R56) rests on agent judgment and user instruction.
- GIT-WORKFLOW-R8, GIT-WORKFLOW-R16, GIT-WORKFLOW-R29: the policy names a route but does not tie a gate to the rule.

## Ownership

### Owner

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](approval-boundaries.md#authorization-source-and-records)).

### Review Triggers

Changes land in place with Task evidence; related documents:

- [Quality standards](quality-standards.md)
- [Operations runbook index](../../docs/05.operations/runbooks/README.md)
- [GitHub governance](github-governance.md)
- [Bootstrap policy](bootstrap.md)
