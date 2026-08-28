---
status: draft
artifact_id: reference:agentic-engineering-research-draft:ai-agent-catalogs
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# AI Agent Catalogs

## Overview

External agent catalogs are candidate inputs, not local roles. This leaf uses a
pinned Agency source to show how an upstream persona can be inspected and
projected without granting it repository authority or permissions.

## Purpose

Provide a safe intake analysis: audit a pinned source and license, extract a
job, map it to a canonical role/skill and permission profile, project native
syntax, then review before any adoption.

## Scope

The retained analysis covers the Agency pin and its Codex converter mechanics.
It does not install agents, run the converter, write `~/.codex/agents`, or
assert that upstream prose is suitable for this repository.

## Definitions / Facts

| Claim ID | Claim | Evidence class | State | Workspace target | Implication |
| --- | --- | --- | --- | --- | --- |
| `AAC-001` | Agency is retained at pin `ebe9c99acb5c96f9468de368d8bead775387d1a7` under MIT; pinning supports repeatable audit but does not establish fitness. | retained fixed source | HISTORICAL VERIFIED | intake boundary only | Audit content and license before extraction. |
| `AAC-002` | The retained 2026-08-14 converter observation maps source Markdown `name`, `description`, and body to TOML `name`, `description`, and `developer_instructions`; it discards `color`, `emoji`, and `vibe`. | retained fixed source | HISTORICAL VERIFIED | native projection analysis | Persona metadata is not a permission grant. |
| `AAC-003` | The upstream installer targets global `~/.codex/agents/`; it was not executed or approved for this draft. | retained fixed source | HISTORICAL VERIFIED | protected user-global destination | Do not run a catalog installer as intake. |
| `AAC-004` | Canonical roles remain the files under `docs/00.agent-governance/roles`; an external catalog cannot create a local role merely by supplying prose. | tracked governance | VERIFIED | `docs/00.agent-governance/roles/` | Map a job to an owner before considering projection. |

### Converter and intake mechanics

The converter's retained mechanics are intentionally narrow: it retains the
agent name, description, and Markdown body, putting the body verbatim into
`developer_instructions`. It does not translate visual/persona fields. The
older statement that it discarded `name` or `description` is erroneous and is
not used here. The global installer destination is an operational boundary,
not an approved installation instruction.

The proposed intake path is: pinned-source/license audit → extract the job →
map it to a canonical role, skill, and permission/profile → produce a native
projection → independent review. A persuasive persona does not create tool,
path, credential, or deployment entitlement. Any adopted instruction must
still be checked against the canonical role and its scoped permission profile.

## Sources

| Source ID | Claim IDs | Title / publisher | URL or path | Class | Revision / observed | Accessed at | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `AAC-SRC-001` | `AAC-001` | Agency agents / msitarzewski | [pinned repository](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7) | retained fixed source | `ebe9c99acb5c96f9468de368d8bead775387d1a7`, MIT | 2026-08-08 | Pin/license do not establish quality or local authority. |
| `AAC-SRC-002` | `AAC-002` | Codex converter description / Agency agents | [pinned Codex integration](https://raw.githubusercontent.com/msitarzewski/agency-agents/ebe9c99acb5c96f9468de368d8bead775387d1a7/integrations/codex/README.md) | retained fixed source | pinned tree | 2026-08-14T13:40:00+09:00 | Retained converter description; no script was run. |
| `AAC-SRC-003` | `AAC-003` | Codex installer description / Agency agents | [pinned Codex integration](https://raw.githubusercontent.com/msitarzewski/agency-agents/ebe9c99acb5c96f9468de368d8bead775387d1a7/integrations/codex/README.md) | retained fixed source | pinned tree | 2026-08-14T13:40:00+09:00 | Retained installer destination; no installation was run. |
| `AAC-SRC-004` | `AAC-004` | Canonical roles / workspace | [roles](../../../00.agent-governance/roles/) | tracked governance | `4481e73d433f6738e0e09b9e94977d4a2ac127cf` | 2026-08-28 | Role documents, not catalog prose, own local responsibilities. |

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | `workflow-supervisor` maps an extracted job to a canonical role/skill/profile. | Compare against `roles/` and `registry.yaml`. | No projection created. |
| architecture | applies | Architecture owner reviews a catalog-derived responsibility split. | Inspect approved design evidence. | No role architecture changed. |
| common | applies | `code-reviewer` examines instructions for scope and hidden authority. | Review exact pinned body. | Pin does not make text safe. |
| docs | applies | `doc-writer` preserves provenance and license boundaries. | Check source pin and README aggregation. | No external catalog becomes canonical docs. |
| infra | applies | `infra-implementer` assesses user-global install location and filesystem permissions before any projection rollout. | Review an approved concrete target plan. | `~/.codex/agents` was untouched. |
| ops | applies | `ci-cd-engineer` owns a rollout/rollback runbook for any projected agent distribution. | Inspect approved rollout evidence. | No agent was activated. |
| qa | applies | `qa-engineer` defines acceptance cases for a proposed projection. | Inspect evaluation before adoption. | No projection evaluated. |
| security | applies | `security-auditor` reviews projected permissions and supply-chain pin. | Review license/pin and permission mapping. | Persona text grants no permissions. |

## Maintenance

Re-audit only a newly proposed pin and license before a new intake. Do not
reopen or install the upstream catalog merely to refresh this advisory leaf.

## Related Documents

- [Research pack README](./README.md)
- [Agent instructions and bounded generated work](./agent-instructions-vibe-coding.md)
- [Harness engineering](./harness-engineering.md)
