---
title: "Agent Memory Restic Coverage"
version: "0.2.0"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0237"
parent_ids:
- "REQ-0024"
- "AD-0004"
- "ADR-0049"
created: "2026-10-13"
---

# Agent Memory Restic Coverage

## Overview

SPEC-0236 created one shared agent memory store in the main checkout,
`.workspace-memory/memory.sqlite3`, which Git ignores. Its backup was a
manual CLI command writing one file outside Restic, so a disk failure could
lose both. The owner deferred Restic coverage to a separate Spec and asked on
2026-10-13 to proceed with it.

## Scope

In scope: one step in `infra/09-platform-ops/restic/bin/hyhome-backup.sh`, its
test, the POL-0021 data-set row and the RUN-0021 procedure. Out of scope: the
Compose model, Restic include sets, the systemd unit, retention, and any real
service run or restore on HOME.

## Contracts

1. Before the Restic backup step, the daily run copies the store into staging
   as `agent-memory.sqlite3` with `scripts/operations/agent_memory.py backup`,
   the SQLite online backup the CLI already performs. Staging is already
   snapshotted by Restic and emptied by the run's EXIT trap.
2. When the store does not exist, the step does not call the CLI, which would
   create an empty store, and the run does not fail.
3. When the backup fails, the partial output is removed and the run fails
   (`status=1`), like every other export.
4. POL-0021 lists the store as a protected data set, and RUN-0021 states the
   daily backup and how to restore from a Restic snapshot.

## Acceptance Criteria

1. A test that runs the step against a synthetic store shows contracts 1 to 3
   and fails against the script on `main` before this change.
2. `bash -n`, shellcheck, the backup contract tests and the document checks
   pass.
3. An independent IaC review finds nothing blocking.
4. A real `hyhome-backup.service` run includes `agent-memory.sqlite3` in the
   Restic snapshot.

## Failure Conditions

A missing store must skip the export without invoking the CLI or creating
an empty database. A failed online backup removes partial staging output and
fails the daily run; source and synthetic checks alone do not prove the real
Restic snapshot contains the store.

## Related Documents

- [REQ-0024](../../01.requirements/0024-agent-governance-standardization.md)
- [AD-0004](../../02.architecture/descriptions/0004-data-architecture.md)
- [ADR-0049](../../02.architecture/decisions/0049-shared-agent-memory-store.md)
- [SPEC-0236](../0236-shared-agent-memory/spec.md)
- [Plan](plan.md)
