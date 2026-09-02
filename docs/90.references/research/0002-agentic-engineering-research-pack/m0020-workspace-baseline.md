---
title: "Reference: Agentic Engineering Workspace Baseline"
version: 1.0.0
type: reference/research
layer: references
status: active
owner: "@buenhyden"
artifact_id: RES-0002-m0020
parent_ids: [RES-0002]
created: 2026-08-23
updated: 2026-09-01
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# Reference: Agentic Engineering Workspace Baseline

## Overview

This reference is the measured workspace-state entry point for the agentic
engineering research pack. It records tracked corpus, agent-system, delivery,
documentation, infrastructure, and scope counts at Git commit
`528c225d35d6c986b50f9b997fd08921a8df9a9b` on 2026-08-08, re-derived at commit
`55809319e462ed6ae9ed4a3f31055fc55c2a2294` on 2026-08-11, and re-derived again
at commit `ece3eda9c3e1a603c6495dd55caba7df1c29ef6c` on 2026-08-14. Earlier
commits remain valid historical provenance for counts that did not change
between measurements; where a count moved, this document states the delta and
its cause rather than silently replacing the number.

The baseline is Stage 90 analysis. It supports later research leaves but does
not become policy, runtime truth, remote-enforcement proof, or execution
evidence merely because another document cites it.

## Purpose

Provide REQ-31 with one reproducible, current baseline for every research-pack
category. Later leaves can cite this document for corpus cardinalities and
evidence boundaries instead of copying historical counts from the predecessor
pack.

A second purpose, added by the 2026-08-14 deepening, is to make the baseline
answerable rather than merely quotable: for each class of fact, name which
tracked artifact owns it, which command re-derives it, and where no owner
exists at all.

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
- The original nineteen-leaf baseline and the approved Task 9a amendment that
  adds `verification-validation.md` as the twentieth research leaf.
- Read-only validator executions performed for this baseline, reported with the
  interpreter they ran under.

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
five evidence classes and never promotes one into another:

- **Tracked definition**: a Git-visible file, typed registry, or stage
  artifact. Establishes that something is declared.
- **Local observation**: a safe command or validator run captured for this
  Task, reported with its interpreter and exit status. Establishes that a check
  executed here, not that it executes in CI.
- **Runtime or remote state**: state requiring container, provider, or remote
  control-plane evidence; it remains unverified here.
- **External comparison**: primary-source context that does not establish local
  adoption.
- **Historical retained**: a predecessor measurement preserved for delta
  analysis and explicitly not re-asserted as current.

Implementation labels are `Implemented`, `Partial`, `Missing`, `Not
Applicable`, and `Unverified`. `Implemented` means the tracked contract or
surface exists; it never upgrades runtime or remote evidence.

Three external practices anchor this separation and are cited only as
comparison, never as local authority:

- SLSA v1.1 provenance describes _how_ an artifact was produced through
  `buildDefinition` and `runDetails`; it does not assert properties of the
  artifact itself, and it separates `externalParameters` (untrusted, MUST be
  verified downstream) from `internalParameters` (trusted only because the
  platform is trusted). The same asymmetry applies here: a tracked contract is
  an internal parameter of this repository, while any claim about provider or
  remote behavior is an external parameter this baseline cannot verify.
- The Model Context Protocol 2026-07-28 specification states that "MCP itself
  cannot enforce these security principles at the protocol level" and makes
  capability negotiation per-request rather than a one-time handshake. A
  declared capability is a contract, not an execution guarantee.
- GitHub `CODEOWNERS` assigns reviewers but does not enforce review; the vendor
  documentation is explicit that enforcement requires branch protection or a
  ruleset. A tracked ownership file is therefore `Tracked definition`, and its
  enforcement is `Runtime or remote`.

### Reproducible baseline measurements

All results use the 2026-08-14 re-derivation commit unless marked otherwise.
Counts from `git ls-files` exclude ignored-local and untracked paths. The
`Delta` column compares against the 2026-08-11 measurement.

| Measurement                                | Derivation                                                |    Result | Delta |
| ------------------------------------------ | --------------------------------------------------------- | --------: | ----- |
| Tracked paths                              | `git ls-files \| wc -l`                                   |     1,673 | +1    |
| Normative persona scopes                   | sorted `find .../scopes -maxdepth 1 -type f -name '*.md'` |        14 | —     |
| Typed governance contracts                 | `git ls-files docs/00.agent-governance/contracts`         |         3 | —     |
| Typed catalog scopes                       | `scopes` in `agent-catalog.yaml`                          |         8 | —     |
| Typed agents / functions                   | `agents` and `functions` in `agent-catalog.yaml`          |   14 / 24 | —     |
| Work profiles / model records              | `work_profiles` and `models` in `provider-models.yaml`    |    5 / 11 | —     |
| Harness layers / loops / workflow states   | typed provider-model collections                          | 8 / 4 / 8 | —     |
| Capability-intake decisions                | `capability_intake` in `agent-catalog.yaml`               |         9 | —     |
| Path-authority records / artifact profiles | `agent-governance-artifacts.yaml`                         |    7 / 25 | —     |
| Synthetic fixtures / regressions           | catalog `evaluation.fixture_count` / `regression_count`   |   11 / 16 | —     |
| Active Spec directories                    | `find docs/03.specs -mindepth 1 -maxdepth 1 -type d`      |        28 | —     |
| Archived `spec.md` files                   | `find docs/98.archive/03.specs -type f -name spec.md`     |        32 | —     |
| Workflow files / declared jobs             | tracked workflow YAML parsed in the isolated environment  |    7 / 23 | —     |
| Script files / validation scripts          | `git ls-files scripts` and `scripts/validation`           |   64 / 42 | —     |
| Test files / validation tests              | `git ls-files tests` and `tests/validation`               |   58 / 26 | —     |
| Compose-named YAML files                   | `git ls-files '*docker-compose*.yml'`                     |        49 | —     |
| Infrastructure files / numbered domains    | `git ls-files infra`; first-level numbered directories    |  275 / 11 | —     |
| Template files / pre-commit repositories   | tracked `99.templates/templates/**`; `repo` rows          |   33 / 10 | —     |
| Pre-commit hook entries                    | sum of `hooks` across all configured repositories         |        24 | —     |
| TSX/JSX files / mobile source files        | tracked extension queries                                 |     6 / 0 | —     |

