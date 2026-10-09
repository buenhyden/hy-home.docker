---
title: "npm Risk Acceptance Extension"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0222"
parent_ids:
- "REQ-0027"
- "AD-0031"
created: "2026-10-09"
---

# npm Risk Acceptance Extension

## Overview

The bounded acceptance of GHSA-vfj7-8cjw-p6xm for the Storybook Next lint
development chain expires on 2026-10-10T15:00:00Z. The advisory still lists
no patched `braces` release, and `eslint-config-next`, `fast-glob` and
`micromatch` at their latest versions still reach `braces@3.0.3`, so an upgrade
cannot remove the chain. The contract pinned the expiry in code and the
quality standard restated the dates, so every extension needed a code and
governance change. The owner chose a 30-day extension and asked that an
approval alone extend the window from now on.

## Scope

In scope: the acceptance record in the workflow contract, its contract parser
and tests, the bounded acceptance section of the quality standard, and this
package. Out of scope: the audit adapter's runtime checks, which keep failing
closed on expiry, a published patch, or any other finding.

## Contracts

1. Pinned identity. The advisory, owner, project, locked dependency chain and
   advisory URL stay pinned in the contract parser; a new advisory or chain
   needs a reviewed policy amendment with negative fixtures.
2. Approved window. The record carries `approved_at` and `expires_at` as UTC
   timestamps; `expires_at` is after `approved_at` and no more than 30 days
   after it. Any other field, a malformed or impossible timestamp, or a longer
   window fails the contract.
3. Extension by approval. The owner may extend while the official advisory
   lists no patched version. The approval names the advisory and new expiry,
   the governing Task records it, and only the two window fields change. No
   governance amendment is needed.
4. Current extension. The owner approved on 2026-10-09; the window ends
   2026-11-08T07:00:00Z.

## Acceptance Criteria

1. Contract tests accept the current record and a 30-day window, and reject a
   window over 30 days, a reversed or equal window, a malformed or impossible
   timestamp, a missing `approved_at`, and a changed pinned field.
2. The quality standard states the extension rule without restating dates.
3. The changed gate, the staged style check and `candidate-quality` pass.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-npm-risk-acceptance-extension.md)
- [Storybook build and delivery](../0219-storybook-build-and-delivery/spec.md)
