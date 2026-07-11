---
status: active
---

<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/ai-agent-catalogs.md -->

# Reference: AI Agent Catalogs and Role-Based Agent Packs

## Overview

External catalogs can supply useful role taxonomies and prompt patterns, but
agent definitions are executable instructions once installed. This reference
uses the community `agency-agents` repository as a point-in-time comparison
with the small, governance-first catalog in `hy-home.docker`.

The upstream evidence is pinned to commit
`9f3e401ccd09aa0ee0ef8e015226d0647908e01e` (committed 2026-07-09) and was
retrieved on 2026-07-10. Nothing from that repository was installed, converted,
vendored, or executed.

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

- The pinned upstream README says “230+” specialized agents and exposes 17
  headings named as divisions: Engineering, Design, Paid Media, Sales,
  Marketing, Product, Project Management, Testing, Security, Support, Spatial
  Computing, Specialized, Finance, Game Development, Academic, GIS, and
  Healthcare. The prior “16 divisions” statement is stale.
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
- The workspace catalog contains 15 roles (one workflow supervisor and
  fourteen workers) and 22 tracked skills. Stage 00 is canonical.
- `scripts/operations/sync-provider-surfaces.sh` generates Codex role TOMLs
  and Gemini/Antigravity agent/skill pointers from canonical/local sources;
  `--check` currently reports no drift.

## Catalog Comparison Matrix

| Catalog concern | agency-agents pattern | Workspace pattern | Importability | Required wrapper/control | Recommendation | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| Persona breadth | 230+ role personas across 17 observed division headings optimize for broad business coverage | 15 repository-specific roles optimize for bounded recurring work | Reference only | Candidate role must correspond to a demonstrated workspace gap and avoid duplicate ownership | Use division taxonomy for discovery; add no role without an approved Stage 00 proposal | `docs/00.agent-governance/agents/README.md` |
| Role boundaries | Persona files emphasize identity, mission, workflows, deliverables, and voice; boundary precision varies by role | Each canonical role is tied to purpose, scope, model policy, delegation, and repository rules | Adapt after review | Rewrite mission into explicit in-scope/out-of-scope and canonical-owner boundaries | Import the job to be done, not the persona's assumed authority | `docs/00.agent-governance/agents/README.md` |
| Prompt portability | Markdown bodies are copied or converted across many tool formats | Provider adapters are projections of Stage 00 and shared Claude skill content where applicable | Adapt after review | Normalize provider-required fields and remove tool-specific invocation assumptions | Maintain one reviewed canonical role, then generate/test each adapter | `scripts/operations/sync-provider-surfaces.sh` |
| Scope imports | Upstream personas may refer to generic projects, departments, files, or external systems | Stage 00 scopes route work by repository surface and lifecycle owner | Do not direct-import | Replace all generic scope text with tracked repo paths, stage owners, and explicit exclusions | Reject any definition whose target scope cannot be expressed in the Stage 00 model | `docs/00.agent-governance/scopes/README.md` |
| Tools and permissions | Installer/converter targets provider-native agent directories; persona/tool assumptions may be broad | Repository approvals and environment rules govern actions; local metadata is not an enforced allowlist | Do not direct-import | Apply least privilege in the native provider schema and preserve repository approval boundaries | Review every command, MCP, web, external-action, and protected-path request before adaptation | `docs/00.agent-governance/rules/approval-boundaries.md` |
| Model tier | Upstream roles are portable and do not centrally enforce this workspace's supervisor/worker mappings | `subagent-protocol.md` assigns active provider tiers and reasoning settings | Adapt after review | Select model only through current policy and Task 2 evidence; validate projection parity | Never preserve an upstream model assumption by default | `docs/00.agent-governance/subagent-protocol.md` |
| Lifecycle behavior | Upstream distribution focuses on installing/invoking agent definitions across tools | Stage 00 task/review protocol, hooks, checklists, memory, and provider notes constrain lifecycle | Reference only | Wrap the role with bootstrap, evidence, completion, and independent-review requirements | Treat persona workflow prose as advisory until mapped to an owned repository loop | `docs/00.agent-governance/rules/agentic.md` |
| Handoffs and delegation | Roles can be selected by name, but a shared repository-specific handoff contract is not established by the README | Supervisor/worker delegation and cross-role evidence are defined by the subagent protocol | Adapt after review | Declare caller, deliverable, allowed files, base commit, evidence, and return path | Use the existing supervisor protocol instead of importing a parallel orchestration model | `docs/00.agent-governance/subagent-protocol.md` |
| Evidence and provenance | Pinned Git history, Markdown sources, README, license, and converter code provide upstream provenance; per-agent outcome evidence varies | Task cards, diffs, checks, commits, review reports, and source ledgers provide adoption evidence | Reference only until pinned | Pin upstream commit, record exact source file/license, retain review rationale, and never cite self-claims as independent proof | Require a source ledger and lifecycle artifact for any proposed adaptation | `docs/04.execution/tasks/README.md` |
| Security review | Agent text and installation scripts are third-party instruction/code surfaces; direct global-directory installation changes runtime behavior | Security scope, approval boundaries, sandbox rules, and protected adapter surfaces constrain adoption | Do not direct-import | Review prompt injection, secrets, external actions, commands, dependency/install behavior, and permission escalation | Inspect offline at a pin; adapt manually; do not run upstream installers against provider directories | `docs/00.agent-governance/scopes/security.md` |
| Evaluations | Upstream “production-ready”/“battle-tested” language is a publisher claim; no independent workspace benchmark follows from it | Deterministic contract fixtures exist, but new-role semantic quality requires task-specific acceptance evidence | Adapt only with evaluation | Define representative tasks, rubric/scorer, failure cases, baseline, privacy boundary, and reviewer calibration | Pilot a candidate role against existing generalist roles before catalog adoption | `docs/00.agent-governance/scopes/qa.md` |
| Direct-import risks | Convert/install flows can write many definitions into user-global provider directories and later auto-update through the desktop app | Tracked adapters are reviewable, generated in-repo, parity-checked, and subordinate to Stage 00 | Prohibited without separate explicit approval | No global install; no auto-update; pin source; narrow text/tools; generate locally; review diff; run repository contracts | Use external catalogs as design references by default; propose one bounded role at a time | `docs/00.agent-governance/rules/approval-boundaries.md` |

