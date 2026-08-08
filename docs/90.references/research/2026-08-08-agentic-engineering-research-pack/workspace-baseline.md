---
status: draft
artifact_id: reference:agentic-engineering-research:workspace-baseline
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-08
review_cycle: on-source-change
---

# Reference: Agentic Engineering Workspace Baseline

## Overview

This reference is the measured workspace-state entry point for the agentic
engineering research pack. It records tracked corpus, agent-system, delivery,
documentation, infrastructure, and scope counts at Git commit
`528c225d35d6c986b50f9b997fd08921a8df9a9b` on 2026-08-08.

The baseline is Stage 90 analysis. It supports later research leaves but does
not become policy, runtime truth, remote-enforcement proof, or execution
evidence merely because another document cites it.

## Purpose

Provide REQ-31 with one reproducible, current baseline for every research-pack
category. Later leaves can cite this document for corpus cardinalities and
evidence boundaries instead of copying historical counts from the predecessor
pack.

## Repository Role

This Stage 90 reference preserves dated source-backed facts and explanatory
context. Current policy remains in Stage 00 and Stage 05, lifecycle intent and
execution remain in Stages 01-04, runtime truth remains in tracked runtime
owners, and remote state requires separate control-plane evidence.

## Scope

### In scope

- Git-tracked repository paths and typed Stage 00 contracts.
- Current Stage 01-05, Stage 90, Stage 98, and Stage 99 corpus observations.
- Provider adapters, workflows, scripts, templates, Compose definitions, and
  infrastructure paths that are visible to Git.
- The nineteen planned research leaves and their current evidence readiness.

### Out of scope

- Ignored-local files and volumes, secret values, credentials, private provider
  state, shell history, and raw logs.
- Live containers, service health, remote GitHub settings, provider
  entitlements, deployment results, and other runtime or remote state.
- Adoption of a research recommendation or mutation of any policy, runtime,
  workflow, generated artifact, or provider adapter.
- The stale Graphify snapshot as proof. Its report was built from `f8a72211`;
  all facts below were corroborated against tracked sources and stage docs.

## Definitions / Facts

### Concept and evidence model

A baseline is a dated inventory, not a health verdict. This document separates
four evidence classes:

- **Tracked definition**: a Git-visible file, typed registry, or stage artifact.
- **Local observation**: a safe command result captured for this Task.
- **Runtime or remote state**: state requiring container, provider, or remote
  control-plane evidence; it remains unverified here.
- **External comparison**: primary-source context that does not establish local
  adoption. NIST SSDF v1.1 supplies a stable secure-development comparison
  vocabulary; local owners and validators remain repository-defined.

Implementation labels are `Implemented`, `Partial`, `Missing`, `Not
Applicable`, and `Unverified`. `Implemented` means the tracked contract or
surface exists; it never upgrades runtime or remote evidence.

### Reproducible baseline measurements

All results use the stated baseline commit. Counts produced from `git ls-files`
exclude ignored-local and untracked paths.

| Measurement | Derivation | Result |
| --- | --- | ---: |
| Tracked paths | `git ls-files > /tmp/agentic-research-tracked-paths.txt; wc -l ...` | 1,646 |
| Normative persona scopes | sorted `find docs/00.agent-governance/scopes -maxdepth 1 -type f -name '*.md'` | 14 |
| Typed catalog scopes | `scopes` in `contracts/agent-catalog.yaml` | 8 |
| Typed agents / functions | `agents` and `functions` in `contracts/agent-catalog.yaml` | 14 / 24 |
| Work profiles / model records | `work_profiles` and `models` in `contracts/provider-models.yaml` | 5 / 11 |
| Harness layers / loops / workflow states | typed provider-model collections | 8 / 4 / 8 |
| Capability-intake decisions | `capability_intake` in `contracts/agent-catalog.yaml` | 9 |
| Synthetic fixtures / regressions | catalog `evaluation.fixture_count` / `regression_count` | 11 / 16 |
| Active Spec directories | `find docs/03.specs -mindepth 1 -maxdepth 1 -type d \| wc -l` | 28 |
| Archived `spec.md` files | `find docs/98.archive/03.specs -type f -name spec.md \| wc -l` | 32 |
| GitHub workflow files / declared jobs | tracked workflow YAML parsed by the isolated Python environment | 7 / 23 |
| Script files / validation files | `git ls-files scripts` and `git ls-files scripts/validation` | 63 / 41 |
| Compose-named YAML files | `git ls-files '*docker-compose*.yml'` | 49 |
| Infrastructure files / numbered domains | `git ls-files infra`; first-level numbered directories | 275 / 11 |
| Template files / pre-commit repositories | tracked `docs/99.templates/templates/**`; `.pre-commit-config.yaml` `repo` rows | 33 / 10 |
| TSX/JSX files / mobile source files | tracked extension queries | 6 / 0 |