The single `+1` delta is the new Stage 04 Task
`docs/04.execution/tasks/2026-08-14-agentic-research-pack-deepening.md`,
confirmed by `git diff --name-status 55809319 HEAD --diff-filter=A`. No other
tracked path was added, removed, or renamed between the two measurements, so
every `—` row above is a genuine re-derivation rather than a forwarded copy.

### Whole-repository path census

The 1,673 tracked paths decompose exactly as follows. This census is the
denominator for any corpus proportion a later leaf computes.

| Root            | Files | Character                                                   |
| --------------- | ----: | ----------------------------------------------------------- |
| `docs/`         |   980 | Nine numbered stages plus the corpus index.                 |
| `infra/`        |   275 | Eleven numbered domains plus ten root policy/config files.  |
| `scripts/`      |    64 | Validation, operations, security, knowledge, hooks.         |
| `tests/`        |    58 | 26 validation tests, 31 fixtures, one index.                |
| `projects/`     |    52 | One Storybook/Next fixture (50 files) plus two indexes.     |
| `.claude/`      |    48 | Claude-native adapter surface.                              |
| `graphify-out/` |    47 | Generated graph artifacts, tracked but not authored.        |
| `.agents/`      |    41 | Provider-neutral compatibility and shared-skill surface.    |
| (root files)    |    26 | Shims, lint/format configs, root Compose, `llms.txt`.       |
| `secrets/`      |    19 | Bind-mount placeholders and examples only; no values.       |
| `.github/`      |    17 | Workflows, contract, CODEOWNERS, ruleset record, templates. |
| `.gemini/`      |    17 | Gemini-native adapter surface.                              |
| `.codex/`       |    16 | Codex-native adapter surface.                               |
| `examples/`     |     9 | Illustrative material outside the lifecycle stages.         |
| `_workspace/`   |     2 | Scratch-adjacent tracked placeholders.                      |
| `archive/`      |     1 | Root archive placeholder, distinct from `docs/98.archive`.  |
| `.rtk/`         |     1 | Local tooling filter declaration.                           |

Two entries need an explicit evidence note. `graphify-out/` is 47 tracked files
of _generated_ content inside the tracked corpus, so any path total mixes
authored and generated material and a leaf reasoning about authoring effort
must subtract it. `secrets/` is 19 tracked files that are placeholders by
construction — a README, a `.example`, and `.gitkeep` markers — so its presence
in the census is not evidence that a secret value is tracked, and no file under
it was opened for this baseline.

### Source-language census

Language counts are a stronger negative test than directory counts, because a
scope can claim a stack that no tracked file uses.

| Extension | Files | Where they live                                    |
| --------- | ----: | -------------------------------------------------- |
| `.sh`     |    61 | `scripts/`, provider hook wrappers, infra helpers. |
| `.py`     |    45 | `scripts/` and `tests/` only; zero elsewhere.      |
| `.ts`     |    10 | `projects/storybook/nextjs/` only.                 |
| `.tsx`    |     6 | `projects/storybook/nextjs/` only.                 |
| `.sql`    |     5 | Infrastructure data-domain assets.                 |

No tracked file matched `.go`, `.rs`, `.java`, `.kt`, `.swift`, `.dart`, `.rb`,
`.php`, `.cs`, `.js`, or `.jsx`. Exactly one `package.json` is tracked, at
`projects/storybook/nextjs/`. The repository therefore has no tracked backend
application, no tracked mobile application, and exactly one bounded frontend
fixture. This is the derivation behind the `backend` and `mobile` dispositions
in the scope matrix, and it is a negative result produced by enumeration rather
than an assumption.

### Documentation corpus

| Canonical surface                                             | Files | Interpretation                                                                           |
| ------------------------------------------------------------- | ----: | ---------------------------------------------------------------------------------------- |
| [Stage 00 governance](../../../00.agent-governance/README.md) |   110 | Policy, scopes, agents, functions, typed contracts, provider rules, Memory.              |
| [Stage 01 requirements](../../../01.requirements/README.md)   |    26 | Active product-intent corpus including its index.                                        |
| [Stage 02 architecture](../../../02.architecture/README.md)   |    53 | 26 requirement-path files, 26 decision-path files, and the stage index.                  |
| [Stage 03 specifications](../../../03.specs/README.md)        |    53 | 28 active Spec directories; file and directory counts answer different questions.        |
| Stage 04 execution (retired path: `../../../04.execution/README.md`)         |   239 | 104 Plan-path files, 134 Task-path files, and the stage index.                           |
| [Stage 05 operations](../../../05.operations/README.md)       |   263 | 88 guide, 87 policy, 85 runbook, one incident index, one release index, one stage index. |
| [Stage 90 references](../../../90.references/README.md)       |   118 | 42 research, 39 audits, 30 data, 3 LLM Wiki, 3 learning, one stage index.                |
| [Stage 98 archive](../../../98.archive/README.md)             |    69 | Historical tombstones and archived lifecycle evidence, including 32 Specs.               |
| [Stage 99 templates](../../../99.templates/README.md)         |    48 | Template sources and support contracts; 33 files are under the template tree.            |

