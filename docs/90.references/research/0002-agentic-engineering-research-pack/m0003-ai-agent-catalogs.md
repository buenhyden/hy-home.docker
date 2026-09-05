---
title: "Reference: External AI-Agent Catalogs and Local Intake"
version: "1.1.0"
type: "reference/research"
status: "published"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "references"
artifact_id: "RES-0002-m0003"
parent_ids:
- "RES-0002"
created: "2026-08-23"
observed_at: "2026-09-05"
reviewed_at: "2026-09-05"
review_cycle: "on-source-change"
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

Re-resolving the default branch on 2026-08-14T13:40:00+09:00 with
`git ls-remote https://github.com/msitarzewski/agency-agents.git HEAD
refs/heads/main` returns the identical SHA
`ebe9c99acb5c96f9468de368d8bead775387d1a7`. The upstream default branch has
not advanced since the 2026-08-08 pin, so the pinned tree and every count
derived from it are re-confirmed unchanged without re-running the full
clone-and-count derivation. This is recorded as a fresh dated observation of
the same evidence, not a new count.

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

| Division           | Agents | Division          |  Agents |
| ------------------ | -----: | ----------------- | ------: |
| academic           |      6 | design            |      10 |
| engineering        |     58 | finance           |       5 |
| game-development   |     21 | gis               |      13 |
| healthcare         |      3 | marketing         |      36 |
| paid-media         |      7 | product           |       5 |
| project-management |      7 | sales             |       9 |
| security           |     12 | spatial-computing |       6 |
| specialized        |     57 | support           |       6 |
| testing            |      9 | **Total**         | **270** |

`divisions.json` explicitly excludes integrations, examples, scripts, and
strategy from division counting. The upstream Codex integration documents a
converter that maps source name, description, and body into standalone TOML
and an installer that targets `~/.codex/agents/`. Those are upstream design
facts, not actions taken by this task. The MIT license permits reuse but does
not establish fitness, safety, or authority.

### Prose description versus machine-countable artifact

Reading the repository's rendered landing page on 2026-08-14 (External
mutable, distinct from the pinned tree) surfaces a concrete evidence-quality
lesson: the page's marketing prose describes "18+ divisions" and "over 230
specialized agents" across "395 commits," while the pinned, machine-counted
`divisions.json` plus `git ls-tree` derivation used above yields the exact
17 divisions and 270 agents recorded in the table. The prose rounds down and
uses an inexact "+"/"over" framing; the machine-countable artifact is exact
and re-derivable. Neither figure is wrong on its own terms, but only the
pinned-tree count is evidence-grade for this repository's purposes: a
publisher's landing-page description is not a substitute for counting the
pinned artifact directly, and future re-reads of this or any external
catalog should prefer the countable source over the descriptive one.

### Codex converter mechanics (upstream design, not executed)

Reading the pinned `integrations/codex/README.md` in detail resolves exactly
what the upstream Codex converter does, sharpening this leaf's prior
one-sentence summary:

| Mechanic                                  | Exact behavior                                                                                                                                              |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Fields read from each agent Markdown file | `name`, `description`, and the full Markdown body                                                                                                           |
| Fields explicitly discarded               | `color`, `emoji`, `vibe` — visual/persona metadata with no Codex TOML equivalent                                                                            |
| Generated TOML fields                     | The minimal Codex-required set: `name`, `description`, `developer_instructions`                                                                             |
| Body mapping                              | The Markdown body becomes `developer_instructions` verbatim                                                                                                 |
| Generation path                           | `integrations/codex/agents/<slug>.toml`                                                                                                                     |
| Install path                              | `~/.codex/agents/`, via the upstream install script                                                                                                         |
| Identity mechanics                        | Codex treats the TOML `name` field as the source of truth; the filesystem slug exists only for filesystem safety and is not how a user references the agent |

This confirms the "Distribution" row of the intake decision boundary below
in concrete terms: the converter is a real, working design that writes to a
provider-global directory (`~/.codex/agents/`), which is exactly the path
this repository's safe adaptation sequence prohibits running directly. No
part of this converter or its output was executed or copied into this
workspace.

### Sample agent texture (one pinned file, inspected offline)

