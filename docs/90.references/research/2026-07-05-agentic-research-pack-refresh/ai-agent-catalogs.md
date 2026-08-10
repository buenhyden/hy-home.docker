---
status: active
artifact_id: reference:agentic-research:ai-agent-catalogs
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-07
---

<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/ai-agent-catalogs.md -->

# Reference: AI Agent Catalogs and Role-Based Agent Packs

## Overview

External catalogs can supply useful role taxonomies and prompt patterns, but
agent definitions are executable instructions once installed. This reference
uses the community `agency-agents` repository as a point-in-time comparison
with the small, governance-first catalog in `hy-home.docker`.

The current upstream comparison is pinned to commit
`8ef49232e02431f7ca4792b487e5a85a7939ff3a` (committed 2026-07-23) and was
retrieved read-only at `2026-08-07T12:45:48+09:00`. Nothing from that
repository was installed, converted, vendored, or executed.

## Purpose

Define an evidence-backed import boundary: external personas may inform
design, but adoption starts in Stage 00, receives narrow controls, and only
then becomes provider projections.

## Repository Role

This reference supports the Stage 00 catalog, subagent protocol, approval
boundaries, provider comparison, and future agent proposals. It changes no
agent, skill, model mapping, or runtime adapter. It owns catalog intake and
adaptation only; instruction authority, tools/permissions, generated-code
review, escalation, and vibe-coding criteria are canonical in
[`agent-instructions-vibe-coding.md`](./agent-instructions-vibe-coding.md).

## Scope

### In Scope

- Upstream catalog breadth, source format, conversion, and distribution
- Local catalog/projection implementation
- Portability, permissions, security, evidence, and evaluation risks

### Out of Scope

- Running upstream installers/converters
- Importing, renaming, or adding agents
- Endorsing upstream “production-ready” claims
- Changing provider settings or active model policy

## Definitions / Facts

- At the pinned commit, the 17 canonical divisions named by `divisions.json`
  contain 269 source agent-definition Markdown files. The Hermes builder reads
  that division registry and its generated README reports the same 269 count;
  the top-level README still displays the rounded and stale public total
  `230+`. These are repository inventory facts, not evidence that every
  definition is production-ready or suitable for this workspace.
- The 2026-08-07 revalidation re-opened the pinned commit and confirmed it still
  resolves with 269 agent definitions, 17 divisions, a 16-entry `tools.json`,
  and an MIT license. The pin's own commit message states "Hermes generated
  count 265 -> 269", and its generated roster reads "Generated agent count:
  269", so the figure is corroborated by upstream's own artifacts rather than
  by counting files. Upstream `main` moved to 270 in commit `c89557f7`
  (2026-07-30), whose message states "Hermes generated count 269 -> 270"; the
  latest commit at revalidation, `ebe9c99a` (2026-08-06), relocated one agent
  between sections without changing the count. That movement is a re-pin
  trigger under the update policy below, not a defect in the pinned analysis.
- The `230+` figure in the top-level README is still stale at upstream `main`
  and appears in exactly two places: a feature bullet reading
  "**230+ Specialized Agents** across every division" and a community paragraph
  reading "**230+ agents across every division**". Three different counts
  therefore coexist in one repository — 230+ in the README, 270 in the
  generated roster, and whatever the division directories currently hold — of
  which only the generated roster is machine-maintained.
- The upstream project is MIT-licensed and publishes persona-oriented Markdown
  definitions plus conversion/install paths for multiple tools.
- Its Codex converter maps source name/description/body into current minimal
  `name`, `description`, and `developer_instructions` TOML fields.
- Its Gemini CLI integration says it installs Markdown agents under
  `~/.gemini/agents/`. Official Gemini CLI documentation independently
  confirms user-level `~/.gemini/agents/*.md` and project-level
  `.gemini/agents/*.md` custom definitions with required `name`/`description`
  frontmatter and optional tool/MCP/model/run controls; public support was
  announced in v0.38.1 on 2026-04-16. This corroborates the upstream target,
  but does not mean the workspace's separate `.agents` projection adopts it.