### Documentation corpus

| Canonical surface | Tracked files | Interpretation |
| --- | ---: | --- |
| [Stage 00 governance](../../../00.agent-governance/README.md) | 109 | Policy, scopes, agents, functions, typed contracts, provider rules, and Memory routing. |
| [Stage 01 requirements](../../../01.requirements/README.md) | 26 | Active product-intent corpus including its index. |
| [Stage 02 architecture](../../../02.architecture/README.md) | 53 | 26 requirement-path files and 26 decision-path files plus the stage index. |
| [Stage 03 specifications](../../../03.specs/README.md) | 53 | 28 active Spec directories; file count and directory count answer different questions. |
| [Stage 04 execution](../../../04.execution/README.md) | 237 | 104 Plan-path files, 132 Task-path files, and the stage index. |
| [Stage 05 operations](../../../05.operations/README.md) | 263 | 88 guide, 87 policy, 85 runbook, one incident-index, one release-index, and the stage index. |
| [Stage 90 references](../../../90.references/README.md) | 97 | Stable references and generated/reference data at the baseline before these new files are tracked. |
| [Stage 98 archive](../../../98.archive/README.md) | 69 | Historical tombstones and archived lifecycle evidence, including 32 archived Specs. |
| [Stage 99 templates](../../../99.templates/README.md) | 48 | Template sources and their support contracts; 33 files are under the template tree itself. |

### Agent, provider, and harness system

The [typed agent catalog](../../../00.agent-governance/contracts/agent-catalog.yaml)
contains 14 agents and 24 functions. Its eight-value scope enum is `agentic`,
`architecture`, `common`, `docs`, `infra`, `ops`, `qa`, and `security`.
Agent records use seven of those values: `agentic` 4, `common` 1, `docs` 1,
`infra` 3, `ops` 2, `qa` 2, and `security` 1. `architecture` is admitted by the
enum but has no current agent record.

The exact six normative persona scopes outside the typed enum are `backend`,
`entry`, `frontend`, `meta`, `mobile`, and `product`. That is a catalog-routing
finding, not proof that their subject matter is absent. The detailed
disposition is in [the scope application matrix](./scope-application-matrix.md).

Provider adapter counts are `.claude/` 48, `.agents/` 41, `.codex/` 16, and
`.gemini/` 17 tracked files. The
[provider-model contract](../../../00.agent-governance/contracts/provider-models.yaml)
defines 3 providers, 5 work profiles, 11 model records, 8 harness layers, 8
workflow states, 4 harness loops, and 7 semantic events. These are definitions;
provider loading, entitlements, event interception, and model execution are
unverified here.

### Research-category readiness

This table covers the nineteen-leaf pack contract. `Current evidence` is a
tracked starting point, not a substitute for each later leaf's source and claim
review.

