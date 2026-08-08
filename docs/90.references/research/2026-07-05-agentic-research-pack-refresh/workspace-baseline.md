---
status: active
artifact_id: reference:agentic-research:workspace-baseline
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-07
review_cycle: on-source-change
---

<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md -->

# Reference: Agentic Engineering Workspace Baseline

## Overview

This reference compares the current tracked `hy-home.docker` workspace with
primary external SDLC, automation, and document-role sources. It covers 27
requested categories using one comparison vocabulary and keeps repo-local
implementation status separate from external practice.

## Purpose

Provide a source-backed workspace baseline for later research-pack tasks without
turning external guidance into adopted policy or treating an advisory knowledge
graph as repository truth.

## Repository Role

This Stage 90 reference supports Stage 00 governance and the active Stage 01-05
lifecycle. It does not replace policy, specifications, plans, task evidence,
operations procedures, runtime Compose files, CI workflows, or provider/model
configuration.

## Scope

### In Scope

- Workspace purpose, structure, roles, rules, and lifecycle
- Documentation, automation, CI, QA, security, and infrastructure surfaces
- Agent, harness, loop, and task-characteristic model-selection baselines
- External comparison and clearly assigned follow-up ownership

### Out of Scope

- Active policy, runtime, workflow, template, script, or provider changes
- Formal adoption of ISO, NIST, GitHub Spec Kit, SRE, or other external practice
- Repeating the completed provider/model, harness/loop/catalog, QA/automation,
  Compose, or security comparison bodies that are linked from this baseline
- Implementing any residual gap identified by those specialized references

## Definitions / Facts

- **Workspace evidence** means current state corroborated by tracked files and
  active stage documents. Graphify was built from `30df271a` while this task
  started from `cf8790ca`; its report was navigation-only and is not evidence
  for any row below.
- **External evidence** is a comparison lens. A cited practice is not adopted
  workspace policy unless a tracked active policy or stage artifact says so.
- **Status** uses exactly four values: `Implemented` (the tracked workspace has
  the category contract and evidence), `Partially Implemented` (some contract,
  coverage, or verification remains), `Missing` (no tracked implementation),
  and `Not Applicable` (the category does not apply).
- **Canonical owner** is the first tracked surface that owns a future change;
  downstream documents should link to it rather than duplicate it.
- **Confidence** is `High`, `Medium`, or `Low` based on source directness,
  currentness, and coverage. It does not express approval.
- **Current agentic cardinality** is 14 roles, 24 functions, five exact work
  profiles, 11 model records, eight harness layers, eight ordered workflow
  states, nine capability-intake decisions, 11 synthetic fixtures, and 16
  deterministic regressions. The model policy has no active fallback graph or
  implicit substitution.

## Workspace Category Map