Stage 04 moved from 238 to 239 for the single reason recorded above. The Stage
90 row is unchanged at 118 but its internal split is stated here for the first
time: the 42 research files are this twenty-one-file pack plus the
twenty-one-file predecessor pack, which is why a research-file count alone
cannot distinguish canonical from superseded material.

### Stage 00 internal decomposition

Stage 00 is the layer every other leaf routes against, so its 110 files are
decomposed rather than totalled.

| Subtree      | Files | Content                                                               |
| ------------ | ----: | --------------------------------------------------------------------- |
| `agents/`    |    39 | 14 agent-role documents, 24 function documents, one catalog index.    |
| `rules/`     |    36 | 17 rule documents plus 19 Hookify rules under `rules/hooks/`.         |
| `scopes/`    |    14 | One document per normative persona scope.                             |
| `memory/`    |    11 | `README.md`, `current.md`, `progress.md`, and eight durable notes.    |
| `providers/` |     4 | `agents-md.md` plus one overlay each for Claude, Codex, and Gemini.   |
| `contracts/` |     3 | The three typed YAML contracts described below.                       |
| (root)       |     3 | `README.md`, `harness-implementation-map.md`, `subagent-protocol.md`. |

The `agents/` subtree is exactly `14 + 24 + 1`, matching the typed catalog's
agent and function cardinality with no orphan document and no undocumented
catalog entry. That one-to-one correspondence is the strongest catalog-integrity
fact in the baseline, and it is machine-checked below.

### Typed contract inventory

Prior revisions of this baseline named two typed contracts. There are three.
Naming only two understates the governed surface, because the third contract
carries path authority and document profiles.

| Contract                          | Collections                                                                                                                       | Governs                                                               |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `agent-catalog.yaml`              | 4 projection targets, 8 scopes, 2 permission profiles, 14 agents, 24 functions, 9 capability-intake decisions, 1 evaluation block | Which roles and functions exist, in which scope, at which permission. |
| `provider-models.yaml`            | 3 providers, 1 compatibility surface, 5 work profiles, 11 models, 8 harness layers, 8 workflow states, 4 loops, 7 semantic events | Which provider and model a work profile may use, and how loops run.   |
| `agent-governance-artifacts.yaml` | 3 governed families, 25 artifact profiles, 3 root shims, 3 README profiles, 7 path-authority records, 1 path-pattern limit block  | Which document profile each governed path takes, and who owns it.     |

`agent-governance-artifacts.yaml` is the only one of the three whose file
modification time moved since the 2026-08-08 baseline; the role and model
contracts retain their 2026-07-26 content. That asymmetry matters for freshness
reasoning: the older contracts are older by design, not by neglect.

The evaluation block inside `agent-catalog.yaml` names its own owner
(`eval-engineer`), reviewer (`code-reviewer`), fixture catalog, scorer, runner,
and test path, and declares `fixture_count: 11`, `regression_count: 16`,
`input_classification: synthetic-fixture`, and two input roots. It is the one
place in the typed system where a contract states not only what exists but how
its own conformance is measured.

### Provider surface decomposition and projection parity

Adapter file counts alone hide the load-bearing fact: role projection and
function projection have different declared reach.

| Surface    | Files | Composition                                                                     |
| ---------- | ----: | ------------------------------------------------------------------------------- |
| `.claude/` |    48 | 1 `CLAUDE.md`, 14 agents, 24 skills, 7 hook wrappers, 1 output style, settings. |
| `.agents/` |    41 | 1 `README.md`, 14 agents, 24 skills, 1 rules file, 1 workflows file.            |
| `.gemini/` |    17 | 1 `README.md`, 14 agents, 1 hook wrapper, settings.                             |
| `.codex/`  |    16 | 1 `README.md`, 14 agent TOMLs, `hooks.json`.                                    |

Every agent record declares `provider_projections: [agents-md, claude, codex,
gemini]`, so 14 roles times 4 targets equals 56 role adapters, and the tracked
count is exactly 56. Every function record declares
`provider_projections: [agents-md, claude]` only, so 24 functions times 2
targets equals 48 skill projections, and the tracked count is exactly 48. The
absence of skill bodies under `.codex/` and `.gemini/` is therefore a
**contract-declared boundary, not adapter drift** — a distinction that a raw
file-count comparison inverts. Any leaf that wants Codex or Gemini skills must
first change `provider_projections` in the typed catalog, and that change is
owned by the Stage 00 catalog owner.

`.claude/settings.local.json` exists on disk and is not tracked. The
predecessor pack recorded `.claude/` at 49 files because it counted the local
override; today's tracked 48 reflects the settings-SSOT rule that personal
overrides stay out of Git. That is a `Historical retained` delta with a known
cause, not a lost file.

### Instruction entry-point asymmetry

The three root shims are near-identical in size but not in behavior, and the
difference is measurable without any runtime observation.

