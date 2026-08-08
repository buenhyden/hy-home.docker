---
status: active
artifact_id: task:2026-08-08-agentic-research-pack-rebuild
artifact_type: task
parent_ids:
  - plan:2026-08-08-agentic-research-pack-rebuild
---

# Task: Agentic Engineering Research Pack Rebuild

## Overview

This Task is the execution evidence and control ledger for the source-backed
Agentic Engineering Research Pack Rebuild defined by Spec 137 and its active
Plan. It records immutable predecessor objects, requirement and scope coverage,
source verification, claim migration, generated-artifact freshness, old-path
allowlisting, verification, reviews, and logical commits. The ledger reports
observed evidence only; an unperformed activity is `Not Run` and no Stage 90
research statement becomes policy, runtime truth, or remote-enforcement proof.

Task 1 started from branch `codex/agentic-research-rebuild` at immutable BASE
`9917fcdadf700e7f68541e73188620e133485470`. The active Spec 137 input is commit
`353182551d47c4232bceb58e573abd55b846420a`. The stale Graphify report was built
from `f8a72211`; it remains advisory and was corroborated against tracked
governance, the active Spec, the active Plan, and the old pack.

## Inputs

| Input | Immutable or tracked identity | Task 1 state |
| --- | --- | --- |
| Active Spec 137 | `docs/03.specs/137-agentic-research-pack-rebuild/spec.md` at `353182551d47c4232bceb58e573abd55b846420a` | Verified tracked input |
| Active Plan | `docs/04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md` at Task BASE `9917fcdadf700e7f68541e73188620e133485470` | Verified tracked input |
| Old research pack | `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/` at Task BASE | 20 filenames and 20 blobs pinned below |
| Canonical Task template | `docs/99.templates/templates/sdlc/task.template.md` at Task BASE | Applied; all required headings retained |
| Stage 00 governance | `docs/00.agent-governance/` at Task BASE | Corroborated; private and secret boundaries preserved |
| Graphify | `graphify-out/GRAPH_REPORT.md`, built from `f8a72211` | Advisory and stale; not used as current evidence |

### Immutable old-pack file objects

The filename and object inventories were captured before any old-pack change.
Both commands returned exactly 20 records at Task BASE
`9917fcdadf700e7f68541e73188620e133485470`.

| Old file | Blob ID |
| --- | --- |
| `README.md` | `a5c8b67e839ab074c2861caab5ed23366f4cb1b7` |
| `agent-instructions-vibe-coding.md` | `a014383a3585ba8945ccbb583781ba6b45cb982c` |
| `agent-model-selection.md` | `7b82620f75ad74bd515db385c9d0a64133dd4848` |
| `ai-agent-catalogs.md` | `f4c5dbd0c2e4f266df9590a592a204599415fe42` |
| `automation-pipeline-workflow.md` | `69b9ac96be78692b46e523ca3dedf871ee8e3ffb` |
| `docker-compose-infrastructure.md` | `5e70579fde9136d3d1b3f27e7e0d5aeb77b1b9b7` |
| `document-metadata-lifecycle.md` | `8a1212e9715cff80060db5d4c4d48a556d03a096` |
| `documentation-architecture.md` | `a0cf3b22431aae367570bc515821cee8c2cf4a19` |
| `harness-engineering.md` | `6d6cf79e2c724b801d2c66fa85d364acb363c784` |
| `llm-wiki-system.md` | `553dafd5690a521071e900b453748393b2cf74fa` |
| `loop-engineering.md` | `1436c0b22e54f7c3679cc695577c0ae10700cb2a` |
| `memory-hierarchy.md` | `27439218ae394c2df0dd936eb8dbd2bcf9062202` |
| `provider-implementation-comparison.md` | `26e3c6e9d56f4f412de46532a8f98c6fbd6e8b76` |
| `provider-model-landscape.md` | `f51b3d4bbb23490f66de4d8bf2c46d85f5a8f99b` |
| `quality-ci-formatting.md` | `7f4e064dce61f468e0be3cf5002af7bf5a8d80c8` |
| `scope-application-matrix.md` | `ac19e2c93cc2ecf09f3a14b6308553221e637f45` |
| `sdlc-document-roles.md` | `b4aeeffafcfeda3fe1ccdf6637c01ef811c69236` |
| `security-governance.md` | `32af3c515643ea326fbd9db84ce71a57028a4a05` |
| `spec-driven-sdlc.md` | `10b06739620306465bf924a7b5fed2df3dd1e900` |
| `workspace-baseline.md` | `7cda3c192ba8a2577f5d4427a532d75455678853` |

## Goals and Non-goals

Goals:

- Provide the closed execution-control schema required by all twelve Plan
  units before new-pack authoring begins.
- Preserve exact old-pack file provenance and every observed predecessor
  classification without rewriting design-time facts.
- Keep requirement, scope, source, claim, generated-artifact, path, review, and
  commit state auditable through later Task updates.

Non-goals:

- Author, move, rewrite, or delete research-pack content in this unit.
- Refresh generated artifacts, Graphify, runtime configuration, or remote state.
- Inspect secrets, raw logs, shell history, ignored volumes, private provider
  state, or live services.
- Claim requirement, source, claim-migration, scope, or deletion completion
  before its named evidence and independent reviews exist.

## Scope and Change Boundaries

Allowed tracked paths for Task 1 are this Task and
`docs/04.execution/tasks/README.md`. The disposable validation environment at
`/tmp/agentic-research-validation-venv` is outside the repository.

Forbidden tracked paths in Task 1 include the Spec, Plan, old pack, new pack,
generated artifacts, governance memory, scripts, runtime configuration, and
all other repository files. Compose, security, operations, and runtime impact
is none: this unit creates documentation evidence only.

## Approval Evidence

The active Spec 137 and Plan authorize this bounded Stage 04 execution ledger.
They do not authorize remote mutation, secret-value access, runtime or Compose
changes, generated-output refresh, old-pack deletion, or Graphify refresh.
Recovery for the tracked unit is the logical Task 1 commit; the old pack is
independently recoverable from the pinned BASE and blob IDs. Evidence records
only paths, identifiers, commands, exit classifications, and redacted-safe
summaries.

## Work Breakdown

| Unit | Description | Validation / evidence | Status |
| --- | --- | --- | --- |
| Task 1 | Initialize execution ledgers and immutable baselines | Task 1 checks and committed-unit review ledger | Complete after fix `528c225d`; scoped specification and quality re-reviews Approved C0/I0/M0 |
| Task 2 | Author workspace foundation and scope axis | Requirement, scope, source, and leaf gates | Complete at `9a6e09ca`; specification and quality reviews Approved C0/I0/M0 |
| Task 3 | Author harness, loop, and provider comparison | Assigned requirement and claim rows plus leaf gates | Implemented as draft leaves; focused validation and self-review PASS; independent review `Not Run` |
| Task 4 | Author instructions, models, catalogs, and memory | Assigned requirement and claim rows plus leaf gates | Not Run |
| Task 5 | Author spec-driven SDLC and document contracts | Assigned requirement and claim rows plus leaf gates | Not Run |
| Task 6 | Author documentation architecture and LLM Wiki | Assigned requirement and claim rows plus leaf gates | Not Run |
| Task 7 | Author automation, CI/CD, GitHub Actions, and QA | Assigned requirement and claim rows plus leaf gates | Not Run |
| Task 8 | Author Compose, infrastructure, and security | Assigned requirement and claim rows plus leaf gates | Not Run |
| Task 9 | Assemble and review the new pack | 19 leaves, 35 requirements, 14 scopes, sources, claims | Not Run |
| Task 10 | Switch human and machine routes | Literal scan, reviewed allowlist, generators, route checks | Not Run |
| Task 11 | Delete the old pack behind fail-closed gates | Proposed and staged deletion reviews plus recovery evidence | Not Run |
| Task 12 | Final verification and handoff | Whole-branch checks, reviews, closure, and handoff | Not Run |

