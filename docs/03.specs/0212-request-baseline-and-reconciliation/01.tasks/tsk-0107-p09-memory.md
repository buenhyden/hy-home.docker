---
title: "P09 Shared Memory Task"
version: "0.1.4"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-24"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0107"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-24"
---

# P09 Shared Memory Task

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the task payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Scope

##### Objective and Parent

Own criterion163/W179 in the [Spec](../spec.md) and [Plan](../plan.md).
Apply the D09 shared memory delta to the existing Docker memory and session
analysis stores without rebuilding what TSK-0082 already observed.

##### Inputs and Authority

The direct P09-MEMORY1.2.0 request authorizes this workspace, scoped
implementation, bounded observations and normal commit, push, PR and merge.
Inputs are the matching package README/P09, D09, D10, the session retention
policy, the requirements matrix rows U02, U06, U47, U48 and U56, and the
Docker profile and findings D23-12, D23-14 and D23-15; no other workspace is
required. Start was clean `main` 760b2e34 on branch
`codex/p09-memory-1-2-0`. Brief p09-memory revisions 1 to 4 bound this scope
before each first edit. Direct user authorization is authority; this record
is not.

#### Execution Log

##### Work Performed

Retained without rework: schema 3, CAS and request identity, capacity, search,
selected erase and baseline cutover, and the TSK-0082 Claude to Codex to
Claude round trip and stale-write refusal. Discovery against D09 found four
gaps. Source checks were a single pass or fail, so a changed, missing or
expired source could not be told apart. A record with a stored conflict stayed
in default reads and search. `expected_revision=True` passed as revision 1,
and a non-finite number reached the request digest as an unhandled error.
Accepting an analysis candidate changed no memory and had no outbox, against
U48 and D09.

`memory_sources.source_state` now reports `current`, `changed`, `unavailable`
or `content_expired`; a `session-events` reference expires at its
`content_expires_at` and never makes a record current on its own. A reviewed
record shows `source_state`. A stored conflict against a record's current
revision makes it `conflicted` and holds it out of default `get`, `list` and
`search` until a later revision reconciles it. A boolean revision and a
non-finite number are refused as `MEMORY_INVALID`.

`session_analysis decide ... accepted` records the decision and the whole
promotion request in one transaction. The request fixes the memory ID, a
request key bound to the reviewed fields, the reviewed proposal as the body
and a `session-events` reference with the content expiry, captured time plus
the 90-day capture retention. `decide` and the new `promote` drain the outbox
through the memory CLI into one unreviewed `candidate` record. The captured
prompt text (`pattern`) is never copied, so the session retention is not
bypassed. A changed review is marked `stale`, a refused write stays `pending`
with its reason and exit 1, and a retry after a lost receipt replays the
capacity ledger's recorded result instead of writing again or reviving an
erased record. ENVIRONMENT-CONSTRAINTS 2.2.0 changes R125 and R147 and adds
R165 to R167, and the harness maintenance guide 2.2.0 documents the commands.

##### Blockers and Decisions

No Q01-Q04 question is reopened. Existing R147 forbade analysis candidates
from writing memory; U48 and D09 require the promotion, so the requirement
prevails and R147 now allows only the R167 promotion of an owner-accepted
candidate, as an unreviewed record. The earlier retrieval case ME07 expected
a conflicted record in recall; D09 excludes it, so ME07 now expects an
abstention. No store migration is added. The real memory store was only read.
The real analysis store gained only the empty `promotions` table, created by
the existing schema-on-connect path when `candidates` was read. Its 3 accepted
candidates were decided under the earlier contract and get no promotion
intent; whether to promote them is an owner decision. No real candidate was
decided here.

