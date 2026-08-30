---
status: active
artifact_id: reference:agentic-research:memory-hierarchy
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-07
review_cycle: on-source-change
---

# Reference: Agent Memory Hierarchy and Lifecycle

## Overview

Agent memory is not one thing. Research systems and provider runtimes both
separate a fast, bounded working record from a slower durable store, and they
differ mainly in how content is promoted between the two and how the store is
kept from growing without limit.

This repository has built one rigorously typed tier and two informal ones. The
bounded current-state handoff at `docs/00.agent-governance/memory/current.md`
is validated on bounds, section envelope, forbidden material, Task status, and
Git ancestry. The durable-note tier and the historical navigation tier have no
comparable lifecycle enforcement.

This reference records that architecture at baseline `867a8146`,
compares it against provider mechanisms and research memory models, and states
what a short-term, long-term, and domain-scoped taxonomy would require. It
changes no rule, contract, or validator.

## Purpose

Establish the exact current memory tiering and its enforcement, separate
deliberate exclusions from genuine gaps, and provide the source-backed basis for
a future memory-governance specification.

## Repository Role

`docs/00.agent-governance/memory/README.md` remains the canonical memory
contract, `scripts/validation/agent_governance_contract.py` remains the
validator, and `docs/03.specs/134-agent-governance-canonical-convergence/spec.md`
remains the governing specification for the shared current-memory route. This
Stage 90 document is a comparison and routing aid only.

## Scope

### In Scope

- The three de-facto repository memory tiers and their enforcement status
- The typed contract on the bounded current-state record
- Provider memory hierarchies for Claude, Codex, and Gemini
- Research memory models and their promotion and eviction mechanisms
- Requirements a short-term, long-term, and domain-scoped taxonomy would impose

### Out of Scope

- Changing memory bounds, contracts, validators, or the import chain
- Creating a domain-memory taxonomy or promotion policy
- Synchronizing provider-global or user-private memory
- Recording any credential, token, shell history, or raw output

## Definitions / Facts

- **Short-term memory** is the bounded working record that survives only as long
  as the current unit of work. In this repository nothing durable is
  session-scoped; session transcripts are explicitly out of scope.
- **Long-term memory** is the durable store that outlives a unit of work. Here
  it is the durable-note set plus the historical navigation record.
- **Domain-scoped memory** partitions the durable store by subject area so that
  retrieval loads only the relevant partition. This repository has the signal
  but not the mechanism.
- **Promotion** is the rule that moves content from working to durable memory.
  **Eviction** is the rule that removes or pages out durable content. Every
  research model surveyed here mechanizes at least one of the two.
- **Memory is advisory** in this repository. It aids retrieval and never
  establishes policy precedence over Stage 00 rules.

## Repository Tier Matrix

