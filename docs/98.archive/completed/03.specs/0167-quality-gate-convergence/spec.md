---
title: Quality Gate Convergence Specification
version: 1.0.0
type: sdlc/spec
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0167
parent_ids: [REQ-0024, REQ-0026, AD-0030, ADR-0029]
created: 2026-09-03
updated: 2026-09-03
---

# Quality Gate Convergence Specification

## Overview

SPEC-0166 gave every file type one formatting owner. This package asks the next
question: does anything run those owners where it matters, and does the declared
configuration still describe the repository that exists.

Both answers were no. `1c620dd0` replaced eleven per-gate CI jobs with two jobs
that call `run-ci-gate.py --profile changed|full`. That runner executes only
what the public suite roots reach, and `ci.pre-commit` was never added to one.
The whole lint and format toolchain -- ruff, markdownlint, yamllint, shellcheck,
hadolint, actionlint, gitleaks -- has not run in CI since that commit. Its
CI-only entrypoint survived, still demanding `SKIP=eslint-nextjs` for a hook the
same commit deleted.

Separately, configuration accumulated entries for paths the repository no longer
has: a stage that was removed, two deleted documents, an ignore for a directory
whose name lost its `s`.

## Boundaries and Inputs

Owned here: which gates the public suites reach, the CI pre-commit entrypoint's
contract, the gate-node declarations that no plan can execute, and the key/value
content of the formatting and linting configuration files.

Not owned here: the rules each linter enforces, the two-job workflow shape, and
the 30-minute job timeout bound, which is left as the deliberate guard it is.

Inputs: `.github/workflow-contract.yml`, `.pre-commit-config.yaml`, the six
root-level tool configurations, and the tracked corpus they claim to describe.

## Behavior Contract

- Every gate node that a CI job declares is reachable by a plan that job runs,
  or it does not exist.
- Formatting and linting gate every push and pull request, through the
  changed-profile fallback suite rather than a job of their own.
- The gate and `pre-commit` do not invoke each other without a stated bound.
- A configuration entry names something the repository has today.
- A setting is declared where the tool reads it, and in exactly one place.

## Technical Approach

Route the executable leaf, not the aggregate. `ci.pre-commit` carries a setup
child that the adapter admits in no context, so adding the aggregate to a suite
would fail closed; adding `leaf.pre-commit` alone routes the work and leaves the
aggregate as the job-composition declaration it already was.

Break the orchestration cycle at the script that sits between the two
orchestrators, and let it own the skip list rather than trust a caller. Nothing
had ever supplied that value, which is how the missing route stayed invisible.

Verify each configuration claim against the tree by measurement -- run the tool,
count what it reaches -- rather than by reading the file.

## Interfaces and Data

| Surface | Change |
| :--- | :--- |
| `.github/workflow-contract.yml` | `leaf.pre-commit` routed; `SKIP` dropped; dead QA-recommendation node removed |
| `.github/workflows/ci-quality.yml` | bootstrap installs the pre-commit runner |
| `scripts/validation/run-ci-precommit.sh` | owns its skip list; rejects a caller-supplied one |
| `scripts/lib/gate/ci_gate_contract.py` | bootstrap constant; env allowlist pruned to declared keys |
| `scripts/validation/ci_gate_runner.py` | admits the entrypoint; excludes it locally |
| `.editorconfig` | Python indent matches ruff; Markdown whitespace matches the hook |
| `.shellcheckrc` | the unsupported `severity` key removed |
| `.markdownlint-cli2.yaml` | ignores reduced to paths that exist |
| `.prettierignore` | ownership table completed |
| `.gitignore` | duplicate rules removed |
| `docs/00.agent-governance/policies/quality-standards.md` | section 4 restated |

## Failure Modes and Guardrails

| Failure mode | Guardrail |
| :--- | :--- |
| Routing the gate into pre-commit makes the two recurse | The entrypoint owns a skip list naming both gate hooks, asserted in both directions by its test |
| The lint gate runs locally and fails on CI-only assumptions | `profiles == ("ci",)` filtering, plus an explicit local exclusion, verified per context |
| An ignore entry hides real content | Each removal is measured: lint the path with ignores off and count findings |
| A config cleanup silently changes tool behavior | Compare tool output before and after; treat an unchanged diff as the evidence |
| CI turns red on a backlog the hook never saw | Run the approved all-files wrapper before routing, and fix what it reports |

## Acceptance Contract

1. A CI-context plan contains `leaf.pre-commit`; a local plan does not.
2. No gate node is declared by a CI job and reachable by no plan.
3. The env allowlist equals the set of keys some node declares.
4. Every path named in a lint configuration exists in the tree.
5. `pre-commit run --all-files` is clean under the pinned hook revisions.
6. `run-ci-gate.py --profile full` exits 0.

## Traceability

- Continues SPEC-0166, which established single ownership; this package makes
  that ownership execute.
- Repairs a regression introduced by `1c620dd0`.

## Related Documents

- [Quality standards](../../../../00.agent-governance/policies/quality-standards.md)
- [Documentation protocol](../../../../00.agent-governance/policies/documentation-protocol.md)
