---
status: draft
artifact_id: reference:agentic-engineering-research-draft:provider-model-landscape
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# Provider Model Landscape

## Overview

This leaf separates a provider's documented model/configuration surface from
the small, tracked routing surface. It is retained research and configuration
analysis, not proof that an account can select a model or that a runtime did.

## Purpose

Make model-selection evidence auditable: a provider capability is an input to
an intake decision, while registry eligibility, entitlement, and runtime
acceptance remain independent gates.

## Scope

The analysis covers the tracked Claude and Codex rows and the native controls
recorded in retained primary-source observations. It excludes prices, live
catalogue currency, account state, and any provider-default or fallback claim.

## Definitions / Facts

| Claim ID | Claim | Evidence class | State | Workspace target | Implication |
| --- | --- | --- | --- | --- | --- |
| `PML-001` | The registry has five work profiles and five active model rows: three Claude and two Codex; every row records `needs_revalidation` for entitlement and runtime acceptance. | tracked configuration | VERIFIED | `docs/00.agent-governance/providers/registry.yaml` | A configured row is not executable entitlement. |
| `PML-002` | Claude's retained 2026-08-14 model-configuration observation distinguishes native `effort` from a product orchestration mode; it should not be projected into another provider's control vocabulary. | retained official observation | HISTORICAL VERIFIED | Claude rows in `registry.yaml` | Preserve native control names in any comparison. |
| `PML-003` | The retained 2026-08-14 Codex configuration observation lists `model_reasoning_effort` values differently from the registry's historical `supported_values`; the cause is `UNVERIFIED`. | retained official observation plus configuration | UNVERIFIED | Codex rows in `registry.yaml` | Do not add a new reasoning value from either set without revalidation. |
| `PML-004` | Vendor descriptions are task-fit hypotheses, not comparative performance evidence or a local default. | advisory synthesis | ADVISORY | provider source URLs below | Promotion needs a comparative evaluation and approval. |

### Control and eligibility boundary

The local contract maps `effort` to Claude and `model_reasoning_effort` to
Codex. Those fields describe different native schemas. The 2026-08-14 retained
Claude observation says that an unsupported effort request is resolved by that
provider's own compatibility behavior; it does not authorize a local fallback.
The retained Codex configuration page documented `minimal`, `low`, `medium`,
`high`, and model-dependent `xhigh`, while the tracked Codex rows additionally
contain historical `none` and `max`. This mismatch is deliberately
`UNVERIFIED`, rather than evidence of a fallback or a runtime defect.

The registry's model rows must pass three distinct checks before promotion:
official-source revalidation, entitlement revalidation, and runtime
revalidation. A provider catalog can therefore contain a model that this
repository cannot select; conversely, an existing row is not proof that a
particular user, organization, or session can use it.

### Static profile bindings

The five current tracked-only mappings are below. They are declarations, not
public-entitlement assertions: `adversarial-review` maps to Claude
`claude-opus-5` / `effort: high` and Codex `gpt-5.6-sol` /
`model_reasoning_effort: xhigh`; `complex-implementation` maps to
`claude-sonnet-5` / `high` and `gpt-5.6-sol` / `high`; `evidence-research`
maps to `claude-sonnet-5` / `low` and `gpt-5.6-terra` / `medium`;
`long-horizon-supervision` maps to `claude-opus-5` / `xhigh` and
`gpt-5.6-sol` / `xhigh`; and `routine-validation` maps to
`claude-haiku-4-5-20251001` / no native effort value and `gpt-5.6-terra` /
`low`. The final profile is a useful boundary: a null Claude control is not a
request to invent one.

### Evidence-reading rules

The retained provider-catalog analysis supplies three durable reading rules.
An alias or marketing family is not necessarily an exact API identity; a
provider lifecycle label does not establish account availability; and a
catalogue row does not assert a benchmark ranking. These rules avoid turning a
mutable product page into a claim about local execution. They also mean that
the registry's five rows are a curated routing input, not a claim to enumerate
all provider offerings.

## Sources

| Source ID | Claim IDs | Title / publisher | URL or path | Class | Revision / observed | Accessed at | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `PML-SRC-001` | `PML-001`, `PML-003` | Provider registry / workspace | [registry](../../../00.agent-governance/providers/registry.yaml) | tracked configuration | `4481e73d433f6738e0e09b9e94977d4a2ac127cf` | 2026-08-28 | Configuration does not prove execution or entitlement. |
| `PML-SRC-002` | `PML-002` | Model configuration / Anthropic | [official page](https://code.claude.com/docs/en/model-config) | retained official observation | detailed dated leaf; version not recorded | 2026-08-14T13:40:00+09:00 | Native capability only; no local fallback inferred. |
| `PML-SRC-003` | `PML-003` | Configuration reference / OpenAI | [official page](https://learn.chatgpt.com/docs/config-file/config-reference) | retained official observation | detailed dated leaf; version not recorded | 2026-08-14T13:40:00+09:00 | Historical observation conflicts with local supported-value set; cause unknown. |
| `PML-SRC-004` | `PML-004` | Models overview / Anthropic | [official page](https://platform.claude.com/docs/en/about-claude/models/overview) | retained official observation | retrieval-time page | 2026-08-08T16:18:04+09:00 | Mutable vendor description, not a comparative evaluation. |
| `PML-SRC-005` | `PML-004` | Models / OpenAI | [official page](https://learn.chatgpt.com/docs/models) | retained official observation | retrieval-time page | 2026-08-08T16:18:04+09:00 | Mutable vendor description, not local availability evidence. |

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | `eval-engineer` compares `registry.yaml` native control fields before a promotion. | Re-read the five work-profile bindings. | Runtime acceptance is unobserved. |
| architecture | applies | Architecture owner records a decision only if routing semantics change. | Review the approving ADR/Spec path. | No decision is created here. |
| common | applies | `code-reviewer` checks cross-provider terms are not treated as equivalent. | Inspect claim/source rows. | No benchmark comparison exists. |
| docs | applies | `doc-writer` maintains this advisory source mapping. | Reconcile IDs in README. | Links are not provider proof. |
| infra | applies | `infra-implementer` assesses a concrete provider environment's compatibility/capacity before adoption. | Review an approved target-specific record. | No environment was observed. |
| ops | applies | `incident-responder` owns availability/fallback policy evidence for an operational provider use. | Inspect an approved runbook or incident record. | No fallback graph is configured. |
| qa | applies | `qa-engineer` defines representative evaluation before default promotion. | Inspect an approved evaluation record. | No live comparison was run. |
| security | applies | `security-auditor` checks entitlement-sensitive promotion evidence. | Review value-free approval evidence. | Account state was not inspected. |

## Maintenance

Revisit on source, registry, or evaluation-contract change. Revalidation must
record the exact native surface and must not infer an unsupported fallback.

## Related Documents

- [Research pack README](./README.md)
- [Agent model selection](./agent-model-selection.md)
- [Provider implementation comparison](./provider-implementation-comparison.md)