Re-derived from the tracked tree on 2026-08-07. The original pass measured
baseline `867a8146`; where a figure moved, the current value is stated and the
movement is noted in [Corrections to Stale Claims](#corrections-to-stale-claims).

| Criterion | Tier                          | Artifact                                     | Bound                                                                                            | Enforcement                                                                                                                                                                                                  | Status                | Gap / caveat                                                                                                                                              | Confidence |
| --------- | ----------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| MEM-01    | Session or short-term         | None                                         | Not applicable                                                                                   | None                                                                                                                                                                                                         | Missing               | Deliberate: transcripts and raw output are contractually excluded from durable memory                                                                     | High       |
| MEM-02    | Bounded current-state handoff | `memory/current.md`                          | 32,768 bytes and 400 lines; currently 7,743 bytes and 134 lines, or 24 percent of the byte bound | Typed validator with section envelope, label, Task-status, Git-ancestry, timestamp, and forbidden-material gates, raising `AGC-MEMORY-BOUNDS`, `AGC-MEMORY-FORBIDDEN-MATERIAL`, and `AGC-MEMORY-STALE-STATE` | Implemented           | The strongest tier; stronger than any surveyed provider mechanism                                                                                         | High       |
| MEM-03    | Durable advisory notes        | Seven notes in `memory/`, 26,933 bytes total | None                                                                                             | None specific to the tier. The repository contract check names only five governance memory paths and never enumerates a durable note                                                                         | Partially Implemented | Field values are never validated; see MEM-24 through MEM-26                                                                                               | High       |
| MEM-04    | Historical navigation         | `memory/progress.md`                         | None                                                                                             | Heading profile only                                                                                                                                                                                         | Partially Implemented | 1,384 lines and 1,193,498 bytes, roughly 36 times the byte bound applied to the current-state record, and 44 times the current-state record's actual size | High       |
| MEM-05    | Domain partition              | None                                         | Not applicable                                                                                   | None                                                                                                                                                                                                         | Missing               | The only domain signal is free-text `Applies To` and `Tags`; no scope owns a memory route, and all seven notes declare the same `layer: agentic`          | High       |
| MEM-06    | Provider-private memory       | Excluded                                     | Not applicable                                                                                   | Forbidden-material regex blocks provider-private paths                                                                                                                                                       | Not Applicable        | Deliberate exclusion, not a gap                                                                                                                           | High       |

## Current-State Record Contract

The bounded handoff is the only tier with a typed contract. Its gates are worth
stating precisely because they are unusual.

| Criterion | Gate                | Rule                                                                                                                                                     |
| --------- | ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MEM-07    | Section envelope    | Exactly seven ordered sections; no additional current-state section may be appended                                                                      |
| MEM-08    | Required labels     | Exactly one each of current task, verified commit, and verified time, each as a backticked value                                                         |
| MEM-09    | Task-state coupling | The current task must resolve to a tracked Stage 04 Task path whose frontmatter status is `draft` or `active`                                            |
| MEM-10    | Git ancestry        | The verified commit must be a full lowercase hex SHA and must be an ancestor of `HEAD`                                                                   |
| MEM-11    | Forbidden material  | Fenced code, credential and token vocabulary, shell history, provider-private paths, command and output prefixes, and policy-modal verbs are all blocked |

MEM-09 and MEM-10 are the distinguishing features. They make the record
falsifiable: a handoff cannot silently describe a Task that is closed, or a
commit that is not in the current history. No surveyed provider memory feature
offers an equivalent.

## Provider Memory Comparison

Provider facts were retrieved from official documentation on 2026-08-07.

| Criterion | Concern                      | Claude Code                                                                                                                       | Codex                                                                    | Gemini CLI                                                              |
| --------- | ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------- |
| MEM-12    | Instruction file             | `CLAUDE.md`; reads `CLAUDE.md` rather than `AGENTS.md`                                                                            | `AGENTS.md` with an override variant                                     | `GEMINI.md`, filename configurable                                      |
| MEM-13    | Hierarchy depth              | Four scopes: managed policy, user, project, local                                                                                 | Two scopes: Codex home, then project walked from Git root down           | Three scopes: global, workspace and ancestor, just-in-time subdirectory |
| MEM-14    | Merge semantics              | Concatenated rather than overriding                                                                                               | Concatenated root-down; closer files appear later and therefore override | Concatenated hierarchically; conflict precedence is not documented      |
| MEM-15    | Import syntax                | Path import with a maximum of four hops                                                                                           | None; filename-convention discovery only                                 | Path import supported                                                   |
| MEM-16    | Size cap                     | No hard cap on the instruction file; documented target under 200 lines. Auto-memory index limited to the first 200 lines or 25 KB | Combined chain capped, 32 KiB by default                                 | Not documented                                                          |
| MEM-17    | Agent-written durable memory | Yes: a per-project memory directory with an index plus on-demand topic files                                                      | No; the instruction chain is rebuilt every run                           | Yes: a save-memory tool writes durable facts into hierarchical context  |
| MEM-18    | Domain-scoped loading        | Path-glob scoped rule files load only when matching files are touched                                                             | Directory-nested instruction files only                                  | Subdirectory files plus a configurable filename array                   |
| MEM-19    | Enforcement status           | Documented as context, not enforced configuration; blocking requires a hook                                                       | Not applicable                                                           | Not applicable                                                          |

Claude's index-plus-topic-files layout with on-demand loading, and its
path-glob scoped rule files, are the closest published analogue to the
domain-scoped tier this repository lacks.

Two Claude mechanisms re-verified on 2026-08-07 go further than the earlier
pass recorded, and both bear directly on the gaps listed below.

- **The auto-memory index has an enforced compaction trigger.** After Claude
  writes `MEMORY.md`, Claude Code measures it against the 200-line and 25 KB
  read limits. Near a limit it instructs the model to shorten the index, move
  detail into topic files, and merge or drop stale entries. Over a limit the
  write still succeeds but Claude Code returns an error telling the model to
  rewrite the index, because content past the limit is dropped on the next
  load. That is a capacity-driven eviction rule of the same shape as MemGPT's
  memory-pressure flush, implemented in a shipping product.
- **Durable memory files carry a machine-written freshness stamp.** When a
  memory file begins with YAML frontmatter, Claude Code records the write time
  in a `modified` field as an ISO 8601 timestamp, so both the user and the
  model can see how current a fact is. This repository's durable notes carry a
  hand-maintained `Last Verified` line instead, and nothing writes or checks
  it.

The comparison in the next section should be read with those two facts in
mind: the claim is not that products lack promotion and eviction machinery, but
that this repository has not adopted any.

## Research Memory Models

| Criterion | Model             | Tiering                                                                                        | Promotion                                                                    | Eviction                                                                 | Retrieval                                                                                |
| --------- | ----------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| MEM-20    | Reflexion         | Trajectory history as short-term; self-reflection output as long-term                          | Sparse reward triggers verbal self-reflection appended to an episodic buffer | Fixed-size sliding window, typically one to three stored experiences     | Whole buffer is conditioned on                                                           |
| MEM-21    | MemGPT            | Main context in-window versus external context out-of-window, with recall and archival storage | Not the primary mechanism                                                    | Memory-pressure warning triggers queue flush and recursive summarization | Model-issued function calls with pagination and self-directed edits                      |
| MEM-22    | Generative Agents | Single memory stream of timestamped objects, with reflections as higher-order objects          | Reflection fires when accumulated importance crosses a threshold             | None; storage is unbounded                                               | Weighted score combining recency decay, LLM-assigned importance, and embedding relevance |

The three differ in what drives movement: MemGPT and Reflexion are
capacity-driven, and Generative Agents is salience-driven. All three mechanize
the rule, and as noted above Claude Code ships a capacity-driven variant of it.
This repository mechanizes neither promotion nor eviction on the durable tier.
Its one mechanized bound, the 32,768-byte and 400-line gate on the current-state
record, is a hard rejection rather than a compaction trigger: it stops an
oversized record from being written but never tells an author what to move
where, and it applies to the one tier that is already at 24 percent of its
limit rather than to the tier that is 36 times over that same figure.

## Current-State Assessment

| Category         | Current state                                                                                                                                                      | Primary comparison                                                                     | Status                | Gap                                                                                                                                    | Recommendation                                                                                                                                                         | Canonical owner                             | Evidence                                                                        | Confidence |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------- | ---------- |
| Memory hierarchy | One rigorously typed current-state tier with Task-status and Git-ancestry coupling, plus two informal tiers with no lifecycle enforcement and no domain partition. | Claude, Codex, and Gemini memory hierarchies; Reflexion, MemGPT, and Generative Agents | Partially Implemented | No session tier by design, no promotion or eviction rule, no retention gate, no domain ownership, and no bound on the historical tier. | Keep the typed current-state contract unchanged. Route a domain taxonomy, retention gate, and archival rule through a future Stage 03 memory-governance specification. | `docs/00.agent-governance/memory/README.md` | Matrices above; validator source; official provider documentation; cited papers | High       |

## Potential Follow-up / Gap

1. **MEM-23 — No promotion rule.** The memory README prompts an author to add
   an entry after resolving a complex issue, which is a human judgment cue
   rather than a trigger. Generative Agents demonstrates a threshold-driven
   alternative and Reflexion a reward-driven one. Owner:
   `docs/00.agent-governance/memory/README.md`.
2. **MEM-24 — No retention or staleness gate on durable notes.** The
   `Last Verified` field is a free-text body bullet with no validator. Its
   current values are 2026-05-10, 2026-05-10, 2026-05-26, 2026-05-26,
   2026-05-26, 2026-06-03, and 2026-07-26, so six of the seven notes were last
   verified more than seventy days before this revalidation and nothing
   surfaces that. The current-state record has a falsifiable freshness gate
   through Git ancestry, and Claude Code writes a machine-maintained `modified`
   timestamp on its own memory files; the durable tier has neither. Owner:
   `scripts/validation/check-repo-contracts.sh`.
3. **MEM-25 — Superseded notes remain in the active directory.** Three of the
   seven durable notes carry `- Status: superseded`:
   `docker-doc-contract-backlog.md`, `execution-stage-legacy-debt.md`, and
   `governance-memory-usage-contract.md`. The value is not validated and no
   archival destination or move rule exists, so superseded content still
   surfaces in retrieval. The repository already implements typed retirement for
   models and roles through a retirement ledger, which is a working precedent
   this tier does not use. Owner:
   `docs/00.agent-governance/memory/README.md`.
4. **MEM-26 — Domain ownership is unvalidated prose, and the status field is
   not where the template puts it.**
   `docs/99.templates/templates/governance/memory.template.md` declares
   `status: draft` in YAML frontmatter, but none of the seven durable notes
   carries a `status` frontmatter key. Each declares only `layer: agentic` and
   records status as a `- Status:` body bullet instead. The template's own
   contract is therefore unmet across the whole tier, and a validator written
   against the template would find nothing to read. `Applies To` is likewise
   free text. The fourteen entries under `docs/00.agent-governance/scopes/` are
   the obvious enumerated domain vocabulary, but all seven notes declare the
   same `agentic` layer and no scope owns a memory route. Owner:
   `docs/00.agent-governance/scopes/`.
5. **MEM-27 — The historical tier is unbounded.** `progress.md` is 1,193,498
   bytes, roughly 36 times the byte bound imposed on the current-state record.
   It is not loaded at bootstrap, which is the only thing keeping it
   inexpensive. Owner: `docs/00.agent-governance/memory/README.md`.
6. **MEM-28 — Retrieval is unranked substring matching.** Retrieval is a
   targeted text search over the memory folder, with no recency, importance, or
   relevance weighting, and no declared index enumerating what durable notes
   exist. Owner: `docs/00.agent-governance/rules/agentic.md`.
7. **MEM-29 — WITHDRAWN. No Gemini memory command drift exists.** An earlier
   pass recorded that the repository's Gemini overlay cited unsupported memory
   subcommands. Re-verification against the official Gemini CLI command
   reference on 2026-08-07 falsifies that finding. The reference documents
   `/memory` as managing "the AI's instructional context (hierarchical memory
   loaded from `GEMINI.md` files)" with exactly three subcommands: `list`
   ("Lists the paths of the GEMINI.md files in use for hierarchical memory"),
   `show` ("Display the full, concatenated content of the current hierarchical
   memory"), and `refresh` ("Reload the hierarchical instructional memory from
   all `GEMINI.md` files found in the configured locations"). All three are
   exactly what `docs/00.agent-governance/providers/gemini.md:90-92` instructs
   agents to use. There is no `reload` subcommand; the word appears only inside
   the prose description of `refresh`, which is the likeliest source of the
   original misreading. No overlay change is required, and none should be made
   on the strength of the withdrawn finding.

## Corrections to Stale Claims

- **Withdrawn 2026-08-07.** MEM-29's Gemini memory-command drift finding is
  false. See the withdrawal above. This is the only finding in this document
  that was retracted rather than refined.
- **Corrected 2026-08-07.** MEM-02's current-state measurement moved.
  `memory/current.md` is now 7,743 bytes and 134 lines, not the 10,998 bytes
  and 185 lines measured at baseline `867a8146`. The bounds themselves are
  unchanged. The record is at 24 percent of its byte bound and 34 percent of
  its line bound, so the tier with the only enforced ceiling is also the tier
  furthest from needing one.
- **Corrected 2026-08-07.** MEM-03's enforcement description was too generous.
  The durable-note tier has no enforcement of its own. The repository contract
  check requires exactly five governance memory paths to exist —
  `memory/README.md`, `memory/current.md`, `memory/progress.md`, and the two
  Stage 99 templates — and then performs literal-substring route checks against
  six named files. No durable note is enumerated, bounded, or status-checked
  anywhere. The folder is additionally glob-excluded from two repository-wide
  stale-reference scans in `scripts/validation/check-repo-contracts.sh`, so
  banned-taxonomy and shorthand drift inside memory notes is not reported
  either.
- **Refined 2026-08-07.** The claim that surveyed provider mechanisms offer
  nothing equivalent to this repository's current-state gates remains true for
  Task-status and Git-ancestry coupling, which no provider offers. It is too
  strong for lifecycle generally: Claude Code enforces an index read limit with
  a returned error and writes a `modified` freshness timestamp, both of which
  this repository's durable tier lacks.
- **Confirmed 2026-08-07 against current official sources.** MEM-12 through
  MEM-19 were re-fetched and every row holds. Claude reads `CLAUDE.md`, not
  `AGENTS.md`; its four scopes load broadest-first and are "concatenated into
  context rather than overriding each other"; imports have "a maximum depth of
  four hops"; the documented size guidance is "target under 200 lines per
  CLAUDE.md file" with no hard cap, while the auto-memory index loads "the
  first 200 lines of `MEMORY.md`, or the first 25KB, whichever comes first";
  and both systems are "context, not enforced configuration", where blocking
  "regardless of what Claude decides" requires a `PreToolUse` hook. Codex
  discovers `AGENTS.override.md` then `AGENTS.md` at Codex home, then walks
  Git root down, and caps the combined chain at 32 KiB by default via
  `project_doc_max_bytes`.

## Adoption Boundary

This document changes no rule, contract, or validator, and the gaps above are
not a work order. Anything built from them must resolve five workspace-specific
questions first, in this order, because each one constrains the next.

1. **Which tier is being governed?** A retention gate on the durable notes,
   a bound on `progress.md`, and a domain taxonomy are three separate changes
   with three different owners. Bundling them would put a bound on the one
   tier that is deliberately unbounded for navigation.
2. **Where does status actually live?** MEM-26 shows the template and the notes
   disagree. Any validator must be written against whichever of the two
   becomes canonical, and moving `Status` into frontmatter would edit all seven
   notes. That is a mechanical change, but it is not a no-op and it is not in
   scope for a Stage 90 reference.
3. **What is the domain vocabulary?** The fourteen scope files are the only
   enumerated candidate. Adopting them means deciding whether a note may
   declare more than one scope, and whether a scope with no notes is a defect.
4. **What happens to a superseded note?** The retirement-ledger pattern already
   used for models and roles is the working precedent. Reusing it requires an
   archival destination that retrieval does not search, which does not exist.
5. **Does anything load the new tier?** `progress.md` stays inexpensive only
   because bootstrap does not load it. A domain-partitioned tier that bootstrap
   does load would move cost from retrieval into every session, which is the
   opposite of the Claude path-scoped-rule pattern it would be imitating.

The correct destination for all five is a future Stage 03 memory-governance
specification. `docs/00.agent-governance/memory/README.md` remains the contract,
`scripts/validation/agent_governance_contract.py` remains the validator, and
neither may be changed on the authority of this reference.

## Scope Correction

The deferral commonly cited as a Spec 134 boundary does not appear in that
specification. `grep` for the phrase "typed domain-memory taxonomy" in
`docs/03.specs/134-agent-governance-canonical-convergence/spec.md` returns zero
matches. The phrase originates in the Stage 04 Task ledger and in the current
memory record, not in the specification text.

What Spec 134 actually states is narrower: it requires one bounded,
repository-tracked project-memory route shared by all providers, and its
non-goals exclude synchronizing provider-global or user-private memory. A
domain taxonomy is therefore outside Spec 134 because Spec 134 never addressed
it, not because Spec 134 deferred it. Any future memory-governance
specification should be written against that accurate boundary.

## Source Rules

- Use official provider documentation for current memory mechanics and treat it
  as mutable.
- Use original papers for research memory models and quote their mechanisms
  rather than paraphrasing thresholds.
- Keep repository memory authority with the Stage 00 contract and validator.
- Never record credential, token, shell history, provider-private, or raw output
  material in any memory artifact.

## Sources

- [Claude Code memory documentation](https://code.claude.com/docs/en/memory)
- [Codex AGENTS.md configuration](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Gemini CLI context file documentation](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md)
- [Gemini CLI memory tool documentation](https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/memory.md) - re-fetched 2026-08-07; the page describes routing memories into `GEMINI.md` files and editing them with `write_file` or `replace`, and does NOT document `/memory` subcommands, which is why the command reference below is the source for MEM-29
- [Gemini CLI command reference](https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/commands.md) - the `/memory` command and its `list`, `show`, and `refresh` subcommands; the source that withdraws MEM-29
- [Codex AGENTS.md discovery and limits](https://learn.chatgpt.com/docs/agent-configuration/agents-md) - `AGENTS.override.md` precedence, Git-root-down walk, and the 32 KiB `project_doc_max_bytes` default
- [Reflexion paper](https://arxiv.org/abs/2303.11366)
- [MemGPT paper](https://arxiv.org/abs/2310.08560)
- [Generative Agents paper](https://arxiv.org/abs/2304.03442)
- [Governance memory README](../../../00.agent-governance/memory/README.md)
- [Agentic rule](../../../00.agent-governance/policies/agentic.md)
- [Provider capability matrix](../../../00.agent-governance/policies/provider-capability-matrix.md)

## Source Retrieval Boundary

Provider documentation and papers were retrieved on 2026-08-07. Two retrieval
limits apply. The Generative Agents PDF exceeded the fetch size limit, so its
quantitative parameters were read from the hosted HTML rendering of the same
arXiv record rather than the PDF. The MemGPT tier terminology was read from a
summarized pass over the PDF; its substance is accurate but its exact section
wording was not extracted verbatim and should be confirmed before being quoted
as such.

Repository counts and contract details were re-derived from the tracked tree on
2026-08-07 and are reproducible from it. Figures that moved since baseline
`867a8146` are listed in Corrections to Stale Claims; the baseline itself is
retained where a figure is unchanged. No validator was executed to produce the
numbers in this document.

On the 2026-08-07 pass, provider documentation for Claude memory, the Gemini
CLI command reference, and the Codex `AGENTS.md` guide were all retrieved
successfully. The Gemini memory tool page was retrieved but does not document
`/memory` subcommands, so it cannot support or refute a claim about them; that
limit is recorded on the source entry rather than resolved by substitution. The
Reflexion, MemGPT, and Generative Agents rows were not re-fetched on this pass
and retain the retrieval limits stated above.

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Quarterly, or when memory contracts or provider memory
  mechanisms change
- **Update Trigger**: Memory contract bounds, validator gates, provider memory
  documentation, or a new memory-governance specification

## Related Documents

- [research pack index](./README.md)
- [loop engineering](./loop-engineering.md)
- [provider implementation comparison](./provider-implementation-comparison.md)
- [documentation architecture](./documentation-architecture.md)
- [LLM-WIKI system](./llm-wiki-system.md)
- [governance memory README](../../../00.agent-governance/memory/README.md)
