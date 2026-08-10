---
status: draft
artifact_id: task:2026-08-11-agentic-research-pack-source-refresh
artifact_type: task
parent_ids:
  - spec:137-agentic-research-pack-rebuild
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
- Active Spec authority: `docs/03.specs/137-agentic-research-pack-rebuild/spec.md`.
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
- `docs/04.execution/tasks/2026-08-11-agentic-research-pack-source-refresh.md`
- `docs/04.execution/tasks/README.md` (task index row)
- `docs/00.agent-governance/memory/current.md` (bounded handoff refresh)

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

The user approved the refresh design in session on 2026-08-11 with the explicit
reply `승인한다`, after selecting: refresh over rebuild; volatility-prioritized
leaf scope; a new Task as the only governance artifact; and a two-tier,
domain-clustered subagent decomposition.

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
- Step 1 (`Done`): This Task ledger created at BASE `0b9bd01b`.
- Step 2 (`Not Run`): Cluster A1 refresh.
- Step 3 (`Not Run`): Cluster A2 refresh.
- Step 4 (`Not Run`): Cluster A3 refresh.
- Step 5 (`Not Run`): Cluster B1 refresh.
- Step 6 (`Not Run`): Cluster B2 refresh.
- Step 7 (`Not Run`): Cluster B3 refresh.
- Step 8 (`Not Run`): Index reconciliation, ledger closure, memory handoff.

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

`Not Run`.

### Verification results

`Not Run`.

## Controlled Agent Pre-commit Evidence

### Controlled wrapper command

`scripts/validation/run-agent-precommit-all-files.sh` is the only permitted
all-files pre-commit entry point and is reserved for an approved final QA gate.

### Controlled wrapper allowed prefixes

`docs/90.references/research/2026-08-08-agentic-engineering-research-pack/`,
`docs/90.references/research/README.md`, `docs/04.execution/tasks/`,
`docs/00.agent-governance/memory/current.md`.

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

`Not Run`.

### Specification review verdict

`Not Run`.

### Quality review verdict

`Not Run`.

### Review findings and disposition

`Not Run`.

## Commit Ledger

### Commit identity

`Not Run`.

### Commit logical unit

Planned logical units are one commit per cluster (six) plus one integration
commit that reconciles the index, closes this ledger, and refreshes the bounded
memory handoff.

### Commit validation

Each cluster commit is validated by changed-path metadata validation. The
integration commit is validated by the full repository contract check.

## Deferred and Blocked Items

### Deferred items

- Regeneration of LLM Wiki output and `llms.txt` remains deferred to its
  generator-owning unit.
- All-files controlled pre-commit remains deferred to the approved final QA gate.

### Blocked items

- Deletion of the retiring `2026-07-05-agentic-research-pack-refresh/` pack
  remains blocked and owned by Task 11; its gate stays closed by this Task.

### Deferral destination

`docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md` retains
Task 10b, Task 11, and Task 12 ownership.

## Related Documents

- [Spec 137](../../03.specs/137-agentic-research-pack-rebuild/spec.md)
- [Rebuild Task](./2026-08-08-agentic-research-pack-rebuild.md)
- [Execution task index](./README.md)
- [Canonical research pack](../../90.references/research/2026-08-08-agentic-engineering-research-pack/README.md)
- [Research category router](../../90.references/research/README.md)
- [Canonical Task template](../../99.templates/templates/sdlc/task.template.md)
