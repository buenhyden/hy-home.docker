---
status: active
artifact_id: ref-0048
artifact_type: reference
parent_ids: []
observed_at: '2026-07-05'
reviewed_at: 2026-08-07
---

# Reference: LLM-WIKI System, Rules, and Implementation

## Overview

The LLM Wiki is this repository's machine-facing navigation surface. It answers
one question for an agent that has just been dropped into the tree: which
tracked file is canonical for a given need. It deliberately carries no content
of its own, so it can never become a second, stale copy of runtime truth.

The system is four artifacts and two generators. Root `llms.txt` is the thin
entrypoint, `repository-map.md` is the hand-curated need-to-source table,
`llm-wiki-index.md` is a fully generated path index, and a satellite coverage
snapshot reports what the index covers. Freshness is enforced by byte-exact
regeneration comparison inside the repository contract check.

This reference first described that system at baseline `867a8146`. Every size,
count, and external-convention claim was re-derived at `HEAD` on 2026-08-07 and
corrected rows are labeled inline. It compares the system against the published
external conventions for machine-facing repository context and changes no
generator, validator, or policy.

## Purpose

Record the exact structure, ownership, generation mechanism, and enforcement
boundary of the LLM Wiki, and identify where published external conventions
suggest capabilities this repository does not implement.

## Repository Role

`scripts/knowledge/generate-llm-wiki-index.sh` and
`scripts/knowledge/generate-llm-wiki-coverage.sh` remain the canonical
generators. `scripts/validation/check-repo-contracts.sh` remains the
enforcement boundary.
`docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/policy.md` remains the
canonical maintenance policy. This Stage 90 document is a comparison and
routing aid only.

## Scope

### In Scope

- The four LLM Wiki artifacts and their authored-versus-generated split
- Generation algorithm, safety exclusions, and determinism guarantees
- The freshness, ownership, and drift contract as actually implemented
- Comparison against `llms.txt`, `AGENTS.md`, and `CLAUDE.md` conventions

### Out of Scope

- Modifying any generator, validator, policy, or generated output
- Publishing the wiki to any public site or producing a full-content variant
- Reading or quoting any secret value
- Treating generated graph output as authoritative

## Definitions / Facts

- **LLM Wiki** is a generated tracked repo-local path index plus a small
  hand-curated map. It is explicitly not a deployable wiki site and not a
  Graphify publication surface.
- **Safe path** is a tracked path that survives the generator's allowlist and
  exclusion filters. `secrets/` is excluded in full except `secrets/README.md`.
- **Byte-exact freshness** means the generator re-renders the artifact in
  memory and compares the whole file; any difference fails the check.
- **Runtime truth** stays in tracked Compose files, registries, scripts, and
  configuration. The index points at them and never restates them.

## Artifact Inventory

Re-measured at `HEAD` on 2026-08-07. The earlier `867a8146` figures for
WIKI-03 and WIKI-04 were stale and are corrected here.

| Criterion | Artifact                                                                | Authored or generated | Size                                                                                                       | Language              | Role                                                       |
| --------- | ----------------------------------------------------------------------- | --------------------- | ---------------------------------------------------------------------------------------------------------- | --------------------- | ---------------------------------------------------------- |
| WIKI-01   | `llms.txt`                                                              | Hand-authored         | 30 lines, 1,589 bytes                                                                                      | English               | Root entrypoint with canonical entry points and boundaries |
| WIKI-02   | `docs/90.references/llm-wiki/README.md`                                 | Hand-authored         | 85 lines, 4,689 bytes                                                                                      | Korean                | Folder index and category boundary                         |
| WIKI-03   | `docs/90.references/llm-wiki/repository-map.md`                         | Hand-authored         | 95 lines, 5,834 bytes                                                                                      | English               | Eleven-row need-to-canonical-source table                  |
| WIKI-04   | `docs/90.references/llm-wiki/llm-wiki-index.md`                         | Generated             | 1,458 lines, 198,714 bytes, 1,324 path rows in 12 `###` subsections under one `## Generated Index` heading | Mixed, English-exempt | Deterministic path index                                   |
| WIKI-05   | `docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md` | Generated             | Coverage snapshot                                                                                          | English               | Counts safe paths by bucket, category, and role            |

