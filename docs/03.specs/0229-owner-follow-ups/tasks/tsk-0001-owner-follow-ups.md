---
title: "Owner Follow-ups Task"
version: "0.2.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0229-TSK-0001"
parent_ids:
- "SPEC-0229-PLAN-0001"
created: "2026-10-10"
---

# Owner Follow-ups Task

## Overview

### Objective

Close the Keycloak, Grype and OpenBao snapshot items the owner approved.

## Inputs and Authorization

On 2026-10-10 the owner approved work on the Keycloak errors, the Grype scan
and the OpenBao snapshot token, and kept the Ollama model store where it is.
The owner had approved the Grype database download earlier the same day.

## Work Log

### W1 Keycloak

All 496 `storybook-mcp-client` events in twelve hours were
`REFRESH_TOKEN_ERROR` with `invalid_token` and `Token is not active`, every
one from `192.168.0.13` (this host), at up to 135 an hour. The only
configuration naming the Storybook MCP server is the owner's global
`~/.codex/config.toml` (`[mcp_servers.hyhome_storybook]`), and the Codex
app-server had been running for over four days, so it keeps retrying an
expired refresh token. User-global settings were not changed; the fix is
`codex mcp logout hyhome_storybook` and `codex mcp login hyhome_storybook`,
which GDE-0101 now describes.

### W2 Grype

`seed-grype-db-cache.sh --seed` failed with `seed-cache-size-limit`: the
schema 6 database is 2.99 GiB and the helper capped it at 2 GiB. The cap is
now 6 GiB; `test_grype_db_seed` passes. The tracked approval surface still
grants nothing, as its tests require, so the approval was applied only for
the run. The pinned Grype then downloaded the database once into a scratch
directory and scanned both saved images with `--network none`; the results are
in the [SPEC-0226 Task](../../0226-ai-runtime-pin-verification/tasks/tsk-0001-ai-runtime-pin-verification.md).
The scratch database and image archives sit outside the repository; deleting
them was refused by the session's permissions and is left to the owner.

### W3 OpenBao Snapshot Token

Issuing the token needs the owner's admin token. RUN-0021 now has commands
that read it without echo, pass it and the new token only on stdin, register
`backup-snapshot`, create the 720-hour periodic token, prove it with one
discarded snapshot and only then move it into
`secrets/backup/openbao/snapshot_token.txt`. `bash -n` accepts the block; it
was not run.

### Owner decision 2026-10-29

The owner decided on 2026-10-29 that criterion 3 is `not-required`: RUN-0105
and SPEC-0243 replaced the inline RUN-0021 token procedure, and SPEC-0243
TSK-0001 completed with `SNAPSHOT_TOKEN_DELIVERED`. Criterion 4 is accepted on
the hosted `candidate-quality` run for PR #406 (merge `d19fbfde6`). Criteria 1
and 2 are accepted on their existing PASS rows.

The Evidence and Criterion Acceptance tables moved to the current shape (a
`Required` column and a `Current Owner` column, existing rows kept as they
were) so this acceptance can be recorded.

### Spec approval

The owner ratified the Spec on 2026-10-29.

### Plan approval

The owner ratified the Plan on 2026-10-29.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0229 | draft | approved | #spec-approval |
| SPEC-0229-PLAN-0001 | draft | approved | #plan-approval |
| SPEC-0229-TSK-0001 | draft | ready | #inputs-and-authorization |
| SPEC-0229-TSK-0001 | ready | in-progress | #owner-decision-2026-10-29 |
| SPEC-0229-TSK-0001 | in-progress | completed | #review-and-completion |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Keycloak | 1 | W1 | Event counts by type, client, reason, source | `32fb2e69d` | PASS | W1 Keycloak | required | - |
| Grype | 2 | W2 | Seed tests; offline scans | `32fb2e69d` | PASS | W2 Grype | required | - |
| Snapshot token | 3 | W3 | `bash -n` of the RUN-0021 block | `32fb2e69d` | PASS | W3 OpenBao Snapshot Token | required | - |
| Owner token run | 3 | W3 | Owner runs the RUN-0021 commands; next backup takes a snapshot | — | NOT_RUN | W3 OpenBao Snapshot Token | required | - |
| Changed gate | 4 | W4 | Hardening; `run-ci-gate.py --profile changed --local-only`, base `8594cf406`; operations catalog | `a827e2873` | PASS | Review and Completion | required | - |
| Staged style check | 4 | W4 | `run-ci-precommit.sh --mode local-staged` | `a827e2873` | PASS | Review and Completion | required | - |
| Remote candidate | 4 | W4 | `candidate-quality` | — | NOT_RUN | Review and Completion | required | - |
| Rerun of Remote candidate | 4 | W4 | `candidate-quality` | PR #406 head `d537df0e1`, run 38009744323, merged as `d19fbfde6` | PASS | Review and Completion | required | Remote candidate |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | accepted | Keycloak | Generation 5 row acceptance | SPEC-0229 TSK-0001 |
| 2 | accepted | Grype | Generation 5 row acceptance | SPEC-0229 TSK-0001 |
| 3 | not-required | - | RUN-0105 and SPEC-0243 replaced the inline RUN-0021 procedure; SPEC-0243 TSK-0001 completed with `SNAPSHOT_TOKEN_DELIVERED`. Owner decision 2026-10-29. | SPEC-0229 TSK-0001 |
| 4 | accepted | Changed gate, Staged style check, Rerun of Remote candidate | Local checks PASS; hosted `candidate-quality` PASS on PR #406. | SPEC-0229 TSK-0001 |

## Review and Completion

The local checks passed on `a827e2873`; criteria 3 and 4 remain pending.
The original W3 syntax PASS and owner-run NOT_RUN rows above describe the
2026-10-10 inline procedure, which is no longer a current execution path.

As read back on 2026-10-22, [RUN-0021](../../../05.operations/runbooks/10-platform-and-backup/0021-backup-and-restore.md#procedure)
records removal of that inline block and routes first token issuance to the
reviewed helper in [RUN-0105 W1–W2](../../../05.operations/runbooks/04-security-and-secrets/0105-openbao-maintenance-window.md#maintenance-window-plan),
whose execution record belongs to SPEC-0243. Follow that owner for current
issuance and acceptance evidence. The original candidate and token-run rows
remain unchanged; this readback does not reissue a token or accept a criterion.

On 2026-10-29 the owner closed the package. The hosted `candidate-quality`
check of PR #406 (run 38009744323, head `d537df0e1`) succeeded and the PR
merged as `d19fbfde6`; the appended row resolves the earlier NOT_RUN row.
Criterion 3 is `not-required` and criteria 1, 2 and 4 are accepted.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
