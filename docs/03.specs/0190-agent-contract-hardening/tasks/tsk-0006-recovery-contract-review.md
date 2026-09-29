---
title: "Read-Only Recovery Contract Review"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0190-TSK-0006"
parent_ids:
- "SPEC-0190"
- "SPEC-0190-PLAN-0001"
created: "2026-09-29"
---

# Read-Only Recovery Contract Review

## Objective

Implement Plan W6: add an explicitly invoked read-only recovery-readiness
review with one canonical owner, bounded role routing and native projections.
This reviews a sanitized contract; it never executes or approves a restore.

## Inputs

- [Approved Spec](../spec.md) and [approved Plan](../plan.md); W5 `c2bad7a6e`.
- Existing user approval covers local implementation, tests, independent review
  and logical commits. No installation, paid/native call, remote or runtime action.
- Primary writer: skill-creator; native contributor: hook-developer;
  independent reviewers: iac-reviewer and rules-engineer. Root owns this Task.
- Exact source, test and generated paths are the finite W6 map in the Plan.
  Four new skill files only; no new script, framework, manifest or Codex skill copy.

## Work Log

Read-only preparation confirmed that existing registry fields, renderer and
prompt ROUTES support the addition. Existing resource validation admits the
reference and verdict asset when directly linked from the skill body.
W5 released shared-test ownership after its reviewed logical commit.

## Verification Evidence

NOT_RUN: P RED/GREEN, G/H/C, skill validation, renderer source preservation and
second-run stability. New skill starts draft 0.1.0, then follows actual committed
review and active predecessors; lifecycle approval is not invented by generation.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| R01/R02/R05/R24/R27/R28/R29/R35/R36/R37 | W6 | NOT_RUN | Recovery review skill, existing roles and provider consumers |

## Review Evidence

Independent read-only IaC and policy review pending. Verify named implementer,
reviewer and human approver remain distinct, readiness never means successful
recovery, and an ambiguous or operational request cannot gain execution rights.

## Commit Ledger

Root validates and commits Task draft, ready and in-progress predecessors before
implementation GO. New skill lifecycle commits retain their actual prior states.

## Rulings

- Apply the installed system skill-creator procedure within the approved exact
  four-file design; do not create initializer extras or generic UI metadata.
- Only iac-reviewer gains the new read-only skill. Other roles/skills route to it.
- Register SKILL.md and agents/openai.yaml; resources remain skill-owned.
- New tracked resources and the generated Claude skill must be staged before
  fixture tests whose safe copier uses git ls-files. Root controls the index.
- Preserve model, reasoning and needs_revalidation facts. W9 owns thresholds
  after its fixture exists and the user-directed evaluation migration.

## Deferred Items

W9 owns recovery evaluation scenarios. W10 owns full branch and live/native
acceptance; static routing and generated parity cannot close those observations.
