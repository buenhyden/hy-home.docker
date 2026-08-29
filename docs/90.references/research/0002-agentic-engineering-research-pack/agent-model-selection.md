---
status: active
artifact_id: reference:agentic-engineering-research:agent-model-selection
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# Agent Model Selection

## Overview

Selection is static routing, not a dynamic router: work type routes to a
canonical role, then a registered work profile, provider eligibility,
comparative evaluation, and only then an approved promotion.

## Purpose

Explain which local declarations participate in selection and which important
facts remain unmeasured, so a model label cannot be mistaken for authority.

## Scope

This leaf covers the five tracked work profiles and the native/provider
boundary. It excludes a runtime model-resolution observation, user settings,
cost budgets, and automatic fallback adoption.

## Definitions / Facts

| Claim ID | Claim | Evidence class | State | Workspace target | Implication |
| --- | --- | --- | --- | --- | --- |
| `AMS-001` | `registry.yaml` declares five static work profiles, each with a Claude and Codex model/control pair. | tracked configuration | VERIFIED | `docs/00.agent-governance/providers/registry.yaml` | Route through the declared profile, not an ad-hoc model choice. |
| `AMS-002` | The selection sequence is work type → role → profile → provider eligibility → comparative evaluation → approved promotion. | advisory synthesis grounded in configuration | ADVISORY | `registry.yaml` work profiles and model policy | Treat promotion as a governed change, not routing at request time. |
| `AMS-003` | Retained Claude subagent documentation gives model precedence to an environment override, invocation parameter, agent definition, then conversation model; this does not prove any local override exists. | retained official observation | HISTORICAL VERIFIED | generated-provider boundary | Runtime resolution remains unobserved. |
| `AMS-004` | The registry has no automatic fallback graph, and provider-native substitution must not be claimed as a repository fallback. | tracked configuration plus retained observation | VERIFIED | `registry.yaml` model catalog policy | Stop and revalidate rather than silently substitute. |

### Selection criteria and evaluation

The profile names encode task characteristics, not a live classifier.
`routine-validation` is appropriate only where deterministic evidence decides
completion; `evidence-research` emphasizes source-calibrated synthesis;
`complex-implementation` requires scoped mutation authority; and
`adversarial-review` is a separate challenge role. These are adoption options
based on registry declarations, not assertions that one provider model is
superior to another.

The declared pairs are concrete but static: adversarial review uses Opus/high
or Sol/xhigh; complex implementation Sonnet/high or Sol/high; evidence
research Sonnet/low or Terra/medium; long-horizon supervision Opus/xhigh or
Sol/xhigh; and routine validation Haiku/no Claude effort value or Terra/low.
Each is read from the five registry profiles, so it does not establish provider
entitlement, actual model resolution, or a cross-provider quality ranking.

A proposed promotion needs a frozen representative task set, a baseline,
explicit rubric and threshold, failure cases, permitted latency/cost evidence,
reviewer calibration, and rollback. The local configuration alone cannot show
effective runtime selection because native precedence and account constraints
can intervene. The retained native observation supports that distinction; it
does not evidence that an environment override was set here.

## Sources

| Source ID | Claim IDs | Title / publisher | URL or path | Class | Revision / observed | Accessed at | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `AMS-SRC-001` | `AMS-001`, `AMS-004` | Provider registry / workspace | [registry](../../../00.agent-governance/providers/registry.yaml) | tracked configuration | `4481e73d433f6738e0e09b9e94977d4a2ac127cf` | 2026-08-28 | Declared pairs and absent fallback graph do not prove runtime behavior. |
| `AMS-SRC-002` | `AMS-003` | Subagents / Anthropic | [official page](https://code.claude.com/docs/en/sub-agents) | retained official observation | detailed dated leaf; version not recorded | 2026-08-14T13:40:00+09:00 | Documents native precedence, not this workspace's effective value. |
| `AMS-SRC-003` | `AMS-002` | Provider model landscape / workspace | [provider model landscape](./provider-model-landscape.md) | advisory synthesis | D3 draft | 2026-08-28 | Comparative evaluation is proposed, not performed. |

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | `workflow-supervisor` resolves role/profile from `registry.yaml`. | Check the named profile pair. | Native runtime precedence remains unobserved. |
| architecture | applies | Architecture owner approves changed routing semantics. | Inspect an approved change record. | No routing change is proposed. |
| common | applies | `code-reviewer` confirms implementer/reviewer separation. | Review role and profile mapping. | Role mapping is static only. |
| docs | applies | `doc-writer` records source-backed selection boundaries. | Reconcile README IDs. | This is advisory documentation. |
| infra | applies | `infra-implementer` assesses endpoint compatibility/capacity for a concrete deployment target. | Review a target-specific approval record. | No provider endpoint invoked. |
| ops | applies | `incident-responder` owns any availability or fallback policy for operations. | Inspect an approved runbook or incident record. | No fallback graph exists. |
| qa | applies | `qa-engineer` owns the comparative-evaluation proposal. | Inspect frozen task/rubric before promotion. | No evaluation executed. |
| security | applies | `security-auditor` assesses sensitivity and entitlement evidence. | Review sanitized approval evidence. | No account/organization state read. |

## Maintenance

Revisit when role profiles, native precedence documentation, or evaluation
requirements change. Do not infer a runtime default from an absent tracked key.

## Related Documents

- [Research pack README](./README.md)
- [Provider model landscape](./provider-model-landscape.md)
- [Harness engineering](./harness-engineering.md)