## Generation and Enforcement Matrix

| Criterion | Concern                    | Implementation                                                                                                                                                                                                                                                                                     | Evidence                                                                     | Status                | Gap / caveat                                                                                     | Confidence |
| --------- | -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------ | ---------- |
| WIKI-06   | Path source                | `git ls-files`, plus a small required-local-path escape hatch for in-progress contract files                                                                                                                                                                                                       | `scripts/knowledge/generate-llm-wiki-index.sh`                               | Implemented           | The escape hatch means local output can differ from a clean checkout until the paths are tracked | High       |
| WIKI-07   | Secret exclusion           | Any path under `secrets/` is rejected except `secrets/README.md`                                                                                                                                                                                                                                   | Generator safe-candidate filter                                              | Implemented           | Enforced at generation and re-scanned by the contract check                                      | High       |
| WIKI-08   | Noise exclusion            | Excludes `graphify-out/`, `volumes/`, `node_modules/`, `.git/`, build directories, lockfiles, and minified artifacts                                                                                                                                                                               | Generator prefix and suffix filters                                          | Implemented           | Filters are extension and prefix based, not content based                                        | High       |
| WIKI-09   | Determinism                | Sorted paths, fixed section order, whole-file byte comparison in check mode                                                                                                                                                                                                                        | Generator check mode                                                         | Implemented           | Byte-exact comparison is stronger than a timestamp heuristic                                     | High       |
| WIKI-10   | Classification             | 12 fixed sections and 7 role labels derived from path and suffix                                                                                                                                                                                                                                   | Generator classify and role functions                                        | Partially Implemented | Role labels are extension-derived, not semantic; see WIKI-17                                     | High       |
| WIKI-11   | Freshness enforcement      | Repository contract check shells out to both generators with check mode and folds failures in                                                                                                                                                                                                      | `scripts/validation/check-repo-contracts.sh` LLM Wiki contract section       | Implemented           | Single enforcement point; see WIKI-19                                                            | High       |
| WIKI-12   | Registration enforcement   | Required literals must appear in seven index READMEs, preventing orphaning: `README.md`, `docs/README.md`, `docs/90.references/README.md`, `docs/05.operations/guides/README.md`, `docs/05.operations/00-workspace/README.md`, `scripts/README.md`, and `docs/90.references/data/README.md` | `check-repo-contracts.sh:2545-2582`                                          | Implemented           | `AGENTS.md` is not among the gated files; see WIKI-18                                            | High       |
| WIKI-13   | Safety wording enforcement | Bans `file://` links, secret-reading phrasing, and claims that generated graph output is authoritative                                                                                                                                                                                             | Contract check safety scan                                                   | Implemented           | Literal and regex based                                                                          | High       |
| WIKI-14   | Typed contract ownership   | None. No Stage 00 typed contract governs the LLM Wiki                                                                                                                                                                                                                                              | `grep` over `docs/00.agent-governance/contracts/` returns no match           | Missing               | Every other governed surface has a typed contract; this one is imperative shell only             | High       |
| WIKI-15   | Runtime hook               | None, by explicit policy decision rather than omission                                                                                                                                                                                                                                             | `docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/policy.md`           | Not Applicable        | Policy states hooks are not added without a demonstrated failure mode                            | High       |
| WIKI-16   | Ownership                  | `doc-writer` role using the `knowledge-map-agent` function for the generated index; documentation maintainers for the curated map                                                                                                                                                                  | Generated index maintenance block; `docs/00.agent-governance/scopes/docs.md` | Implemented           | Two different ownership vocabularies for one system                                              | Medium     |

## External Convention Comparison

