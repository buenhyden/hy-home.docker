---
title: "Gateway Authentication and Security Documentation"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "specs"
artifact_id: "SPEC-0198-TSK-0003"
parent_ids:
- "SPEC-0198"
- "SPEC-0198-PLAN-0001"
created: "2026-10-01"
---

# Gateway Authentication and Security Documentation

## Objective

Implement W3 of [SPEC-0198](../spec.md) and its [Plan](../plan.md), preserving
18 existing role leaves and covering all eight named Compose service identities.

## Inputs

The user approved the Plan and tier-scoped agent implementation with independent
review on 2026-10-01. Worktree: `/home/hyunyoun/.codex/worktrees/infra-tier-layout/hy-home.docker`;
branch `codex/infra-tier-layout`; base `c26bc8026254dffd7d51fc45b4081a1f80f855f2`.
Reviewed uncommitted SPEC-0197 and independently CLEAR W1/W2 are dependencies.
Exclusive writer: `/root/ops_w3_gateway_auth_security`, exact W3 paths in W1
plus this Task. Other documents, infra, scripts, registry, index, secret values,
private environment, runtime actions, builds, staging and commits are excluded.
Bootstrap/provider, doc-writer, ops-runbook-agent and role templates were read.
No new executable stateful restore is authorized: existing recovery limitations
remain and any concrete recovery needs independent stateful-contract review.

## Work Log

Before edits, all 18 role bodies and the five implementation packages were read,
including OAuth2 Proxy default/alternate Dockerfiles and their copied entrypoints.
Findings: misplaced mandatory policy bullets; duplicate gateway recovery;
Traefik required limiter missing from consumed chain; Nginx HTTP health redirect
and placeholder before access handlers; missing helper coverage; incorrect
blanket token forwarding and 401/403 wording; missing startup edges and source
versus runtime/build distinction; OpenBao stale platform-policy scope, custody
exception ownership, metrics mode contradiction and legacy Vault wording.
These are source findings, not observed running incidents. Existing security
controls stay mandatory. Independent security review and final semantic/rules
review remain separate from documentary correction.

### Declared versions and official evidence

All sources below were inspected/fetched on 2026-10-01. Tags are mutable unless
an immutable digest is declared; none of these eight service declarations supplies
one. No installed version, image bytes, private override or live endpoint was
observed. Exact version strings here are dated audit evidence, not a second pin
owner. Official current pages were not substituted for unavailable tagged pages.

