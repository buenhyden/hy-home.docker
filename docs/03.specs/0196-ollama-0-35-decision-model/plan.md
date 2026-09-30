---
title: "Ollama 0.35 Decision Model Rehearsal Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-09-30"
layer: "specs"
artifact_id: "SPEC-0196-PLAN-0001"
parent_ids:
- "SPEC-0196"
created: "2026-09-30"
---

# Ollama 0.35 Decision Model Rehearsal Plan

## Objective

Deliver and verify [SPEC-0196](spec.md) as a reversible, single-service upgrade and local decision-model rehearsal.

## Dependencies

- Existing healthy `hy-home-infra` Ollama service and model volume.
- NVIDIA Container Toolkit and the current GTX 1060 6 GiB path.
- Official `ollama/ollama:0.35.0` and `tev1:0.8b` registry artifacts.
- Independent infrastructure review before the image pull or recreate.

## Execution Sequence

1. W1 Baseline: record the current project, image digest, model digests, model volume, GPU/driver, port, health, and rollback target (criteria 2, 3).
2. W2 Configuration: update the image pin and derived projection (criterion 1).
3. W3 Preflight: render and validate Compose, inspect the exact diff, and obtain independent infrastructure review (criteria 1, 2).
4. W4 Rollout: pull `0.35.0`, recreate only `ollama` with `--no-deps`, and verify health, version, boundaries, and preserved models (criteria 2, 3).
5. W5 Model smoke: pull `tev1:0.8b`, record its digest, run the synthetic decision request with `keep_alive: 0`, check the existing embedding model, exporter and Open WebUI backend connectivity, and record limits (criteria 4, 5).
6. W6 Documentation handoff: record the completed bounded API, version-pin source of truth, scoped recreate, and non-destructive recovery boundary in the existing Guide and Runbook (criteria 1, 4, 5).

## Risk and Rollback

The named model volume is never removed. If W4 or W5 detects a service regression, restore the Compose pin to `ollama/ollama:0.34.2`, regenerate the projection, and recreate only `ollama` with `--no-deps`; verify the previous image digest, health, catalog, and connectivity. A failed model smoke does not authorize deleting any model artifact.

## Verification

- Existing `infra-validate` static checks and scoped Compose render.
- Container health, `ollama --version`, `/api/tags`, GPU visibility, and unchanged inspect boundaries.
- Schema and numeric invariants for one `/v1/systemone` response.
- One synthetic `/api/embed` request, exporter metrics, and Open WebUI container-to-Ollama `/api/tags` request.
- Existing Guide and Runbook instructions for the synthetic decision call, version-pin source of truth, and non-destructive rollback boundary.

## Rulings

- 2026-09-30: The owner requested the `0.35.0` upgrade and a trial of a decision model. `tev1:0.8b` is selected as the bounded 812 MB candidate; no automatic integration is included.