- The upstream README calls the catalog “Production-Ready” and
  “battle-tested.” Those are publisher claims, not independent evaluation or
  workspace adoption evidence.
- The workspace catalog contains 14 roles (one workflow supervisor and
  thirteen workers) and 24 canonical functions. Stage 00 is canonical.
- `scripts/operations/sync-provider-surfaces.sh` renders strict Claude, Codex,
  and Gemini native role adapters plus shared `.agents` compatibility adapters
  and Claude/shared function skills from canonical sources; `--check` reports
  three providers and zero drift.
- The typed `capability_intake` registry records nine bounded upstream
  capability decisions, each with `source_retrieved_at: 2026-07-26`. Eleven
  fixtures and 16 synthetic regressions provide deterministic evaluation
  evidence; neither proves live-model acceptance.
- The pinned `tools.json` is upstream installation metadata, not workspace
  policy. It records Codex and Gemini CLI as per-agent render targets with
  user/project destinations, while the MIT license permits reuse subject to
  notice retention. The workspace imports neither the installer nor
  persona/voice text; any future adaptation must preserve attribution and pass
  the local intake, scope, security, evaluation, and review gates.

## Upstream Structure, Rules, and Implementation Approach

The comparison above treats `agency-agents` as a source of role names. Its more
transferable contribution is its build discipline, which is worth recording
precisely because parts of it resemble what this repository already does and
one part is a pattern this repository deliberately does not use. Everything
below was read read-only from the upstream tree on 2026-08-07; nothing was
installed, converted, or executed.

### Structure

The repository is organized as division directories at the top level, with two
JSON registries acting as sources of truth beside them.

| Criterion | Element                  | Upstream implementation                                                                                                                                                                                                                                         |
| --------- | ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AAS-01    | Division registry        | `divisions.json` maps 17 canonical divisions to a display label, a Lucide icon name, and a brand color. Its embedded `_note` states it is the "Source of truth for the agent division set".                                                                     |
| AAS-02    | Non-division directories | `integrations/`, `strategy/`, `examples/`, and `scripts/` are top-level directories that are explicitly _not_ divisions, excluded via `NON_DIVISION_DIRS`. `integrations/` holds conversion outputs, and `strategy/` holds playbooks with no agent frontmatter. |
| AAS-03    | Division admission rule  | "A division must contain at least one frontmatter agent file."                                                                                                                                                                                                  |
| AAS-04    | Tool registry            | `tools.json` carries 16 entries keyed by kebab CLI name, each with an install contract and app presentation metadata.                                                                                                                                           |
| AAS-05    | Registry-to-output skew  | `tools.json` lists `osaurus`, which has no `integrations/` directory; `integrations/` contains `mcp-memory`, which has no `tools.json` entry. The two 16-item sets are the same size but are not the same set.                                                  |
| AAS-06    | Generated roster         | `integrations/hermes/README.md` reports the machine-maintained agent count, currently 270.                                                                                                                                                                      |

### Rules

Three rules in the upstream registries are stated as build-breaking guards
rather than conventions, and each has a named CI script.

File names in the table below belong to the upstream `agency-agents`
repository, not to this workspace. Shell guards live in that repository's
`scripts/` directory and workflows in its `.github/workflows/` directory.
Paths written with a directory prefix elsewhere in this leaf refer to this
workspace.

