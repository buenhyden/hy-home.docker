---
title: "Local Gate Governance Timeout"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0235"
parent_ids:
- "REQ-0010"
- "AD-0024"
created: "2026-10-13"
---

# Local Gate Governance Timeout

## Overview

The local changed gate cannot finish on the owner's host. The node
`leaf.document-governance-library-regressions` in
`.github/workflow-contract.yml` has `timeout_minutes: 15`, but its unittest
batch takes about half an hour there, so `run-ci-gate.py --profile changed`
exits 124 after every earlier step passes, as SPEC-0233 W6 records (added in
PR #448). The earlier SPEC-0231 W6 and SPEC-0232 W5 runs stopped at outer
3000 s and 3600 s limits around the gate, so they do not show the node's own
limit, although both stopped inside the same suite. The node is listed in
`public_gate.local_only_gate_ids`, so hosted `candidate-quality` never runs it
and is not affected.

## Scope

In scope: that node's `timeout_minutes` and the evidence that the new value
fits the measured runtime. Out of scope: splitting the node, speeding up the
suite, and every hosted job or workflow timeout.

The owner chose on 2026-10-13, through AskUserQuestion, to raise the timeout
to 45 minutes rather than accept hosted results only or split the node.

## Contracts

1. `leaf.document-governance-library-regressions` has `timeout_minutes: 45`;
   no other node or workflow changes.
2. The value is justified by a measured run of the node's own module list on
   this host, recorded in the Task.

## Acceptance Criteria

1. The workflow contract and CI gate contract tests pass with the new value.
2. The node's module batch, measured on this host, finishes inside the new
   timeout with margin, and the measured time is recorded.
3. A full local `run-ci-gate.py --profile changed` run reaches and passes the
   node, and hosted `candidate-quality` passes.

## Related Documents

- [REQ-0010](../../01.requirements/0010-tooling.md)
- [AD-0024](../../02.architecture/descriptions/0024-tooling-optimization-hardening-architecture.md)
- [Plan](plan.md)
