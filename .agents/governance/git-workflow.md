---
title: "Git Workflow Governance"
version: "1.4.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-29"
---

# Git Workflow Governance

## Overview

This rule defines the mandatory git workflow for all contributors and agents.

## Scope

Local Git authoring, branch integration, commits, review, and remote delivery boundaries.

## Rules

### 1. Commit Standards

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

메시지 파일은 위 명령 전에 준비한다. 정상 커밋에서 실제 관측한 읽기 전용
pre-commit·commit-msg hook이 최종 index와 메시지를 검사하며 같은 입력의
스타일 검사를 미리 반복하지 않는다. 설치된 검사의 전달이 확인되지 않았거나
진단이 필요하면 `scripts/validation/run-ci-precommit.sh --mode local-staged`가
등록 pin으로 index의 격리 복사본을 검사한다. 이 제어기는 hook을 설치하지
않으며 유효한 secret guard를 보존한다. 실패하면 수정·diff 검토·재staging
후 정상 커밋하고, index가 바뀌면 이전 PASS를 재사용하지 않는다.
user-global hook을 대체하거나 설정만으로 자동 강제를 주장하지 않는다.

### 2. Branching Strategy

- Protected baseline: `main`
- Short-lived human branches use `<type>/<short-description>`; an existing
  intake Issue ID may precede the description. Do not create a duplicate Issue
  or copy the Spec/Task merely to satisfy a branch name.
- Emergency hotfix branches use `hotfix/<short-description>` and preserve the
  same PR, validation and explicit runtime authorization boundaries.
- Other human-authored branches use `<type>/<short-description>`, where `type`
  is an admitted `.cz.toml` change type other than `feat` or `fix`.
- Automation branch exceptions: `dependabot/**` and `codex/**` are allowed for
  tool-generated PR branches only. They must still merge through the PR
  protocol and required checks.
- Create linked worktrees under the ignored `.worktrees/<branch>` directory.
  Remove a worktree and its merged branch when the work ends.

### 3. Pull Request Protocol

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
7. Keep commits atomic and reviewable. Document any cleanup proposal in the PR;
   the recovery-commit and history-rewrite rules it must satisfy are owned by
   `.agents/governance/github-governance.md` section 3.
8. Request review only after self-review and programmatic checks pass. Summarize scope, risk, and how to verify so reviewers can act efficiently.
9. Incorporate review feedback explicitly: resolve or reply to each finding, re-run affected checks, and record what changed before re-requesting review.

### 4. Operational Best Practices

- Keep commits atomic.
- Use `fix` for user-visible or operational defect corrections and include regression evidence.
- Use `refactor` only for behavior-preserving structure changes and list checks that demonstrate unchanged behavior.
- Never commit plaintext secrets.
- Reference issue IDs, ADR IDs, or plan/task IDs when applicable.
- `.cz.toml` owns the one Commitizen grammar; `.gitmessage` is an authoring
  aid. Explicit Commitizen validation gives local feedback; hook delivery is
  claimed only when actually observed. The remote
  candidate verifies its authenticated contributor commit range because client
  hook installation is not trusted evidence. Default Merge/fixup prefix escapes
  are disabled; GitHub's synthetic candidate merge is outside that range. Feature push does not add another public gate.
- Main-targeted release-preparation PRs maintain `CHANGELOG.md` in Keep a
  Changelog form. No development push generates or publishes a changelog.
- Future release tags are `v` plus strict SemVer. The manual main-only release
  workflow is their sole producer and owns create-only tag plus draft Release,
  complete assets, then publication. Do not push a tag independently or add a
  moving channel producer. Existing non-SemVer historical refs remain evidence;
  deleting or rewriting one needs the owner's approval for that ref.
- A specific release publication still requires its exact version, commit,
  approved target and recovery path. Select `RUN-0009` through the
  [Operations runbook index](../../docs/05.operations/runbooks/README.md#cross-cutting-workspace).

### 5. Agent Completion Commit Discipline

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

## Exceptions

No exception is granted here; a separately authorized operation follows [Approval boundaries](approval-boundaries.md).

## Verification

### 6. Enforcement

Changes that bypass checks or violate secret safety must not be merged.
GitHub-specific enforcement rules (branch protection, required checks, CODEOWNERS, Actions security) are governed by `.agents/governance/github-governance.md`.

## Related Documents

- `.agents/governance/github-governance.md`
- `.agents/governance/quality-standards.md`
- [Operations runbook index](../../docs/05.operations/runbooks/README.md)