| Category                            | Workspace evidence                                                                                                                                                                                                                                                                                                                                                                                        | External evidence                                                                                                                                                                                                         | Status                                      | Gap / risk                                                                                                                                                                                                           | Recommendation                                                                                                                                                                  | Canonical owner                                                                                         | Confidence                   |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ---------------------------- |
| purpose                             | `README.md` defines a shared harness-engineering and agent-first Docker Compose workspace with staged documentation.                                                                                                                                                                                                                                                                                      | GitHub Spec Kit similarly starts from an explicit specification before implementation; ISO 12207 supplies lifecycle framing, but the cited 2017 edition is now withdrawn.                                                 | Implemented                                 | Purpose could be overstated if references are mistaken for runtime truth.                                                                                                                                            | Keep the root README authoritative and references advisory.                                                                                                                     | `README.md`                                                                                             | High                         |
| overview                            | `README.md`, `docs/README.md`, `infra/README.md`, and `scripts/README.md` provide tracked entry maps for the workspace.                                                                                                                                                                                                                                                                                   | GitHub Spec Kit publishes a current workflow overview whose artifacts feed the next phase.                                                                                                                                | Implemented                                 | Secondary entry-point READMEs can drift from the root map.                                                                                                                                                           | Keep the root map authoritative and retain README sync plus repository-contract validation.                                                                                     | `README.md`                                                                                             | High                         |
| roles                               | Stage 00 persona, scope, agent catalog, subagent protocol, and stage matrix assign authoring and execution ownership.                                                                                                                                                                                                                                                                                     | ISO 42010 frames architecture stakeholders/concerns; Google SRE separates incident command, operations, and communications roles.                                                                                         | Implemented                                 | Provider adapters can drift from the canonical catalog.                                                                                                                                                              | Keep the Stage 00 catalog authoritative and validate adapter parity as downstream evidence.                                                                                     | `docs/00.agent-governance/agents/README.md`                                                             | High                         |
| CI                                  | Seven tracked GitHub Actions workflows define 23 jobs; `ci-quality.yml` owns 16 independent quality jobs, with no inter-job `needs:` chain. The 2026-07-26 public remote observation saw 15 jobs in a failed run and left root cause and authenticated control-plane state unverified.                                                                                                                    | GitHub defines workflows as event-triggered YAML automation composed of jobs and steps, documents run monitoring/logs, and separates ruleset enforcement.                                                                 | Partially Implemented                       | Tracked YAML proves definitions; public run metadata proves neither root cause nor authenticated required-check/ruleset/environment state.                                                                           | Cite tracked jobs, observed runs, and control-plane readback as separate evidence classes before a merge-readiness claim.                                                       | `docs/00.agent-governance/rules/github-governance.md`                                                   | High                         |
| CD / deployment promotion           | No tracked workflow job references a GitHub deployment environment or performs application/infrastructure deployment; Stage 05 release readiness remains manual and approval-gated.                                                                                                                                                                                                                       | GitHub environments can restrict deployment branches, withhold environment secrets, and require reviewer or custom protection-rule approval before a job proceeds.                                                        | Missing                                     | CI success is not CD; no tracked promotion, environment approval, deployment record, or automated rollback path exists.                                                                                              | Route a later deployment/release specification through Stage 03/04 before workflow or runtime implementation.                                                                   | `docs/03.specs/README.md`                                                                               | High                         |
| release records                     | A Stage 05 Release profile, template, selection route, and index now exist; `CHANGELOG.md`, the release-management runbook, and tag-triggered coverage check remain adjacent inputs. No Release event leaf or GitHub Release is created by those contracts.                                                                                                                                               | GitHub Releases package a tagged software iteration with release notes and optional binary assets; GitHub deployment history records a different execution evidence class.                                                | Partially Implemented                       | Contract readiness is not an executed Release, signed artifact, deployment record, or rollback execution.                                                                                                            | Create a Release leaf only for a real event and keep deployment runtime/evidence in its separately approved chain.                                                              | `docs/05.operations/releases/README.md`                                                                 | High                         |
| QA                                  | QA scope and validation/hardening scripts separate local, CI-only, hook, and skipped-check evidence.                                                                                                                                                                                                                                                                                                      | NIST SSDF v1.1 supplies high-level verification and vulnerability-reduction practices; Spec Kit supplies checklists and cross-artifact analysis.                                                                          | Implemented                                 | External quality practices do not prove which repo-local gate applies to a change.                                                                                                                                   | Preserve change-type gate selection and skipped-check rationale in the QA scope; keep formal framework mapping in the separate security row.                                    | `docs/00.agent-governance/scopes/qa.md`                                                                 | High                         |
| formatting                          | Stage 00 Common scope defines repository-configured formatting; `.pre-commit-config.yaml`, hook validation, templates, and `git diff --check` are implementation evidence.                                                                                                                                                                                                                                | GitHub Actions can automate repeatable jobs; Spec Kit uses structured Markdown artifacts and templates. Neither source mandates this workspace's formatter set.                                                           | Implemented                                 | Tool-specific formatting coverage varies by surface.                                                                                                                                                                 | Change the formatting contract at the Common scope first and keep tool claims tied to tracked implementation.                                                                   | `docs/00.agent-governance/scopes/common.md`                                                             | High                         |
| linting                             | QA scope classifies local and CI evidence; pre-commit, shell/Markdown checks, frontend lint, and zizmor are tracked implementations.                                                                                                                                                                                                                                                                      | GitHub workflow syntax supports separate jobs/steps; NIST SSDF supports integrating verification into the SDLC without prescribing these linters.                                                                         | Implemented                                 | A passing local subset does not prove CI-only lint results.                                                                                                                                                          | Keep implementation commands in evidence and classify each gate in the QA contract.                                                                                             | `docs/00.agent-governance/scopes/qa.md`                                                                 | High                         |
| syntax/type checks                  | QA scope owns gate classification; repository contracts validate workflow YAML, Compose validation resolves configuration, and frontend quality runs lint/typecheck/build.                                                                                                                                                                                                                                | GitHub documents workflow YAML structure and job/step keys; Spec Kit calls for phase artifacts and quality checks.                                                                                                        | Partially Implemented                       | Type checking is implementation-specific and not universal across every repository surface.                                                                                                                          | Define the applicable check and skipped-check rationale in the QA contract; keep Stage 03 and CI artifacts as downstream evidence.                                              | `docs/00.agent-governance/scopes/qa.md`                                                                 | High                         |
| automation                          | `scripts/README.md` owns local purpose-folder entry points; hooks, provider adapters, and CI workflows consume or orchestrate them.                                                                                                                                                                                                                                                                       | GitHub Actions defines event-triggered configurable automation; Spec Kit provides an artifact-producing SDD workflow.                                                                                                     | Implemented                                 | Local automation ownership can blur when consumers are cited as canonical implementations.                                                                                                                           | Keep the script inventory authoritative for local automation and treat hook/provider/CI surfaces as downstream evidence.                                                        | `scripts/README.md`                                                                                     | High                         |
| pipeline                            | `ci-quality.yml` defines independent quality jobs; because no job declares `needs:`, GitHub runs them in parallel by default. Separately, `generate-changelog.yml` runs the changelog check for release tags.                                                                                                                                                                                             | GitHub workflow syntax provides triggers, jobs, dependencies, matrices, permissions, and steps as pipeline primitives.                                                                                                    | Implemented                                 | Remote enforcement and deployment pipelines are outside tracked local proof.                                                                                                                                         | Keep workflow YAML as implementation evidence and route enforcement assertions through the GitHub governance contract.                                                          | `docs/00.agent-governance/rules/github-governance.md`                                                   | High                         |
| workflow                            | Stage 00 workflow rules define provider-neutral orchestration; the stage matrix, GitHub workflows, and provider adapters are distinct downstream evidence surfaces.                                                                                                                                                                                                                                       | GitHub Spec Kit uses Spec → Plan → Tasks → Implement; GitHub Actions models automated workflows as YAML jobs and steps.                                                                                                   | Implemented                                 | “Workflow” can ambiguously mean lifecycle, CI, or provider automation.                                                                                                                                               | Define the workflow class in the Stage 00 workflow rule and cite only the applicable downstream implementation.                                                                 | `docs/00.agent-governance/rules/workflows.md`                                                           | High                         |
| operating contracts                 | The Stage 05 README routes HAFE guides, policies, runbooks, and incidents; Stage 00 rules and templates supply upstream/downstream evidence.                                                                                                                                                                                                                                                              | PagerDuty distinguishes detailed repeatable runbook steps; Google SRE separates live incident state and postmortem learning.                                                                                              | Implemented                                 | External practices may be accidentally restated as policy.                                                                                                                                                           | Route each approved operational change through the Stage 05 document-type owner before updating consumers.                                                                      | `docs/05.operations/README.md`                                                                          | High                         |
| templates                           | `docs/99.templates/README.md` maps canonical templates to every active stage and supporting contract, including the Release event template and typed Spec children.                                                                                                                                                                                                                                       | GitHub Spec Kit uses rich templates and phase-specific Markdown artifacts.                                                                                                                                                | Implemented                                 | A copyable form can be mistaken for proof that its target event or runtime exists.                                                                                                                                   | Keep template/profile instantiation validated and require target-specific evidence before creating a document.                                                                  | `docs/99.templates/README.md`                                                                           | High                         |
| scripts                             | `scripts/README.md` makes purpose-folder scripts canonical and prohibits duplicate root wrappers.                                                                                                                                                                                                                                                                                                         | GitHub Actions permits scripts within steps; Spec Kit provides CLI-driven workflow automation. These are comparisons, not script policy.                                                                                  | Implemented                                 | Docs can retain stale script paths after moves.                                                                                                                                                                      | Update the script inventory first and continue script-reference integrity checks.                                                                                               | `scripts/README.md`                                                                                     | High                         |
| integration guides                  | The Stage 05 guide index routes onboarding, HAFE guidance, and service integration docs to policy/runbook consumers.                                                                                                                                                                                                                                                                                      | GitHub Spec Kit's official walkthrough links workflow phases; PagerDuty explains how repeatable guidance becomes an operational runbook.                                                                                  | Implemented                                 | Guides can drift into policy or recovery procedure.                                                                                                                                                                  | Keep usage context in the guide category and link approved controls/procedures downstream.                                                                                      | `docs/05.operations/guides/README.md`                                                                   | High                         |
| SDLC                                | Stage 01 requirements → Stage 02 architecture → Stage 03 specs → Stage 04 execution → Stage 05 operations, with Stage 90/99 support; the registry and separated human contracts now distinguish SDLC/common/README ownership.                                                                                                                                                                             | Spec Kit uses Spec → Plan → Tasks → Implement; ISO 29148 and 42010 frame requirements and architecture; Diataxis informs content-purpose separation; withdrawn ISO 12207:2017 remains historical lifecycle metadata only. | Implemented                                 | The workspace has a richer pre-spec intent/design chain and operations feedback than external tool/content models.                                                                                                   | Keep the repo-local stage matrix and registry binding and external flows comparative.                                                                                           | `docs/00.agent-governance/rules/stage-authoring-matrix.md`                                              | High                         |
| governance                          | The Stage 00 hub routes bootstrap, persona, scopes, provider overlays, catalog, memory, and approval boundaries.                                                                                                                                                                                                                                                                                          | Spec Kit describes a project constitution; NIST SSDF provides high-level organizational secure-development practices.                                                                                                     | Implemented                                 | External “constitution” or SSDF language could be mistaken for adopted governance.                                                                                                                                   | Route a proposed governance change through the Stage 00 hub before changing a specialized rule or adapter.                                                                      | `docs/00.agent-governance/README.md`                                                                    | High                         |
| system structure                    | The root README owns the repository map; `docker-compose.yml`, `infra/README.md`, docs, scripts, secrets, projects, tests, and provider surfaces supply tracked implementation evidence.                                                                                                                                                                                                                  | ISO 42010 supports explicit architecture descriptions and stakeholder concerns; its public page is metadata, not the full standard.                                                                                       | Implemented                                 | The root map may lag implementation inventories.                                                                                                                                                                     | Update the root map first and corroborate it against tracked Compose, infra, docs, and script evidence.                                                                         | `README.md`                                                                                             | High                         |
| rules                               | Stage 00 bootstrap, agentic, documentation, task-checklist, GitHub, and scope rules define deterministic execution boundaries; provider files are adapters.                                                                                                                                                                                                                                               | Spec Kit's constitution illustrates stable cross-phase principles; NIST SSDF illustrates practice-level secure-development guidance.                                                                                      | Implemented                                 | Duplicate provider-local rules can conflict with the canonical adapter model.                                                                                                                                        | Apply the provider-neutral instruction hierarchy before changing any provider adapter.                                                                                          | `docs/00.agent-governance/providers/agents-md.md`                                                       | High                         |
| security                            | Security scope owns enforcement boundaries; secret handling, workflow controls, template baseline, hardening checks, and disclosure guidance are downstream implementation evidence.                                                                                                                                                                                                                      | NIST SSDF v1.1 recommends integrating secure practices into any SDLC; NIST SP 800-61 Rev. 3 frames incident response within CSF 2.0.                                                                                      | Partially Implemented                       | No formal SSDF mapping is adopted; remote-enforcement uncertainty is owned by the CI row.                                                                                                                            | Route any framework mapping through an approved security-scope change before downstream policy/spec work.                                                                       | `docs/00.agent-governance/scopes/security.md`                                                           | High                         |
| Docker Compose/infrastructure       | Root `docker-compose.yml` and tiered `infra/` remain runtime truth; the completed [Compose comparison](./docker-compose-infrastructure.md) and [security comparison](./security-governance.md) provide the recomputed topology, validation, hardening, and control evidence.                                                                                                                              | Current official Docker guidance covers includes, profiles, networking, secrets, dependencies, production, and trusted-input review.                                                                                      | Partially Implemented                       | Live service/port/volume/health evidence, external-network existence and ACLs, a production-overlay contract, and current backup/restore proof remain unestablished.                                                 | Keep static reference evidence separate from approved runtime preflight, production design, and Stage 05 backup/restore evidence.                                               | `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md` | High                         |
| AI agents                           | Stage 00 owns 14 roles (one supervisor and thirteen workers), 24 functions, and a typed nine-entry external capability-intake ledger. Four role surfaces each contain 14 adapters; function skills project to Claude and shared `.agents` only.                                                                                                                                                           | The pinned `agency-agents` repository and official provider agent schemas show broader catalog and native-agent patterns without proving workspace suitability.                                                           | Implemented for canonical intake/projection | Live provider acceptance and live comparative role/model evaluation remain absent.                                                                                                                                   | Retain merge/defer decisions, source/license provenance, generated-only adapters, 11-fixture/16-regression synthetic evaluation, and independent review for future candidates.  | `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/ai-agent-catalogs.md`             | High for tracked definitions |
| harness engineering                 | The completed [harness matrix](./harness-engineering.md) and [provider comparison](./provider-implementation-comparison.md) map typed Stage 00 contracts, strict native adapters, scripts, hooks, CI/local routing, evidence, and synthetic evaluation.                                                                                                                                                   | Official Claude, Codex, and Gemini sources establish native agents, hooks, sandbox/approval, context, and checkpoint surfaces without establishing cross-provider parity.                                                 | Partially Implemented                       | Tracked schemas and drift checks are current; live native acceptance, complete interception, entitlement, and global sandbox/MCP state remain unverified.                                                            | Validate live compatibility separately from deterministic projection parity.                                                                                                    | `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md`           | High for tracked definitions |
| loop engineering                    | The completed [loop matrix](./loop-engineering.md) links typed retry/stop, calibrated synthetic evaluation, action, validation, CI, memory, review, approval, automation, incident, and human-feedback loops.                                                                                                                                                                                             | ReAct and Reflexion supply research foundations; official provider, CI, eval, and checkpoint sources establish mechanisms rather than workspace enforcement.                                                              | Partially Implemented                       | Live provider parity, current remote-enforcement proof, uniform cross-provider checkpoint/resume, live model comparison, and tested service recovery remain incomplete.                                              | Route each gap through its listed active owner and keep loop research descriptive rather than encoding new runtime authority.                                                   | `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md`              | High                         |
| task-characteristic model selection | The typed policy implements five exact profiles: adversarial review and long-horizon supervision use Opus 5 / Sol / Gemini 3.6; complex implementation uses Sonnet 5 / Sol / Gemini 3.6; evidence research uses Sonnet 5 / Terra / Gemini 3.5 Flash-Lite; routine validation uses Haiku 4.5 / Terra / Gemini 3.5 Flash-Lite. The historical landscape remains 145 structural / 142 cutoff-qualified rows. | Current official provider catalogs and capability sources establish IDs, lifecycles, and provider-native controls, not product acceptance, entitlement, or benchmark parity.                                              | Partially Implemented                       | Current selected models are stable in the contract, but runtime acceptance/entitlement and cross-provider task-quality/latency/cost equivalence remain unproven; historical GPT-5.6 cutoff state is a separate axis. | Preserve exact values, no-substitution policy, and typed evidence states; require a separate approved live-evaluation/runtime task before claiming availability or equivalence. | `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/agent-model-selection.md`         | High for tracked policy      |