`engineering/engineering-backend-architect.md` at the pinned commit was read
directly to give the "Identity/personality" and "Tools/services" rows of the
intake boundary concrete texture rather than only a general claim:

- YAML frontmatter carries exactly the fields the Codex converter discards:
  `name`, `description`, `color`, `emoji`, `vibe`.
- The body opens in first-person persona voice — "You are **Backend
  Architect**, a senior backend architect who specializes in scalable
  system design, database architecture, and cloud infrastructure" — and
  runs to roughly 1,100 lines and 11,000+ words covering identity, mission,
  rules, deliverables, communication style, and success metrics.
- No specific model or provider is named anywhere in the file.
- The file names concrete external tools and standards — PostgreSQL, Redis,
  RabbitMQ, Kubernetes, OAuth 2.0, and OpenAPI/AsyncAPI/protobuf
  specifications — without naming credentials or secrets.

At roughly 1,100 lines, this one sample file is about 23 times the 48-line
average of this repository's 14 canonical role files (672 tracked lines
total across `docs/00.agent-governance/agents/agents/*.md`, confirmed by
direct `wc -l` on 2026-08-14). A persona-voice import at that density would
dwarf this repository's own role files, which is independent evidence for
why the safe adaptation sequence requires rewriting only the
job-to-be-done rather than importing the persona body wholesale.

### Current local catalog

| Concern             | Tracked state at Task 4 baseline                                    | Evidence limit                                                           |
| ------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Canonical roles     | 14: one supervisor and thirteen workers                             | Definition only; no provider execution claim.                            |
| Canonical functions | 24 typed reusable functions                                         | Projection membership does not prove invocation.                         |
| Role projections    | 14 each in Stage 00, Claude, Codex, Gemini, and compatibility views | Generated/configured parity only.                                        |
| Work profiles       | 5 exact provider mappings                                           | Acceptance and entitlement remain `needs_revalidation`.                  |
| Capability intake   | 9 agency-agents-derived rows: 8 `merge`, 1 `defer`                  | Capability knowledge was merged; no upstream identity/persona installed. |
| Evaluation          | 11 fixtures and 16 synthetic regressions                            | Repository semantics, not candidate-role/live-model superiority.         |

The local catalog optimizes for owned outcomes, permissions, handoffs, model
policy, and reviewability rather than breadth. A 270-entry upstream roster and
a 14-role local catalog therefore measure different things and must not be
treated as coverage percentages.

Direct re-count at repository commit `ece3eda9c3e1a603c6495dd55caba7df1c29ef6c`
(2026-08-14) confirms every row above by file count rather than by trusting
the table text:

| Surface                        | Command                                                      | Count                    |
| ------------------------------ | ------------------------------------------------------------ | ------------------------ |
| Canonical role files           | `ls docs/00.agent-governance/agents/agents/*.md \| wc -l`    | 14                       |
| Canonical function files       | `ls docs/00.agent-governance/agents/functions/*.md \| wc -l` | 24                       |
| Claude role projection         | `ls .claude/agents/*.md \| wc -l`                            | 14                       |
| Claude skill projection        | `find .claude/skills -name SKILL.md \| wc -l`                | 24                       |
| Codex role projection          | `ls .codex/agents/*.toml \| wc -l`                           | 14                       |
| Gemini role projection         | `ls .gemini/agents/*.md \| wc -l`                            | 14                       |
| Compatibility skill projection | `find .agents/skills -name SKILL.md \| wc -l`                | 24                       |
| `capability_intake` entries    | direct read of `agent-catalog.yaml:719-791`                  | 9 (8 `merge`, 1 `defer`) |

Every projection surface matches its canonical source count exactly (14
roles across all 4 role surfaces, 24 functions across both skill
surfaces), which is evidence of configured parity at this commit. It is not
evidence that any provider actually loaded, accepted, or executed a
projected file; that remains `needs_revalidation` per the provider-model
landscape leaf's status axes.

### Intake decision boundary

