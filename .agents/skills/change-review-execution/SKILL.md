---
name: "change-review-execution"
description: "Use when an exact diff or commit range needs independent specification-compliance and quality verdicts backed by verification evidence."
metadata:
  title: "change-review-execution"
  version: "1.4.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-11-20"
  function_id: "change-review-execution"
  scope: "common"
  owner_agent: "code-reviewer"
---

# change-review-execution

## Trigger

### When to Use

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

The review package must identify the base/head range, task requirements, and observed verification evidence.

### When Not to Use

Editing the implementation under review is outside this skill; the reviewer never edits it.

## Procedure

### Steps

1. Confirm the logical diff, actual scope, risk, requirements and fresh
   nonimplementer context before inspecting implementation conclusions.
2. Identify the actual execution surface and effective restrictions. Reuse an
   applicable same-condition enforcement witness, retaining its mechanism and
   limits; do not infer enforcement from a role or profile label.
3. Test each candidate finding against repository evidence, then classify it
   with the shared severity vocabulary and a precise remediation condition.
4. Issue separate specification-compliance and quality verdicts with actual
   boundary observations, unverified dependencies and any carried slice.
   Review only an affected semantic delta; result-only evidence does not
   restart an unchanged source review.

#### Gates

- Review remains independent and uses the read-only boundary required by
  the governing risk policy. An allowed source write or missing enforcement
  evidence does not prove that boundary. The
  [governing workflow](../../governance/workflows.md#review-risk) permits an
  explicit current decision by the authorized human to accept the unmet
  outcome; scope changes follow
  [approval boundaries](../../../docs/00.workspace/04.quality/approval-boundaries.md).
  Record its trusted origin, scope and remaining conditions. Without that
  decision, the required review is unmet.
- Acceptance is no automatic waiver or measurement: preserve failed,
  unobserved or unsupported enforcement and allowed writes as observed; do
  not relabel them `enforced`, `denied` or `PASS`. Historical not-required
  decisions do not exempt newly required observations.
- No claim is made without reproducible evidence. Tool absence is a capability
  restriction, not an attempted OS write denial; filesystem read-only alone
  establishes no remote-tool or network denial.

#### Inputs

- Exact diff and commit list.
- Verification evidence, task report, and governing constraints.
- Actual execution surface, relevant version, parent/worker restrictions and
  enforcement evidence, plus any same-condition evidence proposed for reuse.
- Requirements, design and known limitations without an expected verdict.

### Failure Handling

Return `cannot verify` with the missing evidence when the package is incomplete; never edit the implementation while acting as reviewer.

## Outputs

### Artifacts

- Actionable findings and explicit PASS/APPROVED or correction-required verdicts.
- Independence, actual scope/input identity and carried slice;
  `execution_surface`, `read_only_status` (`enforced`, `failed`, `unobserved`,
  `unsupported`) and `source_write` (`denied`, `allowed`, `unobserved`), with
  the mechanism, witness and its limits. These are report facts, not a new
  machine schema or permission grant.

### Handoff

Owning role, policies and related documents:

- [Code reviewer role](../../roles/code-reviewer.md)
- [Code review dimensions](../code-review-dimensions/SKILL.md)
- [Subagent protocol](../../governance/agentic.md)

## Verification

### Checks

- The review cites the exact reviewed range and leaves the working tree unchanged.
- Each finding names a file and line that reproduces it, or it is dropped.
- The specification-compliance verdict and the quality verdict are recorded separately.
- Boundary claims name the surface and actual evidence, distinguishing tool
  removal, native policy refusal and OS denial. A failed or unobserved route
  stays visible even when a supported alternative succeeds.
- Report only examined files and tests actually run; supplied verification is
  identified as supplied evidence, not independent execution.

### Limits

The verdict covers only the examined diff, requirements and declared scope.
A boundary witness proves only its tested or validly reused mechanism and
surface. Review does not establish unobserved runtime behavior, operational
permission or user acceptance.
