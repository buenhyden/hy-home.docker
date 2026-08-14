---
status: draft
artifact_id: reference:agentic-engineering-research:llm-wiki-system
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-14
review_cycle: on-source-change
---

# Reference: LLM Wiki Navigation, Safety, and Freshness System

## Overview

The workspace LLM Wiki is a repo-local, on-demand navigation system. A thin
root `llms.txt`, human README discovery, a curated repository map, a generated
path-only index, and a generated coverage summary route agents to canonical
tracked sources. They do not copy full source content, publish a website,
replace runtime truth, or auto-load into every agent session.

Two shell generators independently render the index and coverage outputs from
safe paths derived from `git ls-files`. Their `--check` modes compare complete
rendered bytes with the committed outputs. On the Task 6 baseline commit
`25acd86225d98151f9149072aff6b60511c62695`, both named checks exit 1 because
their outputs were stale. Task 6 recorded those observations without
regenerating them. Task 9a/10b subsequently regenerated both outputs through
their canonical generators as part of the pack's route switch; the Stage 04
Task ledger records a canonical write/check `PASS` at 1,339 index rows and
1,338 coverage safe paths. This reference did not re-run either generator; the
current byte-exact `--check` result must still be re-confirmed by a task
authorized to execute them.

## Purpose

Satisfy REQ-23 by tracing LLM-facing discovery, local generation, safety
exclusions, metadata behavior, current output state, freshness ownership, and
all fourteen scope implications without exposing private data or conflating a
repository contract result with byte-exact generator freshness.

## Repository Role

This Stage 90 reference describes the system but owns none of its operational
behavior. Root entrypoints and README routes own discovery, the two generators
own their exact outputs, Stage 05 policy owns maintenance controls, Stage 99
profiles own metadata interpretation, and tracked source files own actual
repository or runtime facts. Graphify remains advisory and excluded from both
generated evidence sets.

## Scope

### In scope

- Root `llms.txt`, root `AGENTS.md`, root and registered README discovery.
- The curated map, current generated index, and current coverage snapshot.
- Both generators, their path admission, exclusions, classification, rendering,
  and exact `--check` behavior.
- Metadata and LLM Wiki safety checks in the current repository validator.
- Current external `llms.txt` and `AGENTS.md` convention comparisons.
- Freshness evidence, gaps, limits, owners, and fourteen-scope implications.

### Out of scope

- Regenerating or editing either generated output.
- Editing generators, validators, `llms.txt`, `AGENTS.md`, READMEs, routes,
  policies, templates, or metadata profiles.
- A public wiki, full-content bundle, `llms-full.txt`, external model call,
  runtime hook, deployment workflow, or Graphify publication path.
- Secret contents, credentials, tokens, private keys, shell history, raw logs,
  ignored volumes, dependency trees, runtime state, or remote enforcement.

## Definitions / Facts

### LLM-facing convention boundary

