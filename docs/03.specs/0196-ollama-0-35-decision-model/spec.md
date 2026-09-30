---
title: "Ollama 0.35 Decision Model Rehearsal Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "review"
owner: "@buenhyden"
updated: "2026-09-30"
layer: "specs"
artifact_id: "SPEC-0196"
parent_ids:
- "REQ-0009"
created: "2026-09-30"
---

# Ollama 0.35 Decision Model Rehearsal Specification

## Overview

Upgrade the existing local Ollama service from `0.34.2` to `0.35.0` and rehearse the small `tev1:0.8b` decision model against a synthetic classification input. This exercises Ollama's native decision API without adding an application integration or model-routing layer.

## Boundaries and Inputs

In scope: the `ollama` image pin, its derived tech-stack projection, a single-service recreate in the existing `hy-home-infra` project, preservation of the existing model volume, one local synthetic decision-model smoke, and concise operating instructions for that API and recovery boundary.

Out of scope: automatic routing, private inputs, model fine-tuning, removal or replacement of existing models, resource-limit changes, and a browser-level Open WebUI test.

Inputs are REQ-0009, AD-0008, ADR-0008, POL-0056, the upstream [Ollama v0.35.0 release](https://github.com/ollama/ollama/releases/tag/v0.35.0), and the [`tev1` model page](https://ollama.com/library/tev1).

## Behavior Contract

The `ollama` service runs `0.35.0` with its current project, named model volume, GPU request, resource limits, loopback host binding, networks, and gateway labels unchanged. Its two existing models remain available. `tev1:0.8b` is pulled into that volume and answers a short synthetic choice request through Ollama's native decision API. `keep_alive: 0` releases the model after the smoke.

## Technical Approach

Change only the pinned image tag, regenerate the existing image projection, validate the rendered Compose configuration, then recreate only `ollama` with `--no-deps`. Verify the service before pulling `tev1:0.8b`; then verify the decision response, an existing embedding model, exporter reachability, and Open WebUI-to-Ollama backend reachability. Update the existing Guide and Runbook with the bounded synthetic decision request and the version-pin recovery boundary.

## Interfaces and Data

- Existing host API: `127.0.0.1:11434`.
- Existing internal API: `http://ollama:11434` on `ai_net`.
- Decision endpoint: `/v1/systemone` with a synthetic state and one `choice` question.
- No credentials, private prompts, new ports, volumes, networks, or secrets.

## Failure Modes and Guardrails

- Stop if the rendered project changes the model volume, loopback binding, GPU request, resource limits, networks, or gateway labels.
- Stop and restore `ollama/ollama:0.34.2` if `0.35.0` is unhealthy, loses the existing model catalog, or breaks API, exporter, or backend connectivity.
- Do not delete models or the model volume. Keep the decision input synthetic and short to fit the shared 6 GiB GPU.
- Treat returned probability concentration as model output, not proof of correctness or calibrated confidence.

## Acceptance Contract

1. Compose and `infra/tech-stack.versions.json` declare `ollama/ollama:0.35.0`, and scoped static validation passes.
2. The rendered service preserves the existing project, model volume, GPU request, resource limits, loopback port, networks, and gateway labels.
3. The recreated service is healthy, reports `0.35.0`, and still lists `qwen3-embedding:4b` and `qwen3:8b` with their pre-upgrade digests.
4. `tev1:0.8b` is recorded by exact digest and source, and `/v1/systemone` returns a valid `choice` answer over the declared options for the synthetic ticket; probabilities are finite, within `[0,1]`, and sum approximately to one; usage is present; `keep_alive: 0` leaves no loaded model.
5. A synthetic request to the existing embedding model succeeds, exporter metrics and Open WebUI's backend path can reach Ollama, and any unobserved authenticated browser behavior remains explicit.

## Traceability

- REQ-0009-FR-0001: GPU-backed local inference.
- REQ-0009-FR-0002: managed open-source models through Ollama.
- REQ-0009 STORY-03: structured local text analysis.
- AD-0008 and ADR-0008: Ollama local inference architecture.
- POL-0056: model provenance, preservation, rollout, and rollback controls.

## Open Questions

None. Model quality evaluation and automatic routing require a separate task after this bounded compatibility rehearsal.

## Operational Impact

The rollout briefly recreates only `ollama`. Existing clients may see a short API interruption. The named model volume remains mounted; the prior `0.34.2` image is retained as the rollback target.
