---
title: "Research Packages"
version: "1.1.0"
type: "reference/category-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "references"
created: "2026-07-02"
---

# Research Packages

## Overview

External evidence and source-backed analysis. Research packages inform current
owners without replacing them.

The Stage 90 authority boundary and package lifecycle rules are defined by the
[References index](../README.md) and Stage 99 Registry.

## Packages

| Stable ID | Package | Status |
| :--- | :--- | :--- |
| RES-0001 | Agentic Engineering Research Pack | superseded, retiring — pre-deletion gate 4 admits no clickable link to it |
| [RES-0002](./0002-agentic-engineering-research-pack/README.md) | Agentic Engineering Research Pack | active |
| [RES-0080](../../98.archive/superseded/90.references/research/0080-roadmap-v1/README.md) | Reference: CS, CE & SE Self-Learning Roadmap (v1) | superseded |
| [RES-0081](./0081-roadmap/README.md) | Reference: CS, CE & SE Self-Learning Roadmap (v2) | active |
| [RES-0084](./0084-github-actions-platform/README.md) | Reference: GitHub Actions Platform Mechanics | active |
| [RES-0085](./0085-workspace-engineering-main-baseline-assessment/README.md) | Workspace Engineering Main Baseline Assessment | draft |

### Workspace Engineering Request Route

#### Re-review Baseline

The workspace-engineering request is assessed against
`buenhyden/hy-home.docker` at
`main@4c6d211129615eab372d720ebd209b6c27618c86`, observed on
2026-09-05.

RES-0085 owns the repository-local baseline assessment and its binding request
evidence. Its topical research inputs remain owned by RES-0002, RES-0084, and
the current implementation audits; RES-0085 does not duplicate or replace
those owners. Repository-specific implementation truth remains in Stage 00
policies, provider adapters, Stage 03 contracts, Stage 05 operations, tracked
runtime files, scripts, tests, and CI definitions.

#### Design Decisions

1. **Reuse canonical research.** Extend or correct the existing owner instead
   of copying the same subject into a second research pack.
2. **Separate evidence depth.** Distinguish external capability, tracked
   configuration, local execution, repository enforcement, provider runtime
   acceptance, and remote control-plane proof.
3. **Keep one provider-neutral control plane.** Stage 00 owns shared policy;
   `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/`, and `.codex/` remain
   entrypoints or runtime projections.
4. **Route implementation through the SDLC.** A research gap becomes a
   repository change only through an approved Requirement, Architecture/ADR,
   Spec, Plan, Task, verification evidence, and independent review.
5. **Do not infer runtime state.** Tracked Docker Compose, hook, model, or CI
   configuration proves adoption depth only to the level actually observed.

#### Category Routing and Current Assessment