Criterion138 (TSK-0082) still holds its required R2 copy removal: the bucket
lock releases the 30 copies one a day until about 2026-12-10, and the next
step stays with that Task's owner. This Task neither ran nor scheduled any
removal.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 163 | W179 | method=review; tool=-; command=- | P09 1.2.0 package, D09, D10, retention policy, U47/U48; current agent_memory, memory_sources, memory_cli, memory_search, session_analysis and ENVIRONMENT-CONSTRAINTS R124-R148 | PASS | Four D09 gaps identified; schema 3, CAS, search, capacity and the TSK-0082 round trip retained | required | - |
| E02 | 163 | W179 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.hooks.test_agent_memory tests.validation.test_session_analysis | New regressions on the pre-change code at 760b2e34 | FAIL | Witnessed RED: 3 failures and 7 errors over 8 new tests; no source_state, no conflicted state, True accepted as revision 1, NaN raised ValueError, no promotions table or promote | required | - |
| E03 | 163 | W179 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.hooks.test_agent_memory tests.validation.test_session_analysis | Change at 445ed71e | PASS | Exit0; 44 tests | required | E02 |
| E04 | 163 | W179 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.ops.test_memory_retrieval_eval | Change before the ME07 update | FAIL | ME07 still expected the conflicted record in recall | required | - |
| E05 | 163 | W179 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.ops.test_memory_retrieval_eval | Change at 445ed71e with ME07 expecting abstention | PASS | Exit0; 2 tests; recall 1.0, stale hits 0, abstention 7/7 | required | E04 |
| E06 | 163 | W179 | method=observation; tool=Python3.12.3 CLI; command=session_analysis.py run, decide accepted, promote; agent_memory.py list --all and list | Disposable local clone of 445ed71e with its own memory and capture stores; three synthetic prompts | PASS | decide exit0 promoted one record through the real memory CLI; a second promote wrote nothing; one revision, review_state candidate, no prompt text in the body, a session-events reference expiring 90 days after capture; default reads 0 | required | - |
| E07 | 163 | W179 | method=observation; tool=Python3.12.3 CLI; command=agent_memory.py usage, list --all, list; session_analysis.py candidates --all | Real stores on 2026-11-24 with the change | PASS | Schema 3, migration not required, 19 revisions and 1 conflict before and after E06; 11 records, none reviewed current, default reads 0; analysis 8 pending, 3 accepted, 2 rejected | required | - |
| E08 | 163 | W179 | method=automated; tool=ruff; command=ruff check and ruff format --check on the changed Python files | Change at 445ed71e | PASS | Exit0 after one PLW1510 fix and formatting | required | - |
| E09 | 163 | W179 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.hooks.test_agent_memory tests.validation.test_session_analysis tests.lib.ops.test_memory_search tests.lib.ops.test_memory_capacity tests.lib.ops.test_memory_retrieval_eval tests.validation.test_agent_memory_capacity tests.validation.test_observe tests.lib.hooks.test_session_capture tests.validation.test_task_forecast | Change at 445ed71e with ME07 expecting abstention | PASS | Exit0; 111 tests | required | - |
| E10 | 163 | W179 | method=automated; tool=Python3.12.3; command=check-agent-governance-contract.py --mode repository --section all; check-document-metadata.py --mode check-active and check-changed; check-document-links.py --mode all --changed; check-document-corpus-lifecycle.py; check-candidate-preflight.sh; provider_surface_renderer.py --check; check-script-manifest.py | Changed-profile selection on the candidate; run-ci-gate.py itself refused locally because Python 3.12.3 differs from the hosted 3.14.8 | PASS | Governance failures0; metadata violations0; links failures0; lifecycle violations0; preflight clean; renderer drift0; manifest valid | required | - |
| E11 | 163 | W179 | method=automated; tool=GitHub Actions CI Quality Gates; command=candidate-core changed candidate validation | PR1148 head 9bdfc0a5, run45226430733 | PASS | candidate-core, candidate-quality and candidate-routing passed; CodeQL and GitGuardian passed | required | - |

##### Resolution Links

E03 resolves the witnessed failures in E02. E05 resolves E04 by aligning ME07
with the D09 exclusion of conflicted records.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 163 | accepted | E01,E03,E05,E06,E07,E08,E09,E10,E11 | Owner @buenhyden accepted on 2026-11-24 in this chat during P16 (TSK-0114). | @buenhyden |

##### Remaining Conditions

The provider-side round trip of TSK-0082 is reused because both providers use
the same CLI and its write path is unchanged apart from the typed refusal; no
new native provider run was made here, and the Codex account stays limited
until 2026-11-27 12:53. On the owner's decision of 2026-11-24 the 3 earlier
accepted candidates were promoted as unreviewed candidate records with
`promote --include-earlier` (TSK-0108 E21). Criterion138 keeps its R2 removal
with TSK-0082, which runs it in one pass after 2026-12-10 on the owner's
decision of 2026-11-24. The permission layer refused the agent's removal of
the disposable scratchpad clone twice; the owner deleted it on 2026-11-24.
The owner decides criterion163 in P16.

#### Handoff

##### Promotion Receipt

`agent_memory.py`, `memory_sources.py` and `session_analysis.py` own the
behavior; ENVIRONMENT-CONSTRAINTS R125, R147 and R165-R167 own the rules; the
harness maintenance guide owns the commands. This Task owns execution
evidence only.

##### Next Owner

The owner decides criterion163 and the earlier accepted candidates. The next
input for this workspace is P10-SESSIONS; it is not executed automatically.
Keep the package through P17.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
