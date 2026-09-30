---
title: "Ollama 0.35 Upgrade and Decision Model Smoke"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-09-30"
layer: "specs"
artifact_id: "SPEC-0196-TSK-0001"
parent_ids:
- "SPEC-0196"
- "SPEC-0196-PLAN-0001"
created: "2026-09-30"
---

# Ollama 0.35 Upgrade and Decision Model Smoke

## Objective

Execute W1 through W6 of the [Plan](../plan.md) and retain exact results for the acceptance criteria of [SPEC-0196](../spec.md).

## Inputs

- Existing Compose source: `infra/08-ai/ollama/docker-compose.yml`.
- Existing project: `hy-home-infra`; service: `ollama`; host API: `127.0.0.1:11434`.
- Existing named volume: `hy-home-infra_ollama-data` mounted read/write at `/root/.ollama`.
- Upstream sources: Ollama v0.35.0 release and `tev1` model page linked by the Spec.

## Work Log

- 2026-09-30 W1 baseline: `ollama` was healthy on version `0.34.2`, image ID and repo digest `sha256:da6e0dc5651df159e45686fd663c4dbe1624a52c44d7280eeac1551d8f865532`. The project and volume matched the Inputs; the host binding was `127.0.0.1:11434`; one NVIDIA GPU request was present.
- 2026-09-30 W1 model catalog: `qwen3-embedding:4b` digest `df5bd2e3c74cd8d069d21dc038f1b359fcdc9458fce1c99bd43c9eb1518ff907` (2.5 GB) and `qwen3:8b` digest `500a1f067a9f782620b40bee6f7b0c89e17ae61f686b92c24933e4ca4b2b8b41` (5.2 GB).
- 2026-09-30 W1 GPU: NVIDIA GeForce GTX 1060 6GB, driver `580.178.04`, 6144 MiB total and 5996 MiB free before the rollout.
- 2026-09-30 W2: image pin changed from `0.34.2` to `0.35.0`; the existing tech-stack projection was regenerated.
- 2026-09-30 W3: projection check, Compose quiet render, the named `ollama` profile validation (two services), `git diff --check`, and document metadata all passed. The generic infra static helper reported zero failures but six blocked records because its isolated input graph and optional YAML/shell tools were unavailable; the registered direct Compose checks supplied the required render evidence.
- 2026-09-30 W4: official image digest `sha256:2a6e883b917fc543389599dae79918f5cac9e1438890506982f44aa4f5625d01` was pulled. `docker compose --profile ollama up -d --no-deps --force-recreate ollama` recreated only `ollama`; it became healthy and reported `0.35.0`. The project, named volume, loopback binding, GPU request, four-CPU/eight-GiB limits, `ai_net`/`edge_net`, Traefik and SSO labels, and both existing model digests matched the baseline. Exporter metrics and Open WebUI's backend `/api/tags` path succeeded.
- 2026-09-30 W5: `tev1:0.8b` was pulled from the official Ollama library with digest `d45e875d63fed9465390a4eb9e55f51f470390a446667b55d0a075a15e0336bf` and size 811,856,202 bytes. The synthetic checkout-error choice returned HTTP 200 in 3.385482 seconds with `choice=bug`, choice probability `0.977011841`, probability sum `1.0`, and usage 136 input/1 output token. All response schema and finite-range assertions passed. `/api/ps` was empty after `keep_alive: 0`.
- 2026-09-30 W5 compatibility: `qwen3-embedding:4b` returned one finite 2,560-dimensional embedding in 51.564579 seconds and unloaded; the final catalog retained both pre-upgrade model digests. Authenticated browser UI behavior was not observed.
- 2026-09-30 W6 documentation handoff: the existing Ollama Guide records the bounded `/v1/systemone` synthetic `tev1:0.8b` request, response interpretation, `keep_alive: 0`, and 6 GiB model-selection limit. The Runbook records the Compose image pin as the version source of truth plus scoped recreate and non-destructive rollback boundaries; neither rollback nor authenticated browser UI was executed.

## Verification Evidence

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W2 | PASS: Compose and projection use `0.35.0`; scoped static validation passed | [version projection](../../../../infra/tech-stack.versions.json) |
| 1 | W3 | PASS: quiet render, scoped two-service validation, diff check, metadata, and `python3 scripts/validation/run-ci-gate.py --profile changed` on 2026-09-30 passed | [Ollama Compose](../../../../infra/08-ai/ollama/docker-compose.yml) |
| 1 | W6 | PASS: the bounded API and recovery guidance was recorded | [Guide](../../../05.operations/guides/0056-ollama.md) |
| 2 | W1 | PASS: baseline recorded project, volume, GPU, resources, loopback port, networks, gateway and SSO labels | [Ollama Compose](../../../../infra/08-ai/ollama/docker-compose.yml) |
| 2 | W3 | PASS: rendered boundaries matched the baseline | [Ollama Compose](../../../../infra/08-ai/ollama/docker-compose.yml) |
| 2 | W4 | PASS: post-recreate boundaries matched the baseline | [Ollama Compose](../../../../infra/08-ai/ollama/docker-compose.yml) |
| 3 | W1 | PASS: baseline model names and exact digests recorded | [Task work log](#work-log) |
| 3 | W4 | PASS: healthy `0.35.0`; both existing model names and exact digests preserved | [Task work log](#work-log) |
| 4 | W5 | PASS: `tev1:0.8b` exact digest recorded; choice schema/probabilities/usage passed; `bug` at 0.977011841; `/api/ps` empty after `keep_alive: 0` | [Task work log](#work-log) |
| 5 | W5 | PASS: browser limit retained; existing 2,560-dimensional embedding, exporter metrics, and Open WebUI backend path passed; authenticated browser UI was NOT_RUN | [Ollama runbook](../../../05.operations/runbooks/0056-ollama.md) |

## Review Evidence

Independent IaC review returned CLEAR for the pin/projection diff and runtime plan after independently confirming projection check, Compose render, diff check, metadata, preserved boundaries, isolated recreate, and rollback. On 2026-09-30, final independent outcome review returned CLEAR: the Task evidence consistently proves the healthy upgrade, preserved boundaries and existing models, exact `tev1` provenance, decision and embedding checks, unload behavior, and backend connectivity without inflating the NOT_RUN rollback or browser UI checks.

## Commit Ledger

2026-09-30: the user authorized commit, push, PR merge, `main`/`origin/main` alignment, and cleanup. Initial draft commit: `ba448b1a7`; review/approved/ready transition commit: `c4aa1ae59`; Spec approval transition commit: `eba7243d1`; activation/in-progress transition commit: `29ad5ceac`; Git history remains the resulting completion evidence.

## Rulings

- 2026-09-30: The user's request authorizes the scoped Ollama recreate, model pull, and synthetic local inference. No additional service or routing integration is authorized.

## Deferred Items

- Rollback was NOT_RUN because rollout and compatibility checks passed; the `0.34.2` image remains the recorded recovery target.

- Authenticated Open WebUI browser behavior was NOT_RUN; W5 verified the existing backend container-to-Ollama path.
- Model quality, calibration, prompt design, and automatic routing remain outside SPEC-0196.