## Measured Provider Surface Baseline

Every figure in this section was counted from tracked files at commit
`82fc20dafc86b80393352ce53c86efb29748722a`, measured at
`2026-08-07T17:39:18+09:00`. These are measurements of what the workspace
currently contains, not assertions about what a provider runtime accepts.

### Surface file counts

| Surface    | Files | Composition                                                                                                            |
| ---------- | ----: | ---------------------------------------------------------------------------------------------------------------------- |
| `.claude/` |    49 | 1 directory `CLAUDE.md`, 14 agents, 24 skills, 7 hook wrappers, 1 output style, `settings.json`, `settings.local.json` |
| `.codex/`  |    16 | 1 `README.md`, 14 agent TOMLs, `hooks.json`                                                                            |
| `.gemini/` |    17 | 1 `README.md`, 14 agents, 1 hook wrapper, `settings.json`                                                              |
| `.agents/` |    41 | 1 `README.md`, 14 agents, 24 skills, `rules/workspace.md`, `workflows/documentation.md`                                |

The 14-role catalog is projected to four surfaces, so the role count is
identical everywhere. The 24-function skill catalog reaches only two surfaces,
`.claude/skills/` and `.agents/skills/`. Neither `.codex/` nor `.gemini/`
carries a skill body.

### Instruction entry points

