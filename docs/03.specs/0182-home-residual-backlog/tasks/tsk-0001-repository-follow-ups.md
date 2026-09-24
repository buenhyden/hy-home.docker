---
title: "Repository Follow-ups"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-25"
layer: "specs"
artifact_id: "SPEC-0182-TSK-0001"
parent_ids:
- "SPEC-0182"
- "SPEC-0182-PLAN-0001"
created: "2026-09-25"
---

# Repository Follow-ups

## Objective

Carry out W1 and W2 of the [Plan](../plan.md): six repository changes with
focused tests, then their live applies.

## Inputs

Read-only investigation of 2026-09-25 against main `64497555c`:

- **Qdrant:** `qdrant` exports only `QDRANT__SERVICE__API_KEY` from AI-008
  (`infra/04-data/specialized/qdrant/docker-compose.yml:48-57`); Prometheus
  sends the same key (`prometheus.yml:143`, `prometheus.dev.yml:98`, grant in
  `infra/06-observability/docker-compose.yml:83`). `gen-secrets.sh` generates
  an `O` registry row without a script change. `QdrantApiKeyContractTests`
  (`tests/validation/test_compose_baseline_gates.py:3553`) asserts the full-key
  path today.
- **Open WebUI:** `VECTOR_DB_URL` at `infra/08-ai/open-webui/docker-compose.yml:28`
  without `VECTOR_DB`; Open WebUI ignores it and keeps its local store. The
  Qdrant guide already says so (`0034-qdrant/guide.md:91`); the RAG guide
  (`0059-rag-workflow/guide.md:20,49`), Open WebUI README (`:55,124`), guide
  (`:40,51,100`) and policy (`:37`) claim Qdrant storage; the RAG guide also
  names the wrong embedding model size.
- **n8n:** the queue uses `mng-valkey` correctly; only the Valkey exporter
  targets `mng-n8n-valkey` (`infra/07-workflow/n8n/docker-compose.yml:289`)
  instead of `n8n-valkey`, with no port default. Not running (profile
  `dedicated-valkey`).
- **SeaweedFS:** no `-metricsPort` on any component; master, volume and filer
  sit only on the internal `seaweed_internal`; S3 is on `edge_net`, which
  Prometheus shares. Scraping the internals would expose unauthenticated
  master endpoints, so only S3 is scraped.
- **Runtime-version check:** `_RUNTIME_PATCH` in
  `scripts/lib/document_governance/metadata/heading.py:824` matches any
  `x.y.z`; the prose branch of `_runtime_literal_line` (`:1022-1073`) flags
  SMTP codes (`5.7.1`) and section numbers (`5.4.3`). Model test:
  `test_calendar_dates_are_not_runtime_patch_literals`
  (`tests/lib/document_governance/metadata/test_heading.py:1185`).
- **compose-core-readiness:** its `.env.example` (409 lines, `INFRA_*` keys)
  is referenced by nothing; the harness uses only `env.runtime.example` and
  the override, whose Vault rig is woven through about 200 harness lines.
- **Renovate units:** already regular copies identical to the repository
  (W12 closure).

## Work Log

Pending.

## Verification Evidence

Pending.

## Review Evidence

Pending.

## Commit Ledger

No PR yet.

## Rulings

See the Plan.

## Deferred Items

None yet.