| Shim        | Bytes | Import style                         | Auto-expanding body at this commit |
| ----------- | ----: | ------------------------------------ | ---------------------------------: |
| `CLAUDE.md` |   205 | 4 `@path` imports, depth 1           |    20,543 B across 5 tracked files |
| `GEMINI.md` |   213 | 4 `@./path` imports, depth 1         |    19,009 B across 5 tracked files |
| `AGENTS.md` |   243 | numbered prose steps, no auto-import |                              243 B |

The expanded chain resolves `rules/bootstrap.md` (4,203 B), the matching
provider overlay (`providers/claude.md` 6,771 B, `providers/gemini.md`
5,229 B), `memory/README.md` (5,675 B), and `memory/current.md` (3,689 B).
None contains a further import, so the chain is one hop deep.
`memory/current.md` is 76 lines and 3,689 B against its own declared bound of
400 lines and 32 KiB, so it sits at roughly 11 percent of its size budget.

The predecessor pack measured the Claude chain at 24,597 B on 2026-08-07;
today it is 20,543 B. The entire 4,054 B reduction is accounted for by
`memory/current.md` shrinking from 7,743 B to 3,689 B, with no other chain
member changing size. Recording the delta this precisely is what lets a later
leaf treat the shim chain as a monitored budget rather than a one-off number.

The asymmetry itself is the durable finding: a Claude or Gemini session
receives roughly 20 KiB of governance automatically, while an `AGENTS.md`
session receives 243 B and must be trusted to read the rest with tools. This is
a `Tracked definition` about import syntax. Whether any runtime performs the
expansion is `Unverified` here.

### Agent, provider, and harness system

The typed agent catalog (retired path: `../../../00.agent-governance/contracts/agent-catalog.yaml`)
contains 14 agents and 24 functions. Its eight-value scope enum is `agentic`,
`architecture`, `common`, `docs`, `infra`, `ops`, `qa`, and `security`.

Agent records use seven of those values: `agentic` 4, `common` 1, `docs` 1,
`infra` 3, `ops` 2, `qa` 2, `security` 1. Function records use all eight:
`agentic` 4, `architecture` 2, `common` 2, `docs` 2, `infra` 4, `ops` 4, `qa`
4, `security` 2. The frequently repeated statement that `architecture` "has no
current agent record" is correct but incomplete — `architecture` carries two
active function records (`adr-writing`, `requirements-to-design-agent`) whose
owner agents are declared in other scopes. The corrected disposition lives in
[the scope application matrix](./m0015-scope-application-matrix.md).

Orthogonal agent axes, all re-derived from the contract:

| Axis                 | Distribution                                                                                                           |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `category`           | 7 implementation-operations, 6 review-evaluation, 1 supervisor.                                                        |
| `tier`               | 13 worker, 1 supervisor.                                                                                               |
| `permission_profile` | 7 `workspace-write`, 7 `read-only` — an exact split.                                                                   |
| `work_profile`       | 6 complex-implementation, 5 adversarial-review, 1 evidence-research, 1 routine-validation, 1 long-horizon-supervision. |

The 7/7 permission split is not a coincidence of counting: every
`implementation-operations` agent holds `workspace-write`, and every
`review-evaluation` agent plus the supervisor holds `read-only`. Mutation
authority and review authority are disjoint by construction in the typed
contract. Whether a runtime enforces that split is `Unverified`.

The exact six normative persona scopes outside the typed enum are `backend`,
`entry`, `frontend`, `meta`, `mobile`, and `product`. That is a catalog-routing
finding, not proof that their subject matter is absent.

The provider-model contract (retired path: `../../../00.agent-governance/contracts/provider-models.yaml`)
defines 3 providers, 1 compatibility surface, 5 work profiles, 11 model
records, 8 harness layers, 8 workflow states, 4 harness loops, and 7 semantic
events. Each model record carries separate `provider_lifecycle`,
`repository_disposition`, `runtime_acceptance`, and `entitlement` fields, which
is the contract's own acknowledgement that a catalogued model is not an
available model. These are definitions; provider loading, entitlements, event
interception, and model execution are unverified here.

### Delivery and quality surface

| Surface                                                   | Measurement                             |
| --------------------------------------------------------- | --------------------------------------- |
| Workflow files / declared jobs                            | 7 / 23                                  |
| Jobs in `ci-quality.yml` alone                            | 16                                      |
| `job_roots` in `.github/workflow-contract.yml`            | 16                                      |
| Required checks named in the tracked ruleset record       | 16                                      |
| `gate_nodes` / pinned action identities                   | 80 / 8                                  |
| Pre-commit repositories / hook entries                    | 10 / 24                                 |
| `.github/CODEOWNERS` path rules                           | 30, all resolving to one GitHub account |
| CODEOWNERS patterns required by `check-repo-contracts.sh` | 11                                      |

The 16/16/16 alignment between `ci-quality.yml` jobs, the workflow contract's
`job_roots`, and the ruleset record's required-check list is a genuine
three-way tracked consistency and the strongest delivery-side fact available
without remote access. It remains `Tracked definition`: the ruleset file itself
states that "control-plane verification is `unverified`" and that the proposal
"does not apply remote repository settings by itself".

