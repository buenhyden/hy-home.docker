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
- Regenerating LLM Wiki output or editing LLM Wiki generators.
- Runtime, remote, push, pull request, or merge actions.

## Scope and Change Boundaries

### Allowed paths

- `docs/90.references/research/2026-08-08-agentic-engineering-research-pack/*.md`
- `docs/90.references/research/README.md` (only if routes or counts change)
- `docs/04.execution/tasks/2026-08-14-agentic-research-pack-deepening.md`
- `docs/04.execution/tasks/README.md` (task index row)
- `docs/00.agent-governance/memory/current.md` (bounded handoff refresh)

### Forbidden paths

- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/`
- `docs/03.specs/`, `docs/04.execution/plans/`
- `docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`
- `docs/90.references/llm-wiki/`, `llms.txt`, and their generators
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

  The blocking item is therefore review state, not code state: the fresh
  independent specification and Python/security re-reviews of Step 0e fix
  round 1 remain `Not Run`, and both must return C0/I0/M0 before a real Gate 9
  bundle, package reviews, evidence-ref publication, real-index staging,
  deletion, and pinned lifecycle reconciliation may proceed. Two of the five
  recovery rounds are consumed.

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
