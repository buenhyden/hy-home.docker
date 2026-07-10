---
status: active
---

<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md -->

# Reference: Agentic Engineering Workspace Baseline

## Overview

This reference compares the current tracked `hy-home.docker` workspace with
primary external SDLC, automation, and document-role sources. It covers 25
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
- Provider model cutoff inventory, which is assigned to `T-ARC-002`
- Detailed provider/harness and Compose/security comparisons assigned to later tasks

## Definitions / Facts

- **Workspace evidence** means current state corroborated by tracked files and
  active stage documents. Graphify was built from `30df271a` while this task
  started from `341282da`; its report was navigation-only and is not evidence
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

## Workspace Category Map

| Category | Workspace evidence | External evidence | Status | Gap / risk | Recommendation | Canonical owner | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| purpose | `README.md` defines a shared harness-engineering and agent-first Docker Compose workspace with staged documentation. | GitHub Spec Kit similarly starts from an explicit specification before implementation; ISO 12207 supplies lifecycle framing, but the cited 2017 edition is now withdrawn. | Implemented | Purpose could be overstated if references are mistaken for runtime truth. | Keep the root README authoritative and references advisory. | `README.md` | High |
| overview | `README.md`, `docs/README.md`, `infra/README.md`, and `scripts/README.md` provide tracked entry maps for the workspace. | GitHub Spec Kit publishes a current workflow overview whose artifacts feed the next phase. | Implemented | Multiple entry points can drift independently. | Retain README sync and repository-contract validation. | Root and folder `README.md` files | High |
| roles | Stage 00 persona, scope, agent catalog, subagent protocol, and stage matrix assign authoring and execution ownership. | ISO 42010 frames architecture stakeholders/concerns; Google SRE separates incident command, operations, and communications roles. | Implemented | Provider adapters can drift from the canonical catalog. | Keep Stage 00 as role SSOT and validate adapter parity. | `docs/00.agent-governance/` | High |
| CI/CD | `.github/workflows/ci-quality.yml` defines distinct documentation, repository, Compose, hardening, frontend, pre-commit, and workflow-security jobs. | GitHub defines a workflow as YAML automation made of jobs and steps, with triggers and permissions. | Partially Implemented | Local files cannot prove remote required-check or branch-protection enforcement. | Record local workflow evidence separately from verified remote state. | `.github/workflows/ci-quality.yml` and Stage 00 GitHub governance | High |
| QA | QA scope and validation/hardening scripts separate local, CI-only, hook, and skipped-check evidence. | NIST SSDF v1.1 supplies high-level verification and vulnerability-reduction practices; Spec Kit supplies checklists and cross-artifact analysis. | Implemented | Formal SSDF control mapping is absent and is not implied here. | Preserve change-type gate selection and route formal mapping through approved security work. | `docs/00.agent-governance/scopes/qa.md` | High |
| formatting | `.pre-commit-config.yaml`, hook-mediated validation, templates, and `git diff --check` provide formatting hygiene. | GitHub Actions can automate repeatable jobs; Spec Kit uses structured Markdown artifacts and templates. Neither source mandates this workspace's formatter set. | Implemented | Tool-specific formatting coverage varies by surface. | Keep formatter claims tied to tracked hooks/jobs, not external mandates. | `.pre-commit-config.yaml` | High |
| linting | Pre-commit, shell/Markdown checks, frontend lint, and zizmor are tracked local or CI lint surfaces. | GitHub workflow syntax supports separate jobs/steps; NIST SSDF supports integrating verification into the SDLC without prescribing these linters. | Implemented | A passing local subset does not prove CI-only lint results. | Label each lint gate local, CI-only, or remote-state evidence. | `scripts/validation/run-local-qa-gates.sh` and `.github/workflows/ci-quality.yml` | High |
| syntax/type checks | Repository contracts validate workflow YAML; Compose validation resolves configuration; frontend quality runs lint/typecheck/build. | GitHub documents workflow YAML structure and job/step keys; Spec Kit calls for phase artifacts and quality checks. | Partially Implemented | Type checking is implementation-specific and not universal across every repository surface. | Maintain surface-specific checks and explicit skipped-check rationale. | Relevant Stage 03 test contract and CI job | High |
| automation | `scripts/README.md`, hooks, provider adapters, and workflows expose canonical automation entry points. | GitHub Actions defines event-triggered configurable automation; Spec Kit provides an artifact-producing SDD workflow. | Implemented | Automation ownership can blur across scripts, hooks, and CI. | Keep scripts canonical for local behavior and workflows canonical for CI orchestration. | `scripts/README.md` | High |
| pipeline | `ci-quality.yml` sequences independent quality jobs; release changelog checking runs for release tags. | GitHub workflow syntax provides triggers, jobs, dependencies, matrices, permissions, and steps as pipeline primitives. | Implemented | Remote enforcement and deployment pipelines are outside tracked local proof. | Treat tracked pipeline definition and remote enforcement as separate evidence classes. | `.github/workflows/` | High |
| workflow | Documentation workflows route PRD through operations; GitHub workflows route automated checks; provider workflows adapt Stage 00 policy. | GitHub Spec Kit uses Spec → Plan → Tasks → Implement; GitHub Actions models automated workflows as YAML jobs and steps. | Implemented | “Workflow” can ambiguously mean lifecycle, CI, or provider automation. | Name the workflow class and owning surface in every claim. | Stage matrix, `.github/workflows/`, or provider adapter as applicable | High |
| operating contracts | HAFE guide/policy/runbook, Stage 00 rules, and Stage 05 templates separate guidance, controls, and procedures. | PagerDuty distinguishes detailed repeatable runbook steps; Google SRE separates live incident state and postmortem learning. | Implemented | External practices may be accidentally restated as policy. | Keep adopted controls only in active Stage 00/05 documents. | `docs/05.operations/` | High |
| templates | `docs/99.templates/` maps canonical templates to every active stage and supporting contract. | GitHub Spec Kit uses rich templates and phase-specific Markdown artifacts. | Implemented | Release notes have a convention but no dedicated repo template. | Keep template coverage validated; consider a changelog template only through approved template work. | `docs/99.templates/` | High |
| scripts | `scripts/README.md` makes purpose-folder scripts canonical and prohibits duplicate root wrappers. | GitHub Actions permits scripts within steps; Spec Kit provides CLI-driven workflow automation. These are comparisons, not script policy. | Implemented | Docs can retain stale script paths after moves. | Continue script-reference integrity checks. | `scripts/README.md` | High |
| integration guides | Root onboarding, HAFE guidance, provider notes, and operations guides connect entry points to validators and runtime surfaces. | GitHub Spec Kit's official walkthrough links workflow phases; PagerDuty explains how repeatable guidance becomes an operational runbook. | Implemented | Guides can drift into policy or recovery procedure. | Preserve guide-to-policy/runbook handoffs and tracked-path checks. | `docs/05.operations/guides/` | High |
| SDLC | Stage 01 requirements → Stage 02 architecture → Stage 03 specs → Stage 04 execution → Stage 05 operations, with Stage 90/99 support. | Spec Kit uses Spec → Plan → Tasks → Implement; ISO 29148 and 42010 frame requirements and architecture; withdrawn ISO 12207:2017 remains historical lifecycle metadata only. | Implemented | The workspace has a richer pre-spec intent/design chain and operations feedback than Spec Kit's tool workflow. | Keep the repo-local stage matrix binding and external flows comparative. | `docs/00.agent-governance/rules/stage-authoring-matrix.md` | High |
| governance | Stage 00 owns bootstrap, persona, scopes, provider overlays, catalog, memory, and approval boundaries. | Spec Kit describes a project constitution; NIST SSDF provides high-level organizational secure-development practices. | Implemented | External “constitution” or SSDF language could be mistaken for adopted governance. | Translate proposals through the earliest approved workspace owner before adoption. | `docs/00.agent-governance/` | High |
| system structure | Root Compose includes tiered `infra/**`; docs, scripts, secrets, projects, tests, and provider surfaces have tracked entry points. | ISO 42010 supports explicit architecture descriptions and stakeholder concerns; its public page is metadata, not the full standard. | Implemented | Reference maps may lag the runtime inventory. | Validate structural claims against tracked Compose, READMEs, and scripts. | Root `README.md`, `docker-compose.yml`, and `infra/README.md` | High |
| rules | Bootstrap, agentic, documentation, task-checklist, GitHub, and scope rules define deterministic execution boundaries. | Spec Kit's constitution illustrates stable cross-phase principles; NIST SSDF illustrates practice-level secure-development guidance. | Implemented | Duplicate provider-local rules can conflict with Stage 00. | Keep root/provider files thin and Stage 00 canonical. | `docs/00.agent-governance/rules/` | High |
| security | Security scope, secret boundaries, GitHub workflow controls, template baseline, hardening checks, and disclosure guidance are tracked. | NIST SSDF v1.1 recommends integrating secure practices into any SDLC; NIST SP 800-61 Rev. 3 frames incident response within CSF 2.0. | Partially Implemented | No formal SSDF mapping is adopted; remote enforcement is unverified here. | Keep framework mapping and remote-state verification as separately approved evidence work. | Security scope and active security stages | High |
| Docker Compose/infrastructure | Root `docker-compose.yml`, tiered `infra/`, version registry, validation, and hardening scripts are current tracked runtime evidence. | The Task 1 source set provides lifecycle framing, not Compose-specific requirements; official Docker comparison is assigned to `T-ARC-005`. | Implemented | Using SDLC sources as Compose guidance would overreach their scope. | Preserve runtime-source precedence and defer Docker-specific comparison to Task 5. | `docker-compose.yml` and `infra/` | High |
| AI agents | Stage 00 catalog plus Claude, Codex, and Gemini adapter surfaces define agent roles and provider boundaries. | GitHub Spec Kit states that phase artifacts feed an AI coding agent structured context; it does not define this workspace's multi-provider catalog. | Implemented | Provider feature parity and mutable vendor behavior need Task 3 revalidation. | Keep shared policy provider-neutral and revalidate adapter capabilities in `T-ARC-003`. | Stage 00 agent catalog and provider notes | High |
| harness engineering | HAFE spec, implementation map, operations documents, scripts, hooks, CI, and evidence stages treat the harness as a cross-surface contract. | Spec Kit combines templates, checklists, cross-artifact analysis, and agent context; GitHub Actions supplies automation primitives. | Implemented | “Harness” has no single external normative definition in the Task 1 source set. | Preserve the repo-local definition and label external analogies as comparison. | HAFE Stage 03/05 chain | High |
| loop engineering | Agentic rules define discover → plan → execute → verify → progress; QA, CI, incidents, postmortems, and evals provide feedback. | Spec Kit provides a forward artifact loop; Google SRE makes incident state and reviewed postmortems learning inputs. | Partially Implemented | Later tasks still need provider-loop and eval/CI-specific evidence consolidation. | Complete loop/provider and automation comparisons in `T-ARC-003` and `T-ARC-004`. | Stage 00 agentic rule and task/eval owners | High |
| task-characteristic model selection | `agent-model-selection.md` records task traits, evidence requirements, and risk caveats without changing model policy. | The Task 1 sources show structured agent context but do not compare provider models or prove task fit. Official cutoff research is assigned to `T-ARC-002`. | Partially Implemented | Current provider catalogs and cutoff state are not established by this task. | Revalidate official catalogs at the fixed cutoff and label task-fit mappings as inference. | Stage 90 model landscape/selection references; active policy remains Stage 00 | Medium |

