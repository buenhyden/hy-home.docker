---
title: "Implementation Alignment Fixes Specification"
version: "0.1.1"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0255"
parent_ids:
- "REQ-0026"
- "AD-0030"
created: "2026-11-04"
---

# Implementation Alignment Fixes Specification

## Overview

### Intent

Read-only audits compared the READMEs, agent surfaces and the Stage 01, 02,
05 and 99 documents with the current implementation. This change corrects the
verified discrepancies that lie outside the files still open in other
branches, so documents state what Compose, scripts and the Registry do now.

### Owning Requirements

The user directed that every README, AGENTS.md, `.agents/`, `.claude/` and
`.codex/` file, and the documents under `docs/01.requirements`,
`docs/02.architecture`, `docs/05.operations` and `docs/99.templates`, be
checked against the implementation and corrected; that ADR-0011 references,
references to deleted Specs and missing owners be included; and that items
the first audits did not check be handled.

SPEC-0255 has parent_ids REQ-0026 and AD-0030. It makes concrete REQ-0026 (document retention and retirement) and the AD-0030 document lifecycle architecture constraint by aligning documents with the implementation. The body also cites REQ-0023-FR-0002 (the egress-isolation exception the user decided), AD-0026, POL-0004, POL-0021, ADR-0011 and ADR-0051.

## Scope

### In Scope

- AD-0026 network table: the networks Compose defines but the table omitted,
  and the Crawl4AI egress structure.
- POL-0004 scope globs for the domain-foldered operations catalog.
- Present-tense pointers to deleted Specs in current documents.
- Secret names Compose uses that owning documents with a secret list omit.
- The SonarQube README credential key and the POL-0021 management database
  list.
- Small provenance, audience and Related Documents corrections.
- The REQ-0023-FR-0002 egress-isolation exception the user decided.

### Non-goals

- Files edited by open branches: the Registry and schemas (except the Spec
  allocation counters), infra README
  operations paths, `.github/**`, hook scripts, Stage 01–03 lifecycle
  statuses, ADR-0011, ADR-0002 and folder AGENTS.md files.
- Rewriting accepted ADR decision bodies and terminal Task bodies.

## Behavior Contract

### Normal Behavior

Each corrected statement matches the Compose file, script or Registry entry it
describes, and each reference to a deleted Spec is either historical prose or
names the current owner.

Prose may name a retired identity to explain lineage (ADR-0051).

### Failure and Edge Cases

A corrected document that breaks metadata, lifecycle or link alignment fails
the document gates.

Only secret names are written; no secret value is read or recorded.

**Observable failures.** A corrected statement contradicts Compose, a link breaks, or a deleted Spec is
still named as a current owner.

**Stop boundaries.** This Task pushes and merges nothing. The coordinator pushes the branch and
opens the pull request, and the user merges.

## Acceptance Criteria

### Criteria

1. AD-0026 lists every network Compose defines for the services it covers,
   with subnets and members matching Compose.
2. No current document states that a deleted Spec owns, records or defines a
   current rule or result.
3. The corrected operations, requirement and README statements match the
   implementation they describe.
4. The document gates pass locally, with actual results in the Task.

### Evidence Requirements

- Criteria 1 and 3 are observed by comparing each corrected statement with the Compose file, script or Registry entry it describes; the Task records the comparison.
- Criterion 2 is observed by searching current documents for deleted Spec names used as current owners.
- Criterion 4 is verified by running the document gates locally; the actual results go in the Task.
- The frontmatter owner judges each criterion and records the decision in the Task's Criterion Acceptance table.

## References

### Normative and Evidence

- [Plan](plan.md)
- [Task](tasks/tsk-0001-implementation-alignment-fixes.md)

### Historical and Navigation

No historical or navigation link applies; the package links only its Plan and Task.
