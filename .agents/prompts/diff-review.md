---
title: "Diff Review Prompt"
version: "0.1.0"
type: "governance/prompt"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-06"
created: "2026-09-06"
---

# Diff Review Prompt

## Purpose

Review one exact diff independently of the contributor who produced it. The
review judges the diff against the governing acceptance contract and the
repository's own guards, not against a general sense of code quality.

## Required Inputs

- The exact diff under review, produced by a named command such as
  `git diff`, `git diff --staged`, or `git diff <base>...HEAD`. The command and
  its arguments are part of the input; a paraphrased or partial diff is not.
- The governing Spec's `Acceptance Contract` and the Plan work unit the diff
  claims to satisfy.
- The verification results the contributor recorded, with their exit codes.
- The protected-surface table in
  [approval boundaries](../governance/approval-boundaries.md).

Stop and request the exact diff command if the change set cannot be reproduced.

## Output Contract

A findings list, most severe first. Each finding carries:

1. **Severity** — `blocker`, `high`, `medium`, or `low`.
2. **Location** — `file:line` inside the reviewed diff.
3. **Claim** — one sentence stating the defect.
4. **Failure scenario** — the concrete input or state that produces the wrong
   outcome. A finding without one is a suggestion, not a defect, and is
   labelled as such.
5. **Owner** — the canonical owner that must resolve it.

After the findings, a disposition: `approve`, `approve with follow-up`, or
`block`, plus one line naming what the review did not cover.

An empty findings list is a valid result and is stated explicitly.

## Prohibited

- Reviewing your own implementation as if independent. Independence means the
  reviewer did not write the diff; say so plainly when that is not the case.
- Approving on the strength of a passing check the reviewer did not see, or
  treating a configured hook, a static parity check, or a renderer result as
  runtime, entitlement, Hosted CI, or remote acceptance.
- Requesting changes outside the diff's approved scope. Out-of-scope
  observations are reported separately as advisory, never as blockers.
- Editing files. A reviewer reports; the owner resolves.
- Recording a review disposition that was not actually performed.
- Weakening a guard, threshold, fixture, or negative test to make the diff pass.

## Failure Handling

If the diff cannot be reproduced from the stated command, stop and report that
before reviewing anything. If the diff touches a protected surface without the
required evidence, raise a `blocker` naming the missing evidence rather than
inferring approval. If the acceptance contract and the diff disagree about
intent, report the conflict to the owning Spec instead of choosing a reading.

## Applies To

- Roles: `code-reviewer`, `security-auditor`, `iac-reviewer`, and
  `qa-engineer` consume this prompt within their own read-only permission
  profile. The reviewer is never the implementer of the same change.
- Skills: [code-review-dimensions](../skills/code-review-dimensions/SKILL.md)
  and [change-review-execution](../skills/change-review-execution/SKILL.md) own
  the review dimensions and execution procedure; this prompt owns only the
  input and output envelope.
- Evaluation: the review is adequate when every `blocker` names a reproducible
  failure scenario, every claim cites a location inside the reviewed diff, and
  the uncovered area is stated rather than left implicit.

## Related Documents

- [Prompt index](README.md)
- [Quality standards](../governance/quality-standards.md)
- [Approval boundaries](../governance/approval-boundaries.md)
- [Workflows](../governance/workflows.md)