| Concern              | Upstream pattern                                       | Required local disposition/control                                                                       |
| -------------------- | ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| Identity/personality | Strong persona voice and domain identity               | Do not import voice; rewrite only the job-to-be-done under an existing or approved owner.                |
| Scope                | General divisions and projects                         | Map to one of 14 repository scopes and concrete owned paths; stop if no owner exists.                    |
| Tools/services       | Agents may name external tools/services                | Review commands, MCP/web access, credentials, external writes, and paid services under least privilege.  |
| Model/effort         | Cross-tool portable definitions                        | Assign one typed local work profile; discard upstream model assumptions.                                 |
| Workflow             | Persona-specific process text                          | Map to the canonical lifecycle and four bounded loops; no parallel workflow authority.                   |
| Distribution         | Converter/installer writes provider-native directories | Prohibit direct/global install in research; canonical Stage 00 source first, then generated projections. |
| Provenance           | Public Git, files, scripts, license                    | Pin commit/file/license and preserve source/date in Stage 04 evidence.                                   |
| Security             | Third-party prompt and executable scripts              | Inspect offline as untrusted input; no execution or permission inheritance.                              |
| Evaluation           | Publisher descriptions and success metrics             | Compare representative tasks against existing roles with an approved rubric and independent reviewer.    |