| Dimension            | `llms.txt` proposal                                                                                                                                                        | `AGENTS.md` and `CLAUDE.md`                                                                                                                                                                                      | This repository's LLM Wiki                                                  |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Consumer             | External model fetching a website                                                                                                                                          | Coding agent at session start                                                                                                                                                                                    | Repo-local agent exploring the tree                                         |
| Delivery             | HTTP fetch of a root path                                                                                                                                                  | Auto-loaded into context every session                                                                                                                                                                           | Read on demand through file tools; nothing auto-loads                       |
| Size discipline      | Concise by design, with a skippable optional tier                                                                                                                          | Codex stops adding files once the combined size reaches `project_doc_max_bytes`, 32 KiB by default; Claude documents a target under 200 lines per `CLAUDE.md` and loads `CLAUDE.md` in full regardless of length | No budget; the generated index is 198,714 bytes                             |
| Content              | Curated links with prose notes                                                                                                                                             | Instructions, commands, conventions                                                                                                                                                                              | Path plus role label only, by contract                                      |
| Authoring            | Hand-curated                                                                                                                                                               | Hand-written                                                                                                                                                                                                     | Hybrid: three authored artifacts, two generated                             |
| Freshness            | Not specified                                                                                                                                                              | Not specified                                                                                                                                                                                                    | Byte-exact regeneration gate in the contract check                          |
| Safety boundary      | Not specified                                                                                                                                                              | Not specified                                                                                                                                                                                                    | Secret allowlist, banned phrases, excluded-path scans                       |
| Full-content variant | **Corrected 2026-08-07:** not part of the proposal. The site cites FastHTML's project-specific `llms-ctx-full.txt` expansion as an example, not a specified companion file | Not applicable                                                                                                                                                                                                   | Explicitly forbidden at `llm-wiki-index.md:35`                              |
| Required structure   | Only an H1 project name is required; a blockquote summary, free paragraphs, and H2-delimited file lists are optional                                                       | No required fields; standard Markdown with flexible headings                                                                                                                                                     | Twelve fixed `###` subsections and seven role labels, all generator-emitted |
| Priority tier        | An `Optional` section whose "URLs provided there can be skipped if a shorter context is needed"                                                                            | Not specified                                                                                                                                                                                                    | None; every row is equal weight                                             |

## Current-State Assessment

| Category        | Current state                                                                                                            | Primary comparison                                                       | Status                | Gap                                                                                                                                                  | Recommendation                                                                                                                                      | Canonical owner                                                    | Evidence                                             | Confidence |
| --------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------ | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ | ---------------------------------------------------- | ---------- |
| LLM-WIKI system | A generated, byte-exactly gated, safety-scanned path index with a small curated map and an explicit no-content contract. | `llms.txt` proposal, `AGENTS.md` convention, Claude memory documentation | Partially Implemented | No context budget on the largest artifact, no typed contract, no priority tier, and the one file most agents read first does not reference the wiki. | Keep the no-content contract, which is stronger than any external convention. Address the budget and registration gaps through their listed owners. | `docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/policy.md` | Matrices above; generator and contract check sources | High       |

## Potential Follow-up / Gap

1. **WIKI-17 — No context budget on the generated index.** Codex caps its
   combined instruction chain at 32 KiB and Claude documents a target under 200
   lines. `llm-wiki-index.md` is 198,714 bytes across 1,458 lines. It is never
   auto-loaded, which is what keeps it harmless today, but an agent instructed
   to read the index ingests the whole file. There is no size gate, no
   chunking, and no per-section split. Owner:
   `scripts/knowledge/generate-llm-wiki-index.sh`.