| Requested area | Research owner | Implementation evidence | Assessment |
| --- | --- | --- | --- |
| Harness engineering | [Harness engineering](./0002-agentic-engineering-research-pack/m0008-harness-engineering.md) | [Harness audit](../audits/0025-harness-engineering-implementation/README.md) | Partial |
| Loop engineering | [Loop engineering](./0002-agentic-engineering-research-pack/m0010-loop-engineering.md) | [Loop audit](../audits/0027-loop-engineering-implementation/README.md) | Partial |
| Workspace harness, loop, rules, and environment | [Workspace baseline](./0002-agentic-engineering-research-pack/m0020-workspace-baseline.md) | [Workspace rules audit](../audits/0032-workspace-rules-environment-implementation/README.md) | Partial |
| Claude Code and Codex implementation | [Provider comparison](./0002-agentic-engineering-research-pack/m0012-provider-implementation-comparison.md) | [Provider audit](../audits/0028-provider-harness-loop-implementation/README.md) | Partial |
| Shared Claude/Codex governance | [Provider comparison](./0002-agentic-engineering-research-pack/m0012-provider-implementation-comparison.md) | [Stage 00](../../00.agent-governance/README.md) and [provider registry](../../00.agent-governance/providers/registry.yaml) | Repository-enforced projection; cross-provider acceptance remains point-in-time |
| System prompts and context loading | [Agent instructions](./0002-agentic-engineering-research-pack/m0001-agent-instructions-vibe-coding.md) | [Bootstrap policy](../../00.agent-governance/policies/bootstrap.md), [AGENTS.md](../../../AGENTS.md), and [CLAUDE.md](../../../CLAUDE.md) | Implemented |
| Spec-driven development | [Spec-driven SDLC](./0002-agentic-engineering-research-pack/m0018-spec-driven-sdlc.md) | [Stage 03](../../03.specs/README.md) and [SDLC audit](../audits/0029-sdlc-document-contracts-implementation/README.md) | Repository-enforced for registered forms; intended-use acceptance remains owner-bound |
| PRD, SPEC, PLAN, TASK, and ADR | [SDLC document roles](./0002-agentic-engineering-research-pack/m0016-sdlc-document-roles.md) | [Stage 99 templates](../../99.templates/README.md) | Implemented for registered repository forms |
| SDLC purpose, governance, and lifecycle | [Spec-driven SDLC](./0002-agentic-engineering-research-pack/m0018-spec-driven-sdlc.md) | [SDLC policy](../../00.agent-governance/sdlc.md) and [workflows](../../00.agent-governance/policies/workflows.md) | Implemented |
| Guide, Incident, Postmortem, Policy, Release, and Runbook | [SDLC document roles](./0002-agentic-engineering-research-pack/m0016-sdlc-document-roles.md) | [Operations](../../05.operations/README.md) and [SDLC audit](../audits/0029-sdlc-document-contracts-implementation/README.md) | Guide/Policy/Runbook/Incident/Postmortem registered; Release is composed evidence, not a profile |
| Diátaxis and documentation architecture | [Documentation architecture](./0002-agentic-engineering-research-pack/m0007-documentation-architecture.md) | [Documentation protocol](../../00.agent-governance/policies/documentation-protocol.md) | Partial |
| C4 Model and arc42 | [Documentation architecture](./0002-agentic-engineering-research-pack/m0007-documentation-architecture.md) | [Architecture stage](../../02.architecture/README.md) | Partial |
| ADR | [SDLC document roles](./0002-agentic-engineering-research-pack/m0016-sdlc-document-roles.md) | [Architecture decisions](../../02.architecture/decisions/README.md) | Implemented |
| LLM Wiki | [LLM Wiki system](./0002-agentic-engineering-research-pack/m0009-llm-wiki-system.md) | [Generated index](../data/0082-llm-wiki-index/README.md) and [generator](../../../scripts/knowledge/generate-llm-wiki.py) | Implemented |
| Docker Compose and infrastructure | [Docker Compose and infrastructure](./0002-agentic-engineering-research-pack/m0005-docker-compose-infrastructure.md) | [Compose readiness audit](../audits/0022-compose-infrastructure-operations-readiness/README.md) | Partial; static evidence exceeds runtime evidence |
| CI/CD | [Automation pipeline](./0002-agentic-engineering-research-pack/m0004-automation-pipeline-workflow.md) | [Quality audit](../audits/0030-sdlc-quality-formatting-implementation/README.md) | Partial; CI is stronger than CD |
| GitHub Actions | [GitHub Actions platform](./0084-github-actions-platform/README.md) | [CI workflow](../../../.github/workflows/ci-quality.yml) and [protection record](../../../.github/rulesets/main-protection.md) | Hosted aggregate jobs and 2026-09-05 remote check read-back verified |
| QA, formatting, linting, testing, and syntax | [Quality, CI, and formatting](./0002-agentic-engineering-research-pack/m0014-quality-ci-formatting.md) | [Quality audit](../audits/0030-sdlc-quality-formatting-implementation/README.md) | Implemented across registered surfaces |
| Security | [Security governance](./0002-agentic-engineering-research-pack/m0017-security-governance.md) | [Security audit](../audits/0031-security-framework-maturity/README.md) | Partial |
| Verification and Validation | [Verification and validation](./0002-agentic-engineering-research-pack/m0019-verification-validation.md) | Current Task evidence and registered gates | Partial; intended-use acceptance remains owner-bound |
| AI agent catalog and agency-agents | [AI agent catalogs](./0002-agentic-engineering-research-pack/m0003-ai-agent-catalogs.md) | [Instruction/catalog/model audit](../audits/0020-agent-instructions-catalog-vibe-models/README.md) | Partial |
| Task-aware model selection | [Agent model selection](./0002-agentic-engineering-research-pack/m0002-agent-model-selection.md) | [Provider registry](../../00.agent-governance/providers/registry.yaml) | Implemented as tracked policy; entitlement unverified |
| Agent memory hierarchy | [Memory hierarchy](./0002-agentic-engineering-research-pack/m0011-memory-hierarchy.md) | Stage 00 memory and Task evidence surfaces | Partial |
| Git pre-commit hooks | [Quality, CI, and formatting](./0002-agentic-engineering-research-pack/m0014-quality-ci-formatting.md) | [.pre-commit-config.yaml](../../../.pre-commit-config.yaml) | Implemented |
| Editor shortcuts and code actions | [Workspace baseline](./0002-agentic-engineering-research-pack/m0020-workspace-baseline.md) | No registered repository-wide editor action contract | Missing |
| Rate limits, cost, tokens, and context | [Provider model landscape](./0002-agentic-engineering-research-pack/m0013-provider-model-landscape.md) | Provider registry and bounded context-loading rules | Configured; entitlement observations are point-in-time and cost remains unmeasured |
| Test and CI agent hooks | [Automation pipeline](./0002-agentic-engineering-research-pack/m0004-automation-pipeline-workflow.md) | Claude/Codex hooks and CI definitions | Partial |
| Claude/Codex context sharing | [Provider comparison](./0002-agentic-engineering-research-pack/m0012-provider-implementation-comparison.md) | Stage 00 canonical sources and generated provider projections | Implemented structurally; live handoff remains partial |
| README purpose and role | [Documentation architecture](./0002-agentic-engineering-research-pack/m0007-documentation-architecture.md) | [Repository README](../../../README.md) and registered README profiles | Implemented |

