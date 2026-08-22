---
profile_id: task
status: active
artifact_id: task-0137-0002
artifact_type: task
parent_ids:
  - SPEC-0137
  - plan-0137
created: 2026-08-11
updated: 2026-08-22
---

# Task: Agentic Engineering Research Pack Source Refresh

## Overview

This Task is the execution evidence ledger for an in-place source refresh of the
canonical `2026-08-08-agentic-engineering-research-pack`. It re-verifies external
sources and tracked workspace evidence for the pack's twenty leaves and its
index, and records the observed result of that re-verification.

The refresh does not create a new pack, does not rename or relocate any file, and
does not change the pack's topic decomposition. It updates leaf bodies, source
observations, and `reviewed_at` metadata only where re-verification produced a
material change.

This ledger reports observed evidence only. An unperformed activity is `Not Run`.
No Stage 90 research statement in this pack becomes policy, runtime truth, or
remote-enforcement proof.

Immutable BASE for this Task is `0b9bd01b548e615dcdfa5e893acbaa07cd3550be` on
branch `codex/agentic-research-rebuild`.

## Inputs

- Approved user direction recorded in Approval Evidence.
- Active Spec authority: `docs/03.specs/0137-agentic-research-pack-rebuild/spec.md`.
- Canonical pack under refresh:
  `docs/90.references/research/2026-08-08-agentic-engineering-research-pack/`.
- Authoring contract: `docs/99.templates/templates/common/reference.template.md`.
- Metadata contract: `scripts/validation/check-document-metadata.py`.
- Repository contract: `scripts/validation/check-repo-contracts.sh`.

## Goals and Non-goals

### Goals

- Re-verify high-volatility external sources for the nine Tier A leaves.
- Re-verify tracked workspace evidence and external link/version survival for the
  eleven Tier B leaves.
- Reconcile the pack index and cross-links with any leaf change.
- Record per-cluster logical commits and verification evidence in this ledger.

### Non-goals

- Creating a new dated research pack or relocating existing files.
- Changing the pack's twenty-leaf topic decomposition.
- Modifying Spec 137, its Plan, Task 10b, or Task 11.
- Deleting or editing the retiring `2026-07-05-agentic-research-pack-refresh/`
  pack, whose deletion gate remains owned by Task 11.
- Regenerating LLM Wiki output or editing LLM Wiki generators.
- Runtime, remote, push, pull request, or merge actions.

## Scope and Change Boundaries

### Allowed paths

- `docs/90.references/research/2026-08-08-agentic-engineering-research-pack/*.md`
- `docs/90.references/research/README.md` (only if leaf counts or routes change)
- `docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0002-source-refresh.md`
- `docs/04.execution/tasks/README.md` (task index row)
- `docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0004-stage00.md` (bounded handoff refresh)

### Forbidden paths

- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/`
- `docs/03.specs/`, `docs/04.execution/plans/`
- `docs/90.references/llm-wiki/`, `llms.txt`, and their generators
- `infra/`, `secrets/`, any credential-bearing surface

### Compose impact

None. This Task changes no Compose file, service definition, or runtime setting.

### Security impact

None expected. The refresh records no secret value, credential, token, private
key, shell history, or raw log. Security source re-verification updates analysis
text only.

### Operations impact

None. No runbook, incident, or policy body is authored or altered.

### Runtime impact

None. No runtime or remote state is observed or mutated by this Task.

## Approval Evidence

### Approval source

The user approved the refresh design in session on 2026-08-11 with an explicit
one-word approval reply, after selecting: refresh over rebuild;
volatility-prioritized leaf scope; a new Task as the only governance artifact;
and a two-tier, domain-clustered subagent decomposition.

### Protected surfaces

The retiring 2026-07-05 pack, Spec 137, the active Plan, Task 10b, Task 11, and
all generated LLM Wiki artifacts remain untouched and outside this boundary.

### Approval boundary

Approval covers in-place refresh of the canonical pack plus this Task ledger and
the bounded memory handoff. It does not authorize deletion, pack relocation,
generator changes, push, or any remote action.

### Rollback or recovery

Every change is a tracked Git commit on `codex/agentic-research-rebuild`.
Recovery is `git revert` of the named cluster commit; no external state changes.

### Redaction boundary

No secret, credential, token, private key, personal data, shell history, or raw
log is recorded in this Task or in any refreshed leaf.

## Work Breakdown

The pack's twenty leaves are partitioned into two volatility tiers and six
non-overlapping ownership clusters. No two clusters own the same file.

### Tier A — full external re-research

Leaves whose claims depend on fast-moving vendor product documentation.

| Cluster                        | Owned leaves                                                                                       | Primary external hosts                                                     |
| ------------------------------ | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| A1 Provider and model          | `provider-implementation-comparison.md`, `provider-model-landscape.md`, `agent-model-selection.md` | `code.claude.com`, `platform.claude.com`, `learn.chatgpt.com`, `agents.md` |
| A2 Harness, loop, instruction  | `harness-engineering.md`, `loop-engineering.md`, `agent-instructions-vibe-coding.md`               | provider hook and subagent documentation                                   |
| A3 Catalog, memory, automation | `ai-agent-catalogs.md`, `memory-hierarchy.md`, `automation-pipeline-workflow.md`                   | `github.com/msitarzewski/agency-agents`, `docs.github.com`                 |

### Tier B — workspace re-verification and source survival check

Leaves anchored mainly on versioned standards and tracked workspace evidence.

| Cluster                          | Owned leaves                                                                                                                             |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| B1 Delivery and quality          | `quality-ci-formatting.md`, `security-governance.md`, `verification-validation.md`                                                       |
| B2 SDLC and documentation        | `spec-driven-sdlc.md`, `sdlc-document-roles.md`, `documentation-architecture.md`, `document-metadata-lifecycle.md`, `llm-wiki-system.md` |
| B3 Infrastructure and foundation | `docker-compose-infrastructure.md`, `workspace-baseline.md`, `scope-application-matrix.md`                                               |

### Integration

Index reconciliation (`README.md`), cross-link consistency, this ledger, the task
index row, and the bounded memory handoff are owned by the orchestrating session,
not by a cluster agent.

### Per-cluster agent contract

Each cluster agent receives its owned file list and may write only those files.
Each agent must keep leaf bodies in English, edit in place, preserve the
`reference.template.md` required sections, end each document with exactly one
`## Related Documents` section, mark unobserved runtime or remote facts
`UNVERIFIED`, and record no secret value. Creating new files, authoring policy
text, and touching another cluster's files are prohibited.