| Criterion | Rule                                                                                                                                                                                     | Guard                                                   |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| AAR-01    | The division list must agree with the directories on disk, with the `AGENT_DIRS` arrays in `convert.sh` and `lint-agents.sh`, and with the path filters in `lint-agents.yml`.            | `check-divisions.sh`, CI workflow `check-divisions.yml` |
| AAR-02    | The tool list must agree with `ALL_TOOLS` in `install.sh` and the converter set in `convert.sh`, and every entry must carry `id`, `label`, `kebab`, `format`, `installKind`, and `dest`. | `check-tools.sh`                                        |
| AAR-03    | "the same `format` name guarantees byte-identical output, so two tools may share a format only if their rendered files are identical."                                                   | Enforced by the `format` contract itself                |
| AAR-04    | Adding a tool requires three coordinated edits: a `tools.json` entry, a `convert_<tool>` function or reused `format`, and an `install_<tool>` function.                                  | `check-tools.sh`                                        |

AAR-01 and AAR-02 are recognizably the same idea as this repository's
`scripts/validation/check-repo-contracts.sh` parity checks: a declarative
registry, a generator, and a check that fails when the two disagree. The
convergence is worth naming because it means the pattern is not
workspace-specific invention, and because it is the part of upstream most
defensible to learn from.

### Implementation approach

| Criterion | Concern                    | Upstream approach                                                                                                                                                                                                                                            | Workspace approach                                                                                                |
| --------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| AAI-01    | Install mechanism taxonomy | Three `installKind` values: `per-agent` (one rendered file or directory per agent), `roster` (one combined file for all agents), and `plugin` (a built artifact that is not per-agent renderable and is CLI-only).                                           | One mechanism only. Every role and function renders per-agent from Stage 00 into the tracked tree.                |
| AAI-02    | Install destination        | Writes into live provider directories at user or project scope. The Claude, Codex, and Gemini `dest` templates are `.claude/agents/{slug}.md`, `.codex/agents/{slug}.toml`, and `.gemini/agents/{slug}.md`, each listed for both `user` and `project` scope. | Renders only into the repository tree. No user-global write path exists.                                          |
| AAI-03    | Scale strategy             | The Hermes plugin keeps the full roster in `data/agents.json` on disk and never preloads it; four routing tools — `agency_agents_search`, `agency_agents_inspect`, `agency_agents_load`, and `agency_agents_delegate` — search and load lazily.              | Not applicable at 14 roles. All roles are directly addressable and none needs a retrieval layer.                  |
| AAI-04    | Detection                  | Each tool entry declares `detect.dirs` and a `version` command so the installer can discover which CLIs are present.                                                                                                                                         | No detection. The provider set is fixed by the typed contract.                                                    |
| AAI-05    | Update path                | The catalog is designed to be reinstalled as upstream grows; the app can auto-update.                                                                                                                                                                        | No upstream link exists after adaptation. Adoption is a one-time, reviewed copy of knowledge, not a subscription. |

AAI-03 is the most interesting divergence. A 270-role catalog needs a retrieval
layer because a roster that size cannot sit in context; a 14-role catalog does
not. That is a direct argument against importing breadth: every role added past
the point where the supervisor can hold the whole catalog in view converts a
routing decision into a search problem, and this workspace has no search layer
and no reason to build one.

AAI-02 is the most important risk. The exact `dest` templates confirm that the
upstream installer's normal mode of operation is to write agent definitions
directly into the same `.claude/agents/`, `.codex/agents/`, and
`.gemini/agents/` paths this repository generates and parity-checks. Running it
against this workspace would not merely add files; it would collide with
generated adapters that `scripts/operations/sync-provider-surfaces.sh` owns.
That is why the Direct-import risks row remains "Prohibited without separate
explicit approval" and why no upstream installer may be executed here.

## Capability-Family Gap Analysis

The comparison unit is a recurring capability family, not the number of
upstream names. Upstream evidence is limited to the pinned commit; the local
disposition is task-fit analysis and does not add or rename a role.

