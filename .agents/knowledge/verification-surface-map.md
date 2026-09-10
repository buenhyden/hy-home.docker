---
title: "Verification Surface Map"
version: "0.5.1"
type: "governance/knowledge"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-08"
created: "2026-09-06"
observed_at: "2026-09-08"
review_cycle: "on-gate-change"
---

# Verification Surface Map

## Overview

Which check covers which change, and where each check lives. Use it to predict
what a change will run before running it, and to find the owner of a failure.
The workflow contract owns the actual composition; this map is navigation.

## Scope

The two public validation profiles, the six public suites, their root gate
nodes, the prefix rules that select suites for a changed path, and the leaves
the local context withholds. Excluded: Hosted CI job scheduling, remote branch
protection, and any runtime observation.

## Public Entrypoints

| Command | Use |
| --- | --- |
| `python3 scripts/validation/run-ci-gate.py --profile changed` | The routine local gate for a working-tree change |
| `python3 scripts/validation/run-ci-gate.py --profile changed --explain` | Inspect the selected leaves without executing them |
| `python3 scripts/validation/run-ci-gate.py --profile full` | Every locally admitted suite; nine leaves stay remote, listed below |
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
| `document-lifecycle` | document corpus lifecycle; document lifecycle regressions |
| `operations` | operations catalog; supply chain; Compose validation; infrastructure hardening; template security baseline; quickwin baseline |
| `repository-integrity` | diff hygiene; shell syntax; script manifest; tech stack version drift; workflow harness; dependency vulnerability audit; git-flow contract; frontend quality; Storybook coverage; `zizmor`; pre-commit; repository integrity regressions |

## What the Local Context Withholds

`--profile full` names every suite, not every leaf. `_LOCAL_EXCLUDED_GATE_IDS`
in `scripts/validation/ci_gate_runner.py` removes nine leaves when the context
is `local`, so a local pass is not a CI pass and must not be reported as one.
The suite table above lists these among their roots because CI reaches them.

| Withheld leaf | Why it is not local | Local route |
| --- | --- | --- |
| `leaf.pre-commit` | Its entrypoint refuses to run outside GitHub Actions | The same hook suite, through `scripts/validation/run-agent-precommit-all-files.sh` |
| `leaf.git-flow-contract` | Reads `PR_TITLE` and `HEAD_REF`, and its adapter admits only `pull_request` | None; a real pull request is the input |
| `leaf.frontend-lint` | Needs `npm ci` in `projects/storybook/nextjs` | Install the project dependencies, then run the package script directly |
| `leaf.frontend-typecheck` | Needs `npm ci` in `projects/storybook/nextjs` | Install the project dependencies, then run the package script directly |
| `leaf.frontend-build` | Needs `npm ci` in `projects/storybook/nextjs` | Install the project dependencies, then run the package script directly |
| `leaf.frontend-quality` | Needs `npm ci` in `projects/storybook/nextjs` | Install the project dependencies, then run the package script directly |
| `leaf.storybook-coverage` | Needs `npm ci` and a Playwright browser install | Install both, then run the package script directly |
| `leaf.dependency-vulnerability-audit` | `npm audit` reads a remote advisory database | Run the audit where that network access is approved |
| `leaf.zizmor` | Runs a `uv`-installed pinned `zizmor` and writes SARIF | Install the pinned version where that is approved |

Dependency installation is a setup leaf, never part of a local gate run: the
local gate installs nothing. `install-playwright` and `run-zizmor-sarif` are
independently restricted to CI contexts inside the adapter, so removing a leaf
from this list alone would not make it reachable.

## What a Change Selects

The declared `repository-integrity` fallback is always included. Rows below
show the suites selected by each matching path rule, not a replacement for
that fallback. Exact prefixes remain owned by the workflow contract.

| Changed prefix | Suites selected |
| --- | --- |
| `.agents/`, `.claude/`, `.codex/`, `AGENTS.md`, `CLAUDE.md` | agent-governance, document-contract, document-graph, document-lifecycle |
| `README.md`, `_workspace/`, `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/90.references/`, `docs/98.archive/`, `docs/99.templates/` | document-contract, document-graph, document-lifecycle |
| `docker-compose.yml`, `docs/05.operations/`, `examples/`, `infra/`, `secrets/` | document-contract, document-graph, document-lifecycle, operations |
| `.github/`, `.pre-commit-config.yaml`, `evals/`, `projects/`, `scripts/`, `tests/` | all six suites |
| Root tool/commit paths declared in the contract, including `.cz.toml`, `.gitmessage`, and `ruff.toml` | repository-integrity |
| any other tracked path | repository-integrity, by the declared fallback |