## Work Log

- Step 0 (`Done`): Coverage analysis established that the twenty existing leaves
  already cover every requested research category, that no topic gap exists, and
  that a refresh rather than a rebuild is the correct unit. External host census
  produced the volatility tiering used in Work Breakdown.
- Step 1 (`Done`): This Task ledger created at BASE `0b9bd01b`; commit `8976824a`.
- Step 1a (`Done`): Out-of-scope breakage recorded. While removing a scratch
  directory this unit had just created, the agent deleted `.superpowers/` in
  this worktree, destroying the prior 2026-08-08 plan's git-ignored subagent
  working set. Three files cited by SHA-256 in the rebuild Task's Inputs table
  are unrecoverable; all three are self-labeled advisory input, not durable
  authority. Recovery from the main checkout and the sibling worktree was
  attempted and failed. The user directed recording and continuing. Memory note
  `ignored-sdd-scratch-deletion.md`; commit `7a88efc1`.
- Step 2 (`Done`): Clusters A1, A2, and A3 re-verified nine Tier A leaves
  against live vendor documentation. A1 and A2 found no stale claim across six
  leaves. A3 corrected `memory-hierarchy.md` note counts and bounds after this
  unit added one durable memory note. Commit `55809319`.
- Step 3 (`Done`): Cluster B3 re-derived foundation counts. `workspace-baseline.md`
  corrected tracked paths 1,646 to 1,672, script/validation 63/41 to 64/42,
  Stage 00 109 to 110, Stage 04 237 to 238, Stage 90 97 to 118.
  `scope-application-matrix.md` confirmed the fourteen-scope axis unchanged and
  refreshed stale Spec/Plan source citations. `docker-compose-infrastructure.md`
  survived re-verification unchanged. Commit `bc16b198`.
- Step 4 (`Done`): Cluster B2 corrected corpus counts in `spec-driven-sdlc.md`
  and `document-metadata-lifecycle.md` (531 to 532 leaves, 234 to 235 execution,
  2 to 3 draft, Task 131 to 132), and corrected `llm-wiki-system.md` generated
  path measurements and freshness routing. `sdlc-document-roles.md` and
  `documentation-architecture.md` survived unchanged. Commit `7a5eb5cd`.
- Step 5 (`Done`): Cluster B1 was interrupted mid-task by an API session limit
  and was resumed from its transcript. On resume it justified rather than
  retracted its security-readiness reframing, corrected an unreproducible
  "32 SHA-pinned actions" figure to the verified 17, corrected the Python
  `unittest` file count 22 to 24, and added an ISO source revalidation note
  after `iso.org` returned HTTP 403. Commit `22b06ba1`.
- Step 6 (`Done`): Independent review of `7a88efc1..7a5eb5cd` returned
  specification `PASS` and quality `Needs fixes` with one Important finding.
  Fix round 1/5 corrected `spec-driven-sdlc.md` line 99, where the prose
  restated the pre-correction leaf count that the adjacent table already fixed.
  Commit `acd46f28`.
