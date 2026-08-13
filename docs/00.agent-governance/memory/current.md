---
layer: agentic
status: active
---

# Current Project Memory

## Current objective

- Current task: `docs/03.specs/spec-0136-sdlc-taxonomy-convergence/task.md`
- Task 9 script-manifest enforcement and LLM Wiki generator consolidation is
  complete and committed as `707dc415` after final general and Python approval.

## Approved decisions

- Task 9 replaces two shell wrappers with one default-check Python generator
  and adds an executable manifest gate backed by machine authority.
- Task 10 is the next approved implementation boundary.

## Active boundary

- Task 9 changes are limited to manifest/generator ownership, current
  consumers, behavioral tests, generated outputs, and factual evidence.
- Runtime and Compose topology were unchanged; no external resources or
  sensitive runtime material were modified.

## Verified state

- Verified commit: `707dc415`
- Verified at: `2026-08-13T13:06:15+09:00`
- Review-remediation rounds are `17/17`, `5/5`, and `3/3`; manifest and
  generator suites are `37/37` and `6/6`, with CI `7/7`, workflow `39/39`
  (eleven declared Wave A skips), and governance `162/162`.
- Manifest validation, aggregate freshness, whole-repository bounded mutation
  checks, exact 43-entry generator parity, compilation, Ruff, and diff hygiene
  pass.

## Blockers and unverified facts

- No Task 9 blocker remains; final general and Python reviews are
  `APPROVED (C0/I0/M0)`.
- Repository-wide `check-repo-contracts.sh` retains pre-existing transitional
  failures owned by later Spec 136 tasks; Task 9 focused gates are green.

## Evidence links

- `docs/03.specs/spec-0136-sdlc-taxonomy-convergence/task.md`
- `.superpowers/sdd/2026-08-07-sdlc-taxonomy-convergence/task-9-report.md`
- `scripts/manifest.yaml`
- `.github/workflow-contract.yml`

## Next handoff

- Begin Plan Task 10 at the approved validator-consolidation boundary without
  absorbing the Task 11 policy-monolith or Task 12 CI-alignment work.
