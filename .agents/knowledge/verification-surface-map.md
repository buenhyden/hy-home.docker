---
title: "Verification Surface Map"
version: "0.2.0"
type: "governance/knowledge"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-07"
created: "2026-09-06"
observed_at: "2026-09-07"
review_cycle: "on-gate-change"
---

# Verification Surface Map

## Overview

Which check covers which change, and where each check lives. Use it to predict
what a change will run before running it, and to find the owner of a failure.
The workflow contract owns the actual composition; this map is navigation.

## Scope

The two public validation profiles, the six public suites, their root gate
nodes, and the prefix rules that select suites for a changed path. Excluded:
Hosted CI job scheduling, remote branch protection, and any runtime observation.

## Public Entrypoints

| Command | Use |
| --- | --- |
| `python3 scripts/validation/run-ci-gate.py --profile changed` | The routine local gate for a working-tree change |
| `python3 scripts/validation/run-ci-gate.py --profile changed --explain` | Inspect the selected leaves without executing them |
| `python3 scripts/validation/run-ci-gate.py --profile full` | The complete local surface |
| `python3 scripts/operations/provider_surface_renderer.py --check` | Provider projection drift, a separate direct interface |
| `scripts/validation/run-agent-precommit-all-files.sh` | The single approved all-files route; direct `pre-commit run` is prohibited |

Inspect with `--explain` before executing when a change touches an unfamiliar
surface. A leaf may need inputs the current authorization does not cover.

## Suites and Their Roots

| Suite | Root gate nodes |
| --- | --- |
| `agent-governance` | provider surface drift; agent-output eval fixture gate; agent governance contract; agent governance regressions; provider governance regressions |
| `document-contract` | repository metadata base; repository document metadata |
| `document-graph` | documentation traceability |
| `document-lifecycle` | document corpus lifecycle; document lifecycle regressions; LLM Wiki freshness; audit matrix freshness; security readiness freshness |
| `operations` | operations catalog; supply chain; Compose validation; infrastructure hardening; template security baseline; quickwin baseline |
| `repository-integrity` | diff hygiene; shell syntax; script manifest; tech stack version drift; workflow harness; dependency vulnerability audit; git-flow contract; frontend quality; Storybook coverage; `zizmor`; pre-commit; repository integrity regressions |

## What a Change Selects

| Changed prefix | Suites selected |
| --- | --- |
| `.agents/`, `.claude/`, `.codex/`, `AGENTS.md`, `CLAUDE.md` | agent-governance, document-contract, document-graph, document-lifecycle |
| `README.md`, `_workspace/`, `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/90.references/`, `docs/98.archive/`, `docs/99.templates/` | document-contract, document-graph, document-lifecycle |
| `docker-compose.yml`, `docs/05.operations/`, `examples/`, `infra/`, `secrets/` | document-contract, document-graph, document-lifecycle, operations |
| `.github/`, `.pre-commit-config.yaml`, `evals/`, `projects/`, `scripts/`, `tests/` | all six suites |
| any other tracked path | repository-integrity, by the declared fallback |

A path with no matching rule still selects a suite. Silence is never the result
of an unmatched path.

## Two Selectors, One Requirement

Two independent selectors decide whether the public gate runs:

- `.github/workflow-contract.yml` `public_gate.changed_path_rules` decides which
  suites a changed path needs.
- `.pre-commit-config.yaml` decides whether the public gate hook runs at all for
  the staged file set.

The second must admit every prefix the first names. A prefix the contract routes
but the hook selector omits produces a change that needs suites and runs none
locally. The reverse asymmetry is safe: a broader hook selector only runs the
gate more often. A registered test owns this relation so a divergence fails
rather than passing quietly.

## Generated Outputs and Staging Order

The LLM Wiki generator builds its inventory from `git ls-files --cached`, so an
added file is invisible to it until that file is staged. A freshness check run
on an unstaged working tree therefore reports fresh while the outputs are
already stale, and the truth appears only after `git add`.

Run the freshness check after staging, and carry the regenerated LLM Wiki
outputs in the same commit as the document that changed them. The separate-unit
rule in the quality standards targets `graphify-out/`, whose separation exists
to avoid the pre-commit intermediate-stash race, not the Wiki snapshots.

## Test Ownership

| Layer | Location | Verifies |
| --- | --- | --- |
| Library behavior | `tests/lib/<domain>/` | importable logic in `scripts/lib/<domain>/` |
| CLI and context | `tests/validation/` | entrypoints, argv, execution context, aggregates |
| Synthetic input | underscore-prefixed modules beside their suite, such as `tests/lib/<domain>/_support.py` and `tests/validation/_sample_delivery_fixtures.py` | test-only inputs built deterministically; production code never reads them |
| Operational rehearsal | `examples/operations/` | reusable synthetic operational input |
| Agent output | `evals/` | deterministic, model-free fixture evaluation |

## Provenance

Read from `.github/workflow-contract.yml` `public_gate` and
`.pre-commit-config.yaml` at repository commit
`9ede309a5b1feba91e6f8b973a729716b14c55ab` on 2026-09-06. Suite and prefix rows
are transcribed from those files, not summarized from prose. The workflow
contract remains the authority for execution; a disagreement between this map
and that file is a defect in this map.

The Test Ownership table has a different source and had no stated one when this
map was written, which is how it came to describe a `tests/fixtures/` layer that
a completed convergence had already emptied. Its rows are now read from
`git ls-files` on 2026-09-07, which reports zero tracked paths under that
prefix. A row here names a location that the tracked tree actually contains.

## Refresh Triggers

- A public suite is added, removed, or renamed.
- A root gate node joins or leaves a suite.
- A changed-path rule or the declared fallback changes.
- The public entrypoint set or its normalized arguments change.
- The `tests/lib` and `tests/validation` ownership boundary changes, or a test
  location named in the Test Ownership table is added, moved, or emptied.

## Related Documents

- [Knowledge index](README.md)
- [Repository authority map](repository-map.md)
- [Quality standards](../governance/quality-standards.md)
- [Environment constraints](../governance/environment-constraints.md)
