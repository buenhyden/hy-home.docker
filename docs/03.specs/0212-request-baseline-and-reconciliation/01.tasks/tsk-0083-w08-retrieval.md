---
title: "W08 Memory Recall Task"
version: "0.3.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-19"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0083"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-18"
---

# W08 Memory Recall Task

## Scope

### Objective and Parent

Own criterion 139 and work units W152 and W153 under the [Spec](../spec.md)
and [Plan](../plan.md). Bring shared memory recall to the 4.2.0
W08-RETRIEVAL design: useful, safe and current recall rather than storage
success, measured against the earlier search on the same cases.

### Inputs and Authority

The direct 2026-11-18 request runs W08-RETRIEVAL from the git-ignored 4.2.0
package, with designs D16, D06 and D12 and the synthetic
`memory-eval-cases`. It builds on the W08-MEMORY record semantics in
[TSK-0082](tsk-0082-w08-memory.md). No real memory body enters a fixture,
and changes to the real store need their own approval of that target.

## Execution Log

### Work Performed

#### Gap analysis

`search` matched one case-folded substring of the body among admissible
records, sorted by memory ID. It already filtered by eligibility, source
pins, baseline, validity and supersession before matching, kept no index or
cache and read nothing for records it skipped. It missed an exact or partial
memory ID, a source path, Korean text whose spacing differed and terms that
were not adjacent, gave no reason for a hit, did not flag unresolved
conflicts and read records and provenance in separate statements outside
one snapshot.

#### Evaluation and baseline

`tests/lib/ops/test_memory_retrieval_eval.py` turns the retrieval cases of
`memory-eval-cases` into 17 synthetic cases: exact ID, path, Korean with
and without spacing, a two-character Korean query, mixed identifiers, an
updated fact, an unresolved conflict, abstention, another clone's store,
an earlier baseline, an erased record, poisoning, a wrong premise, a
withdrawn record and an expired record. The corpus is written through the
store API and every query runs through the `search` command. ME09 has no
case because the store holds no sensitivity above `internal` and every
caller is the same local account. ME13 to ME15, ME17 to ME19 and ME21 are
write, capture and provider cases owned by TSK-0082 and W08-CAPTURE; ME20
has no index to fall out of step.

On `c35849426`, with the controller Python 3.14.8 and SQLite 3.45.1 on this
host, three runs each, the earlier search reached recall@5 0.545 with
precision 1.0, no stale hit, no disclosure and 6 of 6 abstentions; it
missed ME01, ME02, ME03, ME07 and ME16. Latency was p50 5.5 ms and p95
10.1 ms with 13 records, and p50 118.7 ms and p95 151.9 ms with 2,013.

#### W152 design

Matching keeps the admissibility filter first and then tries, in rank
order, the exact ID, a partial ID, a source reference, the phrase, the
phrase without whitespace and all terms, with ties broken by memory ID.
Each hit adds its kind, baseline, selection reason, unresolved conflict
count and `authority: data-only`; an empty result is the abstention. Read
commands select and hydrate inside one read snapshot. On the same cases,
environment and runs, recall@5 rose to 1.0 with precision 1.0, no stale
hit, no disclosure and 6 of 6 abstentions. Latency was p50 5.0 ms and p95
6.2 ms with 13 records, and p50 130.8 ms and p95 185.8 ms with 2,013; the
largest result grew from 153 to 197 estimated tokens.

A split over 2,008 admissible records, 20 runs, put 122.4 ms in building
the admissible views and 13.8 ms in matching; an FTS5 trigram match over
the same bodies took 0.02 ms. An index therefore saves at most the
matching share while the admissibility work stays, trigram cannot match
the two-character Korean case, unicode61 does not bridge Korean spacing,
and an external-content index would add insert, delete, rebuild and
generation duties that the current design does not need. No lexical,
trigram or vector index is adopted, and no lexical failure remains to
justify a hybrid. ENVIRONMENT-CONSTRAINTS-R132 to R135, the search prose
and RUN-0021 state the behavior.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0083 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0083 | ready | in-progress | #w152-design |

### Blockers and Decisions

W153 waited for Codex's usage limit, which ended at 16:29 KST on
2026-11-18, and then ran on the real store. Before any change, Codex
`codex exec` found probes `w153-probe-withdraw` and `w153-probe-erase` for
`zephyrquartz`, both revision 1 and matched by phrase. Claude Code then set
the first ineligible at revision 2 and erased the second, which deleted its
one revision. Claude and Codex searches then returned no hit, and both got
`MEMORY_NOT_FOUND` for the erased probe even with `--historical`; the
withdrawn probe stays only as an ineligible historical revision. The real
store is small, so no real recall sample beyond the synthetic corpus is
measured.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Recall RED | 139 | W152 | `test_memory_retrieval_eval` | Evaluation on the earlier search at `c35849426` | FAIL | One failure and one error; ME01, ME02, ME03, ME07 and ME16 missed | required | - |
| Recall GREEN | 139 | W152 | `test_memory_retrieval_eval` | Evaluation on the W152 search | PASS | Both tests passed; recall@5 1.0, no stale hit or disclosure | required | Recall RED |
| Recall regression | 139 | W152 | memory store, CLI, search, capacity and evaluation suites | W152 search on `c35849426` | PASS | 56 tests | required | - |
| Latency split | 139 | W152 | admissible view build, matching and FTS5 trigram timing | 2,008 synthetic records, 20 runs | PASS | 122.4 ms views, 13.8 ms matching, 0.02 ms FTS5 | optional | - |
| Native recall | 139 | W153 | Claude and Codex search after withdrawal and erase | Real store | NOT_RUN | Codex usage limit until 16:29 KST | required | - |
| Native recall observed | 139 | W153 | Claude and Codex search after withdrawal and erase | Real store, probes at revision 1, then withdrawn and erased | PASS | Codex before: 2 phrase hits; after: Claude and Codex `[]`, erased probe `MEMORY_NOT_FOUND` historically for both | required | Native recall |

### Resolution Links

Recall GREEN resolves Recall RED. Native recall observed resolves Native
recall.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 139 | accepted | Recall GREEN, Recall regression, Latency split, Native recall observed | Owner @buenhyden accepted on 2026-11-19 in this chat (W11-ACCEPT) | @buenhyden |

### Remaining Conditions

The owner accepted criterion 139 on 2026-11-19.

None in W152 or W153; the owner decides criterion 139.

## Handoff

### Promotion Receipt

`memory_search.py`, `memory_cli.py`, `agent_memory.py`,
ENVIRONMENT-CONSTRAINTS-R132 to R135 and RUN-0021 hold the W152 behavior.

### Next Owner

The owner decides criterion 139.
