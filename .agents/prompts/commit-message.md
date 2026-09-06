---
title: "Commit Message Prompt"
version: "0.1.0"
type: "governance/prompt"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-06"
created: "2026-09-06"
---

# Commit Message Prompt

## Purpose

Draft a Conventional Commit message from the staged diff so the message
describes what the commit actually changes. The draft is reviewed by a human or
by the repository's own commit-message validation before it is used; this prompt
produces a draft, never a commit.

## Required Inputs

- `git diff --staged --stat` and `git diff --staged`, so the message is derived
  from staged content rather than from intent.
- `git status --porcelain`, so unstaged work is visible and excluded from the
  message.
- The governing Plan work unit this commit closes.
- The commit conventions in
  [git workflow](../governance/git-workflow.md), which own type, scope, and
  message shape. The repository's commit-message check enforces that shape from
  `.cz.toml`; read the documented rules rather than inferring them from a
  sample.

Stop and request staging if the staged set is empty or spans unrelated
concerns.

## Output Contract

One draft message:

1. **Subject** — `<type>(<scope>): <Description>` within the repository's
   configured length limit. The type comes from the conventions document; the
   scope names the changed authority surface, not a directory listing.
2. **Body** — what changed and why, in the shape the conventions define. It
   states the reason a reader cannot recover from the diff itself and omits
   anything the diff already shows plainly.
3. **Trailers** — only trailers the repository's conventions define.

Validate the draft against the enforced pattern before offering it. A message
that fails the commit-message check after a long pre-commit run wastes the whole
run, so check the cheapest gate first.

Alongside the draft, list any staged path the message does not account for. That
list being empty is part of the output.

## Prohibited

- Describing unstaged, planned, or intended work.
- Claiming a verification result the commit does not carry. A message never
  asserts that a check passed; the Task owns that evidence.
- Inventing a scope, type, or trailer the conventions do not define.
- Bypassing commit-message validation, running the commit with a verification
  bypass flag, or using an arbitrary skip list to silence a hook.
- Creating the commit. This prompt ends at the draft.
- Secret values, credentials, tokens, private paths, or raw log excerpts.

## Failure Handling

If the staged set mixes unrelated logical changes, report the split rather than
writing a message that covers both; the correct fix is restaging, not looser
wording. If a staged path cannot be explained from the diff, say so and stop.
If message validation rejects the draft, correct the draft against the stated
rule; never disable the validation.

## Applies To

- Roles: any role authorized to commit within its approved Task scope. Drafting
  a message grants no commit authorization by itself.
- Skills: [change-review-execution](../skills/change-review-execution/SKILL.md)
  owns the review-then-commit ordering; this prompt owns only the message
  envelope.
- Evaluation: the draft is adequate when every staged path is accounted for,
  the subject names one logical change, and the body states a reason that the
  diff alone does not convey.

## Related Documents

- [Prompt index](README.md)
- [Git workflow](../governance/git-workflow.md)
- [Task checklists](../governance/task-checklists.md)
- [Postflight routing](../governance/postflight-checklist.md)