| Research leaf / category | Current tracked evidence | Baseline state and limit |
| --- | --- | --- |
| `workspace-baseline.md` | 1,646-path inventory and typed registries | Implemented by this draft; independent review pending. |
| `scope-application-matrix.md` | 14 scope files, persona map, 8-value catalog enum | Implemented by its companion draft; independent review pending. |
| `harness-engineering.md` | 8 typed harness layers and provider adapters | Partial; definitions exist, live provider execution is unverified. |
| `loop-engineering.md` | 4 typed harness loops and 8 workflow states | Partial; deterministic contracts exist, live feedback behavior is unverified. |
| `provider-implementation-comparison.md` | 4 adapter projections and 3 provider records | Partial; tracked parity is measurable, provider-native execution is not. |
| `agent-instructions-vibe-coding.md` | root shims, bootstrap, scopes, and adapter rules | Partial; tracked instructions exist, behavioral compliance is evidence-specific. |
| `provider-model-landscape.md` | 11 model records across 3 providers | Partial; catalog facts exist, current entitlements and acceptance are unverified. |
| `agent-model-selection.md` | 5 work profiles, typed tiers/effort/fallback fields | Partial; selection contract exists, live comparative evaluation is unverified. |
| `ai-agent-catalogs.md` | 14 local agents, 24 functions, 9 intake decisions | Partial; local import boundary exists, external catalog comparison remains later work. |
| `memory-hierarchy.md` | Stage 00 Memory README/current route and one typed memory eval fixture | Partial; active policy covers bounded governance Memory, not a complete domain-memory lifecycle. |
| `spec-driven-sdlc.md` | 28 active Spec directories and 237 Stage 04 files | Implemented as a document system; enforcement strength requires per-gate evidence. |
| `sdlc-document-roles.md` | registered profiles/templates across Stages 01-05 | Implemented as metadata contracts; an artifact does not prove its intended outcome. |
| `document-metadata-lifecycle.md` | metadata profile registry and two document lifecycle validators | Implemented for registered surfaces; current command result belongs in Task evidence. |
| `documentation-architecture.md` | staged corpus plus 33 template-tree files | Partial; repository taxonomy exists, Diataxis comparison remains later work. |
| `llm-wiki-system.md` | 3 tracked LLM Wiki files and 3 knowledge scripts | Partial; Task 1 preserved stale index/coverage predecessors for the route-switch unit. |
| `automation-pipeline-workflow.md` | 63 scripts, 7 workflows, and 23 jobs | Partial; tracked orchestration exists, remote execution and deployment are unverified. |
| `quality-ci-formatting.md` | 41 validation files and 10 pre-commit repositories | Partial; local gates exist, remote required-check enforcement is unverified. |
| `docker-compose-infrastructure.md` | 49 Compose-named YAML files in 11 infra domains | Partial; definitions exist, no containers were started and runtime health is unverified. |
| `security-governance.md` | hardening, security, validation, incident, and supply-chain surfaces | Partial; tracked controls exist, secret values/private state were not inspected, and runtime/remote enforcement is unverified. |

### Workspace adoption environment and rules

1. Route changes to the canonical owner named by Stage 00 or the lifecycle
   stage; a Stage 90 recommendation is never the change owner.
2. For a tracked workspace claim, cite the owner path, baseline commit, and a
   reproducible identifier or command. Re-measure rather than forward-copying a
   historical count.
3. Keep provider capability, local adapter definition, local execution,
   runtime state, and remote enforcement as separate evidence fields.
4. Apply explicit approval boundaries before Stage 01-99 mutation, runtime or
   Compose mutation, secret-value access, remote mutation, or provider changes.
5. Use the isolated validation environment required by the active Plan for the
   repository contract. Preserve unrelated failures rather than relabeling
   them as passes or widening this unit's scope.

### Implementation status, limitations, and gaps

The workspace has substantial tracked implementation for all research groups
except current mobile and backend application surfaces. The highest-confidence
counts come from typed registries and Git path enumeration. The largest
verification boundary is outside Git: no claim here proves live Compose health,
provider behavior, GitHub rulesets, deployment promotion, private configuration,
or secret hygiene.

Current gaps and first owners are:

- scope/catalog reachability, including the six outside values and admitted
  `architecture` without an agent record: Stage 00 agent catalog owner;
- domain-memory lifecycle beyond bounded governance Memory: a future approved
  Stage 03 specification;