### Requirement matrix

Every requirement text below is copied verbatim from Spec 137. `Not Run`
states are intentional and may change only with named evidence and review.

| ID | Requirement text | Primary leaf | Supporting leaves | External source state | Workspace evidence owner | Scopes | Implementation status | Review verdict | Canonical link |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-01 | Harness engineering elements and patterns | `harness-engineering.md` | `loop-engineering.md`, provider comparison, workspace baseline, scope matrix | Nine official Claude/Codex pages verified 2026-08-08; tracked claims use direct owners | WS-TASK3-HARNESS | 14/14 explicit in leaf | Implemented as draft Stage 90 leaf; route switch pending | Implementer PASS C0/I0; independent review `Not Run` | [harness engineering](../../90.references/research/2026-08-08-agentic-engineering-research-pack/harness-engineering.md) |
| REQ-02 | Loop engineering elements and feedback systems | `loop-engineering.md` | Harness, provider comparison, workspace baseline, scope matrix | Official hooks/subagent pages verified 2026-08-08; tracked claims use direct owners | WS-TASK3-HARNESS | 14/14 explicit in leaf | Implemented as draft Stage 90 leaf; route switch pending | Implementer PASS C0/I0; independent review `Not Run` | [loop engineering](../../90.references/research/2026-08-08-agentic-engineering-research-pack/loop-engineering.md) |
| REQ-03 | Systems, environment, and rules needed to apply harness and loop engineering to this workspace | `harness-engineering.md` | Loop, provider comparison, workspace baseline, scope matrix | Official settings/instruction/hook pages verified 2026-08-08; tracked rules remain canonical | WS-TASK3-HARNESS | 14/14 explicit in leaf | Implemented as draft Stage 90 leaf; route switch pending | Implementer PASS C0/I0; independent review `Not Run` | [harness engineering](../../90.references/research/2026-08-08-agentic-engineering-research-pack/harness-engineering.md) |
| REQ-04 | Current Claude and Codex harness and loop implementation | `provider-implementation-comparison.md` | Harness, loop, workspace baseline, scope matrix | EXT-CLAUDE-* and EXT-CODEX-* verified from nine direct official pages | WS-TASK3-HARNESS | 14/14 explicit in leaf | Implemented as draft Stage 90 leaf; runtime/provider acceptance explicitly unverified | Implementer PASS C0/I0; independent review `Not Run` | [provider implementation comparison](../../90.references/research/2026-08-08-agentic-engineering-research-pack/provider-implementation-comparison.md) |
| REQ-05 | Common Claude/Codex environment, rules, systems, translations, and irreducible provider-native differences | `provider-implementation-comparison.md` | Harness, loop, workspace baseline, scope matrix | Nine-page direct provider set verified; mutable retrieval-time observations only | WS-TASK3-HARNESS | 14/14 explicit in leaf | Exact Spec 137 construction matrix implemented; route switch pending | Implementer PASS C0/I0; independent review `Not Run` | [provider implementation comparison](../../90.references/research/2026-08-08-agentic-engineering-research-pack/provider-implementation-comparison.md#common-construction-matrix) |
| REQ-06 | Spec-driven development concepts, workflow, traceability, and enforcement | `spec-driven-sdlc.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-07 | Docker Compose concepts, current workspace implementation, and adoption rules | `docker-compose-infrastructure.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-08 | Infrastructure concepts, topology, controls, operations evidence, and adoption rules | `docker-compose-infrastructure.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-09 | SDLC lifecycle, stage gates, feedback, ownership, and evidence | `spec-driven-sdlc.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-10 | PRD role, purpose, trigger, owner, consumer, system, and rules | `sdlc-document-roles.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-11 | ARD role, purpose, trigger, owner, consumer, system, and rules, including its local-coinage boundary | `sdlc-document-roles.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-12 | ADR role, purpose, trigger, owner, consumer, system, and rules | `sdlc-document-roles.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-13 | Spec and child-contract roles, purpose, trigger, owner, consumer, system, and rules | `sdlc-document-roles.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-14 | Plan role, purpose, trigger, owner, consumer, system, and rules | `sdlc-document-roles.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-15 | Task role, purpose, trigger, owner, consumer, system, and rules | `sdlc-document-roles.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-16 | Guide role, purpose, trigger, owner, consumer, system, and rules | `sdlc-document-roles.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-17 | Incident role, purpose, trigger, owner, consumer, system, and rules | `sdlc-document-roles.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-18 | Postmortem role, purpose, trigger, owner, consumer, system, and rules | `sdlc-document-roles.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-19 | Policy role, purpose, trigger, owner, consumer, system, and rules | `sdlc-document-roles.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-20 | Release role, purpose, trigger, owner, consumer, system, and rules, including its deployment-evidence boundary | `sdlc-document-roles.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-21 | Runbook role, purpose, trigger, owner, consumer, system, and rules | `sdlc-document-roles.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-22 | Diataxis tutorial, how-to, reference, and explanation analysis and workspace mapping | `documentation-architecture.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-23 | LLM Wiki architecture, safety, generation, freshness, discovery, and implementation | `llm-wiki-system.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-24 | CI/CD system, rules, implementation, evidence, promotion, deployment, and rollback boundaries | `quality-ci-formatting.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-25 | GitHub Actions workflow, action, permissions, pinning, gate, and remote-enforcement analysis | `quality-ci-formatting.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-26 | QA formatting, linting, testing, syntax, type, coverage, and failure-handling analysis | `quality-ci-formatting.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-27 | Security governance, secure SDLC, supply chain, secret, approval, runtime, and implementation analysis | `security-governance.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-28 | External AI-agent catalog analysis using the official agency-agents repository and local import boundary | `ai-agent-catalogs.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-29 | Task-characteristic agent model, tier, effort, settings, evaluation, fallback, and change rules | `agent-model-selection.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-30 | Short-term, long-term, and domain memory plus promotion, retrieval, retention, eviction/deletion, archival, partition, privacy, and management rules | `memory-hierarchy.md` | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-31 | Current workspace baseline for every research category | `workspace-baseline.md` | `scope-application-matrix.md` | EXT-NIST verified as fixed comparison context; workspace claims use tracked sources | WS-TASK2-FOUNDATION | All 14 through the scope matrix | Implemented as draft Stage 90 leaf; route switch pending | Implementer PASS; specification and quality Approved C0/I0/M0 | [workspace baseline](../../90.references/research/2026-08-08-agentic-engineering-research-pack/workspace-baseline.md) |
| REQ-32 | Explicit analysis and disposition for all fourteen workspace scopes | `scope-application-matrix.md` | `workspace-baseline.md` | EXT-NIST verified as fixed comparison context; scope claims use tracked sources | WS-SCOPES, WS-CONTRACTS, WS-TASK2-FOUNDATION | 14/14 explicit dispositions | Implemented as draft Stage 90 leaf; route switch pending | Implementer PASS; specification and quality Approved C0/I0/M0 | [scope application matrix](../../90.references/research/2026-08-08-agentic-engineering-research-pack/scope-application-matrix.md) |
| REQ-33 | New authorship plus claim-level validation and integration before old-pack deletion | Pack README and Task migration ledger | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-34 | One-off cleanup, canonical cross-link switch, stale-path control, and affected generated artifacts | Task verification ledger | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| REQ-35 | Logical-unit commits, independent reviews, final verification, and branch handoff | Plan and Task | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |

### Normative scope ledger

| Scope | Governance owner | Applicable leaves | Current state | Rules / exceptions | Evidence owner | Validation owner | Catalog reachability | Review verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `agentic` | `docs/00.agent-governance/scopes/agentic.md` | Agentic leaves, automation | Implemented definitions; runtime unverified | Stage 00/provider parity and approval gates | `hook-developer`, `skill-creator` | `rules-engineer`; provider/repo contracts | Enum + 4 agents | Implementer PASS; independent `Not Run` |
| `architecture` | `docs/00.agent-governance/scopes/architecture.md` | SDLC, roles, Compose, security, automation | Partial; 53 Stage 02 files; runtime protocols unverified | ADR/Spec ownership before adoption | System Architect persona; Stage 02 path owner `infra-implementer` | Metadata/repo contracts and architecture review | Enum only; 0 agents | Implementer PASS; independent `Not Run` |
| `backend` | `docs/00.agent-governance/scopes/backend.md` | Quality/security/Compose when surface exists | Not Applicable to current application corpus | Requires approved backend Spec and surface | Backend persona; no typed agent | Future layer owner plus QA/security | Outside enum; 0 agents | Implementer PASS; independent `Not Run` |
| `common` | `docs/00.agent-governance/scopes/common.md` | Instructions, metadata, docs, quality, security | Partial; shared gates exist; some claimed roots absent | No direct pre-commit/lint/format | Cross-layer implementer | `code-reviewer`; scoped checks | Enum + 1 agent | Implementer PASS; independent `Not Run` |
| `docs` | `docs/00.agent-governance/scopes/docs.md` | SDLC/docs/metadata/LLM Wiki/memory; all leaves as references | Implemented corpus; later route integration pending | Explicit approval, template, link, generator rules | `doc-writer` | Metadata/repo contracts and docs review | Enum + 1 agent | Implementer PASS; independent `Not Run` |
| `entry` | `docs/00.agent-governance/scopes/entry.md` | Compose, security, automation, quality | Partial; 16 gateway files; edge/runtime unverified | Route through infra; concrete runtime approval | `infra-implementer` | `iac-reviewer`, `drift-detector` | Outside enum; 0 agents | Implementer PASS; independent `Not Run` |
| `frontend` | `docs/00.agent-governance/scopes/frontend.md` | Quality, automation, security, instructions | Partial; Storybook fixture, no product frontend proof | Treat current sandbox as QA-owned | Existing Storybook owner `code-reviewer` | Frontend/Storybook quality gates | Outside enum; 0 agents | Implementer PASS; independent `Not Run` |
| `infra` | `docs/00.agent-governance/scopes/infra.md` | Compose, security, automation, quality, harness environment | Implemented definitions; runtime unverified | Compose pre-flight; targeted approval/rollback; no secrets | `infra-implementer` | `iac-reviewer`, `drift-detector` | Enum + 3 agents | Implementer PASS; independent `Not Run` |
| `meta` | `docs/00.agent-governance/scopes/meta.md` | Metadata, docs architecture, LLM Wiki, roles, SDLC | Partial; validator-backed subject, missing typed route | Route through docs; Meta ADR for structure | `doc-writer` | Metadata/corpus/repo contracts | Outside enum; 0 agents | Implementer PASS; independent `Not Run` |
| `mobile` | `docs/00.agent-governance/scopes/mobile.md` | Quality/security/automation after surface exists | Not Applicable; 0 tracked mobile sources | Requires approved product/Spec/surface | Mobile persona; no typed agent | Future layer owner plus QA/security | Outside enum; 0 agents | Implementer PASS; independent `Not Run` |
| `ops` | `docs/00.agent-governance/scopes/ops.md` | Automation, quality, Compose, security, roles | Partial; tracked ops surfaces; outcomes unverified | Incident/runtime evidence stays in owners | `incident-responder`, `ci-cd-engineer` | Independent ops/infra review | Enum + 2 agents | Implementer PASS; independent `Not Run` |
| `product` | `docs/00.agent-governance/scopes/product.md` | SDLC, roles, documentation architecture | Partial; 26 Stage 01 files; typed owner missing | Human approval before Spec and Stage 01 mutation | Product persona/human stakeholder | Human approval plus docs gates | Outside enum; 0 agents | Implementer PASS; independent `Not Run` |
| `qa` | `docs/00.agent-governance/scopes/qa.md` | Harness, loop, automation, quality, security, LLM Wiki | Partial; extensive gates; remote state unverified | Smallest applicable check; docs coverage N/A; no direct pre-commit | `qa-engineer` | `eval-engineer` | Enum + 2 agents | Implementer PASS; independent `Not Run` |
| `security` | `docs/00.agent-governance/scopes/security.md` | Security, Compose, quality, automation, provider/harness | Partial; tracked controls; secret/runtime/remote excluded | Metadata-only secret evidence and concrete approval | Relevant layer implementer | `security-auditor` and named gates | Enum + 1 read-only agent | Implementer PASS; independent `Not Run` |

### External source ledger

These are required source-family seeds, not verified claims. Retrieval and
claim association remain `Not Run` until the assigned authoring unit opens the
source and records its current evidence.

| Source ID | Topic | Authority | Direct URL | Version / revision | Retrieved at | Mutability | Verification state | Claim IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXT-CLAUDE-HOOKS | Claude Code hooks | Anthropic | `https://code.claude.com/docs/en/hooks` | Retrieval-time page; no stable revision displayed | 2026-08-08T15:48:51+09:00 | External mutable | Verified direct official page; HTTP 200; no redirect; lifecycle/configuration facts only | REQ-01 through REQ-05 |
| EXT-CLAUDE-AGENTS | Claude Code subagents | Anthropic | `https://code.claude.com/docs/en/sub-agents` | Retrieval-time page; no stable revision displayed | 2026-08-08T15:48:51+09:00 | External mutable | Verified direct official page; HTTP 200; no redirect; schema/model/effort facts only | REQ-01 through REQ-05 |
| EXT-CLAUDE-SETTINGS | Claude Code settings | Anthropic | `https://code.claude.com/docs/en/settings` | Retrieval-time page; no stable revision displayed | 2026-08-08T15:48:51+09:00 | External mutable | Verified direct official page; HTTP 200; no redirect; scope/precedence facts only | REQ-03 through REQ-05 |
| EXT-CLAUDE-MEMORY | Claude Code instructions and memory | Anthropic | `https://code.claude.com/docs/en/memory` | Retrieval-time page; no stable revision displayed | 2026-08-08T15:48:51+09:00 | External mutable | Verified direct official page; HTTP 200; no redirect; context is not enforcement | REQ-01, REQ-03 through REQ-05 |
| EXT-CODEX-HOOKS | Codex hooks | OpenAI | `https://learn.chatgpt.com/docs/hooks` | Retrieval-time page; no stable revision displayed | 2026-08-08T15:48:51+09:00 | External mutable | Verified direct official page; HTTP 200; no redirect; 11 events including advisory main-thread `SessionEnd` | REQ-01 through REQ-05 |
| EXT-CODEX-AGENTS | Codex subagents | OpenAI | `https://learn.chatgpt.com/docs/agent-configuration/subagents` | Retrieval-time page; no stable revision displayed | 2026-08-08T15:48:51+09:00 | External mutable | Verified direct official page; HTTP 200; no redirect; orchestration/schema/model/sandbox facts only | REQ-01 through REQ-05 |
| EXT-CODEX-INSTRUCTIONS | Codex AGENTS.md | OpenAI | `https://learn.chatgpt.com/docs/agent-configuration/agents-md` | Retrieval-time page; no stable revision displayed | 2026-08-08T15:48:51+09:00 | External mutable | Verified direct official page; HTTP 200; no redirect; discovery/order/size facts only | REQ-03 through REQ-05 |
| EXT-CODEX-CONFIG | Codex configuration | OpenAI | `https://learn.chatgpt.com/docs/config-file/config-basic` | Retrieval-time page; no stable revision displayed | 2026-08-08T15:48:51+09:00 | External mutable | Verified direct official page; HTTP 200; no redirect; precedence/trust facts only | REQ-03 through REQ-05 |
| EXT-CODEX-MODELS | Codex models and reasoning controls | OpenAI | `https://learn.chatgpt.com/docs/models` | Retrieval-time page; no stable revision displayed | 2026-08-08T15:48:51+09:00 | External mutable | Verified direct official page; HTTP 200; no redirect; selection controls do not prove entitlement | REQ-04, REQ-05 |
| EXT-COMPOSE | Docker Compose | Docker | `https://docs.docker.com/reference/compose-file/` | Not Run | Not Run | External mutable | Not Run | Not Run |
| EXT-GHA | GitHub Actions | GitHub | `https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions` | Not Run | Not Run | External mutable | Not Run | Not Run |
| EXT-DIATAXIS | Documentation architecture | Diataxis | `https://diataxis.fr/` | Not Run | Not Run | External mutable | Not Run | Not Run |
| EXT-NIST | Secure SDLC | NIST | `https://csrc.nist.gov/pubs/sp/800/218/final` | SP 800-218 v1.1 | 2026-08-08 | External fixed | Verified direct primary page; HTTP 200; comparison only | REQ-31, REQ-32 |
| EXT-OWASP | Secure SDLC | OWASP | `https://owaspsamm.org/model/` | Not Run | Not Run | External mutable | Not Run | Not Run |
| EXT-SLSA | Supply chain | SLSA | `https://slsa.dev/spec/v1.2/` | v1.2 | Not Run | External fixed | Not Run | Not Run |
| EXT-OPENSSF | Supply chain | OpenSSF | `https://github.com/ossf/scorecard` | Not Run | Not Run | External mutable | Not Run | Not Run |
| EXT-AGENCY | AI-agent catalogs | agency-agents | `https://github.com/msitarzewski/agency-agents` | Not Run | Not Run | External mutable | Not Run | Not Run |

### Workspace evidence ledger

| Evidence ID | Tracked path | Identifier or command | Baseline commit | Verification state | Runtime limit | Claim IDs |
| --- | --- | --- | --- | --- | --- | --- |
| WS-SPEC-137 | `docs/03.specs/137-agentic-research-pack-rebuild/spec.md` | `artifact_id: spec:137-agentic-research-pack-rebuild` | `353182551d47c4232bceb58e573abd55b846420a` | Verified tracked input | Does not prove runtime or remote state | REQ-01 through REQ-35 |
| WS-PLAN | `docs/04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md` | `artifact_id: plan:2026-08-08-agentic-research-pack-rebuild` | `9917fcdadf700e7f68541e73188620e133485470` | Verified tracked input | Prospective plan, not execution proof | REQ-33 through REQ-35 |
| WS-OLD-PACK | `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/` | `find` plus `git ls-tree -r HEAD` | `9917fcdadf700e7f68541e73188620e133485470` | 20 files / 20 blobs verified | Historical input only | REQ-33, REQ-34 |
| WS-SCOPES | `docs/00.agent-governance/scopes/` | Fourteen normative filenames plus complete content analysis | `528c225d35d6c986b50f9b997fd08921a8df9a9b` | 14/14 verified and dispositioned | Tracked governance only | REQ-32 |
| WS-CONTRACTS | `docs/00.agent-governance/contracts/` | Parsed agent and provider-model registries | `528c225d35d6c986b50f9b997fd08921a8df9a9b` | 8 scopes, 14 agents, 24 functions, 5 profiles, 11 models verified | Tracked definitions do not prove execution | REQ-31, REQ-32 |
| WS-VALIDATORS | `scripts/knowledge/`, `scripts/validation/` | Task 1 baseline commands | `9917fcdadf700e7f68541e73188620e133485470` | Observed in verification ledger | Local command results only | REQ-23, REQ-24, REQ-26, REQ-27, REQ-34, REQ-35 |
| WS-TASK2-FOUNDATION | New foundation leaves | Required derivations, tracked inventory, and scope matrix | `528c225d35d6c986b50f9b997fd08921a8df9a9b` | Draft leaves implemented; focused metadata/diff gates PASS; repo contract retains separate predecessor | No runtime, remote, private, or ignored-state proof | REQ-31, REQ-32 |
| WS-TASK3-HARNESS | Stage 00 catalogs/providers plus `.claude/`, `.codex/`, `.agents/`, `.gemini/`, matching scripts/tests, and three new leaves | Required tracked inventory and `SessionEnd`/semantic-binding/effort/loop/harness derivations | `9a6e09ca06d99ae8234199443974c978640f3ae6` | 14 agents, 24 functions, 104 catalog projection memberships, 8 layers, 8 states, 4 typed loops, 7 semantic events/21 cells, 11 fixtures, 16 regressions verified; leaves drafted | Definitions/configuration/tests do not prove native execution, entitlement, private state, or remote enforcement | REQ-01 through REQ-05 |

### Old-claim migration ledger

The rows below pin one provisional claim-inventory container per old file so
later authoring units can add section- or claim-level rows without losing file
provenance. These rows are explicitly insufficient for the deletion gate: each
unique material claim must be decomposed, classified as `retain`, `correct`,
`omit`, or `supersede`, assigned a current evidence state and new destination,
and independently reviewed.

| Old path | Old commit | Old blob | Claim anchor | Claim summary | Disposition | Evidence state | New path | New anchor | Correction / omission reason | Review verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `README.md` | `9917fcdadf700e7f68541e73188620e133485470` | `a5c8b67e839ab074c2861caab5ed23366f4cb1b7` | Full-file claim inventory | Unique material claims require decomposition | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| `agent-instructions-vibe-coding.md` | `9917fcdadf700e7f68541e73188620e133485470` | `a014383a3585ba8945ccbb583781ba6b45cb982c` | Full-file claim inventory | Unique material claims require decomposition | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| `agent-model-selection.md` | `9917fcdadf700e7f68541e73188620e133485470` | `7b82620f75ad74bd515db385c9d0a64133dd4848` | Full-file claim inventory | Unique material claims require decomposition | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| `ai-agent-catalogs.md` | `9917fcdadf700e7f68541e73188620e133485470` | `f4c5dbd0c2e4f266df9590a592a204599415fe42` | Full-file claim inventory | Unique material claims require decomposition | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| `automation-pipeline-workflow.md` | `9917fcdadf700e7f68541e73188620e133485470` | `69b9ac96be78692b46e523ca3dedf871ee8e3ffb` | Full-file claim inventory | Unique material claims require decomposition | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| `docker-compose-infrastructure.md` | `9917fcdadf700e7f68541e73188620e133485470` | `5e70579fde9136d3d1b3f27e7e0d5aeb77b1b9b7` | Full-file claim inventory | Unique material claims require decomposition | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| `document-metadata-lifecycle.md` | `9917fcdadf700e7f68541e73188620e133485470` | `8a1212e9715cff80060db5d4c4d48a556d03a096` | Full-file claim inventory | Unique material claims require decomposition | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| `documentation-architecture.md` | `9917fcdadf700e7f68541e73188620e133485470` | `a0cf3b22431aae367570bc515821cee8c2cf4a19` | Full-file claim inventory | Unique material claims require decomposition | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| `harness-engineering.md` | `9917fcdadf700e7f68541e73188620e133485470` | `6d6cf79e2c724b801d2c66fa85d364acb363c784` | `Definitions / Facts` | Harness joins context, roles, tools, isolation, approvals, hooks, validation/eval, evidence, and governance | Retain | Verified against tracked owners | `harness-engineering.md` | `Harness element model` | Reauthored with explicit evidence-depth separation | Implementer classification; independent `Not Run` |
| `harness-engineering.md` | `9917fcdadf700e7f68541e73188620e133485470` | `6d6cf79e2c724b801d2c66fa85d364acb363c784` | `Provider Harness Criteria` | Claude/Codex instruction, agent, tool, hook, isolation, model, and evaluation capabilities differ | Retain | Official pages reverified 2026-08-08 | `provider-implementation-comparison.md` | `Current upstream construction` | Current direct provider observations replace inherited retrieval state | Implementer classification; independent `Not Run` |
| `harness-engineering.md` | `9917fcdadf700e7f68541e73188620e133485470` | `6d6cf79e2c724b801d2c66fa85d364acb363c784` | `HAR-04` | Seven semantic events yield 21 configured-not-executed provider bindings | Correct | Complete YAML shows 20 configured-not-executed and one unsupported Codex cell | `harness-engineering.md` | `Measured local construction` | Corrected semantic-binding depth and current upstream Codex `SessionEnd` support | Implementer classification; independent `Not Run` |
| `harness-engineering.md` | `9917fcdadf700e7f68541e73188620e133485470` | `6d6cf79e2c724b801d2c66fa85d364acb363c784` | `HAR-06` / Claude effort | Generated Sonnet and Opus adapters uniformly use high effort | Correct | Adapters show 11 high, one low, one xhigh, one omitted overall | `provider-implementation-comparison.md` | `Corrected local drift` | Typed work-profile outputs are correct; provider prose is stale | Implementer classification; independent `Not Run` |
| `harness-engineering.md` | `9917fcdadf700e7f68541e73188620e133485470` | `6d6cf79e2c724b801d2c66fa85d364acb363c784` | `Harness Implementation Matrix` | Canonical catalogs, adapters, scripts, tests, fixtures, and evidence form the local harness | Supersede | Re-measured at Task 3 BASE | `harness-engineering.md` | `Measured local construction` | New compact matrix separates definition/configuration/execution/enforcement/runtime/remote proof | Implementer classification; independent `Not Run` |
| `harness-engineering.md` | `9917fcdadf700e7f68541e73188620e133485470` | `6d6cf79e2c724b801d2c66fa85d364acb363c784` | `Adoption Boundary` / `Sources` | Adoption requires canonical ownership, least privilege, validation, review, and dated primary evidence | Retain | Governance and nine provider pages verified | `harness-engineering.md` | `Environment and rules for workspace application` | Reauthored with fourteen-scope routes and refreshed sources | Implementer classification; independent `Not Run` |
| `llm-wiki-system.md` | `9917fcdadf700e7f68541e73188620e133485470` | `553dafd5690a521071e900b453748393b2cf74fa` | Full-file claim inventory | Unique material claims require decomposition | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| `loop-engineering.md` | `9917fcdadf700e7f68541e73188620e133485470` | `1436c0b22e54f7c3679cc695577c0ae10700cb2a` | `Definitions / Facts` | Controlled loops require trigger, action, feedback, exit, retry, escalation, owner, and evidence | Retain | Reverified against typed loop fields and workflow rules | `loop-engineering.md` | `Loop anatomy` | Reauthored as a reusable element model | Implementer classification; independent `Not Run` |
| `loop-engineering.md` | `9917fcdadf700e7f68541e73188620e133485470` | `1436c0b22e54f7c3679cc695577c0ae10700cb2a` | `Loop Contract Matrix` | Ten prose feedback patterns describe current practice | Correct | Ten rows exist, but they are analytical and not ten canonical enforced objects | `loop-engineering.md` | `Analytical feedback patterns` | Retained taxonomy without converting it into policy or adding it arithmetically to typed loops | Implementer classification; independent `Not Run` |
| `loop-engineering.md` | `9917fcdadf700e7f68541e73188620e133485470` | `1436c0b22e54f7c3679cc695577c0ae10700cb2a` | `Typed Harness Loops` | Four loops have exact attempts, stop, failure, reviewer, permission, and evidence bounds | Retain | Complete provider contract and validator tests verified | `loop-engineering.md` | `Canonical lifecycle and typed loops` | Exact values preserved; repository enforcement is not native execution proof | Implementer classification; independent `Not Run` |
| `loop-engineering.md` | `9917fcdadf700e7f68541e73188620e133485470` | `1436c0b22e54f7c3679cc695577c0ae10700cb2a` | `remaining six loops` | Seven named prose patterns are the remaining six after typed-loop comparison | Correct | Arithmetic and model relationship are invalid; views overlap without a bijection | `loop-engineering.md` | `Analytical feedback patterns` | Removed subtraction claim and named the non-bijective relationship | Implementer classification; independent `Not Run` |
| `loop-engineering.md` | `9917fcdadf700e7f68541e73188620e133485470` | `1436c0b22e54f7c3679cc695577c0ae10700cb2a` | `Provider Loop Criteria` / `Claude and Codex Implementation Status` | Stop is translated per provider; semantic hooks provide feedback with local gaps | Correct | Shared dispatcher/config/tests plus current official hooks pages | `loop-engineering.md` | `Semantic-event feedback depth` / `Stop and retry behavior` | Corrected 21-cell depth and upstream-supported/local-missing Codex `SessionEnd` | Implementer classification; independent `Not Run` |
| `loop-engineering.md` | `9917fcdadf700e7f68541e73188620e133485470` | `1436c0b22e54f7c3679cc695577c0ae10700cb2a` | `Adoption Boundary` / `Sources` | Loops preserve approval, privacy, independent review, and direct evidence boundaries | Retain | Governance, contracts, scripts, tests, and official pages verified | `loop-engineering.md` | `Scope Implications` / `Sources` | Reauthored with explicit 14-scope dispositions and refreshed sources | Implementer classification; independent `Not Run` |
| `memory-hierarchy.md` | `9917fcdadf700e7f68541e73188620e133485470` | `27439218ae394c2df0dd936eb8dbd2bcf9062202` | Full-file claim inventory | Unique material claims require decomposition | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| `provider-implementation-comparison.md` | `9917fcdadf700e7f68541e73188620e133485470` | `26e3c6e9d56f4f412de46532a8f98c6fbd6e8b76` | `Official Evidence Ledger` | Claude/Codex instruction, agent, hook, settings, and model mechanisms require current official evidence | Supersede | Nine minimum pages directly reverified 2026-08-08; all HTTP 200/no redirect | `provider-implementation-comparison.md` | `Sources` | Replaced predecessor access state with the required current retrieval set | Implementer classification; independent `Not Run` |
| `provider-implementation-comparison.md` | `9917fcdadf700e7f68541e73188620e133485470` | `26e3c6e9d56f4f412de46532a8f98c6fbd6e8b76` | `Measured Workspace Facts` / role surfaces | One canonical catalog projects 14 roles and 24 functions into provider surfaces | Retain | Catalog, complete directories, renderer, and tests verified | `provider-implementation-comparison.md` | `Measured local adoption` | Current counts and proof limits retained compactly | Implementer classification; independent `Not Run` |
| `provider-implementation-comparison.md` | `9917fcdadf700e7f68541e73188620e133485470` | `26e3c6e9d56f4f412de46532a8f98c6fbd6e8b76` | `Instruction and role surfaces` | Claude transcludes imports; Codex discovers AGENTS.md hierarchy and project config is trust-gated | Retain | Official memory/AGENTS/config pages and root shims verified | `provider-implementation-comparison.md` | `Common Construction Matrix` instruction/settings rows | Kept semantic commonality and native loading differences separate | Implementer classification; independent `Not Run` |
| `provider-implementation-comparison.md` | `9917fcdadf700e7f68541e73188620e133485470` | `26e3c6e9d56f4f412de46532a8f98c6fbd6e8b76` | `Model control` / `Effort control` | Work profiles translate to provider-native model and reasoning fields | Correct | Complete contract/adapters/tests show Claude effort distribution and Codex fields | `provider-implementation-comparison.md` | `Corrected local drift` / model matrix rows | Corrected stale uniform-high Claude prose; runtime selection remains unverified | Implementer classification; independent `Not Run` |
| `provider-implementation-comparison.md` | `9917fcdadf700e7f68541e73188620e133485470` | `26e3c6e9d56f4f412de46532a8f98c6fbd6e8b76` | `Loop surfaces` / `Repository-side event gap` | Claude binds seven semantic events; Codex binds six and lacks local `SessionEnd` | Correct | Official Codex now supports `SessionEnd`; local contract/config remains stale | `provider-implementation-comparison.md` | `Corrected local drift` / semantic hook rows | Reclassified as upstream-supported local gap and corrected binding-depth count | Implementer classification; independent `Not Run` |
| `provider-implementation-comparison.md` | `9917fcdadf700e7f68541e73188620e133485470` | `26e3c6e9d56f4f412de46532a8f98c6fbd6e8b76` | `Common Claude/Codex Environment` | Common semantic policy requires translation and preserves irreducibly native mechanisms | Supersede | Spec 137 exact matrix contract plus current official/tracked evidence | `provider-implementation-comparison.md` | `Common Construction Matrix` | Rebuilt with all ten required columns and explicit execution/enforcement/gap cells | Implementer classification; independent `Not Run` |
| `provider-model-landscape.md` | `9917fcdadf700e7f68541e73188620e133485470` | `f51b3d4bbb23490f66de4d8bf2c46d85f5a8f99b` | Full-file claim inventory | Unique material claims require decomposition | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| `quality-ci-formatting.md` | `9917fcdadf700e7f68541e73188620e133485470` | `7f4e064dce61f468e0be3cf5002af7bf5a8d80c8` | Full-file claim inventory | Unique material claims require decomposition | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| `scope-application-matrix.md` | `9917fcdadf700e7f68541e73188620e133485470` | `ac19e2c93cc2ecf09f3a14b6308553221e637f45` | Full-file claim inventory | Unique material claims require decomposition | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| `sdlc-document-roles.md` | `9917fcdadf700e7f68541e73188620e133485470` | `b4aeeffafcfeda3fe1ccdf6637c01ef811c69236` | Full-file claim inventory | Unique material claims require decomposition | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| `security-governance.md` | `9917fcdadf700e7f68541e73188620e133485470` | `32af3c515643ea326fbd9db84ce71a57028a4a05` | Full-file claim inventory | Unique material claims require decomposition | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| `spec-driven-sdlc.md` | `9917fcdadf700e7f68541e73188620e133485470` | `10b06739620306465bf924a7b5fed2df3dd1e900` | Full-file claim inventory | Unique material claims require decomposition | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |
| `workspace-baseline.md` | `9917fcdadf700e7f68541e73188620e133485470` | `7cda3c192ba8a2577f5d4427a532d75455678853` | Full-file claim inventory | Unique material claims require decomposition | Not Run | Not Run | Not Run | Not Run | Not Run | Not Run |

### Generated-artifact inventory

| Artifact | Source trigger | Generator | Freshness check | Baseline result | Required disposition | Final result |
| --- | --- | --- | --- | --- | --- | --- |
| `docs/90.references/llm-wiki/llm-wiki-index.md` | Tracked safe-path set or canonical route changes | `scripts/knowledge/generate-llm-wiki-index.sh` | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | Design-time PASS; Task 1 observation FAIL, exit 1: stale index | Regenerate after route switch and require PASS; preserve observed drift | Not Run |
| `docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md` | Tracked Stage/category path set changes | `scripts/knowledge/generate-llm-wiki-coverage.sh` | `bash scripts/knowledge/generate-llm-wiki-coverage.sh --check` | Design-time FAIL; Task 1 observation FAIL, exit 1: stale coverage | Regenerate after route switch and require PASS | Not Run |
| `docs/90.references/data/security/security-automation-readiness.md` | Security controls, scripts, workflows, or typed workflow registry changes | `scripts/validation/generate-security-automation-readiness.sh` | `bash scripts/validation/generate-security-automation-readiness.sh --check` | Design-time FAIL; Task 1 observation FAIL, exit 1: stale snapshot | Preserve classified predecessor; do not regenerate known-invalid output without separate approval | Not Run |
| `graphify-out/**` | Tracked corpus changes | Graphify workspace updater | `bash scripts/knowledge/report-graphify-health.sh` after explicitly authorized refresh | Advisory and stale at `f8a72211`; no refresh authorized | Keep advisory and unchanged; corroborate against tracked sources | Not Run |

### Old-path allowlist

The allowlist is fail-closed. No historical literal is approved by Task 1.
Task 10 must scan the complete tracked-text universe and add only reviewed,
non-link historical literals with path, stable anchor, reason, and verdict.

| Path | Line or stable anchor | Literal class | Reason | Review verdict |
| --- | --- | --- | --- | --- |
| No entries approved | Not Run | Not Run | Complete retiring-path scan has not run | Not Run |

## Work Log

| Date | Unit | Evidence | Result |
| --- | --- | --- | --- |
| 2026-08-08 | Task 1 | Loaded governance, template, Spec 137, Plan, old pack, and stale Graphify report | Inputs corroborated; Graphify remained advisory |
| 2026-08-08 | Task 1 | Captured Task BASE, 20 sorted filenames, and 20 Git blob records | Immutable old-pack objects pinned |
| 2026-08-08 | Task 1 | Ran five predecessor checks | Exact classifications recorded below |
| 2026-08-08 | Task 1 | Created `/tmp/agentic-research-validation-venv` and installed `scripts/requirements.txt` | Install PASS; `html5lib 1.1` import PASS |
| 2026-08-08 | Task 1 | Ran repository contract through the isolated environment | Missing-dependency failure removed; separate memory predecessor remained |
| 2026-08-08 | Task 1 | Ran scoped metadata, traceability, whitespace, row-count, and changed-path checks | PASS; self-review found no Critical or Important issue |
| 2026-08-08 | Task 2 | Re-measured tracked corpus, scope files, typed registries, provider adapters, workflows, scripts, templates, stages, and infra | 1,646 paths; 14 scopes; 28 active Spec directories; 32 archived Specs; all reported counts derived at `528c225d` |
| 2026-08-08 | Task 2 | Analyzed fourteen scopes plus persona and complete typed catalog | 14/14 dispositions; exact six outside enum recorded; `architecture` enum-only distinction preserved |
| 2026-08-08 | Task 2 | Authored workspace baseline and scope matrix from the Stage 90 contract | Two draft leaves cover 19 categories, 14 scopes, adoption rules, limits, owners, and dated sources |
| 2026-08-08 | Task 2 | Ran focused gates and implementer self-review | Metadata and diff PASS; repository contract retains only the separate Memory predecessor; C0/I0 |
| 2026-08-08 | Task 3 | Backfilled completed Task 1 fix/re-reviews and Task 2 commit/reviews from the ignored SDD ledger before adding Task 3 evidence | Task 1 fix `528c225d`, scoped spec/quality Approved C0/I0/M0; Task 2 `9a6e09ca`, spec/quality Approved C0/I0/M0 |
| 2026-08-08 | Task 3 | Reopened nine minimum official Claude/Codex pages and checked effective URLs | All HTTP 200 with no redirects; mutable retrieval-time observations recorded |
| 2026-08-08 | Task 3 | Measured catalogs, projections, adapters, hooks, harness layers, workflow states, loops, semantic bindings, fixtures, regressions, scripts, and tests | 14 agents, 24 functions, 104 memberships, 8 layers, 8 states, 4 loops, 7 events/21 cells, 11 fixtures, 16 regressions |
| 2026-08-08 | Task 3 | Authored three new leaves and decomposed the three predecessor claim containers | REQ-01 through REQ-05 and 14-scope implications drafted; Task 3 independent review remains `Not Run` |

## Verification Evidence

Evidence capture timestamp for the Task 1 baseline set is
`2026-08-08T15:12:19+09:00`. Command output is summarized without raw-log or
private-state material.

| Command | Comparison / baseline | Exit | Classification | Attributable result |
| --- | --- | --- | --- | --- |
| `find docs/90.references/research/2026-07-05-agentic-research-pack-refresh -maxdepth 1 -type f -printf '%f\n' \| sort` | Task BASE | 0 | PASS | 20 filenames |
| `git ls-tree -r HEAD docs/90.references/research/2026-07-05-agentic-research-pack-refresh` | Task BASE | 0 | PASS | 20 blob records |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | Task BASE | 1 | FAIL, predecessor | Stale index; differs from design-time PASS and is preserved as observed |
| `bash scripts/knowledge/generate-llm-wiki-coverage.sh --check` | Task BASE | 1 | FAIL, predecessor | Stale coverage snapshot; matches design-time classification |
| `bash scripts/validation/generate-security-automation-readiness.sh --check` | Task BASE | 1 | FAIL, predecessor | Stale security readiness snapshot; matches design-time classification |
| `bash scripts/validation/check-doc-implementation-alignment.sh` | Task BASE | 1 | FAIL, predecessor | `failures=184`, including 182 archive direct links and 2 missing local targets |
| `bash scripts/validation/check-repo-contracts.sh` | Task BASE, system Python | 1 | FAIL, dependency | `AGC-DEPENDENCY-MISSING path=html5lib location=validation-runtime` |
| `python3 -m venv /tmp/agentic-research-validation-venv` | Disposable environment | 0 | PASS | Virtual environment created outside repository |
| `/tmp/agentic-research-validation-venv/bin/python -m pip install --requirement scripts/requirements.txt` | Repository-pinned requirements | 0 | PASS | Pinned validation requirements installed |
| `/tmp/agentic-research-validation-venv/bin/python -c 'import html5lib; print(html5lib.__version__)'` | Isolated interpreter | 0 | PASS | Printed `1.1` |
| `env PATH=/tmp/agentic-research-validation-venv/bin:$PATH bash scripts/validation/check-repo-contracts.sh` | Task BASE, isolated interpreter | 1 | FAIL, separate predecessor | Dependency failure absent; `AGC-MEMORY-FORBIDDEN-MATERIAL` remains in `docs/00.agent-governance/memory/current.md` |
| `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 35318255 --changed-path docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md --changed-path docs/04.execution/tasks/README.md` | Spec activation base | 0 | PASS | `selected=2 violations=0 legacy_exceptions=0 transition_overrides=0` |
| `bash scripts/validation/check-doc-traceability.sh` | Working tree | 0 | PASS | `catalog_pairs_total=46 failures=0` |
| `git diff --check` | Working tree | 0 | PASS | No whitespace errors |
| Required Task 2 derivation set | `528c225d35d6c986b50f9b997fd08921a8df9a9b` | 0 | PASS | 1,646 tracked paths; exactly 14 scopes; 28 active Spec directories; 32 archived `spec.md` files |
| `curl -sSL` direct NIST SP 800-218 page check | External fixed source, 2026-08-08 | 0 | PASS | HTTP 200; comparison context only |
| Task 2 exact metadata command for both foundation leaves | Spec activation base `35318255` | 0 | PASS | `selected=2 violations=0 legacy_exceptions=0 transition_overrides=0` |
| First isolated Task 2 repository-contract run | Working tree before heading correction | 1 | FAIL, attributable plus predecessor | Found two missing `## Repository Role` headings and separate `AGC-MEMORY-FORBIDDEN-MATERIAL`; headings corrected in owned leaves |
| `env PATH=/tmp/agentic-research-validation-venv/bin:$PATH bash scripts/validation/check-repo-contracts.sh` after correction | Working tree | 1 | FAIL, separate predecessor | Task 2 reference-stage findings cleared; sole reported failure is `AGC-MEMORY-FORBIDDEN-MATERIAL` in forbidden `memory/current.md` |
| Task 2 exact fourteen-scope `rg` command | Both foundation leaves | 0 | PASS | `## Scope Implications` and every normative scope name present |
| `git diff --check` after Task 2 edits | Working tree | 0 | PASS | No whitespace errors |
| Task 3 exact metadata command for three agentic-core leaves | Spec activation base `35318255` | 0 | PASS | `selected=3 violations=0 legacy_exceptions=0 transition_overrides=0` |
| `env PATH=/tmp/agentic-research-validation-venv/bin:$PATH bash scripts/validation/check-repo-contracts.sh` after Task 3 authoring | Working tree | 1 | FAIL, separate predecessor | All Task 3 reference-stage checks cleared; sole failure is `AGC-MEMORY-FORBIDDEN-MATERIAL` in forbidden `memory/current.md` |
| Task 3 exact 14-scope and construction-matrix checks | Three leaves | 0 | PASS | Every leaf names all 14 scopes; provider leaf contains all ten Spec 137 columns |
| `git diff --check` after Task 3 edits | Working tree | 0 | PASS | No whitespace errors |

## Controlled Agent Pre-commit Evidence

The controlled all-files wrapper is outside Task 1 and was not authorized as
this unit's scoped validation. Command, allowed prefixes, exit status, snapshot
result, observation boundary, path sets, and disposition are all `Not Run`.
Task 1 uses only the exact checks named by its Plan.

## Review Evidence

| Review | Range | Reviewer | Verdict | Findings / disposition |
| --- | --- | --- | --- | --- |
| Implementer self-review | Working tree before Task 1 commit | Task 1 implementer | PASS | Exact row counts are 35 requirements, 14 scopes, and 20 pinned old-file claim containers; two owned tracked files only; no Critical or Important finding |
| Specification compliance | `9917fcdadf700e7f68541e73188620e133485470..c15c296b5d3dc90c95a28dbee4336f2aa98cc3e4` | Independent reviewer | Approved; C0/I0/M0 | First committed-unit specification review returned no findings |
| Documentation quality | `9917fcdadf700e7f68541e73188620e133485470..c15c296b5d3dc90c95a28dbee4336f2aa98cc3e4` | Independent reviewer | Needs fixes; C0/I1/M0 | Important finding: backfill the known Task 1 commit and review identities; fix re-review Not Run |
| Task 1 scoped specification re-review | `c15c296b5d3dc90c95a28dbee4336f2aa98cc3e4..528c225d35d6c986b50f9b997fd08921a8df9a9b` | Independent specification reviewer | Approved; C0/I0/M0 | Fix round 1 resolved the prior identity/evidence finding |
| Task 1 scoped quality re-review | `c15c296b5d3dc90c95a28dbee4336f2aa98cc3e4..528c225d35d6c986b50f9b997fd08921a8df9a9b` | Independent documentation-quality reviewer | Approved; C0/I0/M0 | Fix round 1 returned a clean scoped verdict |
| Task 2 implementer self-review | Working tree before Task 2 commit | Task 2 implementer | PASS; C0/I0 | Exactly two new leaves plus this Task ledger; 19/19 category rows, 14/14 scope rows, six outside-enum scopes explicit, `architecture` enum-only explicit, advisory/secret/runtime/remote boundaries preserved |
| Task 2 specification compliance | `528c225d35d6c986b50f9b997fd08921a8df9a9b..9a6e09ca06d99ae8234199443974c978640f3ae6` | Independent specification reviewer | Approved; C0/I0/M0 | Committed foundation unit met Task 2/Spec 137 requirements |
| Task 2 documentation quality | `528c225d35d6c986b50f9b997fd08921a8df9a9b..9a6e09ca06d99ae8234199443974c978640f3ae6` | Independent documentation-quality reviewer | Approved; C0/I0/M0 | Committed foundation unit returned a clean quality verdict |
| Task 3 implementer self-review | Working tree before Task 3 commit | Task 3 implementer | PASS; C0/I0 | Three leaf contracts, exact construction-matrix columns, 14/14 scope implications, source/evidence distinctions, old-claim decomposition, and owned-path boundary verified; independent reviews remain `Not Run` |

## Commit Ledger

| Unit | Commit identity | Logical unit | Validation | Review state |
| --- | --- | --- | --- | --- |
| Task 1 | `c15c296b5d3dc90c95a28dbee4336f2aa98cc3e4`; `docs(task): initialize agentic research rebuild ledger` | Execution ledger and immutable baselines | Task 1 scoped checks | Specification Approved C0/I0/M0; quality Needs fixes C0/I1/M0 |
| Task 1 fix 1 | `528c225d35d6c986b50f9b997fd08921a8df9a9b`; `docs(task): backfill task 1 review identity` | Review-identity/evidence correction | Focused metadata and diff PASS | Scoped specification and quality re-reviews Approved C0/I0/M0 |
| Task 2 | `9a6e09ca06d99ae8234199443974c978640f3ae6`; `docs(research): establish workspace and scope baseline` | Workspace baseline, scope matrix, and execution evidence | Focused metadata/scope/diff PASS; repository contract has separate predecessor | Implementer PASS C0/I0; specification and quality Approved C0/I0/M0 |
| Task 3 | Commit identity pending this unit; `docs(research): analyze harness loops and providers` | Harness, loop, provider comparison, and execution evidence | Metadata/scope/matrix/diff PASS; repository contract retains only separate Memory predecessor | Implementer PASS C0/I0; independent reviews `Not Run` |
| Tasks 4-12 | Not Run | Not Run | Not Run | Not Run |

## Deferred and Blocked Items

- The LLM Wiki index is stale at Task BASE even though it passed at design
  time. The observation is carried forward for the route-switch unit.
- LLM Wiki coverage and security readiness remain their known FAIL
  predecessors. The security generator repair is outside this documentation
  unit unless separately approved.
- The isolated repository-contract run removes the `html5lib` blocker but
  reveals the separate `AGC-MEMORY-FORBIDDEN-MATERIAL` predecessor in
  `docs/00.agent-governance/memory/current.md`; Task 1 does not modify that
  forbidden path.
- Claim-level decomposition beyond the two foundation leaves, remaining
  external-source retrieval, old-path scanning, generated refresh, independent
  Task 2 reviews, and old-pack deletion are all Not Run. The deletion gate
  remains closed.
- Push, pull request, merge, remote mutation, and live runtime validation
  remain outside the approved boundary.

## Related Documents

- [Spec 137](../../03.specs/137-agentic-research-pack-rebuild/spec.md)
- [Implementation Plan](../plans/2026-08-08-agentic-research-pack-rebuild.md)
- [Execution task index](./README.md)
- [Canonical Task template](../../99.templates/templates/sdlc/task.template.md)
- [Research category router](../../90.references/research/README.md)
- [Old research pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