| File        | Lines | Bytes | Auto-expanding                                            |        Auto-loaded body |
| ----------- | ----: | ----: | --------------------------------------------------------- | ----------------------: |
| `CLAUDE.md` |     8 |   205 | Yes, four `@path` imports at depth 1                      | 24,597 B across 5 files |
| `AGENTS.md` |     7 |   243 | No; the same four files are named as numbered prose steps |                   243 B |
| `GEMINI.md` |     8 |   213 | Yes, four `@./path` imports at depth 1                    | 23,063 B across 5 files |

The Claude and Gemini chains resolve `rules/bootstrap.md` (4,203 B),
`providers/<provider>.md` (6,771 B for Claude), `memory/README.md` (5,675 B),
and `memory/current.md` (7,743 B). None of those four files contains a further
`@path` import, so the chain is one hop deep against a documented Claude limit
of four hops. `memory/current.md` is 134 lines and 7,743 B against its own
declared bound of 400 lines and 32 KiB.

The asymmetry is the load-bearing fact: a Claude or Gemini session receives
about 24 KiB of governance automatically, while a Codex session receives 243 B
and must be trusted to read the remaining four files with tools.

### Typed contract cardinality

`docs/00.agent-governance/contracts/agent-catalog.yaml` holds 4 projection
targets, 8 scopes, 2 permission sets, 14 agents, 24 functions, and 9
capability-intake decisions. `contracts/provider-models.yaml` holds 3 providers,
1 compatibility surface, 5 work profiles, 11 models, 8 harness layers, 8
workflow states, 4 harness loops, and 7 semantic events. These match the
cardinality already recorded under Definitions / Facts above.

