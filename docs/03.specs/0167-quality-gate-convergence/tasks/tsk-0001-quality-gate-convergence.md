---
title: Make the Declared Quality Gate the Executed One
version: 1.0.0
type: sdlc/task
layer: specs
status: active
owner: "@buenhyden"
artifact_id: SPEC-0167-TSK-0001
parent_ids: [SPEC-0167, SPEC-0167-PLAN-0001]
created: 2026-09-03
updated: 2026-09-03
---

# Make the Declared Quality Gate the Executed One

## Objective

Route the lint and format toolchain back into CI, and reduce every quality
configuration to entries that describe the repository as it is.

## Inputs

- `.github/workflow-contract.yml`, `.github/workflows/ci-quality.yml`
- `.pre-commit-config.yaml` and the six root tool configurations
- `scripts/validation/run-ci-precommit.sh` and the gate contract and runner
- the tracked corpus each configuration claims to cover

## Work Log

### The gate that stopped running

`run-ci-gate.py` executes only what `public_gate.suite_roots` reaches. Walking
that graph against the CI job roots separates what the jobs declare from what
they can run:

| Node | Declared by a CI job | Reachable by a plan |
| :--- | :--- | :--- |
| `ci.pre-commit` -> `leaf.pre-commit` | yes | no |
| `leaf.docs-qa-gate-recommendations` | yes | no |
| `setup.compose-env`, `setup.repo-python-dependencies`, `setup.precommit-python-dependencies` | yes | no |

`run-ci-gate.py --profile full --explain` confirms it directly: the CI
pre-commit entrypoint appears in no row.

`1c620dd0` is the origin. It replaced eleven per-gate jobs, one of which ran
`--profile ci --gate ci.pre-commit` with `SKIP: eslint-nextjs` in its step
environment, with two jobs that select public profiles. The same commit deleted
the `eslint-nextjs` hook. What remained was an entrypoint demanding an
environment variable that nothing sets, guarding a route nothing takes.

### Why the aggregate could not simply be routed

`ci.pre-commit` has two children, and `setup.precommit-python-dependencies`
invokes the adapter subcommand `install-python-requirements`, whose
`ADAPTER_CONTEXTS` entry is the empty set -- "workflow setup steps, never
admitted as gate leaves". Routing the aggregate would have put a
never-admitted invocation in the plan. Routing `leaf.pre-commit` alone works,
and the bootstrap step installs the runner instead, which is what
`CI_DEPENDENCY_BOOTSTRAP` now says.

### The cycle

After `1c620dd0` the direction of control reversed: `pre-commit` gained
`public-validation-changed` and `public-validation-full` hooks that call the
gate. Routing the gate back into `pre-commit` closes a loop. The break is the
skip list, and the script now owns it rather than accepting one from a caller,
because a caller-supplied value is exactly what went missing and stayed missing.

### Configuration measured against the tree

| Finding | Measurement |
| :--- | :--- |
| `.shellcheckrc` `severity=warning` did nothing | shellcheck's output is byte-identical with that key and with `not-a-real-key=1`; severity is a command-line flag |
| `.editorconfig` said Python indents 2 | every tracked `.py` indents 4, which is what `ruff format` writes |
| `.editorconfig` preserved Markdown trailing whitespace | zero tracked `.md` files use a two-space hard break; the `trailing-whitespace` hook had already won |
| `.markdownlint-cli2.yaml` ignored `AGENTS.md` and `CLAUDE.md` as divergent | both lint clean with the ignores removed |
| It ignored all of `.claude/` | 39 files, 1 finding, in `.claude/output-styles/` alone, whose shape Claude Code fixes |
| Its `.agents/` twin was never ignored | 38 files, 0 findings |
| It ignored six paths the repository no longer has | `docs/04.execution/` (stage removed), two deleted documents, `archive/`, `artifacts/`, `.agent/` |
| `graphify-out/` must stay ignored | GRAPH_REPORT.md alone reports 1464 findings, and it is generated |
| `.gitignore` repeated four rules | the three `graphify-out/` negations and `.env` |

## Verification Evidence

- Plan composition, per execution context: `leaf.pre-commit` is present under
  `push` and `pull_request` in both profiles, absent under `local` in both.
- `run-ci-gate.py --profile full --explain` locally: no pre-commit row.
- `tests/validation/test_run_ci_precommit.sh`: passes; two mutants caught --
  dropping one hook from the skip list, and dropping the caller-supplied-SKIP
  rejection.
- Gate contract and runner suites: `test_ci_gate_contract`,
  `test_ci_gate_runner`, `test_github_workflow_contract`, `test_ci_gate_adapters`.
- All 782 tracked Markdown files linted under the new ignore rules.

## Review Evidence

Pending.

## Commit Ledger

Pending.

## Rulings

- The 30-minute job timeout bound is left alone. Raising it to fit the new leaf
  was tried and reverted: the bound is a deliberate guard in the workflow
  contract, and widening it to make room for new work inverts its purpose.
- The env allowlist is pruned to exactly the keys some node declares, and a test
  now asserts that equality rather than restating a literal. `EVENT_NAME`,
  `PR_BASE_SHA`, and `PUSH_BEFORE_SHA` stay readable by the runner from its own
  environment; they are simply no longer admissible as node keys.
- `ci.pre-commit` and the `ci.X` aggregates are kept. They declare job
  composition, which is a different claim from executability, and the scope
  chosen for this package was the nodes that cannot execute at all.

## Deferred Items

Pending.

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