`.github/CODEOWNERS` is easily over-interpreted. It contains 30 path rules,
every one assigning the same single human account. It encodes none of the
fourteen scopes and none of the fourteen agent identities. Under GitHub's
documented "last matching pattern takes the most precedence" rule, and because
all rules resolve to one owner, the file is functionally equivalent to its own
`*` catch-all line. Its value is as a required-review hook once a ruleset is
applied — not as an ownership model. The validator requires only 11 of its 30
patterns, and `docs/01.requirements/`, `docs/02.architecture/`,
`docs/04.execution/`, `projects/`, and `tests/` have no rule beyond the
catch-all.

### Evidence-owner assignment and ownerless fact classes

The question this baseline previously left implicit is _who owns each class of
fact_. The table assigns an owner where one exists and names the absence where
one does not.

| Fact class                                 | Evidence owner                                         | Status                    |
| ------------------------------------------ | ------------------------------------------------------ | ------------------------- |
| Tracked path inventory                     | the Git index itself                                   | Owned                     |
| Agent / function / scope-enum cardinality  | `contracts/agent-catalog.yaml`                         | Owned and machine-checked |
| Provider, model, harness, loop cardinality | `contracts/provider-models.yaml`                       | Owned and machine-checked |
| Document profiles and path authority       | `contracts/agent-governance-artifacts.yaml`            | Owned and machine-checked |
| Document frontmatter conformance           | `99.templates/support/document-metadata-profiles.yaml` | Owned                     |
| Workflow job identity                      | `.github/workflow-contract.yml`                        | Owned                     |
| Scope-file frontmatter                     | `tests/validation/test_agent_governance_contract.py`   | Owned for 13 of 14 files  |
| Persona-to-scope mapping                   | `rules/persona.md`                                     | **No validator owner**    |
| Prose "File Ownership SSOT" tables         | six scope files                                        | **No validator owner**    |
| Provider runtime acceptance                | none tracked                                           | **No owner**              |
| Applied branch protection and rulesets     | a tracked _proposal_ only                              | **No owner**              |
| Live Compose and service health            | none tracked                                           | **No owner**              |
| Deployment and release promotion           | none tracked                                           | **No owner**              |

Two rows are new findings rather than restatements. First, the scope-file
frontmatter test enumerates thirteen scope names at
`tests/validation/test_agent_governance_contract.py:1955-1967` and omits
`docs`, so `docs.md` is the one scope file whose `layer:` frontmatter no test
asserts. Second, no file under `scripts/` or `tests/` contains the string
`File Ownership`, so the prose ownership tables carried by six scope files are
entirely unvalidated while the seven typed `path_authority` records are
validated on every run. The repository has one machine-checked ownership system
and one prose ownership system, and they do not overlap.

### Executed checks at this baseline

These are `Local observation` results, not CI results. Every command was run
for this Task on 2026-08-14 at commit `ece3eda9`, and the outcome reported is
the outcome observed. "Isolated" means an environment built from
`scripts/requirements.txt`.

| Command                                                              | Interpreter | Result                                                              |
| -------------------------------------------------------------------- | ----------- | ------------------------------------------------------------------- |
| `check-agent-governance-contract.py --mode contract`                 | default     | exit 1, `AGC-DEPENDENCY-MISSING path=html5lib`                      |
| `check-agent-governance-contract.py --mode contract`                 | isolated    | `PASS contracts=3 agents=14 functions=24 providers=3 failures=0`    |
| `check-agent-governance-contract.py --mode repository --section all` | isolated    | `PASS mode=repository section=all failures=0`                       |
| `unittest tests.validation.test_agent_governance_contract`           | default     | 159 tests, 26 failures and 338 errors, all from the same dependency |
| `unittest tests.validation.test_agent_governance_contract`           | isolated    | 159 tests, `OK`, 272.6 s                                            |

Three conclusions follow, and only these three. The typed contract set is
internally consistent at this commit, and the validator's own output
independently confirms `contracts=3`, `agents=14`, `functions=24`, and
`providers=3`. The governance test suite passes in full when its declared
dependencies are present. And the default interpreter in this workspace cannot
run either check, because `html5lib` is declared at `scripts/requirements.txt`
line 4 but absent from the interpreter — the pre-existing, unowned
validation-runtime gap already recorded in governance Memory. None of this says
anything about whether the same checks pass in hosted CI, which is
`Unverified`.

### Research-category readiness

This table preserves the original nineteen-leaf baseline contract plus the
approved 2026-08-09 amendment's twentieth row for V&V. The 2026-08-14
re-derivation updates the counts this table cites; it does not change any
leaf's implementation status. `Current evidence` is a tracked starting point,
not a substitute for each leaf's own source and claim review.

