---
layer: agentic
---

# Memory: Stage Docs Lifecycle Audit

- Date: 2026-05-22
- Layer: docs
- Status: active
- Applies To: `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/`
- Tags: #docs #governance #traceability
- Retrieval Keywords: stage docs lifecycle audit, PRD ARD ADR Spec Plan Task Operations traceability, docs 01 05 review
- Last Verified: 2026-05-22

## Problem

The workspace goal depends on a clear lifecycle from requirements to
architecture, specs, execution, and operations. Earlier hardening focused on
runtime governance and targeted documentation repairs, but future agents need a
single advisory note that summarizes the current `docs/01` to `docs/05`
review surface and the remaining legacy-shape risks.

## Context

The stage taxonomy is implemented and validators pass, but many historical
documents predate the current templates. The safe implementation boundary is to
preserve historical evidence, fix clear validator-backed drift in scoped
changes, and avoid bulk rewrites that could alter recorded decisions or task
evidence.

Traceability review matrix:

| Stage | Review Focus | Current Finding | Disposition |
| --- | --- | --- | --- |
| `docs/01.requirements/` | PRD scope, success criteria, downstream links | All files have `## Related Documents`; success criteria and scope are present. Current template NFR heading is not uniformly present in legacy PRDs. | Treat as legacy template-shape debt unless a PRD is actively edited. |
| `docs/02.architecture/` | ARD/ADR separation, decision history, Compose architecture alignment | ARD and ADR indexes exist and all files have `## Related Documents`. Prior remediation marked canonical `0026` infra-net documents and deferred dated duplicates. | Preserve historical decisions; resolve duplicates only in a scoped architecture pass. |
| `docs/03.specs/` | Implementation contract, config/interface, verification, operations handoff | All files have `## Related Documents`; one leaf spec is missing a direct `## Verification` heading under a simple heading scan. | Verify during the next spec edit; do not rewrite the full spec tree now. |
| `docs/04.execution/` | Plan/Task separation, evidence, deviations, completion criteria | Plans expose verification and completion criteria. Many historical task files do not use the newest `## Evidence` / `## Completion Evidence` headings. | Keep historical evidence intact; update only touched task files to the current template contract. |
| `docs/05.operations/` | Guide/policy/runbook purpose separation and secret-safe content | Purpose profile validators pass. Broad heading drift remains in guides/runbooks, and secret scans flag prompt lines such as `read -rsp`, not stored secret values. | Treat prompt-line findings as false positives; keep checking actual secret values out of docs. |

## Resolution

This pass records the lifecycle audit as advisory memory and hardens the
runtime/governance contract around `.agents/`. It does not bulk-edit
`docs/01` to `docs/05`, because the observed gaps are mostly legacy
template-shape drift rather than validator-backed correctness failures.

## Prevention

- Before editing any target-stage document, load the mapped template from
  `docs/99.templates/`.
- Keep fixes scoped to touched documents and parent README synchronization.
- Use `check-repo-contracts.sh` and `check-doc-traceability.sh` as the
  completion gate for stage changes.
- Record broad legacy drift here or in a dedicated memory note instead of
  silently rewriting historical evidence.
- When checking for secrets in operations docs, distinguish interactive
  prompts from stored secret values.

## Evidence

- `bash scripts/validation/check-repo-contracts.sh`
- `bash scripts/validation/check-doc-traceability.sh`
- `bash scripts/validation/check-template-security-baseline.sh`
- `bash scripts/validation/validate-docker-compose.sh`
- Stage scan summary on 2026-05-22:
  - `docs/01.requirements`: 24 Markdown files, 24 with `## Related Documents`
  - `docs/02.architecture`: 51 Markdown files, 51 with `## Related Documents`
  - `docs/03.specs`: 37 Markdown files, 37 with `## Related Documents`
  - `docs/04.execution`: 70 Markdown files, 70 with `## Related Documents`
  - `docs/05.operations`: 268 Markdown files, 268 with `## Related Documents`

## Related Documents

- [Memory README](./README.md)
- [Progress log](./progress.md)
- [Documentation protocol](../rules/documentation-protocol.md)
- [Stage authoring matrix](../rules/stage-authoring-matrix.md)
- [Docs scope](../scopes/docs.md)
