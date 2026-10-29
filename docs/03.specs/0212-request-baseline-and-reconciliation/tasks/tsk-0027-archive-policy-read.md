---
title: "Archive Policy Read Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0027"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# Archive Policy Read Task

## Overview

### Objective

Execute W43: read the Stage 98 policy text against the code and checks that
enforce it, and correct each statement that no longer matches. This Task owns
criterion 38 only.

## Inputs and Authorization

On 2026-10-29 the owner chose the archive policy as the first area for a
manual policy-against-behavior read, matching the request's first priority.
The owner also confirmed that the request-line audit, the pairwise CR check,
four-repository adoption, and the Codex loader stay as TSK-0026 records them.
The input is `main` at merged PR #624. The authorization covers corrections
in the read surfaces, this branch, its pull request, and merge.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0027 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0027 | ready | in-progress | #objective |
| SPEC-0212-TSK-0027 | in-progress | completed | #evidence |

### Statements checked

| Statement | Source | Checked against | Result |
| --- | --- | --- | --- |
| Six dispositions; a disposition with no record has no directory | `docs/98.archive/README.md`, protocol | `docs/98.archive/` listing | Matches; `resolved/` is absent |
| Assessment values and availability values | Protocol | `common.archive_retention` in `registry.json`, `archive_assessments.py` defaults | Matches; `purged` is absent |
| Route records live at `tombstones/<stage>/` and `migrations/` | README Structure | Tree | Matches |
| The corpus CLI has no `--mode` | README Usage 6 | `check-document-corpus-lifecycle.py` arguments | Matches |
| `active-archive-link` runs in `--mode alignment` and `all` | README | `links.py`, `check-document-links.py` | Matches |
| Frozen subtrees and three migrations are ignored by markdownlint | README Usage 2 | `.markdownlint-cli2.yaml` ignore list | Matches |
| `.markdownlint-cli2.yaml` runs with `fix: true` | README Usage 2; docstring of `test_every_text_mutator_excludes_the_same_frozen_payloads` | `.markdownlint-cli2.yaml` | Stale. `fix: false` since `3745b3db2` (2026-10-15) |

### Correction

The README and the test docstring now say that commit checks run with
`fix: false` and that an explicit `markdownlint-cli2 --fix` rewrites files,
which is why the frozen subtrees stay in the ignore list. The rule itself is
unchanged. The comment in `.markdownlint-cli2.yaml` that says the linter once
rewrote five frozen bodies is accurate history and is kept.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Archive corpus | 38 | W43 | `check-document-corpus-lifecycle.py` | This branch | PASS | 0 violations | required | - |
| Metadata contracts | 38 | W43 | `check-document-metadata.py --mode check-contracts` | This branch | PASS | 0 violations | required | - |
| Link alignment | 38 | W43 | `check-document-links.py --mode alignment` | This branch | PASS | 0 failures | required | - |
| Routing tests | 38 | W43 | `python3 -m unittest tests.validation.test_agent_governance_ci_routing` | This branch | PASS | OK | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 38 | accepted | Archive corpus, Metadata contracts, Link alignment, Routing tests | The archive policy text matches its code and checks; one stale reason is corrected. | SPEC-0212 TSK-0027 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