#### Prioritized Design Gaps

1. Add native provider acceptance tests without reading user-global settings or
   assuming account entitlement.
2. Define a tracked, provider-neutral cost and rate-limit evidence contract
   before introducing hard budgets.
3. Complete durable memory promotion, retention, expiry, privacy, and deletion
   rules.
4. Register editor tasks and code actions only after their command, permission,
   and documentation-hook boundaries are specified.
5. Separate deployment promotion, Release evidence, rollback automation, and
   runtime acceptance from the existing CI quality plane.
6. Apply C4 and arc42 selectively through the Architecture stage rather than
   creating a competing documentation hierarchy.

The clean `main` baseline passed
`python3 scripts/validation/run-ci-gate.py --profile full` on 2026-09-05. This
is local-execution and repository-enforcement evidence; it is not deployment or
runtime acceptance.

Each item requires a separately approved active Spec when implementation is
requested. This index records routing and design only; it does not authorize
runtime, remote, provider, secret, or infrastructure mutation.

## Authoring

Create packages only under `research/####-<slug>/` and use the matching Stage 99
template. Preserve observation dates, citations, provenance, and active-owner
Traceability.

Before allocating a new research identity, search active packages and audits.
Extend an existing owner when the question, evidence model, and lifecycle are
already covered.

## Related Documents

- [References index](../README.md)
- [Agentic engineering research](./0002-agentic-engineering-research-pack/README.md)
- [GitHub Actions platform mechanics](./0084-github-actions-platform/README.md)
- [Implementation overview](../audits/0026-implementation-overview/README.md)
- [Stage 00 governance](../../00.agent-governance/README.md)
- [Stage 99 Registry](../../99.templates/registry.json)
