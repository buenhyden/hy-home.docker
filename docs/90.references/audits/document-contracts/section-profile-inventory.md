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
| SP-001 | `git ls-files '*.md'` plus a line-based Python heading scan using `^(#{1,6})\s+(.+?)\s*$` and the surface groups named below | Count Markdown headings by derived surface and print the 25 most common headings per surface with examples. |

The rerun grouped root `*.md` files as `root`; `.agents`, `.claude`, and
`.codex` as `provider`; `.github/**` as `github`; known stage folders under
`docs/` by stage; `docs/README.md` as `docs/other`; and top-level
`infra`, `projects`, `scripts`, `secrets`, `tests`, `examples`, `archive`,
and `graphify-out` paths by their directory name. No unclassified `other`
surface was present.

## Findings

| Surface | Measurement | Representative Paths | Disposition |
| --- | --- | --- | --- |
| `root` | 6 tracked Markdown files, 47 headings; `Related Documents` appears 4 times and provider quick-reference headings appear twice each | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `README.md` | no-action |
| `github` | 3 tracked Markdown files, 23 headings; PR template, security policy, and ruleset proposal headings each appear once | `.github/PULL_REQUEST_TEMPLATE.md`, `.github/SECURITY.md`, `.github/rulesets/main-protection.md` | no-action |
| `provider` | 102 tracked Markdown files, 888 headings; `Related Documents` appears 46 times, `Error Handling` 19 times, `Purpose` 18 times, and skill bootstrap headings 16 times | `.agents/README.md`, `.claude/CLAUDE.md`, `.claude/agents/code-reviewer.md`, `.claude/skills/compose-stack-agent/skill.md` | no-action |
| `docs/other` | 1 tracked Markdown file, 18 headings; root docs routing headings each appear once | `docs/README.md` | no-action |
| `docs/00.agent-governance` | `Related Documents` appears 105 times; `Overview`, `Scope`, and `Structure` each appear 33 times | `docs/00.agent-governance/README.md`, `docs/00.agent-governance/agents/README.md` | no-action |
| `docs/01.requirements` | PRD sections repeat across 24 to 25 files, including `Vision`, `Problem Statement`, `Functional Requirements`, and `Success Criteria` | `docs/01.requirements/2026-03-26-01-gateway.md`, `docs/01.requirements/2026-03-26-02-auth.md` | historical-evidence |
| `docs/02.architecture` | Architecture profiles show 51 `Overview` and 51 `Related Documents` headings, plus ADR and ARD-specific section clusters | `docs/02.architecture/decisions/0001-traefik-nginx-hybrid.md`, `docs/02.architecture/requirements/0001-gateway-architecture.md` | no-action |
| `docs/03.specs` | Spec profile sections appear 24 to 26 times, including `Contracts`, `Core Design`, `Verification`, and `Success Criteria & Verification Plan` | `docs/03.specs/01-gateway/spec.md`, `docs/03.specs/02-auth/spec.md` | no-action |
| `docs/04.execution` | Execution documents show 156 `Overview`, 156 `Related Documents`, 88 `Task Table`, 88 `Verification Summary`, and 64 plan-section repeats | `docs/04.execution/plans/2026-03-26-01-gateway-standardization.md`, `docs/04.execution/tasks/2026-03-26-01-gateway-tasks.md` | no-action |
| `docs/05.operations` | Operations docs show 267 `Related Documents`, 273 `Overview` headings across all levels, 67 `Usage`, 67 `Common Checks`, 73 README profile repeats, and 130 nested `Purpose` headings | `docs/05.operations/README.md`, `docs/05.operations/guides/00-workspace/developer-setup.md` | no-action |
| `docs/90.references` | Reference surfaces now show 29 `Overview`, 29 `Scope`, 29 `Related Documents`, 26 `In Scope`, and 26 `Out of Scope` headings after the Task 2 inventory reports are tracked | `docs/90.references/README.md`, `docs/90.references/audits/README.md`, `docs/90.references/audits/document-contracts/frontmatter-inventory.md` | no-action |
| `docs/98.archive` | Archive tombstones show 20 `Archive Metadata`, 20 `Current Replacement`, and 20 `Archive Ledger` headings | `docs/98.archive/04.execution/plans/2026-05-30-ai-governance-reorg.md`, `docs/98.archive/04.execution/tasks/2026-05-30-standardizing-agent-governance.md` | historical-evidence |
| `docs/99.templates` | 36 tracked Markdown files, 390 headings; `Related Documents` appears 36 times, `Overview` 33 times, and template category headings such as `Templates` and `Target Rules` 6 times each | `docs/99.templates/README.md`, `docs/99.templates/support/README.md`, `docs/99.templates/templates/common/readme.template.md` | no-action |
| `infra` | 68 tracked Markdown files, 1055 headings; `Related Documents` appears 70 times, and `Audience`, `Scope`, `Structure`, and `How to Work in This Area` each appear 68 times | `infra/01-gateway/README.md`, `infra/01-gateway/nginx/README.md` | no-action |
| `projects` | 3 tracked Markdown files, 29 headings; README profile headings appear 3 times, and `Related References` appears 3 times | `projects/README.md`, `projects/storybook/README.md`, `projects/storybook/nextjs/README.md` | batch-fix |
| `scripts` | 1 tracked Markdown file, 44 headings; README profile and script-catalog headings each appear once | `scripts/README.md` | no-action |
| `secrets` | 1 tracked Markdown file, 18 headings; README profile, inventory, registry, automation, and security-policy headings each appear once | `secrets/README.md` | no-action |
| `tests` | 1 tracked Markdown file, 9 headings; README profile headings and `Related References` each appear once | `tests/README.md` | batch-fix |
| `examples` | 2 tracked Markdown files, 18 headings; `Validation` and `Related Documents` each appear twice across the sample README and service scaffold | `examples/sample-web-service/README.md`, `examples/sample-web-service/service.md` | out-of-scope-gap |
| `archive` | 1 tracked Markdown file, 1 heading | `archive/Windows-Network-IP.md` | historical-evidence |
| `graphify-out` | 3 tracked Markdown files, 3128 headings; generated report headings such as `Corpus Check`, `Summary`, `Graph Freshness`, and graph community headings repeat across the three reports | `graphify-out/GRAPH_REPORT.md`, `graphify-out/2026-06-04/GRAPH_REPORT.md`, `graphify-out/2026-06-05/GRAPH_REPORT.md` | no-action |

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
