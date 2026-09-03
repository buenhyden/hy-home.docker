---
title: Make the Declared Quality Gate the Executed One
version: 1.0.0
type: sdlc/task
layer: specs
status: completed
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

### The backlog the route would have exposed

`pre-commit` passes only changed files, so findings accumulate in files nobody
touches. The approved all-files wrapper, run against the pinned hook revisions,
gave the real number:

| Run | Result | Files rewritten |
| :--- | :--- | ---: |
| First | `hook_result=failed` | 27 |
| After accepting the fixes | `hook_result=failed`, `changed_count=0` | 0 |
| After the ten manual findings | `hook_result=passed hook_exit=0` | 0 |

Of the 27, twenty-five were Markdown documents markdownlint fixes itself and two
were the test files edited earlier in this Task, which `ruff format` rewraps --
evidence that the formatter now reaches work an agent produces.

The ten that no formatter fixes had been miscounted in an earlier tally of mine:
the pattern matched `file.md:LINE error` while MD033 emits `file.md:LINE:COL`.
The totals reconcile exactly at 39 = 29 auto-fixed + 10 manual.

## Verification Evidence

- Plan composition, per execution context: `leaf.pre-commit` present under
  `push` and `pull_request` in both profiles, absent under `local` in both.
- `run-ci-gate.py --profile full --explain` locally: no pre-commit row.
- `tests/validation/test_run_ci_precommit.sh`: passes; two mutants caught --
  dropping one hook from the skip list, and dropping the caller-supplied-SKIP
  rejection.
- Gate contract and runner suites: `test_ci_gate_contract`,
  `test_ci_gate_runner`, `test_github_workflow_contract`,
  `test_ci_gate_adapters`.
- 774 tracked Markdown files under the new ignore rules: 0 findings.
- `run-agent-precommit-all-files.sh`: `hook_result=passed hook_exit=0`,
  `changed_count=0`, `unexpected_count=0`.
- `run-ci-gate.py --profile full` -> `EXIT=0`, 18 OK suites, after each commit.
- `.gitignore` deduplication: `git check-ignore` on eight probe paths before
  and after is byte-identical.

## Review Evidence

The route was measured before it was opened. Had it been opened on the state
this Task began from, CI would have failed on 27 files the local hook had never
looked at. That ordering -- verify the corpus, then route -- is the reason the
routing commit is green.

Corrections made during the work rather than carried:

| Severity | Site | Defect |
| :--- | :--- | :--- |
| high | this Task's own change | A `cd` into a scratch directory moved the shell to the main checkout, where two edits landed. Caught by `git status`, reverted with `git checkout --`, and reapplied in the worktree with absolute paths. |
| medium | this Task's own change | Raising the job timeout to 45 minutes broke eighteen contract tests. The bound is deliberate; the change was reverted rather than the bound widened. |
| medium | this Task's own analysis | `local.generated-freshness` was reported as unreachable. It is a declared `profile_roots` root; the walk had only covered job roots and public suites. Retracted. |
| low | this Task's own analysis | The per-rule tally silently dropped every finding carrying a column number, hiding nine MD033 findings until the wrapper surfaced them. |

## Commit Ledger

| Commit | Scope |
| :--- | :--- |
| `3989da58` | route `leaf.pre-commit`; drop the dead QA node; reconcile configuration with the tree |
| `858dd13c` | the 27-file auto-fixable backlog |
| `8bf30bd1` | the ten findings no formatter fixes |

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

- `leaf.repo-contracts` and `leaf.local-script-manifest` are the same
  invocation of `check-script-manifest.py` with no arguments, under two gate
  ids. Both are declared profile roots, so neither is dead; collapsing them
  changes what the local profiles declare and is its own decision.
- The five `ci.X` / `local.X` aggregate pairs differ only by a setup child, and
  the public gate routes the `local.` side, so `setup.compose-env` and
  `setup.repo-python-dependencies` never execute. They describe workflow steps
  rather than gate leaves, which is defensible, but nothing states that.
- `ci.validation-changed` and `ci.validation-full` declare identical children
  while running different profiles, so the job DAG describes a superset of what
  either job does.
- `examples/sample-web-service/site/index.html` still has no formatter, carried
  from SPEC-0166.
- The 30-minute job timeout now has to accommodate a full-corpus `pre-commit`
  run on a cold GitHub runner. That cannot be measured from here; the first CI
  run is the measurement.

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
