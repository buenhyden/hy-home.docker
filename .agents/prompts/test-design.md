---
title: "Test Design Prompt"
version: "0.1.0"
type: "governance/prompt"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-06"
created: "2026-09-06"
---

# Test Design Prompt

## Purpose

Derive tests from a stated requirement and its failure conditions, so the tests
encode the contract rather than the current implementation. A test written from
the implementation passes by construction and proves nothing.

## Required Inputs

- The requirement or acceptance criterion under test, quoted from its owning
  Requirement, Spec, or contract document.
- The failure conditions the requirement implies: the inputs, states, or
  sequences that must be rejected, bounded, or recovered from.
- The existing test owner for the surface, so a new test extends the right
  module instead of creating a parallel suite.
- The boundary between library behavior and command-line behavior, because this
  repository separates `tests/lib/` from `tests/validation/`.

Stop and route to the owning stage if the requirement does not state an
observable outcome.

## Output Contract

For each behavior:

1. **Name** — a test name that states the behavior, not the function called.
2. **Arrange, act, assert** — the three parts kept visibly separate.
3. **Expected failure first** — the assertion and the exact failure message
   expected before the implementation exists, so the RED state is observable
   rather than assumed.
4. **Negative case** — at least one case proving the guard rejects what it must
   reject. Permission, path escape, symlink, refusal, retry bound, and
   canonical-source protection cases are kept even when they are the only
   failing case.
5. **Placement** — the exact module path the test belongs in, and why that module
   rather than a new one.

State which inputs are synthetic. Synthetic input is required wherever real
input would carry credentials, live logs, or environment values.

## Prohibited

- Building a fixture by copying the implementation's own output, which makes the
  assertion tautological.
- Asserting a hardcoded count, file total, past commit identifier, or line
  number as a contract, unless the enumeration itself is the contract being
  protected.
- Lowering a threshold, deleting a failing case, or narrowing a guard to make a
  suite pass.
- Reading diagnostics dumps, local logs, auth files, credentials, tokens, secret
  values, or shell history as test input.
- Adding a discovery-only placeholder module that runs no assertion.
- Claiming coverage from a test that was written but not executed.

## Failure Handling

If the requirement admits two readings, write the test for neither and return
the ambiguity to the owning document. If a behavior cannot be observed without a
credential, a live service, or a network call, record it as unverifiable at this
layer and name the boundary rather than mocking the guarantee away. If an
existing test already covers the behavior, extend it and say so instead of
adding a second owner.

## Applies To

- Roles: `qa-engineer` owns authoring and running these tests within its
  approved Task scope; `eval-engineer` owns deterministic evaluation fixtures.
- Skills: [test-authoring](../skills/test-authoring/SKILL.md) owns the authoring
  procedure and [e2e-testing](../skills/e2e-testing/SKILL.md) owns end-to-end
  flow; this prompt owns only the derivation envelope.
- Evaluation: the design is adequate when each test names an observable
  behavior, at least one negative case exists per guard, the RED state was
  actually observed before implementation, and no assertion depends on the
  implementation's own output as its oracle.

## Related Documents

- [Prompt index](README.md)
- [Quality standards](../governance/quality-standards.md)
- [Workflows](../governance/workflows.md)
- [Environment constraints](../governance/environment-constraints.md)
