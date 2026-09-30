---
title: "Agent Native Observation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-30"
layer: "specs"
artifact_id: "SPEC-0195-PLAN-0001"
parent_ids:
- "SPEC-0195"
created: "2026-09-30"
---

# Agent Native Observation Plan

## Objective

Observe only the transferred native obligations after separate execution
approval, preserving the original acceptance and evidence boundaries.

## Dependencies

- [Spec](spec.md) and SPEC-0194 delivery evidence at its reviewed revision.
- Original hardening packet c86f55518b8a9a156e10e38fbd52d1a883063d6a.
- Installed native tools, synthetic targets, an independent reviewer, and
  explicit observation approval. No dependency installation is authorized.

## Execution Sequence

1. W1: Reconcile the transferred R04/R15/R18/R19/R22 receipts with SPEC-0194.
   Identify installed versions and propose exact synthetic targets, actions,
   refusal cases, and cleanup owners for criteria 1-5. Record original Plan
   model-entitlement requirements separately from static model configuration.
2. W2: Obtain concrete execution approval and provider/account context without
   reading authentication files. State call/token/time/concurrency/retry/spend
   limits and available supported hard enforcement. Unsupported enforcement
   keeps criterion 4 BLOCKED; do not add an inference gateway or guess controls.
3. W3: Observe approved native hook delivery and explicit skill/role invocation
   for both providers, separately from syntax and deterministic regressions
   (criteria 1-2). Preserve denied or failed results.
4. W4: Observe the approved editor action/selection with unchanged bindings
   (criterion 3), supported entitlement/budget enforcement (criterion 4), and
   cross-provider handoff refusal plus valid resumption (criterion 5).
5. W5: Obtain independent read-only review of each receipt against the same
   revision. Complete only when all applicable criteria are evidenced; preserve
   BLOCKED/NOT_RUN and keep this package open otherwise.

## Risk and Rollback

No blanket provider, service, secret, global configuration, or spending authority.
Stop before unapproved actions. Synthetic target ownership and cleanup must be
explicit; preserve pre-existing paths and user bindings. Record partial evidence
instead of rerunning indefinitely or silently switching providers/models.

## Verification

Use existing syntax, hook, and handoff regressions for their encoded invariants.
For criteria 1-5, record actual authorized native observations, exact version and
revision, result metadata, and independent review in the Task. No static test
substitutes for those observations. Coverage and delivery gates stay in SPEC-0194.

## Rulings

- The user approved separate follow-up ownership on 2026-09-30, not execution.
- Missing tools or unsupported controls do not waive acceptance.
- Real recovery is outside this package; R27 requires read-only contract review.