| Capability family         | Pinned `agency-agents` evidence                                                                                                                                                                 | Workspace coverage                                                                                                                                                                                                                                       | Gap / overlap                                                                                                                                  | Disposition                                                                                                                                                                         |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Product and specification | `Product Manager` owns discovery, PRDs, roadmaps, GTM, and outcomes; `Senior Project Manager` converts specs to tasks; `Workflow Architect` maps system paths before code.                      | `workflow-supervisor`, `doc-writer`, `rules-engineer`, and requirements/design/task skills cover orchestration and document mechanics, but no catalog role owns product discovery or outcome validation.                                                 | Product intent is a real capability gap; spec/task conversion overlaps existing skills and should not become another generic agent.            | Candidate: a bounded product/spec capability under the product scope, only after recurring demand and evaluation; merge spec conversion into existing roles/skills.                 |
| Performance               | `Performance Benchmarker` covers load/speed testing and optimization; `Infrastructure Maintainer` also names performance optimization.                                                          | `qa-engineer`, `iac-reviewer`, `drift-detector`, and infra validation skills cover correctness and drift, not a dedicated benchmark baseline/regression owner.                                                                                           | Performance evidence is under-specified; a broad new infra persona would overlap current ownership.                                            | First add benchmark/evidence capability to QA/infra workflow; propose a dedicated role only if workload and independent eval justify it.                                            |
| Reliability               | `SRE`, `Infrastructure Maintainer`, and `Incident Response Commander` span SLOs, observability, capacity, incidents, and postmortems.                                                           | `incident-responder`, `drift-detector`, `iac-reviewer`, `ci-cd-engineer`, and Stage 05 artifacts already split prevention, detection, delivery, and response.                                                                                            | Upstream SRE breadth would duplicate several canonical owners; SLO/capacity/chaos depth may remain a skill gap.                                | Merge missing reliability methods into existing roles/scopes; do not add an umbrella SRE role without an ownership redesign.                                                        |
| Release and deployment    | `DevOps Automator` covers CI/CD, deployment automation, cloud operations, and monitoring; `Reality Checker` covers production/release readiness.                                                | `ci-cd-engineer`, `qa-engineer`, deployment-pipeline skill, task review, and Stage 04/05 gates cover the family.                                                                                                                                         | Release certification and deployment execution must remain distinct from CI configuration and remote authority.                                | Merge readiness rubrics into existing QA/CI workflows; no new role now.                                                                                                             |
| Software supply chain     | The pinned `Supply Chain Strategist` is a business procurement/logistics role, while `Senior SecOps Engineer` and `Application Security Engineer` are closer to dependency/provenance controls. | `security-auditor`, `ci-cd-engineer`, security skills, workflow governance, and approval boundaries own software supply-chain checks.                                                                                                                    | Name matching would import the wrong domain; dependency provenance/release artifact review may still need sharper checklist coverage.          | Do not import the business supply-chain persona; merge software supply-chain checks into security/CI and evaluate a specialist only for demonstrated recurring gaps.                |
| Evaluation                | `Test Results Analyzer`, `Reality Checker`, `Experiment Tracker`, `Tool Evaluator`, and `Model QA Specialist` cover result analysis, readiness, experiments, tools, and model QA.               | `eval-engineer` owns repository semantic evaluation with 11 exact fixtures, 16 synthetic regressions, calibrated scorers, and exact thresholds; QA, review, and workflow roles consume that evidence. No live comparative model-quality baseline exists. | The bounded repository eval capability exists; multiple upstream names overlap, while live provider comparison remains an unadopted extension. | Consolidate upstream evaluation methods under `eval-engineer`; extend to live comparison only after dataset, privacy, entitlement, cost, runtime, scorer, and calibration approval. |
| Model routing             | `Autonomous Optimization Architect` explicitly covers LLM routing, cost optimization, and shadow testing; `Agents Orchestrator` covers multi-agent coordination.                                | `workflow-supervisor` routes work and `subagent-protocol.md` fixes provider model tiers/effort; no autonomous cost/quality router is adopted.                                                                                                            | Orchestration overlaps. Automatic routing would conflict with fixed policy and lacks cross-provider task evals.                                | Keep routing policy with the supervisor; treat shadow evaluation as a future eval capability and prohibit autonomous policy mutation.                                               |

