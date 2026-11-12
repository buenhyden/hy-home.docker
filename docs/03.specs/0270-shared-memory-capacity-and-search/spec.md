---
title: "Shared Memory Capacity and Search Specification"
version: "0.1.1"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0270"
parent_ids:
- "REQ-0024"
- "REQ-0027"
- "AD-0027"
created: "2026-11-10"
---

# Shared Memory Capacity and Search Specification

## Overview

### Intent

Extend the existing repository-shared memory writer with a 1 GiB logical
allocation covering managed memory and its backups, and bounded current-source
search. Preserve all committed memory revisions and historical acceptance.

### Owning Requirements

The owner approved the complete implementation plan on 2026-11-10 in the
current interactive request. REQ-0024-FR-0015 and ADR-0049 remain the durable
shared-memory owners. The earlier SPEC-0236 implementation is historical;
this package is a follow-up, not a reopened completed Task.

This Spec makes concrete REQ-0024 (including REQ-0024-FR-0015), REQ-0027 and AD-0027, its frontmatter `parent_ids` and body citation, and applies the ADR-0049 shared agent memory store decision.

## Scope

### In Scope

The existing memory CLI, new capacity/search and backup-coordination helpers,
focused tests, existing manual/daily/offsite backup callers, registered test
and script routes, and matching current governance and operations guidance.

### Non-goals

Reading personal memory bodies, operating an actual backup, changing live
services or credentials, deleting data or snapshots, provider setting changes,
external repositories, remote Git writes, or paid model API calls. Native
memory verification remains SPEC-0244.

## Behavior Contract

### Normal Behavior

A separate ignored `.workspace-memory/capacity.sqlite3` schema-1 ledger and
stable `capacity.lock` account for a fixed 1,073,741,824-byte allocation.
The memory database stays schema 2 with existing body/database limits and
schema-1 snapshot compatibility. Restoring memory never rolls back the
capacity ledger. Count memory and ledger databases/journals, temporary copies,
registered manual/daily exports, and memory-containing local/offsite snapshots.
Charge each external snapshot location 64 MiB without compression or dedup
credits. This is conservative logical accounting, not a filesystem quota.

Before increasing storage, persist a reservation under a shared lock and
SQLite transaction. After I/O, confirm the result and settle atomically.
Identical request identities and inputs do not execute twice. Pending or
uncertain results stay charged until explicit result reconciliation; age never
releases them. No existing revision or backup is deleted to create capacity.

Keep `backup --output`. Add `capacity status`, `capacity reconcile`, and
`backup-run --target state|offsite`. A host coordinator wraps the existing
shell-only Restic jobs, reserves before starting them, and records actual
snapshot identities. Existing metadata inventory is required before adoption;
unknown inventory stops only storage growth. Initial adoption includes every
known pre-upgrade arbitrary backup output through repeatable
`capacity reconcile --legacy-output PATH`. Completeness covers configured
producers, registered outputs and declared legacy paths; it is not a claim
that unregistered machine-wide copies were discovered. The generic Restic command route
is restricted to read-only commands rather than bypassing the coordinator.

Add `search --query TEXT --limit N`, default 10 and maximum 50. Use deterministic
local lexical matching and the existing current-source/eligibility filter.
Return identity, revision, provenance and short snippets; full body retrieval
remains `get`. Search and capacity status open existing state read-only and
never initialize a database, schema or permissions.

One writer owns each path. Library code remains in focused modules. New
behaviour has witnessed RED/GREEN tests and at least 80 percent meaningful
coverage including branches. Operational execution and owner acceptance are
separate from source/test results.

### Failure and Edge Cases

Missing/corrupt capacity state, unknown external inventory, exhausted capacity,
conflicting request identities, unsafe paths and uncertain results refuse new
writes/copies with value-free diagnostics. Existing reads and original data
remain available. Preserve the current capacity exit classification.

Manual backup, daily export, local snapshot and offsite copy consume the same
ledger. Existing backup network isolation and offsite-only egress stay intact.
No extra memory service, embeddings, inference calls or global installation.

**Observable failures.**

Overspending, uncounted managed backups, duplicate execution, timeout-based
reservation release, lost revisions, a restored stale ledger, stale-memory
search results, read-side initialization or secret-bearing evidence fail the
corresponding criterion.

**Stop boundaries.**

An unapproved live target, private body read, external mutation, missing source
ownership or unclear backup inventory stops only the dependent operation.

## Acceptance Criteria

### Criteria

1. The independent ledger admits concurrent reservations without overspending the 1 GiB logical allocation, includes all managed resource classes, and preserves uncertain reservations and old data.
2. Every memory-writing, backup and restore entrypoint uses capacity admission while legacy snapshots remain readable and memory restore never rewinds the ledger.
3. Search provides bounded deterministic current-source results and search/status perform no initialization or write.
4. Manual, daily and offsite producers use the shared reservation lifecycle, and generic Restic commands cannot bypass the registered mutation route.
5. Focused regression, branch coverage, registration, metadata and independent code/security reviews are recorded without promoting isolated results to operational acceptance.
6. Current governance and operations describe capacity, search, failure/reconciliation and recovery with honest local/remote/operational boundaries.

### Evidence Requirements

- Each criterion needs an observation of the stated result, recorded as an evidence row in the package Task under `tasks/` (`tsk-0001-capacity-search-and-backup.md`) with actual results, not intended ones.
- Verification uses the checks the package [Plan](plan.md) and that Task name; a criterion with no recorded observation is unverified.
- The frontmatter owner (`@buenhyden`) judges each criterion and accepts the Spec; a failed, blocked or skipped check is reported as such and does not count as met.

## References

### Normative and Evidence

- [REQ-0024](../../01.requirements/0024-agent-governance-standardization.md)
- [REQ-0027](../../01.requirements/0027-home-development-host.md)
- [AD-0027](../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md)
- [ADR-0049](../../02.architecture/decisions/0049-shared-agent-memory-store.md)
- [Plan](plan.md)
- [Task](tasks/tsk-0001-capacity-search-and-backup.md)

### Historical and Navigation

No retired, superseded or purely navigational link applies to this Spec.
