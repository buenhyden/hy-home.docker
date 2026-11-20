---
title: "Commit Message Prompt"
version: "1.0.0"
type: "governance/prompt"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: Commit Message Prompt
  layer: agent
updated: "2026-11-20"
created: "2026-09-06"
---

# Commit Message Prompt

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the prompt payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Purpose

Draft a Conventional Commit message from the staged diff so the message
describes what the commit actually changes. The draft is reviewed by a human or
by the repository's own commit-message validation before it is used; this prompt
produces a draft, never a commit.

#### Inputs

- `git diff --staged --stat` and `git diff --staged`, so the message is derived
  from staged content rather than from intent.
- `git status --porcelain`, so unstaged work is visible and excluded from the
  message.
- The governing Plan work unit this commit closes.
- The current worktree and staged-set digest, plus current approval validity.
- The commit conventions in
  [git workflow](../../docs/00.workspace/03.process/git-workflow.md), which governs commit usage.
  `.cz.toml` owns the type vocabulary and descriptions, message grammar,
  and header length.

Stop and request staging if the staged set is empty or spans unrelated concerns.
Stop the draft for stale or partial inputs, worktree disagreement, or revoked
approval. This prompt never commits or claims check results.

#### Instructions

##### Constraints

- Describing unstaged, planned, or intended work.
- Claiming a verification result the commit does not carry. A message never
  asserts that a check passed; the Task owns that evidence.
- Inventing a scope, type, or trailer the conventions do not define.
- Bypassing commit-message validation, running the commit with a verification
  bypass flag, or using an arbitrary skip list to silence a hook.
- Creating the commit. This prompt ends at the draft.
- Secret values, credentials, tokens, private paths, or raw log excerpts.

##### Applies To

- Roles: any role authorized to commit within its approved Task scope. Drafting
  a message grants no commit authorization by itself.
- Skills: [change-review-execution](../skills/change-review-execution/SKILL.md)
  owns the review-then-commit ordering; this prompt owns only the message
  envelope.
- Evaluation: the draft is adequate when every staged path is accounted for,
  the subject names one logical change, and the body states a reason that the
  diff alone does not convey.

#### Outputs

One draft message:

1. **Subject** — `<type>[(<scope>)][!]: <Description>`, where brackets denote
   optional parts rather than literal characters, with the full header within
   the repository's configured length limit. The type comes from `.cz.toml`'s
   `change_type_map`; the scope names the changed authority surface, not a
   directory listing.
2. **Body** — what changed and why, in the shape the conventions define. It
   states the reason a reader cannot recover from the diff itself and omits
   anything the diff already shows plainly.
3. **Trailers** — only trailers the repository's conventions define.

Offer the draft for the ordinary commit path when commit-msg delivery is
confirmed. When delivery is unconfirmed or diagnosis is needed, validate
the draft with Commitizen:

```bash
cz check --message-length-limit 75 \
  --message "docs(governance): Align commit contract"
```

Explicit Commitizen validation checks the full grammar. Claim `commit-msg`
hook enforcement only when its installation and delivery are observed. The
remote candidate validates the authenticated contributor commit range separately.

Alongside the draft, list any staged path the message does not account for. That
list being empty is part of the output.

#### Failure Handling

If the staged set mixes unrelated logical changes, report the split rather than
writing a message that covers both; the correct fix is restaging, not looser
wording. If a staged path cannot be explained from the diff, say so and stop.
If message validation rejects the draft, correct the draft against the stated
rule; never disable the validation.

#### Related Documents

- [Prompt index](README.md)
- [Git workflow](../../docs/00.workspace/03.process/git-workflow.md)
- [Task checklists](../../docs/00.workspace/04.quality/task-checklists.md)
- [Postflight routing](../governance/postflight-checklist.md)

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
