---
status: active
artifact_id: reference:agentic-research:llm-wiki-system
artifact_type: reference
parent_ids: [spec:123-agentic-engineering-audit-remediation]
reviewed_at: 2026-08-07
review_cycle: on-source-change
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

This reference describes that system at baseline `867a8146` and
compares it against the published external conventions for machine-facing
repository context. It changes no generator, validator, or policy.

## Purpose

Record the exact structure, ownership, generation mechanism, and enforcement
boundary of the LLM Wiki, and identify where published external conventions
suggest capabilities this repository does not implement.

## Repository Role

`scripts/knowledge/generate-llm-wiki-index.sh` and
`scripts/knowledge/generate-llm-wiki-coverage.sh` remain the canonical
generators. `scripts/validation/check-repo-contracts.sh` remains the
enforcement boundary.
`docs/05.operations/policies/00-workspace/llm-wiki-maintenance.md` remains the
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

Measured at baseline `867a8146`.

| Criterion | Artifact                                                                | Authored or generated | Size                                                     | Language              | Role                                                       |
| --------- | ----------------------------------------------------------------------- | --------------------- | -------------------------------------------------------- | --------------------- | ---------------------------------------------------------- |
| WIKI-01   | `llms.txt`                                                              | Hand-authored         | 30 lines, 1,589 bytes                                    | English               | Root entrypoint with canonical entry points and boundaries |
| WIKI-02   | `docs/90.references/llm-wiki/README.md`                                 | Hand-authored         | 85 lines, 4,689 bytes                                    | Korean                | Folder index and category boundary                         |
| WIKI-03   | `docs/90.references/llm-wiki/repository-map.md`                         | Hand-authored         | 95 lines, 5,834 bytes                                    | English               | Twelve-row need-to-canonical-source table                  |
| WIKI-04   | `docs/90.references/llm-wiki/llm-wiki-index.md`                         | Generated             | 1,464 lines, 199,864 bytes, 1,330 path rows, 12 sections | Mixed, English-exempt | Deterministic path index                                   |
| WIKI-05   | `docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md` | Generated             | Coverage snapshot                                        | English               | Counts safe paths by bucket, category, and role            |

## Generation and Enforcement Matrix

| Criterion | Concern                    | Implementation                                                                                                                    | Evidence                                                                     | Status                | Gap / caveat                                                                                     | Confidence |
| --------- | -------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------ | ---------- |
| WIKI-06   | Path source                | `git ls-files`, plus a small required-local-path escape hatch for in-progress contract files                                      | `scripts/knowledge/generate-llm-wiki-index.sh`                               | Implemented           | The escape hatch means local output can differ from a clean checkout until the paths are tracked | High       |
| WIKI-07   | Secret exclusion           | Any path under `secrets/` is rejected except `secrets/README.md`                                                                  | Generator safe-candidate filter                                              | Implemented           | Enforced at generation and re-scanned by the contract check                                      | High       |
| WIKI-08   | Noise exclusion            | Excludes `graphify-out/`, `volumes/`, `node_modules/`, `.git/`, build directories, lockfiles, and minified artifacts              | Generator prefix and suffix filters                                          | Implemented           | Filters are extension and prefix based, not content based                                        | High       |
| WIKI-09   | Determinism                | Sorted paths, fixed section order, whole-file byte comparison in check mode                                                       | Generator check mode                                                         | Implemented           | Byte-exact comparison is stronger than a timestamp heuristic                                     | High       |
| WIKI-10   | Classification             | 12 fixed sections and 7 role labels derived from path and suffix                                                                  | Generator classify and role functions                                        | Partially Implemented | Role labels are extension-derived, not semantic; see WIKI-17                                     | High       |
| WIKI-11   | Freshness enforcement      | Repository contract check shells out to both generators with check mode and folds failures in                                     | `scripts/validation/check-repo-contracts.sh` LLM Wiki contract section       | Implemented           | Single enforcement point; see WIKI-19                                                            | High       |
| WIKI-12   | Registration enforcement   | Required literals must appear in seven index READMEs, preventing orphaning                                                        | Contract check README literal gates                                          | Implemented           | `AGENTS.md` is not among the gated files; see WIKI-18                                            | High       |
| WIKI-13   | Safety wording enforcement | Bans `file://` links, secret-reading phrasing, and claims that generated graph output is authoritative                            | Contract check safety scan                                                   | Implemented           | Literal and regex based                                                                          | High       |
| WIKI-14   | Typed contract ownership   | None. No Stage 00 typed contract governs the LLM Wiki                                                                             | `grep` over `docs/00.agent-governance/contracts/` returns no match           | Missing               | Every other governed surface has a typed contract; this one is imperative shell only             | High       |
| WIKI-15   | Runtime hook               | None, by explicit policy decision rather than omission                                                                            | `docs/05.operations/policies/00-workspace/llm-wiki-maintenance.md`           | Not Applicable        | Policy states hooks are not added without a demonstrated failure mode                            | High       |
| WIKI-16   | Ownership                  | `doc-writer` role using the `knowledge-map-agent` function for the generated index; documentation maintainers for the curated map | Generated index maintenance block; `docs/00.agent-governance/scopes/docs.md` | Implemented           | Two different ownership vocabularies for one system                                              | Medium     |

## External Convention Comparison

