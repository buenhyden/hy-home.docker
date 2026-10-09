---
title: "Stage 05 Format Refresh"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "specs"
artifact_id: "SPEC-0227"
parent_ids:
- "REQ-0026"
- "AD-0030"
created: "2026-10-10"
---

# Stage 05 Format Refresh

## Overview

Every tracked Stage 05 guide, policy and runbook (230 files in 90 subjects)
had the current template's H2 headings with the previous template's content
nested under them: 464 headings whose only child repeated their name, 476
empty sections and old headings such as Purpose, Checklist or Controls under
the new ones. The validator checked only that the required H2s existed, so
none of this failed. The owner asked to bring every Stage 05 document to its
type's current template, language and operating meaning, and to report any
file not processed.

## Scope

In scope: the guide, policy and runbook profiles and their validator, every
tracked file under `docs/05.operations/{guides,policies,runbooks}` except the
README indexes, the inbound links to anchors they rename, and the operations
catalog bindings they carry. Out of scope: the README indexes (their own
profile), incidents and postmortems, Stage 03 and archived documents, and
historical Task records that link to old anchors.

## Contracts

1. Shape. Guide, policy and runbook profiles declare `ordered_sections` and
   `nonempty_sections`: the required H2s appear in the template order, no
   heading is empty, and no heading holds only a child of the same name.
   Like other body findings, they apply to deficits a change introduces.
2. Content. Restructuring keeps commands, cautions, recovery steps, evidence,
   artifact IDs, `created` and relations; a removed command, link or token is
   either still present in the subject's other documents or recorded as a
   deliberate correction.
3. Meaning. Prose is Korean; headings, keys, IDs, paths and commands are kept.
   Statements match current Compose files; LAB-only services are described as
   LAB; no runtime patch versions are copied into prose; each Compose service
   is bound to exactly one Guide.
4. Ownership. Within a subject the Guide explains, the Policy controls and the
   Runbook executes; a duplicated block stays with its owner and the others
   link to it.

## Acceptance Criteria

1. The validator reports out-of-order, empty and self-repeating sections for
   the three profiles, with unit tests.
2. All 230 files pass the section rule, markdownlint, the metadata check and
   the language check, and the processed list equals the tracked list.
3. Every lost command, link or inline token is accounted for, and the
   corrected facts are recorded.
4. The link check and the operations catalog pass.
5. The changed gate, the staged style check and `candidate-quality` pass.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-stage05-format-refresh.md)