### Lifecycle event coverage

| Provider | Native events wired | Bound to the shared dispatcher                          | Gap                  |
| -------- | ------------------: | ------------------------------------------------------- | -------------------- |
| Claude   |                   7 | Indirectly, through 7 wrappers in `.claude/hooks/`      | none                 |
| Gemini   |                   7 | Indirectly, through `.gemini/hooks/agent-event-hook.sh` | none                 |
| Codex    |                   6 | Directly, inline in `.codex/hooks.json`                 | `SessionEnd` unwired |

All three route to `scripts/hooks/agent-event-hook.sh`, which is 673 lines and
holds the only blocking logic in the system: a template stop gate and a logical
commit stop gate, both of which inspect `stop_hook_active` before re-blocking.
Claude and Gemini reach it through a per-provider wrapper file; Codex embeds the
dispatcher invocation directly in its hook JSON. Tracked Claude timeouts range
from 10 to 30 seconds; every tracked Codex timeout is 600 seconds.

### Surfaces that do not exist

- No `.codex/config.toml`. Codex therefore runs on default values for every
  configurable key here, including `project_doc_max_bytes` and
  `project_doc_fallback_filenames`, and the repository has no tracked way to
  point Codex at `CLAUDE.md` or to raise the instruction size ceiling.
- No `.claude/rules/`. Path-scoped instruction loading is unused, so every byte
  of the 24 KiB chain loads for every session regardless of the task.