| Dimension            | `llms.txt` proposal                               | `AGENTS.md` and `CLAUDE.md`                                                        | This repository's LLM Wiki                            |
| -------------------- | ------------------------------------------------- | ---------------------------------------------------------------------------------- | ----------------------------------------------------- |
| Consumer             | External model fetching a website                 | Coding agent at session start                                                      | Repo-local agent exploring the tree                   |
| Delivery             | HTTP fetch of a root path                         | Auto-loaded into context every session                                             | Read on demand through file tools; nothing auto-loads |
| Size discipline      | Concise by design, with a skippable optional tier | Codex caps the combined chain at 32 KiB; Claude documents a target under 200 lines | No budget; the generated index is 199,864 bytes       |
| Content              | Curated links with prose notes                    | Instructions, commands, conventions                                                | Path plus role label only, by contract                |
| Authoring            | Hand-curated                                      | Hand-written                                                                       | Hybrid: three authored artifacts, two generated       |
| Freshness            | Not specified                                     | Not specified                                                                      | Byte-exact regeneration gate in the contract check    |
| Safety boundary      | Not specified                                     | Not specified                                                                      | Secret allowlist, banned phrases, excluded-path scans |
| Full-content variant | `llms-full.txt` is the community companion        | Not applicable                                                                     | Explicitly forbidden                                  |

## Current-State Assessment

| Category        | Current state                                                                                                            | Primary comparison                                                       | Status                | Gap                                                                                                                                                  | Recommendation                                                                                                                                      | Canonical owner                                                    | Evidence                                             | Confidence |
| --------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------ | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ | ---------------------------------------------------- | ---------- |
| LLM-WIKI system | A generated, byte-exactly gated, safety-scanned path index with a small curated map and an explicit no-content contract. | `llms.txt` proposal, `AGENTS.md` convention, Claude memory documentation | Partially Implemented | No context budget on the largest artifact, no typed contract, no priority tier, and the one file most agents read first does not reference the wiki. | Keep the no-content contract, which is stronger than any external convention. Address the budget and registration gaps through their listed owners. | `docs/05.operations/policies/00-workspace/llm-wiki-maintenance.md` | Matrices above; generator and contract check sources | High       |

## Potential Follow-up / Gap

1. **WIKI-17 — No context budget on the generated index.** Codex caps its
   combined instruction chain at 32 KiB and Claude documents a target under 200
   lines. `llm-wiki-index.md` is 199,864 bytes across 1,464 lines. It is never
   auto-loaded, which is what keeps it harmless today, but an agent instructed
   to read the index ingests the whole file. There is no size gate, no
   chunking, and no per-section split. Owner:
   `scripts/knowledge/generate-llm-wiki-index.sh`.
2. **WIKI-18 — `AGENTS.md` does not reference the LLM Wiki.** Under the
   published `AGENTS.md` convention this is the first file many agents read,
   and `repository-map.md` advertises it as the provider-neutral entry shim.
   `grep -c llms AGENTS.md` returns 0, and `AGENTS.md` is not among the seven
   files whose registration literals the contract check gates. Owner:
   `AGENTS.md` and `scripts/validation/check-repo-contracts.sh`.
3. **WIKI-19 — Role labels are extension-derived, not semantic.** Seven labels
   are computed from filename and suffix, so 1,330 rows read as a filesystem
   listing rather than a map. The genuinely navigational content is the
   twelve-row curated table in `repository-map.md`, which is a fraction of the
   size. The published convention allows per-link notes describing what each
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
   `docs/05.operations/policies/00-workspace/llm-wiki-maintenance.md`.

## Source Rules

- Prefer tracked source files over the generated index whenever a fact must be
  authoritative.
- Treat generated graph output as advisory navigation context only.
- Never quote a secret value; `secrets/` is policy context, and only its README
  is indexable.
- Re-run both generators in check mode after any in-scope path change.

## Sources

- [llms.txt proposal](https://llmstxt.org/)
- [AGENTS.md convention](https://agents.md/)
- [Claude Code memory documentation](https://code.claude.com/docs/en/memory)
- [Codex AGENTS.md configuration](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [LLM Wiki category README](../../llm-wiki/README.md)
- [Repository map](../../llm-wiki/repository-map.md)
- [LLM Wiki maintenance policy](../../../05.operations/policies/00-workspace/llm-wiki-maintenance.md)
- [Docs scope](../../../00.agent-governance/scopes/docs.md)

## Source Retrieval Boundary

External conventions were retrieved on 2026-08-07. The
`developers.openai.com` guide path for `AGENTS.md` returned an HTTP 308
redirect and served no content directly; the redirect target on
`learn.chatgpt.com` is cited above instead. Published conventions are mutable
documentation and must be re-checked before operational use. Repository facts
in this document are counted from the tracked tree at baseline
`867a8146` and are reproducible from it.

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Quarterly, or when the generators or contract check change
- **Update Trigger**: Generator algorithm, contract check literals, LLM Wiki
  artifact structure, or external convention changes

## Related Documents

- [research pack index](./README.md)
- [documentation architecture](./documentation-architecture.md)
- [memory hierarchy](./memory-hierarchy.md)
- [workspace baseline](./workspace-baseline.md)
- [document metadata lifecycle](./document-metadata-lifecycle.md)
- [LLM Wiki category README](../../llm-wiki/README.md)
