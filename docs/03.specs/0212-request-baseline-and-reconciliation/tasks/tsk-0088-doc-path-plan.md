---
title: "Document Path Plan Task"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-18"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0088"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-18"
---

# Document Path Plan Task

## Scope

### Objective and Parent

Own criterion 144 and work unit W160 under the [Spec](../spec.md) and
[Plan](../plan.md). Prepare the numbered docs subfolder layout for the
final cutover without moving anything now.

### Inputs and Authority

The direct 2026-11-18 request runs DOC-PATH-PLAN from the git-ignored
4.2.0 package with designs D27, D28, D14 and D24. On 2026-11-18 the owner
answered SDD-PATHS with "Adopt all candidates". The attachment's
`05.releases` folder and Release role are not adopted. Q07-CUTOVER alone
applies the moves, renumbers identities and resets allocators.

## Execution Log

### Work Performed

#### Three kinds of number

Folder classification (`NN.name`), document and object identities with
their file numbers, and document versions change for different reasons.
This plan covers only the first. Identity renumbering and the next Spec
starting at 0001 belong to Q07, and versions never reset because of a
move. The Spec allocator high-water mark stays at 270; nothing here
consumes an identity.

#### Move plan

Taken from `8932c76e4`. Each digest is the Git tree of the source directory.
Every source exists, none is a symbolic link, no target exists, and the
543 resulting paths have no duplicate and no case-fold or Unicode
normalization collision. No pull request was open when the plan was taken.

| Source path | Target path | Kind | Source digest | Contents | Operation | Phase | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `docs/02.architecture/descriptions/` | `docs/02.architecture/01.descriptions/` | classification move | `11a133fc9c32` | 28 files | move with Git, rewrite current links and paths | Q07 final cutover | SDD-PATHS |
| `docs/02.architecture/decisions/` | `docs/02.architecture/02.decisions/` | classification move | `123222bf3c4e` | 31 files | move with Git, rewrite current links and paths | Q07 final cutover | SDD-PATHS |
| `docs/05.operations/guides/` | `docs/05.operations/01.guides/` | classification move | `641347995542` | 95 files | move with Git, rewrite current links and paths | Q07 final cutover | SDD-PATHS |
| `docs/05.operations/policies/` | `docs/05.operations/02.policies/` | classification move | `f6a0d42dea5c` | 94 files | move with Git, rewrite current links and paths | Q07 final cutover | SDD-PATHS |
| `docs/05.operations/runbooks/` | `docs/05.operations/03.runbooks/` | classification move | `a7b885e4e36d` | 95 files | move with Git, rewrite current links and paths | Q07 final cutover | SDD-PATHS |
| `docs/05.operations/incidents/` | `docs/05.operations/04.incidents/` | classification move | `7cf8dddd659d` | 4 files | move with Git, rewrite current links and paths | Q07 final cutover | SDD-PATHS |
| `docs/90.references/research/` | `docs/90.references/01.research/` | classification move | `7a1cd8a9705f` | 28 files | move with Git, rewrite current links and paths | Q07 final cutover | SDD-PATHS |
| `docs/90.references/audits/` | `docs/90.references/02.audits/` | classification move | `53b074694c34` | 1 files | move with Git, rewrite current links and paths | Q07 final cutover | SDD-PATHS |
| `docs/90.references/data/` | `docs/90.references/03.data/` | classification move | `d687baeced81` | 1 files | move with Git, rewrite current links and paths | Q07 final cutover | SDD-PATHS |
| `docs/99.templates/contracts/` | `docs/99.templates/01.contracts/` | classification move | `cd8cfc035818` | 5 files | move with Git, rewrite current links and paths | Q07 final cutover | SDD-PATHS |
| `docs/99.templates/templates/` | `docs/99.templates/02.templates/` | classification move | `4935d24ebc2f` | 44 files | move with Git, rewrite current links and paths | Q07 final cutover | SDD-PATHS |
| `docs/03.specs/0204-service-integration-security-and-operations/tasks/` | `docs/03.specs/0204-service-integration-security-and-operations/01.tasks/` | classification move | `e6b6e0fa0227` | 22 files | move with Git, rewrite current links and paths | Q07 final cutover | SDD-PATHS |
| `docs/03.specs/0212-request-baseline-and-reconciliation/tasks/` | `docs/03.specs/0212-request-baseline-and-reconciliation/01.tasks/` | classification move | `f042dd53d836` | 86 files | move with Git, rewrite current links and paths | Q07 final cutover | SDD-PATHS |
| `docs/03.specs/0218-common-controls-and-exceptions/tasks/` | `docs/03.specs/0218-common-controls-and-exceptions/01.tasks/` | classification move | `6b28089c0409` | 2 files | move with Git, rewrite current links and paths | Q07 final cutover | SDD-PATHS |
| `docs/03.specs/0244-native-memory-controlled-verification/tasks/` | `docs/03.specs/0244-native-memory-controlled-verification/01.tasks/` | classification move | `7142eafa5057` | 1 files | move with Git, rewrite current links and paths | Q07 final cutover | SDD-PATHS |
| `docs/03.specs/0245-observability-ca-execution/tasks/` | `docs/03.specs/0245-observability-ca-execution/01.tasks/` | classification move | `036f260bb917` | 1 files | move with Git, rewrite current links and paths | Q07 final cutover | SDD-PATHS |
| `docs/03.specs/0255-implementation-alignment-fixes/tasks/` | `docs/03.specs/0255-implementation-alignment-fixes/01.tasks/` | classification move | `72c980a20d76` | 1 files | move with Git, rewrite current links and paths | Q07 final cutover | SDD-PATHS |
| `docs/03.specs/0262-analytics-labs-migration/tasks/` | `docs/03.specs/0262-analytics-labs-migration/01.tasks/` | classification move | `2421f4bc3ffa` | 1 files | move with Git, rewrite current links and paths | Q07 final cutover | SDD-PATHS |
| `docs/03.specs/0263-lab-promotion-contract/tasks/` | `docs/03.specs/0263-lab-promotion-contract/01.tasks/` | classification move | `1666d03f481f` | 3 files | move with Git, rewrite current links and paths | Q07 final cutover | SDD-PATHS |