- No nested `AGENTS.md`. Directory-scoped Codex instructions are unused, so the
  root shim is the only Codex instruction file in the repository.
- No skill attachment on any Codex or Gemini role. All 14 Claude adapters
  declare a `skills` list; 0 of 14 Codex adapters declare `skills.config`.

### Local quality gate

`.pre-commit-config.yaml` declares 24 hooks across 10 repositories: 9 from
`pre-commit-hooks`, plus `yamllint`, `markdownlint-cli2`, `shellcheck`,
`actionlint`, `check-dependabot`, `hadolint-docker`, `gitleaks`, `commitizen`,
and 7 local hooks (`eslint-nextjs`, `docker-compose-check`,
`check-repo-contracts`, `check-document-metadata`, `check-doc-traceability`,
`check-quickwin-baseline`, `check-template-security-baseline`). No hook in this
set validates provider adapter parity directly; that check lives in the
repository-contract script rather than in a dedicated gate.

## Reaching a Common Claude/Codex System in This Workspace

The provider comparison establishes which elements can be shared and which are
structurally provider-native. This section records what would have to be
investigated or changed here, in dependency order. Nothing below is adopted
policy; each item names the canonical owner that would own the change.

| #   | Investigation or change                                         | Why it is needed                                                                                                                                                                                    | Canonical owner                                           | Blocking dependency                                                                                                            |
| --- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| 1   | Establish whether this project is marked trusted for Codex      | Codex skips project-scoped `.codex/` layers, including config, hooks, and rules, for an untrusted project. If untrusted, all 16 tracked Codex files are inert and every parity claim below is moot  | `docs/00.agent-governance/providers/codex.md`             | Requires a runtime observation, which is outside static evidence                                                               |
| 2   | Correct the two adapter-contradicting policy statements         | `providers/claude.md:31-32` and `providers/gemini.md:59-60` describe values their own generated adapters do not emit. Prose that disagrees with its generator is a false authority surface          | `docs/00.agent-governance/providers/`                     | None; both corrected states are already derived                                                                                |
| 3   | Decide the shared-instruction direction                         | Two documented methods exist and they are mutually exclusive in practice: a `CLAUDE.md` that imports `@AGENTS.md`, or a `.codex/config.toml` adding `CLAUDE.md` to `project_doc_fallback_filenames` | `docs/00.agent-governance/providers/agents-md.md`         | Depends on item 1 if the Codex-side method is chosen                                                                           |
| 4   | Size the shared instruction body to the Codex ceiling           | Codex stops adding files at 32 KiB across the concatenated set; the current Claude chain is already 24,597 B. A shared body has roughly 7 KiB of headroom before Codex silently truncates           | `docs/00.agent-governance/rules/bootstrap.md`             | Depends on item 3                                                                                                              |
| 5   | Reconcile the `session-end` contract record with upstream Codex | `contracts/provider-models.yaml` records the Codex binding as `unsupported` with a null native event, but Codex documents `SessionEnd` today. This is a stale repository record                     | `docs/00.agent-governance/contracts/provider-models.yaml` | The 1-second default and 3-second ceiling on Codex `SessionEnd` must be measured against the dispatcher's actual runtime first |
| 6   | Decide whether Codex roles should carry skills                  | 24 function bodies are projected to `.agents/skills/` but no Codex role references them through `[[skills.config]]`, so the shared function catalog is inert on Codex                               | `docs/00.agent-governance/agents/README.md`               | No official Codex skills page could be retrieved, so the discovery-path assumption in the contract is unverified               |
| 7   | Consider `.claude/rules/` for path-scoped loading               | The full 24 KiB chain loads for every Claude session regardless of task. Path scoping is Claude-only, so adopting it deliberately widens the Claude/Codex gap in exchange for context efficiency    | `docs/00.agent-governance/providers/claude.md`            | Depends on item 4, since moving content out of the chain changes the shared-body size calculation                              |
| 8   | Decide whether instruction loading should be observable         | Claude documents an `InstructionsLoaded` event that would prove which governance files actually reached a session. Codex documents no equivalent, so this can verify only one side                  | `docs/00.agent-governance/rules/hooks/`                   | None, but it produces one-sided evidence by construction                                                                       |

