---
title: "Repository Authority Map"
version: "0.1.0"
type: "governance/knowledge"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-06"
created: "2026-09-06"
observed_at: "2026-09-06"
review_cycle: "on-surface-change"
---

# Repository Authority Map

## Overview

This map answers one question: for a given repository surface, which document
owns it, who must approve a change to it, and which check proves the change.
It routes; it never states an obligation. Where a rule is needed, the owner
column names the document that holds it.

## Scope

Tracked repository surfaces and their canonical owners. Excluded: runtime
state, service health, credential contents, user-global provider settings, and
anything outside this repository.

## Surface Ownership

| Surface | Canonical owner | Approval boundary | Proving check |
| --- | --- | --- | --- |
| `.agents/governance/**` | the policy file itself | policy change requires `rules-engineer` review | `check-agent-governance-contract.py`, document metadata |
| `.agents/roles/**` | the role file's frontmatter | role permission change requires approval | agent governance contract, renderer parity |
| `.agents/skills/**` | `SKILL.md` per skill id | explicit invocation only; discovery grants nothing | agent governance contract, renderer parity |
| `.agents/knowledge/**` | this category's index | routing only; an obligation here is a defect | document metadata, agent governance contract |
| `.agents/prompts/**` | this category's index | contract envelope only; no procedure body | document metadata, agent governance contract |
| `.agents/governance/providers/registry.yaml` | the Provider Registry | provider, model, permission and hook facts, plus the `canonical_sources` inventory every canonical file must appear in, work profiles, projections, evaluation binding and `generated_roots`; it owns no agent governance policy | agent governance contract |
| `.claude/**`, `.codex/**` | authored `provider.md` per provider; everything else is generated or native mechanics | canonical contract plus authored/native distinction | `provider_surface_renderer.py --check` |
| `docs/01.requirements/**` | the Requirement Package | solution-independent needs only | metadata, links, traceability |
| `docs/02.architecture/**` | Description for structure, ADR for one decision | accepted decisions are superseded, never rewritten | metadata, links, taxonomy tests |
| `docs/03.specs/**` | the active Spec Package; its Task owns execution evidence | bounded change contract | metadata, corpus lifecycle, spec package tests |
| `docs/05.operations/**` | the operations catalog subject | operator procedure and incidents | operations catalog check |
| `docs/90.references/**` | Research, Audit, or Data package | non-normative dated evidence | metadata, reference protection tests |
| `docs/98.archive/**` | preserved frozen bodies plus Migration and Tombstone | frozen bodies are never edited | corpus lifecycle, archive recovery |
| `docs/99.templates/registry.json` | the Stage 99 registry | document shape, path, identity, lifecycle | registry and metadata suites |
| `.github/workflow-contract.yml` | executable composition and public suite membership | workflow contract plus security review | `check-github-workflow-contract.py` |
| `.github/workflows/**` | the workflow files | least privilege, pinned actions, no secrets in `run` | actionlint, workflow contract |
| `scripts/manifest.yaml` | file inventory, kind, lifecycle, consumers, tests | script surface changes | `check-script-manifest.py` |
| `scripts/lib/**` | importable domain logic | focused tests | `tests/lib/**` |
| `scripts/operations/**`, `scripts/validation/**` | executable entrypoints | focused tests plus harness validation | `tests/validation/**` |
| `tests/**` | `tests/lib` for library behavior, `tests/validation` for CLI | production code never reads `tests/` | the suites themselves |
| `evals/**` | deterministic model-free agent-output evaluation | synthetic fixtures only | agent-output eval fixture gate |
| `infra/**`, `docker-compose.yml` | the Compose layer | scoped Compose validation and Task approval | `validate-docker-compose.sh`, hardening checks |
| `secrets/**` | path and policy context only | metadata-only evidence; values are never read | template security baseline |
| `graphify-out/**` | generated navigation snapshot | advisory when its commit differs from HEAD | regenerate with the CLI; never hand-edit |

## Entry Order

1. Root `AGENTS.md` or `CLAUDE.md`.
2. [Bootstrap policy](../governance/bootstrap.md) and the matching authored
   provider adapter.
3. Only the policies, canonical role, and explicitly invoked skills the request
   needs.
4. For a repository change, the governing Requirement, Architecture, and Spec
   Package plus its current Task.
5. The applicable registered gates, with evidence recorded in that Task.

Loading more than the request needs is a cost, not a safeguard. Discovery of any
file in this map grants no permission.

## Where Similar Things Differ

- A Requirement states a need; a Spec states a bounded change; a Task states
  what actually happened. Execution evidence belongs only to the Task.
- A skill owns an ordered procedure; a prompt owns an input and output contract;
  a policy owns an obligation. Copying one into another creates a second
  authority.
- Stage 90 preserves dated observations; `.agents/knowledge/` holds living
  routing. A dated measurement is never rewritten to look current.
- The workflow contract owns which checks run; the script manifest owns which
  files exist and who consumes them. Neither repeats the other.

## Provenance

Derived by reading tracked sources at repository commit
`9ede309a5b1feba91e6f8b973a729716b14c55ab` on 2026-09-06: the canonical
governance policies, the Provider Registry, the Stage 99 registry, the workflow
contract's `public_gate` section, `scripts/manifest.yaml`, and the stage index
documents. The knowledge graph under `graphify-out/` was not used as evidence
because its build commit differs from HEAD.

## Refresh Triggers

- A canonical category is added to or removed from `.agents/`.
- A public suite, gate node, or changed-path rule changes in the workflow
  contract.
- A Stage 99 profile path pattern changes.
- A stage directory is added, renamed, or retired.

## Related Documents

- [Knowledge index](README.md)
- [Bootstrap policy](../governance/bootstrap.md)
- [Approval boundaries](../governance/approval-boundaries.md)
- [Documentation protocol](../governance/documentation-protocol.md)
- [Stage authoring matrix](../governance/stage-authoring-matrix.md)
