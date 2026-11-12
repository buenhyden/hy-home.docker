---
title: "Native OIDC for Open WebUI and the Airflow UI"
version: "0.2.2"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "architecture"
artifact_id: "ADR-0059"
parent_ids:
- "AD-0013"
- "AD-0022"
- "AD-0023"
created: "2026-11-06"
---

# ADR-0059: Native OIDC for Open WebUI and the Airflow UI

## Context

### Problem and Drivers

[ADR-0038](0038-selective-native-oidc-for-native-auth-apps.md) decided that an
application with its own OIDC and authorization does not also get Traefik
ForwardAuth. The implementation applies that to Open WebUI and the Airflow web
UI: `infra/08-ai/open-webui/docker-compose.yml` configures Keycloak OIDC
(`OAUTH_CLIENT_ID: home-openwebui`, PKCE `S256`, signup and account merge off)
and its router uses only `gateway-standard-chain@file`; the Airflow router in
`infra/07-workflow/airflow/docker-compose.yml` also uses only
`gateway-standard-chain@file`. Flower and Ollama keep
`gateway-standard-chain@file,sso-errors@file,sso-auth@file`. The n8n router uses
only `gateway-standard-chain@file` and n8n's own login. Open WebUI keeps
its state in the `open-webui` volume at `/app/backend/data`, and no
`DATABASE_URL` is set.

- ForwardAuth in front of an OIDC application authenticates twice and can
  clash on the `Authorization` header.
- Keycloak stays the single identity provider.
- Services without their own authentication keep ForwardAuth.

### Decision Scope

This decision covers the router authentication of the Open WebUI, Airflow,
Flower, n8n and Ollama endpoints, and the 07-workflow and 08-ai hardening items
listed below. Services without their own authentication keep ForwardAuth.

## Decision

### Chosen Option

1. Open WebUI is the primary AI and RAG interface, with Ollama as its primary
   inference engine. It authenticates users through Keycloak OIDC, and its
   router uses `gateway-standard-chain@file` without `sso-auth`. Signup, account
   merge by email and OAuth role or group management stay off unless a new
   decision enables them.
2. Open WebUI keeps its state in its `open-webui` volume with the application
   default store, on `template-stateful-med`. An external database needs a new
   decision.
3. The Airflow web UI authenticates through the Keycloak Auth Manager (ADR-0038)
   and its router uses `gateway-standard-chain@file` without `sso-auth`.
   Flower keeps `gateway-standard-chain`, `sso-errors` and `sso-auth`. n8n
   uses `gateway-standard-chain` and its own login only: its OIDC is a paid
   feature, and ForwardAuth in front of its login authenticates twice.
4. Ollama keeps `gateway-standard-chain`, `sso-errors` and `sso-auth`, the
   `OLLAMA_NUM_PARALLEL`, `OLLAMA_MAX_LOADED_MODELS` and `OLLAMA_MAX_QUEUE`
   ceilings, a health-gated dependency and a healthy `ollama-exporter`.
5. Airflow and n8n keep Valkey health-based dependencies, with shared
   `mng-valkey` by default and the `dedicated-valkey` profile for a dedicated
   one; n8n keeps worker and task-runner healthchecks and its custom non-root
   image with a secret guard.
6. `check-all-hardening.sh 07-workflow` and `08-ai` with the CI
   `infrastructure-hardening` job guard these items. The DAG quality gate,
   worker autoscale, n8n Git backup and credential integration, model
   promotion, model access separation and conversation log retention proceed
   in phases.

### Authority and Effect

Decided by the owner, @buenhyden; status `accepted`. No separate approval
record is linked. Effective from 2026-11-06. On 2026-11-09 the owner directed
an in-place amendment: n8n leaves ForwardAuth and keeps only its own login.

## Alternatives

### Considered Options

- Keep ForwardAuth on Open WebUI and Airflow as well as their OIDC: rejected;
  double sign-in and header conflicts (ADR-0038).