| Research leaf / category                | Current tracked evidence                                                   | Baseline state and limit                                                                                                                                                                |
| --------------------------------------- | -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `workspace-baseline.md`                 | 1,673-path inventory, 3 typed registries, 5 executed checks                | Implemented by this draft; independent review pending.                                                                                                                                  |
| `scope-application-matrix.md`           | 14 scope files, persona map, 8-value enum, 7 path-authority records        | Implemented by its companion draft; independent review pending.                                                                                                                         |
| `harness-engineering.md`                | 8 typed harness layers and provider adapters                               | Partial; definitions exist, live provider execution is unverified.                                                                                                                      |
| `loop-engineering.md`                   | 4 typed harness loops and 8 workflow states                                | Partial; deterministic contracts exist, live feedback behavior is unverified.                                                                                                           |
| `provider-implementation-comparison.md` | 4 adapter projections, 3 provider records, 56 role adapters, 48 skills     | Partial; tracked parity is measurable, provider-native execution is not.                                                                                                                |
| `agent-instructions-vibe-coding.md`     | root shims, bootstrap, scopes, and adapter rules                           | Partial; tracked instructions exist, behavioral compliance is evidence-specific.                                                                                                        |
| `provider-model-landscape.md`           | 11 model records across 3 providers                                        | Partial; catalog facts exist, current entitlements and acceptance are unverified.                                                                                                       |
| `agent-model-selection.md`              | 5 work profiles, typed tiers/effort/fallback fields                        | Partial; selection contract exists, live comparative evaluation is unverified.                                                                                                          |
| `ai-agent-catalogs.md`                  | 14 local agents, 24 functions, 9 intake decisions                          | Partial; local import boundary exists, external catalog comparison remains later work.                                                                                                  |
| `memory-hierarchy.md`                   | Memory README/current route, 8 durable notes, one typed memory fixture     | Partial; policy covers bounded governance Memory, not a complete domain-memory lifecycle.                                                                                               |
| `spec-driven-sdlc.md`                   | 28 active Spec directories and 239 Stage 04 files                          | Implemented as a document system; enforcement strength requires per-gate evidence.                                                                                                      |
| `sdlc-document-roles.md`                | registered profiles and templates across Stages 01-05                      | Implemented as metadata contracts; an artifact does not prove its intended outcome.                                                                                                     |
| `document-metadata-lifecycle.md`        | metadata profile registry and two document lifecycle validators            | Implemented for registered surfaces; current command result belongs in Task evidence.                                                                                                   |
| `documentation-architecture.md`         | staged corpus plus 33 template-tree files                                  | Partial; repository taxonomy exists, Diataxis comparison remains later work.                                                                                                            |
| `llm-wiki-system.md`                    | 3 tracked LLM Wiki files and 3 knowledge scripts                           | Partial; Task 1 preserved stale index/coverage predecessors for the route-switch unit.                                                                                                  |
| `automation-pipeline-workflow.md`       | 64 scripts, 7 workflows, 23 jobs, an 80-node workflow gate contract        | Partial; tracked orchestration exists, remote execution and deployment are unverified.                                                                                                  |
| `quality-ci-formatting.md`              | 42 validation scripts, 26 validation tests, 10 pre-commit repos, 24 hooks  | Partial; local gates exist, remote required-check enforcement is unverified.                                                                                                            |
| `docker-compose-infrastructure.md`      | 49 Compose-named YAML files in 11 infra domains                            | Partial; definitions exist, no containers were started, runtime health is unverified.                                                                                                   |
| `security-governance.md`                | hardening, security, validation, incident, and supply-chain surfaces       | Partial; controls are tracked, secret values were not inspected, runtime/remote enforcement is unverified.                                                                              |
| `verification-validation.md`            | Task 9a base `ac51a532`; 14 scopes, typed workflow, named freshness owners | Implemented as cross-system V&V analysis; static verification is strong, provider, hosted GitHub, Compose runtime, release acceptance, and residual-risk authority remain `UNVERIFIED`. |

### Workspace adoption environment and rules

1. Route changes to the canonical owner named by Stage 00 or the lifecycle
   stage; a Stage 90 recommendation is never the change owner.
2. For a tracked workspace claim, cite the owner path, baseline commit, and a
   reproducible identifier or command. Re-measure rather than forward-copying a
   historical count.
3. Keep provider capability, local adapter definition, local execution, runtime
   state, and remote enforcement as separate evidence fields.
4. Apply explicit approval boundaries before Stage 01-99 mutation, runtime or
   Compose mutation, secret-value access, remote mutation, or provider changes.
5. Use the isolated validation environment required by the active Plan for the
   repository contract. Preserve unrelated failures rather than relabeling them
   as passes or widening this unit's scope.
6. When a count changes between baselines, state the delta and its cause. A
   silently replaced number destroys the provenance that makes the baseline
   reusable.
7. Do not aggregate authored and generated tracked files without saying so. The
   47 tracked `graphify-out/` files and the 42 tracked Stage 90 research files
   both mix categories that a naive total would conflate.

### Implementation status, limitations, and gaps

The workspace has substantial tracked implementation for all research groups
except current mobile and backend application surfaces. The highest-confidence
counts come from typed registries validated by an executed check, and from Git
path enumeration. The largest verification boundary is outside Git: no claim
here proves live Compose health, provider behavior, GitHub rulesets, deployment
promotion, private configuration, or secret hygiene.

Current gaps, each paired with the observation that would close it:

| Gap                                                                                      | First owner                       | Closing observation                                                                          |
| ---------------------------------------------------------------------------------------- | --------------------------------- | -------------------------------------------------------------------------------------------- |
| Six persona scopes outside the enum; `architecture` admitted with functions but no agent | Stage 00 catalog owner            | A contract change, or a recorded decision that the enum is intentionally narrower.           |
| `docs` missing from the scope-frontmatter test tuple                                     | Stage 00 validator/test owner     | Adding the fourteenth name and observing the suite still pass.                               |
| Prose ownership tables unvalidated and disjoint from typed `path_authority`              | Stage 00 catalog owner            | A validator that reads the prose tables, or a decision that typed authority supersedes them. |
| `html5lib` declared but absent from the default interpreter                              | unowned; pre-existing             | Adding the dependency to the standard environment and re-running both checks there.          |
| Domain-memory lifecycle beyond bounded governance Memory                                 | a future approved Stage 03 Spec   | An approved Spec defining non-governance memory retention.                                   |
| CD promotion and deployment evidence                                                     | a future approved delivery chain  | A recorded deployment with its own artifact.                                                 |
| Applied remote branch protection and required checks                                     | repository owner                  | Authenticated `gh api` readback of rulesets and branch protection.                           |
| Provider runtime acceptance of adapters, hooks, and models                               | separately approved evidence task | A live provider session recorded as runtime evidence.                                        |
| Live Compose health for 49 tracked definitions                                           | separately approved runtime unit  | A runtime unit with pre-check, change, and post-check evidence.                              |

