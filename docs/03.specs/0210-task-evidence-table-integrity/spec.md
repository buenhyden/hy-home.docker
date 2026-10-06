---
title: "Task Evidence Table Integrity Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-06"
layer: "specs"
artifact_id: "SPEC-0210"
parent_ids:
- "REQ-0024"
- "REQ-0026"
- "AD-0027"
- "AD-0030"
- "ADR-0037"
created: "2026-10-06"
---

# Task Evidence Table Integrity Specification

## Overview

Reject generation 5 Plan and Task table fragments that currently fall outside
the first parsed table block and can therefore disappear from contract
validation. Preserve the existing scalar Task status and registered six-column
Work Breakdown and eight-column Evidence models.

## Scope

This change is limited to the generation 5 Plan and Evidence readers, focused
unit and public metadata regressions, authoring guidance in the Plan and Task
templates, Stage 03 navigation, the SPEC identity allocation, this package,
and section-boundary correction in current SPEC-0182 Task 0003 and SPEC-0204
Task 0001. The authorized implementation owns exactly twelve files. The
baseline is clean `main@92e2a702fa52f86e49964235af99602fffb7d94c`.

Generation 3 and 4 readers, lifecycle and migration proof, Registry profiles,
schemas, table columns, result and acceptance vocabularies, provider settings,
frozen records, and public CLI behavior remain unchanged. Remote delivery,
runtime actions, secret access, and archive disposition are outside scope.

## Contracts

1. Generation 5 Work Breakdown and Evidence sections admit at most one
   canonical header, separator, and contiguous data-row block. A visible pipe
   row outside that block is an error, including an orphan before the header,
   a row after a blank or prose break, and a headerless fragment.
2. Fenced and HTML-comment examples remain excluded by the existing visible-line
   filter. Ordinary prose before or after a table and a lawful no-table
   unassigned cancelled Task remain valid.
3. The strict rule is opt-in only for generation 5 Plan and Evidence readers.
   Legacy completion and review, migration, and Lifecycle Events readers keep
   their existing default behavior.
4. Validators report the defect without joining rows or rewriting source.
   Completion still requires registered `PASS` and `accepted` evidence for each
   required criterion and Work Unit.
5. Existing auxiliary tables in current Tasks remain byte-identical under an
   `Evidence Notes` section, while the unchanged canonical eight-column table
   stays in the registered `Evidence` section. The metadata integration fixture
   uses an explicit synthetic in-progress package and one idempotent router row.

## Acceptance Criteria

1. Fragmented Work Breakdown and Evidence rows in in-progress or completed
   generation 5 documents are rejected instead of being silently omitted.
2. Continuous generation 5 tables, excluded examples, lawful no-table
   cancellation, generations 3 and 4, source proof, and frozen source bytes
   retain their existing behavior.
3. Authoring guidance, Stage 03 routing, validation evidence, promotion, and
   independent review trace to one current Task before package closure.

## Related Documents

- [REQ-0024](../../01.requirements/0024-agent-governance-standardization.md)
- [REQ-0026](../../01.requirements/0026-document-retention-and-retirement.md)
- [AD-0027](../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md)
- [AD-0030](../../02.architecture/descriptions/0030-document-lifecycle-governance.md)
- [ADR-0037](../../02.architecture/decisions/0037-package-disposition-wait-and-task-cancellation.md)
- [Plan](plan.md)
- [Task 0001](tasks/tsk-0001-task-evidence-table-integrity.md)
- [Stage 99 Registry](../../99.templates/registry.json)
