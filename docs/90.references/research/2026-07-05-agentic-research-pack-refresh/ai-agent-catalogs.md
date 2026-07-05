---
status: active
---

<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/ai-agent-catalogs.md -->

# Reference: AI Agent Catalogs and Role-Based Agent Packs

## Overview

This reference analyzes external AI agent catalogs, using the `agency-agents`
community pack as the anchor example, and compares catalog-style agent
distribution with the curated, governance-first agent catalog used in
`hy-home.docker`.

## Purpose

Explain how large external agent-persona catalogs are structured, what value
and risk they carry, and which import path any external agent definition must
follow before it can become part of this workspace.

## Repository Role

This reference supports the Stage 00 agent catalog, the subagent protocol, and
provider adapter surfaces. It does not add, rename, or import agents, change
model policy, or modify provider runtime directories.

## Scope

### In Scope

- External role-based agent catalog structure and conventions
- Multi-tool agent distribution and conversion patterns
- Comparison with the repo-local canonical agent catalog
- Import boundary and security review considerations

### Out of Scope

- Installing or converting external agent definitions
- Agent catalog, model policy, or subagent protocol changes
- Provider runtime configuration changes
- Endorsement of any external catalog as adopted tooling

## Definitions / Facts

- **Agent catalog**: A maintained inventory of agent definitions with names,
  roles, capabilities, and invocation conventions. Catalogs can be curated
  (small, governed) or community-scale (large, general-purpose).
- **agency-agents**: A community MIT-licensed repository publishing a large
  role-based agent pack. At the 2026-07-05 review, its README described roughly
  232 Markdown agent personas across 16 divisions (engineering, design,
  marketing, product, testing, security, game development, GIS, and others).
- **Persona-style definition**: agency-agents agents are Markdown documents
  combining identity, mission, workflows, deliverables, and communication
  style, intended to be copied or adapted per tool.
- **Multi-tool conversion**: agency-agents ships install/convert scripts that
  detect installed AI coding tools and place agent files into tool-specific
  directories such as `~/.claude/agents/`, with converters for Claude Code,
  Codex, Gemini-based tools, Cursor, and other runtimes.
- **Repo-local canonical catalog**: `docs/00.agent-governance/agents/` defines
  one `workflow-supervisor` and fourteen worker agents. `.claude/agents/*.md`,
  `.codex/agents/*.toml`, and `.agents/` are provider adapters, not separate
  governance.
- **Repo-local model policy**: `subagent-protocol.md` assigns the supervisor
  and worker model tiers; provider adapters must keep name/model/scope parity,
  and `check-repo-contracts.sh` checks the machine-checkable parts.

## Catalog Model Comparison

| Dimension        | agency-agents (community pack)                | `hy-home.docker` (curated catalog)                            |
| ---------------- | --------------------------------------------- | ------------------------------------------------------------- |
| Size and scope   | ~232 agents, 16 business divisions            | 15 agents scoped to this workspace                            |
| Source of truth  | Per-tool copies after install scripts         | Stage 00 catalog with provider adapter projections            |
| Definition style | Personality-driven persona Markdown           | Role, scope, tools, and model policy per governance templates |
| Distribution     | Install/convert scripts into tool directories | Tracked repo surfaces with parity validation                  |
| Governance       | User discretion, MIT license                  | Subagent protocol, approval boundaries, contract checks       |
| Model policy     | Not centrally enforced                        | Supervisor/worker model tiers defined in Stage 00             |

## Analysis

Catalog packs such as agency-agents optimize for breadth: many ready-made
personas, quick installation, and portability across AI coding tools. That
breadth is useful as a design reference for role decomposition, naming, and
division taxonomy when new worker agents are considered.

This workspace optimizes for the opposite property: a small catalog whose every
entry has a defined scope, tool surface, and model tier, with provider adapters
kept in parity by validators. Directly running an external install script
against `.claude/agents/` or `.codex/agents/` would bypass Stage 00 governance
and create untracked runtime behavior, so the catalogs differ in import path,
not only in size.

Agent definitions are also instructions, and imported instructions are
untrusted input. An external persona can request broad tool access or embed
behavior that conflicts with approval boundaries. Any adoption therefore needs
the same review posture as other third-party code: read the definition, strip
or narrow tool grants, and record the decision in the active lifecycle.

## Application Notes for This Workspace

- Treat external catalogs as design references for role taxonomy, not as
  installable runtime content.
- Route any new agent through Stage 00: catalog entry first, then provider
  adapters, then parity validation via `check-repo-contracts.sh`.
- Review imported agent text for tool access, external action requests, and
  conflicts with approval boundaries before adaptation.
- Keep persona style subordinate to scope: a repo-local agent definition needs
  clear scope, tools, and model policy more than personality voice.
- Record catalog-derived adoption decisions as active-stage work, not inside
  this reference.

## Potential Follow-up / Gap

- A future review could compare the agency-agents division taxonomy against the
  repo-local worker roster to identify missing roles (for example, dedicated
  performance or accessibility reviewers) as candidate catalog entries.
- Community catalog contents change quickly; counts and division names cited
  here must be rechecked against the upstream README before reuse.
- A future governance note could define a checklist for vetting third-party
  agent definitions before adaptation.

## Source Rules

- Prefer the upstream repository README and license text for catalog facts.
- Treat community catalog claims (agent counts, tool support) as
  point-in-time observations that require recheck before reuse.
- Repo-local catalog facts must be verified against Stage 00 agents, the
  subagent protocol, and provider notes.

## Sources

- [agency-agents repository](https://github.com/msitarzewski/agency-agents) - community agent pack structure, divisions, conversion scripts, MIT license
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) - provider-native subagent definition and tool-access model
- [Codex subagents](https://developers.openai.com/codex/subagents) - Codex subagent and `.codex/agents/*.toml` model
- [Agent catalog](../../../00.agent-governance/agents/README.md) - repo-local canonical agent inventory
- [Subagent protocol](../../../00.agent-governance/subagent-protocol.md) - repo-local model policy and provider adapter mapping
- [Approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md) - protected surfaces relevant to agent tool grants
- [Repository contract check](../../../../scripts/validation/check-repo-contracts.sh) - runtime catalog parity gate

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when the Stage 00 agent catalog, subagent
  protocol, or referenced external catalogs change materially
- **Update Trigger**: Update when agent import policy, provider adapter
  surfaces, or upstream catalog structure changes

## Related Documents

- [research pack index](./README.md)
- [provider implementation comparison](./provider-implementation-comparison.md)
- [harness engineering](./harness-engineering.md)
- [workspace baseline](./workspace-baseline.md)
- [subagent protocol](../../../00.agent-governance/subagent-protocol.md)