| Convention             | Verified external intent                                                                                                                                                                             | Workspace implementation and boundary                                                                                                                                                                                      |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/llms.txt` proposal   | A root Markdown entrypoint for helping models use a website at inference time. The H1 is the only required section; summary, details, file lists, and an optional lower-priority section may follow. | Root `llms.txt` is a 30-line repo-local navigation file with relative links and stronger safety exclusions. It is not a claim of public-site or proposal-wide conformance.                                                 |
| `AGENTS.md` convention | A predictable standard-Markdown instruction file for coding agents; a root file may be refined by nearer files, and direct user instructions prevail.                                                | Root `AGENTS.md` is a seven-line bootstrap shim into Stage 00 governance and Memory. It contains no direct `llms.txt` or LLM Wiki link. Instruction discovery and on-demand repository navigation remain distinct systems. |
| Root README            | Human-facing project map and verification entrypoint.                                                                                                                                                | It registers `llms.txt`, the LLM Wiki directory, curated map, generated index, and index freshness command.                                                                                                                |

Both external convention pages returned HTTP 200 on 2026-08-08. They are
mutable convention sources, not evidence that a provider loaded these local
files or that any model followed their contents. Re-fetched directly this
revision (2026-08-14), both conventions moved in ways worth recording even
though neither changes this workspace's implementation:

- `llmstxt.org` now presents a **v2** of the proposal, explicitly revised
  after "two years of adoption." The load-bearing structural claim this
  reference already cites (H1-only-required, optional lower-priority
  section) is unchanged, but v2 drops the `llms_txt2ctx` tool's special
  mechanical meaning for the `Optional` heading — it "no longer carries
  mechanical semantics for automated processing," remaining only a human
  convention — and adds standard `rel="alternate"`/`rel="describedby"` link
  relations and hierarchical (most-specific-file-wins) subdirectory
  coverage, neither of which this repository's single root `llms.txt`
  exercises. This is **External mutable**, re-verified fresh; it does not
  change the workspace disposition row above.
- `agents.md` now states the convention is governed by the **Agentic AI
  Foundation under the Linux Foundation**, used by "over 60k open-source
  projects," with the closest-file-wins precedence this reference already
  cites unchanged. The governance-body detail is new since 2026-08-08 and is
  recorded here as landscape context; it does not add a repository
  obligation, and this workspace's root `AGENTS.md` remains a seven-line
  shim regardless of upstream adoption scale.

### Current navigation architecture

| Layer                       | Current tracked owner                                                               | Function                                                                                                                                 | Evidence and limit                                                                                                                                                                                                                             |
| --------------------------- | ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Human discovery             | `README.md` and seven README registration surfaces named by the repository contract | Routes contributors to the machine entrypoint, map, outputs, scripts, and maintenance docs.                                              | Literal registration is validator-checked; discoverability or usage is not observed.                                                                                                                                                           |
| Agent instruction discovery | `AGENTS.md` -> Stage 00 bootstrap/provider/Memory owners                            | Loads repository execution rules for compatible agents.                                                                                  | No direct LLM Wiki link in the root shim; provider loading is not proven by the tracked file.                                                                                                                                                  |
| Thin machine entrypoint     | `llms.txt`                                                                          | Links nine canonical entrypoints and states tracked-source, runtime, secret, volume, Graphify, public-site, and full-content boundaries. | Authored file; repository contract gates required literals, not consumer behavior.                                                                                                                                                             |
| Curated navigation          | `docs/90.references/llm-wiki/repository-map.md`                                     | Maps eleven reader needs to canonical sources and maintenance entrypoints.                                                               | Small authored map; navigation aid only.                                                                                                                                                                                                       |
| Generated path index        | `generate-llm-wiki-index.sh` -> `llm-wiki-index.md`                                 | Emits categorized safe path links and suffix-derived role labels.                                                                        | Stored file is 1,473 lines / 202,188 bytes with 1,339 path rows. The Stage 04 Task ledger records a Task 9a canonical write/check `PASS` at this row count; this reference did not re-run the check itself.                                    |
| Generated coverage          | `generate-llm-wiki-coverage.sh` -> coverage snapshot                                | Emits source-bucket, category, and role counts with representative links.                                                                | Stored file is 127 lines / 11,911 bytes and states 1,338 safe paths, 17 buckets, 12 categories, and 7 roles. The Stage 04 Task ledger records a matching Task 9a canonical write/check `PASS`; this reference did not re-run the check itself. |
| Maintenance and recovery    | Stage 05 Guide, Policy, and Runbook                                                 | Defines when to check/refresh, safety controls, and recovery handoff.                                                                    | Tracked operations contract; no hook or execution event is inferred.                                                                                                                                                                           |

The stored index and coverage counts were measured directly from the current
committed files and cross-checked against the Stage 04 Task ledger's Task 9a
canonical write/check result, which independently reports the same 1,339/1,338
figures. This reference still did not execute either generator's `--check`
mode itself, so the Task ledger entry — not a re-run in this unit — is the
evidence for current byte-exact freshness.

### Generator comparison

| Dimension           | Index generator                                                                                                   | Coverage generator                                                               | Shared boundary                                                                                                                                            |
| ------------------- | ----------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Source set          | `git ls-files`, plus required local contract paths only when they exist.                                          | Same.                                                                            | Git-visible paths plus named local contract files; ignored/private state is outside observation.                                                           |
| Self-exclusion      | Excludes the index output itself.                                                                                 | Excludes both the coverage output and generated index.                           | Prevents derived output recursion.                                                                                                                         |
| Admission           | Root entrypoints; `.github/`, `.claude/`, `.codex/`; `docs/`, `infra/`, `scripts/`; and only `secrets/README.md`. | Same.                                                                            | `.agents/` and `.gemini/` do not satisfy the final admission rule even though they are current provider/compatibility surfaces elsewhere in the workspace. |
| Suffix rule         | Allows `.conf`, `.env`, `.graphql`, `.json`, `.md`, `.proto`, `.sh`, `.toml`, `.txt`, `.yaml`, `.yml`.            | Same.                                                                            | Unsupported suffixes are excluded before final root-membership acceptance.                                                                                 |
| Explicit exclusions | `graphify-out/`, `volumes/`, `.git/`, dependency/build/cache parts, minified files, and package-manager locks.    | Same.                                                                            | Secret content is excluded except `secrets/README.md`; path selection does not inspect secret values.                                                      |
| Rendered meaning    | Twelve navigation categories, relative links, and seven filename/suffix-derived roles.                            | Source-bucket/category/role counts and up to three examples per bucket/category. | Classification is navigational metadata, not semantic document quality or runtime truth.                                                                   |
| Freshness           | Reads the committed output and compares it byte for byte with the full rendered string.                           | Same.                                                                            | `--check` is the named exact freshness proof.                                                                                                              |

The coverage generator contains a `.agents/` source-bucket branch, but its
shared admission predicate never admits `.agents/` paths. Neither generator
admits `.gemini/`. This is a current coverage-design observation for the
generator owner, not authorization to widen the allowlist.

### Safety and metadata layers

1. **Path selection safety:** both generators use the same allowlist/exclusion
   structure, exclude secret content paths, and admit only the secret-handling
   README as policy context.
2. **Rendered-output safety:** relative links are generated from admitted paths;
   no file contents are bundled. The index explicitly rejects full-content and
   public-site roles.
3. **Repository literal/safety contract:** `check-repo-contracts.sh` checks the
   required files and README registrations, required boundary literals,
   disallowed `file://` links and unsafe phrases, public-site scoping, forbidden
   path markers in generated tables, and secret-link restrictions.
