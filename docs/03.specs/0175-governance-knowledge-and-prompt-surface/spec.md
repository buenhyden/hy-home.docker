---
title: "Governance Knowledge and Prompt Surface Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-06"
layer: "specs"
artifact_id: "SPEC-0175"
parent_ids:
- "REQ-0024"
- "AD-0027"
- "ADR-0034"
created: "2026-09-06"
---

# Governance Knowledge and Prompt Surface Specification

## Overview

Introduce `.agents/knowledge/` and `.agents/prompts/` as registered canonical
categories, then use them in this package's own execution. `knowledge/` owns
verified routing from a repository surface to its canonical authority, plus the
repository's own vocabulary and verification-surface map. `prompts/` owns
reusable input and output contracts for handoff, independent diff review,
commit-message drafting, and test authoring.

The same change closes five defects found while establishing that boundary. The
Claude output style omits `keep-coding-instructions`, so it silently replaces
the provider's built-in engineering instructions. That same adapter is the sole
owner of the conversational-language rule that `standards.md` routes to
`output-style.md`, which states no such rule. The adapter also asserts a
per-stage artifact-language mandate that the tracked corpus contradicts for
Stage 03 and Stage 90. The local pre-commit gate selector omits prefixes the
workflow contract routes. The external capability-intake decision boundary has
no current canonical owner, and the recorded upstream identity for the external
agent catalog is stale.

## Boundaries and Inputs

- Baseline: `codex/0173-agent-governance-home` at
  `9ede309a5b1feba91e6f8b973a729716b14c55ab`, clean worktree, seven commits
  ahead of `origin/main` at `8176cdee732954415bc5462d6d4d43da4e319394`.
- SPEC-0173 remains active and untouched. Its Rulings forbid introducing a new
  policy, Spec, Plan, or Task inside that package, so this work takes its own
  package rather than extending that acceptance contract.
- In scope: `.agents/knowledge/**`, `.agents/prompts/**`, the canonical root
  inventory and profile set in `scripts/lib/agent_governance/`, the Stage 99
  registry profiles, templates, and template catalog, the Provider Registry
  `canonical_sources` list, the canonical output-style and documentation
  policies, the Claude output style, the pre-commit public-gate path selector,
  and the affected tests. `scripts/manifest.yaml` owns only `scripts/` and
  `evals/` and is not touched.
- Preserve unchanged: 14 role IDs, 23 skill IDs, six public suite names, two
  public profiles, permission profiles, work profiles, model rows, hook
  contracts, `generated_roots`, and every frozen archive body.
- Out of scope: REQ-0026, AD-0030, and ADR-0031 retention-owner promotion,
  which SPEC-0173 owns as a separate open design dependency. Also out of scope:
  push, pull request, merge, deployment, live Compose or service action,
  credential values, user-global settings, global installation, model
  entitlement change, and hook trust change.
- Deferred with a named reason rather than silently dropped: consolidating the
  Stage 90 curated repository map into `knowledge/`, extending model rows with
  context, cost, latency, and output ceilings, binding Codex `skills.config`,
  editor workspace-task integration, automated pull-request review expansion,
  and fixture reduction.

## Behavior Contract

1. The canonical root inventory admits exactly `README.md`, `governance`,
   `knowledge`, `prompts`, `roles`, and `skills`. Any other entry fails closed
   and is preserved for review, never deleted automatically.
2. Stage 99 owns the shape of both new categories. Each category has one member
   profile and one index profile because the registry's `{slug}` token is
   lowercase-only and cannot match `README.md`.
3. A `knowledge/` member routes to a canonical owner. It states no obligation,
   and it copies no policy body, design, specification, or runbook. It declares
   an observation date and a refresh trigger so staleness is detectable.
4. A `prompts/` member declares purpose, required inputs, output contract,
   prohibitions, failure handling, and the roles, skills, and evaluation
   criteria it applies under. It names the owning skill rather than restating
   that skill's ordered procedure.
5. Neither category owns execution state. The current Spec Package Task remains
   the only progress and handoff authority, and the existing unsupported-token
   guard against the retired shared progress ledger is unchanged.
6. Discovering a knowledge or prompt file grants no permission, tool, model, or
   approval. The already selected role's permission profile still governs.