2. **WIKI-18 — `AGENTS.md` does not reference the LLM Wiki.** Under the
   published `AGENTS.md` convention, which the site states is used by over 60k
   open-source projects, this is the first file many agents read, and
   `repository-map.md:52` advertises it as the provider-neutral entry shim.
   `grep -ci 'llm.wiki\|llms.txt' AGENTS.md` returns 0, and `AGENTS.md` is not
   among the seven files whose registration literals the contract check gates.

   Two measurements sharpen this. First, the file is 7 lines and 243 bytes,
   roughly 0.7 percent of Codex's 32 KiB `project_doc_max_bytes` default, so
   there is no size pressure justifying the omission. Second, Claude Code does
   not read `AGENTS.md` at all; its documentation states it reads `CLAUDE.md`
   and recommends importing `AGENTS.md` with `@AGENTS.md` when a repository has
   both. This repository's `CLAUDE.md` imports Stage 00 governance directly
   rather than `AGENTS.md`, so the two providers reach the wiki, or fail to,
   by different paths. Owner: `AGENTS.md` and
   `scripts/validation/check-repo-contracts.sh`.

3. **WIKI-19 — Role labels are extension-derived, not semantic.** Seven labels
   are computed from filename and suffix, so 1,324 rows read as a filesystem
   listing rather than a map. The distribution is heavily skewed: 831
   `Markdown reference`, 221 `folder index`, 111 `YAML config`, 74
   `JSON registry`, 57 `script`, 27 `source path`, and 3 `text entrypoint`.
   Two labels therefore account for 1,052 of 1,324 rows, so the label carries
   almost no discriminating information. The genuinely navigational content is
   the eleven-row curated table in `repository-map.md`, which is a fraction of
   the size. The published convention allows per-link notes describing what each
   link is for. Owner: `scripts/knowledge/generate-llm-wiki-index.sh`.
4. **WIKI-20 — No typed contract.** Every other governed surface in this
   repository is described by a typed contract under
   `docs/00.agent-governance/contracts/`. The LLM Wiki contract is imperative
   shell and embedded Python with many hardcoded literals, which is brittle
   relative to the repository's own declarative standard. Owner:
   `docs/00.agent-governance/contracts/`.
5. **WIKI-21 — No generation provenance in the generated output.** The index
   frontmatter records status and generator but no generation timestamp or
   source commit, so a reader cannot judge currency without re-running the
   generator. Owner: `scripts/knowledge/generate-llm-wiki-index.sh`.
6. **WIKI-22 — Enforcement funnels through one CI step and no hook.** The
   no-hook stance is deliberate policy and defensible, but it means a local
   agent that renames documents and skips the contract check produces a
   silently stale index until continuous integration runs. Owner:
   `docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/policy.md`.

## Workspace Application: What to Investigate or Change Here

Each item is an investigation prompt with a named owner. None is approved work,
and none may modify a generator, validator, or generated output.

1. **Register the LLM Wiki in `AGENTS.md`, or record why not.** This is the
   cheapest high-value change available: the file is 243 bytes, the convention
   it implements is provider-neutral, and `repository-map.md:52` already
   advertises it as the entry shim. Adding one line and one contract-check
   literal closes WIKI-18 entirely. The alternative — deciding that Codex
   reaches the wiki through Stage 00 governance and that `AGENTS.md` should
   stay minimal — is defensible but is currently undocumented, which is the
   real gap. Owner: `AGENTS.md`.
2. **Measure whether the generated index is ever actually read.** WIKI-17
   treats the 198,714-byte index as a latent context hazard, but the hazard is
   hypothetical until an agent is instructed to read it. Investigate whether
   any tracked rule, skill, scope, or policy tells an agent to open
   `llm-wiki-index.md` whole. If none does, the size finding should be
   downgraded from a gap to a documented non-issue; if one does, the size gate
   becomes urgent rather than advisory.
3. **Consider a priority tier before considering chunking.** The `llms.txt`
   proposal solves exactly this problem with an `Optional` section whose URLs
   "can be skipped if a shorter context is needed". That is a smaller change
   than per-section splitting and preserves byte-exact determinism, since the
   generator would still emit one file. Owner:
   `scripts/knowledge/generate-llm-wiki-index.sh`.
4. **Reconsider the role-label vocabulary, not just its derivation.** WIKI-19
   frames the problem as labels being extension-derived. The measured
   distribution shows a sharper problem: `Markdown reference` and `folder
index` cover 1,052 of 1,324 rows, so most rows carry a label that
   distinguishes nothing. A semantic label set is only worth building if it
   would actually partition the corpus; test that before investing.