## Workspace Implementation Status

| Category | Current state | External primary | Comparison | Status | Gap | Recommendation | Canonical owner | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Agent catalog and import boundary | Stage 00 owns 15 roles and provider projections; 22 skills and generated pointer/TOML surfaces are tracked and parity-checked. | Pinned `agency-agents` repository, README, license, and integration documentation | Upstream optimizes for catalog breadth and cross-tool installation; the workspace optimizes for bounded ownership and reviewed projections. | Partially Implemented | No dedicated third-party-agent intake checklist or semantic candidate-role benchmark is adopted. | Keep reference-only as the default; route one pinned candidate through security, QA, Stage 00 proposal, generation, and independent review. | `docs/00.agent-governance/agents/README.md` | Catalog files; sync `--check`; repository contracts; pinned upstream sources | High |

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
  implementations.

## Sources

- [agency-agents pinned repository](https://github.com/msitarzewski/agency-agents/tree/9f3e401ccd09aa0ee0ef8e015226d0647908e01e)
- [pinned README](https://github.com/msitarzewski/agency-agents/blob/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/README.md)
- [pinned MIT license](https://github.com/msitarzewski/agency-agents/blob/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/LICENSE)
- [pinned Codex integration](https://github.com/msitarzewski/agency-agents/blob/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/integrations/codex/README.md)
- [pinned Gemini CLI integration](https://github.com/msitarzewski/agency-agents/blob/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/integrations/gemini-cli/README.md)
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents)
- [Codex subagents](https://developers.openai.com/codex/subagents)
- [Gemini CLI documentation](https://google-gemini.github.io/gemini-cli/docs/)
- [Gemini CLI subagents](https://github.com/google-gemini/gemini-cli/blob/main/docs/core/subagents.md)
- [Gemini CLI v0.38.1 subagent announcement](https://github.com/google-gemini/gemini-cli/discussions/25562)
- [Agent catalog](../../../00.agent-governance/agents/README.md)
- [Subagent protocol](../../../00.agent-governance/subagent-protocol.md)
- [Approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md)
- [Repository contract check](../../../../scripts/validation/check-repo-contracts.sh)

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