- Native OIDC only, without ForwardAuth, for every workflow and AI UI:
  rejected; Flower, n8n and Ollama have no Keycloak OIDC of their own here.
- Native OIDC without ForwardAuth for Open WebUI and the Airflow web UI, SSO
  ForwardAuth for the rest: selected.

### Trade-offs

- Negative: the gateway no longer blocks unauthenticated requests to these two
  UIs; the application's login is the only authentication boundary.
- Negative: the concurrency ceilings can limit short-term throughput.

## Consequences

### Impacts

- Positive: one sign-in for Open WebUI and Airflow, and no header conflict.
- Positive: application RBAC (Airflow Keycloak Authorization Services, Open
  WebUI roles) is used as designed.

### Follow-up

On 2026-11-09 the owner directed an in-place amendment: n8n leaves ForwardAuth
and keeps only its own login. The Context and Decision item 3 state this.

Confirm in AD-0013 that the Open WebUI store is the application default in its
volume.

#### Compliance

`scripts/hardening/check-all-hardening.sh` checks the router middleware labels
for 07-workflow and 08-ai. OIDC client secrets are injected as Docker Secrets
(ADR-0038 guardrails).

## Traceability

### Sources

Evidence is the current repository configuration; no runtime state is
claimed.

- [REQ-0013 Open WebUI](../../01.requirements/0013-ai-open-webui.md)
- [AD-0013 Open WebUI architecture](../descriptions/0013-open-webui-architecture.md)
- [AD-0022 Workflow hardening](../descriptions/0022-workflow-optimization-hardening-architecture.md)
- [AD-0023 AI hardening](../descriptions/0023-ai-optimization-hardening-architecture.md)
- [ADR-0007 Airflow and n8n hybrid workflow](0007-airflow-n8n-hybrid-workflow.md)
- [ADR-0008 Ollama and Open WebUI local AI](0008-ollama-openwebui-local-ai.md)
- [ADR-0038 Selective native OIDC](0038-selective-native-oidc-for-native-auth-apps.md)

### Supersession

This record replaces three accepted ADRs, deleted in the same change
(ADR-0051); all three are historical and non-authoritative.

- ADR-0016 chose Open WebUI as the primary AI and RAG interface over LibreChat
  (more complex local RAG) and the Ollama CLI (no RAG, no multi-user history),
  with Ollama as the primary inference engine, SQLite for state, and the
  Traefik SSO middleware for authentication. The interface, Ollama and the
  rejected alternatives carry forward; SSO middleware is replaced by native
  OIDC. The SQLite item carries forward as the application's default store in
  its volume, because no external database is configured.
- ADR-0022 ordered the workflow hardening: the gateway and SSO chain on the
  Airflow and n8n management paths, Valkey health-based dependencies with the
  shared `mng-valkey` boundary (now split by the `dedicated-valkey` profile in
  each single Compose file after SPEC-0156, SPEC-0171 and SPEC-0176), n8n
  worker and task-runner healthchecks, the n8n custom image as the non-root
  default with a secret guard, and the `check-all-hardening.sh 07-workflow`
  gate, with the Airflow DAG quality gate, worker autoscale criteria and n8n Git
  backup and credential integration in phases. Everything carries forward
  except SSO on the Airflow web UI.
- ADR-0023 ordered the AI hardening: the gateway and SSO chain on the Ollama
  and Open WebUI routers, `OLLAMA_NUM_PARALLEL`, `OLLAMA_MAX_LOADED_MODELS` and
  `OLLAMA_MAX_QUEUE` ceilings, Open WebUI on `template-stateful-med`, a
  health-gated `ollama` dependency and an `ollama-exporter` healthcheck, and
  the `check-all-hardening.sh 08-ai` gate, with model promotion, model access
  separation and conversation log retention in phases. Everything carries
  forward except SSO on the Open WebUI router.

Each rejected "everything at once" and "documentation only" alternative in
ADR-0022 and ADR-0023 stays rejected.