### Carried source-evidence claims

Source-evidence claims carried forward from the superseded 2026-07-05
research pack on 2026-08-19. Each states what the upstream evidence supports
and, where it matters more, what it does not.

- **The tracked Codex session-end record conflicts with upstream.** `contracts/provider-models.yaml` records the Codex `session-end` binding as `unsupported` with a null native event, while Codex documents `SessionEnd`, which makes the tracked record stale rather than merely incomplete. The upstream half is a dated observation carried from the retiring pack and was not re-fetched here, so it is `UNVERIFIED` as a current capability claim; the repository half is directly checkable in the named contract.

## Scope Implications

The companion [scope matrix](./m0015-scope-application-matrix.md) is the normative
scope-axis map for this pack. This baseline's own disposition is summarized
below so a topic-first reader encounters all fourteen scopes.

| Scope          | Baseline implication                                                                                                        |
| -------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `agentic`      | Direct: 3 typed contracts, 110 Stage 00 files, 56 role adapters, 48 skill projections, harness/loop/model counts.           |
| `architecture` | Direct: 53 Stage 02 files and 28 active Spec directories; enum-admitted with 2 functions and 0 agents.                      |
| `backend`      | Not applicable: enumeration found 0 tracked service files in any stack the scope claims.                                    |
| `common`       | Direct: 10 pre-commit repositories, 24 hook entries, shared review route; claimed root `common/`, `lib/`, `shared/` absent. |
| `docs`         | Direct: 980 tracked `docs/` files, 33 template-tree files, metadata registry; the one scope file no test asserts.           |
| `entry`        | Direct but routing-limited: 16 tracked gateway files; scope is outside the typed catalog.                                   |
| `frontend`     | Limited: one tracked `package.json`, 51 Storybook files, 16 `.ts`/`.tsx` files; no product frontend is proven.              |
| `infra`        | Direct: 275 infra files, 11 numbered domains, 49 Compose definitions, 11 Dockerfiles; runtime unverified.                   |
| `meta`         | Direct but routing-limited: 25 typed artifact profiles, 3 README profiles, 3 governed families; outside the enum.           |
| `mobile`       | Not applicable: 0 tracked Swift, Kotlin, Dart, Java, Android, or iOS source files matched the enumeration.                  |
| `ops`          | Direct: 263 Stage 05 files, 99 observability files, 8 operations scripts; service outcomes remain unverified.               |
| `product`      | Direct but routing-limited: 26 Stage 01 files; the catalog records an explicit `defer` on product-discovery capability.     |
| `qa`           | Direct: 42 validation scripts, 26 validation tests, 31 fixtures, 7 workflows, 23 jobs, 11 fixtures and 16 regressions.      |
| `security`     | Direct: tracked hardening/supply-chain/incident surfaces and 19 placeholder-only `secrets/` files; no value inspected.      |

## Sources