## Catalog Comparison Matrix

| Catalog concern         | agency-agents pattern                                                                                                                                                                                | Workspace pattern                                                                                                                                                                                      | Importability                                 | Required wrapper/control                                                                                                        | Recommendation                                                                                        | Owner                                                   |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| Catalog breadth         | The immutable 2026-07-23 pin contains 269 source agent-definition Markdown files across the 17 canonical divisions; the generated Hermes roster agrees, while the top-level README still says `230+` | 14 repository-specific roles optimize for bounded recurring work                                                                                                                                       | Reference only                                | Candidate role must correspond to a demonstrated workspace gap and avoid duplicate ownership                                    | Use the pinned taxonomy for discovery; add no role without an approved Stage 00 proposal              | `docs/00.agent-governance/agents/README.md`             |
| Role boundaries         | Persona files emphasize identity, mission, workflows, deliverables, and voice; boundary precision varies by role                                                                                     | Each canonical role is tied to purpose, scope, model policy, delegation, and repository rules                                                                                                          | Adapt after review                            | Rewrite mission into explicit in-scope/out-of-scope and canonical-owner boundaries                                              | Import the job to be done, not the persona's assumed authority                                        | `docs/00.agent-governance/agents/README.md`             |
| Prompt portability      | Markdown bodies are copied or converted across many tool formats                                                                                                                                     | Provider adapters are projections of Stage 00 and shared Claude skill content where applicable                                                                                                         | Adapt after review                            | Normalize provider-required fields and remove tool-specific invocation assumptions                                              | Maintain one reviewed canonical role, then generate/test each adapter                                 | `scripts/operations/sync-provider-surfaces.sh`          |
| Scope imports           | Upstream personas may refer to generic projects, departments, files, or external systems                                                                                                             | Stage 00 scopes route work by repository surface and lifecycle owner                                                                                                                                   | Do not direct-import                          | Replace all generic scope text with tracked repo paths, stage owners, and explicit exclusions                                   | Reject any definition whose target scope cannot be expressed in the Stage 00 model                    | `docs/00.agent-governance/scopes/README.md`             |
| Tools and permissions   | Installer/converter targets provider-native agent directories; persona/tool assumptions may be broad                                                                                                 | Repository approvals and environment rules govern actions; local metadata is not an enforced allowlist                                                                                                 | Do not direct-import                          | Apply least privilege in the native provider schema and preserve repository approval boundaries                                 | Review every command, MCP, web, external-action, and protected-path request before adaptation         | `docs/00.agent-governance/rules/approval-boundaries.md` |
| Model tier              | Upstream roles are portable and do not centrally enforce this workspace's supervisor/worker mappings                                                                                                 | `subagent-protocol.md` assigns active provider tiers and reasoning settings                                                                                                                            | Adapt after review                            | Select model only through current policy and Task 2 evidence; validate projection parity                                        | Never preserve an upstream model assumption by default                                                | `docs/00.agent-governance/subagent-protocol.md`         |
| Lifecycle behavior      | Upstream distribution focuses on installing/invoking agent definitions across tools                                                                                                                  | Stage 00 task/review protocol, hooks, checklists, memory, and provider notes constrain lifecycle                                                                                                       | Reference only                                | Wrap the role with bootstrap, evidence, completion, and independent-review requirements                                         | Treat persona workflow prose as advisory until mapped to an owned repository loop                     | `docs/00.agent-governance/rules/agentic.md`             |
| Handoffs and delegation | Roles can be selected by name, but a shared repository-specific handoff contract is not established by the README                                                                                    | Supervisor/worker delegation and cross-role evidence are defined by the subagent protocol                                                                                                              | Adapt after review                            | Declare caller, deliverable, allowed files, base commit, evidence, and return path                                              | Use the existing supervisor protocol instead of importing a parallel orchestration model              | `docs/00.agent-governance/subagent-protocol.md`         |
| Evidence and provenance | Pinned Git history, Markdown sources, README, license, and converter code provide upstream provenance; per-agent outcome evidence varies                                                             | Task cards, diffs, checks, commits, review reports, and source ledgers provide adoption evidence                                                                                                       | Reference only until pinned                   | Pin upstream commit, record exact source file/license, retain review rationale, and never cite self-claims as independent proof | Require a source ledger and lifecycle artifact for any proposed adaptation                            | `docs/04.execution/tasks/README.md`                     |
| Security review         | Agent text and installation scripts are third-party instruction/code surfaces; direct global-directory installation changes runtime behavior                                                         | Security scope, approval boundaries, sandbox rules, and protected adapter surfaces constrain adoption                                                                                                  | Do not direct-import                          | Review prompt injection, secrets, external actions, commands, dependency/install behavior, and permission escalation            | Inspect offline at a pin; adapt manually; do not run upstream installers against provider directories | `docs/00.agent-governance/scopes/security.md`           |
| Evaluations             | Upstream maturity language is a publisher claim; no independent workspace benchmark follows from it                                                                                                  | `eval-engineer`, 11 exact fixtures, and 16 synthetic regressions provide repository-semantic evidence, but new-role or live-model quality still requires task-specific comparative acceptance evidence | Adapt only with evaluation                    | Define representative tasks, rubric/scorer, failure cases, comparative baseline, privacy boundary, and reviewer calibration     | Pilot a candidate role against existing generalist roles before catalog adoption                      | `docs/00.agent-governance/scopes/qa.md`                 |
| Direct-import risks     | Convert/install flows can write many definitions into user-global provider directories and later auto-update through the desktop app                                                                 | Tracked adapters are reviewable, generated in-repo, parity-checked, and subordinate to Stage 00                                                                                                        | Prohibited without separate explicit approval | No global install; no auto-update; pin source; narrow text/tools; generate locally; review diff; run repository contracts       | Use external catalogs as design references by default; propose one bounded role at a time             | `docs/00.agent-governance/rules/approval-boundaries.md` |

