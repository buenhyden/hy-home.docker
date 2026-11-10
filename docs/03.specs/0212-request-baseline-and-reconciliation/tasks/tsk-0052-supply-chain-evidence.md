---
title: "Supply-Chain Review and Artifact Evidence Task"
version: "0.2.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-10"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0052"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-10"
---

# Supply-Chain Review and Artifact Evidence Task

## Overview

### Objective

Finish the supply-chain evidence that TSK-0047 handed off for criteria 86 and
89. Criterion 104 gives every current update-ledger entry a fresh review and a
reviewed decision, so the latest-version gate passes or each unreviewable
entry is an explicit residual. Criterion 105 binds each selected image artifact
to its own signature, provenance and SBOM evidence. Nothing has run.

## Inputs and Authorization

On 2026-11-10 the owner (@buenhyden) set TSK-0047 criteria 86 and 89 to
not-required and approved this dedicated Task for the unfinished work. That
decision opens the Task only. Every network lookup stays inside the host
scope the owner approved in Owner decisions 2026-11-10, under the
[approval boundaries](../../../../.agents/governance/approval-boundaries.md).
No image pull, deployment or HOME change is part of this Task.

The starting state comes from the
[TSK-0047 supply-chain handoff](tsk-0047-image-supply-chain-storybook.md#supply-chain-handoff-2026-11-10):
on 2026-11-10 `security_update_gate` exits 2, with all 89 ledger entries
`blocked-evidence` (`fresh_review` and `reviewed_decision` missing for 89,
`primary_advisory` for 79).

## Work Log

### Order

1. W109: review each ledger entry against its official release and advisory
   source, record the reviewed decision, and rerun the gate.
2. W110: for each selected artifact, verify the publisher signature and
   available provenance and SBOM against its exact digest, and record what the
   publisher does not provide.

Services that HOME runs go first; the rest follow in the same Task.

### Owner decisions 2026-11-10

The owner (@buenhyden) answered the open items on 2026-11-10. N1: lookups may
reach the hosts already approved for earlier work (`github.com`,
`api.github.com`, Sigstore, `cgr.dev`, the Alpine mirrors, `proxy.golang.org`,
`sum.golang.org`), registry metadata on Docker Hub (`registry-1.docker.io`,
`auth.docker.io`), `ghcr.io` and `quay.io`, and each project's official
release or advisory page when it is not on GitHub, recorded per host. All
access is read-only metadata; no image layer is pulled. N2: the services HOME
runs come first; the remaining entries follow in this Task.

The same day the owner reframed criterion 104. The latest-version gate needs a
lookup under 24 hours old for every entry and every service on its latest
version; on 2026-11-10 it exits 2 with `fresh_lookup` 89, `latest_mismatch` 32,
`stable_channel` 11, `primary_release_reference` 8 and `latest_unresolved` 5.
That conflicts with Renovate's 7-day release soak and cannot stay passing, so
104 now records a dated lookup and a decision per entry and keeps the gate
result as an observation.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ledger fresh review | 104 | W109 | Dated official lookup and decision per entry | HOME-running entries first | NOT_RUN | Not started; N1 and N2 answered. | required | - |
| Latest-version gate observation | 104 | W109 | `latest_version_gate` against the update ledger | `main` `648a78a26`, 89 entries | FAIL | Exit 2 on 2026-11-10: `fresh_lookup` 89, `latest_mismatch` 32, `stable_channel` 11, `primary_release_reference` 8, `latest_unresolved` 5. Recorded as an observation; not a pass condition after the reframing. | optional | - |
| Artifact verification | 105 | W110 | Per-artifact signature, provenance and SBOM verification | Selected image digests | NOT_RUN | Not started; waits for W109. | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 104 | pending | Ledger fresh review | No review has run. | SPEC-0212 TSK-0052 |
| 105 | pending | Artifact verification | No verification has run. | SPEC-0212 TSK-0052 |

## Review and Completion

Completion needs a passing latest-version gate or each remaining entry recorded
as a residual, and a verification row for each selected artifact. A receipt
for one artifact never proves another.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Image supply-chain Task](tsk-0047-image-supply-chain-storybook.md)