4. **Metadata interpretation:** generated outputs use `status` plus
   `generated_by`. The Stage 99 `generated` profile requires `generated_by`,
   allows `status`, and forbids authored identity/parent/freshness fields. The
   two LLM outputs are not among the three exact paths in
   `common.generated_outputs`; their present `generated_by` metadata still
   selects the generated profile, while byte ownership remains explicit in
   each file and generator.
5. **Canonical-source boundary:** `llms.txt`, the map, both outputs, and policy
   state that tracked owners—not generated navigation—remain authoritative.
   Graphify is excluded and advisory even when present.

These layers are complementary. The aggregate repository contract does **not**
invoke either generator in byte-exact `--check` mode; it validates structure,
registrations, literals, and safety rules. Therefore a repository-contract
result never substitutes for:

```bash
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
```

### Named freshness baseline

| Command                                                        | Historical Task 6 result                                    | Later Task-ledger result                                                                       | Interpretation and owner                                                                                                                                                          |
| -------------------------------------------------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check`    | Exit 1: `FAIL: stale generated LLM Wiki index`              | Task 9a canonical write/check recorded `PASS` at 1,339 rows in the Stage 04 Task ledger.       | Task 6 exit 1 is a preserved historical observation, superseded by the Task 9a/10b regeneration. This reference did not re-execute the command; the ledger entry is the evidence. |
| `bash scripts/knowledge/generate-llm-wiki-coverage.sh --check` | Exit 1: `FAIL: stale generated LLM Wiki coverage snapshot`  | Task 9a canonical write/check recorded `PASS` at 1,338 safe paths in the Stage 04 Task ledger. | Task 6 exit 1 is a preserved historical observation, superseded by the Task 9a/10b regeneration. This reference did not re-execute the command; the ledger entry is the evidence. |
| `bash scripts/validation/check-repo-contracts.sh`              | Aggregate validation is run separately for authored leaves. | Aggregate validation is run separately for authored leaves.                                    | May expose reference/profile or LLM literal/safety findings, but cannot change either freshness result because it does not execute the named checks.                              |

### Implementation status, gaps, and risks

- **Implemented:** thin authored entrypoint, human README registrations,
  curated map, two deterministic generators, two committed outputs, safety
  scans, maintenance ownership, and exact check modes.
- **Regenerated:** both generated outputs were stale at the Task 6 baseline
  and were subsequently regenerated by Task 9a/10b; the Stage 04 Task ledger
  records a canonical write/check `PASS` at 1,339 index rows and 1,338
  coverage safe paths, matching this reference's direct file measurement.
  Re-confirmed again this revision: `git log` shows neither generator script
  nor either generated output has changed since the commit that produced
  this PASS state, and direct `wc`/`grep` re-measurement of both stored
  files on 2026-08-14 still returns the same 1,339/1,338 figures. This is a
  second independent no-drift observation, not a re-run of `--check` itself.
  This reference did not itself run either generator, so the ledger entry —
  not a fresh `--check` execution — is the evidence for the current PASS
  state.
- **Partial discovery:** root README exposes the LLM Wiki; root `AGENTS.md`
  delegates to governance but does not link it directly. The system is
  on-demand, and no tracked evidence proves which route agents actually read.
- **Coverage question:** `.agents/` and `.gemini/` are omitted from generated
  safe paths by the final allowlist despite being tracked compatibility/provider
  surfaces. A future approved generator change must decide intent and preserve
  safety; this reference does not prescribe the answer.
- **Context risk:** the index is large, but it is not auto-loaded by the
  local contract. Size alone does not prove context consumption or failure.
- **Evidence risk:** passing only `check-repo-contracts.sh` can leave stale
  bytes undetected regardless of the current PASS state, because it does not
  execute either named `--check` command. CI/QA owners must retain both
  explicit freshness commands wherever byte-exact currency is required.
- **Privacy boundary:** no ignored file, secret value, volume, raw log, private
  provider state, or external model interaction was read for this analysis.

## Scope Implications

| Scope          | LLM Wiki implication                                                                                                                                              |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agentic`      | `AGENTS.md` instruction loading and `llms.txt` navigation are distinct; provider execution or actual context ingestion remains unverified.                        |
| `architecture` | The map can route to architecture owners, but generated navigation cannot replace ARDs, ADRs, Specs, or architectural review.                                     |
| `backend`      | No current backend application surface was established; future APIs may add safe paths only after approved source and documentation owners exist.                 |
| `common`       | Relative links, deterministic ordering, naming, review, and diff hygiene apply to both authored and generated surfaces.                                           |
| `docs`         | Direct owner of authored navigation and generated-document workflow; exact freshness checks are required after applicable path changes.                           |
| `entry`        | Gateway paths may be indexed as tracked infra/config context; live edge, certificate, and request behavior remain outside the wiki.                               |
| `frontend`     | Storybook paths are not admitted by the current final allowlist unless they match an admitted top-level surface; no product frontend coverage is inferred.        |
| `infra`        | Admitted `infra/` paths are navigation only. Compose definitions do not prove running services, health, backup, or deployment.                                    |
| `meta`         | Generated-profile semantics, path classification, coverage categories, and exact owners are metadata concerns; changes route through approved Stage 00/99 owners. |
| `mobile`       | No current mobile source surface was established; mobile navigation is not applicable until an approved surface exists.                                           |
| `ops`          | Stage 05 Guide/Policy/Runbook own maintenance and recovery; no runtime hook or successful refresh event is inferred from their presence.                          |
| `product`      | Product intent should determine which canonical sources deserve curated prominence; the index's exhaustive path list is not prioritization evidence.              |
| `qa`           | Must distinguish literal/safety contract checks from the two named byte-exact freshness checks and preserve failing baselines until their owner acts.             |
| `security`     | Secret contents, volumes, dependencies, minified outputs, raw logs, and Graphify evidence are excluded; only `secrets/README.md` is admitted as policy context.   |