| Source                                                                                                 | Accessed   | Class                  | Verification state                                                                                                                                                                                                                              |
| ------------------------------------------------------------------------------------------------------ | ---------- | ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [SPEC-0158 preservation contract](../../../03.specs/0158-document-governance-lifecycle-convergence/spec.md) | 2026-08-14 | Tracked fixed baseline | Re-verified; REQ-31 and the twenty-leaf/twenty-one-file counts are unchanged since the 2026-08-11 access. |
| Implementation Plan (retired path: `../../../04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md`)         | 2026-08-14 | Tracked mutable        | Re-verified; REQ-31's derivations are unchanged.                                                                                                                                                                                                |
| Agent catalog (retired path: `../../../00.agent-governance/contracts/agent-catalog.yaml`)                             | 2026-08-14 | Tracked mutable        | Re-parsed at `ece3eda9`; unchanged since 2026-07-26. Cardinality independently confirmed by an executed run.                                                                                                                                    |
| Provider-model contract (retired path: `../../../00.agent-governance/contracts/provider-models.yaml`)                 | 2026-08-14 | Tracked mutable        | Re-parsed at `ece3eda9`; unchanged since 2026-07-26.                                                                                                                                                                                            |
| Governance artifact contract (retired path: `../../../00.agent-governance/contracts/agent-governance-artifacts.yaml`) | 2026-08-14 | Tracked mutable        | Newly cited. 25 artifact profiles, 7 path-authority records, 3 families, 3 shims, 3 README profiles.                                                                                                                                            |
| [Persona protocol](../../../00.agent-governance/policies/persona.md)                                      | 2026-08-14 | Tracked mutable        | Re-read in full; fourteen persona-to-scope rows confirmed at lines 25-38; unchanged since 2026-05-15.                                                                                                                                           |
| [Governance contract validator](../../../../scripts/validation/check-agent-governance-contract.py)     | 2026-08-14 | Local observation      | Newly cited. Executed in both interpreters; results recorded verbatim above.                                                                                                                                                                    |
| [Governance contract tests](../../../../tests/lib/agent_governance/test_agent_governance_contract.py)            | 2026-08-14 | Local observation      | Newly cited. 159 tests executed, `OK` in the isolated environment; `scope_names` enumerates 13 of 14 scopes.                                                                                                                                    |
| [Workflow contract](../../../../.github/workflow-contract.yml)                                         | 2026-08-14 | Tracked mutable        | Newly cited. Parsed; 16 `job_roots`, 80 `gate_nodes`, 3 `profile_roots`, 8 pinned actions.                                                                                                                                                      |
| [Branch-protection ruleset record](../../../../.github/rulesets/main-protection.md)                    | 2026-08-14 | Tracked mutable        | Newly cited. The file itself declares control-plane verification `unverified` and lists the same 16 checks.                                                                                                                                     |
| [Stage authoring matrix](../../../00.agent-governance/policies/stage-authoring-matrix.md)                 | 2026-08-14 | Tracked mutable        | Re-verified directly; Stage 90 remains advisory.                                                                                                                                                                                                |
| [NIST SP 800-218 SSDF v1.1](https://csrc.nist.gov/pubs/sp/800/218/final)                               | 2026-08-14 | External fixed         | Re-fetched; live. Published February 2022; explicitly leaves tool choice to the adopting organization.                                                                                                                                          |
| [SLSA v1.1 provenance](https://slsa.dev/spec/v1.1/provenance)                                          | 2026-08-14 | External fixed         | Newly cited. Provenance describes the build process, not artifact properties; untrusted external parameters.                                                                                                                                    |
| [MCP specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28)               | 2026-08-14 | External mutable       | Newly cited. Per-request capability negotiation; opt-in extensions; protocol cannot enforce its own principles.                                                                                                                                 |
| GitHub CODEOWNERS documentation (URL below)                                                            | 2026-08-14 | External mutable       | Newly cited. Last matching pattern wins; CODEOWNERS alone does not enforce review.                                                                                                                                                              |
| [SPDX 3.0.1 model](https://spdx.github.io/spdx-spec/v3.0.1/model/AI/AI/)                               | 2026-08-14 | External fixed         | Newly cited. Profile-based modular inventory as a comparison for 25 typed artifact profiles.                                                                                                                                                    |
| ISO/IEC 42001 landing page                                                                             | 2026-08-14 | External, unretrieved  | Direct retrieval returned HTTP 403, the known `iso.org` refusal. No claim here depends on it.                                                                                                                                                   |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md)                                            | 2026-08-08 | Tracked stale/advisory | Built from `f8a72211`; not current evidence. Its 47 tracked files are counted as generated content.                                                                                                                                             |
| Predecessor workspace baseline, retiring 2026-07-05 pack                                               | 2026-08-14 | Historical retained    | Read for delta analysis only; its `.claude/` 49 and 24,597 B chain figures are superseded and explained above. Cited without a path because pre-deletion gate 4 admits no clickable link and the canonical router surface carries no allowlist. |

The GitHub CODEOWNERS documentation cited above is at
<https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners>.
It is held outside the table only so one long URL does not widen every row.

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | Use the Stage 00 authority sequence before agentic changes. | Read cited policy at the literal baseline. | No runtime activity observed. |
| architecture | applies | Before architecture use, compare a tracked architecture artifact with its canonical owner. | Confirm the artifact and scoped diff; seek separate approval for runtime observation. | Baseline evidence does not select an architecture. |
| common | applies | Preserve shared-worktree ownership and declared boundaries. | Inspect the scoped diff and Task ledger. | Shared rules are configuration, not enforcement proof. |
| docs | applies | Use the approved research profile and reference contract. | Check metadata and required sections. | Draft identity reconciliation remains deferred. |
| infra | applies | Inspect tracked infrastructure configuration only; seek separate approval for runtime observation. | Confirm the cited configuration revision and scoped diff. | Compose configuration is not runtime proof. |
| ops | applies | Route operational evidence to its owner and inspect tracked records before use. | Confirm the record path and scoped diff; seek separate approval for live operation. | No operational result is claimed. |
| qa | applies | Run only the scoped metadata, path, census, and whitespace checks. | Record exact commands and exits in Task 0004; seek separate approval for execution-environment checks. | Broad acceptance suites remain Not Run. |
| security | applies | Preserve the approval boundary and avoid secrets or credential access. | Confirm sources are tracked paths only; seek separate approval for control testing. | No security control effectiveness is claimed. |

## Maintenance

Re-measure this document when tracked path sets, Stage 00 typed registries,
stage corpus routes, workflows, scripts, template families, Compose paths, or
the twenty-leaf pack contract changes. Preserve the baseline commit and dated
command result when interpreting an older count, and state the delta and its
cause whenever a number moves. Re-run the governance contract validator and its
test suite in an environment that satisfies `scripts/requirements.txt` before
citing any cardinality as machine-confirmed. Do not refresh Graphify or any
generated artifact by hand; use its canonical owner in the separately approved
unit.

## Related Documents

- [Scope application matrix](./m0015-scope-application-matrix.md)
- [Verification and validation](./m0019-verification-validation.md)
- [SPEC-0158 preservation contract](../../../03.specs/0158-document-governance-lifecycle-convergence/spec.md)
- Implementation Plan (retired path: `../../../04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md`)
- Execution Task (retired path: `../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`)
- [Agent governance hub](../../../00.agent-governance/README.md)
- [Research category router](../README.md)