Items 1 and 2 are prerequisites for the rest: without the trust answer no Codex
parity claim is verifiable, and until the contradicting prose is corrected the
tracked policy misdescribes its own generated output. Items 3 and 4 are one
decision with two halves, because choosing a direction fixes the size ceiling
that applies. Items 5 through 8 are independent of each other.

The honest summary of current status is narrower than the adapter counts
suggest. Role definition, model and effort selection, and lifecycle dispatch are
genuinely common: one Stage 00 catalog, one typed contract, and one shell
dispatcher serve all three providers. Instruction delivery is not common, is not
currently normalizable without a decision, and is the layer where a Codex
session and a Claude session in this repository see the most different worlds.

## Analysis

All 27 requested categories have a current tracked state, an external comparison
or an explicit external-source limitation, a status, a gap, a recommendation,
one canonical owner, and a confidence judgment. The dominant pattern is a
multi-surface workspace: active stages own decisions and evidence, runtime files
own execution truth, and Stage 90 explains rather than governs.

Completed specialized evidence now resides in the
[provider](./provider-implementation-comparison.md),
[harness](./harness-engineering.md), [loop](./loop-engineering.md),
[catalog](./ai-agent-catalogs.md), [QA](./quality-ci-formatting.md),
[automation](./automation-pipeline-workflow.md),
[Compose](./docker-compose-infrastructure.md), and
[security](./security-governance.md) references. Those documents close the
former Tasks 2-5 research assignments while preserving three evidence
boundaries: tracked files do not prove live/runtime or remote enforcement,
provider catalogs do not prove entitlement or cross-provider parity, and
external frameworks do not become adopted policy through Stage 90.

## Application Notes for This Workspace

- Start repo-local claims from tracked root/stage files, then use Graphify only
  for navigation.
- State whether “workflow” means documentation lifecycle, CI automation, or a
  provider runtime adapter.
- Treat external sources as comparisons until an approved active artifact adopts
  a practice.
- Route a discovered gap to one canonical owner before linking downstream work.
- Treat README files as routing/local context and add metadata only for a
  declared profile consumer; keep complete semantics in the registry.

## Potential Follow-up / Gap

- Compose follow-up: gather approved live/external-network evidence, decide
  whether a production overlay is required, and record current backup/restore
  proof through the owners named in the Compose reference.
- Release/deployment follow-up: use the implemented Release contract only for
  real event evidence, then separately define artifact integrity, promotion
  stages, environment approvals, deployment history, and rollback/recovery
  without presenting CI and tag coverage as CD.
- Provider/catalog follow-up: retain strict native schemas and the governed
  capability-intake ledger, then verify live provider acceptance only under a
  separately approved runtime-observation task.
- Loop follow-up: retain synthetic eval evidence, separately design any live
  comparative evaluation, reverify remote enforcement, normalize
  checkpoint/resume evidence, and test service recovery through each row's
  active owner.
- Model follow-up: preserve the typed cutoff/retrieval/entitlement boundaries
  and establish representative live cross-provider evaluation before claiming
  task equivalence.

## Source Rules

- Repo-local claims use tracked files and active stage documents at baseline
  `ab3a047511c2bf9b5a95ebac737f3ebdb5589384`.
- External sources were retrieved and revalidated by the completed specialized
  research on `2026-07-10` and `2026-07-11`. The document-contract and GitHub
  enforcement/deployment sources used for the bounded rows above were re-opened
  on `2026-07-13`; mutable pages without a displayed update date prove
  retrieval-time content only.
- On `2026-07-19`, only the exact high-risk official URLs for GitHub workflow
  syntax, secure use, deployments/environments, and rulesets; pre-commit and
  DORA; Docker Compose include, profiles, secrets, and trust model; SLSA v1.2;
  and NIST SP 800-61 Rev. 3 were re-opened. No stale claim was confirmed in
  that bounded set. Lower-risk source dates and the `2026-07-10 10:00 KST`
  provider-model cutoff remain unchanged.
- Current typed provider/catalog facts retain their
  `2026-07-26T20:08:18+09:00` retrieval timestamp. External provider,
  GitHub, zizmor, and immutable `agency-agents` sources were separately
  revalidated at `2026-08-07T12:45:48+09:00`; that later observation does not
  rewrite the fixed 2026-07-10 model ledger.
- The Measured Provider Surface Baseline and the Claude/Codex convergence
  section were derived at `2026-08-07T17:39:18+09:00` from tracked files at
  commit `82fc20dafc86b80393352ce53c86efb29748722a`. Every count in those
  sections is a direct file measurement, not a restatement of an earlier
  document. They do not move the fixed 2026-07-10 model cutoff or the
  2026-07-26 typed contract timestamps.