The digests are a snapshot of the plan's base. Work continues in these
folders until Q07 freezes writes, so Q07 takes the digests again at the
freeze and moves what is there then; a changed digest is expected, not a
conflict.

Spec package `contracts/` folders keep their name; the attachment numbered
only `tasks/` inside a package. Stage folders, native provider paths,
`infra/`, Vault, service and operating data are outside the plan.

#### Rehearsal

A disposable detached worktree at `8932c76e4` applied all 19 moves with Git,
recomputed relative Markdown links from each file's new place, and
rewrote repository path prefixes in 673 files, leaving 78 terminal Task
bodies unchanged. The worktree was removed afterwards; the real tree,
Registry and identities did not change.

A plain path rewrite cannot reach the following consumers, so the cutover
must convert them by hand:

| Consumer | What pins the old name |
| --- | --- |
| `document-profile.schema.json` | regexes for `contracts/` and `templates/` under Stage 99 |
| `registry.json` | Task `path_pattern` with the `{package_number}` placeholder, plus every literal path |
| `links.py` | the moved-Operations regex, the Stage 90 directory tuples and the role-root lookup |
| `taxonomy.py` | the Stage 02 directory regex and the incident path tuple and regex |
| `operations_catalog.py` | the role directory map, top-level entries, Task segment, incident root, Guide family check and role table |
| `architecture.py` | allowed Stage 02 entries, the directory loop and the parent check |
| `check-script-manifest.py` | the Runbook path regex |
| `spec_packages.py`, `references.py`, `identity_history.py`, `metadata/profile.py`, `metadata/lifecycle.py`, `operations_moves.py` | bare folder-name literals to review (12, 5, 2, 2, 1 and 1) |
| Tests | literals in `test_registry`, `test_spec_packages` and `test_architecture` among others |
| Terminal Tasks | 16 links from completed Tasks into moved folders; the checker needs a moved-folder resolution or Q07 retires those Tasks |

With the first seven pinned in the rehearsal, link alignment fell from
2,447 to those 16 failures, the agent governance contract, renderer and
script manifest passed, change selection found no unmapped path, and the
operations catalog (267 findings), changed metadata (architecture parent
check) and corpus lifecycle still failed on the unconverted consumers
above.

#### Recheck on `548b42ecb`

The DOC-PATH-PLAN request ran again on 2026-11-18 after five more merges.
The 19 folders and the eight packages are unchanged, 545 files now move
(TSK-0088 and TSK-0089 were added), no target exists, nothing collides,
and the code and schema pins are the same files listed above. The
`runbooks` and 0212 `tasks` digests changed with the new runbook section
and Tasks, as the refresh rule expects.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0088 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0088 | ready | in-progress | #move-plan |

### Blockers and Decisions

None block the plan. The moves wait for Q07-CUTOVER, which needs every
other open obligation and acceptance closed first.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Collision review | 144 | W160 | source, symlink, target, duplicate, case-fold and NFC checks | 19 planned moves at `8932c76e4` | PASS | 543 files; no issue | required | - |
| Rehearsal links | 144 | W160 | `check-document-links.py --mode alignment` in the rehearsal | Moves, rewrite and seven pinned consumers | FAIL | 16 links from terminal Tasks into moved folders | required | - |
| Rehearsal contracts | 144 | W160 | agent governance contract, renderer check, script manifest, change selection | Same rehearsal | PASS | 0 failures, drift 0, manifest valid, no unmapped path | required | - |
| Rehearsal readers | 144 | W160 | operations catalog, changed metadata, corpus lifecycle | Same rehearsal | FAIL | 267 catalog findings; architecture parent check; Spec package rule; consumers listed above | required | - |
| Plan recheck | 144 | W160 | source, target, collision, package-set and pin rescan | 19 planned moves at `548b42ecb` | PASS | 545 files; no issue; pins unchanged; two digests refreshed by new work | required | - |
| Real tree unchanged | 144 | W160 | `git status`, Spec high-water mark | Real checkout after the rehearsal | PASS | No change; high-water 270 | required | - |

### Resolution Links

None: the rehearsal failures are the plan's findings, which Q07 resolves.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 144 | pending | Collision review, Rehearsal contracts, Real tree unchanged | Awaits the owner's decision; the failing rehearsal rows are inputs to Q07 | @buenhyden |

### Remaining Conditions

Q07-CUTOVER converts the listed consumers, moves the 19 folders, and
decides how terminal Task links resolve.

## Handoff

### Promotion Receipt

None yet: no current meaning changes until Q07 applies the plan.

### Next Owner

Q07-CUTOVER owns the moves. The owner decides criterion 144.