7. A native provider adapter routes to canonical policy and does not restate it.
   The Claude output style keeps only presentation rules that are genuinely
   provider-specific and preserves the provider's built-in engineering
   instructions rather than replacing them by omission.
8. The pre-commit public-gate selector admits every prefix the workflow
   contract routes. A broader selector is safe; a narrower one produces a change
   that needs suites and runs none locally, and is a test failure rather than a
   documentation note.
9. The external capability-intake decision boundary has exactly one current
   canonical owner. A Stage 90 research member may describe it but cannot own it.
10. A dated external observation is added beside earlier observations. No
    earlier dated measurement is rewritten to look current.

## Technical Approach

Register before authoring. The registry profiles, templates, contract inventory,
and tests land first so that every file written under the two new roots is
validated by a registered profile from its first commit rather than retrofitted.

Take the contract change in two commits: a failing test that asserts the new
root inventory and profile set, then the implementation that satisfies it. The
canonical root inventory is a single pinned tuple in
`scripts/lib/agent_governance/agent_governance_contract.py`, so its failure mode
is a clear, value-free finding code rather than a partial pass.

Author the prompts before the knowledge files, then use both for the remaining
commits of this package. That ordering is what makes the required usage evidence
real work rather than a retrospective claim.

Treat the five defect fixes as separate reviewable commits. A reviewer can
reject the output-style change while accepting the new categories.

## Interfaces and Data

- `scripts/lib/agent_governance/agent_governance_contract.py`: `ROOT_ENTRIES`
  pins the canonical root inventory; `GOVERNANCE_PROFILES` pins the registered
  profile set that the registry must contain.
- `docs/99.templates/registry.json`: `profiles`, `template_roles`, and
  `transitions` own the shape and lifecycle of both categories.
- `docs/99.templates/templates/governance/knowledge.template.md` and
  `prompt.template.md`: the copyable sources.
- `.agents/governance/providers/registry.yaml`: `canonical_sources` lists every
  authored canonical file; `generated_roots` is unchanged.
- `.agents/knowledge/`: `README.md`, `repository-map.md`, `glossary.md`,
  `verification-surface-map.md`.
- `.agents/prompts/`: `README.md`, `handoff.md`, `diff-review.md`,
  `commit-message.md`, `test-design.md`.
- `.pre-commit-config.yaml` and `.github/workflow-contract.yml`: the two path
  selectors a new test proves consistent.
- `tests/lib/agent_governance/` and `tests/validation/`: contract and selector
  regression owners.

## Failure Modes and Guardrails

- A new category drifts into a second authority. Guard: registered required
  sections plus review. A knowledge or prompt file that states an obligation is
  routed back to `governance/`.
- Prose that names a retired path trips the unsupported-token guard. Guard:
  describe the retired surface without spelling its path; never weaken the
  pattern to admit the prose.
- A forward link to a document created in a later commit breaks link
  validation. Guard: the link lands in the commit that creates its target.
- Changing the root inventory without the registry, or the registry without the
  contract, half-lands the category. Guard: the failing test asserts both
  before either changes.
- The output-style change alters session behavior. Guard: an output style is
  read at session start, so the change takes effect on the next session and is
  reviewed as text, not as observed runtime.
- The pre-commit selector change widens which commits run the public gate.
  Guard: compare the two selectors as sets and record the exact added prefixes.
- Registry edits reformat the whole file. Guard: the file round-trips
  byte-identically under `json.dumps(..., indent=2, ensure_ascii=False)` plus a
  trailing newline; confirm that before and after each edit.
- Static parity is mistaken for runtime acceptance. Guard: record discovery,
  loading, invocation, and runtime acceptance as separate states.

## Acceptance Contract

1. The canonical root inventory admits exactly `README.md`, `governance`,
   `knowledge`, `prompts`, `roles`, and `skills`, and
   `check-agent-governance-contract.py --mode repository` passes.
2. Stage 99 registers `governance-knowledge`, `governance-knowledge-index`,
   `governance-prompt`, and `governance-prompt-index` with the `living`
   lifecycle, a `template_roles` entry, and a `transitions` entry each.
3. Two copyable templates exist under `docs/99.templates/templates/governance/`
   and the template catalog lists both registered types.