## Sources

| Source                                                                                                                        | Accessed   | Class                            | Verification state                                                                                                                                                    |
| ----------------------------------------------------------------------------------------------------------------------------- | ---------- | -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`llms.txt` proposal, re-fetched](https://llmstxt.org/)                                                                       | 2026-08-14 | External mutable                 | Direct page HTTP 200; now v2 — H1-only-required and optional-section structure unchanged, `llms_txt2ctx` mechanical semantics dropped, link-relation discovery added. |
| [`llms.txt` v1-to-v2 changes](https://llmstxt.org/changes.html)                                                               | 2026-08-14 | External mutable                 | Direct page HTTP 200; itemizes the discoverability, URL-flexibility, hierarchy, and semantics changes cited above.                                                    |
| [`AGENTS.md` convention, re-fetched](https://agents.md/)                                                                      | 2026-08-14 | External mutable                 | Direct page HTTP 200; root/nearest-file/standard-Markdown claims unchanged; now states Agentic AI Foundation / Linux Foundation governance and 60k+ project adoption. |
| [Root LLM entrypoint](../../../../llms.txt)                                                                                   | 2026-08-11 | Workspace tracked                | Complete 30-line file re-read; unchanged from Task 6 baseline.                                                                                                        |
| [Root agent shim](../../../../AGENTS.md)                                                                                      | 2026-08-11 | Workspace tracked                | Complete seven-line file re-read; no direct LLM Wiki registration; unchanged.                                                                                         |
| [Root README](../../../../README.md)                                                                                          | 2026-08-08 | Workspace tracked                | LLM Wiki routes and index-check entrypoint verified directly.                                                                                                         |
| [LLM Wiki references](../../llm-wiki/README.md)                                                                               | 2026-08-08 | Workspace tracked                | Current category, safety, generation, and ownership description.                                                                                                      |
| [Curated repository map](../../llm-wiki/repository-map.md)                                                                    | 2026-08-08 | Workspace tracked                | Eleven current need-to-owner rows; advisory navigation only.                                                                                                          |
| [Index generator](../../../../scripts/knowledge/generate-llm-wiki-index.sh)                                                   | 2026-08-11 | Workspace tracked executable     | Now a 553-line generator (grew from 336 lines with an unrelated Gate 9 manifest-mode addition); read but not executed by this reference.                              |
| [Coverage generator](../../../../scripts/knowledge/generate-llm-wiki-coverage.sh)                                             | 2026-08-11 | Workspace tracked executable     | Now a 606-line generator (grew from 389 lines with an unrelated Gate 9 manifest-mode addition); read but not executed by this reference.                              |
| [Generated index](../../llm-wiki/llm-wiki-index.md)                                                                           | 2026-08-11 | Workspace generated              | Stored output inspected directly: 1,473 lines / 202,188 bytes / 1,339 path rows; Stage 04 Task ledger records Task 9a canonical write/check `PASS`.                   |
| [Generated coverage](../../data/knowledge/llm-wiki-stage-category-coverage.md)                                                | 2026-08-11 | Workspace generated              | Stored output inspected directly: 127 lines / 11,911 bytes / 1,338 safe paths; Stage 04 Task ledger records Task 9a canonical write/check `PASS`.                     |
| [Stage 04 Task ledger: generated-artifact inventory](../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md) | 2026-08-11 | Workspace tracked                | Records Task 9a canonical write/check `PASS` at 1,339 index rows and 1,338 coverage safe paths, superseding the Task 6 FAIL baseline.                                 |
| [Metadata profiles](../../../99.templates/support/document-metadata-profiles.yaml)                                            | 2026-08-08 | Workspace tracked                | Reference/generated roles and registered-output behavior verified.                                                                                                    |
| [Repository contract checker](../../../../scripts/validation/check-repo-contracts.sh)                                         | 2026-08-08 | Workspace tracked executable     | LLM Wiki literal/safety block read directly; does not invoke generators.                                                                                              |
| [Maintenance policy](../../../05.operations/policies/00-workspace/llm-wiki-maintenance.md)                                    | 2026-08-08 | Workspace tracked                | Refresh triggers, exclusions, exception, and no-hook boundary.                                                                                                        |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md)                                                                   | 2026-08-08 | Workspace tracked stale/advisory | Built from `f8a72211`; corroborated against direct sources and excluded from generator evidence.                                                                      |

## Maintenance

Run both named `--check` commands after applicable tracked path or route changes
and regenerate only through their canonical scripts in the approved unit.
Re-read the scripts, metadata profiles, safety block, discovery surfaces, and
actual generated outputs when their owners change. Reopen external convention
pages before relying on mutable guidance. Never conceal a stale result behind
an aggregate contract result. This reference's 2026-08-11 re-verification read
the current committed outputs and the Stage 04 Task ledger's Task 9a PASS
entry, but did not itself execute either `--check` command; a task authorized
to run the generators still owes the next live confirmation.

## Related Documents

- [Verification and validation](./verification-validation.md)
- [Documentation architecture](./documentation-architecture.md)
- [Document metadata lifecycle](./document-metadata-lifecycle.md)
- [Agent instructions and vibe coding](./agent-instructions-vibe-coding.md)
- [Workspace baseline](./workspace-baseline.md)
- [Scope application matrix](./scope-application-matrix.md)
- [LLM Wiki category](../../llm-wiki/README.md)
- [Execution Task](../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
