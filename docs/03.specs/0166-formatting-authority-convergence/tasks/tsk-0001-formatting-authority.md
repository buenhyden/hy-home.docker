---
title: Move Formatting Authority into the Repository
version: 1.0.0
type: sdlc/task
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0166-TSK-0001
parent_ids: [SPEC-0166, SPEC-0166-PLAN-0001]
created: 2026-09-03
updated: 2026-09-03
---

# Move Formatting Authority into the Repository

## Objective

Leave one formatting owner per file type, pinned in the repository and enforced
by the gate.

## Inputs

- `~/.claude/prettier-hook.sh` as a measurement subject, not an edit target
- `.pre-commit-config.yaml`, `.prettierrc.json`, `.prettierignore`
- `scripts/lib/document_governance/operations_catalog.py`
- the 106 tracked Python files and 776 tracked Markdown files

## Work Log

The formatter was located outside the repository: an agent editor hook
dispatching `ruff format` for `.py` and `npx prettier` for `.md`, `.yaml`,
`.json`, and web types. Neither tool appeared in `.pre-commit-config.yaml`.

Measured disagreement between corpus and tool:

| Tool | Scope | Would change |
| :--- | :--- | ---: |
| `ruff format` | 106 Python files | 88 |
| `npx prettier` | 776 Markdown files | 596 |

No ruff configuration reduced the Python gap: line length 79 gave 97, 100 gave
92, 120 gave 93, and single quotes gave 105, against 88 at the defaults. The
repository is hand-formatted, not formatted to any setting.

Prettier's unique coverage was one HTML file. Every other type it touches
already has an owner, and it holds JavaScript options for a tree with zero
JavaScript outside the excluded Storybook workspace. The repository's own Stage
90 research had already recorded it as "configuration only / not enforced".

Applying `ruff format` as a measurement failed two tests with 17 findings, all
`active-operations-reference-invalid`. The cause was sixteen lines that recorded
retired routes and satisfied a line-oriented scan by splitting the path across
adjacent string literals:

    "docs/05.operations/" "guides/04-data/analytics/README.md",

The check was met by typography. That is why the decoupling had to come first.

Corrections made during the work rather than carried:

| Severity | Site | Defect |
| :--- | :--- | :--- |
| medium | this Task's own change | Removing `.prettierrc.json` alone would have left Prettier running with its own defaults. The no-op was verified by running `prettier --check` afterwards, not assumed from the deletion. |
| low | this Task's own change | A renumbering loop applied repeatedly and left four sections numbered 8. Rewritten to derive each number from an ordered list. |

## Verification Evidence

- `run-ci-gate.py --profile full` -> `EXIT=0`, 18 OK suites, after each of the
  three commits.
- `ruff format --check` on every tracked Python file -> 106 already formatted.
- `npx prettier --check` on documents that previously failed -> all matched, so
  the external hook is a no-op here.
- Retired-route scan: an unmarked reference to a retired route reports; a
  marker on the preceding line does not exempt the line below it; the scan
  reports 0 findings on the corpus.

## Review Evidence

Each step was verified against the full gate before the next began. The
reformat commit is green only because the decoupling commit precedes it, which
the ledger order records.

## Commit Ledger

| Commit | Scope |
| :--- | :--- |
| `37dbb59c` | retired-route scan honours a stated marker |
| `bb72acfa` | ruff pinned and applied; Prettier configuration removed |
| `411263bc` | ownership recorded in the quality policy |

## Rulings

- Prettier is removed rather than scoped, but `.prettierignore` is kept. It is a
  registered target-surface path and the only lever this repository has over a
  hook that lives outside it.
- The exemption marker is a deliberate, greppable bypass. It is better than the
  alternative it replaces, which was an invisible bypass that any formatter
  could undo by accident.
- ruff's defaults are adopted as the pinned values because measurement chose
  them, not because they are defaults.

## Deferred Items

- `scripts/validation/run-ci-precommit.sh` requires `SKIP=eslint-nextjs`, but
  `eslint-nextjs` appears zero times in `.pre-commit-config.yaml` and no
  workflow invokes the script. The requirement names a hook that does not exist,
  and its tests assert the requirement. Removing a tested CI contract with no
  consumer is its own decision.
- `examples/sample-web-service/site/index.html` now has no formatter. It was
  Prettier's only unique coverage.

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
