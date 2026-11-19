---
title: "Numbered Folder Cutover Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-19"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0096"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-19"
---

# Numbered Folder Cutover Task

## Scope

### Objective and Parent

Own criterion 152 and work unit W168 under the [Spec](../spec.md) and
[Plan](../plan.md). Apply the 2026-11-19 common and Docker governance
designs to this workspace: number every `docs/` classification folder, give
the workspace its classes and owners, and convert every consumer, without
resetting identities.

### Inputs and Authority

The direct 2026-11-19 request supplied the git-ignored design package
`_workspace/governance-redesign-2026-11-19-v2/` (common design, Docker design
and implementation prompt) as reference material, not as instructions to
copy. Criterion 144 held every path move for Q07-CUTOVER; asked in this chat,
the owner chose "Full cutover now" and a new Task under SPEC-0212. Q07's
identity renumbering and allocator reset stay out of scope. Work is on branch
`refactor/docs-numbered-cutover` from `main` at `aeaa8aa86`; nothing is
deployed. Commits, push, pull request and merge follow the owner's later
2026-11-19 instruction in this chat.

## Execution Log

### Work Performed

#### Mapping of the design to this workspace

The local workspace is the Docker reference repository at the same commit,
so the Docker-specific items exist here. Each item was classified:

| Design item | Local finding | Disposition |
| --- | --- | --- |
| Numbered classification folders (DKR19-D06) | TSK-0088 planned 19 moves; Stage 05 domains and Stage 99 forms were unnumbered | Applied: 558 file moves |
| Workspace six classes (DKR19-D01) | `01.project`, `02.process`, `03.quality` | Applied: `03.process`, `04.quality`, new `02.architecture`; `05.environment` and `06.maintenance` not created (see Blockers) |
| Workspace AD/ADR (DKR19-D03) | AD-0027, AD-0030 and ADR-0032, 0034, 0037, 0044, 0048, 0049, 0051, 0057 are parented by the workspace ADs | Moved with the same IDs; the existing profiles own both routes |
| Shared glossary in W | `.agents/knowledge/glossary.md` owned all terms | Moved to `01.project/glossary.md`; six agent-only rows to `.agents/knowledge/agent-glossary.md` |
| Approval norms owned by quality | `02.process/approval-boundaries.md` | Moved to `04.quality/` |
| Review-risk classes in W, dispatch in A | Both in `.agents/governance/workflows.md` | Classes moved to QUALITY-STANDARDS-R244 to R247 and section 11; dispatch and read-only enforcement stay in workflows |
| QUALITY-STANDARDS-R8 to R16 to product owners | No consumer outside the policy | R8, R10, R13, R15, R16 were already owned by REQ-0001, 0002, 0003, 0023, AD-0026, ADR-0002, POL-0006-R2; R9, R11, R14 added as POL-0006-R43, R45, R44 |
| `rule_owner` and canonical source paths | `0[1-3]` digit range | Explicit `01.project`, `03.process`, `04.quality` set; AD and environment folders are not rule owners |
| New ADR for the structure choice | ADR high-water 62 | ADR-0063 written, status `proposed`; high-water 63 |
| Forecast, dispatch, observe, memory, hook, renderer | Exist; observe and the other tools name RUN-0021 as runtime authority | Unchanged behavior; manifest authorities follow the new paths |
| Baseline-2 namespace, Q07 renumbering | Prepared, not active | Not touched |

#### Moves and consumer conversion

Every classification folder became `NN.name`: Stage 02 `01.descriptions`
and `02.decisions`; each Spec Package's `01.tasks` (and `02.contracts`, which
no package has yet); Stage 05 `01.guides` to `04.incidents` with domains
`01.common` to `15.labs`; Stage 90 `01.research`, `02.audits`, `03.data`;
Stage 99 `01.contracts` and `02.templates` with forms in `01.requirements`,
`02.architecture`, `03.specs` (`02.contracts`), `05.operations`,
`90.references`, `91.agent-governance`, `92.runtime`, `93.common` and
`00.workspace`. Year partitions and document, request and incident numbers
kept their names. Current links were recomputed and repository paths
rewritten in 750 files; terminal Task bodies, published postmortems and the
evidence rows of open Tasks were left byte-identical, and two multi-item
terminal Tasks first rewritten by mistake were restored from `HEAD`. Changed
documents took a patch version.