- Step 7 (`Done`): Independent review of `7a5eb5cd..22b06ba1` returned
  specification `PASS` and quality `Approved`, C0/I0/M0.
- Step 8 (`Done`): Pack index reconciled with the refresh boundary, ledger
  closed, and the bounded memory handoff refreshed.

## Verification Evidence

### Exact commands

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed
bash scripts/validation/check-repo-contracts.sh
```

### Expected evidence

Metadata validation passes for every changed Markdown path before each cluster
commit. The repository contract check passes with zero failures before ledger
closure.

### Actual evidence

Changed-path metadata validation ran before every commit in this unit and
returned `violations=0` each time, with eight pre-existing legacy exceptions
outside this Task's scope and zero new deficits.

The repository contract check first returned `failures=2`. One failure,
`closed English-only doc surfaces contain Korean text`, was caused by this Task
quoting the user's Korean approval reply verbatim inside an English-only
surface; the quotation was replaced with an English description. The other,
`AGC-DEPENDENCY-MISSING path=html5lib location=validation-runtime`, is a
pre-existing validation-runtime dependency gap in the default interpreter and
is not caused by any change in this unit.

Re-run after the English-only correction returned `failures=1`, leaving only
the `html5lib` dependency gap. Re-run in an isolated interpreter that provides
`html5lib` 1.1 returned `failures=0`.

The controller independently re-derived the load-bearing numbers rather than
accepting agent self-reports: tracked paths 1,672; `scripts/` 64 and
`scripts/validation/` 42; Stage 00 110; Stage 04 238; Stage 90 118; scope files
14; durable memory notes 8; generated LLM Wiki index 1,473 lines and 202,188
bytes; generated coverage snapshot 127 lines and 11,911 bytes; tracked Python
`unittest` files 24; workflow `uses:` references 17 of 17 pinned to full commit
SHAs. All matched the refreshed text.

The controller also executed
`bash scripts/validation/generate-security-automation-readiness.sh --check`,
which returned `PASS` at exit 0, and counted the snapshot's control rows at 11
Implemented, 1 Partially Implemented, and 1 Gap. This corroborates the
security-readiness reframing in `security-governance.md`.

### Verification results

Documentation contract state is clean for this unit. The only outstanding
repository-contract failure in the default environment is the pre-existing
`html5lib` runtime dependency gap, which is unrelated to this Task and is not
claimed as resolved here.

No generator was executed by this unit. LLM Wiki freshness statements in
`llm-wiki-system.md` cite the Stage 04 rebuild ledger's recorded result and
state plainly that this reference did not re-run either check.

## Controlled Agent Pre-commit Evidence

### Controlled wrapper command

`scripts/validation/run-agent-precommit-all-files.sh` is the only permitted
all-files pre-commit entry point and is reserved for an approved final QA gate.

### Controlled wrapper allowed prefixes

`docs/90.references/research/2026-08-08-agentic-engineering-research-pack/`,
`docs/90.references/research/README.md`, `docs/04.execution/tasks/`,
`docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0004-stage00.md`.

### Controlled wrapper exit status

`Not Run`.

### Controlled wrapper snapshot result

`Not Run`.

### Controlled wrapper observation boundary

Only Git-visible, non-ignored repository paths are in scope for this wrapper.

### Controlled wrapper path sets

`Not Run`.

### Controlled wrapper disposition

Deferred to the approved final QA gate for this Task.

## Review Evidence

### Implementation review verdict

Each cluster agent self-reported per-leaf results to a report file. Self-reports
were treated as claims to audit, not as evidence. Every load-bearing number was
independently re-derived by the controller before its commit.

### Specification review verdict

Two independent reviews ran over disjoint commit ranges. Review of
`7a88efc1..7a5eb5cd` returned `PASS`. Review of `7a5eb5cd..22b06ba1` returned
`PASS`.

### Quality review verdict

Review of `7a88efc1..7a5eb5cd` returned `Needs fixes` with one Important
finding, resolved in fix round 1/5. Review of `7a5eb5cd..22b06ba1` returned
`Approved` at C0/I0/M0.

### Review findings and disposition

- Important, resolved: `spec-driven-sdlc.md` line 99 restated the
  pre-correction Stage 01-05 leaf count in prose while the adjacent table
  already carried the corrected value. Fixed in commit `acd46f28` after the
  controller independently re-derived 532. A sweep of both affected leaves for
  further prose restatements of changed counts found none.
- Disclosed, not a finding: the 37-non-gateway-port and 102-volume-declaration
  figures in `security-governance.md` were corroborated through an unchanged
  freshness snapshot rather than re-derived cell by cell. Neither figure was
  among the claims re-verification showed to be stale. Routed as a gap for a
  future infrastructure-focused unit.
- Disclosed, not a finding: `iso.org` returned HTTP 403 on repeated automated
  retrieval. The dependent claim was retained with a Maintenance revalidation
  note and corroborated through the sibling IEEE route. The source is not
  represented as verified.
- Process deviation, recorded: fix round 1/5 was verified directly by the
  controller instead of through a dispatched scoped re-review. The finding was
  a single scalar the controller had already re-derived independently, and the
  fix diff was one line. This is recorded rather than silently skipped.
- Process deviation, recorded: cluster agents were dispatched in parallel and
  prohibited from running any Git command, with the controller owning every
  commit. File ownership was partitioned so that no two agents could write the
  same path.
- Critical, resolved: the final whole-unit review found that this unit's own
  memory handoff summarized the outcome as six leaves unchanged and eight
  changed. The true split is eleven unchanged and nine changed; the bad figures
  came from summing only some clusters and dropping cluster A3. The controller
  re-derived the true split from `git diff --name-only` over the pack before the
  correction landed. This defect was in the controller's own bookkeeping, not in
  any agent's output.
- Important, resolved: the final review found this Task's front matter status
  inconsistent with its own closed Work Log, and identified that the status is
  load-bearing because this Task leaf is inside the Stage 01-05 corpus whose
  status split two refreshed leaves report. The first fix set `completed`, which
  then failed `AGC-MEMORY-STALE-STATE` because the memory contract requires the
  current-task label to name a `draft` or `active` Task. The resolved value is
  `active`: execution and verification are finished, owner acceptance is not.
  Both dependent leaves were re-measured to 295 active, 235 completed, and 2
  draft over 532 leaves, and their boundary sentences were rewritten to describe
  the coupling instead of naming a status value that would go stale again.

## Commit Ledger

### Commit identity

| Commit     | Logical unit                                                       |
| ---------- | ------------------------------------------------------------------ |
| `8976824a` | Open this Task ledger and its execution index row                  |
| `7a88efc1` | Record the out-of-scope ignored-scratch deletion as a memory note  |
| `55809319` | Tier A refresh; only `memory-hierarchy.md` required correction     |
| `bc16b198` | Infrastructure and foundation leaves                               |
| `7a5eb5cd` | SDLC and documentation leaves                                      |
| `22b06ba1` | Delivery and quality leaves                                        |
| `acd46f28` | Fix round 1/5 for the reviewed prose-count finding                 |
| `7d304cd7` | Pack index reconciliation, ledger closure, memory handoff          |
| `3f433e68` | Final-review fix wave: outcome summary and Task status coupling    |
| closing    | This inventory's own completion; a commit cannot name its own hash |

### Commit logical unit

Realized logical units are four leaf-content commits, a ledger-open commit, a
memory-note commit, two review-fix commits, an integration commit, and this
closing commit. Clusters A1 and A2 produced no commit because all six of their
leaves survived re-verification unchanged, which the authoring contract treats
as a valid outcome rather than a reason to manufacture edits.

### Commit validation

Each cluster commit is validated by changed-path metadata validation. The
integration, fix-wave, and closing commits are validated by the full repository
contract check, which returns zero failures in an interpreter that supplies
`html5lib`.

## Deferred and Blocked Items

### Deferred items

- Regeneration of LLM Wiki output and `llms.txt` remains deferred to its
  generator-owning unit.
- All-files controlled pre-commit remains deferred to the approved final QA gate.
- The `html5lib` validation-runtime dependency gap is pre-existing and remains
  unowned by this unit. This Task observed `failures=0` only in an isolated
  interpreter that supplies the module.
- Live revalidation of `iso.org` ISO/IEC/IEEE identifiers remains deferred; the
  host refused automated retrieval with HTTP 403.
- Cell-by-cell re-derivation of the Compose port and volume figures cited in
  `security-governance.md` is routed to a future infrastructure-focused unit.
- Three advisory input files cited by SHA-256 in the rebuild Task are
  permanently unrecoverable after the Step 1a deletion. Reconciling those
  dangling citations belongs to the rebuild Task's owner, not to this unit.

### Blocked items

- Deletion of the retiring `2026-07-05-agentic-research-pack-refresh/` pack
  remains blocked and owned by Task 11; its gate stays closed by this Task.

### Deferral destination

`docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0001-rebuild.md` retains
Task 10b, Task 11, and Task 12 ownership.

## Related Documents

- [Spec 137](../spec.md)
- [Rebuild Task](./tsk-0001-rebuild.md)
- [Execution task index](../../README.md)
- [Canonical research pack](../../../90.references/research/2026-08-08-agentic-engineering-research-pack/README.md)
- [Research category router](../../../90.references/research/README.md)
- [Canonical Task template](../../../99.templates/templates/sdlc/task.template.md)

## Objective

Complete the approved work and evidence outcome described in the preserved Task record above.