The "Scope" row's phrase "one of 14 repository scopes" refers to the pack's
fixed 14-scope axis, not to `agent-catalog.yaml`'s own `scopes:` enum. Direct
re-read of that enum (`agent-catalog.yaml:8-16`) shows only 8 values are
actually assignable today: `agentic`, `architecture`, `common`, `docs`,
`infra`, `ops`, `qa`, `security`. An intake candidate proposing to land in
`backend`, `entry`, `frontend`, `meta`, `mobile`, or `product` cannot be
mapped to an existing scope at all — it would first need an approved
`agent-catalog.yaml` schema change adding the scope value, before any role
or function assignment could follow. See
[Agent model selection: the 8-of-14 scope gap](./m0002-agent-model-selection.md#full-role-to-profile-registry-and-the-8-of-14-scope-gap)
for the full per-scope breakdown; it is not repeated here to keep this leaf
a router rather than a duplicate policy body.

### Gaps and revalidation

- No workspace fixture or validator exercises the intake decision boundary
  itself (the 9-row table above); the `capability_intake` entries are
  recorded as data, and `agent_governance_contract.py` checks catalog
  structure, not whether an intake decision followed the documented safe
  adaptation sequence.
- The `product-discovery` intake row (`decision: defer`) has no recorded
  re-evaluation trigger or date; "defer" without a typed revisit condition
  can persist indefinitely without becoming a decision either way.
- This leaf inspects one sample upstream file
  (`engineering-backend-architect.md`) as illustrative texture, not a
  representative sample across the 17 divisions; a systematic intake
  evaluation of a specific capability gap would need its own targeted
  sample, not this leaf's single-file observation.
- The upstream repository's rendered landing page is not re-fetched on a
  defined cadence; only the pinned tree and the default-branch SHA are
  re-resolved. A future refresh should record the landing-page prose date
  alongside the SHA if the prose itself becomes load-bearing for any claim.

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

### Carried source-evidence claims

Source-evidence claims carried forward from the superseded 2026-07-05
research pack on 2026-08-19. Each states what the upstream evidence supports
and, where it matters more, what it does not.

- **The upstream converter drops every safety-bearing field.** The converter maps only `name`, `description` and `developer_instructions`. An imported definition therefore arrives with no model, no effort, no sandbox and no MCP constraint, and inherits whatever the session provides. That is why direct conversion is a security problem rather than a formatting one.
- **Upstream build guards converge with this repository's parity pattern.** The upstream catalog's build guards are recognizably the same pattern as this repository's parity checks: a declarative registry, a generator, and a check that fails when the two disagree. The convergence matters because it shows the pattern is transferable practice rather than workspace-specific invention.

### Converter and intake mechanics

The converter's retained mechanics are intentionally narrow: it retains the
agent name, description, and Markdown body, putting the body verbatim into
`developer_instructions`. It does not translate visual/persona fields. The
older statement that it discarded `name` or `description` is erroneous and is
not used here. The global installer destination is an operational boundary,
not an approved installation instruction.

The proposed intake path is: pinned-source/license audit → extract the job →
map it to a canonical role, skill, and permission/profile → produce a native
projection → independent review. A persuasive persona does not create tool,
path, credential, or deployment entitlement. Any adopted instruction must
still be checked against the canonical role and its scoped permission profile.

## Scope Implications

| Scope          | Application and disposition                                                                                                        |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `agentic`      | Owns catalog/intake/profile/projection changes; external identities remain reference-only until approved and generated.            |
| `architecture` | External architect capabilities may inform functions, but the enum-only local scope needs an ownership decision before a new role. |
| `backend`      | No current local application surface; reject/defer backend persona intake until a product/Spec creates one.                        |
| `common`       | Merge broadly reusable review knowledge into existing functions rather than duplicating roles.                                     |
| `docs`         | Preserve pin, license, claim dates, and migration evidence; external prose is not local policy.                                    |
| `entry`        | Gateway specialists map to adjacent infra ownership; no direct role import while the typed scope route is absent.                  |
| `frontend`     | Existing fixture ownership is not a product-role gap; require representative work and an approved owner before intake.             |
| `infra`        | DevOps/SRE capabilities already merge into existing infra/ops roles; tools and runtime writes remain approval-bound.               |
| `meta`         | Taxonomy/catalog mechanics route through docs/Stage 00; do not infer a new meta role from upstream breadth.                        |
| `mobile`       | No current surface; mobile personas remain deferred unless an approved lifecycle chain creates the domain.                         |
| `ops`          | Incident/SRE capability is merged into existing owners; external service assumptions and outcome claims are not adopted.           |
| `product`      | Upstream product roles remain deferred because the local typed route/owner is absent and stakeholder authority is human.           |
| `qa`           | Own candidate-role fixtures, comparative baseline, failure cases, and independent scoring before adoption.                         |
| `security`     | Inspect prompts/installers for injection, secrets, commands, external actions, dependencies, and permission expansion.             |

## Sources

| Source                                                                                                                                                                                       | Accessed                          | Class                       | Verification state                                                                                  |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- | --------------------------- | --------------------------------------------------------------------------------------------------- |
| [agency-agents immutable tree](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7)                                                                  | 2026-08-08T16:18:04+09:00         | External fixed              | Default-branch SHA resolved by `git ls-remote`; detached tree counted 17 divisions / 270 agents.    |
| [Pinned division registry](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/divisions.json)                                                       | 2026-08-08                        | External fixed              | Canonical division set and exclusion notes.                                                         |
| [Pinned Codex integration](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/integrations/codex/README.md)                                         | 2026-08-08                        | External fixed              | Converter/install design; not executed.                                                             |
| [Pinned MIT license](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/LICENSE)                                                                    | 2026-08-08                        | External fixed              | Distribution license only.                                                                          |
| [Workspace historical pin](https://github.com/msitarzewski/agency-agents/tree/8ef49232e02431f7ca4792b487e5a85a7939ff3a)                                                                      | retained from 2026-07-27 analysis | External fixed / historical | Prior workspace basis: 17 divisions / 269 agents; not used for the new current count.               |
| Agent catalog contract (retired path: `../../../00.agent-governance/contracts/agent-catalog.yaml`)                                                                                                          | 2026-08-08                        | Workspace tracked           | Complete 14-role, 24-function, 9-intake registry at Task 4 baseline.                                |
| Subagent protocol (retired path: `../../../00.agent-governance/subagent-protocol.md`)                                                                                                                       | 2026-08-08                        | Workspace tracked           | Scope, role, permission, model, and handoff boundary.                                               |
| [agency-agents default branch re-resolution](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7)                                                    | 2026-08-14T13:40:00+09:00         | External fixed              | `git ls-remote` re-run; identical SHA to the 2026-08-08 pin, confirming zero upstream drift.        |
| [agency-agents rendered landing page](https://github.com/msitarzewski/agency-agents)                                                                                                         | 2026-08-14T13:40:00+09:00         | External mutable            | HTTP 200; source of the "18+ divisions / 230+ agents / 395 commits" prose-vs-count mismatch.        |
| [Pinned Codex integration (re-read for exact mechanics)](https://raw.githubusercontent.com/msitarzewski/agency-agents/ebe9c99acb5c96f9468de368d8bead775387d1a7/integrations/codex/README.md) | 2026-08-14T13:40:00+09:00         | External fixed              | Re-read for exact TOML field list, discarded fields, and slug/name distinction.                     |
| [Pinned sample agent](https://raw.githubusercontent.com/msitarzewski/agency-agents/ebe9c99acb5c96f9468de368d8bead775387d1a7/engineering/engineering-backend-architect.md)                    | 2026-08-14T13:40:00+09:00         | External fixed              | One-file offline inspection; frontmatter fields, persona length, named tools, no model/credentials. |
| Canonical role files (retired path: `../../../00.agent-governance/agents/agents/`)                                                                                                                          | 2026-08-14                        | Workspace tracked           | Direct `wc -l`: 14 files, 672 tracked lines, confirming the local-density comparison.               |
| [Governance contract validator](../../../../scripts/lib/agent_governance/agent_governance_contract.py)                                                                                                 | 2026-08-14                        | Workspace tracked           | `EXPECTED_AGENT_COUNT = 14`, `EXPECTED_FUNCTION_COUNT = 24` at lines 69-70.                         |

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | `workflow-supervisor` maps an extracted job to a canonical role/skill/profile. | Compare against `roles/` and `registry.yaml`. | No projection created. |
| architecture | applies | Architecture owner reviews a catalog-derived responsibility split. | Inspect approved design evidence. | No role architecture changed. |
| common | applies | `code-reviewer` examines instructions for scope and hidden authority. | Review exact pinned body. | Pin does not make text safe. |
| docs | applies | `doc-writer` preserves provenance and license boundaries. | Check source pin and README aggregation. | No external catalog becomes canonical docs. |
| infra | applies | `infra-implementer` assesses user-global install location and filesystem permissions before any projection rollout. | Review an approved concrete target plan. | `~/.codex/agents` was untouched. |
| ops | applies | `ci-cd-engineer` owns a rollout/rollback runbook for any projected agent distribution. | Inspect approved rollout evidence. | No agent was activated. |
| qa | applies | `qa-engineer` defines acceptance cases for a proposed projection. | Inspect evaluation before adoption. | No projection evaluated. |
| security | applies | `security-auditor` reviews projected permissions and supply-chain pin. | Review license/pin and permission mapping. | Persona text grants no permissions. |

## 2026-09-05 Revalidation

Baseline: `main@4c6d211129615eab372d720ebd209b6c27618c86`.
The repository currently has 14 canonical roles and 23 canonical skills under
Stage 00, with generated provider projections. The upstream agency-agents
catalog now declares its division set in `divisions.json`; that moving catalog
is an intake source, not a repository role authority.

| Capability | Repository implementation | Evidence depth | Gap | Verification route |
| --- | --- | --- | --- | --- |
| Canonical role catalog | Stage 00 role files with generated native adapters | Repository-enforced | Runtime tool effectiveness varies | provider-surface renderer and contract checks |
| Skill catalog | Stage 00 skill sources project to `.agents/skills` and `.claude/skills` | Repository-enforced | No outcome benchmark for every skill | task-specific eval and review |
| External intake | Research compares upstream roles before admission | Defined | No automatic trust or sync | fixed-commit review, threat model, separate Spec |

Recommendation: admit an external role only when it fills a proved capability
gap and can be expressed with existing permissions and ownership. Re-opened
upstream authority: [agency-agents divisions](https://github.com/msitarzewski/agency-agents/blob/main/divisions.json).

## Maintenance

Re-resolve the default-branch SHA and rerun the exact immutable-tree count only
when an intake decision or catalog refresh needs current upstream facts. Keep
historical and current pins separate; never replace a pin with `main` in a
load-bearing citation.

## Related Documents

- [Agent instructions](./m0001-agent-instructions-vibe-coding.md)
- [Agent model selection](./m0002-agent-model-selection.md)
- [Workspace baseline](./m0020-workspace-baseline.md)
- [Scope application matrix](./m0015-scope-application-matrix.md)
- Execution Task (retired path: `../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`)
