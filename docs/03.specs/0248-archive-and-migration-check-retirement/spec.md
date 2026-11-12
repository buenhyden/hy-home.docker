---
title: "Archive and Migration Check Retirement"
version: "0.1.1"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0248"
parent_ids:
- "REQ-0026"
- "AD-0030"
created: "2026-11-03"
---

# Archive and Migration Check Retirement

## Overview

### Intent

Stage 98 (`docs/98.archive/`) is history. CI and local gates still validated
its files and records: archive integrity, the Retention Catalog, Tombstone
pairing, recovery rows, archive links, migration ledgers, and archive record
metadata. Those checks failed changes that never touched the archive. The
user directed that they be removed, together with the migration checks, and
that the remaining legacy allowances be made removable later.

### Owning Requirements

This Spec makes concrete the frontmatter parents REQ-0026 (document retention and retirement) and AD-0030 (document lifecycle governance). The body cites no ADR and no REQ-####-FR or REQ-####-NFR identifier.

## Scope

### In Scope

Remove every gate that validates Stage 98 files or records, and every check of
document migration status that exists only to verify Stage 98 ledgers. Keep the
non-archive checks that live beside them, and keep the narrow read-only loaders
that current checks still need. Do not edit or delete Stage 98 bodies; their
removal is a later, separate phase. Record the remaining legacy allowances as a
backlog with exit conditions.

### Non-goals

Stage 98 bodies are not edited or deleted here because their removal is a later, separate phase, and non-archive checks are kept; both limits are stated in the In Scope text.

## Behavior Contract

### Normal Behavior

- No gate validates a record under `docs/98.archive/`: metadata validation
  returns no finding for it, the corpus lifecycle route runs no archive
  recovery or promoted check, and link alignment skips outbound links from it.
  A link into it is still checked for ordinary target integrity.
- Active-stage occupancy and Task cancellation checks keep running from the
  corpus lifecycle route. The incident corrective-owner check keeps working.
- Read-only loaders that current checks need (lineage, identity allocation,
  recorded retirements, requirement gaps, preserved predecessors) may read
  Stage 98 and are listed in the Task. A Tombstone grants a retirement or
  requirement-gap exemption only when it meets the minimal sealed contract;
  otherwise it grants none. The 0003 ledger verifier, the preserved ADR loader
  and the preserved Spec Package loader deliberately stay fail-closed until the
  archive-file deletion phase removes them.
- `docs/98.archive/` stays in the document suite path trigger, so an
  archive-only change still runs the current checks that read it.
- The `--profiles` transition alias is removed; `--registry` is the only flag.

### Failure and Edge Cases

**Observable failures and stop boundaries.**

A removal that drops a non-archive check, or a gate that still reports a Stage
98 finding, fails this Spec. A reader that raises on a malformed archive record
instead of granting no exemption fails criterion 2.

## Acceptance Criteria

### Criteria

1. The archive and migration validators, their tests, and their gate
   registrations are removed, and no gate reports a finding for a Stage 98 path.
2. Occupancy, cancellation, incident closure, recorded-retirement exemptions,
   lineage, and identity allocation behave as before on this repository.
3. Governance text no longer requires archive validation, and the remaining
   Stage 98 readers and legacy allowances are inventoried in the Task with
   their removal conditions.
4. The changed tests, document gates, Script Manifest and workflow-contract
   checks pass locally, with actual results recorded in the Task.

### Evidence Requirements

- Each criterion is evidenced by rows in TSK-0001 under `tasks/`, including the inventory of remaining Stage 98 readers and legacy allowances with their removal conditions.
- The changed tests, document gates, Script Manifest and workflow-contract checks are run locally by the Task owner and their actual results recorded.
- The frontmatter owner (`@buenhyden`) judges each criterion and records acceptance.

## References

### Normative and Evidence

- [Plan](plan.md)
- [Task](tasks/tsk-0001-archive-and-migration-check-retirement.md)
- [Document retention requirement](../../01.requirements/0026-document-retention-and-retirement.md)
- [Document lifecycle architecture](../../02.architecture/descriptions/0030-document-lifecycle-governance.md)

### Historical and Navigation

No historical or navigation link applies; every link above is current authority or evidence.
