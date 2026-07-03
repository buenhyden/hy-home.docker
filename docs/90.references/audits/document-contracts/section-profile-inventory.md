---
status: active
---

<!-- Target: docs/90.references/audits/document-contracts/section-profile-inventory.md -->

# Section Profile Inventory

## Overview

This inventory records heading distribution by repository surface. It preserves
the command evidence needed to compare observed section profiles with the
document contract, while leaving all target documents unchanged.

## Scope

In scope: tracked Markdown headings grouped by root, provider, GitHub, docs
stage, infra, project, scripts, secrets, tests, examples, archive, and generated
graph surfaces.

Out of scope: fenced-aware parser changes, section normalization, renaming
headings, or editing historical evidence.

## Method

| Evidence ID | Command | Measured Purpose |
| --- | --- | --- |
| SP-001 | `python3 - <<'PY' ... surface_counts[group][key] += 1 ... print(f"{count}\t{key}\t{', '.join(examples[group][key])}") ... PY` | Count Markdown headings by derived surface and print the 25 most common headings per surface with examples. |

## Findings

| Surface | Measurement | Representative Paths | Disposition |
| --- | --- | --- | --- |
| `docs/00.agent-governance` | `Related Documents` appears 105 times; `Overview`, `Scope`, and `Structure` each appear 33 times | `docs/00.agent-governance/README.md`, `docs/00.agent-governance/agents/README.md` | no-action |
| `docs/01.requirements` | PRD sections repeat across 24 to 25 files, including `Vision`, `Problem Statement`, `Functional Requirements`, and `Success Criteria` | `docs/01.requirements/2026-03-26-01-gateway.md`, `docs/01.requirements/2026-03-26-02-auth.md` | historical-evidence |
| `docs/02.architecture` | Architecture profiles show 51 `Overview` and 51 `Related Documents` headings, plus ADR and ARD-specific section clusters | `docs/02.architecture/decisions/0001-traefik-nginx-hybrid.md`, `docs/02.architecture/requirements/0001-gateway-architecture.md` | no-action |
| `docs/03.specs` | Spec profile sections appear 24 to 26 times, including `Contracts`, `Core Design`, `Verification`, and `Success Criteria & Verification Plan` | `docs/03.specs/01-gateway/spec.md`, `docs/03.specs/02-auth/spec.md` | no-action |
| `docs/04.execution` | Execution documents show 156 `Overview`, 156 `Related Documents`, 88 `Task Table`, 88 `Verification Summary`, and 64 plan-section repeats | `docs/04.execution/plans/2026-03-26-01-gateway-standardization.md`, `docs/04.execution/tasks/2026-03-26-01-gateway-tasks.md` | no-action |
| `docs/05.operations` | Operations docs show 267 `Related Documents`, 174 `Overview`, 67 `Usage`, 67 `Common Checks`, and 73 README profile section repeats | `docs/05.operations/README.md`, `docs/05.operations/guides/00-workspace/developer-setup.md` | no-action |
| `docs/90.references` | Reference surfaces show 26 `Overview`, 26 `Scope`, 26 `In Scope`, 26 `Out of Scope`, and 26 `Related Documents` headings | `docs/90.references/README.md`, `docs/90.references/audits/README.md` | no-action |
| `infra` | Infra README surfaces show 68 `Audience`, 68 `Scope`, 68 `Structure`, 68 `How to Work in This Area`, and 68 `Related Documents` headings | `infra/01-gateway/README.md`, `infra/01-gateway/nginx/README.md` | no-action |
| `provider` | Provider surfaces show 46 `Related Documents`, 19 `Error Handling`, and repeated agent/skill profile sections | `.agents/README.md`, `.claude/agents/code-reviewer.md`, `.claude/skills/compose-stack-agent/skill.md` | no-action |
| `docs/98.archive` | Archive tombstones show 20 `Archive Metadata`, 20 `Current Replacement`, and 20 `Archive Ledger` headings | `docs/98.archive/04.execution/plans/2026-05-30-ai-governance-reorg.md`, `docs/98.archive/04.execution/tasks/2026-05-30-standardizing-agent-governance.md` | historical-evidence |

## Gaps For Register

| Gap Candidate | Evidence | Disposition | Register Handling |
| --- | --- | --- | --- |
| Requirement agent section naming is split | `AI Agent Requirements (If Applicable)` appears 20 times and `AI Agent Requirements` appears 4 times under `docs/01.requirements` | batch-fix | Add to the register as a future naming-normalization batch if requirements profiles require one spelling. |
| Line-based heading scan surfaces fenced or comment-like H1 lines | `.github/PULL_REQUEST_TEMPLATE.md`, `scripts/README.md`, and `secrets/README.md` report H1 entries such as command or instruction lines | out-of-scope-gap | Record as an automation/parser gap for later fenced-aware audit tooling, not a Task 2 content fix. |
| Infra validation terminology has a small split | `Validation` appears 47 times and `Validation Commands` appears 2 times under `infra` | batch-fix | Defer to a later infra README profile decision before any content edits. |
| Operations nested `Overview` and `Purpose` headings are common | `docs/05.operations` reports 98 H3 `Overview` and 123 H3 `Purpose` entries | no-action | Treat as expected nested guide/runbook profile evidence unless a later contract comparison proves otherwise. |

## Related Documents

- [Document contract audit references](./README.md)
- [Workspace document contract audit pack task](../../../04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md)
- [Template selection](../../../99.templates/support/template-selection.md)
- [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Reference template](../../../99.templates/templates/common/reference.template.md)
