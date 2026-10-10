---
title: "Owner Follow-ups Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "specs"
artifact_id: "SPEC-0229-TSK-0001"
parent_ids:
- "SPEC-0229-PLAN-0001"
created: "2026-10-10"
---

# Owner Follow-ups Task

## Objective

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

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Keycloak | 1 | W1 | Event counts by type, client, reason, source | `32fb2e69d` | PASS | W1 Keycloak | accepted |
| Grype | 2 | W2 | Seed tests; offline scans | `32fb2e69d` | PASS | W2 Grype | accepted |
| Snapshot token | 3 | W3 | `bash -n` of the RUN-0021 block | `32fb2e69d` | PASS | W3 OpenBao Snapshot Token | accepted |
| Owner token run | 3 | W3 | Owner runs the RUN-0021 commands; next backup takes a snapshot | — | NOT_RUN | W3 OpenBao Snapshot Token | pending |
| Validation | 4 | W4 | Changed gate, staged style check, `candidate-quality` | — | NOT_RUN | Review and Completion | pending |

## Review and Completion

Not complete: validation, the merge and the owner's token run remain.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
