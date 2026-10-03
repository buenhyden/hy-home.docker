---
title: "Secret Layout and Environment Parity Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0004"
parent_ids:
- "SPEC-0204"
- "SPEC-0204-PLAN-0001"
created: "2026-10-03"
---

# Secret Layout and Environment Parity Task

## Objective

Reconcile the entire secret tree and its source consumers under the user's
2026-10-03 explicit request. Consolidate common/communication and
surreal_db/surrealdb duplicates, group credentials by service and DB instance,
and preserve actual values and issued IDs. This is a source and value-preserving
path operation; HOME recreation, credential rotation and deletion remain separate.

## Inputs

Main baseline `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`, integrated
secret-layout commit `8df1e89fce0b3bea1f5f3241b95af5c8fefb8fd3`, public
registry, literal Compose/entrypoint consumers and key-only env comparison.
Private values are consumed only by approved local execution tools, never
printed, searched, included in fixtures or copied to this receipt.

## Work Log

The user authorized the entire auth, automation, backup, certs, common,
communication, data, db, labs, observability, security, storage and tools tree.
Exact source writers are `docker-compose.yml`, `.gitignore`,
`secrets/README.md`, `secrets/SENSITIVE_ENV_VARS.md.example`, empty tracked
secret directory markers, path literals in `scripts/operations/gen-secrets.sh`,
and `tests/validation/test_secret_metadata_sync.py`. Public operations path
consumers are amended only for the exact renamed path. Root/LAB actual env and
private registry are ignored execution inputs; public examples own their key
sets. Any key rename must update both examples, actual assignments and all
source consumers atomically without guessing a value.

Every old/new pair is checked for regular-file identity and metadata before
value-preserving relocation. Legacy paths remain compatibility hardlinks while
main consumers still name them. Removing an alias is a separate post-cutover
operation; no currently mounted inode is destroyed. Backup/snapshot/custody and
certificate artifacts are distinct from generated Docker secrets and are not
removed as registry orphans. DB directories follow actual endpoint consumers;
IDs and original creation dates retain their meaning.

On 2026-10-03 a read-only child improperly included private registry value
cells for AI-003 and COMM-001/002/003/004/006 in its tool output. The child
context was quarantined; root received only sanitized IDs and command scope.
Independent security review found no evidence of Git, document or runtime
propagation. The user subsequently approved resuming value-preserving path
moves and metadata sync while reserving rotation for a separate plan. No
exposed values or original output are stored in this package.

## Verification Evidence

Root key comparison: 212 actual/example keys, no missing/extra/duplicate keys.
LAB comparison: 48 keys, no missing/extra/duplicate keys. Empty LAB data,
cluster-ID, certificate and Locust paths retain their unapproved-runtime status;
no fabricated value is supplied. `_PIP_ADDITIONAL_REQUIREMENTS` is intentionally
empty. Final relocation, metadata prune-check, regressions and independent
review are pending.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1, 4, 8 | W1/W5 | IN_PROGRESS: whole-tree source and private metadata contract | Secret README, public registry and generator |

## Review Evidence

Independent incident review is recorded above. The final source/path diff
requires separate independent review without private values.

## Commit Ledger

Baseline and predecessor integration are named above; the final source commit
will record the exact changed set. Remote publication and merge are not implied.

## Rulings

No key/token/password regeneration, HOME start/restart, private-log inspection,
secret rotation or irreversible alias/backup deletion. Synthetic tests only.

## Deferred Items

Rotate/reissue SurrealDB administrator, SMTP app password, Supabase SMTP
password, Slack webhook and Stalwart administrator credentials through a
separately approved provider/server-first plan. COMM-001 is an account identity;
its replacement depends on the selected provider procedure. Each rotation needs
selected consumers, rollback window and verification before revoking the old
credential. No current rotation or HOME execution is authorized.
