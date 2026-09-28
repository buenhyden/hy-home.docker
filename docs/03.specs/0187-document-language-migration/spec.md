---
title: "Document Language Migration Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-28"
layer: "specs"
artifact_id: "SPEC-0187"
parent_ids:
- "REQ-0024"
- "REQ-0026"
- "AD-0030"
created: "2026-09-28"
---

# Document Language Migration Specification

## Overview

SPEC-0184 made document language a checked contract, but it judges non-README
documents only when they change. Two hundred tracked documents still read in
the other language. This package translates them, then lets the `language`
link mode judge the whole corpus, so a document's language no longer depends
on whether someone happened to edit it.

## Boundaries and Inputs

In scope, measured on local `main` at `a406430b2` by applying
`language_mismatch` to every non-README document whose profile declares a
language:

| Profile | Count | Direction |
| --- | --- | --- |
| `requirements-package` | 17 | Korean to English |
| `adr` | 29 | Korean to English |
| `architecture-description` | 20 | Korean to English |
| `guide` | 45 | English to Korean |
| `policy` | 47 | English to Korean |
| `runbook` | 41 | English to Korean |
| `repository-readme` (`.github/repository-surface.md`) | 1 | English to Korean |

The set holds about 620,000 characters bound for Korean and 233,000 bound for
English. The `language` link mode and the lifecycle body filter that SPEC-0184
added for unchanged documents are also in scope.

Out of scope:

- READMEs, which SPEC-0184 already migrated.
- Frozen Stage 98 records and any profile without a declared language.
- Changing what a document says. Translation carries meaning over; it does not
  correct, extend, or restructure content.

## Behavior Contract

1. Every document in the measured set reads in its profile's declared
   language afterwards.
2. Structure tokens stay byte-identical: frontmatter keys and every value other
   than `version` and `updated`, registered section headings, identifiers,
   paths, link targets, inline code, fenced blocks, and table column counts.
3. Headings that a profile does not register are translated. Every link that
   targets such a heading's anchor is updated in the same commit.
4. Each translated document takes a patch `version` increment, because the
   documentation protocol treats a meaning-preserving change as a compatible
   correction, and `updated` is set to the change date.
5. Korean output passes through a humanize-korean pass before it is committed,
   and a review against the source finds no added or dropped claim.
6. After the migration, `check-document-links.py --mode language` judges every
   document with a declared language, and the lifecycle validator no longer
   excuses `document-language-mismatch` on unchanged documents.

## Technical Approach

1. Record the measured list in the Task, one row per document, so the scope
   cannot drift during the work.
2. Translate by profile. Subagents take batches of documents. Each batch is
   checked for structure tokens with a comparison script kept outside the
   repository, and Korean batches go through humanize-korean.
3. Commit each profile separately, or in smaller batches for large profiles,
   so a bad translation can be reverted without touching others.
4. When the list is empty, widen `check_language` to every document with a
   declared language, remove `_CHANGED_ONLY_BODY_CODES` from
   `lifecycle/contract.py`, and change the tests first so they fail on the old
   behavior.

## Interfaces and Data

No CLI, Registry, or schema change. `--mode language` keeps its name and
finding code; only the set of documents it judges grows. The
[documentation protocol](../../../.agents/governance/documentation-protocol.md#document-language)
and ADR-0044 already state the full-corpus rule, so they need at most a
wording update that removes the transitional note.

## Failure Modes and Guardrails

| Failure | Guard |
| --- | --- |
| A translation alters a command, path, or identifier | Behavior rule 2 and the per-batch token comparison |
| A translated heading breaks an inbound anchor | Behavior rule 3 and `check-document-links.py --mode all` |
| Translation drifts in meaning | Behavior rule 5 review against the source |
| Korean output reads as machine translation | The humanize-korean pass |
| Enforcement lands before the corpus is clean | Step 4 runs only when the measured list is empty |
| A runbook's procedure changes | Fenced commands are structure tokens and stay identical |

## Acceptance Contract

1. The measured list is recorded in the Task before any translation.
2. Every listed document reads in its declared language, with structure tokens
   unchanged, as the token comparison records.
3. Every Korean batch has humanize-korean evidence and a meaning review.
4. `--mode language` judges every document with a declared language and
   reports no findings, and the lifecycle body filter is removed. Tests that
   fail on the old behavior are added first.
5. Changed-profile members, except the blocked `check-conftest-policy.sh`,
   return 0.
6. `tests/lib` and `tests/validation` pass.

## Traceability

- REQ-0024: canonical agent governance and documentation contracts.
- REQ-0026: document validation.
- AD-0030: document lifecycle governance.
- ADR-0044 and SPEC-0184 Task, Deferred Items, P2: the source of this package.

## Open Questions

None. The owner chose subagent translation with a humanize pass, by area, with
Spec and Plan approval first.

## Operational Impact

Wording changes in 133 operations documents. Commands, paths, and procedure
steps stay identical, so no runtime or service behavior changes.