| Evidence key / named service | Source declaration and inspected behavior | Version-matched official evidence and certainty |
| --- | --- | --- |
| N / `nginx` | `infra/01-gateway/nginx/docker-compose.yml`, config/nginx.conf, README; image `nginx:alpine`; no build. Config has fixed listeners80/443, HTTP return301, HTTPS ping200, placeholder return200, three single-node upstreams. | [rewrite return](https://nginx.org/en/docs/http/ngx_http_rewrite_module.html#return), [request phases](https://nginx.org/en/docs/dev/development_guide.html): phase semantics only. Mutable channel has no exact release to match; current runtime/module/CA/health behavior UNVERIFIED. |
| T / `traefik` | `infra/01-gateway/traefik/docker-compose.yml`, config/traefik.yml, dynamic/middleware.yml, dynamic/tls.yaml, package/config/dynamic README routing; image `traefik:v3.7.13`; no build. | [v3.7 Chain](https://doc.traefik.io/traefik/v3.7/reference/routing-configuration/http/middlewares/chain/), [Errors](https://doc.traefik.io/traefik/v3.7/reference/routing-configuration/http/middlewares/errorpages/#statusrewrites), [ForwardAuth](https://doc.traefik.io/traefik/v3.7/reference/routing-configuration/http/middlewares/forwardauth/). Matched minor line, tag not runtime proof. |
| K / `keycloak` | `infra/02-auth/keycloak/docker-compose.yml` and README; `quay.io/keycloak/keycloak:26.7.4-0`; image-only, shell Secret injection then kc.sh start. Adjacent Dockerfile read but NOT selected: builder kc.sh build plus demonstration keystore, copied optimized tree; no claim either is active. | [26.7.4 release](https://github.com/keycloak/keycloak/releases/tag/26.7.4), tagged [health](https://raw.githubusercontent.com/keycloak/keycloak/26.7.4/docs/guides/observability/health.adoc), [reverse proxy](https://raw.githubusercontent.com/keycloak/keycloak/26.7.4/docs/guides/server/reverseproxy.adoc), [import/export](https://raw.githubusercontent.com/keycloak/keycloak/26.7.4/docs/guides/server/importExport.adoc). Product tag matched; packaging suffix/image and runtime UNVERIFIED. |
| O / `oauth2-proxy` | `infra/02-auth/oauth2-proxy/docker-compose.yml`, both Dockerfiles and both copied entrypoints, config/oauth2-proxy.cfg, README. Effective default context `.`, dockerfile `${OAUTH2_PROXY_DOCKERFILE:-dev.Dockerfile}`, no args/target; binary FROM `quay.io/oauth2-proxy/oauth2-proxy:v7.15.4`, final FROM `alpine:3.24.2`. | [v7.15.4 release](https://github.com/oauth2-proxy/oauth2-proxy/releases/tag/v7.15.4), tagged [endpoints](https://raw.githubusercontent.com/oauth2-proxy/oauth2-proxy/v7.15.4/docs/docs/features/endpoints.md), [Keycloak provider](https://raw.githubusercontent.com/oauth2-proxy/oauth2-proxy/v7.15.4/docs/docs/configuration/providers/keycloak_oidc.md), [Redis source](https://raw.githubusercontent.com/oauth2-proxy/oauth2-proxy/v7.15.4/pkg/sessions/redis/redis_store.go). Versioned website/session-storage raw URLs unavailable (404); used tagged source, did not claim a successful historical-doc fetch. |
| V / `oauth2-proxy-valkey` | Same OAuth2 Compose; image `valkey/valkey:9.1.2-alpine`; no build; requirepass, appendonly yes, fixed6379, UID999, bind-backed data. | [9.1.2 release](https://github.com/valkey-io/valkey/releases/tag/9.1.2), [tagged valkey.conf](https://raw.githubusercontent.com/valkey-io/valkey/9.1.2/valkey.conf) persistence configuration. AOF is persistence, not rehearsal/backup/HA. |
| E / `oauth2-proxy-valkey-exporter` | Same OAuth2 Compose; `oliver006/redis_exporter:v1.91.1-alpine`; no build; /bin/sh wrapper exports password then passes `-redis.password`, target dedicated Valkey, configured listen port, healthy dependency, no own healthcheck/volume. | [v1.91.1 release](https://github.com/oliver006/redis_exporter/releases/tag/v1.91.1), [tagged README](https://raw.githubusercontent.com/oliver006/redis_exporter/v1.91.1/README.md): credential arguments, metrics, Alpine shell. Source command support only; exporter scrape/runtime UNVERIFIED. |
| B / `openbao` | `infra/03-security/openbao/docker-compose.yml`, all five config/policies/*.hcl, README; image `openbao/openbao:2.6.2`; no build; server command and BAO_LOCAL_CONFIG single-node Raft/HTTP/telemetry. | [2.6.2 section](https://openbao.org/community/release-notes/2-6-0/#v262), [2.6 status](https://openbao.org/docs/2.6.x/commands/status/), [unauthenticated root deprecation](https://openbao.org/community/deprecation/unauthed-generate-root/). The attempted separate2-6-2 page failed; actual2.6.x page contains2.6.2. Installed policy/role/image unobserved. |
| A / `openbao-agent` | Same Compose/image; config/agent.hcl and all ten template bodies inspected. Only keycloak_admin_password.ctmpl and grafana_admin_password.ctmpl selected; no extra package/build. Agent command and VAULT_ADDR override,0600 sink/two outputs, consume-on-read SecretID. | [2.6 AppRole auto-auth](https://openbao.org/docs/2.6.x/agent-and-proxy/autoauth/methods/approle/), same2.6.2 release above. Cached credentials and consumed file do not prove a valid login; runtime renew/render NOT_RUN. |

OAuth2 default Dockerfile installs no packages; it copies only the upstream binary
and dev entrypoint (0555), creates a nonroot oauth2proxy user/group, and has no CMD.
Compose does not override command/entrypoint; the copied script supplies
`--config /etc/oauth2-proxy.cfg` when no args exist, strips CR/LF from management
Valkey Secret, preserves an existing REDIS_PASSWORD override, then execs the binary.
The alternative `Dockerfile` copies docker-entrypoint.sh, fixes UID100/GID101 and
reads the dedicated Valkey Secret; all FROM/COPY/USER/ENTRYPOINT bodies were read.
No private Dockerfile selector was read, so the real deployed alternative is unknown.
The config and CA bind mounts override runtime files, not the copied entrypoint.

Transferred Airflow client provisioning was additionally checked against
`infra/07-workflow/airflow/docker-compose.yml` common build args and Dockerfile:
Compose selects base3.3.1, constraints filename Python3.13 and Keycloak provider0.9.0;
args override direct-build fallback3.3.2. The Python argument does not prove the
base interpreter. No COPY/ENTRYPOINT/CMD is locally added. Exact provider
[permissions](https://raw.githubusercontent.com/apache/airflow/providers-keycloak/0.9.0/providers/keycloak/docs/auth-manager/manage/permissions.rst)
and [CLI definition](https://raw.githubusercontent.com/apache/airflow/providers-keycloak/0.9.0/providers/keycloak/src/airflow/providers/keycloak/cli/definition.py)
confirm create-all/create-permissions, optional secure password prompt and no
automatic user-role assignment. Full Airflow identity audit remains W5.

### Service-by-topic evidence matrix

Topic numbers correspond exactly to the Spec's nine required groups. Every row
inherits its named evidence key's exact implementation path, declared version,
official URL/release and runtime uncertainty above. `G/P/R` mean that subject's
Guide/Policy/Runbook, resolved by the exact artifact table below. `source` is the
specific implementation section inspected; old-to-final section mappings below
preserve the original complete bodies. All rows received manual source comparison;
at this author checkpoint independent semantic/policy disposition was PENDING;
the final independent receipt below records acceptance. Shared policy links do not erase the local exceptions stated here.

| Service / evidence | Topic | Source section | Original owner/section and finding | Resolution, final owner/section and applicability |
| --- | --- | --- | --- | --- |
| `nginx` / N | 1 | profiles / README | 0011 G Overview: consistent | Retain OPTIONAL path gateway; G Source, activation and route limits explains placeholder and single-upstream limits. |
| `nginx` / N | 2 | image / depends_on / config listeners | 0011 G Prerequisites: incomplete | G Source, activation and route limits records mutable tag, nginx-only selector, healthy S3 edge but additional auth DNS dependencies; no exact release/runtime proof. |
| `nginx` / N | 3 | ports / locations / auth_request / return | 0011 G Purpose; R Verification: contradictory | G route table and R Acceptance distinguish HTTP301/HTTPS200, placeholder-before-auth, read-only CDN and unverified Keycloak prefix; P limitations preserve controls. |
| `nginx` / N | 4 | volumes / tmpfs / port variables | 0011 G Prerequisites: incomplete | G Configuration, state and signals names cert/config inputs, fixed internal ports and disposable cache/log/PID; P Shared controls governs private custody. |
| `nginx` / N | 5 | extends / worker / cache / logs | 0011 G Common Checks: incomplete | G Configuration, state and signals supplies low budget, tmpfs logs, no metrics exporter, cache budget warning; P resource review triggers. |
| `nginx` / N | 6 | policy versus auth phase | 0011 P Controls: contradictory placement | P Required now owns mandatory checks/incident triggers; no weakened auth rule; timeout exception retained with owner/risk/closure. |
| `nginx` / N | 7 | root include / profiles / mount | 0011 R Steps: incomplete | R Startup, shutdown and configuration change gives exact existing-image target operations and POL0006 recreation/hash; no implicit Traefik selection. |
| `nginx` / N | 8 | health / lint / special paths | 0011 R Steps/Verification: incomplete | R Static checks and diagnosis + Acceptance require actual dependency/TLS/auth results and stop on mismatch; @buenhyden escalation. |
| `nginx` / N | 9 | config / cert / tmpfs | 0011 G recovery + R two recovery sections: duplicate | R Rollback or Recovery owns consolidated config/cert/image canary, no tmpfs backup; unavailable isolated acceptance remains NOT_RUN; deletion approval preserved. |
| `traefik` / T | 1 | profiles / README | 0013 G Overview: consistent | G Source, activation and middleware behavior retains HOME, actual selectors and alternative-listener boundary. |
| `traefik` / T | 2 | image / networks / providers | 0013 G Prerequisites: incomplete | G source section names no startup edges and real auth/app dependencies, bind/port inputs, declaration versus runtime. |
| `traefik` / T | 3 | middlewares / labels / secrets | 0013 G Steps and P Controls: contradictory | G/P preserve required limiter but identify missing chain membership; authResponseHeaders identity-only,401→302 and403 preserved; BasicAuth and socket boundary retained. |
| `traefik` / T | 4 | volumes / command / dynamic watch | 0013 G Prerequisites: incomplete | G Configuration, state and signals names config/cert/secret references, fixed edge address and watch versus single-file recreate; no ACME state. |
| `traefik` / T | 5 | extends / ping / metrics / tracing / logs | 0013 G Common Checks: incomplete | G signals gives medium limits, internal8082 metrics/ping and OTLP target; P review triggers; no auth assurance from health. |
| `traefik` / T | 6 | policy / chain source | 0013 P Controls/Exceptions: contradictory placement | Move mandatory bullets to Required, preserve limiter/retry/breaker thresholds and emergency exception with accountable owner; source defect remains. |
| `traefik` / T | 7 | root context / mounts | 0013 R Checklist/Steps: incomplete | R Startup, shutdown and apply states side effects, local-image prerequisite, bounded target commands and common post-apply validation. |
| `traefik` / T | 8 | BasicAuth / Errors / health | 0013 R Steps: incomplete | R symptom table distinguishes dashboard401, group403, route/CA,429 and health; stop/escalate rather than removing auth. |
| `traefik` / T | 9 | config/cert / no ACME | 0013 G recovery + R duplicate recovery: duplicate | R Rollback or Recovery consolidates reviewed config and private cert pairing, canary/upgrade identity, cleanup limits, and unexecuted historical recovery. |
| `keycloak` / K | 1 | README / profiles | 0014 G Overview: incomplete | G Implementation, readiness and resources retains HOME and native/proxy distinctions; historical OpenBao login is not all-client acceptance. |
| `keycloak` / K | 2 | image / entrypoint / DB env | 0014 G Steps: incomplete | G explains image-only selection, inactive local Dockerfile, shell Secret injection, no DB depends_on and no realm init/import job. |
| `keycloak` / K | 3 | labels / KC_HOSTNAME / proxy headers | 0014 G Tracked Configuration/OIDC: consistent | Retain exact issuer/client/callback distinctions and management-port isolation; R diagnoses CA/redirect and separates session/token revocation. |
| `keycloak` / K | 4 | volumes / environment / secrets | 0014 G Prerequisites: incomplete | G names required variables plus read-only conf/providers/themes and private backup pairing; port-reference variables do not change KC listeners. |
| `keycloak` / K | 5 | template high / pool / metrics / tracing | 0014 G Common Checks: incomplete | G adds2CPU/2GiB, pool10, declared histograms/events/OTLP, not observed telemetry; R bash management check and status whitespace clarified. |
| `keycloak` / K | 6 | policy Controls / shared governance | 0014 P Controls: contradictory placement | Move required checks/incident triggers; retain offline export, matching DB rollback, owner approval, common retention/resource/deletion controls. |
| `keycloak` / K | 7 | entrypoint / mounts / image | 0014 R Steps: incomplete | R Lifecycle provides existing-image startup/stop/recreate, bootstrap-not-rotation distinction and blocked unprovisioned restore. Airflow client commands moved into R Application authorization provisioning with tagged CLI evidence. |
| `keycloak` / K | 8 | health / DB / OIDC | 0014 R Steps: consistent but unsafe evidence shorthand | Keep nine symptom/revocation branches; replace raw-log collection with sanitized summaries, source-aware health, concrete owner and approval boundary. |
| `keycloak` / K | 9 | external DB and files | 0014 G recovery and R recovery: duplicate/incomplete | G links R; R requires DB backup plus matching image and customization, isolated contract before restore, no in-place schema downgrade, finite token/client rotation boundary retained. |
| `oauth2-proxy` / O | 1 | profiles / config static upstream | 0015 G Overview: consistent | Retain HOME ForwardAuth, static://200 and native RBAC separation; helper classes separately named. |
| `oauth2-proxy` / O | 2 | build / scripts / profiles / no depends_on | 0015 G Prerequisites/Steps: incomplete | G Build selection and effective startup traces exact default/alternate FROM,COPY,USER,ENTRYPOINT, no args/target/packages, config fallback and credential precedence; no profile-driven build switch. |
| `oauth2-proxy` / O | 3 | config / labels / Traefik authResponseHeaders | 0015 G Cookie, Token, and Session: contradictory | Correct token production versus gateway identity-only forwarding; retain PKCE,/admins,cookie policy,issuer/callback/CA, sign_out-versus-provider logout. |
| `oauth2-proxy` / O | 4 | mounts / Secret files / Redis URL | 0015 G Tracked Configuration: incomplete | G Services, inputs and persistence names shared/dedicated selector inputs, required CA and client/cookie secrets, external sessions and fixed listeners. |
| `oauth2-proxy` / O | 5 | template medium / health / metrics | 0015 G Common Checks: incomplete | G/R distinguish ping from ready, internal44180 metrics, limits and sanitized diagnostics; authenticated session outage remains historically untested. |
| `oauth2-proxy` / O | 6 | Policy / fail closed | 0015 P Controls/Exceptions: contradictory placement | Required bullets restored; approval/expiry/rollback required for degraded mode; R explicitly says no implemented automatic fail-open command. |
| `oauth2-proxy` / O | 7 | build source / mounts | 0015 R Steps: incomplete | R Lifecycle covers local-image target start/stop, no implicit build/pull, recreate/hash on file change and approved rebuild route. |
| `oauth2-proxy` / O | 8 | OIDC / Redis / cookie / endpoints | 0015 R Steps: consistent | Keep issuer/CA/PKCE/state/session/logout/readonly cases, sanitized failures, actual backend selectors and concrete escalation. |
| `oauth2-proxy` / O | 9 | external session store | 0015 G recovery + R recovery: duplicate | R owns reauthentication after loss, cookie/client/Valkey rotation distinctions, prior image/endpoint and cleanup limits; no stale-session restore. |
| `oauth2-proxy-valkey` / V | 1 | dedicated-valkey profile | 0015 G helper mention: incomplete | G Services table explicitly OPTIONAL session store; profile only adds service and does not switch Proxy. |
| `oauth2-proxy-valkey` / V | 2 | image / command / user / no depends_on | 0015 G Prerequisites: incomplete | G names image authority, UID999, server6379, AOF/password; R requires readiness before exporter/Proxy switch. |
| `oauth2-proxy-valkey` / V | 3 | networks / expose / requirepass | 0015 G table absent: missing | G/P require private mng_data_net password-auth boundary, no host route; fixed server port versus VALKEY_PORT probe mismatch risk explicit. |
| `oauth2-proxy-valkey` / V | 4 | volume / password Secret | 0015 G persistence absent: missing | G names DEFAULT_AUTH_DIR/valkey bind data and shared-versus-dedicated credential; P retention/invalidation and safe evidence apply. |
| `oauth2-proxy-valkey` / V | 5 | template low / AOF / health | 0015 G signals absent: missing | G records0.5CPU/256MiB, PONG health, no maxmemory declaration, AOF disk/OOM pressure; session recovery not implied. |
| `oauth2-proxy-valkey` / V | 6 | argv / P0006 | 0015 P helper scope missing | P Helper and session boundaries applies same access/resource/removal controls and bans full argv/health/inspect evidence; no plaintext value inspected. |
| `oauth2-proxy-valkey` / V | 7 | startup / binding | 0015 R helper commands missing | R Lifecycle helpers starts store first with existing image/input, waits healthy, then exporter; explicit backend/image/credential agreement before switch. |
| `oauth2-proxy-valkey` / V | 8 | PONG / readiness | 0015 R helper diagnosis missing | R stops on unhealthy store, uses Proxy ready and fresh login; never flush/restart shared mng-valkey for isolated Proxy incident. |
| `oauth2-proxy-valkey` / V | 9 | AOF session contents | 0015 R backup/cleanup missing | AOF not authoritative business backup; R re-login/invalidation plan, no FLUSHALL/down-v, separate volume deletion approval. |
| `oauth2-proxy-valkey-exporter` / E | 1 | profile / target | 0015 G implementation one line: incomplete | G Services table identifies OPTIONAL dedicated-store exporter; no business/state ownership. |
| `oauth2-proxy-valkey-exporter` / E | 2 | image / wrapper / depends_on | 0015 G startup absent: missing | G names healthy dedicated Valkey dependency, image-only shell wrapper and no build; R starts after store healthy. |
| `oauth2-proxy-valkey-exporter` / E | 3 | networks / flags / secrets | 0015 G access absent: missing | G/P internal mng_data_net+obs_net endpoint only; password command argument exposure limit is explicit and escalated for separate review. |
| `oauth2-proxy-valkey-exporter` / E | 4 | listen flag / no volumes | 0015 G inputs absent: missing | G requires VALKEY_EXPORTER_PORT (command lacks fallback), same dedicated Secret, no persistent data or own certificate/bootstrap. |
| `oauth2-proxy-valkey-exporter` / E | 5 | template low / absent health | 0015 G health absent: missing | G separates process state, scrape target UP and redis_up; P keeps common health requirement and records missing healthcheck as implementation limitation, not approved exemption. |
| `oauth2-proxy-valkey-exporter` / E | 6 | P0006 / P0015 | 0015 P scope only Proxy: incomplete | P Helper and session boundaries applies ownership/approvals/review/removal; no public metrics or implied compliance. |
| `oauth2-proxy-valkey-exporter` / E | 7 | startup / stateless image | 0015 R lifecycle absent: missing | R exact service target start, store prerequisite, exporter-first shutdown and source-based recreate; no implicit build. |
| `oauth2-proxy-valkey-exporter` / E | 8 | scrape versus backend | 0015 R diagnostics absent: missing | R observes exporter state and authorized collector signals separately; missing health cannot be reported PASS; no raw password-bearing output. |
| `oauth2-proxy-valkey-exporter` / E | 9 | no volume / shared credential | 0015 R recovery absent: missing | Stateless re-creation, no backup/restore or credential issuance capability; shared dedicated password rotation belongs to paired store/proxy owner, deletion has no exporter data volume. |
| `openbao` / B | 1 | README / profiles | 0085 G Usage: contradictory stale Vault | G/P remove current Vault migration claim in favor of dated retirement; HOME secret authority and all five selectors explicit. |
| `openbao` / B | 2 | image / server / BAO_LOCAL_CONFIG | 0085 G Usage: incomplete | G Service behavior describes image-only single-node Raft server, internal HTTP/TLS gateway, manual init/unseal and no HA claim. |
| `openbao` / B | 3 | OIDC/AppRole/Kubernetes ACL source | 0085 G operator / P ESO summaries: incomplete/contradictory | G names actual operator exact paths/capabilities; P reconciles exactly five ESO data/metadata reads using later explicit owner-authored commit and completed Task provenance; no wildcards or new grant; source ACL not deployed proof. |
| `openbao` / B | 4 | Raft volume / env / custody | 0085 G Usage: incomplete | G maps Raft/agent/out inputs, port variables and protected identity/custody; existing single-file exception moves to P with missing expiry/exit explicitly unresolved. |
| `openbao` / B | 5 | status / telemetry / limits | 0085 G checks: incomplete | G/R explain exit0/2, sealed-health limitation, medium budget, disk/OOM and authenticated sys/metrics; no current live proof. |
| `openbao` / B | 6 | Policy / existing dated exception | 0085 P controls: incomplete | P preserves nonroot human use, root emergency limits, exact renderer scopes, unauthenticated-root prohibition; prior custody decision kept without new approval or invented closure. |
| `openbao` / B | 7 | server lifecycle / bind / unseal | 0085 R generic Procedure: incomplete | R Lifecycle names target start/stop, manual initialization, mount identity stops, unseal prerequisite and separate upgrade/recovery contracts. |
| `openbao` / B | 8 | status / auth / metrics / root API | 0085 R detailed procedures: consistent plus contradiction | Preserve bootstrap/OIDC/root-recovery/Kubernetes handling; fix circular before-revoke condition and metrics consumer0640 versus temporary0600 wording; escalate authorization gaps. |
| `openbao` / B | 9 | Raft snapshot / credential custody | 0085 R recovery: consistent planned limitation | Retain isolated snapshot plan, restored token recheck, no in-place downgrade/reinit, no executed rehearsal; common retention applies; last viable admin access preserved until replacement verified. |
| `openbao-agent` / A | 1 | profiles / template purpose | 0085 G Usage: incomplete | G explicitly HOME renderer, only two selected admin-password outputs, no automatic Docker Secret replacement. |
| `openbao-agent` / A | 2 | image / command / depends_on / VAULT_ADDR | 0085 G Usage: incomplete | G traces agent command/config and override, healthy-server edge permits sealed server; manual AppRole bootstrap required. |
| `openbao-agent` / A | 3 | secrets_net / AppRole policy | 0085 G credential table: consistent | Retain machine credentials distinct from human/root and two read-only KV paths; unused mounted templates grant no access. |
| `openbao-agent` / A | 4 | agent data/output / templates | 0085 G mounts: incomplete | G maps bind-backed agent/out,0600 token and outputs; all ten templates inspected, only two active; retained bootstrap versus regenerated outputs separated. |
| `openbao-agent` / A | 5 | health token file / limits | 0085 G Common Checks: incomplete | G/R distinguish stale nonempty token from auth/renew/render, CPU1/512MiB, no HTTP/metrics listener; sanitized auth counts are bounded evidence. |
| `openbao-agent` / A | 6 | policy / unused templates / custody | 0085 P controls: incomplete | P retains no secret logging, renderer least privilege, independent rotation/cleanup approval, common backup rules; file consumption not authentication proof. |
| `openbao-agent` / A | 7 | agent lifecycle / copied config | 0085 R scattered restart delivery: incomplete | R target lifecycle plus primary SecretID delivery; existing RUN0096-session alternative explicitly separated, no duplicate minting; config recreation/hash controls linked. |
| `openbao-agent` / A | 8 | SecretID consumption / token max TTL | 0085 R Renderer delivery: consistent | Retain one-use10minute historical role contract, secure OIDC CLI delivery, success/error counts, consumed-file+timestamp checks with real auth result; add pipefail to protect pipeline status. |
| `openbao-agent` / A | 9 | derived auth/render state | 0085 R recovery: incomplete | Agent rebuild never substitutes Raft/custody restore; human reissue of required AppRole credential remains necessary, staged files cleaned under existing owner scope, outputs not generic evidence. |

### Findings, conflicts and preservation decisions

- Gateway recovery duplicates moved into their existing Runbooks. Static lint,
  readonly/tmpfs, timeouts, route checks, certificate custody, historical NOT_RUN,
  rollback and escalation substance remain; HTTP ping and placeholder claims were
  corrected rather than retained as false acceptance requirements.
- Four service Policies placed mandatory zero-failure/incident-response bullets
  under Disallowed. They now live under Required with their obligations unchanged.
- Traefik's limiter requirement remains mandatory despite missing chain membership.
  Independent pilot security review classified implementation nonconformance;
  docs explicitly do not repair or certify it.
- Default image/build details and helper differences are explicit. Nginx exact
  release remains unknowable from nginx:alpine, not retroactively filled from latest.
- GDE0079's401/403 blanket redirect and historical401 expectations differed from
  current statusRewrites. Preserve the dated rehearsal, correct current401→302 and
  unchanged403, and remove TLS-bypass probing as a current instruction. Identity
  headers alone cross the standard ForwardAuth response boundary.
- ESO three-path prose predates approved additions in owner-authored commits
  e3d811870b020fff5430a52585b8360ca21942c9 and5fb725b2aff27fde82cecd33e354ebf7457e4afe
  (2026-09-23). Completed SPEC0180 Task0008 records exact Prometheus path and
  merged Grafana PR231; owner completion is dated2026-09-24. Independent security
  review verified this provenance; POL0085 now absorbs only those exact five
  data/metadata reads. Grafana-static has no adequate explicit exception approval
  despite Task0008 S18 intent; its restrictive policy and bounded source
  nonconformance remain unchanged.
- Existing2026-09-22 single-file custody decision is preserved in Policy with all
  constraints and risk. Its missing expiry/exit are unresolved historical approval
  fields, not newly granted exceptions. No credential was inspected or changed.
- OpenBao metrics destination mode corrected to0640/SECRETS_GID, matching its own
  consumer contract and existing install command;0600 session/custody files remain.
- Source-only helper argv and missing-exporter-health limits were sent for independent
  security review. No secret exposure, actual attack or credential rotation need is
  asserted from this static audit.

### Exact artifact disposition and old-section mapping

Every original heading and its attached tables/examples/notes/links was read.
The table maps complete original sections. A same-title mapping means retained
substance with the topic-specific corrections above, not a claim that every byte
is unchanged. Child sections inherit their nearest mapped parent unless listed
separately. No role/ID/status/service-binding was removed or transferred.

| Artifact / exact existing path | Disposition | Original sections → final owner/sections |
| --- | --- | --- |
| `GDE-0011` / `docs/05.operations/guides/0011-nginx.md` | revise in place | Retained owners: Usage; Implementation Sources; Overview; Usage Type; Target Audience; Purpose; Prerequisites; Step-by-step Instructions; Common Pitfalls; Common Checks; Runbook Handoff; Traceability; Related Documents. Configuration Recovery and Upgrade → RUN-0011 Rollback or Recovery (all config/cert/canary/tmpfs instructions) |
| `GDE-0012` / `docs/05.operations/guides/0012-edge-routing-stack.md` | revise in place | Retained owners: Usage; Overview; Edge Routing Stack Usage; Common Checks; Runbook Handoff; Traceability; Related Documents.  |
| `GDE-0013` / `docs/05.operations/guides/0013-traefik.md` | revise in place | Retained owners: Usage; Implementation Sources; Overview; Usage Type; Target Audience; Purpose; Prerequisites; Step-by-step Instructions; Common Pitfalls; Common Checks; Runbook Handoff; Traceability; Related Documents. Configuration Recovery and Upgrade → RUN-0013 Rollback or Recovery (config/cert/metrics/routes/rollback) |
| `GDE-0014` / `docs/05.operations/guides/0014-keycloak.md` | revise in place | Retained owners: Usage; Implementation Sources; Overview; Usage Type; Target Audience; Purpose; Tracked Configuration Snapshot; OIDC Concepts for This Host; Step-by-step Instructions; Common Pitfalls; Common Checks; Runbook Handoff; Traceability; Related Documents. Data Protection and Upgrade → RUN-0014 Lifecycle and configuration changes + Rollback or Recovery; Guide retains data explanation |
| `GDE-0015` / `docs/05.operations/guides/0015-oauth2-proxy.md` | revise in place | Retained owners: Usage; Implementation Sources; Overview; Usage Type; Target Audience; Purpose; Prerequisites; Tracked Configuration Snapshot; Cookie, Token, and Session Distinctions; Logout Boundary; Step-by-step Instructions; Common Pitfalls; Common Checks; Runbook Handoff; Traceability; Related Documents. Session Recovery and Upgrade → RUN-0015 Lifecycle, helpers and change acceptance + Rollback or Recovery; Guide retains state explanation |
| `GDE-0079` / `docs/05.operations/guides/0079-application-auth-integration.md` | revise in place | Retained owners (Korean source headings rendered here as English glosses): Usage; Overview; Usage Type; Target Audience; Purpose; Terms and responsibilities; Authentication Pattern; Keycloak Client Matrix; Authorization Code and verification boundaries; Token, cookie and permission distinctions; Current OAuth2 Proxy boundaries; Logout and permission revocation; New application integration sequence and acceptance criteria; ForwardAuth Service Review; Kafbat UI; Airflow; Airflow failure patterns; Route Authentication Matrix; SSO Behavioural Matrix; Per-service static verification; Runbook Handoff; Common Checks; Traceability; Related Documents. Airflow / Authorization bootstrap → RUN-0014 Application authorization provisioning (tagged CLI verified); diagrams, client/RBAC tables, failure patterns, candidate cutover/history and behavioural matrix retained with current-source corrections |
| `GDE-0085` / `docs/05.operations/guides/0085-openbao.md` | revise in place | Retained owners: Usage; Implementation Sources; Common Checks; Runbook Handoff; Traceability; Related Documents.  |
| `POL-0011` / `docs/05.operations/policies/0011-nginx.md` | revise in place | Retained owners: Overview; Policy Scope; Controls; Exceptions; Verification; Recovery and Upgrade Controls; Review Cadence; Traceability; Related Documents.  |
| `POL-0013` / `docs/05.operations/policies/0013-traefik.md` | revise in place | Retained owners: Overview; Policy Scope; Controls; Exceptions; Verification; Recovery and Upgrade Controls; Review Cadence; Traceability; Related Documents.  |
| `POL-0014` / `docs/05.operations/policies/0014-keycloak.md` | revise in place | Retained owners: Overview; Policy Scope; Controls; Exceptions; Verification; Backup and Upgrade Controls; Review Cadence; Traceability; Related Documents.  |
| `POL-0015` / `docs/05.operations/policies/0015-oauth2-proxy.md` | revise in place | Retained owners: Overview; Policy Scope; Controls; Exceptions; Verification; Session and Upgrade Controls; Review Cadence; Traceability; Related Documents.  |
| `POL-0079` / `docs/05.operations/policies/0079-application-auth-integration.md` | revise in place | Retained owners: Overview; Policy Scope; Controls; Required; Disallowed; Exceptions; Verification; Review Cadence; Traceability; Related Documents.  |
| `POL-0085` / `docs/05.operations/policies/0085-openbao.md` | revise in place | Retained owners: Overview; Policy Scope; Controls; Prometheus Metrics Credential; hy-home.k8s Kubernetes Auth; Exceptions; Verification; Review Cadence; Traceability; Related Documents.  |
| `RUN-0011` / `docs/05.operations/runbooks/0011-nginx.md` | revise in place | Retained owners: Overview; Purpose; When to Use; Procedure; Evidence; Rollback or Recovery; Escalation; Traceability; Related Documents. Checklist → RUN-0011 Target and prerequisites + Static checks and diagnosis; Steps → RUN-0011 Static checks and diagnosis + Startup, shutdown and configuration change + Acceptance and stop conditions; Verification Steps → RUN-0011 Acceptance and stop conditions (HTTP versus HTTPS correction); Observability and Evidence Sources → RUN-0011 Evidence (sanitized error categories, no raw logs); Safe Rollback or Recovery Procedure → RUN-0011 Rollback or Recovery (duplicate consolidated) |
| `RUN-0013` / `docs/05.operations/runbooks/0013-traefik.md` | revise in place | Retained owners: Overview; Purpose; When to Use; Procedure; Evidence; Rollback or Recovery; Escalation; Traceability; Related Documents. Checklist → RUN-0013 Target and prerequisites + Static checks and diagnosis; Steps → RUN-0013 Static checks and diagnosis + Startup, shutdown and apply; Verification Steps → RUN-0013 Startup, shutdown and apply; Observability and Evidence Sources → RUN-0013 Evidence (sanitized signals); Safe Rollback or Recovery Procedure → RUN-0013 Rollback or Recovery (duplicate consolidated) |
| `RUN-0014` / `docs/05.operations/runbooks/0014-keycloak.md` | revise in place | Retained owners: Overview; Purpose; When to Use; Procedure; Checklist; Steps; Verification Steps; Observability and Evidence Sources; Safe Rollback or Recovery Procedure; Evidence; Rollback or Recovery; Escalation; Traceability; Related Documents.  |
| `RUN-0015` / `docs/05.operations/runbooks/0015-oauth2-proxy.md` | revise in place | Retained owners: Overview; Purpose; When to Use; Procedure; Checklist; Steps; Verification Steps; Observability and Evidence Sources; Safe Rollback or Recovery Procedure; Evidence; Shared Valkey outage rehearsal (2026-09-22, owner-approved); Rollback or Recovery; Escalation; Traceability; Related Documents.  |
| `RUN-0085` / `docs/05.operations/runbooks/0085-openbao.md` | revise in place | Retained owners: When to Use; Procedure; Initial Bootstrap and Credential Recovery; Renderer SecretID Delivery; Prometheus Metrics Credential; OIDC Configuration Contract; Human Login and Normal Root Recovery; hy-home.k8s Kubernetes Auth; No Administrative Identity: Explicit Break-glass Recovery; Evidence; Rollback or Recovery; Escalation; Traceability; Related Documents. Initial Bootstrap dated custody paragraph → POL-0085 Existing custody decision and missing closure; unseal handling retained; Prometheus block second SecretID route → Renderer delivery from an existing integration session (alternative, not consecutive execution) |

## Verification Evidence

Focused receipts on 2026-10-01 (worktree root):

- `python3 scripts/validation/check-operations-catalog.py`: exit0, PASS.
- `python3 scripts/validation/check-document-metadata.py --mode check-changed`
  with explicit `--changed-path` for every one of the19 owned files: exit0,
  selected19, violations0, legacy exceptions0, transition overrides0. Base was
  local origin/main merge-base c26bc8026254dffd7d51fc45b4081a1f80f855f2.
  Initial FAIL identified7 runtime-version literals in official tagged URLs;
  same-line compatibility evidence annotations corrected those without changing pins.
- `python3 scripts/validation/check-document-links.py --mode all`: exit0,
  documents1019, links10285 at the earlier checkpoint; final review log records
  links10286, failures0, warnings1. Existing archive warning:
  2870 legacy links have no capture source; historical resolution remains unverified.
- `bash -n` through stdin for all27 bash/sh fenced examples in the18 leaves:
  exit0 for every block, no command execution.
- `git diff --check -- <19 exact owned paths>`: exit0, no whitespace errors.
- Manual audit: eight identities times nine topics, all72 cells and every original
  section mapped; selected default/alternate OAuth2 Dockerfiles and copied sources
  inspected. Existing snapshots remain unchanged; final byte hashes and complete
  scoped diff are included in the integrator scratch review packet.

All manual matrix comparisons are source-only. No executable repository logic
changed, so new unit/integration/E2E tests and coverage are N/A. No live service,
private environment/credential, image build or stateful restore was inspected or
executed; their result is NOT_RUN, never PASS. Full changed CI gate is reserved
for the integrator's stable tree, not run concurrently by this worker.

## Review Evidence

Independent pilot security evidence for limiter/placeholder consumed from Plan.
Additional independent security review completed on2026-10-01 for ACL/custody/static
route and dedicated Valkey argv. ESO provenance verified against exact commits
and completed Spec/Task; custody remains Important residual risk, static route and
argv remain Minor source findings without observed exploit/secret disclosure.
The grafana-static finding is bounded to the exact Grafana Host and two Paths,
priority200/grafana-svc, LAN/TLS exposure and all-method/no-chain source semantics;
its name-only test does not fix that rule. No wider exposure was observed. ESO
source authorization does not prove live roles or exact allowlist regression tests;
the one authenticated principal's compromise affects all five entries. The Valkey
server/exporter/probe argv trust boundary excludes full inspect, top/ps/proc and raw
health-log evidence. Implementation remediation and current runtime validation
remain outside this wave.
At the pre-review author checkpoint final semantic/rules review was PENDING.
The independent W3 receipt below supersedes that checkpoint; full Spec acceptance
remains the responsibility of W8.

### Independent W3 review receipt

Reviewer `/root/ops_w3_rules_review` on 2026-10-01: specification compliance
PASS; task quality PASS WITH ONE MINOR CORRECTION; approve with follow-up,
no blocker to W4. All 19 file hashes, 72 service-topic cells and 18 preservation
mappings were checked. Policy provenance and source nonconformance distinctions
were independently confirmed. W3 complete (uncommitted task-scoped snapshot;
no material findings). Minor closed during W8 receipt reconciliation: Verification Evidence distinguishes
the earlier10,285-link and final10,286-link receipts after one valid added link.
Full changed-profile and terminal acceptance remain W8 responsibilities; hosted
CI and operational checks are not claimed by this task-scoped content verdict.

## Commit Ledger

No W3 staging or commit by the worker. Parent staged this newly created Task for
checker discovery; existing18 leaves were already tracked. Before snapshots were
preserved before first mutation. Integrator owns review, staging and delivery.

## Deferred Items

Separate implementation/approval decisions: missing limiter membership, placeholder
access-phase design, Nginx HTTP health/route compatibility and exact image identity,
exporter health/credential argv exposure, static-route policy mismatch, missing
custody expiry/exit and all current runtime/canary/isolated stateful recovery evidence.
No missing capability was invented to close a matrix cell. Package README/source
wording outside these18 leaves may still overstate Nginx auth/health and Traefik403
redirect behavior; integrator must route those outside-scope findings explicitly.