- Claude and Codex documentation facts cited in those sections are owned by the
  [provider implementation comparison](./provider-implementation-comparison.md)
  and are not re-derived here. Every such page is mutable and displays no
  publication or last-updated date, so it supports retrieval-time state only.
- UNVERIFIED: whether this project is marked trusted for Codex. The Codex
  configuration reference states that an untrusted project causes Codex to skip
  project-scoped `.codex/` layers including config, hooks, and rules. No tracked
  file can establish the trust state, so the operational effect of the 16
  tracked Codex files is unproven.
- UNVERIFIED: the Codex skills discovery path. No official Codex skills page
  could be retrieved during this pass, so the
  `native_skill_pattern: .agents/skills/**/SKILL.md` value recorded for Codex in
  `contracts/provider-models.yaml` has no confirming official source here.
- ISO public pages provide metadata and summaries, not full standard text.
- ISO/IEC/IEEE 12207:2017 is marked withdrawn and is used only as historical
  lifecycle framing. The 2026-08-07 revalidation confirmed this from the
  ISO-operated `committee.iso.org` catalog after `www.iso.org` returned HTTP
  403 to automated retrieval: record 63712 is at stage 95.99 and names
  ISO/IEC/IEEE 12207:2026 as its successor.
- No external source listed here is adopted as workspace policy by this reference.

## Sources

- [Root README](../../../../README.md) - purpose, structure, lifecycle, and quality gates
- [Documentation hub](../../../README.md) - stage routing and document contracts
- [Agent governance hub](../../../00.agent-governance/README.md) - governance coverage and provider adapters
- [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md) - stage owners, templates, and done criteria
- [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md) - template and evidence boundaries
- [Harness implementation map](../../../00.agent-governance/harness-implementation-map.md) - tracked harness surfaces
- [Scripts README](../../../../scripts/README.md) - canonical automation entry points
- [Infra README](../../../../infra/README.md) - Compose inventory and runtime boundary
- [CI workflow](../../../../.github/workflows/ci-quality.yml) - tracked jobs and checks
- [Agent catalog contract](../../../00.agent-governance/contracts/agent-catalog.yaml) - 14 agents, 24 functions, 8 scopes, 4 projection targets, 9 capability-intake decisions
- [Provider models contract](../../../00.agent-governance/contracts/provider-models.yaml) - 3 providers, 5 work profiles, 11 models, 7 semantic events, and the Codex `session-end` gap
- [Shared hook dispatcher](../../../../scripts/hooks/agent-event-hook.sh) - the single blocking-gate implementation shared by all three providers
- [Pre-commit configuration](../../../../.pre-commit-config.yaml) - 24 hooks across 10 repositories
- [Provider implementation comparison](./provider-implementation-comparison.md) - owner of the Claude and Codex documentation facts used by the convergence section
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) - workflow/job/step automation model
- [GitHub deployments and environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments) - deployment protection, reviewers, branch restrictions, and environment-secret boundaries
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases) - tagged release records, release notes, and assets
- [GitHub deployment history](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/view-deployment-history) - deployment event and outcome evidence
- [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets) and [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) - remote enforcement distinct from tracked workflow definitions
- [GitHub Docs content best practices](https://docs.github.com/en/contributing/writing-for-github-docs/best-practices-for-github-docs) and [Diataxis](https://diataxis.fr/) - the site returns a Cloudflare bot challenge to automated clients; content re-verified 2026-08-07 from the pinned upstream source, which is the current upstream head - audience/purpose and content-type separation
- [GitHub Spec Kit documentation](https://github.github.com/spec-kit/) - Spec → Plan → Tasks → Implement workflow
- [ISO/IEC/IEEE 12207:2017](https://www.iso.org/standard/63712.html) - withdrawn lifecycle-process metadata
- [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) - requirements-engineering metadata
- [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) - architecture-description metadata
- [NIST SP 800-218 SSDF v1.1](https://csrc.nist.gov/pubs/sp/800/218/final) - secure-development practice framework
- [Google SRE incident management](https://sre.google/sre-book/managing-incidents/) - incident roles and live state
- [Google SRE postmortem culture](https://sre.google/sre-book/postmortem-culture/) - reviewed, blameless learning

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when Stage 00, CI, script, Compose, or lifecycle surfaces change
- **Update Trigger**: Update when a tracked owner changes or assigned research tasks close a stated evidence gap

## Related Documents

- [research pack index](./README.md)
- [spec-driven development and SDLC](./spec-driven-sdlc.md)
- [SDLC and operations document-type roles](./sdlc-document-roles.md)
- [agent model selection](./agent-model-selection.md)
- [quality, CI, and formatting](./quality-ci-formatting.md)
