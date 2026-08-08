---
status: draft
artifact_id: reference:agentic-engineering-research:ai-agent-catalogs
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-08
review_cycle: on-source-change
---

# Reference: External AI-Agent Catalogs and Local Intake

## Overview

External catalogs are discovery inputs, not install sources or local
authority. The official `msitarzewski/agency-agents` default branch was
inspected read-only at immutable commit
`ebe9c99acb5c96f9468de368d8bead775387d1a7` on 2026-08-08. Its canonical
`divisions.json` and immutable tree yield 17 divisions and 270 Markdown agent
files. No installer, converter, or generated output was executed or copied.

The workspace's prior analytic pin is
`8ef49232e02431f7ca4792b487e5a85a7939ff3a` (17 divisions, 269 agents). That
historical pin remains valid provenance; the new upstream head is a distinct
current observation, not a silent rewrite of the old evidence.

## Purpose

Satisfy REQ-28 by comparing the external breadth/installation model with the
workspace's curated catalog, typed capability-intake ledger, generation
boundary, permissions, evaluation, and approval rules.

## Repository Role

This Stage 90 reference may suggest capability gaps. It cannot add a role,
function, scope, model, permission, provider adapter, or user-global install.
Stage 00 and an approved lifecycle change remain the only adoption path.

## Scope

### In scope

- Immutable upstream identity, license/distribution pattern, division and agent counts.
- Local 14-role, 24-function, 9-intake catalog and provider projections.
- Safe reference/merge/defer/reject and evaluation boundaries.

### Out of scope

- Running upstream install/convert scripts or writing provider-global directories.
- Importing persona voice, prompt bodies, model assumptions, tools, or permissions.
- Treating publisher maturity language or catalog size as outcome evidence.

## Definitions / Facts

### Immutable upstream derivation

The default branch and exact revision were resolved with:

```bash
git ls-remote https://github.com/msitarzewski/agency-agents.git \
  HEAD refs/heads/main refs/heads/master
git clone --filter=blob:none --no-checkout \
  https://github.com/msitarzewski/agency-agents.git <temporary-directory>/repo
git -C <temporary-directory>/repo checkout --detach \
  ebe9c99acb5c96f9468de368d8bead775387d1a7
```

The exact count command, run from that detached checkout, was:

```bash
git ls-tree -r --name-only HEAD | jq -R -s --slurpfile d divisions.json \
  'split("\n") | map(select(test("\\.md$"))) | map(split("/")[0]) |
   map(select(. as $x | ($d[0].divisions | has($x)))) | group_by(.) |
   map({division: .[0], agents: length}) |
   {division_count: length, agent_count: (map(.agents) | add), by_division: .}'
```

| Division | Agents | Division | Agents |
| --- | ---: | --- | ---: |
| academic | 6 | design | 10 |
| engineering | 58 | finance | 5 |
| game-development | 21 | gis | 13 |
| healthcare | 3 | marketing | 36 |
| paid-media | 7 | product | 5 |
| project-management | 7 | sales | 9 |
| security | 12 | spatial-computing | 6 |
| specialized | 57 | support | 6 |
| testing | 9 | **Total** | **270** |

`divisions.json` explicitly excludes integrations, examples, scripts, and
strategy from division counting. The upstream Codex integration documents a
converter that maps source name, description, and body into standalone TOML
and an installer that targets `~/.codex/agents/`. Those are upstream design
facts, not actions taken by this task. The MIT license permits reuse but does
not establish fitness, safety, or authority.

### Current local catalog

| Concern | Tracked state at Task 4 baseline | Evidence limit |
| --- | --- | --- |
| Canonical roles | 14: one supervisor and thirteen workers | Definition only; no provider execution claim. |
| Canonical functions | 24 typed reusable functions | Projection membership does not prove invocation. |
| Role projections | 14 each in Stage 00, Claude, Codex, Gemini, and compatibility views | Generated/configured parity only. |
| Work profiles | 5 exact provider mappings | Acceptance and entitlement remain `needs_revalidation`. |
| Capability intake | 9 agency-agents-derived rows: 8 `merge`, 1 `defer` | Capability knowledge was merged; no upstream identity/persona installed. |
| Evaluation | 11 fixtures and 16 synthetic regressions | Repository semantics, not candidate-role/live-model superiority. |

The local catalog optimizes for owned outcomes, permissions, handoffs, model
policy, and reviewability rather than breadth. A 270-entry upstream roster and
a 14-role local catalog therefore measure different things and must not be
treated as coverage percentages.

### Intake decision boundary