4. `.agents/knowledge/` contains exactly `README.md`, `repository-map.md`,
   `glossary.md`, and `verification-surface-map.md`. Each member declares an
   observation date and refresh trigger, routes to a canonical owner, and
   states no obligation.
5. `.agents/prompts/` contains exactly `README.md`, `handoff.md`,
   `diff-review.md`, `commit-message.md`, and `test-design.md`. Each prompt
   declares purpose, required inputs, output contract, prohibitions, failure
   handling, and applicability, and restates no skill procedure.
6. `canonical_sources` lists all nine new files,
   `provider_surface_renderer.py --check` reports zero drift, and
   `generated_roots` is unchanged.
7. `.claude/output-styles/hy-home.md` declares `keep-coding-instructions: true`
   and contains no language, documentation-routing, or completion policy of its
   own; it routes to the canonical owners instead. The conversational-language
   rule that `standards.md` already routes to `output-style.md` is stated there,
   and the artifact-language rule in `documentation-protocol.md` describes the
   corpus as measured rather than asserting a per-stage mandate the tracked
   files contradict.
8. The `.pre-commit-config.yaml` public-gate `files` selector admits a
   representative path for every prefix in the workflow contract's
   `changed_path_rules`, and a test fails when a routed prefix is not admitted.
9. The external capability-intake decision boundary has one current canonical
   owner reachable from `.agents/`, and the Stage 90 research member links to it
   instead of implying it owns the decision.
10. `RES-0002-m0003` records the 2026-09-06 upstream head
    `1454492577d1af4884722837f491fef14b501e21` as a new dated observation, and
    every earlier dated observation is preserved verbatim.
11. 14 role IDs, 23 skill IDs, six public suite names, two public profiles,
    permission profiles, work profiles, model rows, and hook contracts are
    unchanged.
12. This package's own execution uses at least the handoff, diff-review,
    commit-message, and test-design prompts and the repository map, and the
    Task records where each was used.
13. Focused validators pass for each changed authority surface, and the changed
    public profile passes on the final path set. A required but unexecuted check
    is recorded as BLOCKED or NOT_RUN and is never promoted to a PASS.
14. Final evidence distinguishes local-executed, configured,
    repository-enforced, unverified runtime, unverified entitlement, and
    unverified remote state.

## Traceability

- Requirements: [REQ-0024](../../01.requirements/0024-agent-governance-standardization.md),
  specifically REQ-0024-FR-0003 and REQ-0024-FR-0014.
- Architecture: [AD-0027](../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md).
- Decision: [ADR-0034](../../02.architecture/decisions/0034-canonical-knowledge-and-prompt-surfaces.md).
- Execution: SPEC-0175-PLAN-0001 and SPEC-0175-TSK-0001.
- External evidence reused, not duplicated:
  [RES-0002-m0003](../../90.references/research/0002-agentic-engineering-research-pack/m0003-ai-agent-catalogs.md),
  [RES-0002-m0008](../../90.references/research/0002-agentic-engineering-research-pack/m0008-harness-engineering.md), and
  [RES-0002-m0011](../../90.references/research/0002-agentic-engineering-research-pack/m0011-memory-hierarchy.md).
- Concurrent package: [SPEC-0173](../0173-governance-qa-surface-convergence/spec.md),
  which this package does not modify.

## Open Questions

Whether the Stage 90 curated repository map consolidates into
`.agents/knowledge/` remains open. It has tracked consumers in the LLM Wiki
generator, the reference validator, `llms.txt`, and four documents, so it
requires its own coordinated change and a registered data lifecycle transition.
Codex `skills.config` binding, model context and cost rows, editor task
integration, and automated pull-request review expansion each need an
observation or an owner decision this package does not supply.

## Operational Impact

This package changes tracked Markdown, JSON, YAML, and Python plus their tests.
It starts, stops, and reconfigures nothing. The output-style change takes effect
at the next provider session rather than the current one. Rollback is a reviewed
revert of the affected logical commit; no reset, clean, force push, or archive
body rewrite is part of the plan.

## Related Documents

- [Implementation plan](plan.md)
- [Stage 03 index](../README.md)
- [Canonical agent governance](../../../.agents/README.md)