## Analysis

All 25 requested categories have a current tracked state, an external comparison
or an explicit external-source limitation, a status, a gap, a recommendation,
one canonical owner, and a confidence judgment. The dominant pattern is a
multi-surface workspace: active stages own decisions and evidence, runtime files
own execution truth, and Stage 90 explains rather than governs.

The comparison also exposes three evidence boundaries. First, tracked workflow
YAML does not prove remote branch protection or required-check enforcement.
Second, secure-SDLC references do not create an SSDF control mapping. Third,
Task 1's SDLC/document-role sources cannot prove provider model cutoff state,
provider feature parity, or Docker-specific best practice; those remain assigned
to Tasks 2, 3, and 5.

## Application Notes for This Workspace

- Start repo-local claims from tracked root/stage files, then use Graphify only
  for navigation.
- State whether “workflow” means documentation lifecycle, CI automation, or a
  provider runtime adapter.
- Treat external sources as comparisons until an approved active artifact adopts
  a practice.
- Route a discovered gap to one canonical owner before linking downstream work.

## Potential Follow-up / Gap

- `T-ARC-002`: establish provider model cutoff evidence and refresh
  task-characteristic selection.
- `T-ARC-003`: revalidate provider/harness/agent capability comparisons.
- `T-ARC-004`: consolidate local, CI-only, and remote automation evidence.
- `T-ARC-005`: perform official Docker Compose and security-framework comparison.

## Source Rules

- Repo-local claims use tracked files and active stage documents as of
  `2026-07-10`.
- External sources were retrieved on `2026-07-10`; mutable pages without a
  displayed update date prove retrieval-time content only.
- ISO public pages provide metadata and summaries, not full standard text.
- ISO/IEC/IEEE 12207:2017 is marked withdrawn and is used only as historical
  lifecycle framing.
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
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) - workflow/job/step automation model
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
