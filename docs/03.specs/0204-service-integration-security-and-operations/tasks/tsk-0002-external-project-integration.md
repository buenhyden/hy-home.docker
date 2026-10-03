---
title: "External Project Integration Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0002"
parent_ids:
- "SPEC-0204"
- "SPEC-0204-PLAN-0001"
created: "2026-10-03"
---

# External Project Integration Task

## Objective

Define and, after approval, implement an infra-owned metadata schema and
validator for external Project-Template-derived applications. Inspect current
ingress, identity, network and telemetry boundaries without changing their
source until a named project and exact follow-up Task exist. Prompt 06 owns
the external application's consumed manifest, source, migrations, Compose
and deployment.

## Inputs

SPEC-0201 external-project field contract; SPEC-0202 dev DB/Valkey roles;
SPEC-0203's bounded Alloy metrics path; current Traefik, Keycloak,
OAuth2 Proxy, OpenBao and project-network declarations. No live project ID,
endpoint, issuer/client, bucket, search authority or host topology has been
approved. The proposed source write scope is limited to new
`infra/09-platform-ops/project-registration/{README.md,schema.json}`,
`scripts/validation/check-project-registration.py`,
`scripts/manifest.yaml`, and
`tests/validation/test_project_registration.py` after Task approval; no
resource provision or service change is authorized by this draft alone.

## Work Log

| Service and source evidence | Writer scope or read-only source | Regression and rollback | Approval boundary |
| --- | --- | --- | --- |
| Traefik has `exposedByDefault: false` and `edge_net`; root declares external project networks with no observed attached service | READ_ONLY: `infra/01-gateway/traefik/config/traefik.yml`, `infra/01-gateway/traefik/docker-compose.yml`, `infra/01-gateway/traefik/dynamic/middleware.yml`, root `docker-compose.yml`; later exact Task owns any project route/network | Synthetic route table rejects unknown host, duplicate name, unsafe POST retry and absent machine auth; direct backend and project A-to-B connections must be denied by a project/service network or backend auth; revert only approved declaration | Project endpoint/network, DNS/firewall, and runtime independently approved |
| Keycloak/OAuth2 Proxy currently implement management browser SSO; project clients are absent | READ_ONLY: `infra/02-auth/keycloak/docker-compose.yml`, `infra/02-auth/oauth2-proxy/docker-compose.yml`, existing GDE/POL-0079; later exact Task owns client ID and secret reference | Issuer/audience/PKCE/redirect/cookie/logout and machine HTML-rejection fixtures; no admin token granted to app; revert client mapping before issuance | Project OIDC creation and secret issuance require exact owner approval |
| OpenBao Agent currently renders management secrets with one sink and output volume | Keep `infra/03-security/openbao/config/agent.hcl` and management policy/output unchanged. A future approved project gets its own AppRole, token sink, policy, output directory/volume and exact-file mounts; manifest carries reference names only | Missing/expired/renewed template and cross-project/management denial tests; revert project-only source | No shared renderer/output, live secret read, rotation or admin-token share |
| Alloy Docker relabel keeps only `hy-home-infra`; SPEC-0203 added bounded quality metrics | READ_ONLY: `infra/06-observability/alloy/config/config.alloy`, `config.home.alloy`, `infra/06-observability/docker-compose.yml`; later exact Task owns approved project identity and receiver changes | Synthetic registered/unregistered/LAB labels, authenticated receiver identity mapped to server labels, spoofed OTLP/trace-attribute denial, metrics/logs/traces preservation and quota; revert allowlist change | Project label allowlist and HOME collector restart separately approved |
| Infra resource metadata has only dev-pg fixture fields today | WRITE AFTER APPROVAL: new `infra/09-platform-ops/project-registration/schema.json` and Korean `README.md`, `scripts/validation/check-project-registration.py`, existing `scripts/manifest.yaml`, new `tests/validation/test_project_registration.py`; existing dev-pg `project.py` remains SPEC-0202-owned, Prompt 06 owns external `integration/infra-consumer.yaml` | Reject missing project_id/environment/ref, unapproved secret reference names, malformed or credential-bearing endpoint, invalid DB/Valkey/S3/OIDC/search scope; run separate secret scan/review; no resource created by metadata alone; revert only these new files | Named project ID, resource quotas and provision/secret operations separate |

The proposed metadata fields are `project_id`, `environment`, `infra_ref`,
`template_ref`, `project_ref`, endpoints by connection location, allowed
networks, DB/role, Valkey ACL prefix, S3 bucket/prefix, OIDC client ID,
search collection and authorization path, telemetry `service.name`,
backup/restore owner, secret reference names, quota, schema/interface version,
and approval/verification state. The schema is closed to unknown fields:
`secret_refs` accepts only reference-shaped IDs matching a documented
bounded pattern and present in a Task-approved name allowlist supplied to the
validator; its default is empty and missing allowlist data fails closed.
Fields such as `password`/`token` are forbidden.
Endpoints are structured scheme/host/port/path values, with userinfo, query,
fragment, interpolation tokens and credential URI forms forbidden. Other
free-form strings are closed or tightly bounded; quota fields are nonnegative
integers subject to later approved ceilings. A separate secret scanner and
human review remain mandatory because schema validity cannot prove that a
string contains no secret. Unknown project IDs, unapproved scopes and
deployment actions remain rejected by their later authorization owner.
Same-daemon Docker DNS is never exported as another-host DNS; cross-Compose
dependencies require bounded retry and operational disconnect handling.

Use the repository's installed `jsonschema` dependency for the bounded
registration validator; its exact failure reasons and valid/invalid synthetic
fixtures belong to `tests/validation/test_project_registration.py`. Register
the new script in `scripts/manifest.yaml` and run the existing script-manifest
check. The validator is called by focused tests and an explicit Task command;
no public gate or project manifest is added without a separate exact scope.
Existing route/auth and secret-reference tests remain read-only evidence.
TSK-0002 is the sole writer of these five paths. Root, Alloy, environment
and Registry service-source edits are excluded until a later exact Task and
project approval; SPEC-0203's merged source is not runtime proof.

## Verification Evidence

| Check | Result | Limit |
| --- | --- | --- |
| Current Traefik, root, Alloy and dev-pg declaration inspection | READ_ONLY | No external project consumer or approved project label found |
| Registration schema/validator synthetic fixtures | NOT_RUN | Await Task approval; route, collector and disconnect runtime remain excluded |
| External project network, OIDC/S3/search/DB provision and HOME restart | NOT_RUN | Named project and separate operation approval absent |

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1/W5 | DRAFT source ledger | This Task and current GDE/POL/RUN owners |
| 4 | W3/W5 | PARTIAL design; no source auth change | POL-0079, GDE/POL/RUN-0085 |
| 5 | W3/W5 | NOT_RUN | Infra registration schema/validator; Prompt 06 external manifest remains separate |
| 8 | W5 | NOT_RUN | This Task verification receipts |

## Review Evidence

Independent route, identity and security review is pending a bounded source
diff. Existing ForwardAuth exceptions and socket access remain risks; source
inspection alone is not an authorization test.

## Commit Ledger

No Prompt 04 commit. Baseline only: `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`.

## Rulings

No blanket `exposedByDefault`, full-Docker discovery, shared admin client,
management superuser, shared OpenBao renderer, unauthenticated OTLP producer,
fake collection RBAC or root include of app source.
A manifest is metadata until a separate operation provisions a resource.

## Deferred Items

Project ID, endpoint topology, real audience/client, network, bucket, search
permission, secret names and quotas; HOME collector/gateway changes and all
project deployment/credentials remain separately gated.
