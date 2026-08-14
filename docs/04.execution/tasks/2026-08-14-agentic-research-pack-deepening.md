---
status: active
artifact_id: task:2026-08-14-agentic-research-pack-deepening
artifact_type: task
parent_ids:
  - spec:137-agentic-research-pack-rebuild
---

# Task: Agentic Engineering Research Pack Deepening

## Overview

This Task is the execution evidence ledger for an in-place analytical deepening
of the canonical `2026-08-08-agentic-engineering-research-pack`. It re-researches
external sources and re-surveys tracked workspace evidence for the pack's twenty
leaves, then expands each leaf's analysis, scope implications, and source set.

The deepening does not create a new pack, does not rename or relocate any file,
and does not change the pack's twenty-leaf topic decomposition, its fourteen-scope
axis, or its thirty-six requirement destinations. It expands leaf bodies and
`Sources` sections, and advances `reviewed_at` only where re-research produced a
material change.

The pack's router contract is preserved. Deepening adds analysis and sources; it
does not copy policy bodies from canonical owners into this reference.

This ledger reports observed evidence only. An unperformed activity is `Not Run`.
No Stage 90 research statement in this pack becomes policy, runtime truth, or
remote-enforcement proof.

Immutable BASE for this Task is `2ca5f4b87d4567d53f53364ebd2310675981fc75` on
branch `docs/agentic-research-pack-deepening`.

## Inputs

- Approved user direction recorded in Approval Evidence.
- Active Spec authority: `docs/03.specs/137-agentic-research-pack-rebuild/spec.md`.
- Canonical pack under deepening:
  `docs/90.references/research/2026-08-08-agentic-engineering-research-pack/`.
- Immediate predecessor evidence:
  `docs/04.execution/tasks/2026-08-11-agentic-research-pack-source-refresh.md`.
- Superseded historical pack read as input only, never mutated:
  `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/`.
- Authoring contract: `docs/99.templates/templates/common/reference.template.md`.
- Metadata contract: `scripts/validation/check-document-metadata.py`.
- Repository contract: `scripts/validation/check-repo-contracts.sh`.

## Goals and Non-goals

### Goals

- Re-research external sources for all twenty leaves across the user's requested
  category axis, recording retrieval dates and evidence classes.
- Re-survey tracked workspace evidence per scope so each leaf's workspace claims
  are re-derived rather than inherited.
- Expand each leaf's `Definitions / Facts`, `Scope Implications`, and `Sources`
  while preserving the canonical-owner routing contract.
- Reconcile the pack index and parent research router with any leaf change.
- Record per-cluster logical commits and verification evidence in this ledger.

### Non-goals

- Creating a new dated research pack or relocating existing files.
- Changing the twenty-leaf decomposition, fourteen-scope axis, or the thirty-six
  requirement destinations.
- Promoting leaf `status` from `draft` to `active`.
- Copying policy, plan, or runbook bodies into this reference.
- Deleting or editing the retiring `2026-07-05-agentic-research-pack-refresh/`
  pack. Its deletion gate remains owned by Task 11 and is executed in that
  ledger, not here.
- Modifying Spec 137, its Plan, Task 10b, Task 11, or the 2026-08-11 refresh Task.
- Editing LLM Wiki generators, or hand-editing any generated artifact.
- Runtime, remote, push, pull request, or merge actions.

## Scope and Change Boundaries

### Allowed paths

- `docs/90.references/research/2026-08-08-agentic-engineering-research-pack/*.md`
- `docs/90.references/research/README.md` (only if routes or counts change)
- `docs/04.execution/tasks/2026-08-14-agentic-research-pack-deepening.md`
- `docs/04.execution/tasks/README.md` (task index row)
- `docs/00.agent-governance/memory/current.md` (bounded handoff refresh)
- `docs/90.references/llm-wiki/llm-wiki-index.md` and
  `docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md`,
  through their generators only, never by hand
- `docs/04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md`, for the
  Plan-only Gate 9 correction the user approved on 2026-08-14, one file per
  commit and no other Plan
- `docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`, for
  review receipts only. The Plan assigns receipt ownership to that Task, and the
  user directed on 2026-08-14 that Spec, Plan, and Task be inspected and
  reconciled. No other content in that ledger is touched.

### Forbidden paths

- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/`
- `docs/03.specs/`, every Plan other than the Gate 9 rebuild Plan, and every
  part of the rebuild Task other than its review-receipt rows
- `docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`
- `llms.txt`, all LLM Wiki generators, and every other generated artifact
- `infra/`, `secrets/`, any credential-bearing surface

### Compose impact

None. This Task changes no Compose file, service definition, or runtime setting.

### Security impact

None expected. The deepening records no secret value, credential, token, private
key, shell history, or raw log. Security source re-research updates analysis text
only.

### Operations impact

None. No runbook, incident, or policy body is authored or altered.

### Runtime impact

None. No runtime or remote state is observed or mutated by this Task.

## Approval Evidence

### Approval source

The user approved the deepening design in session on 2026-08-14 with an explicit
approval reply, after selecting: in-place deepening of the existing canonical
pack over a new dated pack; a mid-depth target that expands analysis while
retaining the router character; and a category-group subagent decomposition.

The user also selected inclusion of old-pack deletion. The agent recorded that
deletion is a separately gated work item owned by Task 11 and scoped it to a
follow-on phase outside this ledger. That boundary is restated under Deferred
and Blocked Items.

### Protected surfaces

The retiring 2026-07-05 pack, Spec 137, the active Plan, Task 10b, Task 11, the
2026-08-11 refresh Task, and all generated LLM Wiki artifacts remain untouched
and outside this boundary.

### Approval boundary

Approval covers in-place deepening of the canonical pack plus this Task ledger
and the bounded memory handoff. It does not authorize deletion, pack relocation,
leaf status promotion, generator changes, push, or any remote action.

### Rollback or recovery

Every change is a tracked Git commit on `docs/agentic-research-pack-deepening`.
Recovery is `git revert` of the named cluster commit; no external state changes.

### Redaction boundary

No secret, credential, token, private key, personal data, shell history, or raw
log is recorded in this Task or in any deepened leaf.

## Work Breakdown

The pack's twenty leaves are partitioned into six non-overlapping ownership
clusters. No two clusters own the same file, so cluster work is parallel-safe and
each cluster closes as one logical commit.

### Cluster G1 — Foundation

Leaves: `workspace-baseline.md`, `scope-application-matrix.md`.
Axis: fourteen-scope disposition re-derivation and tracked baseline recount.

### Cluster G2a — Harness and loop

Leaves: `harness-engineering.md`, `loop-engineering.md`,
`provider-implementation-comparison.md`, `agent-instructions-vibe-coding.md`.
Axis: harness elements, loop anatomy, Claude and Codex implementation state, and
the common construction shared by both providers.

### Cluster G2b — Model and memory

Leaves: `provider-model-landscape.md`, `agent-model-selection.md`,
`ai-agent-catalogs.md`, `memory-hierarchy.md`.
Axis: model landscape, task-characteristic model and control selection, external
agent catalogs, and the short-term, durable, and domain memory tiers.

### Cluster G3 — SDLC and documentation

Leaves: `spec-driven-sdlc.md`, `sdlc-document-roles.md`,
`document-metadata-lifecycle.md`, `documentation-architecture.md`,
`llm-wiki-system.md`.
Axis: spec-driven development, the PRD through Runbook document role set,
metadata lifecycle, Diataxis reader modes, and the LLM Wiki system.

### Cluster G4 — Delivery and quality

Leaves: `automation-pipeline-workflow.md`, `quality-ci-formatting.md`,
`verification-validation.md`.
Axis: CI/CD topology, GitHub Actions, formatting/lint/type/test gates, and the
verification versus validation distinction.

### Cluster G5 — Infrastructure and security

Leaves: `docker-compose-infrastructure.md`, `security-governance.md`.
Axis: Compose topology and controls, infrastructure evidence ladder, and secure
SDLC with supply chain and secret handling.

### Per-cluster agent contract

Each cluster agent must:

1. Re-research external sources first, preferring official vendor documentation,
   standards bodies, primary papers, and official repositories; record retrieval
   date and evidence class for every source used.
2. Re-survey tracked workspace evidence for the cluster's scope by reading the
   actual tracked files, not by inheriting prior leaf prose.
3. Expand the leaf in place, preserving the reference template section order and
   the canonical-owner routing contract.
4. Set `reviewed_at: 2026-08-14` only on leaves whose body materially changed;
   leave the prior value when re-verification produced no change.
5. Record any claim it could not verify as `UNVERIFIED` rather than asserting it.
6. Never edit a file outside its cluster, never touch the retiring pack, and
   never write secret values.

## Work Log

| Date       | Step                        | Result                                                                                                                                                                                                                              |
| ---------- | --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-08-14 | Pre-task discovery          | Confirmed the requested twenty categories map one-to-one onto the canonical pack's twenty leaves; recorded the 2026-08-11 refresh as immediate predecessor with nine leaves at `reviewed_at: 2026-08-11` and eleven at `2026-08-08` |
| 2026-08-14 | Deletion-gate discovery     | Read the Plan's Task 11 section and confirmed Step 0d is `BLOCKED` under its review breaker with no round 6; deletion therefore stays outside this ledger                                                                           |
| 2026-08-14 | Branch and ledger creation  | Created branch `docs/agentic-research-pack-deepening` from BASE `2ca5f4b8` and authored this ledger from the Stage 99 Task template                                                                                                 |
| 2026-08-14 | Cluster dispatch            | Dispatched six non-overlapping cluster agents across the twenty leaves under one shared brief contract                                                                                                                              |
| 2026-08-14 | Step 0e routing observation | Corrected the earlier discovery note: Step 0e is implemented through fix round 1, not unimplemented. Ran the Gate 9 evidence test module read-only, recorded the result under Blocked Items, and took no Task 11 action             |

## Verification Evidence

### Exact commands

```bash
python3 scripts/validation/check-document-metadata.py \
  --mode check-changed --base-ref <cluster-base>
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-repo-contracts.sh
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
```

### Expected evidence

- Changed-document metadata exits 0 with zero violations for every cluster commit.
- Traceability and repository contracts reach their named results; the known
  `html5lib` runtime dependency gap is a pre-existing, unowned failure and is
  recorded as such rather than suppressed.
- Both LLM Wiki generator checks stay byte-identical because this Task changes
  tracked file contents only and adds no path.

### Actual evidence

| Date       | Unit                   | Command                                                                                                                       | Observed result                                                                                      |
| ---------- | ---------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| 2026-08-14 | Ledger creation        | Changed-document metadata against BASE `2ca5f4b8`                                                                             | `selected=2 violations=0 legacy_exceptions=0 transition_overrides=0`                                 |
| 2026-08-14 | Ledger creation        | `check-doc-traceability.sh`                                                                                                   | `catalog_pairs_total=46 failures=0`, PASS                                                            |
| 2026-08-14 | Ledger creation        | `check-repo-contracts.sh` on the host interpreter                                                                             | `failures=1`; the sole failure is `AGC-DEPENDENCY-MISSING path=html5lib location=validation-runtime` |
| 2026-08-14 | Validation environment | `python3 -m venv --system-site-packages /tmp/agentic-research-validation-venv` then `pip install -r scripts/requirements.txt` | `html5lib` 1.1, `PyYAML`, and `markdown-it-py` importable                                            |
| 2026-08-14 | Ledger creation        | `check-repo-contracts.sh` with the prepared interpreter on `PATH`                                                             | `failures=0`, PASS: repository Docker/docs contracts are synchronized                                |

| 2026-08-14 | G5 Infrastructure and security | Changed-document metadata against `c68985be` | `selected=2 violations=0 legacy_exceptions=0 transition_overrides=0` |
| 2026-08-14 | G5 Infrastructure and security | Secret-pattern scan of both owned leaves | 0 matches in each file |
| 2026-08-14 | G5 Infrastructure and security | `scripts/validation/validate-docker-compose.sh` executed by the cluster agent | Default mode PASS at `services_total=5`; `--preflight` FAILED on four missing bind-mount directories and two missing external networks |
| 2026-08-14 | G5 Infrastructure and security | `scripts/validation/generate-security-automation-readiness.sh` re-executed read-only by the cluster agent | Readiness re-derived at current HEAD rather than inherited |

| 2026-08-14 | G4 Delivery and quality | Changed-document metadata against `8c3f0fce` | `selected=3 violations=0 legacy_exceptions=0 transition_overrides=0` |
| 2026-08-14 | G4 Delivery and quality | `UNVERIFIED` marker census across the three owned leaves | 15 in quality, 12 in verification and validation, 6 in automation |
| 2026-08-14 | G4 Delivery and quality | External source retrieval | Six new sources cited; `iso.org` refused retrieval with HTTP 403 for a second dated attempt; an FDA source failed both routes and was dropped rather than cited unseen |

| 2026-08-14 | Validation environment | `pip install --target "$(python3 -m site --user-site)" html5lib` after PEP 668 blocked a plain user install | `html5lib` 1.1 importable from the default interpreter without `--break-system-packages` |
| 2026-08-14 | Validation environment | `check-repo-contracts.sh` on the default interpreter | `failures=0`, PASS; the Stop-gate path now reaches the same result as the prepared interpreter |

| 2026-08-14 | G2a Harness and loop | Changed-document metadata against `88f4b2e2` | `selected=4 violations=0 legacy_exceptions=0 transition_overrides=0` |
| 2026-08-14 | G2a Harness and loop | Top-level heading comparison against BASE `2ca5f4b8` | Section order preserved in all four leaves, including the pre-existing `Common Construction Matrix` |
| 2026-08-14 | G2a Harness and loop | Personal-path and identifier scan | 0 matches across the four owned leaves |

| 2026-08-14 | G2b Model and memory | Changed-document metadata against `1e61643c` | `selected=4 violations=0 legacy_exceptions=0 transition_overrides=0` |
| 2026-08-14 | G2b Model and memory | Frontmatter and section census | All four leaves keep `status: draft`, carry `reviewed_at: 2026-08-14`, and retain nine top-level sections |
| 2026-08-14 | G2b Model and memory | External catalog re-pin | `agency-agents` default-branch SHA re-verified unchanged since the 2026-08-08 pin via `git ls-remote` rather than a re-clone |

| 2026-08-14 | G3 SDLC and documentation | Changed-document metadata against `9f931ff1` | `selected=5 violations=0 legacy_exceptions=0 transition_overrides=0` |
| 2026-08-14 | G3 SDLC and documentation | Frontmatter and section census | All five leaves keep `status: draft`, carry `reviewed_at: 2026-08-14`, and retain nine top-level sections |
| 2026-08-14 | G3 SDLC and documentation | External source re-pin | Spec Kit and OpenSpec re-pinned at fresh commits after upstream evolution; Diataxis re-fetched successfully after its earlier HTTP 429; `agents.md` recorded as having moved under Linux Foundation governance; `iso.org` not re-attempted and routed to a browser-capable reviewer |

| 2026-08-14 | G1 Foundation | Changed-document metadata against `f2e96ed4` | `selected=2 violations=0 legacy_exceptions=0 transition_overrides=0` |
| 2026-08-14 | G1 Foundation | Fourteen-scope axis preservation check | All fourteen normative scope identifiers remain present in the matrix leaf |
| 2026-08-14 | G1 Foundation | Governance contract validator run by the cluster agent | `PASS contracts=3 agents=14 functions=24 providers=3 failures=0` and `PASS mode=repository failures=0` |
| 2026-08-14 | G1 Foundation | Governance test suite run by the cluster agent | 159 tests, `OK` |

| 2026-08-14 | Index reconciliation | Changed-document metadata against `4f37f0c1` | `selected=4 violations=0 legacy_exceptions=0 transition_overrides=0` |
| 2026-08-14 | Generated route | `generate-llm-wiki-index.sh --check` before regeneration | FAIL, stale |
| 2026-08-14 | Generated route | `generate-llm-wiki-coverage.sh --check` before regeneration | FAIL, stale |
| 2026-08-14 | Generated route | Path-set comparison of the regenerated index against `HEAD` | 1,064 to 1,067 paths; exactly three additions and zero removals |
| 2026-08-14 | Generated route | Both generators re-run, then `--check` re-run | Both PASS, fresh; coverage safe tracked source paths moved 1,338 to 1,341 |

| 2026-08-14 | Document-family split | Role-row census of the regrouped `Complete role contract` | Two subsections holding exactly six SDLC lifecycle roles and six operations roles; all twelve original rows present, none dropped or reworded |
| 2026-08-14 | Document-family split | Changed-document metadata for the affected leaf | `violations=0` |

Cluster rows are appended to this table as each cluster closes.

### Verification results

The ledger-creation unit passes changed-document metadata and traceability.

The repository contract initially returned `failures=1` on the host interpreter.
That failure is not a repository defect and is not unowned: `scripts/requirements.txt`
line 4 declares `html5lib>=1.1,<2.0` as a required validation dependency, and
`scripts/validation/agent_governance_contract.py` line 32 imports it fail-closed.
The host simply lacked the declared dependency. Preparing an interpreter from the
repository's own requirements file resolves it, and the full contract then passes
at `failures=0`.

This corrects the characterization inherited from the predecessor record, which
described the gap as pre-existing and unowned. The owner is the declared
requirements file; the missing element was local environment preparation. Later
units in this Task run the repository contract with the prepared interpreter.

Both LLM Wiki generator checks are `Not Run` for this unit because it adds no
research path and changes no generated input.

## Controlled Agent Pre-commit Evidence

### Controlled wrapper command

`Not Run`. The approved final QA gate wrapper
`scripts/validation/run-agent-precommit-all-files.sh` is invoked only at the
Task's final gate, not per cluster.

### Controlled wrapper allowed prefixes

`Not Run`.

### Controlled wrapper exit status

`Not Run`.

### Controlled wrapper snapshot result

`Not Run`.

### Controlled wrapper observation boundary

`Not Run`.

### Controlled wrapper path sets

`Not Run`.

### Controlled wrapper disposition

`Not Run`.

## Review Evidence

### Implementation review verdict

`Not Run`.

### Specification review verdict

`Not Run`.

### Quality review verdict

`Not Run`.

### Review findings and disposition

`Not Run`.

## Commit Ledger

### Commit identity

| Logical unit                   | Commit  | Scope                                      |
| ------------------------------ | ------- | ------------------------------------------ |
| Ledger creation                | Pending | This Task and the execution task index row |
| G1 Foundation                  | Pending | Two Foundation leaves                      |
| G2a Harness and loop           | Pending | Four agentic-construction leaves           |
| G2b Model and memory           | Pending | Four model and memory leaves               |
| G3 SDLC and documentation      | Pending | Five SDLC and documentation leaves         |
| G4 Delivery and quality        | Pending | Three delivery and quality leaves          |
| G5 Infrastructure and security | Pending | Two infrastructure and security leaves     |
| Index reconciliation           | Pending | Pack README and parent research router     |

### Commit logical unit

Each cluster closes as exactly one commit covering only its owned leaves. The
ledger row for that cluster is updated in the same commit.

### Commit validation

Each commit runs the changed-document metadata command against its own base and
records the observed `selected`/`violations` counts before staging.

## Deferred and Blocked Items

### Deferred items

- Leaf `status` promotion from `draft` to `active` is deferred. Deepening changes
  leaf content, not the pack's publication state.

- The generated LLM Wiki index was already stale before this Task began. Of the
  three paths the regeneration adds, only
  `docs/04.execution/tasks/2026-08-14-agentic-research-pack-deepening.md` belongs
  to this Task. The other two,
  `docs/04.execution/tasks/2026-08-11-agentic-research-pack-source-refresh.md` and
  `docs/00.agent-governance/memory/ignored-sdd-scratch-deletion.md`, were created
  by earlier work that did not refresh the generated route.

  The generators rebuild the whole index, so a partial refresh limited to this
  Task's own path is not available. This Task therefore corrects the pre-existing
  omission as an unavoidable consequence of running the generator, records it
  here rather than presenting it as its own change, and hand-edits nothing. The
  original Task boundary that excluded generated artifacts was wrong for a Task
  that adds a tracked document, and it was corrected in place rather than
  worked around.

### Blocked items

- Old-pack deletion is blocked outside this ledger. `docs/04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md`
  records Task 11 Step 0d as `BLOCKED` under its five-round review breaker with
  no round 6. The user-approved Step 0e tree-object, sealed-descriptor, and
  atomic-bundle recovery is the sole current path.

- Step 0e readiness observed on 2026-08-14 for routing purposes only. This Task
  performs no Task 11 action; the observation is recorded so the deletion owner
  can resume from a known state.

  | Item                                                                        | Observed state                                                                             |
  | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
  | Step 0e round 1 implementation `6817a76f`                                   | Ancestor of this branch `HEAD`                                                             |
  | Step 0e round 1 reviews                                                     | Needs fixes C0/I1/M0 (specification) and C0/I2/M0 (Python/security) per the rebuild ledger |
  | Step 0e fix round 1                                                         | Rebuild ledger records all three findings addressed in the minimal helper/test/Task subset |
  | `scripts/validation/agentic-research-gate9-evidence.py`                     | Present, 128.7 KB                                                                          |
  | `tests/validation/test_agentic_research_gate9_evidence.py`                  | Present, 112.6 KB                                                                          |
  | `python3 -m unittest tests.validation.test_agentic_research_gate9_evidence` | 32 tests, `OK`, 114.671s, run on 2026-08-14                                                |

  The blocking item is review state, not code state. A first reading of this
  Task placed the open review at Step 0e fix round 1; a closer reading of the
  Plan's reviewed correction gate corrected that. The actual sequence is
  recorded below, and the earlier characterization is superseded.

  Recovery rounds consumed, per the Plan's own accounting:

  | Round                     | Commit     | Review outcome                                                                                           |
  | ------------------------- | ---------- | -------------------------------------------------------------------------------------------------------- |
  | 1, initial implementation | `6817a76f` | Specification Needs fixes C0/I1/M0; Python/security Needs fixes C0/I2/M0                                 |
  | 2, first fix              | `cfc271c5` | Both re-reviews Needs fixes C0/I2/M0; the original semantic finding closed, two residual findings opened |
  | 3, second fix             | `96d06221` | Recorded in the Plan only; the rebuild Task ledger still carries this commit identity as pending         |

  The Plan states that the residual findings after round 3 do not authorize
  another same-implementer edit, and that round 4 requires a fresh, more capable
  implementer. Before round 4 may begin, the Plan itself must pass a Plan-only
  correction gate:

  | Plan-only step | Commit     | Review outcome                                                                                                                              |
  | -------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
  | Correction     | `1cd723fa` | Found insufficient: `--bundle` alone cannot bind a later consumer to the controller-captured build receipt                                  |
  | fix-1          | `bb1794cd` | Specification Approved C0/I0/M0; Python/security Needs fixes C0/I1/M0 on a FIFO substituted after raw snapshot blocking Git ref enumeration |
  | fix-2          | `0b9bd01b` | Both independent re-reviews returned on 2026-08-14: specification `Needs fixes C0/I1/M4`, Python/security `Needs fixes C0/I3/M3`            |

  Plan-only fixes do not consume an implementation round. The Plan forbids
  beginning round 4, or editing the Task, helper, or tests, until both fix-2
  re-reviews return C0/I0/M0. Package construction, Phase A, evidence-ref
  publication, real-index staging, deletion, pinned lifecycle reconciliation,
  Task 12, remote actions, and push all remain closed.

  This Task dispatched the two fix-2 re-reviews and records their verdicts as
  routing evidence. It takes no action on them, because the Plan is outside
  this Task's allowed paths.

  Both reviewers reached the same root defect independently: the latency bound
  fix-2 introduced is scoped by name to `git for-each-ref`, leaving other
  blocking calls on the generic unbounded runner.

  | Finding         | Reviewer        | Substance                                                                                                                                                                                                                                                                                                                                                                                                     |
  | --------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | I1              | Both            | The bound covers `for-each-ref` only. The Python/security reviewer measured that `for-each-ref` does not block on special-file substitution at all; it skips silently. The blocking call is the `git symbolic-ref --quiet` fallback, reached exactly when `for-each-ref` returns empty, which is exactly the substituted-FIFO case. The hazard named in fix-1 is therefore untouched by fix-1 and fix-2 alike |
  | I2              | Python/security | The create-only CAS `git update-ref --no-deref` is excluded from the bound and creates `<ref>.lock` before the blocking read, so terminating a blocked run leaves a stale lock that the Plan's own raw enumeration must reject as `FOREIGN_REF` permanently                                                                                                                                                   |
  | I3              | Python/security | Mandated RED test 4 cannot pass as written: injecting a FIFO ahead of `for-each-ref` produces no timeout and no child to reap, so its bound, grace, and reap assertions are vacuous while the run hangs in the unbounded `symbolic-ref`                                                                                                                                                                       |
  | I1, second half | Specification   | The risk row edited by this same diff promises the helper stops "without blocking", a property the corrected contract does not deliver                                                                                                                                                                                                                                                                        |

  Consequence: fix-2 does not pass the Plan-only gate and recovery round 4 stays
  closed. The implementation count remains three of five. A fix-3 would need to
  re-target the correction at the calls that actually block, rather than extend
  the existing name-scoped bound.

- Gate redesign review, approved by the user on 2026-08-14 after three
  successive Plan corrections each targeted a hazard that was not where the
  correction assumed. Two independent read-only investigations were dispatched:
  one on threat-model coherence, one on measured hazard surface. Both are
  recorded here because they change what a fix-3 must say.

  Threat-model finding. Gate 9's stated trust boundary defends against a
  reviewer subagent asserting a review it did not perform. That principal can
  emit text and nothing else; the tracked review-family roles in `.claude/agents/`
  are provisioned `Read`, `Grep`, and `Glob` only. The findings that keep failing
  the gate defend against a principal with write access to `.git` or to a
  same-UID temporary path. Those are disjoint principal sets, not two points on
  one spectrum.

  The decisive point is that the second principal already holds strictly easier
  total bypass. The helper executes from the worktree as a user-writable file;
  its self-integrity preflight validates its own already-loaded bytes from
  inside the same process; `run_git` invokes bare `git` with an inherited
  environment, and the repository root is resolved before any authority check.
  The Plan itself names this adversary a concurrent same-UID actor and concedes
  the guarantee is unattainable under POSIX, then resolves the round by
  redefining the linearization point rather than closing the finding. A defence
  whose own specification concedes impossibility cannot terminate.

  Measured hazard surface. An AST-derived inventory found 151 external call
  sites, 59 process and 92 filesystem, funnelling through three physical
  `subprocess.run` calls. The string `timeout` appears zero times in 3,512
  lines, and none of the three calls passes a timeout. Eight sites were measured
  as actually blocking under substitution against a regular-file control that
  completes in single-digit milliseconds:

  | Site                                                                      | Blocking condition                                                                            |
  | ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
  | `git symbolic-ref --quiet`                                                | FIFO, symlink to FIFO, symlink to device                                                      |
  | `git update-ref --no-deref`                                               | Creates `<ref>.lock` before the blocking read                                                 |
  | `git diff --quiet`, `git diff --cached --quiet`, `git status --porcelain` | FIFO at `.git/index`, reached before the only `S_ISREG` index guard, so the guard never fires |
  | `os.open` in the control-file reader                                      | Bare FIFO at any of ten CLI control-file arguments                                            |
  | `os.open` in the bundle reader                                            | FIFO matching the bundle name pattern                                                         |
  | Eight `Path.read_bytes()` sites                                           | Their respective paths                                                                        |

  The calls fix-1 and fix-2 bounded were measured as not blocking. `for-each-ref`
  returns exit zero with empty output for all six substitutions, which satisfies
  the existing guard and forces the unbounded fallback. That is why two
  corrections in a row missed.

  Test-coverage finding, correcting the specification reviewer's reading. No
  hazard assertion in the suite is vacuous. The defect is absence: `mkfifo` and
  `mknod` appear zero times in the test file, so all eight measured blocking
  sites are untested. Two tests whose names read as special-file coverage
  exercise regular-file dirent races instead.

  Recovery finding. A terminated blocked run leaves an orphan zero-byte `.lock`.
  If the substitution persists the helper re-blocks; if it is removed the helper
  rejects permanently as `FOREIGN_REF`, a misleading terminal code because no
  `.lock` inspection exists anywhere in the source. A blocked child also
  survives parent termination, because no call establishes a new session or
  process group and nothing reaps it.

  Proportionality finding. The deletion under guard is locally reversible and
  remotely replicated. All twenty blobs at `HEAD` are byte-identical to
  `origin/main`, the deletion occurs on a local-only branch, and restoration was
  verified by execution at twenty of twenty files with the worktree untouched.
  Permanent loss would additionally require local garbage collection and a
  force-push that the approved boundary already forbids.

  Consequent redesign direction, carried into fix-3: keep the security claim
  scoped to reviewer-identity binding, where it is well matched and already
  sufficient; reclassify the filesystem hazards as availability and robustness
  requirements, where the obligation is a finite measured list rather than an
  unbounded space of imagined races; and place the bounds at the three
  `subprocess.run` funnels and the descriptor-opening helpers rather than at
  individually named commands.

  One real capability gap was found and is not the one under repair.
  `qa-engineer` is the only review-family role provisioned with `Edit`, `Write`,
  and `Bash`. If a Gate 9 reviewer role resolves to it, the distrusted reviewer
  acquires exactly the capability set the gate treats as hostile, and
  simultaneously the ability to bypass the gate. The proportionate control is a
  role-assignment constraint at capability provisioning, not another filesystem
  race defence.

- Plan fix-3 outcome and the Spec boundary conflict it exposed, recorded
  2026-08-14. The user directed that Spec, Plan, and Task be inspected and
  reconciled before continuing.

  fix-3 was committed as `b6e2219f` with the Plan's declared subject and passed
  changed-document metadata, traceability, and the repository contract. Both
  independent re-reviews then returned `Needs fixes; C0/I4/M4`. Their receipts
  are recorded in the rebuild Task, which the Plan designates as receipt owner.

  The Python/security reviewer's agent terminated on a session limit after
  writing its review. The artifact is complete: 340 lines, every review question
  answered in a closing checklist, and a terminal verdict line. Its final
  message indicated an intent to cross-check the Plan's claims against helper
  source, so that corroboration step is unperformed and is not claimed here.

  Two findings were independently reached by both reviewers: the respecified RED
  method still cannot fire on the CAS and lock-residue path, and the funnel
  definition does not cover what its own closure claim asserts.

  The Spec conflict. Spec 137 section `Gate 9 evidence architecture boundary`
  records a user-approved boundary dated 2026-08-09 stating that package
  construction may append Git objects but may not delete objects, mutate a
  branch, index, or worktree, or clean up unreachable objects, and that a
  separately reviewed create-only evidence-ref publication is the only permitted
  Gate 9 ref mutation. The Spec assigns the Plan ownership of executable schemas
  only within that boundary.

  The `STALE_REF_LOCK` clearance introduced by fix-3 unlinks a `.lock` file
  inside `.git`. The Python/security reviewer identified this as a new
  destructive operation on its own merits. Read against the Spec it is also
  outside the approved architecture boundary, so it cannot be repaired by
  refining its clearance conditions. Either the design drops the unlink, or the
  Spec boundary changes, and the Spec boundary is user-approved.

  Consequent direction for a fix-4: treat an orphan lock as a fail-closed
  terminal state that reports what a human must clear, rather than as a state
  the gate clears itself. That removes the destructive operation, removes the
  ownership-attribution problem the reviewer raised, and stays inside the
  approved Spec boundary. The remaining findings on funnel definition, terminate
  and reap vocabulary for non-spawning funnels, the index-guard worked example,
  and RED method reachability are contract-text defects that do not touch the
  Spec boundary.

- Plan fix-4 outcome, recorded 2026-08-14. Committed as `a6613da9` with the
  Plan's declared subject; changed-document metadata, traceability, and the
  repository contract all passed. Both independent re-reviews then returned
  `Needs fixes`: specification `C0/I4/M5`, Python/security `C0/I2/M5`. Receipts
  are in the rebuild Task.

  What this round settled. The Python/security reviewer verified the no-mutation
  claim exhaustively and upheld the central design: the lock-residue path is
  read-only end to end, the Spec 137 architecture boundary is respected and
  correctly cited so a later round cannot re-derive clearance, the Plan's own
  static scan banning the `unlink` token independently forecloses it, the index
  guard anchor provably precedes all six `git diff` calls in
  `authority_preflight`, the CAS sub-case boundary sits where claimed, and the
  declared indistinguishability of lock origins introduces no hazard beyond a
  denial that already requires total-bypass capability. The specification
  reviewer independently confirmed the Spec boundary check and found the
  no-clearance semantics consistent in all four locations.

  This is the first round in which the structural judgement passed. The
  remaining defects are text-consistency and measured-behaviour mismatches.

  Where the two reviewers diverged. The Python/security reviewer accepted every
  RED sub-case as injecting at a reachable site; the specification reviewer
  measured that two of them assert an outcome that does not occur, because a
  blocked `git update-ref --no-deref` exits on `SIGTERM` within a second and git
  then removes its own lock. Both readings hold: injection reachability and
  assertion firing are separate properties, and the specification reviewer
  examined the second.

  Important-finding trend across the Plan-only gate: fix-2 four, fix-3 eight,
  fix-4 six. The fix-3 increase came from a self-clearing design that added a
  new destructive operation; removing that design reversed the trend.

- Plan fix-5 outcome, recorded 2026-08-14. Committed as `a17281a8` with the
  Plan's declared subject; metadata, traceability, and the repository contract
  all passed. The Python/security re-review returned `Approved; C0/I0/M6`, the
  first approval in this correction gate. The specification re-review returned
  `Needs fixes; C0/I2/M5`, closing five of the six fix-4 defects.

  Both reviewers verified against primitives rather than accepting the Plan's
  account. The Python/security reviewer measured `setitimer` armed before `open`
  interrupting a parked FIFO open at 0.500 seconds on CPython 3.12.3, confirmed
  `poll()` returns `POLLIN` immediately on a regular descriptor so its demotion
  is correct, and read the exit-1 convention out of the helper's own ternary at
  `agentic-research-gate9-evidence.py:3507`. The specification reviewer verified
  the same exit convention and the size-independent predicate against the helper,
  and confirmed the namespace enumeration is `for-each-ref`-only, so a `.lock` is
  invisible today rather than misreported as fix-4 had claimed.

  Both confirmed no Spec 137 mutation was reintroduced and nothing fix-4
  established was weakened. The new planted-lock fixture creates its file as a
  test action inside a temporary root, with the gate's non-interference asserted.

  The two remaining Important findings share one root: the Plan contradicts its
  own other clauses. The claim that no omitted leaf reaches `for-each-ref`
  through the gate is falsified by the Plan's own sub-case 2, and the retargeted
  disagreement instantiation is unreachable for the same class of reason as the
  one it replaced, which the reviewer established by measuring git 2.43.0 rather
  than by reading the Plan.

  Important-finding trend across the Plan-only gate: fix-2 four, fix-3 eight,
  fix-4 six, fix-5 two. Structure, Spec-boundary compliance, round accounting,
  and the security dimension are now all settled; what remains is internal
  consistency of two statements.

### Deferral destination

Deletion and its lifecycle reconciliation remain owned by Task 11 in
`docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`. This Task
strengthens the claim-migration evidence that gate consumes but does not open it.

## Related Documents

- [Spec 137](../../03.specs/137-agentic-research-pack-rebuild/spec.md)
- [Rebuild Plan](../plans/2026-08-08-agentic-research-pack-rebuild.md)
- [Rebuild Task holding the deletion gate](./2026-08-08-agentic-research-pack-rebuild.md)
- [Source refresh Task](./2026-08-11-agentic-research-pack-source-refresh.md)
- [Canonical research pack](../../90.references/research/2026-08-08-agentic-engineering-research-pack/README.md)
- [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