A path with no matching rule still selects a suite. Silence is never the result
of an unmatched path.

For `changed`, the contract's `changed_root_rules` then selects the optional
frontend-quality and Storybook roots within those suites. Their current inputs
are workflow/pre-commit definitions, the Next.js package, scripts, and tests.
Known document/provider/root-tool paths alone omit those optional roots; the
dependency audit and other required roots remain selected. An unknown valid
path retains every root of its fallback-selected suite. Unavailable or invalid
changed-path evidence fails closed before planning. `full` retains all suite
roots before the execution-context exclusions above apply.

## Two Selectors, One Requirement

Two routing surfaces have different responsibilities:

- `.github/workflow-contract.yml` `public_gate.changed_path_rules` decides which
  suites a changed path needs.
- `.pre-commit-config.yaml` admits every path for both public hooks and sets
  `always_run: true`, so empty or deletion-only input does not omit validation.

The hook does not maintain a second impact list. Registered regressions compare
its admitted paths and always-run behavior with the public routing contract.
Automatic commit hooks observe the index with surviving untracked inputs;
direct local `changed` observes the staged/unstaged/untracked union. A receipt
from either route proves its own snapshot only.

## Generated Outputs and Staging Order

A generator that builds its inventory from `git ls-files --cached` cannot see an
added file until that file is staged, so a freshness check can pass on an
unstaged candidate and become stale the moment it is staged. The generators this
described were retired on 2026-09-10, so no tracked output carries that hazard
today; the rule is kept because it applies to the next one, and staging order is
the thing to get right before believing a freshness result. `graphify-out/`
is not a comparable case: it is untracked local output, so it produces no diff
to separate and the intermediate-stash race it once caused cannot occur.

## Test Ownership

| Layer | Location | Verifies |
| --- | --- | --- |
| Library behavior | `tests/lib/<domain>/` | importable logic in `scripts/lib/<domain>/` |
| CLI and context | `tests/validation/` | entrypoints, argv, execution context, aggregates |
| Synthetic input | underscore-prefixed modules beside their suite, such as `tests/lib/<domain>/_support.py` and `tests/validation/_sample_delivery_fixtures.py` | test-only inputs built deterministically; production code never reads them |
| Operational rehearsal | `examples/operations/` | reusable synthetic operational input |
| Agent output | `evals/` | deterministic, model-free fixture evaluation |

## Provenance

Suite/path/root routing and public hook settings were revalidated against
`.github/workflow-contract.yml`, `scripts/lib/gate/ci_gate_contract.py` and
`.pre-commit-config.yaml` on 2026-09-08 after the convergence implementation.
The previous claim that the path rules were unchanged is superseded by the
explicit root-tool rules and optional-root selection now described above.
The workflow contract remains the execution authority; a disagreement between
this navigation map and that source is a defect in this map. Dated execution
and staging-recovery receipts belong to the current Spec Package Task.

The local exclusion table is transcribed from `_LOCAL_EXCLUDED_GATE_IDS` and
`_PR_ONLY_GATE_IDS` in `scripts/validation/ci_gate_runner.py`, and the reasons
from the `gate_nodes` entries and adapter context sets those identifiers reach,
read at `6aa4287e21c56a7073356f67cb2c214df46618a7` on 2026-09-08. A registered
test compares the identifiers in that table against the runner constant, so the
two cannot drift apart silently.

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
- A leaf joins or leaves the local exclusion set in `ci_gate_runner.py`.
- The `tests/lib` and `tests/validation` ownership boundary changes, or a test
  location named in the Test Ownership table is added, moved, or emptied.

## Related Documents

- [Knowledge index](README.md)
- [Repository authority map](repository-map.md)
- [Quality standards](../governance/quality-standards.md)
- [Environment constraints](../governance/environment-constraints.md)
