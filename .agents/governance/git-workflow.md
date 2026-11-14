---
title: "Git Workflow Governance"
version: "1.8.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-14"
---

# Git Workflow Governance

## Purpose

### Objective

This rule defines the mandatory git workflow for all contributors and agents.

### Authority

This policy is the canonical owner of local Git authoring, branch integration, commits, review, and remote delivery boundaries under [bootstrap precedence](bootstrap.md#authority-and-precedence).

## Scope

### Applies To

Local Git authoring, branch integration, commits, review, and remote delivery boundaries.

### Exclusions

None: this document states no exclusion.

## Rules

### Requirements

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
- Validate a draft with
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

### Enforcement

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
| Commit before | `run-ci-precommit.sh --mode local-staged` on the index tree | Run: the agent route before a commit |
| Commit during | Installed `pre-commit` hook on the index; `commit-msg` hook on the message file | Run: blocks the commit |
| Commit after | No `post-commit` hook | Not applicable: nothing could block |
| Push before | Installed native `pre-push` guard on the pushed refs | Run: refuses any `refs/heads/main` update and nothing else; it runs no QA, because the pull request candidate owns it |
| Push during | GitHub branch protection on `main` | Observe: the server accepts or refuses |
| Push after | Git has no `post-push` hook; the `push` event on `main` runs `main-security` | Observe: security audit of the merged input |
| PR before | No hook. The agent runs `python3 scripts/validation/run-ci-gate.py --profile changed` (inspect with `--explain`) and the local candidate preflight (`scripts/validation/check-candidate-preflight.sh`) on the final source, then fills every section of `.github/PULL_REQUEST_TEMPLATE.md` | Observe: a local, advisory route; opening a PR is a separate remote write, and no gate reads the PR body |
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

## Exceptions

### Exception Conditions

No exception is granted here; a separately authorized operation follows [Approval boundaries](approval-boundaries.md).

### Approval and Review

None: no exception exists to approve.

## Ownership

### Responsibilities

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](approval-boundaries.md#authorization-source-and-records)).

### Change and Adoption

Changes land in place with Task evidence; related documents:

- [Quality standards](quality-standards.md)
- [Operations runbook index](../../docs/05.operations/runbooks/README.md)
- [GitHub governance](github-governance.md)
- [Bootstrap policy](bootstrap.md)