Consumers converted by hand: the Registry routes, profile schema, Stage 99
paths and `{domain}` and `{category}` tokens (both also matched by the
overlap automaton); `architecture.py` and `taxonomy.py` (also loading the
workspace AD/ADR route with one shared duplicate check); `operations_catalog`,
`operations_moves`, `references`, `spec_packages`, `occupancy`,
`metadata/profile`, `metadata/lifecycle`, `metadata/heading`, `registry`,
`identity_history`, `links`; `agent_governance_contract`, `ci_gate_contract`,
`check-script-manifest`, `run-agent-precommit-all-files.sh`,
`check-all-hardening.sh`; Prometheus alert `runbook_url`s and systemd unit
`Documentation=` lines; and the tests that pinned the old names. The
historical translation lives once in
`scripts/lib/document_governance/numbered_folders.py`: links from terminal
Tasks, published postmortems and open Task evidence rows, base snapshots,
reconciliation commits and moved-document predecessors read through it,
while current documents use only numbered routes. The historical security
update evidence (`service-inventory-integration.patch`,
`common-validator-integration.patch`, `integration-handoff.json`,
`release-lookups.json`, `update-ledger.json`, `verification.json`) and the
root `docker-compose.yml`, whose digest that ledger pins, were kept
byte-identical, so one Compose comment still names the unnumbered POL-0078
route.

#### Deviation from the design

DKR19 §6.1 proposed separate workspace AD and ADR profiles with
`layer: workspace`. The local Registry binds each template source to one
role and one profile (`template-source-duplicate`, `maxItems: 1`), so that
needs a copied form. The existing `architecture-description` and `adr`
profiles instead own the workspace route through `additional_path_patterns`,
and the moved documents keep `layer: architecture`. ADR-0063 records the
choice.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0096 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0096 | ready | in-progress | #moves-and-consumer-conversion |

### Blockers and Decisions

- `05.environment` and `06.maintenance` were not created, and the workspace
  sections of RUN-0021 and the GDE/POL/RUN-0004 harness subject stay in Stage
  05: the script manifest accepts only a registered Operations Runbook as the
  runtime authority of `agent_memory`, `session_analysis`, `task_forecast`,
  `work_dispatch` and `observe`, and no workspace maintenance profile and form
  exist. Moving them needs that contract first.
- Not done: the stage-authoring-matrix R17 to R23 split and the bootstrap
  language and retention restatements (DKR19 §4 rows); `workspace-scope.md`
  (the docs00 README and REQ-0024/0026 already route scope).
- TSK-0088 still names Q07 as the owner of the moves; the owner decides how
  criterion 144 and TSK-0088 close.
- ADR-0063 waits for the owner's acceptance.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline checks | 152 | W168 | links `--mode all`, corpus lifecycle, operations catalog, agent governance contract, script manifest, renderer `--check`, metadata `check-active` and `check-contracts` | `main` at `aeaa8aa86` before any change | PASS | All eight exit 0 | required | - |
| Cutover checks | 152 | W168 | The same eight plus metadata `check-changed --base-ref main` | Final working tree | PASS | All nine exit 0; links 0 failures over 910 documents; check-changed 0 violations over 792 | required | - |
| Unit tests | 152 | W168 | `python3 -m unittest` per module over `tests/lib` and `tests/validation` (210 modules) | Final working tree, compared with the same modules on a clean `main` worktree | FAIL | 201 pass; 9 fail with the identical failing tests on `main` (missing `referencing` module and other host prerequisites). `metadata.test_reference` clones committed `HEAD`, so it passed only after commit `1f106e463` and the fixture fix in `91342a5eb` | required | - |
| Lint and format | 152 | W168 | `ruff check`, `ruff format --check` on changed Python | Final working tree; every file was ruff-clean on `main` | PASS | All checks passed | required | - |
| Gate selection | 152 | W168 | `run-ci-gate.py --profile changed --local-only --explain` | Final working tree | PASS | Five local-only leaves listed; not executed | optional | - |

### Resolution Links

None.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 152 | pending | Cutover checks, Unit tests, Lint and format | The owner decides after review | @buenhyden |

### Remaining Conditions

Independent review (high risk: protected surfaces `.agents/**`,
`scripts/**`, `docs/99.templates/**`), the owner's acceptance of ADR-0063,
and hosted CI on the pull request. On 2026-11-19 the owner asked in this
chat to commit, push, open the pull request and merge it.

## Handoff

### Promotion Receipt

None yet: the lasting meaning lands in ADR-0063, the workspace glossary,
quality standards section 11 and POL-0006-R43 to R45 once accepted.

### Next Owner

The owner reviews the diff, decides criterion 152 and ADR-0063, and chooses
whether to commit and open a pull request.