## Workspace Implementation Status

| Category                          | Current state                                                                                                                                                                  | External primary                                                                                             | Comparison                                                                                                                                                                   | Status      | Gap                                                                                  | Recommendation                                                                                                                                                    | Canonical owner                             | Evidence                                                                                                    | Confidence |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ---------- |
| Agent catalog and import boundary | Stage 00 owns 14 roles, 24 functions, four role-projection surfaces, and a typed nine-entry `capability_intake` registry; exact renderer and semantic-eval checks are tracked. | Pinned `agency-agents` repository, README, `tools.json`, license, and Codex/Gemini integration documentation | Upstream optimizes for catalog breadth and cross-tool installation; the workspace optimizes for bounded ownership, explicit merge/defer decisions, and reviewed projections. | Implemented | No live candidate-role acceptance benchmark or autonomous catalog import is adopted. | Keep reference-only as the default; route any new pinned candidate through the typed intake, security, QA, Stage 00 proposal, generation, and independent review. | `docs/00.agent-governance/agents/README.md` | Catalog/intake contracts; sync `--check`; `11/11` fixtures and `16/16` regressions; pinned upstream sources | High       |

## Corrections to Stale Claims

- **Confirmed 2026-08-07.** The pin still resolves at `8ef49232`, still reports
  269 generated agents, still declares 17 divisions, still carries a 16-entry
  `tools.json`, and is still MIT-licensed. The pinned analysis needs no
  revision.
- **Corrected 2026-08-07.** The upstream `230+` figure is not merely rounded
  and stale; it is contradicted by upstream's own generated roster at 270, and
  the gap has widened by one since the pin. Treat any headline count in a
  community catalog README as marketing copy unless a generated artifact
  restates it.
