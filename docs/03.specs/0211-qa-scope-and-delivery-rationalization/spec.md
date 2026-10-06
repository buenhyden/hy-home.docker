---
title: "QA Scope and Delivery Rationalization"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-07"
layer: "specs"
artifact_id: "SPEC-0211"
parent_ids:
- "REQ-0024"
- "REQ-0026"
- "REQ-0027"
- "AD-0027"
- "AD-0030"
- "ADR-0037"
created: "2026-10-07"
---

# QA Scope and Delivery Rationalization

## Overview

Consolidate current document and Docker/Compose quality guarantees into one
changed-input pipeline for this public repository. Supersede the local-only
candidate policy adopted by W7 without rewriting its historical evidence.

## Scope

Current governance, Git and GitHub delivery configuration, scripts and tests,
script registration, authored templates and README routing, Commitizen, main
release preparation, SemVer release production, and Issue/Project navigation.
Preserve completed Tasks, frozen archive bytes, runtime authorization, existing
tag objects, npm acceptance expiry, and unrelated user configuration.

## Contracts

1. Admit recurring document profile, frontmatter, relationship, link, lifecycle,
   template and preservation checks plus Docker/Compose/service configuration
   and behavior checks. Supporting pipeline regressions must prove a current
   admitted contract; event-specific Spec/Task hashes and counts are not
   permanent release or development gates.
2. Retire obsolete QA by transferring any continuing guarantee, removing its
   callers and registration, then its exclusive helper, fixture and test.
   Record the disposition with a current owner instead of manufacturing an
   archive-only package or a numerical deletion target.
3. Commit owns the shared Commitizen message grammar. Authoring may format or
   run focused RED/GREEN checks. Feature push does not repeat candidate QA.
   Remote PR QA owns candidate acceptance, with no path-skipped required
   summary and no title-edit cancellation of revision evidence. Main does not
   rerun the same candidate QA; separately scoped remote observations retain
   their different input and trust boundaries.
4. Select checks by actual change impact. Ordinary document changes retain
   profile, relationship, link and lifecycle checks without whole-library,
   frontend or Compose regressions. Implementation changes select their
   relevant regressions; rename, delete and unknown input fail closed.
5. Execute each identical invocation once per declared input, base, history,
   configuration, tool, mode and trust context. Formatting writes are explicit
   authoring actions; required validation is read-only. Reuse cannot cross a
   changed base, toolchain or trust boundary without an identity proof.
6. Commitizen `.cz.toml` owns commit grammar and `.gitmessage` consumes it.
   Main release-preparation PRs own a Keep a Changelog `CHANGELOG.md`. One
   reviewed producer owns future SemVer release tags and GitHub Releases,
   attaches complete assets to a draft before publication, and rejects a
   duplicate published version. Moving channel production is retired after
   consumer reconciliation; existing historical refs are preserved.
7. Issues own request and priority plus Spec/Task links. Specs own contracts,
   Tasks own execution and acceptance, and Projects expose a filtered work
   view. No body replication or bidirectional lifecycle synchronization.
8. Changes use least-privilege immutable Action pins, bounded execution and
   secret-safe output. Source implementation does not authorize deployment,
   credential changes, release publication or historical tag deletion. Actual
   remote settings and results are separately observed or authorized.

## Acceptance Criteria

1. Removed QA has no remaining active caller; every retained recurring guarantee
   has a current document or Docker/Compose owner and a recorded disposition.
2. Representative ordinary-document and implementation plans differ, contain
   no duplicate invocation and retain rename/delete/unknown failure handling.
3. Commit, feature push, PR, main and release stages have one quality owner each;
   required remote candidate failure propagates without repeating full QA.
4. Commit grammar, main changelog preparation and one SemVer draft-asset release
   producer are executable and preserve current historic refs.
5. Current policy, templates and Issue/Project guidance agree on ownership;
   meaningful regression, selected validation and independent review evidence
   is recorded in the Task with observed and unobserved lanes distinct.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-qa-scope-and-delivery-rationalization.md)
- [Governance requirement](../../01.requirements/0024-agent-governance-standardization.md)
- [Retention requirement](../../01.requirements/0026-document-retention-and-retirement.md)
- [Home host requirement](../../01.requirements/0027-home-development-host.md)
- [Lifecycle architecture](../../02.architecture/descriptions/0030-document-lifecycle-governance.md)
- [Disposition decision](../../02.architecture/decisions/0037-package-disposition-wait-and-task-cancellation.md)
