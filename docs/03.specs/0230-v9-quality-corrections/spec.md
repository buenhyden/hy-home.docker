---
title: "Prompt v9 Quality Corrections"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0230"
parent_ids:
- "REQ-0024"
- "AD-0027"
created: "2026-10-13"
---

# Prompt v9 Quality Corrections

## Overview

The prompt v9 request on 2026-10-13 asks to correct automation and checks
that act on the wrong signal. Finding F17: `.github/workflows/stale.yml`
closed an issue or pull request seven days after marking it stale, so a
thread could close on inactivity alone while its Task was still open. While
validating that change, two checks on `main` `4af41f1a8` failed for reasons
unrelated to this request: the compose-baseline selector test did not list a
selector that `c80915370` registered, and the SEC01 update ledger kept the
input digests of three Compose files that `b8d3ea818` changed after the
ledger was written. Both fail every branch whose gate selects them.
Finding F26 asked whether the PostToolUse `--write` text normalizer conflicts
with the formatter owner that `.pre-commit-config.yaml` registers.

## Scope

In scope: the stale workflow inputs, its contract entry and test fixture; the
selector list in the workflow contract test; the three `include_inputs`
digests in the update ledger; the PostToolUse normalizer in
`scripts/hooks/post-tool-validate.sh`. Out of scope: reopening threads closed earlier,
other non-gating workflows, repository settings, image versions and the
historical census in the ledger.

## Contracts

1. The stale workflow still labels a thread after 30 days without activity
   and says it will not close it; `days-before-close` is `-1`, which the
   pinned `actions/stale` v11 manifest defines as never closing. Job
   permissions stay as they are, since the label and notice still need them.
2. The selector test lists exactly the selectors the contract registers.
3. The ledger `include_inputs` equal the census the ledger's own test
   computes; only digests of files whose image and build lines did not change
   are refreshed this way.
4. The PostToolUse normalizer changes a file only where pre-commit-hooks
   `trailing-whitespace` and `end-of-file-fixer` would: lines split on LF
   only, a CRLF ending kept, trailing ASCII whitespace removed, a missing
   final LF added. It stays opt-in through `--write`, edits only the files
   in the current edit payload and skips the frozen archive payloads.

## Acceptance Criteria

1. No workflow input closes a thread on inactivity alone.
2. The workflow contract tests and the update-gate tests pass on the branch.
3. The changed gate and `candidate-quality` pass.
4. The normalizer leaves every file the registered owners accept unchanged.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-v9-quality-corrections.md)