- **Added 2026-08-07.** The 16 `tools.json` entries and the 16 `integrations/`
  subdirectories are not the same set. `osaurus` appears only in the registry
  and `mcp-memory` only in the output tree. A future intake must not treat
  either count as a proxy for the other.
- **Added 2026-08-07.** The Codex converter's minimal `name` / `description` /
  `developer_instructions` mapping remains accurate against current Codex
  documentation, which still lists exactly those three as required and treats
  model, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, and
  `skills.config` as optional. An imported upstream definition would therefore
  arrive with no model, no effort, no sandbox, and no MCP constraint, and would
  inherit whatever the session provides. That is a concrete least-privilege gap
  in any direct conversion, not a hypothetical one.

## Repository Investigation Before Any Import

The Safe Adaptation Sequence below states the procedure. These are the
workspace-specific facts that determine whether the procedure can even start,
re-derived from the tracked tree on 2026-08-07.

1. **Where a role would land.** Stage 00 holds 14 role definitions under
   `docs/00.agent-governance/agents/agents/` and 24 function definitions under
   `docs/00.agent-governance/agents/functions/`. A new role means a fifteenth
   canonical file plus four generated adapters; a new function means a
   twenty-fifth plus two skill surfaces. The canonical file is written first
   and the adapters are never hand-authored.
2. **What the renderer would overwrite.** The four role surfaces currently hold
   14 adapters each: `.claude/agents/`, `.codex/agents/`, `.gemini/agents/`,
   and `.agents/agents/`. Any file placed in those directories by an external
   installer is drift that the next render removes.
3. **Which scope would own it.** The 14 files under
   `docs/00.agent-governance/scopes/` are the complete routing vocabulary:
   `agentic`, `architecture`, `backend`, `common`, `docs`, `entry`, `frontend`,
   `infra`, `meta`, `mobile`, `ops`, `product`, `qa`, and `security`. An
   upstream persona whose work does not map onto one of these has no owner
   here, which is the practical test behind the "Do not direct-import" verdict
   on Scope imports.
4. **What model policy it would inherit.** The five typed work profiles are the
   only permitted configurations. A candidate role must be assigned one of
   them; no upstream model, effort, or temperature assumption survives intake.
5. **What evidence would justify it.** The 11 fixtures and 16 synthetic
   regressions score repository semantics only. Nothing tracked establishes
   that a new specialist role outperforms an existing generalist, so the
   "Adapt only with evaluation" verdicts currently have no baseline to run
   against. Building one is a prerequisite, not a follow-up.

## Safe Adaptation Sequence

1. Identify a verified role gap and name the Stage 00 owner.
2. Pin the upstream commit, exact agent file, license, and retrieval date.
3. Read the prompt and any converter/installer code as untrusted third-party
   input; do not execute it or grant global-directory writes.
4. Extract only useful role knowledge. Remove provider assumptions, broad
   commands, external actions, secrets access, and conflicting instructions.
5. Define scope, exclusions, model tier, handoff contract, evidence, and
   evaluation cases in an approved lifecycle artifact.
6. Add the canonical Stage 00 role first, generate provider projections, and
   inspect native-schema compatibility.
7. Run sync parity and repository-contract checks, then obtain independent
   review. No upstream auto-update path remains after adoption.

## Importability Interpretation

- **Reference only**: useful for taxonomy or design, but not executable.
- **Adapt after review**: a small pattern may be rewritten into the canonical
  local contract after scoped security/governance review.
- **Adapt only with evaluation**: adoption also needs representative outcome
  evidence against an explicit baseline.
- **Do not direct-import / Prohibited without separate explicit approval**:
  never copy/install into active provider directories as an ordinary research
  step.

## Source Rules

- Pin external catalog claims to an immutable commit and prefer upstream
  repository files over secondary descriptions.