5. **Do not weaken the no-content contract to fix any of the above.** The
   explicit prohibition on a full-content variant, the secret allowlist, and
   the banned-phrase scan are stronger than anything the external conventions
   specify. `llms.txt`, `AGENTS.md`, and the Claude memory documentation all
   specify no freshness contract and no safety boundary at all. Every
   improvement above must preserve those three properties.

## Source Rules

- Prefer tracked source files over the generated index whenever a fact must be
  authoritative.
- Treat generated graph output as advisory navigation context only.
- Never quote a secret value; `secrets/` is policy context, and only its README
  is indexable.
- Re-run both generators in check mode after any in-scope path change.

## Sources

- [llms.txt proposal](https://llmstxt.org/) - re-read 2026-08-07: root `/llms.txt`, an H1 project name as the only required section, optional blockquote summary and H2 file lists, and an `Optional` tier whose URLs "can be skipped if a shorter context is needed". `llms-full.txt` is **not** specified by the proposal
- [AGENTS.md convention](https://agents.md/) - re-read 2026-08-07: root file, standard Markdown, no required fields, nearest-file-wins in monorepos, explicit user prompts override; states use by "over 60k open-source projects" and 88 `AGENTS.md` files in the main OpenAI repo; no size limit stated
- [Claude Code memory documentation](https://code.claude.com/docs/en/memory) - re-read 2026-08-07: "target under 200 lines per CLAUDE.md file"; CLAUDE.md files are loaded in full regardless of length; `@path` imports resolve to a maximum depth of four hops; Claude Code reads `CLAUDE.md`, not `AGENTS.md`, and recommends an `@AGENTS.md` import when both exist
- [Codex AGENTS.md configuration](https://learn.chatgpt.com/docs/agent-configuration/agents-md) - re-read 2026-08-07: Codex "stops adding files once the combined size reaches the limit defined by `project_doc_max_bytes` (32 KiB by default)"; discovery walks global `~/.codex` then project root to cwd, closer files overriding earlier ones
- [LLM Wiki category README](../llm-wiki/README.md)
- [Repository map](../llm-wiki/ref-0083-repository-map.md)
- [LLM Wiki maintenance policy](../../05.operations/00-workspace/ops-0007-llm-wiki-maintenance/policy.md)
- [Docs scope](../../00.agent-governance/scopes/docs.md)

## Source Retrieval Boundary

All four external conventions were re-retrieved on 2026-08-07 and all four
returned HTTP 200 and served content. **No source in this document is
unverified.**

The `developers.openai.com` guide path for `AGENTS.md` returns an HTTP 308
redirect and serves no content directly; the redirect target on
`learn.chatgpt.com` is cited above instead, and it was read successfully.

Published conventions are mutable documentation with no displayed update date,
so each citation proves only the content visible on 2026-08-07 and must be
re-checked before operational use.

Repository facts in this document were originally counted at baseline
`867a8146` and were re-counted at `HEAD` on 2026-08-07. Where the two disagree
the current figure is used and the row is labeled. The counts are reproducible
from the tracked tree: sizes come from `wc -l -c`, path rows from the `| [`
line prefix inside the `## Generated Index` section, and the README gate list
from `check-repo-contracts.sh:2545-2582`.

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Quarterly, or when the generators or contract check change
- **Update Trigger**: Generator algorithm, contract check literals, LLM Wiki
  artifact structure, or external convention changes

## Related Documents

- [research pack index](ref-0039-readme.md)
- [documentation architecture](ref-0046-documentation-architecture.md)
- [memory hierarchy](ref-0050-memory-hierarchy.md)
- [workspace baseline](ref-0058-workspace-baseline.md)
- [document metadata lifecycle](ref-0045-document-metadata-lifecycle.md)
- [LLM Wiki category README](../llm-wiki/README.md)