| Concern | Upstream pattern | Required local disposition/control |
| --- | --- | --- |
| Identity/personality | Strong persona voice and domain identity | Do not import voice; rewrite only the job-to-be-done under an existing or approved owner. |
| Scope | General divisions and projects | Map to one of 14 repository scopes and concrete owned paths; stop if no owner exists. |
| Tools/services | Agents may name external tools/services | Review commands, MCP/web access, credentials, external writes, and paid services under least privilege. |
| Model/effort | Cross-tool portable definitions | Assign one typed local work profile; discard upstream model assumptions. |
| Workflow | Persona-specific process text | Map to the canonical lifecycle and four bounded loops; no parallel workflow authority. |
| Distribution | Converter/installer writes provider-native directories | Prohibit direct/global install in research; canonical Stage 00 source first, then generated projections. |
| Provenance | Public Git, files, scripts, license | Pin commit/file/license and preserve source/date in Stage 04 evidence. |
| Security | Third-party prompt and executable scripts | Inspect offline as untrusted input; no execution or permission inheritance. |
| Evaluation | Publisher descriptions and success metrics | Compare representative tasks against existing roles with an approved rubric and independent reviewer. |

### Safe adaptation sequence

1. Demonstrate a capability gap in a named owned outcome.
2. Pin the upstream commit, exact source file, and license.
3. Inspect text/code offline as untrusted input; do not install it.
4. Prefer merging a capability into an existing function/role.
5. If a new role/function is still justified, define scope, permission,
   profile, handoff, fixtures, and failure behavior in approved Stage 03/04 work.
6. Change the canonical Stage 00 catalog first, render projections, inspect the
   diff, validate parity/evaluation, and obtain independent review.
7. Keep upstream auto-update and user-global install paths outside adoption.

## Scope Implications

| Scope | Application and disposition |
| --- | --- |
| `agentic` | Owns catalog/intake/profile/projection changes; external identities remain reference-only until approved and generated. |
| `architecture` | External architect capabilities may inform functions, but the enum-only local scope needs an ownership decision before a new role. |
| `backend` | No current local application surface; reject/defer backend persona intake until a product/Spec creates one. |
| `common` | Merge broadly reusable review knowledge into existing functions rather than duplicating roles. |
| `docs` | Preserve pin, license, claim dates, and migration evidence; external prose is not local policy. |
| `entry` | Gateway specialists map to adjacent infra ownership; no direct role import while the typed scope route is absent. |
| `frontend` | Existing fixture ownership is not a product-role gap; require representative work and an approved owner before intake. |
| `infra` | DevOps/SRE capabilities already merge into existing infra/ops roles; tools and runtime writes remain approval-bound. |
| `meta` | Taxonomy/catalog mechanics route through docs/Stage 00; do not infer a new meta role from upstream breadth. |
| `mobile` | No current surface; mobile personas remain deferred unless an approved lifecycle chain creates the domain. |
| `ops` | Incident/SRE capability is merged into existing owners; external service assumptions and outcome claims are not adopted. |
| `product` | Upstream product roles remain deferred because the local typed route/owner is absent and stakeholder authority is human. |
| `qa` | Own candidate-role fixtures, comparative baseline, failure cases, and independent scoring before adoption. |
| `security` | Inspect prompts/installers for injection, secrets, commands, external actions, dependencies, and permission expansion. |

## Sources

| Source | Accessed | Class | Verification state |
| --- | --- | --- | --- |
| [agency-agents immutable tree](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7) | 2026-08-08T16:18:04+09:00 | External fixed | Default-branch SHA resolved by `git ls-remote`; detached tree counted 17 divisions / 270 agents. |
| [Pinned division registry](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/divisions.json) | 2026-08-08 | External fixed | Canonical division set and exclusion notes. |
| [Pinned Codex integration](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/integrations/codex/README.md) | 2026-08-08 | External fixed | Converter/install design; not executed. |
| [Pinned MIT license](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/LICENSE) | 2026-08-08 | External fixed | Distribution license only. |
| [Workspace historical pin](https://github.com/msitarzewski/agency-agents/tree/8ef49232e02431f7ca4792b487e5a85a7939ff3a) | retained from 2026-07-27 analysis | External fixed / historical | Prior workspace basis: 17 divisions / 269 agents; not used for the new current count. |
| [Agent catalog contract](../../../00.agent-governance/contracts/agent-catalog.yaml) | 2026-08-08 | Workspace tracked | Complete 14-role, 24-function, 9-intake registry at Task 4 baseline. |
| [Subagent protocol](../../../00.agent-governance/subagent-protocol.md) | 2026-08-08 | Workspace tracked | Scope, role, permission, model, and handoff boundary. |

## Maintenance

Re-resolve the default-branch SHA and rerun the exact immutable-tree count only
when an intake decision or catalog refresh needs current upstream facts. Keep
historical and current pins separate; never replace a pin with `main` in a
load-bearing citation.

## Related Documents

- [Agent instructions](./agent-instructions-vibe-coding.md)
- [Agent model selection](./agent-model-selection.md)
- [Workspace baseline](./workspace-baseline.md)
- [Scope application matrix](./scope-application-matrix.md)
- [Execution Task](../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