- Label publisher maturity claims as self-claims unless independent evidence
  exists.
- Verify workspace facts against Stage 00 and tracked generator/validator
  implementations. Repo-local contract facts retain their 2026-07-26 source
  date; the immutable upstream pin was separately retrieved on 2026-07-27.

## Sources

- [agency-agents pinned repository](https://github.com/msitarzewski/agency-agents/tree/8ef49232e02431f7ca4792b487e5a85a7939ff3a)
- [pinned README](https://github.com/msitarzewski/agency-agents/blob/8ef49232e02431f7ca4792b487e5a85a7939ff3a/README.md)
- [pinned canonical division registry](https://github.com/msitarzewski/agency-agents/blob/8ef49232e02431f7ca4792b487e5a85a7939ff3a/divisions.json)
- [pinned Hermes builder](https://github.com/msitarzewski/agency-agents/blob/8ef49232e02431f7ca4792b487e5a85a7939ff3a/scripts/build-hermes-plugin.py)
- [pinned generated Hermes roster](https://github.com/msitarzewski/agency-agents/blob/8ef49232e02431f7ca4792b487e5a85a7939ff3a/integrations/hermes/README.md)
- [pinned tool registry](https://github.com/msitarzewski/agency-agents/blob/8ef49232e02431f7ca4792b487e5a85a7939ff3a/tools.json)
- [pinned MIT license](https://github.com/msitarzewski/agency-agents/blob/8ef49232e02431f7ca4792b487e5a85a7939ff3a/LICENSE)
- [pinned Codex integration](https://github.com/msitarzewski/agency-agents/blob/8ef49232e02431f7ca4792b487e5a85a7939ff3a/integrations/codex/README.md)
- [pinned Gemini CLI integration](https://github.com/msitarzewski/agency-agents/blob/8ef49232e02431f7ca4792b487e5a85a7939ff3a/integrations/gemini-cli/README.md)
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents)
- [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Gemini CLI documentation](https://google-gemini.github.io/gemini-cli/docs/)
- [Gemini CLI subagents](https://github.com/google-gemini/gemini-cli/blob/main/docs/core/subagents.md)
- [Gemini CLI v0.38.1 subagent announcement](https://github.com/google-gemini/gemini-cli/discussions/25562)
- [Agent catalog](../../../00.agent-governance/agents/README.md)
- [Subagent protocol](../../../00.agent-governance/subagent-protocol.md)
- [Approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md)
- [upstream `main` at revalidation](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7) - the mutable head observed 2026-08-07, carrying 270 generated agents and the unchanged `230+` README figure
- [upstream 269-to-270 commit](https://github.com/msitarzewski/agency-agents/commit/c89557f78509868c6d4cc08e5cbc79bc8625fe1c) - dated 2026-07-30, the commit whose message records the count change
- [Repository contract check](../../../../scripts/validation/check-repo-contracts.sh)
- [Provider surface sync](../../../../scripts/operations/sync-provider-surfaces.sh)

Upstream evidence in this document was retrieved read-only through the GitHub
API on 2026-08-07. Both the immutable pin and the mutable head were read; the
pin remains the analytic basis and the head is recorded only to date the
re-pin trigger. No upstream installer, converter, or build script was executed,
and no upstream file was copied into this repository. Workspace counts were
re-derived from the tracked tree on the same date.

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Recheck on any proposed import or material upstream/local
  catalog change
- **Update Trigger**: Upstream count/schema/license changes, local catalog
  changes, or new provider adapter behavior

## Related Documents

- [research pack index](./README.md)
- [provider implementation comparison](./provider-implementation-comparison.md)
- [harness engineering](./harness-engineering.md)
- [workspace baseline](./workspace-baseline.md)
- [agent instructions and safe vibe coding](./agent-instructions-vibe-coding.md)
- [subagent protocol](../../../00.agent-governance/subagent-protocol.md)