- CD promotion/deployment evidence: a future approved delivery/release chain;
- stale generated LLM Wiki and security readiness predecessors: the Task's
  later route-switch/security units, using only canonical generators;
- runtime, remote, and provider observations: remain `Unverified` until a
  separately approved evidence-gathering task executes them.

## Scope Implications

The companion [scope matrix](./scope-application-matrix.md) is the normative
scope-axis map for this pack. This baseline's own disposition is summarized
below so a topic-first reader encounters all fourteen scopes.

| Scope | Baseline implication |
| --- | --- |
| `agentic` | Direct: typed catalogs, provider adapters, harness, loop, instruction, model, and memory counts. |
| `architecture` | Direct: Stage 02/03 corpus counts; admitted catalog scope with no current agent record. |
| `backend` | Not applicable to a current backend application surface; future backend work must re-baseline code/tests. |
| `common` | Direct: shared formatting, naming, review, and diff-hygiene evidence. |
| `docs` | Direct: Stage 01-99 corpus, templates, metadata, and LLM Wiki evidence. |
| `entry` | Direct but routing-limited: 16 tracked gateway files; scope is outside the typed catalog. |
| `frontend` | Limited: 51 Storybook files and 6 TSX/JSX files; no general product frontend is proven. |
| `infra` | Direct: 275 infra files, 11 domains, and 49 Compose-named definitions; runtime unverified. |
| `meta` | Direct but routing-limited: metadata/template systems exist; scope is outside the typed catalog. |
| `mobile` | Not applicable: no tracked Swift, Kotlin, Dart, Android, or iOS source matched the derivation. |
| `ops` | Direct: 263 Stage 05 files and observability definitions; service outcomes remain unverified. |
| `product` | Direct but routing-limited: 26 Stage 01 files; scope is outside the typed catalog. |
| `qa` | Direct: 41 validation files, 7 workflows, 23 jobs, and 10 pre-commit repositories. |
| `security` | Direct: tracked control surfaces; private, secret, runtime, and remote states remain excluded. |

## Sources

| Source | Accessed | Class | Verification state |
| --- | --- | --- | --- |
| [Spec 137](../../../03.specs/137-agentic-research-pack-rebuild/spec.md) | 2026-08-08 | Tracked fixed baseline | Verified at active Spec commit `35318255`. |
| [Implementation Plan](../../../04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md) | 2026-08-08 | Tracked mutable | Verified at the Task baseline; defines REQ-31 and derivations. |
| [Agent catalog](../../../00.agent-governance/contracts/agent-catalog.yaml) | 2026-08-08 | Tracked mutable | Parsed through the isolated repository environment. |
| [Provider-model contract](../../../00.agent-governance/contracts/provider-models.yaml) | 2026-08-08 | Tracked mutable | Parsed through the isolated repository environment. |
| [Persona protocol](../../../00.agent-governance/rules/persona.md) | 2026-08-08 | Tracked mutable | Verified directly; names all fourteen persona scopes. |
| [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md) | 2026-08-08 | Tracked mutable | Verified directly; Stage 90 remains advisory. |
| [NIST SP 800-218, Secure Software Development Framework v1.1](https://csrc.nist.gov/pubs/sp/800/218/final) | 2026-08-08 | External fixed | Direct primary page returned HTTP 200; used only as comparison context. |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md) | 2026-08-08 | Tracked stale/advisory | Built from `f8a72211`; not used as current evidence. |

## Maintenance

Re-measure this document when tracked path sets, Stage 00 typed registries,
stage corpus routes, workflows, scripts, template families, Compose paths, or
the nineteen-leaf pack contract changes. Preserve the baseline commit and dated
command result when interpreting an older count. Do not refresh Graphify or any
generated artifact by hand; use its canonical owner in the separately approved
unit.

## Related Documents

- [Scope application matrix](./scope-application-matrix.md)
- [Spec 137](../../../03.specs/137-agentic-research-pack-rebuild/spec.md)
- [Implementation Plan](../../../04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md)
- [Execution Task](../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
- [Agent governance hub](../../../00.agent-governance/README.md)
- [Research category router](../README.md)
